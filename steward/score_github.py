#!/usr/bin/env python3
"""Score the public GitHub FDE surface against the steward criteria."""
from __future__ import annotations

import argparse
import ast
import base64
import binascii
import hashlib
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping, Sequence
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

if __package__:
    from steward.catalog_mcp import NotFoundError, gh_api, regular_file
else:
    from catalog_mcp import NotFoundError, gh_api, regular_file


OWNER = "mrodgersjs-web"
PROFILE_REPO = "mrodgersjs-web"
CHECKS = frozenset({"gh", "file", "http", "regex", "llm"})
PLANTS = ("missing-license",)
LLM_ORDINALS = (33, 42, 46, 63, 83)
BASELINE_TOPICS = frozenset(
    {
        "ai-agents",
        "forward-deployed-engineer",
        "llm",
        "agent-governance",
        "proof-gates",
        "evals",
        "mlops",
    }
)
Evaluator = Callable[[Mapping[str, object]], tuple[bool, str]]


LANGUAGE_BADGES = frozenset(
    {
        "c",
        "c#",
        "c++",
        "css",
        "dart",
        "elixir",
        "fortran",
        "go",
        "html",
        "java",
        "javascript",
        "julia",
        "kotlin",
        "lua",
        "objective-c",
        "php",
        "python",
        "r",
        "ruby",
        "rust",
        "scala",
        "shell",
        "swift",
        "typescript",
    }
)

class ScoreError(RuntimeError):
    """A malformed criterion or incomplete scoring run."""


def _yaml_scalar(raw: str, line_number: int) -> object:
    raw = raw.strip()
    if re.fullmatch(r"[0-9]+", raw):
        return int(raw)
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    raise ScoreError(
        f"criteria.yaml line {line_number} must use an integer or single-quoted scalar"
    )


def load_criteria(path: Path) -> tuple[dict[str, object], ...]:
    """Parse and validate the constrained stdlib-only criteria YAML."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        raise ScoreError(f"cannot read {path}") from exc
    if not lines or lines[0] != "criteria:":
        raise ScoreError("criteria.yaml must begin with criteria:")

    rows: list[dict[str, object]] = []
    current: Optional[dict[str, object]] = None
    item_pattern = re.compile(r"  - id:\s*(.+)")
    field_pattern = re.compile(r"    ([a-z_]+):\s*(.+)")
    for line_number, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue
        item_match = item_pattern.fullmatch(line)
        if item_match:
            if current is not None:
                rows.append(current)
            current = {"id": _yaml_scalar(item_match.group(1), line_number)}
            continue
        field_match = field_pattern.fullmatch(line)
        if current is None or field_match is None:
            raise ScoreError(f"criteria.yaml line {line_number} is malformed")
        key = field_match.group(1)
        if key in current:
            raise ScoreError(f"criteria.yaml line {line_number} duplicates {key}")
        current[key] = _yaml_scalar(field_match.group(2), line_number)
    if current is not None:
        rows.append(current)

    required = {"id", "check", "target", "pass_rule", "description"}
    if len(rows) != 100:
        raise ScoreError("criteria.yaml must contain exactly 100 criteria")
    identifiers: list[str] = []
    for ordinal, row in enumerate(rows, start=1):
        if set(row) != required:
            missing = sorted(required - set(row))
            extra = sorted(set(row) - required)
            raise ScoreError(
                f"criterion {ordinal} has missing fields {missing} and extra fields {extra}"
            )
        identifier = row["id"]
        if not isinstance(identifier, str) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", identifier
        ):
            raise ScoreError(f"criterion {ordinal} has an invalid id")
        if row["check"] not in CHECKS:
            raise ScoreError(f"criterion {ordinal} has an unknown check")
        for key in ("target", "pass_rule", "description"):
            if not isinstance(row[key], str) or not row[key].strip():
                raise ScoreError(f"criterion {ordinal} has an empty {key}")
        identifiers.append(identifier)
    if len(set(identifiers)) != len(identifiers):
        raise ScoreError("criteria.yaml contains duplicate ids")
    llm_ordinals = tuple(
        ordinal
        for ordinal, row in enumerate(rows, start=1)
        if row["check"] == "llm"
    )
    if llm_ordinals != LLM_ORDINALS:
        raise ScoreError(
            "only criteria 33, 42, 46, 63, and 83 may use the llm check"
        )
    return tuple(rows)


def criteria_sha256(path: Path) -> str:
    """Return the SHA-256 digest of the exact criteria bytes."""
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise ScoreError(f"cannot hash {path}") from exc


def evaluate_criteria(
    criteria: Sequence[Mapping[str, object]],
    evaluator: Evaluator,
    *,
    plant: str | None = None,
) -> tuple[dict[str, object], ...]:
    """Evaluate deterministic rows and leave LLM rows null."""
    if plant not in (None, *PLANTS):
        raise ScoreError(f"unknown planted failure: {plant}")
    rows: list[dict[str, object]] = []
    for definition in criteria:
        identifier = str(definition["id"])
        check = str(definition["check"])
        if check == "llm":
            passed: Optional[bool] = None
            evidence: Optional[str] = None
        else:
            try:
                passed, evidence_value = evaluator(definition)
                if type(passed) is not bool or not isinstance(evidence_value, str):
                    raise ScoreError("checker returned an invalid result")
                evidence = evidence_value.strip() or "check completed without detail"
            except Exception as exc:  # one failed provider read is one red row
                passed = False
                evidence = (
                    f"{type(exc).__name__}: {exc}. Resolve the check input or provider "
                    "access, then rerun the steward."
                )
        if plant == "missing-license" and identifier == "every-license":
            passed = False
            evidence = "PLANTED: simulated one missing LICENSE in memory; no repository changed."
        rows.append(
            {
                "id": identifier,
                "check": check,
                "description": str(definition["description"]),
                "status": None if passed is None else ("green" if passed else "red"),
                "evidence": evidence,
            }
        )
    return tuple(rows)


def build_scoreboard(
    digest: str,
    rows: Sequence[Mapping[str, object]],
    now: datetime,
) -> dict[str, object]:
    """Build the normalized 100-row scoreboard payload."""
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise ScoreError("criteria digest must be a lowercase SHA-256")
    if len(rows) != 100:
        raise ScoreError("scoreboard requires exactly 100 criterion rows")
    statuses = [row.get("status") for row in rows]
    if any(status not in ("green", "red", None) for status in statuses):
        raise ScoreError("criterion status must be green, red, or null")
    identifiers = [row.get("id") for row in rows]
    if len(set(identifiers)) != 100:
        raise ScoreError("scoreboard criterion ids must be unique")
    if now.tzinfo is None:
        raise ScoreError("scoreboard time must be timezone-aware")
    utc = now.astimezone(timezone.utc).replace(microsecond=0)
    normalized_rows = [dict(row) for row in rows]
    return {
        "schema": 1,
        "date": utc.date().isoformat(),
        "generated_at": utc.isoformat().replace("+00:00", "Z"),
        "criteria_sha256": digest,
        "summary": {
            "total": 100,
            "green": statuses.count("green"),
            "red": statuses.count("red"),
            "null": statuses.count(None),
        },
        "criteria": normalized_rows,
    }


def _json_bytes(value: Mapping[str, object]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = 0o644
    try:
        if path.exists():
            mode = stat.S_IMODE(path.stat().st_mode)
        descriptor, temporary = tempfile.mkstemp(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
        )
    except OSError as exc:
        raise ScoreError(f"cannot stage {path}") from exc
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except OSError as exc:
        raise ScoreError(f"cannot atomically write {path}") from exc
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def _badge(scoreboard: Mapping[str, object]) -> dict[str, object]:
    summary = scoreboard.get("summary")
    if not isinstance(summary, Mapping):
        raise ScoreError("scoreboard summary is missing")
    green = summary.get("green")
    red = summary.get("red")
    null = summary.get("null")
    if not all(type(value) is int for value in (green, red, null)):
        raise ScoreError("scoreboard summary counts are malformed")
    color = "brightgreen" if green == 100 else ("red" if red else "yellow")
    return {
        "schemaVersion": 1,
        "label": "steward",
        "message": f"{green}/100",
        "color": color,
    }


def write_scoreboard(
    root: Path,
    scoreboard: Mapping[str, object],
) -> tuple[Path, Path, Path]:
    """Atomically write the dated, latest, and Shields JSON outputs."""
    measured = scoreboard.get("date")
    if not isinstance(measured, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", measured
    ):
        raise ScoreError("scoreboard date is malformed")
    directory = root / "steward" / "scoreboard"
    today = directory / f"{measured}.json"
    latest = directory / "latest.json"
    badge = directory / "badge.json"
    payload = _json_bytes(scoreboard)
    badge_payload = _json_bytes(_badge(scoreboard))
    _atomic_write(today, payload)
    _atomic_write(latest, payload)
    _atomic_write(badge, badge_payload)
    return today, latest, badge


class ScoringContext:
    """One-run cached reader for public GitHub and HTTP evidence."""

    def __init__(self, root: Path, now: datetime) -> None:
        self.root = root
        self.now = now.astimezone(timezone.utc)
        self._api_cache: dict[tuple[str, tuple[tuple[str, str], ...]], object] = {}
        self._api_errors: dict[tuple[str, tuple[tuple[str, str], ...]], Exception] = {}
        self._http_cache: dict[str, tuple[int, bytes]] = {}
        self._command_cache: dict[tuple[str, ...], subprocess.CompletedProcess[str]] = {}
        self._public_repos: Optional[list[dict[str, object]]] = None
        self._repo_cache: dict[str, dict[str, object]] = {}
        self._tree_cache: dict[str, list[dict[str, object]]] = {}
        self._readme_cache: dict[str, str] = {}
        self._blob_text_cache: dict[tuple[str, str], str] = {}

    def api(
        self,
        endpoint: str,
        headers: Optional[Mapping[str, str]] = None,
    ) -> object:
        if headers is not None and (
            not isinstance(headers, Mapping)
            or any(
                not isinstance(name, str)
                or not isinstance(value, str)
                or "\n" in name
                or "\n" in value
                or "\r" in name
                or "\r" in value
                for name, value in headers.items()
            )
        ):
            raise ScoreError("GitHub API headers are malformed")
        header_key = tuple(sorted((headers or {}).items()))
        key = (endpoint, header_key)
        if key in self._api_errors:
            raise self._api_errors[key]
        if key not in self._api_cache:
            try:
                if not header_key:
                    payload = gh_api(endpoint)
                else:
                    argv = [
                        "gh",
                        "api",
                        "--hostname",
                        "github.com",
                        "--method",
                        "GET",
                    ]
                    for name, value in header_key:
                        argv.extend(("--header", f"{name}: {value}"))
                    argv.append(endpoint)
                    result = self.command(tuple(argv))
                    try:
                        payload = json.loads(result.stdout)
                    except json.JSONDecodeError as exc:
                        raise ScoreError(
                            "GitHub API returned malformed JSON"
                        ) from exc
                self._api_cache[key] = payload
            except Exception as exc:
                self._api_errors[key] = exc
                raise
        return self._api_cache[key]

    def blob_text(self, repo: str, sha: str) -> str:
        if (
            not isinstance(repo, str)
            or not re.fullmatch(r"[A-Za-z0-9_.-]+", repo)
            or repo.startswith("-")
        ):
            raise ScoreError("blob repository name is malformed")
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-fA-F]{40}", sha):
            raise ScoreError("blob SHA must be exactly 40 hexadecimal characters")
        key = (repo, sha.lower())
        if key in self._blob_text_cache:
            return self._blob_text_cache[key]
        data = self.api(f"repos/{OWNER}/{repo}/git/blobs/{sha}")
        if (
            not isinstance(data, Mapping)
            or data.get("sha") != sha
            or data.get("encoding") != "base64"
            or not isinstance(data.get("content"), str)
            or type(data.get("size")) is not int
            or data["size"] < 0
            or data["size"] > 524288
        ):
            raise ScoreError("GitHub blob response is malformed or exceeds 512 KB")
        try:
            encoded = "".join(data["content"].split())
            raw = base64.b64decode(encoded, validate=True)
            text = raw.decode("utf-8")
        except (binascii.Error, ValueError, UnicodeError) as exc:
            raise ScoreError("GitHub blob is not strict base64 UTF-8 text") from exc
        if len(raw) > 524288:
            raise ScoreError("decoded GitHub blob exceeds 512 KB")
        self._blob_text_cache[key] = text
        return text

    def command(self, argv: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
        if argv not in self._command_cache:
            try:
                result = subprocess.run(
                    argv,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    env={**os.environ, "GH_PROMPT_DISABLED": "1", "GH_PAGER": "cat"},
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise ScoreError(f"command unavailable: {argv[0]}") from exc
            self._command_cache[argv] = result
        result = self._command_cache[argv]
        if result.returncode:
            raise ScoreError(f"{argv[0]} read failed with exit {result.returncode}")
        return result

    def graphql(self, query: str) -> object:
        result = self.command(("gh", "api", "graphql", "-f", f"query={query}"))
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise ScoreError("GitHub GraphQL returned malformed JSON") from exc

    def http(self, url: str) -> tuple[int, bytes]:
        if url not in self._http_cache:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "mrodgersjs-web-steward/1"},
                method="GET",
            )
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    status = int(response.status)
                    body = response.read(1_048_577)
            except urllib.error.HTTPError as exc:
                status = int(exc.code)
                body = b""
            except (urllib.error.URLError, OSError, TimeoutError) as exc:
                raise ScoreError(f"HTTP read failed for {url}") from exc
            self._http_cache[url] = (status, body)
        return self._http_cache[url]

    def public_repos(self) -> list[dict[str, object]]:
        if self._public_repos is None:
            rows: list[dict[str, object]] = []
            for page in range(1, 11):
                endpoint = f"users/{OWNER}/repos?" + urllib.parse.urlencode(
                    {
                        "type": "public",
                        "sort": "full_name",
                        "direction": "asc",
                        "per_page": 100,
                        "page": page,
                    }
                )
                data = self.api(endpoint)
                if not isinstance(data, list):
                    raise ScoreError("public repository inventory is malformed")
                page_rows = [
                    row
                    for row in data
                    if isinstance(row, dict)
                    and row.get("private") is False
                    and isinstance(row.get("owner"), Mapping)
                    and row["owner"].get("login") == OWNER
                ]
                rows.extend(page_rows)
                if len(data) < 100:
                    break
            self._public_repos = rows
            for row in rows:
                name = row.get("name")
                if isinstance(name, str):
                    self._repo_cache[name] = row
        return self._public_repos

    def repo(self, name: str) -> dict[str, object]:
        if name not in self._repo_cache:
            data = self.api(f"repos/{OWNER}/{name}")
            if not isinstance(data, dict):
                raise ScoreError(f"repository metadata is malformed for {name}")
            self._repo_cache[name] = data
        return self._repo_cache[name]

    def private_or_404(self, name: str) -> tuple[bool, str]:
        try:
            data = self.repo(name)
        except Exception as exc:
            if "HTTP 404" in str(exc):
                return True, f"{name} returned 404"
            raise
        private = data.get("private") is True
        return private, f"{name} private={str(private).lower()}"

    def default_branch(self, name: str) -> str:
        value = self.repo(name).get("default_branch")
        if not isinstance(value, str) or not value:
            raise ScoreError(f"{name} has no default branch")
        return value

    def file_text(self, name: str, path: str) -> str:
        key = f"{name}:{path}"
        if key not in self._readme_cache:
            data = regular_file(
                self.api,
                f"repos/{OWNER}/{name}",
                path,
                self.default_branch(name),
            )
            content = data.get("content")
            if not isinstance(content, str):
                raise ScoreError(f"{name}/{path} is not UTF-8 text")
            self._readme_cache[key] = content
        return self._readme_cache[key]

    def exists(self, name: str, path: str) -> bool:
        try:
            self.file_text(name, path)
            return True
        except NotFoundError:
            return False

    def readme(self, name: str) -> str:
        return self.file_text(name, "README.md")

    def tree(self, name: str) -> list[dict[str, object]]:
        if name not in self._tree_cache:
            endpoint = (
                f"repos/{OWNER}/{name}/git/trees/"
                f"{urllib.parse.quote(self.default_branch(name), safe='')}?recursive=1"
            )
            data = self.api(endpoint)
            if not isinstance(data, dict) or not isinstance(data.get("tree"), list):
                raise ScoreError(f"{name} tree response is malformed")
            if data.get("truncated") is True:
                raise ScoreError(f"{name} tree is truncated")
            rows = data["tree"]
            if any(not isinstance(row, dict) for row in rows):
                raise ScoreError(f"{name} tree contains a malformed row")
            self._tree_cache[name] = rows
        return self._tree_cache[name]

    def workflows(self, name: str) -> list[dict[str, object]]:
        data = self.api(f"repos/{OWNER}/{name}/actions/workflows?per_page=100")
        if not isinstance(data, dict) or not isinstance(data.get("workflows"), list):
            raise ScoreError(f"{name} workflow response is malformed")
        return [row for row in data["workflows"] if isinstance(row, dict)]

    def runs(self, name: str, workflow: str = "") -> list[dict[str, object]]:
        suffix = f"/actions/workflows/{urllib.parse.quote(workflow, safe='')}/runs" if workflow else "/actions/runs"
        endpoint = f"repos/{OWNER}/{name}{suffix}?per_page=100&branch=main"
        data = self.api(endpoint)
        if not isinstance(data, dict) or not isinstance(data.get("workflow_runs"), list):
            raise ScoreError(f"{name} run response is malformed")
        return [row for row in data["workflow_runs"] if isinstance(row, dict)]

    def latest_run(self, name: str, workflow: str = "") -> Optional[dict[str, object]]:
        rows = self.runs(name, workflow)
        return rows[0] if rows else None

    def pins(self) -> tuple[str, ...]:
        path = self.root / "steward" / "PINNED.txt"
        try:
            values = tuple(
                line.split("/", 1)[-1]
                for line in path.read_text(encoding="utf-8").splitlines()
                if line
            )
        except (OSError, UnicodeError) as exc:
            raise ScoreError("cannot read steward/PINNED.txt") from exc
        if len(values) != 6:
            raise ScoreError("PINNED.txt must contain six rows")
        return values

    def pinned_names(self) -> tuple[str, ...]:
        query = (
            f'query {{ user(login: "{OWNER}") {{ pinnedItems(first: 6, '
            "types: REPOSITORY) { nodes { ... on Repository { name } } } } }"
        )
        data = self.graphql(query)
        try:
            nodes = data["data"]["user"]["pinnedItems"]["nodes"]
            return tuple(node["name"] for node in nodes)
        except (KeyError, TypeError):
            raise ScoreError("GitHub pinnedItems response is malformed") from None

    def code_search(self, query: str) -> list[dict[str, object]]:
        endpoint = "search/code?" + urllib.parse.urlencode(
            {"q": f"{query} user:{OWNER}", "per_page": 100}
        )
        data = self.api(
            endpoint,
            headers={"Accept": "application/vnd.github.text-match+json"},
        )
        if not isinstance(data, dict) or not isinstance(data.get("items"), list):
            raise ScoreError("GitHub code search response is malformed")
        rows = data["items"]
        if any(not isinstance(row, dict) for row in rows):
            raise ScoreError("GitHub code search contains a malformed row")
        for row in rows:
            sha = row.get("sha")
            repository = row.get("repository")
            repo_name = (
                repository.get("name")
                if isinstance(repository, Mapping)
                else None
            )
            if (
                not isinstance(sha, str)
                or not re.fullmatch(r"[0-9a-fA-F]{40}", sha)
                or not isinstance(repo_name, str)
                or not re.fullmatch(r"[A-Za-z0-9_.-]+", repo_name)
            ):
                raise ScoreError("GitHub code search identity is malformed")
            matches = row.get("text_matches")
            if matches is None:
                continue
            if not isinstance(matches, list) or any(
                not isinstance(match, Mapping)
                or not isinstance(match.get("fragment"), str)
                or not match["fragment"]
                for match in matches
            ):
                raise ScoreError("GitHub code search text_matches are malformed")
        return rows

    def latest_success(self, name: str, workflow: str = "") -> tuple[bool, str]:
        run = self.latest_run(name, workflow)
        if run is None:
            return False, f"{name} has no matching workflow run"
        conclusion = run.get("conclusion")
        return conclusion == "success", f"{name} latest conclusion={conclusion}"

    def all_readmes(self) -> list[tuple[str, str]]:
        return [(str(repo["name"]), self.readme(str(repo["name"]))) for repo in self.public_repos()]

    def evaluate(self, criterion: Mapping[str, object]) -> tuple[bool, str]:
        identifier = str(criterion["id"])
        repos = self.public_repos
        profile = lambda: self.readme(PROFILE_REPO)

        if identifier == "profile-readme-exists":
            ok = self.exists(PROFILE_REPO, "README.md")
            return ok, f"profile README exists={str(ok).lower()}"
        if identifier == "banner-200":
            url = f"https://raw.githubusercontent.com/{OWNER}/{PROFILE_REPO}/main/assets/profile-banner-v2.jpg"
            status, _ = self.http(url)
            return status == 200, f"banner HTTP status={status}"
        if identifier == "no-phone":
            phone_pattern = re.compile(
                r"(?<!\d)\d{3}[.\-\s]?\d{3}[.\-\s]?\d{4}(?!\d)"
            )
            found = phone_pattern.search(profile())
            return found is None, "profile phone pattern absent" if found is None else "profile phone pattern found"
        if identifier == "contact-email":
            ok = "mrodgersjs@gmail.com" in profile()
            return ok, f"profile email present={str(ok).lower()}"
        if identifier in {"bio-fde", "blog-url", "location-denver", "hireable"}:
            user = self.api("user")
            if not isinstance(user, Mapping):
                raise ScoreError("authenticated GitHub user response is malformed")
            if identifier == "bio-fde":
                ok = "Forward Deployed Engineer" in str(user.get("bio") or "")
                return ok, f"bio contains FDE={str(ok).lower()}"
            if identifier == "blog-url":
                value = str(user.get("blog") or "").rstrip("/")
                ok = value == "https://rodgersintelligence.com"
                return ok, f"blog={value or 'empty'}"
            if identifier == "location-denver":
                ok = "denver" in str(user.get("location") or "").lower()
                return ok, f"location={user.get('location')!s}"
            ok = user.get("hireable") is True
            return ok, f"hireable={str(ok).lower()}"
        if identifier == "linkedin-social":
            rows = self.api("user/social_accounts")
            if not isinstance(rows, list):
                raise ScoreError("social account response is malformed")
            urls = {str(row.get("url")) for row in rows if isinstance(row, Mapping)}
            expected = "https://www.linkedin.com/in/mike-rodgers-14416414/"
            return expected in urls, f"LinkedIn social account present={str(expected in urls).lower()}"
        if identifier == "pins-six":
            actual, expected = self.pinned_names(), self.pins()
            return actual == expected, f"pinned={list(actual)} expected={list(expected)}"
        if identifier == "following-20":
            rows = self.api("user/following?per_page=100")
            if not isinstance(rows, list):
                raise ScoreError("following response is malformed")
            return len(rows) >= 20, f"following count={len(rows)}"
        if identifier == "live-repo-count":
            count = len(repos())
            claims = [int(value) for value in re.findall(r"\b(\d+)\s+(?:public\s+)?repos(?:itories)?\b", profile(), re.I)]
            ok = not claims or all(value == count for value in claims)
            return ok, f"live public count={count}; static claims={claims}"
        if identifier == "public-cap":
            count = len(repos())
            return count <= 30, f"public repository count={count}"
        if identifier == "every-desc":
            missing = [str(row.get("name")) for row in repos() if not str(row.get("description") or "").strip()]
            return not missing, f"repositories without descriptions={missing}"
        if identifier == "every-license":
            missing = [str(row["name"]) for row in repos() if not self.exists(str(row["name"]), "LICENSE")]
            return not missing, f"repositories without LICENSE={missing}"
        if identifier == "no-empty-stub":
            bad = []
            for row in repos():
                name = str(row["name"])
                paths = [str(item.get("path")) for item in self.tree(name) if item.get("type") == "blob"]
                non_asset = [path for path in paths if path != "README.md" and not path.startswith("assets/")]
                if "README.md" not in paths or not non_asset:
                    bad.append(name)
            return not bad, f"empty or README-less repositories={bad}"
        if identifier in {"birch-private", "openwork-private", "omniscout-private", "legacy-site-private"}:
            names = {
                "birch-private": "birch-rig-boots",
                "openwork-private": "openwork",
                "omniscout-private": "rig-omniscout-l2",
                "legacy-site-private": "mike-rodgers-site",
            }
            return self.private_or_404(names[identifier])
        if identifier == "no-abs-home-paths":
            offending = set()

            def fragment_is_exempt(fragment: str) -> bool:
                home_lines = [
                    line
                    for line in fragment.splitlines()
                    if "/Users/rig128gb" in line
                    or "/home/operator" in line
                ]
                return bool(home_lines) and all(
                    "no-abs-home-paths" in line
                    and "/Users/rig128gb" in line
                    and "/home/operator" in line
                    for line in home_lines
                )

            for needle in ('"/Users/rig128gb"', '"/home/operator"'):
                for item in self.code_search(needle):
                    path = str(item.get("path") or "")
                    sha = item.get("sha")
                    repository = item.get("repository")
                    repo_name = (
                        str(repository.get("name"))
                        if isinstance(repository, Mapping)
                        else ""
                    )
                    if not repo_name or not path or not isinstance(sha, str):
                        offending.add(f"unknown:{path or 'unknown'}")
                        continue
                    matches = item.get("text_matches")
                    fragments = (
                        [str(match["fragment"]) for match in matches]
                        if isinstance(matches, list) and matches
                        else [self.blob_text(repo_name, sha)]
                    )

                    unsafe_fragment = any(
                        not fragment_is_exempt(fragment)
                        for fragment in fragments
                    )
                    if unsafe_fragment:
                        offending.add(f"{repo_name}:{path}")
            return not offending, f"forbidden home path matches={sorted(offending)}"
        if identifier == "no-pycache":
            bad = [str(row["name"]) for row in repos() if any("__pycache__" in str(item.get("path")) for item in self.tree(str(row["name"])))]
            return not bad, f"repositories with __pycache__={bad}"
        if identifier == "no-env-files":
            pattern = re.compile(r"(^|/)(\.env[^/]*|id_rsa|[^/]+\.pem)$", re.I)
            bad = [f"{row['name']}:{item.get('path')}" for row in repos() for item in self.tree(str(row["name"])) if pattern.search(str(item.get("path") or ""))]
            return not bad, f"credential-like public paths={bad}"
        if identifier == "flagship-homepage":
            bad = []
            for name in ("rigforge", "proof-studio", "fde-portfolio"):
                homepage = str(self.repo(name).get("homepage") or "")
                parsed = urllib.parse.urlparse(homepage)
                if not homepage or not (parsed.netloc == "rodgersintelligence.com" or "docs" in parsed.path.lower()):
                    bad.append(name)
            return not bad, f"flagships without approved homepage={bad}"
        if identifier == "topics-baseline":
            bad = [str(row["name"]) for row in repos() if not BASELINE_TOPICS.issubset(set(row.get("topics") or []))]
            return not bad, f"repositories missing baseline topics={bad}"
        if identifier == "topics-specific":
            bad = [str(row["name"]) for row in repos() if len(set(row.get("topics") or [])) < 10]
            return not bad, f"repositories with fewer than 10 topics={bad}"
        if identifier == "desc-no-typo":
            bad = [str(row["name"]) for row in repos() if "ProofPates" in str(row.get("description") or "")]
            return not bad, f"description typo repositories={bad}"
        if identifier == "default-main":
            bad = [str(row["name"]) for row in repos() if row.get("default_branch") != "main"]
            return not bad, f"non-main default repositories={bad}"
        if identifier == "clone-org":
            bad = [name for name, text in self.all_readmes() if "github.com/rodgemd1-lgtm" in text or "github.com/rig-intelligence/" in text]
            return not bad, f"legacy clone organizations in={bad}"
        if identifier == "unique-desc":
            seen: dict[str, str] = {}
            duplicates = []
            for row in repos():
                description = str(row.get("description") or "").strip()
                if description in seen:
                    duplicates.append((seen[description], str(row["name"])))
                else:
                    seen[description] = str(row["name"])
            return not duplicates, f"duplicate descriptions={duplicates}"
        if identifier == "readme-exists":
            missing = [str(row["name"]) for row in repos() if not self.exists(str(row["name"]), "README.md")]
            return not missing, f"repositories without README.md={missing}"
        if identifier == "install-first":
            bad = [name for name, text in self.all_readmes() if "```" not in "\n".join(text.splitlines()[:80])]
            return not bad, f"repositories without early code fence={bad}"
        if identifier == "live-ci-badge":
            bad = []
            for row in repos():
                name = str(row["name"])
                if self.workflows(name) and "github/actions/workflow/status" not in self.readme(name):
                    bad.append(name)
            return not bad, f"repositories without live CI badge={bad}"
        if identifier == "license-badge-match":
            bad = [name for name, text in self.all_readmes() if re.search(r"\bMIT\b", text) and not self.exists(name, "LICENSE")]
            return not bad, f"MIT claims without LICENSE={bad}"
        if identifier == "install-registry":
            bad = []
            pip_pattern = re.compile(
                r"^\s*(?:\$\s*)?(?:python(?:3(?:\.\d+)?)?\s+-m\s+)?"
                r"pip3?\s+install\s+(.+?)\s*$"
            )
            npx_pattern = re.compile(r"^\s*(?:\$\s*)?npx\s+(.+?)\s*$")
            pip_flags = {
                "--disable-pip-version-check",
                "--no-deps",
                "--pre",
                "--quiet",
                "--upgrade",
                "--user",
                "-q",
                "-U",
            }
            pip_value_flags = {
                "--constraint",
                "--extra-index-url",
                "--index-url",
                "--retries",
                "--target",
                "--timeout",
                "--trusted-host",
                "-c",
                "-r",
                "-t",
            }
            for name, text in self.all_readmes():
                for line in text.splitlines():
                    pip_match = pip_pattern.match(line)
                    if pip_match:
                        try:
                            arguments = shlex.split(pip_match.group(1), comments=True)
                        except ValueError:
                            continue
                        if "-e" in arguments or "--editable" in arguments:
                            continue
                        packages = []
                        index = 0
                        while index < len(arguments):
                            argument = arguments[index]
                            if argument in pip_flags:
                                index += 1
                                continue
                            if argument in pip_value_flags:
                                index += 2
                                continue
                            if any(
                                argument.startswith(f"{flag}=")
                                for flag in pip_value_flags
                                if flag.startswith("--")
                            ):
                                index += 1
                                continue
                            if argument.startswith("-"):
                                index += 1
                                continue
                            if argument.startswith("git+") or "://" in argument:
                                index += 1
                                continue
                            package_match = re.fullmatch(
                                r"([A-Za-z0-9_.-]+)(?:\[[A-Za-z0-9_,.-]+\])?"
                                r"(?:[<>=!~].*)?",
                                argument,
                            )
                            if package_match:
                                packages.append(package_match.group(1))
                            index += 1
                        for package in packages:
                            status, _ = self.http(
                                f"https://pypi.org/pypi/{urllib.parse.quote(package)}/json"
                            )
                            if status != 200:
                                bad.append(f"{name}:pypi:{package}:{status}")
                    npx_match = npx_pattern.match(line)
                    if npx_match:
                        try:
                            arguments = shlex.split(npx_match.group(1), comments=True)
                        except ValueError:
                            continue
                        package_spec = next(
                            (
                                argument
                                for argument in arguments
                                if not argument.startswith("-")
                                and "://" not in argument
                            ),
                            None,
                        )
                        package = package_spec
                        if package and package.startswith("@"):
                            slash = package.find("/")
                            version_at = package.rfind("@")
                            if slash > 1 and version_at > slash:
                                package = package[:version_at]
                        elif package and "@" in package:
                            package = package.split("@", 1)[0]
                        if package and re.fullmatch(
                            r"@?[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)?",
                            package,
                        ):
                            status, _ = self.http(
                                f"https://registry.npmjs.org/{urllib.parse.quote(package, safe='')}"
                            )
                            if status != 200:
                                bad.append(f"{name}:npm:{package}:{status}")
            return not bad, f"unregistered install claims={bad}"
        if identifier == "test-count-honest":
            bad = []
            for name, text in self.all_readmes():
                if re.search(r"\b\d+/\d+\s+tests\b", text, re.I):
                    ok, _ = self.latest_success(name)
                    if not ok:
                        bad.append(name)
            return not bad, f"unbacked test-count claims={bad}"
        if identifier == "footer-site":
            bad = [name for name, text in self.all_readmes() if "rodgersintelligence.com" not in text]
            return not bad, f"repositories without footer site={bad}"
        if identifier == "no-raw-json-tables":
            pattern = re.compile(r"^\|.*(?:\{&quot;|\{\")", re.M)
            bad = [name for name, text in self.all_readmes() if pattern.search(text)]
            return not bad, f"READMEs with raw JSON tables={bad}"
        if identifier == "verify-command":
            pattern = re.compile(r"pytest|smoke|npm test|node --test|rigforge", re.I)
            bad = [name for name, text in self.all_readmes() if not pattern.search(text)]
            return not bad, f"READMEs without verify command={bad}"
        if identifier == "hero-ok":
            bad = []
            image_pattern = re.compile(r"(?:src=[\"']|!\[[^]]*\]\()([^\"')]+)")
            for name, text in self.all_readmes():
                branch = self.default_branch(name)
                for path in image_pattern.findall(text):
                    if path.startswith(("http://", "https://", "data:")):
                        continue
                    url = f"https://raw.githubusercontent.com/{OWNER}/{name}/{branch}/{path.lstrip('./')}"
                    status, _ = self.http(url)
                    if status != 200:
                        bad.append(f"{name}:{path}:{status}")
            return not bad, f"broken local README images={bad}"
        if identifier == "readme-size":
            bad = [name for name, text in self.all_readmes() if len(text.encode("utf-8")) > 40000]
            return not bad, f"READMEs over 40000 bytes={bad}"
        if identifier == "clone-url-self":
            bad = []
            clone_pattern = re.compile(
                r"^\s*(?:\$\s*)?git\s+clone\s+(?:--\S+\s+)*"
                r"https://github\.com/([^/\s]+)/([^/\s]+?)(?:\.git)?(?:\s|$)",
                re.M,
            )
            for name, text in self.all_readmes():
                for owner, repo in clone_pattern.findall(text):
                    if (owner, repo) != (OWNER, name):
                        bad.append(f"{name}->{owner}/{repo}")
            return not bad, f"cross-repository clone examples={bad}"
        if identifier == "languages-honest":
            bad = []
            badge_pattern = re.compile(
                r"shields\.io/badge/([^/?#\s)]+?)-[^/?#\s)]+"
            )
            for name, text in self.all_readmes():
                labels = {
                    urllib.parse.unquote(match).replace("--", "-").lower()
                    for match in badge_pattern.findall(text)
                }
                language_shields = labels & LANGUAGE_BADGES
                data = self.api(f"repos/{OWNER}/{name}/languages")
                if not isinstance(data, Mapping):
                    raise ScoreError(f"{name} language response is malformed")
                languages = {str(value).lower() for value in data}
                unsupported = language_shields - languages
                if unsupported:
                    bad.append(f"{name}:{sorted(unsupported)}")
            return not bad, f"unsupported language shields={bad}"
        if identifier == "insight-quote":
            ok = any(line.startswith(">") for line in profile().splitlines())
            return ok, f"profile blockquote present={str(ok).lower()}"
        if identifier == "no-secret-clearance-string":
            ok = "Secret Security Clearance" not in profile()
            return ok, f"forbidden clearance string absent={str(ok).lower()}"
        if identifier == "product-has-workflow":
            bad = [name for name in self.pins() if not self.workflows(name)]
            return not bad, f"pins without workflows={bad}"
        if identifier == "latest-success":
            results = [self.latest_success(name) for name in self.pins()]
            return all(ok for ok, _ in results), "; ".join(detail for _, detail in results)
        if identifier == "proof-gate-ci":
            cutoff = self.now - timedelta(days=14)
            matching = [run for run in self.runs("proof-gate-action") if run.get("conclusion") == "success" and _parse_time(run.get("updated_at")) >= cutoff]
            return bool(matching), f"recent successful proof-gate runs={len(matching)}"
        if identifier in {"mesh-green", "jake-green", "comms-green", "resume-green", "patents-green", "fde-portfolio-smoke"}:
            mapping = {
                "mesh-green": ("mesh-studio", "ci.yml"),
                "jake-green": ("jake-studio", "smoke.yml"),
                "comms-green": ("communications-studio", "ci.yml"),
                "resume-green": ("resume", "smoke.yml"),
                "patents-green": ("patents", "smoke.yml"),
                "fde-portfolio-smoke": ("fde-portfolio", "smoke.yml"),
            }
            return self.latest_success(*mapping[identifier])
        if identifier == "deviatrix-green-or-unclaimed":
            ok, detail = self.latest_success("deviatrix-genesis", "ci.yml")
            claimed = "MCP" in self.readme("deviatrix-genesis")
            return ok or not claimed, f"{detail}; README MCP claim={str(claimed).lower()}"
        if identifier == "no-continue-on-error":
            bad = []

            def has_unsafe_key(source: str) -> bool:
                block_indent: Optional[int] = None
                block_key = re.compile(
                    r"^(['\"]?)continue-on-error\1\s*:\s*(.*?)"
                    r"\s*(?:#.*)?$",
                    re.I,
                )
                flow_key = re.compile(
                    r"(?:^|[{\[,])\s*(['\"]?)continue-on-error\1"
                    r"\s*:\s*([^,}\]]+)",
                    re.I,
                )
                for line in source.splitlines():
                    if not line.strip():
                        continue
                    indent = len(line) - len(line.lstrip())
                    if block_indent is not None:
                        if indent > block_indent:
                            continue
                        block_indent = None
                    stripped = line.lstrip()
                    if stripped.startswith("#"):
                        continue
                    if re.match(r"['\"]?run['\"]?\s*:", stripped, re.I):
                        if re.match(
                            r"['\"]?run['\"]?\s*:\s*[|>]",
                            stripped,
                            re.I,
                        ):
                            block_indent = indent
                        continue

                    values = []
                    match = block_key.match(stripped)
                    if match:
                        values.append(match.group(2))
                    values.extend(
                        match.group(2) for match in flow_key.finditer(stripped)
                    )
                    for raw_value in values:
                        value = (
                            raw_value.split("#", 1)[0]
                            .strip()
                            .strip("\"'")
                            .lower()
                        )
                        if value != "false":
                            return True
                return False

            for name in self.pins():
                for workflow in self.workflows(name):
                    path = workflow.get("path")
                    if (
                        isinstance(path, str)
                        and path.startswith(".github/workflows/")
                        and has_unsafe_key(self.file_text(name, path))
                    ):
                        bad.append(f"{name}:{path}")
            return not bad, f"workflows with continue-on-error true={bad}"
        if identifier == "workflow-on-default":
            bad = []
            for name in self.pins():
                active = [row for row in self.workflows(name) if "dependabot" not in str(row.get("path") or "").lower()]
                if not active:
                    bad.append(name)
            return not bad, f"pins without non-Dependabot workflow={bad}"
        if identifier == "dependabot-rigforge":
            ok = self.exists("rigforge", ".github/dependabot.yml")
            return ok, f"rigforge dependabot file exists={str(ok).lower()}"
        if identifier == "proof-gate-tag":
            try:
                reference = self.api(
                    f"repos/{OWNER}/proof-gate-action/git/ref/tags/v1"
                )
            except Exception as exc:
                if "HTTP 404" in str(exc):
                    return False, "proof-gate-action tag v1 is missing"
                raise
            tag_object = reference.get("object") if isinstance(reference, Mapping) else None
            if (
                not isinstance(tag_object, Mapping)
                or tag_object.get("type") != "tag"
                or not isinstance(tag_object.get("sha"), str)
            ):
                return False, "tag v1 is lightweight; tagger timestamp is unverifiable"
            tag = self.api(
                f"repos/{OWNER}/proof-gate-action/git/tags/{tag_object['sha']}"
            )
            tagger = tag.get("tagger") if isinstance(tag, Mapping) else None
            tagged_at = tagger.get("date") if isinstance(tagger, Mapping) else None
            if not isinstance(tagged_at, str):
                return False, "annotated tag v1 has no provable tagger timestamp"
            successful = [
                run
                for run in self.runs("proof-gate-action")
                if run.get("conclusion") == "success"
            ]
            run_times = [
                _parse_time(run.get("updated_at"))
                for run in successful
                if run.get("updated_at")
            ]
            if not run_times:
                return False, "proof-gate-action has no successful run updated_at"
            tag_time = _parse_time(tagged_at)
            first_green = min(run_times)
            ok = tag_time > first_green
            return ok, f"tagged_at={tag_time.isoformat()}; first_green_updated_at={first_green.isoformat()}"
        if identifier == "no-skipped-jobs-as-pass":
            bad = []
            for name in self.pins():
                run = self.latest_run(name)
                if run is None or type(run.get("id")) is not int:
                    bad.append(f"{name}:no-run")
                    continue
                data = self.api(f"repos/{OWNER}/{name}/actions/runs/{run['id']}/jobs?per_page=100")
                jobs = data.get("jobs") if isinstance(data, Mapping) else None
                if not isinstance(jobs, list):
                    raise ScoreError(f"{name} jobs response is malformed")
                required_jobs = [
                    job
                    for job in jobs
                    if isinstance(job, Mapping)
                    and re.search(
                        r"\b(?:smoke|test)\b",
                        str(job.get("name") or ""),
                        re.I,
                    )
                ]
                if not required_jobs or any(
                    job.get("status") != "completed"
                    or job.get("conclusion") != "success"
                    for job in required_jobs
                ):
                    bad.append(name)
            return not bad, f"pins without successful required smoke/test job={bad}"
        if identifier == "action-yml-valid":
            ok = self.exists("proof-gate-action", "action.yml") or self.exists("proof-gate-action", "action.yaml")
            return ok, f"proof-gate action metadata exists={str(ok).lower()}"
        if identifier == "public-mcp-count":
            live = sum(any(str(item.get("path") or "").endswith("mcp_server.py") or "stdio_server" in str(item.get("path") or "") for item in self.tree(str(row["name"]))) for row in repos())
            claims = [int(value) for value in re.findall(r"\b(\d+)\s+(?:public\s+)?MCP servers?\b", profile(), re.I)]
            return bool(claims) and all(value == live for value in claims), f"live MCP repo count={live}; claims={claims}"
        if identifier in {"rigforge-mcp-file", "mesh-mcp-file", "catalog-mcp-file"}:
            mapping = {
                "rigforge-mcp-file": ("rigforge", "rigforge/mcp_server.py"),
                "mesh-mcp-file": ("mesh-studio", "src/rig_mesh/mcp_server.py"),
                "catalog-mcp-file": (PROFILE_REPO, "steward/catalog_mcp.py"),
            }
            repo_name, path = mapping[identifier]
            ok = self.exists(repo_name, path)
            return ok, f"{repo_name}/{path} exists={str(ok).lower()}"
        if identifier == "comms-not-mcp":
            ok = re.search(r"\bMCP server\b", self.readme("communications-studio"), re.I) is None
            return ok, f"communications-studio MCP server claim absent={str(ok).lower()}"
        if identifier == "omniscout-not-public-mcp":
            return self.private_or_404("rig-omniscout-l2")
        if identifier == "claude-desktop-snippet":
            ok = '"mcpServers"' in self.readme("rigforge")
            return ok, f"rigforge mcpServers snippet present={str(ok).lower()}"
        if identifier == "catalog-readonly":
            source = (self.root / "steward" / "catalog_mcp.py").read_text(encoding="utf-8")
            bad = re.search(r"gh\s+api\s+(?:-X|--method)\s+(?:POST|PATCH|PUT|DELETE)", source, re.I)
            return bad is None, "catalog contains no mutating gh method" if bad is None else "catalog contains a mutating gh method"
        if identifier == "catalog-evals":
            source = (self.root / "steward" / "evals.xml").read_text(encoding="utf-8")
            count = len(re.findall(r"<eval\s", source))
            return count == 10, f"catalog eval count={count}"
        if identifier == "local-57-unadvertised":
            bad = [name for name, text in self.all_readmes() if "github-repo-mcp" in text or "228 tools" in text]
            return not bad, f"READMEs advertising local adapter={bad}"
        if identifier == "no-public-mcp-port":
            source = (self.root / "steward" / "catalog_mcp.py").read_text(encoding="utf-8")
            try:
                tree = ast.parse(source)
            except SyntaxError as exc:
                raise ScoreError("catalog_mcp.py is not valid Python") from exc
            transports = []
            dynamic = False
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                if not isinstance(node.func, ast.Attribute) or node.func.attr != "run":
                    continue
                for keyword in node.keywords:
                    if keyword.arg != "transport":
                        continue
                    if isinstance(keyword.value, ast.Constant) and isinstance(
                        keyword.value.value, str
                    ):
                        transports.append(keyword.value.value.lower())
                    else:
                        dynamic = True
            ok = bool(transports) and not dynamic and set(transports) == {"stdio"}
            return ok, f"catalog transports={transports}; dynamic={dynamic}"
        if identifier == "mcp-no-plaintext-tokens":
            bad = []
            token_pattern = re.compile(
                r"\b(?:ghp_|github_pat_)[A-Za-z0-9_]+"
            )
            assignment_pattern = re.compile(
                r"[\"']?GH_TOKEN[\"']?\s*[:=]\s*"
                r"(?:\"([^\"]*)\"|'([^']*)'|([^\s,\]]+))",
                re.I,
            )
            safe_values = {"${env:GH_TOKEN}", "${GH_TOKEN}", "$GH_TOKEN"}
            for name, text in self.all_readmes():
                unsafe = bool(token_pattern.search(text))
                for match in assignment_pattern.finditer(text):
                    value = next(
                        (group for group in match.groups() if group is not None),
                        "",
                    )
                    normalized = value.rstrip(",").strip()
                    if normalized not in safe_values:
                        unsafe = True
                if unsafe:
                    bad.append(name)
            return not bad, f"READMEs with plaintext GitHub token={bad}"
        if identifier in {"copilot-instructions-pins", "agents-md-pins", "codeowners-pins"}:
            path = {
                "copilot-instructions-pins": ".github/copilot-instructions.md",
                "agents-md-pins": "AGENTS.md",
                "codeowners-pins": ".github/CODEOWNERS",
            }[identifier]
            bad = []
            for name in self.pins():
                if not self.exists(name, path):
                    bad.append(name)
                elif identifier == "codeowners-pins" and "@mrodgersjs-web" not in self.file_text(name, path):
                    bad.append(name)
            return not bad, f"pins failing {path}={bad}"
        if identifier == "copilot-instructions-profile":
            ok = self.exists(PROFILE_REPO, ".github/copilot-instructions.md")
            return ok, f"profile Copilot instructions exist={str(ok).lower()}"
        if identifier == "copilot-file-short":
            bad = [name for name in self.pins() if len(self.file_text(name, ".github/copilot-instructions.md").encode("utf-8")) > 8000]
            return not bad, f"oversize Copilot instruction files={bad}"
        if identifier == "copilot-has-test-cmd":
            pattern = re.compile(r"pytest|smoke|npm test", re.I)
            bad = [name for name in self.pins() if not pattern.search(self.file_text(name, ".github/copilot-instructions.md"))]
            return not bad, f"Copilot instruction files without test command={bad}"
        if identifier == "resume-pdf":
            pdfs = [str(item.get("path")) for item in self.tree("resume") if str(item.get("path") or "").lower().endswith(".pdf")]
            if pdfs:
                return True, f"resume PDF paths={pdfs}"
            urls = re.findall(
                r"https?://[^\s)\"']+\.pdf(?:\?[^\s)\"']*)?",
                self.readme("resume"),
                re.I,
            )
            live = [url for url in urls if self.http(url)[0] == 200]
            return bool(live), f"live resume PDF links={live}"
        if identifier == "directory-matches-public":
            try:
                public = self.repo("rig-agent-directory").get("private") is False
            except Exception as exc:
                if "HTTP 404" in str(exc):
                    return True, "rig-agent-directory is unavailable"
                raise
            if not public:
                return True, "rig-agent-directory is private"
            claims = [int(value) for value in re.findall(r"\b(\d+)\s+public\s+repos(?:itories)?\b", self.readme("rig-agent-directory"), re.I)]
            count = len(repos())
            return bool(claims) and all(value == count for value in claims), f"directory claims={claims}; live={count}"
        if identifier == "no-star-farming":
            starred = []
            for row in repos():
                name = str(row["name"])
                query = f'query {{ repository(owner: "{OWNER}", name: "{name}") {{ viewerHasStarred }} }}'
                data = self.graphql(query)
                try:
                    if data["data"]["repository"]["viewerHasStarred"] is True:
                        starred.append(name)
                except (KeyError, TypeError):
                    raise ScoreError(f"viewerHasStarred response malformed for {name}") from None
            return not starred, f"self-starred repositories={starred}"
        if identifier == "activity-7d":
            cutoff = self.now - timedelta(days=7)
            event_error: Optional[Exception] = None
            try:
                data = self.api(
                    f"repos/{OWNER}/{PROFILE_REPO}/events?per_page=100"
                )
                if not isinstance(data, list):
                    raise ScoreError("profile activity response is malformed")
                active = [
                    row
                    for row in data
                    if isinstance(row, Mapping)
                    and row.get("type") in {"PushEvent", "CreateEvent"}
                    and _parse_time(row.get("created_at")) >= cutoff
                ]
                if active:
                    return True, f"recent public events={len(active)}"
            except Exception as exc:
                event_error = exc
            try:
                run_data = self.api(
                    f"repos/{OWNER}/{PROFILE_REPO}/actions/runs?per_page=100"
                )
                runs = (
                    run_data.get("workflow_runs")
                    if isinstance(run_data, Mapping)
                    else None
                )
                if not isinstance(runs, list):
                    raise ScoreError("profile Actions run response is malformed")
                recent_runs = [
                    run
                    for run in runs
                    if isinstance(run, Mapping)
                    and _parse_time(run.get("created_at") or run.get("updated_at"))
                    >= cutoff
                ]
                if recent_runs:
                    return True, f"recent Actions runs={len(recent_runs)}"
            except Exception as run_error:
                if event_error is not None:
                    raise ScoreError(
                        f"both activity providers failed: {event_error}; {run_error}"
                    ) from run_error
                raise
            if event_error is not None:
                return False, f"events unavailable and no recent Actions run: {event_error}"
            return False, "no recent public push or Actions run"
        if identifier == "contact-path":
            text = profile()
            ok = "LinkedIn" in text and "rodgersintelligence.com" in text and "mrodgersjs@gmail.com" in text
            return ok, f"profile contact path complete={str(ok).lower()}"
        if identifier == "no-clearance-overclaim":
            ok = "active vetting" not in profile().lower()
            return ok, f"active vetting claim absent={str(ok).lower()}"
        if identifier == "criteria-count":
            count = len(load_criteria(self.root / "steward" / "criteria.yaml"))
            return count == 100, f"criteria count={count}"
        if identifier == "today-scoreboard":
            return True, f"this run atomically writes steward/scoreboard/{self.now.date().isoformat()}.json"
        if identifier == "latest-pointer":
            return True, "this run atomically writes steward/scoreboard/latest.json"
        if identifier == "scoreboard-hash":
            digest = criteria_sha256(self.root / "steward" / "criteria.yaml")
            return bool(re.fullmatch(r"[0-9a-f]{64}", digest)), f"criteria SHA-256={digest}"
        if identifier == "orca-automation":
            result = self.command(("orca", "automations", "list", "--json"))
            data = json.loads(result.stdout)
            if isinstance(data, list):
                rows = data
            elif isinstance(data, Mapping) and isinstance(
                data.get("automations"), list
            ):
                rows = data["automations"]
            elif (
                isinstance(data, Mapping)
                and isinstance(data.get("result"), Mapping)
                and isinstance(data["result"].get("automations"), list)
            ):
                rows = data["result"]["automations"]
            else:
                rows = []
            found = any(isinstance(row, Mapping) and row.get("name") == "GitHub FDE steward" and row.get("enabled") is True for row in rows)
            return found, f"enabled GitHub FDE steward automation={str(found).lower()}"
        if identifier == "local-first":
            source = (self.root / "steward" / "judge.py").read_text(encoding="utf-8")
            list_at = source.find('("ollama", "list")')
            run_at = source.find('("ollama", "run"')
            ok = "FALLBACK_PAID" in source and list_at >= 0 and (run_at < 0 or list_at < run_at)
            return ok, f"local-first judge source ordering={str(ok).lower()}"
        if identifier == "issues-for-reds":
            yesterday = self.now.date() - timedelta(days=1)
            prior_path = (
                self.root
                / "steward"
                / "scoreboard"
                / f"{yesterday.isoformat()}.json"
            )
            if not prior_path.exists():
                return True, f"not due: no scoreboard exists for {yesterday.isoformat()}"
            try:
                prior = json.loads(prior_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                raise ScoreError(
                    f"cannot read prior scoreboard {prior_path}"
                ) from exc
            prior_rows = prior.get("criteria") if isinstance(prior, Mapping) else None
            if not isinstance(prior_rows, list):
                raise ScoreError("prior scoreboard criteria are malformed")
            red_ids = [
                str(row.get("id"))
                for row in prior_rows
                if isinstance(row, Mapping) and row.get("status") == "red"
            ]
            if not red_ids:
                return True, f"{yesterday.isoformat()} scoreboard has no red criteria"
            issues = self.api(f"repos/{OWNER}/{PROFILE_REPO}/issues?state=open&labels=github-steward&per_page=100")
            if not isinstance(issues, list):
                raise ScoreError("github-steward issue response is malformed")
            corpus = "\n".join(f"{row.get('title', '')}\n{row.get('body', '')}" for row in issues if isinstance(row, Mapping))
            missing = [identifier for identifier in red_ids if identifier not in corpus]
            return not missing, f"{yesterday.isoformat()} red criteria without open issue={missing}"
        if identifier == "readme-receipts-fresh":
            block_match = re.search(r"<!-- recent_receipts starts -->(.*?)<!-- recent_receipts ends -->", profile(), re.S)
            dates = [date.fromisoformat(value) for value in re.findall(r"\b\d{4}-\d{2}-\d{2}\b", block_match.group(1) if block_match else "")]
            threshold = self.now.date() - timedelta(days=1)
            ok = bool(dates) and max(dates) >= threshold
            return ok, f"latest receipt date={max(dates).isoformat() if dates else 'missing'}; threshold={threshold.isoformat()}"
        if identifier == "no-direct-main-from-orca":
            path = self.root / "steward" / "ORCA_PROMPT.md"
            ok = path.exists() and "Do not git push to main" in path.read_text(encoding="utf-8")
            return ok, f"ORCA prompt blocks direct main push={str(ok).lower()}"
        if identifier == "planted-failure":
            definitions = load_criteria(self.root / "steward" / "criteria.yaml")

            def self_test(_criterion: Mapping[str, object]) -> tuple[bool, str]:
                return True, "in-memory plant self-test"

            normal = evaluate_criteria(definitions, self_test)
            planted = evaluate_criteria(
                definitions,
                self_test,
                plant="missing-license",
            )
            changed = [
                index
                for index, (before, after) in enumerate(
                    zip(normal, planted),
                    start=1,
                )
                if before.get("status") != after.get("status")
            ]
            ok = (
                changed == [15]
                and normal[14].get("status") == "green"
                and planted[14].get("status") == "red"
            )
            return ok, f"in-memory planted status changes={changed}"
        raise ScoreError(f"no deterministic implementation for criterion {identifier}")


def _parse_time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ScoreError("GitHub timestamp is missing")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError as exc:
        raise ScoreError(f"invalid GitHub timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise ScoreError("GitHub timestamp lacks a timezone")
    return parsed.astimezone(timezone.utc)


def evaluate_check(criterion: Mapping[str, object]) -> tuple[bool, str]:
    """Reject uncoupled use; a cached ScoringContext must own real checks."""
    raise ScoreError("evaluate_check requires the run-scoped scoring context")


def run_score(
    root: Path,
    *,
    evaluator: Evaluator = evaluate_check,
    plant: str | None = None,
    now: datetime | None = None,
) -> dict[str, object]:
    """Complete one scoring run and write all scoreboard outputs."""
    measured_at = now or datetime.now(timezone.utc)
    criteria_path = root / "steward" / "criteria.yaml"
    criteria = load_criteria(criteria_path)
    selected = ScoringContext(root, measured_at).evaluate if evaluator is evaluate_check else evaluator
    rows = evaluate_criteria(criteria, selected, plant=plant)
    scoreboard = build_scoreboard(criteria_sha256(criteria_path), rows, measured_at)
    if plant is None:
        write_scoreboard(root, scoreboard)
    return scoreboard


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plant", choices=PLANTS)
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        scoreboard = run_score(root, plant=args.plant)
    except ScoreError as exc:
        print(f"score_github: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(scoreboard, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
