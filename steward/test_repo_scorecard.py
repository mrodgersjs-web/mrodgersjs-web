"""Unit tests for steward/repo_scorecard.py. No network: API responses are the
recorded fixtures in steward/fixtures/scorecard/ (real anonymous responses
captured 2026-10-10 with `--record`, runs trimmed to the fields used)."""
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from steward import repo_scorecard as sc

FIXTURES = Path(__file__).with_name("fixtures") / "scorecard"
NOW = datetime(2026, 10, 10, 23, 36, 35, tzinfo=timezone.utc)
CONFIG = sc.load_config()
TH = CONFIG["thresholds"]


def fixture(repo: str, name: str) -> object:
    return json.loads((FIXTURES / f"{repo}.{name}.json").read_text(encoding="utf-8"))


class FixtureApi:
    """Serves recorded responses by endpoint; fails on anything unexpected."""

    def __init__(self, repo: str) -> None:
        self.repo = repo
        self.calls: list[str] = []

    def __call__(self, endpoint: str) -> object:
        self.calls.append(endpoint)
        base = f"repos/mrodgersjs-web/{self.repo}"
        if endpoint == base:
            return fixture(self.repo, "meta")
        for name, prefix in (("runs", "/actions/runs?"), ("releases", "/releases?"), ("issues", "/issues?")):
            if endpoint.startswith(base + prefix):
                return fixture(self.repo, name)
        raise AssertionError(f"unexpected endpoint {endpoint}")


def files_facts(**overrides: object) -> dict[str, object]:
    base = {
        "code_loc": 2000,
        "code_files": 20,
        "markdown_loc": 500,
        "test_files": [f"tests/test_{i}.py" for i in range(5)],
        "entrypoints": ["scripts/smoke.sh"],
        "license_file": "LICENSE",
        "security_file": "SECURITY.md",
        "workflows": [".github/workflows/smoke.yml"],
        "readme_file": "README.md",
        "readme_images": ["assets/demo.gif"],
        "readme_images_broken": [],
    }
    base.update(overrides)
    return base


def write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


class ConfigTests(unittest.TestCase):
    def test_config_lists_the_fourteen_repos(self) -> None:
        self.assertEqual(len(CONFIG["repos"]), 14)
        self.assertIn("rigforge", CONFIG["repos"])

    def test_bad_config_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "c.json"
            path.write_text(json.dumps({"owner": "x", "repos": ["a", "a"], "thresholds": {}}))
            with self.assertRaises(ValueError):
                sc.load_config(path)


class CollectFilesTests(unittest.TestCase):
    def test_counts_code_docs_tests_entrypoints_and_images(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_tree(
                root,
                {
                    "README.md": "# x\n\n![ci](https://img.shields.io/badge/a-b-c.svg)\n![demo](assets/demo.gif)\n![gone](assets/missing.png)\n",
                    "assets/demo.gif": "GIF89a",
                    "pkg/app.py": "import os\n\n\ndef f():\n    return 1\n",
                    "tests/test_app.py": "def test_f():\n    assert True\n",
                    "tests/__init__.py": "",
                    "web/app.test.ts": "it('x', () => {})\n",
                    "node_modules/dep/index.js": "x\n" * 500,
                    "docs/guide.md": "a\n\nb\nc\n",
                    "pyproject.toml": "[project]\nname='x'\n[project.scripts]\nx='pkg.app:f'\n",
                    "scripts/smoke.sh": "echo ok\n",
                    "LICENSE": "MIT\n",
                    ".github/workflows/ci.yml": "on: push\n",
                },
            )
            facts = sc.collect_files(root)
        self.assertEqual(facts["code_loc"], 3 + 2 + 1 + 1)  # app.py, test, .ts, smoke.sh; node_modules skipped
        self.assertEqual(facts["markdown_loc"], 4 + 3)
        self.assertEqual(facts["test_files"], ["tests/test_app.py", "web/app.test.ts"])
        self.assertEqual(facts["entrypoints"], ["pyproject.toml [project.scripts]", "scripts/smoke.sh"])
        self.assertEqual(facts["license_file"], "LICENSE")
        self.assertIsNone(facts["security_file"])
        self.assertEqual(facts["workflows"], [".github/workflows/ci.yml"])
        self.assertEqual(facts["readme_images"], ["assets/demo.gif"])
        self.assertEqual(facts["readme_images_broken"], ["assets/missing.png"])

    def test_badges_are_not_demo_images(self) -> None:
        text = (
            "[![smoke](https://github.com/o/r/actions/workflows/smoke.yml/badge.svg)](x)\n"
            '<img src="https://img.shields.io/badge/x-y-z" />\n'
            '<img src="https://github.com/user-attachments/assets/abc" />\n'
        )
        self.assertEqual(sc.readme_images(text), ["https://github.com/user-attachments/assets/abc"])


class CiTests(unittest.TestCase):
    def runs(self, *rows: tuple[str, str | None]) -> dict[str, object]:
        return {
            "workflow_runs": [
                {"id": i, "name": name, "status": "completed", "conclusion": concl,
                 "html_url": f"https://github.com/o/r/actions/runs/{i}", "head_sha": "abcdef123",
                 "created_at": "2026-10-10T00:00:00Z"}
                for i, (name, concl) in enumerate(rows)
            ]
        }

    def test_skipped_runs_are_ignored_not_scored(self) -> None:
        dim = sc.score_ci(self.runs(("rig-lattice", "skipped"), ("smoke", "success")), ["w.yml"], None)
        self.assertEqual(dim["score"], 1.0)
        self.assertEqual(dim["evidence"]["workflow"], "smoke")
        self.assertEqual(dim["evidence"]["skipped_or_neutral_newer_runs"], 1)
        dim = sc.score_ci(self.runs(("rig-lattice", "skipped"), ("smoke", "failure")), ["w.yml"], None)
        self.assertEqual(dim["score"], 0.0)

    def test_only_skipped_runs_is_neutral(self) -> None:
        dim = sc.score_ci(self.runs(("rig-lattice", "skipped"), ("rig-lattice", "skipped")), ["w.yml"], None)
        self.assertIsNone(dim["score"])

    def test_in_progress_runs_are_passed_over(self) -> None:
        payload = self.runs(("smoke", "success"))
        payload["workflow_runs"].insert(0, {"name": "smoke", "status": "in_progress", "conclusion": None})
        self.assertEqual(sc.score_ci(payload, ["w.yml"], None)["score"], 1.0)

    def test_no_workflows_scores_zero(self) -> None:
        self.assertEqual(sc.score_ci({"workflow_runs": []}, [], None)["score"], 0.0)

    def test_older_failure_of_a_now_skipped_workflow_is_stale(self) -> None:
        dim = sc.score_ci(
            self.runs(("rig-lattice", "skipped"), ("rig-lattice", "failure")), ["w.yml"], None
        )
        self.assertIsNone(dim["score"])

    def test_stale_failure_does_not_beat_a_live_workflow(self) -> None:
        dim = sc.score_ci(
            self.runs(("smoke", "success"), ("rig-lattice", "skipped"), ("rig-lattice", "failure")),
            ["w.yml"], None,
        )
        self.assertEqual(dim["score"], 1.0)

    def test_failure_of_a_live_workflow_still_counts(self) -> None:
        dim = sc.score_ci(
            self.runs(("rig-lattice", "skipped"), ("smoke", "failure"), ("rig-lattice", "failure")),
            ["w.yml"], None,
        )
        self.assertEqual(dim["score"], 0.0)
        self.assertEqual(dim["evidence"]["workflow"], "smoke")

    def test_rig_agent_directory_recorded_runs(self) -> None:
        """Recorded 2026-10-10: newest rig-lattice run skipped, Sept 12 run failed."""
        runs = fixture("rig-agent-directory", "runs")
        self.assertEqual(
            [(r["name"], r["conclusion"]) for r in runs["workflow_runs"]],
            [("rig-lattice", "skipped"), ("rig-lattice", "failure")],
        )
        dim = sc.score_ci(runs, [".github/workflows/rig-lattice.yml"], None)
        self.assertIsNone(dim["score"])


class FixtureScoringTests(unittest.TestCase):
    def score(self, repo: str, files: dict[str, object]) -> dict[str, object]:
        api = FixtureApi(repo)
        facts = sc.fetch_api_facts("mrodgersjs-web", repo, api)
        return sc.score_repo(repo, files, facts, NOW, TH), api

    def test_proof_studio_recorded(self) -> None:
        # File facts as measured from the 2026-10-10 clone.
        row, api = self.score(
            "proof-studio",
            files_facts(code_loc=9477, markdown_loc=1716, test_files=[f"t{i}" for i in range(16)]),
        )
        dims = row["dimensions"]
        self.assertEqual(row["status"], "LIVE")
        self.assertEqual(dims["ci"]["score"], 1.0)
        self.assertEqual(dims["ci"]["evidence"]["workflow"], "smoke")
        self.assertEqual(dims["ci"]["evidence"]["skipped_or_neutral_newer_runs"], 1)
        self.assertEqual(dims["release"]["score"], 0.0)
        self.assertEqual(dims["old_issues"]["evidence"]["count"], 0)
        # open_issues_count was 0, so no issues call is spent.
        self.assertEqual(len(api.calls), 3)
        self.assertEqual(row["next_improvement"]["dimension"], "release")
        self.assertIn("release", row["next_improvement"]["action"])

    def test_strategy_studio_recorded(self) -> None:
        row, api = self.score(
            "strategy-studio",
            files_facts(code_loc=98, markdown_loc=222, test_files=["tests/test_smoke.py"]),
        )
        dims = row["dimensions"]
        self.assertEqual(row["status"], "SCAFFOLD")
        self.assertEqual(dims["ci"]["score"], 0.0)
        self.assertEqual(dims["ci"]["evidence"]["conclusion"], "failure")
        # The issues payload contains only pull requests, which are not issues.
        self.assertEqual(dims["old_issues"]["score"], 1.0)
        self.assertEqual(len(api.calls), 4)
        # ci and release both 0.0: tie broken by DIMENSIONS order, ci first.
        self.assertEqual(row["next_improvement"]["dimension"], "ci")
        self.assertIn("rig-lattice", row["next_improvement"]["action"])

    def test_proof_gate_action_recorded(self) -> None:
        row, _ = self.score(
            "proof-gate-action",
            files_facts(code_loc=127, markdown_loc=119, test_files=["test/verify.test.js"],
                        security_file=None, readme_images=["assets/proof-gate-action-hero.png"]),
        )
        dims = row["dimensions"]
        self.assertEqual(row["status"], "SCAFFOLD")
        self.assertEqual(dims["license_security"]["score"], 0.5)
        self.assertEqual(dims["demo"]["score"], 0.5)
        self.assertEqual(dims["freshness"]["evidence"]["days_since_push"], 32)
        self.assertAlmostEqual(dims["freshness"]["score"], 1 - (32 - 14) / (90 - 14), places=3)

    def test_quota_exhaustion_marks_dimensions_not_measured(self) -> None:
        def api(endpoint: str) -> object:
            raise sc.QuotaExhausted("API quota reserve reached (5 left, reserve 5)")

        facts = sc.fetch_api_facts("mrodgersjs-web", "x", api)
        row = sc.score_repo("x", files_facts(), facts, NOW, TH)
        for key in ("ci", "release", "discoverability", "freshness", "old_issues"):
            self.assertIsNone(row["dimensions"][key]["score"], key)
        self.assertEqual(row["measured_dimensions"], 5)
        self.assertTrue(facts["quota_exhausted"])

    def test_api_client_stops_at_reserve(self) -> None:
        client = sc.GitHubApi(None, reserve=5)
        client.remaining = 5
        with self.assertRaises(sc.QuotaExhausted):
            client("repos/o/r")
        self.assertEqual(client.calls, 0)


class CalibrationTests(unittest.TestCase):
    """2026-10-10 audit: these code LOC figures are SCAFFOLD; live repos are larger."""

    SCAFFOLD = {"strategy-studio": 98, "app-factory-studio": 115, "agency-studio": 50,
                "rig-agent-directory": 45, "proof-gate-action": 127, "fde-portfolio": 50, "doctrine": 4}
    LIVE = {"design-studio": 720, "communications-studio": 2351, "mesh-studio": 2891,
            "jake-studio": 4722, "proof-studio": 9477, "rigforge": 10496, "deviatrix-genesis": 14079}

    def test_status_matches_audit(self) -> None:
        for repo, loc in {**self.SCAFFOLD, **self.LIVE}.items():
            row = sc.score_repo(repo, files_facts(code_loc=loc), {}, NOW, TH)
            expected = "SCAFFOLD" if repo in self.SCAFFOLD else "LIVE"
            self.assertEqual(row["status"], expected, repo)
            if expected == "SCAFFOLD":
                self.assertLess(row["dimensions"]["code_vs_docs"]["score"], 0.6, repo)


class PickTests(unittest.TestCase):
    def dims(self, **scores: float | None) -> dict[str, dict[str, object]]:
        out = {k: {"score": 1.0, "evidence": {}} for k in sc.DIMENSION_IDS}
        for key, value in scores.items():
            out[key] = {"score": value, "evidence": {}}
        return out

    def test_lowest_wins(self) -> None:
        d = self.dims(tests=0.4, freshness=0.2)
        d["freshness"]["evidence"] = {"days_since_push": 75}
        p = sc.pick(d, TH)
        self.assertEqual(p["dimension"], "freshness")
        self.assertEqual(p["action"], "Last push was 75 days ago; ship one small verified change.")

    def test_tie_uses_priority_order(self) -> None:
        d = self.dims(release=0.0, tests=0.0)
        d["tests"]["evidence"] = {"test_files": 0}
        self.assertEqual(sc.pick(d, TH)["dimension"], "tests")

    def test_scaffold_prefers_code_then_tests_before_release(self) -> None:
        d = self.dims(release=0.0, tests=0.0, code_vs_docs=0.0, ci=0.0)
        d["code_vs_docs"]["evidence"] = {"code_loc": 45, "markdown_loc": 554}
        d["tests"]["evidence"] = {"test_files": 0}
        self.assertEqual(sc.pick(d, TH, "SCAFFOLD")["dimension"], "code_vs_docs")
        d["code_vs_docs"]["score"] = 1.0
        self.assertEqual(sc.pick(d, TH, "SCAFFOLD")["dimension"], "tests")
        d["tests"]["score"] = 1.0
        self.assertEqual(sc.pick(d, TH, "SCAFFOLD")["dimension"], "ci")
        d["ci"]["score"] = 1.0
        d["release"]["evidence"] = {}
        self.assertEqual(sc.pick(d, TH, "SCAFFOLD")["dimension"], "release")

    def test_scaffold_priority_never_overrides_a_lower_score(self) -> None:
        d = self.dims(release=0.0, code_vs_docs=0.09)
        d["code_vs_docs"]["evidence"] = {"code_loc": 45, "markdown_loc": 554}
        self.assertEqual(sc.pick(d, TH, "SCAFFOLD")["dimension"], "release")

    def test_live_repo_keeps_default_tie_order(self) -> None:
        d = self.dims(release=0.0, code_vs_docs=0.0)
        d["code_vs_docs"]["evidence"] = {"code_loc": 5000, "markdown_loc": 10}
        self.assertEqual(sc.pick(d, TH, "LIVE")["dimension"], "code_vs_docs")
        self.assertEqual(sc.pick(d, TH)["dimension"], "code_vs_docs")

    def test_scaffold_row_from_score_repo_uses_scaffold_order(self) -> None:
        row = sc.score_repo(
            "x", files_facts(code_loc=45, markdown_loc=554, test_files=[], license_file=None,
                             security_file=None, entrypoints=[], readme_images=[]),
            {}, NOW, TH)
        self.assertEqual(row["status"], "SCAFFOLD")
        self.assertEqual(row["next_improvement"]["dimension"], "tests")

    def test_neutral_dimensions_are_never_picked(self) -> None:
        d = self.dims(ci=None, demo=0.5)
        d["demo"]["evidence"] = {"images": ["a.png"], "broken": []}
        p = sc.pick(d, TH)
        self.assertEqual(p["dimension"], "demo")
        self.assertIn("GIF", p["action"])

    def test_all_full_picks_nothing(self) -> None:
        self.assertIsNone(sc.pick(self.dims(), TH)["dimension"])

    def test_every_dimension_has_an_action(self) -> None:
        evidence = {"ci": {"reason": "no .github/workflows files"}, "tests": {"test_files": 1},
                    "code_vs_docs": {"code_loc": 4, "markdown_loc": 1958}, "entrypoint": {},
                    "license_security": {"license_file": "LICENSE"}, "release": {}, "demo": {},
                    "discoverability": {"topics": 2, "description_chars": 10},
                    "freshness": {"days_since_push": 40},
                    "old_issues": {"count": 2, "numbers": [3, 4], "older_than_days": 30}}
        for key in sc.DIMENSION_IDS:
            action = sc.action_for(key, evidence[key], TH)
            self.assertTrue(action and "\n" not in action, key)
        self.assertEqual(sc.action_for("license_security", evidence["license_security"], TH), "Add SECURITY.md at the repo root.")


class RunAndRenderTests(unittest.TestCase):
    def test_run_writes_one_row_per_repo_and_survives_clone_failure(self) -> None:
        config = {**CONFIG, "repos": ["proof-studio", "ghost"]}

        def clone(owner: str, repo: str, dest: Path) -> str:
            if repo == "ghost":
                raise subprocess.CalledProcessError(128, ["git", "clone"])
            write_tree(dest, {"README.md": "# x\n", "a.py": "x = 1\n"})
            return "f" * 40

        def api(endpoint: str) -> object:
            if "proof-studio" in endpoint:
                return FixtureApi("proof-studio")(endpoint)
            raise sc.ApiError("HTTP 404", 404)

        payload = sc.run(config, NOW, api, clone=clone)
        payload["api"] = {"calls": 0, "authenticated": False, "remaining": None}
        self.assertEqual([r["repo"] for r in payload["repos"]], ["proof-studio", "ghost"])
        ghost = payload["repos"][1]
        self.assertEqual(ghost["clone_error"], "clone failed: CalledProcessError")
        self.assertEqual(ghost["measured_dimensions"], 0)
        md = sc.render_markdown(payload)
        self.assertIn("| [proof-studio](https://github.com/mrodgersjs-web/proof-studio) | SCAFFOLD |", md)  # tiny fake tree
        self.assertIn("**ghost** (none, n/a): Nothing measured", md)
        for word in ("unlock", "empower", "synergy", "leverage", "disrupt", "world-class", "!"):
            self.assertNotIn(word, md.lower())
        json.dumps(payload)  # serialisable


if __name__ == "__main__":
    unittest.main()
