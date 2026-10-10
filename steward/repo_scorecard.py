#!/usr/bin/env python3
"""Per-repo scorecard: the Measure + Pick half of the nightly improvement loop.

Measure: score each configured public repo on ten dimensions (each 0-1, with
the raw evidence kept). File facts come from an anonymous shallow `git clone`
over https, which costs no API quota. Only four kinds of REST reads are made
per repo (repo metadata, Actions runs, releases, and issues only when the repo
has open issues), with GH_TOKEN or GITHUB_TOKEN when set and anonymous
otherwise.

Pick: name the single lowest dimension per repo as the next improvement, with
one concrete action.

Outputs: steward/scoreboard/repos.json and steward/scoreboard/SCORECARD.md.
Stdlib only. Config: steward/scorecard.json.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).with_name("scorecard.json")
SCHEMA = "steward.repo-scorecard/v1"

# Order is also the tie-break priority for the Pick step: when two dimensions
# share the lowest score, the earlier one is picked.
DIMENSIONS = (
    ("ci", "CI"),
    ("tests", "Tests"),
    ("code_vs_docs", "Code vs docs"),
    ("entrypoint", "Entrypoint"),
    ("license_security", "LICENSE + SECURITY"),
    ("release", "Release"),
    ("demo", "Demo image"),
    ("discoverability", "Topics + description"),
    ("freshness", "Freshness"),
    ("old_issues", "Old issues"),
)
DIMENSION_IDS = tuple(key for key, _ in DIMENSIONS)

# Conclusions that are neither pass nor fail. Skipped runs (for example the
# rig-lattice workflow once it is changed to skip) are ignored when looking
# for the latest run.
NEUTRAL_CONCLUSIONS = frozenset({"skipped", "neutral", "stale", None, ""})
PASS_CONCLUSIONS = frozenset({"success"})

SKIP_DIRS = frozenset(
    {
        ".git",
        "node_modules",
        "vendor",
        "dist",
        "build",
        ".venv",
        "venv",
        "env",
        "__pycache__",
        "site-packages",
        ".next",
        ".tox",
        "coverage",
        "target",
    }
)
CODE_EXTS = frozenset(
    {
        ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".go", ".rs",
        ".java", ".kt", ".rb", ".php", ".swift", ".c", ".h", ".cc", ".cpp",
        ".hpp", ".cs", ".sh", ".bash", ".zsh", ".lua", ".scala", ".sql",
        ".vue", ".svelte", ".dart", ".ex", ".exs",
    }
)
DOC_EXTS = frozenset({".md", ".mdx", ".markdown", ".rst"})
MAX_FILE_BYTES = 1_000_000
TEST_NAME = re.compile(
    r"(^test_.+\.py$)|(.+_test\.(py|go)$)|(.+\.(test|spec)\.(js|mjs|cjs|ts|tsx|jsx)$)"
    r"|(^test_.+\.(sh|bash)$)"
)
TEST_DIRS = frozenset({"tests", "test", "__tests__", "spec"})
IMAGE_EXT = re.compile(r"\.(gif|png|jpe?g|webp|svg|mp4|webm|mov)(\?|#|$)", re.I)
BADGE_HINT = re.compile(
    r"shields\.io|badge|/actions/workflows/|codecov\.io|badgen\.net|/workflows/.+/badge",
    re.I,
)
ANIMATED = re.compile(r"\.(gif|mp4|webm|mov)(\?|#|$)|user-attachments/assets/", re.I)
MD_IMAGE = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)")
HTML_IMAGE = re.compile(r"<(?:img|video|source)\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)", re.I)

Api = Callable[[str], object]


class ApiError(RuntimeError):
    def __init__(self, message: str, status: int = 0) -> None:
        super().__init__(message)
        self.status = status


class QuotaExhausted(ApiError):
    """Stop spending calls: remaining quota is at or below the reserve."""


# --------------------------------------------------------------------------
# Config


def load_config(path: Path = CONFIG_PATH) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    owner = data.get("owner")
    repos = data.get("repos")
    th = data.get("thresholds")
    if not isinstance(owner, str) or not re.fullmatch(r"[A-Za-z0-9-]{1,39}", owner):
        raise ValueError("scorecard.json: owner must be a GitHub login")
    if (
        not isinstance(repos, list)
        or not repos
        or any(not isinstance(r, str) or not re.fullmatch(r"[A-Za-z0-9._-]{1,100}", r) for r in repos)
        or len(set(repos)) != len(repos)
    ):
        raise ValueError("scorecard.json: repos must be a non-empty list of unique repo names")
    if not isinstance(th, dict) or any(not isinstance(v, (int, float)) for v in th.values()):
        raise ValueError("scorecard.json: thresholds must map names to numbers")
    return data


# --------------------------------------------------------------------------
# GitHub REST client (frugal)


class GitHubApi:
    """Minimal REST GET client that counts calls and respects a quota reserve."""

    def __init__(self, token: Optional[str], reserve: int = 5, timeout: int = 25) -> None:
        self.token = token or None
        self.reserve = reserve
        self.timeout = timeout
        self.calls = 0
        self.remaining: Optional[int] = None
        self.limit: Optional[int] = None

    @property
    def authenticated(self) -> bool:
        return self.token is not None

    def __call__(self, endpoint: str) -> object:
        if endpoint.startswith(("/", "-")) or "://" in endpoint:
            raise ApiError("use a relative endpoint")
        if self.remaining is not None and self.remaining <= self.reserve:
            raise QuotaExhausted(
                f"API quota reserve reached ({self.remaining} left, reserve {self.reserve})"
            )
        request = urllib.request.Request(
            "https://api.github.com/" + endpoint,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "mrodgersjs-web-steward-scorecard",
                **({"Authorization": f"Bearer {self.token}"} if self.token else {}),
            },
        )
        self.calls += 1
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                self._note_quota(response.headers)
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            self._note_quota(exc.headers)
            if exc.code in (403, 429) and self.remaining == 0:
                raise QuotaExhausted(f"HTTP {exc.code}: rate limit exhausted", exc.code) from None
            raise ApiError(f"HTTP {exc.code} for {endpoint}", exc.code) from None
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise ApiError(f"network error for {endpoint}: {exc}") from None

    def _note_quota(self, headers: Optional[Mapping[str, str]]) -> None:
        if not headers:
            return
        remaining = headers.get("X-RateLimit-Remaining")
        limit = headers.get("X-RateLimit-Limit")
        if remaining is not None and str(remaining).isdigit():
            self.remaining = int(remaining)
        if limit is not None and str(limit).isdigit():
            self.limit = int(limit)


# --------------------------------------------------------------------------
# Measure: file facts from a shallow clone


def clone_repo(owner: str, repo: str, dest: Path) -> str:
    """Anonymous shallow clone over https. Returns the HEAD commit sha."""
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0", "GIT_ASKPASS": "true"}
    url = f"https://github.com/{owner}/{repo}.git"
    subprocess.run(
        ["git", "clone", "--quiet", "--depth", "1", "--no-tags", url, str(dest)],
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
        env=env,
    )
    head = subprocess.run(
        ["git", "-C", str(dest), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return head.stdout.strip()


def _nonblank_lines(path: Path) -> int:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return 0
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    return sum(1 for line in text.splitlines() if line.strip())


def _is_test_file(rel: Path) -> bool:
    name = rel.name
    if TEST_NAME.match(name):
        return True
    if rel.suffix in CODE_EXTS and name not in ("__init__.py", "conftest.py"):
        return any(part in TEST_DIRS for part in rel.parts[:-1])
    return False


def _read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _entrypoints(root: Path, files: set[str]) -> list[str]:
    found: list[str] = []
    pyproject = root / "pyproject.toml"
    if "pyproject.toml" in files:
        text = pyproject.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"^\[(project\.scripts|tool\.poetry\.scripts|project\.gui-scripts)\]", text, re.M):
            found.append("pyproject.toml [project.scripts]")
    for name in ("setup.py", "setup.cfg"):
        if name in files and "console_scripts" in (root / name).read_text(encoding="utf-8", errors="ignore"):
            found.append(f"{name} console_scripts")
    if "package.json" in files:
        pkg = _read_json(root / "package.json")
        if isinstance(pkg, dict):
            if pkg.get("bin"):
                found.append("package.json bin")
            scripts = pkg.get("scripts") if isinstance(pkg.get("scripts"), dict) else {}
            for key in ("start", "dev", "serve"):
                if scripts.get(key):
                    found.append(f"package.json scripts.{key}")
                    break
    for rel in sorted(files):
        name = rel.rsplit("/", 1)[-1]
        depth = rel.count("/")
        if name == "__main__.py":
            found.append(rel)
        elif depth == 0 and name in (
            "main.py", "app.py", "cli.py", "server.py", "main.go", "Makefile",
            "Dockerfile", "docker-compose.yml", "compose.yaml", "action.yml", "action.yaml",
        ):
            found.append(rel)
        elif depth <= 1 and re.fullmatch(r"(scripts/)?(smoke|run|start|demo)\.sh", rel):
            found.append(rel)
        elif rel == "src/main.rs" or re.fullmatch(r"cmd/[^/]+/main\.go", rel):
            found.append(rel)
    # de-duplicate, keep order
    seen: set[str] = set()
    return [x for x in found if not (x in seen or seen.add(x))]


def readme_images(text: str) -> list[str]:
    """Non-badge image or video URLs referenced by a README."""
    urls = MD_IMAGE.findall(text) + HTML_IMAGE.findall(text)
    keep = []
    for url in urls:
        if BADGE_HINT.search(url):
            continue
        if IMAGE_EXT.search(url) or "user-attachments" in url or "user-images.githubusercontent" in url:
            keep.append(url)
    return keep


def collect_files(root: Path) -> dict[str, object]:
    """Walk a checkout and return the raw file facts the scorer needs."""
    files: set[str] = set()
    code_loc = 0
    doc_loc = 0
    code_files = 0
    tests: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for filename in sorted(filenames):
            full = Path(dirpath) / filename
            if full.is_symlink() or not full.is_file():
                continue
            rel = full.relative_to(root)
            rel_s = rel.as_posix()
            files.add(rel_s)
            suffix = rel.suffix.lower()
            if filename.endswith((".min.js", ".min.css")):
                continue
            if suffix in CODE_EXTS:
                code_loc += _nonblank_lines(full)
                code_files += 1
            elif suffix in DOC_EXTS:
                doc_loc += _nonblank_lines(full)
            if _is_test_file(rel):
                tests.append(rel_s)
    readme_name = next(
        (n for n in ("README.md", "README.rst", "README", "readme.md", "Readme.md") if n in files),
        None,
    )
    readme_text = (
        (root / readme_name).read_text(encoding="utf-8", errors="ignore") if readme_name else ""
    )
    license_name = next(
        (n for n in sorted(files) if "/" not in n and re.fullmatch(r"(LICEN[CS]E|COPYING)(\.[a-z]+)?", n, re.I)),
        None,
    )
    security_name = next(
        (
            n
            for n in ("SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md")
            if n in files
        ),
        None,
    )
    images = readme_images(readme_text)
    readme_dir = (root / readme_name).parent if readme_name else root

    def _is_broken(url: str) -> bool:
        if re.match(r"[a-z]+:", url, re.I) or url.startswith("//"):
            return False  # remote URL: not checked, no network spent
        local = (readme_dir / urllib.parse.unquote(url.split("#")[0].split("?")[0])).resolve()
        return not (local.is_file() and root.resolve() in local.parents)

    workflows = sorted(
        f for f in files if re.fullmatch(r"\.github/workflows/[^/]+\.ya?ml", f)
    )
    return {
        "code_loc": code_loc,
        "code_files": code_files,
        "markdown_loc": doc_loc,
        "test_files": sorted(tests),
        "entrypoints": _entrypoints(root, files),
        "license_file": license_name,
        "security_file": security_name,
        "workflows": workflows,
        "readme_file": readme_name,
        "readme_images": [u for u in images if not _is_broken(u)],
        "readme_images_broken": [u for u in images if _is_broken(u)],
    }


# --------------------------------------------------------------------------
# Measure: API facts


def _trim_runs(payload: object) -> list[dict[str, object]]:
    runs = payload.get("workflow_runs", []) if isinstance(payload, dict) else []
    keep = ("id", "name", "status", "conclusion", "event", "head_branch", "head_sha", "html_url", "created_at", "updated_at")
    return [{k: r.get(k) for k in keep} for r in runs if isinstance(r, dict)]


def fetch_api_facts(owner: str, repo: str, api: Api, record: Optional[Path] = None) -> dict[str, object]:
    """Fetch the raw API facts for one repo. Missing parts are recorded as errors."""
    facts: dict[str, object] = {"errors": []}
    errors: list[str] = facts["errors"]  # type: ignore[assignment]
    base = f"repos/{owner}/{repo}"

    def get(name: str, endpoint: str) -> object:
        try:
            value = api(endpoint)
        except QuotaExhausted:
            raise
        except ApiError as exc:
            errors.append(f"{name}: {exc}")
            return None
        if record is not None:
            record.mkdir(parents=True, exist_ok=True)
            trimmed = {"workflow_runs": _trim_runs(value)} if name == "runs" else value
            (record / f"{repo}.{name}.json").write_text(
                json.dumps(trimmed, indent=1, sort_keys=True) + "\n", encoding="utf-8"
            )
        return value

    try:
        meta = get("meta", base)
        facts["meta"] = meta
        branch = meta.get("default_branch") if isinstance(meta, dict) else None
        if branch:
            q = urllib.parse.urlencode(
                {"branch": branch, "per_page": 30, "exclude_pull_requests": "true"}
            )
            facts["runs"] = get("runs", f"{base}/actions/runs?{q}")
        facts["releases"] = get("releases", f"{base}/releases?per_page=1")
        open_count = meta.get("open_issues_count") if isinstance(meta, dict) else None
        if open_count == 0:
            facts["issues"] = []
            facts["issues_note"] = "open_issues_count is 0; no issues call made"
        else:
            q = urllib.parse.urlencode(
                {"state": "open", "per_page": 100, "sort": "created", "direction": "asc"}
            )
            facts["issues"] = get("issues", f"{base}/issues?{q}")
    except QuotaExhausted as exc:
        errors.append(str(exc))
        facts["quota_exhausted"] = True
    return facts


# --------------------------------------------------------------------------
# Score (pure)


def _parse_time(value: object) -> Optional[datetime]:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _dim(score: Optional[float], **evidence: object) -> dict[str, object]:
    return {
        "score": None if score is None else round(max(0.0, min(1.0, float(score))), 3),
        "evidence": evidence,
    }


def _not_measured(reason: str) -> dict[str, object]:
    return _dim(None, not_measured=reason)


def score_ci(runs_payload: object, workflows: list[str], api_reason: Optional[str]) -> dict[str, object]:
    if runs_payload is None:
        if not workflows:
            return _dim(0.0, workflows=[], reason="no .github/workflows files")
        return _not_measured(api_reason or "actions runs not fetched")
    runs = _trim_runs(runs_payload)
    skipped = 0
    for run in runs:  # API order: newest first
        if run.get("status") != "completed":
            continue
        if run.get("conclusion") in NEUTRAL_CONCLUSIONS:
            skipped += 1
            continue
        conclusion = run.get("conclusion")
        return _dim(
            1.0 if conclusion in PASS_CONCLUSIONS else 0.0,
            conclusion=conclusion,
            workflow=run.get("name"),
            run_url=run.get("html_url"),
            head_sha=(run.get("head_sha") or "")[:7],
            created_at=run.get("created_at"),
            skipped_or_neutral_newer_runs=skipped,
        )
    if not workflows:
        return _dim(0.0, workflows=[], runs_seen=len(runs), reason="no .github/workflows files")
    return _dim(
        None,
        workflows=workflows,
        runs_seen=len(runs),
        skipped_or_neutral=skipped,
        reason="no completed non-skipped run on the default branch (neutral)",
    )


def score_repo(
    name: str,
    files: Optional[Mapping[str, object]],
    api: Optional[Mapping[str, object]],
    now: datetime,
    th: Mapping[str, float],
) -> dict[str, object]:
    """Score one repo from raw facts. Never raises on missing facts: a dimension
    that could not be measured gets score None and is left out of the average
    and the Pick step."""
    dims: dict[str, dict[str, object]] = {}
    api = api or {}
    api_errors = list(api.get("errors", []) or [])
    api_reason = "; ".join(api_errors) if api_errors else ("API not called" if not api else None)
    meta = api.get("meta") if isinstance(api.get("meta"), dict) else None

    if files is None:
        for key in ("tests", "entrypoint", "code_vs_docs", "demo"):
            dims[key] = _not_measured("clone failed")
        workflows: list[str] = []
    else:
        workflows = list(files.get("workflows", []))
        tests = list(files.get("test_files", []))
        dims["tests"] = _dim(
            len(tests) / th["tests_full_score"], test_files=len(tests), sample=tests[:5]
        )
        entry = list(files.get("entrypoints", []))
        dims["entrypoint"] = _dim(1.0 if entry else 0.0, found=entry)
        code = int(files.get("code_loc", 0))
        docs = int(files.get("markdown_loc", 0))
        share = code / (code + docs) if code + docs else 0.0
        size_part = min(1.0, code / th["code_loc_full_score"])
        share_part = min(1.0, share / th["code_share_full_score"])
        dims["code_vs_docs"] = _dim(
            0.5 * size_part + 0.5 * share_part,
            code_loc=code,
            markdown_loc=docs,
            code_share=round(share, 3),
            scaffold=code <= th["scaffold_max_code_loc"],
        )
        images = list(files.get("readme_images", []))
        moving = [u for u in images if ANIMATED.search(u)]
        dims["demo"] = _dim(
            1.0 if moving else (0.5 if images else 0.0),
            readme=files.get("readme_file"),
            animated=moving[:3],
            images=images[:3],
            broken=list(files.get("readme_images_broken", []))[:3],
        )

    # CI
    if "runs" in api:
        dims["ci"] = score_ci(api.get("runs"), workflows, api_reason)
    elif files is not None and not workflows:
        dims["ci"] = _dim(0.0, workflows=[], reason="no .github/workflows files")
    else:
        dims["ci"] = _not_measured(api_reason or "actions runs not fetched")

    # LICENSE + SECURITY: clone first, repo metadata as a cross-check.
    if files is not None:
        lic = files.get("license_file")
        sec = files.get("security_file")
        spdx = None
        if meta and isinstance(meta.get("license"), dict):
            spdx = meta["license"].get("spdx_id")
        dims["license_security"] = _dim(
            0.5 * bool(lic) + 0.5 * bool(sec), license_file=lic, license_spdx=spdx, security_file=sec
        )
    else:
        dims["license_security"] = _not_measured("clone failed")

    # Release
    releases = api.get("releases")
    if isinstance(releases, list):
        latest = releases[0] if releases else None
        dims["release"] = _dim(
            1.0 if latest else 0.0,
            latest_tag=latest.get("tag_name") if isinstance(latest, dict) else None,
            published_at=latest.get("published_at") if isinstance(latest, dict) else None,
        )
    else:
        dims["release"] = _not_measured(api_reason or "releases not fetched")

    if meta:
        topics = meta.get("topics") or []
        desc = (meta.get("description") or "").strip()
        dims["discoverability"] = _dim(
            0.5 * min(1.0, len(topics) / th["topics_full_score"])
            + 0.5 * min(1.0, len(desc) / th["description_full_score"]),
            topics=len(topics),
            description_chars=len(desc),
        )
        pushed = _parse_time(meta.get("pushed_at"))
        if pushed is None:
            dims["freshness"] = _not_measured("pushed_at missing")
        else:
            days = max(0, (now - pushed).days)
            fresh, stale = th["fresh_days"], th["stale_days"]
            score = 1.0 if days <= fresh else max(0.0, 1 - (days - fresh) / (stale - fresh))
            dims["freshness"] = _dim(score, days_since_push=days, pushed_at=meta.get("pushed_at"))
    else:
        dims["discoverability"] = _not_measured(api_reason or "repo metadata not fetched")
        dims["freshness"] = _not_measured(api_reason or "repo metadata not fetched")

    issues = api.get("issues")
    if isinstance(issues, list):
        cutoff_days = th["old_issue_days"]
        old = []
        for issue in issues:
            if not isinstance(issue, dict) or "pull_request" in issue:
                continue
            created = _parse_time(issue.get("created_at"))
            if created and (now - created).days > cutoff_days:
                old.append(issue.get("number"))
        dims["old_issues"] = _dim(
            1 - len(old) / th["old_issues_zero_score"],
            older_than_days=cutoff_days,
            count=len(old),
            numbers=old[:10],
            note=api.get("issues_note"),
        )
    else:
        dims["old_issues"] = _not_measured(api_reason or "issues not fetched")

    ordered = {key: dims[key] for key in DIMENSION_IDS}
    measured = [d["score"] for d in ordered.values() if d["score"] is not None]
    overall = round(sum(measured) / len(measured), 3) if measured else None
    code_dim = ordered["code_vs_docs"]["evidence"]
    if "code_loc" in code_dim:
        status = "SCAFFOLD" if code_dim["scaffold"] else "LIVE"
    else:
        status = "UNKNOWN"
    return {
        "repo": name,
        "status": status,
        "overall": overall,
        "measured_dimensions": len(measured),
        "dimensions": ordered,
        "next_improvement": pick(ordered, th),
    }


# --------------------------------------------------------------------------
# Pick (pure)


def action_for(key: str, evidence: Mapping[str, object], th: Optional[Mapping[str, float]] = None) -> str:
    th = th or {}
    if key == "ci":
        if evidence.get("reason", "").startswith("no .github/workflows"):
            return "Add a CI workflow under .github/workflows that runs the tests on every push to the default branch."
        return (
            f"Fix the latest default-branch run of '{evidence.get('workflow')}' "
            f"({evidence.get('conclusion')}, {evidence.get('run_url')}) so it passes."
        )
    if key == "tests":
        have = evidence.get("test_files", 0)
        return f"Add tests: {have} test file(s) found; add at least {max(1, int(th.get('tests_full_score', 5)) - int(have))} more that run in CI."
    if key == "code_vs_docs":
        return (
            f"Build the working code the README describes: {evidence.get('code_loc')} code lines "
            f"vs {evidence.get('markdown_loc')} markdown lines today."
        )
    if key == "entrypoint":
        return "Add one runnable command (scripts/smoke.sh, a [project.scripts] entry, or package.json bin) and show it in the README."
    if key == "license_security":
        missing = [n for n, v in (("LICENSE", evidence.get("license_file")), ("SECURITY.md", evidence.get("security_file"))) if not v]
        return f"Add {' and '.join(missing)} at the repo root."
    if key == "release":
        return "Publish a first GitHub release (for example v0.1.0) from the current default branch."
    if key == "demo":
        if evidence.get("broken") and not evidence.get("images"):
            return f"Fix the broken README image path(s) {', '.join(evidence['broken'])} and add a GIF of the tool running."
        if evidence.get("images"):
            return "Replace the static README image with a short GIF of the tool running."
        return "Add a short GIF of the tool running near the top of the README."
    if key == "discoverability":
        parts = []
        need_topics = int(th.get("topics_full_score", 5)) - int(evidence.get("topics", 0))
        if need_topics > 0:
            parts.append(f"add {need_topics} more topic(s) (has {evidence.get('topics')})")
        need_chars = int(th.get("description_full_score", 60))
        if int(evidence.get("description_chars", 0)) < need_chars:
            parts.append(f"write a description of at least {need_chars} characters (has {evidence.get('description_chars')})")
        return ("In the repo About box, " + " and ".join(parts) + ".") if parts else "Review topics and description."
    if key == "freshness":
        return f"Last push was {evidence.get('days_since_push')} days ago; ship one small verified change."
    if key == "old_issues":
        nums = ", ".join(f"#{n}" for n in evidence.get("numbers", []))
        return f"Close or answer {evidence.get('count')} open issue(s) older than {evidence.get('older_than_days')} days ({nums})."
    raise KeyError(key)


def pick(dims: Mapping[str, Mapping[str, object]], th: Optional[Mapping[str, float]] = None) -> dict[str, object]:
    """Lowest measured dimension; ties broken by DIMENSIONS order."""
    candidates = [
        (dims[key]["score"], index, key)
        for index, key in enumerate(DIMENSION_IDS)
        if key in dims and dims[key]["score"] is not None
    ]
    if not candidates:
        return {"dimension": None, "score": None, "action": "Nothing measured; fix the scorer inputs first."}
    score, _, key = min(candidates)
    if score >= 1.0:
        return {"dimension": None, "score": 1.0, "action": "All measured dimensions are at 1.0; nothing to pick."}
    return {"dimension": key, "score": score, "action": action_for(key, dims[key]["evidence"], th)}


# --------------------------------------------------------------------------
# Render


def _cell(score: Optional[float]) -> str:
    return "n/a" if score is None else f"{score:.2f}"


def render_markdown(payload: Mapping[str, object]) -> str:
    labels = dict(DIMENSIONS)
    lines = [
        "# Repo scorecard",
        "",
        f"Measured `{payload['measured_at']}` by `steward/repo_scorecard.py`. "
        "Each dimension is scored 0 to 1; `n/a` means it could not be measured this run "
        "(skipped CI runs count as n/a, not pass or fail). Raw evidence is in `repos.json`.",
        "",
        "| Repo | Status | Overall | " + " | ".join(labels[k] for k in DIMENSION_IDS) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in DIMENSION_IDS) + " |",
    ]
    for row in payload["repos"]:
        dims = row.get("dimensions") or {}
        cells = [_cell(dims[k]["score"]) if k in dims else "n/a" for k in DIMENSION_IDS]
        lines.append(
            f"| [{row['repo']}](https://github.com/{payload['owner']}/{row['repo']}) | {row['status']} "
            f"| {_cell(row.get('overall'))} | " + " | ".join(cells) + " |"
        )
    lines += ["", "## Next improvement per repo", ""]
    for row in payload["repos"]:
        pick_row = row["next_improvement"]
        label = labels.get(pick_row.get("dimension"), "none")
        lines.append(f"- **{row['repo']}** ({label}, {_cell(pick_row.get('score'))}): {pick_row['action']}")
    api = payload.get("api", {})
    lines += [
        "",
        f"API calls this run: {api.get('calls')} ({'token' if api.get('authenticated') else 'anonymous'}); "
        f"quota left: {api.get('remaining')}.",
        "",
    ]
    return "\n".join(lines)


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


# --------------------------------------------------------------------------
# Run


def run(
    config: Mapping[str, object],
    now: datetime,
    api: Optional[Api],
    clone: Callable[[str, str, Path], str] = clone_repo,
    only: Optional[list[str]] = None,
    record: Optional[Path] = None,
) -> dict[str, object]:
    owner = str(config["owner"])
    th = config["thresholds"]  # type: ignore[assignment]
    repos = [r for r in config["repos"] if not only or r in only]  # type: ignore[union-attr]
    rows = []
    for repo in repos:
        files = None
        head = None
        clone_error = None
        with tempfile.TemporaryDirectory(prefix="scorecard-") as tmp:
            dest = Path(tmp) / repo
            try:
                head = clone(owner, repo, dest)
                files = collect_files(dest)
            except (subprocess.SubprocessError, OSError) as exc:
                clone_error = f"clone failed: {type(exc).__name__}"
        api_facts = fetch_api_facts(owner, repo, api, record) if api is not None else {}
        row = score_repo(repo, files, api_facts, now, th)  # type: ignore[arg-type]
        row["head_sha"] = head
        if clone_error:
            row["clone_error"] = clone_error
        if api_facts.get("errors"):
            row["api_errors"] = api_facts["errors"]
        rows.append(row)
    return {
        "schema": SCHEMA,
        "owner": owner,
        "measured_at": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "dimensions": [k for k in DIMENSION_IDS],
        "thresholds": th,
        "repos": rows,
    }


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo", action="append", help="score only this repo (repeatable)")
    parser.add_argument("--no-api", action="store_true", help="file facts only; spend no API calls")
    parser.add_argument("--no-write", action="store_true", help="print JSON, do not write scoreboard files")
    parser.add_argument("--out", type=Path, default=ROOT / "steward" / "scoreboard")
    parser.add_argument("--record", type=Path, help="save trimmed raw API responses here (fixtures)")
    args = parser.parse_args(argv)

    config = load_config()
    if args.repo:
        unknown = sorted(set(args.repo) - set(config["repos"]))  # type: ignore[arg-type]
        if unknown:
            parser.error(f"not in scorecard.json: {', '.join(unknown)}")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    client = None if args.no_api else GitHubApi(token, reserve=int(config["thresholds"].get("api_reserve", 5)))  # type: ignore[union-attr]
    now = datetime.now(timezone.utc)
    payload = run(config, now, client, only=args.repo, record=args.record)
    payload["api"] = {
        "calls": client.calls if client else 0,
        "authenticated": bool(client and client.authenticated),
        "remaining": client.remaining if client else None,
    }
    if not args.no_write:
        _atomic_write(args.out / "repos.json", json.dumps(payload, indent=2, sort_keys=False) + "\n")
        _atomic_write(args.out / "SCORECARD.md", render_markdown(payload))
    print(json.dumps(payload, indent=2))
    measured = [r for r in payload["repos"] if r["measured_dimensions"]]
    if not measured:
        print("scorecard: no repo could be measured", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
