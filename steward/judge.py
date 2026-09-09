#!/usr/bin/env python3
"""Judge only the five LLM criteria with local-first model routing."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

if __package__:
    from steward.score_github import (
        ScoringContext,
        criteria_sha256,
        load_criteria,
        write_scoreboard,
    )
else:
    from score_github import (
        ScoringContext,
        criteria_sha256,
        load_criteria,
        write_scoreboard,
    )


FALLBACK_PAID = "FALLBACK_PAID"
SSH_HOST = "rig128gb"
Run = Callable[[tuple[str, ...], Optional[str]], subprocess.CompletedProcess[str]]
Emit = Callable[[str], None]


class JudgeError(RuntimeError):
    """A malformed scoreboard or local judge response."""


def run_command(
    argv: tuple[str, ...],
    input_text: Optional[str] = None,
) -> subprocess.CompletedProcess[str]:
    """Run one bounded local or SSH model command."""
    try:
        return subprocess.run(
            argv,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=180,
            env={**os.environ, "OLLAMA_NOHISTORY": "1"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(argv, 127, "", str(exc))


def first_model(output: str) -> Optional[str]:
    """Return the first model name from ollama list output."""
    if not isinstance(output, str):
        raise JudgeError("ollama list output must be text")
    rows = [line.split() for line in output.splitlines() if line.strip()]
    if not rows:
        return None
    if rows[0] and rows[0][0].upper() == "NAME":
        rows = rows[1:]
    if not rows:
        return None
    model = rows[0][0]
    if not model or model.startswith("-") or any(character.isspace() for character in model):
        raise JudgeError("ollama returned an invalid model name")
    return model


def _probe(run: Run, argv: tuple[str, ...]) -> Optional[str]:
    try:
        result = run(argv)
    except Exception:
        return None
    if result.returncode != 0:
        return None
    try:
        return first_model(result.stdout)
    except JudgeError:
        return None


def select_backend(run: Run = run_command) -> Optional[tuple[str, str]]:
    """Probe local Ollama first, then the 128GB SSH host."""
    local = _probe(run, ("ollama", "list"))
    if local:
        return "local", local
    remote = _probe(run, ("ssh", SSH_HOST, "ollama", "list"))
    if remote:
        return "remote", remote
    return None


def validate_scoreboard(
    scoreboard: Mapping[str, object],
    criteria: Sequence[Mapping[str, object]],
    digest: str,
    *,
    today: object,
) -> Mapping[str, object]:
    """Bind a scoreboard to the current ordered criteria before judging rows."""
    if not isinstance(scoreboard, Mapping) or scoreboard.get("schema") != 1:
        raise JudgeError("scoreboard schema must equal 1")
    if scoreboard.get("criteria_sha256") != digest:
        raise JudgeError("scoreboard criteria hash is stale")
    expected_date = today.isoformat() if hasattr(today, "isoformat") else None
    if scoreboard.get("date") != expected_date:
        raise JudgeError("scoreboard is not for the current UTC date")
    generated_at = scoreboard.get("generated_at")
    if not isinstance(generated_at, str) or not generated_at.endswith("Z"):
        raise JudgeError("scoreboard generated_at must be a UTC timestamp")

    rows = scoreboard.get("criteria")
    if (
        not isinstance(rows, list)
        or len(rows) != len(criteria)
        or any(not isinstance(row, Mapping) for row in rows)
    ):
        raise JudgeError("scoreboard criteria do not match the current registry")
    expected_ids = [str(row.get("id")) for row in criteria]
    actual_ids = [str(row.get("id")) for row in rows]
    if actual_ids != expected_ids or len(set(actual_ids)) != len(actual_ids):
        raise JudgeError("scoreboard criterion ids are reordered or duplicated")

    statuses = []
    for definition, row in zip(criteria, rows):
        if set(row) != {"id", "check", "description", "status", "evidence"}:
            raise JudgeError(
                f"scoreboard row fields drift for {definition.get('id')}"
            )
        if row.get("check") != definition.get("check"):
            raise JudgeError(f"scoreboard check drift for {definition.get('id')}")
        if row.get("description") != definition.get("description"):
            raise JudgeError(
                f"scoreboard description drift for {definition.get('id')}"
            )
        status = row.get("status")
        if definition.get("check") == "llm":
            if status not in ("green", "red", None):
                raise JudgeError(f"invalid LLM status for {definition.get('id')}")
        elif status not in ("green", "red"):
            raise JudgeError(
                f"deterministic criterion {definition.get('id')} must be resolved"
            )
        evidence = row.get("evidence")
        if status is None:
            if evidence is not None:
                raise JudgeError(f"null criterion {definition.get('id')} has evidence")
        elif not isinstance(evidence, str) or not evidence.strip():
            raise JudgeError(f"resolved criterion {definition.get('id')} lacks evidence")
        statuses.append(status)

    expected_summary = {
        "total": len(rows),
        "green": statuses.count("green"),
        "red": statuses.count("red"),
        "null": statuses.count(None),
    }
    if scoreboard.get("summary") != expected_summary:
        raise JudgeError("scoreboard summary is inconsistent with criterion statuses")
    return scoreboard


def pending_llm_rows(
    criteria: Sequence[Mapping[str, object]],
    scoreboard: Mapping[str, object],
) -> tuple[dict[str, object], ...]:
    """Return only null scoreboard rows whose criteria check is llm."""
    score_rows = scoreboard.get("criteria")
    if not isinstance(score_rows, list) or any(
        not isinstance(row, Mapping) for row in score_rows
    ):
        raise JudgeError("scoreboard criteria must be a list of objects")
    by_id = {str(row.get("id")): row for row in score_rows}
    pending: list[dict[str, object]] = []
    for definition in criteria:
        if definition.get("check") != "llm":
            continue
        identifier = str(definition.get("id"))
        score_row = by_id.get(identifier)
        if score_row is None:
            raise JudgeError(f"scoreboard is missing LLM criterion {identifier}")
        if score_row.get("status") is None:
            pending.append({**dict(score_row), **dict(definition)})
    return tuple(pending)


def _load_scoreboard(path: Path) -> dict[str, object]:
    try:
        raw = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"invalid constant {value}")
            ),
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise JudgeError(f"cannot read a valid scoreboard at {path}") from exc
    if not isinstance(raw, dict) or raw.get("schema") != 1:
        raise JudgeError("scoreboard schema must equal 1")
    rows = raw.get("criteria")
    if not isinstance(rows, list) or len(rows) != 100:
        raise JudgeError("scoreboard must contain exactly 100 criterion rows")
    if any(not isinstance(row, dict) for row in rows):
        raise JudgeError("scoreboard criterion rows must be objects")
    return raw


def _llm_context(identifier: str, context: ScoringContext) -> object:
    if identifier == "how-it-works-visual":
        return [
            {
                "repo": name,
                "image_references": re_find_images(readme),
            }
            for name, readme in context.all_readmes()
        ]
    if identifier == "no-false-e2e":
        return [
            {
                "repo": name,
                "e2e_lines": [
                    line[:500]
                    for line in readme.splitlines()
                    if "e2e" in line.lower()
                ][:20],
                "workflows": [
                    str(row.get("path") or row.get("name") or "")
                    for row in context.workflows(name)
                ],
            }
            for name, readme in context.all_readmes()
        ]
    if identifier == "details-collapse":
        return [
            {
                "repo": name,
                "line_count": len(readme.splitlines()),
                "has_details": "<details" in readme.lower(),
            }
            for name, readme in context.all_readmes()
        ]
    if identifier == "planted-failure-docs":
        readme = context.readme("rigforge")
        return {
            "repo": "rigforge",
            "matching_lines": [
                line[:500]
                for line in readme.splitlines()
                if "planted failure" in line.lower() or "proofpacket" in line.lower()
            ][:30],
        }
    if identifier == "pin-narrative":
        return {"pins": list(context.pins())}
    raise JudgeError(f"unsupported LLM criterion {identifier}")


def re_find_images(readme: str) -> list[str]:
    import re

    references = re.findall(
        r"(?:src=[\"']|!\[[^]]*\]\()([^\"')]+)", readme, re.IGNORECASE
    )
    return references[:30]


def _prompt(row: Mapping[str, object], evidence: object) -> str:
    return json.dumps(
        {
            "instruction": (
                "Judge only the named criterion against the supplied public evidence. "
                "Return exactly one JSON object with keys status and evidence. status must "
                "be green or red; evidence must be a concise factual explanation."
            ),
            "criterion": {
                "id": row.get("id"),
                "description": row.get("description"),
                "target": row.get("target"),
                "pass_rule": row.get("pass_rule"),
            },
            "public_evidence": evidence,
        },
        ensure_ascii=False,
        sort_keys=True,
    )


def _parse_judgment(output: str) -> tuple[str, str]:
    if not isinstance(output, str) or not output.strip():
        raise JudgeError("local judge returned no output")
    try:
        payload = json.loads(
            output.strip(),
            parse_constant=lambda value: (_ for _ in ()).throw(
                ValueError(f"invalid constant {value}")
            ),
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise JudgeError("local judge must return one strict JSON object") from exc
    if not isinstance(payload, dict) or set(payload) != {"status", "evidence"}:
        raise JudgeError("local judge JSON must contain only status and evidence")
    status = payload.get("status")
    evidence = payload.get("evidence")
    if status not in ("green", "red"):
        raise JudgeError("local judge status must be green or red")
    if not isinstance(evidence, str) or not evidence.strip() or len(evidence) > 2000:
        raise JudgeError("local judge evidence must be 1 to 2000 characters")
    return status, evidence.strip()


def _model_argv(backend: str, model: str) -> tuple[str, ...]:
    if backend == "local":
        return "ollama", "run", model
    if backend == "remote":
        return "ssh", SSH_HOST, "ollama", "run", model
    raise JudgeError(f"unknown model backend {backend}")


def _run_judgments(
    pending: Sequence[Mapping[str, object]],
    context: ScoringContext,
    backend: tuple[str, str],
    run: Run,
) -> dict[str, tuple[str, str]]:
    location, model = backend
    results: dict[str, tuple[str, str]] = {}
    for row in pending:
        identifier = str(row["id"])
        prompt = _prompt(row, _llm_context(identifier, context))
        try:
            completed = run(_model_argv(location, model), prompt)
        except Exception as exc:
            raise JudgeError(f"{location} model execution failed") from exc
        if completed.returncode != 0:
            raise JudgeError(f"{location} model execution failed")
        results[identifier] = _parse_judgment(completed.stdout)
    return results


def _remote_backend(run: Run) -> Optional[tuple[str, str]]:
    model = _probe(run, ("ssh", SSH_HOST, "ollama", "list"))
    return ("remote", model) if model else None


def judge(
    root: Path,
    *,
    run: Run = run_command,
    emit: Emit = print,
) -> bool:
    """Judge pending LLM rows, or emit FALLBACK_PAID without writing."""
    backend = select_backend(run)
    if backend is None:
        emit(FALLBACK_PAID)
        return False

    criteria_path = root / "steward" / "criteria.yaml"
    criteria = load_criteria(criteria_path)
    latest_path = root / "steward" / "scoreboard" / "latest.json"
    scoreboard = validate_scoreboard(
        _load_scoreboard(latest_path),
        criteria,
        criteria_sha256(criteria_path),
        today=datetime.now(timezone.utc).date(),
    )
    pending = pending_llm_rows(criteria, scoreboard)
    if not pending:
        return True
    context = ScoringContext(root, datetime.now(timezone.utc))

    try:
        judgments = _run_judgments(pending, context, backend, run)
    except JudgeError:
        if backend[0] != "local":
            emit(FALLBACK_PAID)
            return False
        remote = _remote_backend(run)
        if remote is None:
            emit(FALLBACK_PAID)
            return False
        try:
            judgments = _run_judgments(pending, context, remote, run)
        except JudgeError:
            emit(FALLBACK_PAID)
            return False

    updated = json.loads(json.dumps(scoreboard))
    rows = updated["criteria"]
    for row in rows:
        identifier = str(row.get("id"))
        if identifier in judgments:
            row["status"], row["evidence"] = judgments[identifier]
    statuses = [row.get("status") for row in rows]
    if any(status not in ("green", "red", None) for status in statuses):
        raise JudgeError("judge produced an invalid scoreboard status")
    updated["summary"] = {
        "total": 100,
        "green": statuses.count("green"),
        "red": statuses.count("red"),
        "null": statuses.count(None),
    }
    updated["generated_at"] = (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )
    write_scoreboard(root, updated)
    emit(json.dumps(updated["summary"], sort_keys=True))
    return True


def main(argv: Optional[list[str]] = None) -> int:
    if argv:
        raise JudgeError("judge.py accepts no arguments")
    root = Path(__file__).resolve().parents[1]
    return 0 if judge(root) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
