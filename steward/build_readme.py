#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse


Gh = Callable[[tuple[str, ...]], object]

START = "<!-- recent_receipts starts -->"
END = "<!-- recent_receipts ends -->"
_PIN_COUNT = 6
_PIN_PATTERN = re.compile(r"mrodgersjs-web/[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")


class BuildError(RuntimeError):
    """An input or provider error that makes a README refresh unsafe."""


def load_pins(path: Path) -> tuple[str, ...]:
    """Load the canonical public pin order and reject unsafe input."""
    try:
        pins = tuple(path.read_text(encoding="utf-8").splitlines())
    except OSError as exc:
        raise BuildError(f"cannot read {path}") from exc

    if len(pins) != _PIN_COUNT:
        raise BuildError(f"{path} must contain exactly {_PIN_COUNT} pins")
    if any(not pin or pin != pin.strip() or not _PIN_PATTERN.fullmatch(pin) for pin in pins):
        raise BuildError(f"{path} contains a malformed pin")
    if len(set(pins)) != len(pins):
        raise BuildError(f"{path} contains a duplicate pin")
    return pins


PINNED_REPOS = load_pins(Path(__file__).with_name("PINNED.txt"))


def _required_text(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value
        or value != value.strip()
        or "\n" in value
        or "\r" in value
    ):
        raise BuildError(f"{label} must be a nonempty string")
    return value


def _calendar_date(value: object, label: str) -> str:
    text = _required_text(value, label)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise BuildError(f"{label} must be an ISO calendar date")
    try:
        parsed = date.fromisoformat(text)
    except ValueError as exc:
        raise BuildError(f"{label} must be an ISO calendar date") from exc
    if parsed.isoformat() != text:
        raise BuildError(f"{label} must be an ISO calendar date")
    return text


def _timestamp_date(value: object, label: str) -> str:
    text = _required_text(value, label)
    if "T" not in text:
        raise BuildError(f"{label} must be an ISO timestamp")
    try:
        parsed = datetime.fromisoformat(
            f"{text[:-1]}+00:00" if text.endswith("Z") else text
        )
    except ValueError as exc:
        raise BuildError(f"{label} must be an ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise BuildError(f"{label} must include a timezone")
    return parsed.date().isoformat()


def _github_url(value: object, label: str, repo: str, route: str) -> str:
    text = _required_text(value, label)
    try:
        parsed = urlparse(text)
        hostname = parsed.hostname
    except ValueError as exc:
        raise BuildError(f"{label} must be a public GitHub URL") from exc

    prefix = f"/{repo}/{route}/"
    route_value = parsed.path[len(prefix) :] if parsed.path.startswith(prefix) else ""
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or hostname != "github.com"
        or parsed.username is not None
        or parsed.password is not None
        or not route_value
        or parsed.params
        or parsed.query
        or parsed.fragment
        or (route == "actions/runs" and not route_value.isdigit())
    ):
        raise BuildError(f"{label} must match https://github.com/{repo}/{route}/...")
    return text


def _decode_json(raw: str, label: str) -> object:
    def reject_constant(value: str) -> object:
        raise ValueError(f"invalid JSON constant {value}")

    try:
        return json.loads(raw, parse_constant=reject_constant)
    except (json.JSONDecodeError, ValueError) as exc:
        raise BuildError(f"{label} is not valid JSON") from exc


def _parse_scoreboard(raw: object) -> dict[str, object]:
    """Validate and normalize a present scoreboard payload."""
    if not isinstance(raw, dict):
        raise BuildError("scoreboard root must be an object")

    measured = _calendar_date(raw.get("date"), "scoreboard date")
    summary = raw.get("summary")
    if not isinstance(summary, dict):
        raise BuildError("scoreboard summary must be an object")

    counts: dict[str, int] = {}
    for name in ("total", "green", "red"):
        value = summary.get(name)
        if type(value) is not int:
            raise BuildError(f"scoreboard summary.{name} must be an integer")
        counts[name] = value

    if counts["total"] != 100:
        raise BuildError("scoreboard summary.total must equal 100")
    if counts["green"] < 0 or counts["red"] < 0:
        raise BuildError("scoreboard counts must be nonnegative")
    if counts["green"] + counts["red"] != counts["total"]:
        raise BuildError("scoreboard green and red counts must equal total")
    if not isinstance(raw.get("criteria"), list):
        raise BuildError("scoreboard criteria must be a list")

    return {"date": measured, **counts}


def load_scoreboard(path: Path) -> dict[str, object] | None:
    """Return no measurement for absence; reject every malformed present file."""
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeError) as exc:
        raise BuildError(f"cannot read {path}") from exc
    return _parse_scoreboard(_decode_json(raw, str(path)))


def gh_json(args: tuple[str, ...]) -> object:
    """Run one argv-form GitHub CLI query and decode its JSON response."""
    try:
        repo = args[args.index("--repo") + 1]
    except (ValueError, IndexError):
        repo = "GitHub"
    operation = " ".join(args[:2]) or "query"
    context = f"{repo}: {operation}"

    try:
        completed = subprocess.run(
            ("gh", *args),
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError as exc:
        raise BuildError(f"{context}: gh executable not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise BuildError(f"{context}: GitHub query timed out") from exc
    except subprocess.CalledProcessError as exc:
        raise BuildError(f"{context}: GitHub query failed") from exc
    except (OSError, UnicodeError) as exc:
        raise BuildError(f"{context}: GitHub query could not run") from exc

    payload = _decode_json(completed.stdout, context)
    if not isinstance(payload, (dict, list)):
        raise BuildError(f"{context}: unexpected JSON shape")
    return payload


def _one_row(payload: object, repo: str, operation: str) -> Mapping[str, object] | None:
    if not isinstance(payload, list) or len(payload) > 1:
        raise BuildError(f"{repo}: {operation} returned an unexpected JSON shape")
    if not payload:
        return None
    row = payload[0]
    if not isinstance(row, dict):
        raise BuildError(f"{repo}: {operation} returned a malformed row")
    return row


def _collect_release(repo: str, gh: Gh) -> dict[str, object] | None:
    listed = _one_row(
        gh(
            (
                "release",
                "list",
                "--repo",
                repo,
                "--exclude-drafts",
                "--limit",
                "1",
                "--json",
                "name,tagName,publishedAt",
            )
        ),
        repo,
        "release list",
    )
    if listed is None:
        return None

    tag = _required_text(listed.get("tagName"), f"{repo} release tag")
    listed_date = _timestamp_date(
        listed.get("publishedAt"), f"{repo} release publishedAt"
    )
    viewed = gh(
        (
            "release",
            "view",
            "--repo",
            repo,
            "--json",
            "tagName,publishedAt,url",
            "--",
            tag,
        )
    )
    if not isinstance(viewed, dict):
        raise BuildError(f"{repo}: release view returned an unexpected JSON shape")

    viewed_tag = _required_text(viewed.get("tagName"), f"{repo} release tag")
    viewed_date = _timestamp_date(
        viewed.get("publishedAt"), f"{repo} release publishedAt"
    )
    if viewed_tag != tag or viewed_date != listed_date:
        raise BuildError(f"{repo}: release list and release view disagree")
    return {
        "tag": viewed_tag,
        "date": viewed_date,
        "url": _github_url(
            viewed.get("url"), f"{repo} release URL", repo, "releases/tag"
        ),
    }


def _collect_smoke(repo: str, gh: Gh) -> dict[str, object] | None:
    row = _one_row(
        gh(
            (
                "run",
                "list",
                "--repo",
                repo,
                "--all",
                "--workflow",
                "smoke.yml",
                "--branch",
                "main",
                "--limit",
                "1",
                "--json",
                "conclusion,headSha,status,updatedAt,url",
            )
        ),
        repo,
        "run list",
    )
    if row is None:
        return None

    status = _required_text(row.get("status"), f"{repo} smoke status")
    conclusion = row.get("conclusion")
    if conclusion is not None and not isinstance(conclusion, str):
        raise BuildError(f"{repo} smoke conclusion must be a string or null")
    state = (
        _required_text(conclusion, f"{repo} smoke conclusion")
        if status == "completed"
        else status
    )
    sha = _required_text(row.get("headSha"), f"{repo} smoke SHA")
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", sha):
        raise BuildError(f"{repo} smoke SHA must be hexadecimal")
    return {
        "state": state,
        "date": _timestamp_date(row.get("updatedAt"), f"{repo} smoke updatedAt"),
        "sha": sha,
        "url": _github_url(
            row.get("url"), f"{repo} smoke URL", repo, "actions/runs"
        ),
    }


def collect_receipts(
    gh: Gh = gh_json,
) -> tuple[dict[str, object], ...]:
    """Collect normalized release and smoke rows in canonical pin order."""
    return tuple(
        {
            "repo": repo,
            "release": _collect_release(repo, gh),
            "smoke": _collect_smoke(repo, gh),
        }
        for repo in PINNED_REPOS
    )


def _escape_markdown_text(value: str) -> str:
    escaped = value.replace("\\", "\\\\")
    for character in ("`", "*", "_", "[", "]", "|"):
        escaped = escaped.replace(character, f"\\{character}")
    return escaped


def _normalized_scoreboard(scoreboard: Mapping[str, object]) -> tuple[str, int]:
    measured = _calendar_date(scoreboard.get("date"), "scoreboard date")
    counts: dict[str, int] = {}
    for name in ("total", "green", "red"):
        value = scoreboard.get(name)
        if type(value) is not int:
            raise BuildError(f"scoreboard {name} must be an integer")
        counts[name] = value
    if (
        counts["total"] != 100
        or counts["green"] < 0
        or counts["red"] < 0
        or counts["green"] + counts["red"] != counts["total"]
    ):
        raise BuildError("scoreboard counts are inconsistent")
    return measured, counts["green"]


def _release_cell(repo: str, release: object) -> str:
    if release is None:
        return "no release"
    if not isinstance(release, Mapping):
        raise BuildError(f"{repo} release must be an object or null")
    tag = _required_text(release.get("tag"), f"{repo} release tag")
    published = _calendar_date(release.get("date"), f"{repo} release date")
    url = _github_url(
        release.get("url"), f"{repo} release URL", repo, "releases/tag"
    )
    return f"[{_escape_markdown_text(tag)}]({url}) · `{published}`"


def _smoke_cell(repo: str, smoke: object) -> str:
    if smoke is None:
        return "no smoke run"
    if not isinstance(smoke, Mapping):
        raise BuildError(f"{repo} smoke must be an object or null")
    state = _required_text(smoke.get("state"), f"{repo} smoke state")
    updated = _calendar_date(smoke.get("date"), f"{repo} smoke date")
    sha = _required_text(smoke.get("sha"), f"{repo} smoke SHA")
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", sha):
        raise BuildError(f"{repo} smoke SHA must be hexadecimal")
    url = _github_url(smoke.get("url"), f"{repo} smoke URL", repo, "actions/runs")
    return f"[{state}]({url}) · `{updated}` · `{sha[:7]}`"


def render_recent_receipts(
    scoreboard: Mapping[str, object] | None,
    receipts: Sequence[Mapping[str, object]],
) -> str:
    """Render deterministic receipt Markdown from normalized inputs."""
    if isinstance(receipts, (str, bytes)):
        raise BuildError("receipts must be an ordered sequence")
    if any(not isinstance(row, Mapping) for row in receipts):
        raise BuildError("every receipt must be an object")
    repos = tuple(row.get("repo") for row in receipts)
    if repos != PINNED_REPOS:
        raise BuildError("receipt repositories must match PINNED.txt order")

    if scoreboard is None:
        score_line = "Steward score. **not measured**"
    elif isinstance(scoreboard, Mapping):
        measured, green = _normalized_scoreboard(scoreboard)
        score_line = f"Steward score. **{green}/100 green**. Measured `{measured}`."
    else:
        raise BuildError("scoreboard must be an object or null")

    lines = [
        score_line,
        "",
        "| Pinned system | Latest release | Latest smoke run |",
        "| --- | --- | --- |",
    ]
    for repo, row in zip(PINNED_REPOS, receipts):
        name = repo.rsplit("/", 1)[1]
        lines.append(
            f"| [{name}](https://github.com/{repo})"
            f" | {_release_cell(repo, row.get('release'))}"
            f" | {_smoke_cell(repo, row.get('smoke'))} |"
        )
    return "\n".join(lines)


def _marker_indices(source: str) -> tuple[int, int]:
    if source.count(START) != 1 or source.count(END) != 1:
        raise BuildError("README must contain exactly one receipt marker pair")
    start = source.index(START)
    end = source.index(END)
    if start >= end:
        raise BuildError("receipt markers are out of order")

    def standalone(index: int, marker: str) -> bool:
        before = index == 0 or source[index - 1] == "\n"
        after = index + len(marker)
        line_end = (
            after == len(source)
            or source.startswith("\n", after)
            or source.startswith("\r\n", after)
        )
        return before and line_end

    if not standalone(start, START) or not standalone(end, END):
        raise BuildError("receipt markers must each occupy a standalone line")
    return start + len(START), end


def replace_recent_receipts(source: str, body: str) -> str:
    """Replace the interior of exactly one standalone receipt marker pair."""
    if not isinstance(source, str) or not isinstance(body, str):
        raise BuildError("README source and receipt body must be text")
    if (
        not body
        or body.startswith(("\n", "\r"))
        or body.endswith(("\n", "\r"))
        or "\r" in body
        or START in body
        or END in body
    ):
        raise BuildError("receipt body violates the renderer contract")
    start_after, end = _marker_indices(source)
    return f"{source[:start_after]}\n{body}\n{source[end:]}"


def _atomic_write(path: Path, data: bytes, mode: int) -> None:
    temporary: str | None = None
    try:
        descriptor, temporary = tempfile.mkstemp(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
        temporary = None
    except OSError as exc:
        raise BuildError(f"cannot update {path}") from exc
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass


def build_readme(root: Path, gh: Gh = gh_json) -> bool:
    """Refresh README.md transactionally; return whether its bytes changed."""
    readme_path = root / "README.md"
    try:
        with readme_path.open("rb") as handle:
            original = handle.read()
            mode = stat.S_IMODE(os.fstat(handle.fileno()).st_mode)
    except OSError as exc:
        raise BuildError(f"cannot read {readme_path}") from exc
    try:
        source = original.decode("utf-8")
    except UnicodeError as exc:
        raise BuildError(f"{readme_path} is not valid UTF-8") from exc

    _marker_indices(source)
    pins = load_pins(root / "steward" / "PINNED.txt")
    if pins != PINNED_REPOS:
        raise BuildError("PINNED.txt does not match the canonical public order")
    scoreboard = load_scoreboard(root / "steward" / "scoreboard" / "latest.json")
    receipts = collect_receipts(gh)
    body = render_recent_receipts(scoreboard, receipts)
    candidate = replace_recent_receipts(source, body).encode("utf-8")
    if candidate == original:
        return False
    _atomic_write(readme_path, candidate, mode)
    return True


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    try:
        changed = build_readme(root)
    except BuildError as exc:
        print(f"build_readme: {exc}", file=sys.stderr)
        return 1
    print("README.md updated" if changed else "README.md unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
