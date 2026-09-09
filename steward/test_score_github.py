from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from steward import judge
from steward import score_github as subject


ROOT = Path(__file__).resolve().parents[1]
CRITERIA_PATH = Path(__file__).with_name("criteria.yaml")
EXPECTED_IDS = (
    "profile-readme-exists",
    "banner-200",
    "no-phone",
    "contact-email",
    "bio-fde",
    "blog-url",
    "location-denver",
    "hireable",
    "linkedin-social",
    "pins-six",
    "following-20",
    "live-repo-count",
    "public-cap",
    "every-desc",
    "every-license",
    "no-empty-stub",
    "birch-private",
    "openwork-private",
    "omniscout-private",
    "legacy-site-private",
    "no-abs-home-paths",
    "no-pycache",
    "no-env-files",
    "flagship-homepage",
    "topics-baseline",
    "topics-specific",
    "desc-no-typo",
    "default-main",
    "clone-org",
    "unique-desc",
    "readme-exists",
    "install-first",
    "how-it-works-visual",
    "live-ci-badge",
    "license-badge-match",
    "install-registry",
    "test-count-honest",
    "footer-site",
    "no-raw-json-tables",
    "verify-command",
    "hero-ok",
    "no-false-e2e",
    "readme-size",
    "clone-url-self",
    "languages-honest",
    "details-collapse",
    "insight-quote",
    "no-secret-clearance-string",
    "product-has-workflow",
    "latest-success",
    "proof-gate-ci",
    "mesh-green",
    "jake-green",
    "comms-green",
    "deviatrix-green-or-unclaimed",
    "resume-green",
    "patents-green",
    "no-continue-on-error",
    "workflow-on-default",
    "dependabot-rigforge",
    "proof-gate-tag",
    "no-skipped-jobs-as-pass",
    "planted-failure-docs",
    "action-yml-valid",
    "public-mcp-count",
    "rigforge-mcp-file",
    "mesh-mcp-file",
    "catalog-mcp-file",
    "comms-not-mcp",
    "omniscout-not-public-mcp",
    "claude-desktop-snippet",
    "catalog-readonly",
    "catalog-evals",
    "local-57-unadvertised",
    "no-public-mcp-port",
    "mcp-no-plaintext-tokens",
    "copilot-instructions-pins",
    "copilot-instructions-profile",
    "agents-md-pins",
    "copilot-file-short",
    "copilot-has-test-cmd",
    "codeowners-pins",
    "pin-narrative",
    "resume-pdf",
    "directory-matches-public",
    "no-star-farming",
    "activity-7d",
    "contact-path",
    "fde-portfolio-smoke",
    "no-clearance-overclaim",
    "criteria-count",
    "today-scoreboard",
    "latest-pointer",
    "scoreboard-hash",
    "orca-automation",
    "local-first",
    "issues-for-reds",
    "readme-receipts-fresh",
    "no-direct-main-from-orca",
    "planted-failure",
)
LLM_ORDINALS = (33, 42, 46, 63, 83)
CHECKS = {"gh", "file", "http", "regex", "llm"}
NOW = datetime(2026, 9, 8, 12, 30, tzinfo=timezone.utc)


class CriteriaContractTests(unittest.TestCase):
    def test_all_criteria_parse_in_exact_order_with_only_five_llm_rows(self) -> None:
        criteria = subject.load_criteria(CRITERIA_PATH)
        self.assertEqual(tuple(row["id"] for row in criteria), EXPECTED_IDS)
        self.assertEqual(len(criteria), 100)
        self.assertEqual(
            tuple(
                index
                for index, row in enumerate(criteria, start=1)
                if row["check"] == "llm"
            ),
            LLM_ORDINALS,
        )
        for row in criteria:
            self.assertEqual(
                set(row), {"id", "check", "target", "pass_rule", "description"}
            )
            self.assertIn(row["check"], CHECKS)
            self.assertTrue(row["target"])
            self.assertTrue(row["pass_rule"])
            self.assertTrue(row["description"])

    def test_parser_rejects_unknown_checks_duplicates_and_missing_fields(self) -> None:
        source = CRITERIA_PATH.read_text(encoding="utf-8")
        cases = {
            "unknown-check": source.replace("check: 'gh'", "check: 'shell'", 1),
            "duplicate-id": source.replace(
                "id: 'banner-200'", "id: 'profile-readme-exists'", 1
            ),
            "missing-field": source.replace("    pass_rule:", "    omitted:", 1),
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "criteria.yaml"
            for name, malformed in cases.items():
                with self.subTest(name=name):
                    path.write_text(malformed, encoding="utf-8")
                    with self.assertRaises(subject.ScoreError):
                        subject.load_criteria(path)


class ScoreboardContractTests(unittest.TestCase):
    def test_scoreboard_schema_counts_green_red_and_null(self) -> None:
        definitions = subject.load_criteria(CRITERIA_PATH)
        rows = tuple(
            {
                "id": definition["id"],
                "check": definition["check"],
                "description": definition["description"],
                "status": None if definition["check"] == "llm" else "green",
                "evidence": None if definition["check"] == "llm" else "verified",
            }
            for definition in definitions
        )
        scoreboard = subject.build_scoreboard("a" * 64, rows, NOW)
        self.assertEqual(
            tuple(scoreboard),
            (
                "schema",
                "date",
                "generated_at",
                "criteria_sha256",
                "summary",
                "criteria",
            ),
        )
        self.assertEqual(scoreboard["schema"], 1)
        self.assertEqual(scoreboard["date"], "2026-09-08")
        self.assertEqual(scoreboard["generated_at"], "2026-09-08T12:30:00Z")
        self.assertEqual(scoreboard["criteria_sha256"], "a" * 64)
        self.assertEqual(
            scoreboard["summary"],
            {"total": 100, "green": 95, "red": 0, "null": 5},
        )
        self.assertEqual(len(scoreboard["criteria"]), 100)

    def test_atomic_outputs_write_today_latest_and_shields_payload(self) -> None:
        rows = tuple(
            {
                "id": criterion_id,
                "check": "gh",
                "description": criterion_id,
                "status": "green",
                "evidence": "verified",
            }
            for criterion_id in EXPECTED_IDS
        )
        scoreboard = subject.build_scoreboard("b" * 64, rows, NOW)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = subject.write_scoreboard(root, scoreboard)
            today = root / "steward" / "scoreboard" / "2026-09-08.json"
            latest = root / "steward" / "scoreboard" / "latest.json"
            badge = root / "steward" / "scoreboard" / "badge.json"
            self.assertEqual(paths, (today, latest, badge))
            self.assertEqual(json.loads(today.read_text()), scoreboard)
            self.assertEqual(json.loads(latest.read_text()), scoreboard)
            self.assertEqual(
                json.loads(badge.read_text()),
                {
                    "schemaVersion": 1,
                    "label": "steward",
                    "message": "100/100",
                    "color": "brightgreen",
                },
            )
            self.assertEqual(list(today.parent.glob("*.tmp")), [])

    def test_missing_license_plant_is_in_memory_and_only_criterion_15_is_red(
        self,
    ) -> None:
        definitions = subject.load_criteria(CRITERIA_PATH)
        calls: list[str] = []

        def evaluator(row):
            calls.append(row["id"])
            return True, "verified"

        normal = subject.evaluate_criteria(definitions, evaluator)
        planted = subject.evaluate_criteria(
            definitions, evaluator, plant="missing-license"
        )
        self.assertEqual(normal[14]["status"], "green")
        self.assertEqual(planted[14]["id"], "every-license")
        self.assertEqual(planted[14]["status"], "red")
        self.assertTrue(
            all(
                normal[index]["status"] == planted[index]["status"]
                for index in range(100)
                if index != 14
            )
        )
        self.assertTrue(
            all(
                ordinal not in LLM_ORDINALS
                for ordinal, row in enumerate(definitions, start=1)
                if row["id"] in calls
            )
        )
        self.assertEqual(
            [row["status"] for row in planted if row["check"] == "llm"],
            [None] * 5,
        )


class ObservedFalsePositiveTests(unittest.TestCase):
    def context(self) -> subject.ScoringContext:
        return subject.ScoringContext(ROOT, NOW)

    def test_current_profile_readme_does_not_trigger_no_phone(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        context = self.context()
        with mock.patch.object(context, "readme", return_value=readme):
            passed, evidence = context.evaluate({"id": "no-phone"})
        self.assertTrue(passed, evidence)

    def test_install_registry_ignores_editable_and_git_installs(self) -> None:
        readme = "\n".join(
            (
                "pip install -e .",
                "pip install -e \".[mcp]\"",
                "pip install git+https://github.com/mrodgersjs-web/rigforge.git",
                "python3 -m pip install git+https://github.com/mrodgersjs-web/mesh-studio.git",
            )
        )
        context = self.context()
        with mock.patch.object(
            context, "all_readmes", return_value=[("rigforge", readme)]
        ):
            with mock.patch.object(
                context,
                "http",
                side_effect=AssertionError("registry lookup must not run"),
            ):
                passed, evidence = context.evaluate({"id": "install-registry"})
        self.assertTrue(passed, evidence)

    def test_clone_url_self_checks_clone_commands_not_related_links(self) -> None:
        readme = "\n".join(
            (
                "Related: https://github.com/mrodgersjs-web/proof-studio",
                "git clone https://github.com/mrodgersjs-web/rigforge.git",
            )
        )
        context = self.context()
        with mock.patch.object(
            context, "all_readmes", return_value=[("rigforge", readme)]
        ):
            passed, evidence = context.evaluate({"id": "clone-url-self"})
        self.assertTrue(passed, evidence)

        mismatched = (
            "git clone https://github.com/mrodgersjs-web/proof-studio.git"
        )
        with mock.patch.object(
            context, "all_readmes", return_value=[("rigforge", mismatched)]
        ):
            passed, _ = context.evaluate({"id": "clone-url-self"})
        self.assertFalse(passed)

    def test_languages_honest_ignores_non_language_badges(self) -> None:
        neutral_badges = "\n".join(
            (
                "https://img.shields.io/badge/status-stable-green",
                "https://img.shields.io/badge/license-MIT-blue",
                "https://img.shields.io/badge/runtime-node20-green",
                "https://img.shields.io/badge/dependency-mcp-blue",
                "https://img.shields.io/badge/Python-3.11-blue",
            )
        )
        context = self.context()
        with mock.patch.object(
            context,
            "all_readmes",
            return_value=[("rigforge", neutral_badges)],
        ):
            with mock.patch.object(context, "api", return_value={"Python": 100}):
                passed, evidence = context.evaluate({"id": "languages-honest"})
        self.assertTrue(passed, evidence)

        with mock.patch.object(
            context,
            "all_readmes",
            return_value=[
                (
                    "rigforge",
                    neutral_badges
                    + "\nhttps://img.shields.io/badge/TypeScript-5-blue",
                )
            ],
        ):
            with mock.patch.object(context, "api", return_value={"Python": 100}):
                passed, _ = context.evaluate({"id": "languages-honest"})
        self.assertFalse(passed)

    def test_workflow_scan_ignores_absent_optional_paths(self) -> None:
        context = self.context()
        read_paths: list[str] = []

        def file_text(repo: str, path: str) -> str:
            read_paths.append(path)
            return "jobs:\n  smoke:\n    continue-on-error: false\n"

        with mock.patch.object(context, "pins", return_value=("rigforge",)):
            with mock.patch.object(
                context,
                "workflows",
                return_value=[
                    {"name": "optional metadata", "path": None},
                    {
                        "name": "Dependabot Updates",
                        "path": "dynamic/dependabot/dependabot-updates",
                    },
                    {"name": "smoke", "path": ".github/workflows/smoke.yml"},
                ],
            ):
                with mock.patch.object(
                    context, "file_text", side_effect=file_text
                ):
                    passed, evidence = context.evaluate(
                        {"id": "no-continue-on-error"}
                    )
        self.assertTrue(passed, evidence)
        self.assertEqual(read_paths, [".github/workflows/smoke.yml"])

    def test_successful_proof_gate_test_job_is_a_required_job(self) -> None:
        context = self.context()
        with mock.patch.object(
            context, "pins", return_value=("proof-gate-action",)
        ):
            with mock.patch.object(
                context, "latest_run", return_value={"id": 101}
            ):
                with mock.patch.object(
                    context,
                    "api",
                    return_value={
                        "jobs": [
                            {
                                "name": "test",
                                "status": "completed",
                                "conclusion": "success",
                            }
                        ]
                    },
                ):
                    passed, evidence = context.evaluate(
                        {"id": "no-skipped-jobs-as-pass"}
                    )
        self.assertTrue(passed, evidence)

    def test_directory_count_uses_only_explicit_public_repository_claim(self) -> None:
        context = self.context()
        readme = "\n".join(
            (
                "22 tools indexed",
                "12 release receipts",
                "17 repos",
                "6 public repositories",
            )
        )
        public = [
            {"name": f"repo-{index}", "private": False}
            for index in range(6)
        ]
        with mock.patch.object(
            context,
            "repo",
            return_value={"name": "rig-agent-directory", "private": False},
        ):
            with mock.patch.object(context, "readme", return_value=readme):
                with mock.patch.object(
                    context, "public_repos", return_value=public
                ):
                    passed, evidence = context.evaluate(
                        {"id": "directory-matches-public"}
                    )
        self.assertTrue(passed, evidence)

    def test_issues_for_reds_uses_only_yesterdays_scoreboard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scoreboard_dir = root / "steward" / "scoreboard"
            scoreboard_dir.mkdir(parents=True)
            (scoreboard_dir / "latest.json").write_text(
                json.dumps(
                    {
                        "criteria": [
                            {"id": "every-license", "status": "red"}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            context = subject.ScoringContext(root, NOW)
            with mock.patch.object(
                context,
                "api",
                side_effect=AssertionError(
                    "issues are not due without yesterday's scoreboard"
                ),
            ):
                passed, evidence = context.evaluate({"id": "issues-for-reds"})
            self.assertTrue(passed, evidence)

            yesterday = scoreboard_dir / "2026-09-07.json"
            yesterday.write_text(
                json.dumps(
                    {
                        "criteria": [
                            {"id": "every-license", "status": "red"}
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.object(
                context,
                "api",
                return_value=[
                    {
                        "title": "github-steward: every-license",
                        "body": "Track criterion every-license.",
                    }
                ],
            ):
                passed, evidence = context.evaluate({"id": "issues-for-reds"})
            self.assertTrue(passed, evidence)

            with mock.patch.object(context, "api", return_value=[]):
                passed, _ = context.evaluate({"id": "issues-for-reds"})
            self.assertFalse(passed)



class AcceptedScorerReviewTests(unittest.TestCase):
    def context(
        self,
        root: Path = ROOT,
        now: datetime = NOW,
    ) -> subject.ScoringContext:
        return subject.ScoringContext(root, now)

    def test_plant_run_writes_no_canonical_scoreboard_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            steward = root / "steward"
            steward.mkdir()
            (steward / "criteria.yaml").write_bytes(CRITERIA_PATH.read_bytes())

            def evaluator(row):
                return True, "verified"

            scoreboard = subject.run_score(
                root,
                evaluator=evaluator,
                plant="missing-license",
                now=NOW,
            )
            self.assertEqual(scoreboard["criteria"][14]["status"], "red")
            self.assertFalse((steward / "scoreboard").exists())

    def test_judge_validates_registry_and_scoreboard_before_row_selection(
        self,
    ) -> None:
        definitions = subject.load_criteria(CRITERIA_PATH)
        rows = tuple(
            {
                "id": row["id"],
                "check": row["check"],
                "description": row["description"],
                "status": None if row["check"] == "llm" else "green",
                "evidence": None if row["check"] == "llm" else "verified",
            }
            for row in definitions
        )
        digest = subject.criteria_sha256(CRITERIA_PATH)
        valid = subject.build_scoreboard(digest, rows, NOW)
        self.assertEqual(
            judge.validate_scoreboard(
                valid,
                definitions,
                digest,
                today=NOW.date(),
            ),
            valid,
        )

        invalid = {}
        stale_hash = json.loads(json.dumps(valid))
        stale_hash["criteria_sha256"] = "0" * 64
        invalid["stale-hash"] = stale_hash

        wrong_order = json.loads(json.dumps(valid))
        wrong_order["criteria"][0], wrong_order["criteria"][1] = (
            wrong_order["criteria"][1],
            wrong_order["criteria"][0],
        )
        invalid["wrong-order"] = wrong_order

        duplicate = json.loads(json.dumps(valid))
        duplicate["criteria"][1]["id"] = duplicate["criteria"][0]["id"]
        invalid["duplicate-id"] = duplicate

        invalid_status = json.loads(json.dumps(valid))
        invalid_status["criteria"][0]["status"] = None
        invalid["invalid-deterministic-status"] = invalid_status

        inconsistent = json.loads(json.dumps(valid))
        inconsistent["summary"]["green"] -= 1
        inconsistent["summary"]["red"] += 1
        invalid["inconsistent-summary"] = inconsistent

        for name, scoreboard in invalid.items():
            with self.subTest(name=name):
                with self.assertRaises(judge.JudgeError):
                    judge.validate_scoreboard(
                        scoreboard,
                        definitions,
                        digest,
                        today=NOW.date(),
                    )

    def test_token_check_rejects_literal_tokens_but_accepts_safe_references(
        self,
    ) -> None:
        context = self.context()
        unsafe = (
            "token=ghp_abcdefghijklmnopqrstuvwxyz",
            "token=github_pat_abcdefghijklmnopqrstuvwxyz",
            "GH_TOKEN=literal-secret-value",
        )
        for readme in unsafe:
            with self.subTest(readme=readme):
                with mock.patch.object(
                    context,
                    "all_readmes",
                    return_value=[("rigforge", readme)],
                ):
                    passed, _ = context.evaluate(
                        {"id": "mcp-no-plaintext-tokens"}
                    )
                self.assertFalse(passed)

        for readme in (
            "Use gh auth login before launching the server.",
            "Set ${env:GH_TOKEN} in the client configuration.",
        ):
            with self.subTest(readme=readme):
                with mock.patch.object(
                    context,
                    "all_readmes",
                    return_value=[("rigforge", readme)],
                ):
                    passed, evidence = context.evaluate(
                        {"id": "mcp-no-plaintext-tokens"}
                    )
                self.assertTrue(passed, evidence)

    def test_phone_check_uses_independent_optional_separators_and_digit_boundaries(
        self,
    ) -> None:
        context = self.context()
        phones = (
            "3035550123",
            "303-555-0123",
            "303.555.0123",
            "303 555 0123",
            "303-555 0123",
            "call303-555-0123now",
        )
        for phone in phones:
            with self.subTest(phone=phone):
                with mock.patch.object(context, "readme", return_value=phone):
                    passed, _ = context.evaluate({"id": "no-phone"})
                self.assertFalse(passed)

        with mock.patch.object(
            context,
            "readme",
            return_value="run 32975681777 on 2026-09-08 at 12:30",
        ):
            passed, evidence = context.evaluate({"id": "no-phone"})
        self.assertTrue(passed, evidence)

    def test_home_path_scan_prefers_text_matches_and_narrowly_exempts_quotes(
        self,
    ) -> None:
        context = self.context()
        sha = "a" * 40
        unsafe_item = {
            "path": "docs/internal.md",
            "sha": sha,
            "repository": {"name": "rigforge"},
            "text_matches": [
                {
                    "fragment": (
                        "Install from /Users/rig128gb/Developer/rigforge."
                    )
                }
            ],
        }

        def unsafe_hit(query: str):
            return [unsafe_item] if "/Users/rig128gb" in query else []

        with mock.patch.object(context, "code_search", side_effect=unsafe_hit):
            with mock.patch.object(
                context,
                "blob_text",
                side_effect=AssertionError("text matches must avoid blob reads"),
            ):
                with mock.patch.object(
                    context,
                    "file_text",
                    side_effect=AssertionError("text matches must avoid path reads"),
                ):
                    passed, _ = context.evaluate(
                        {"id": "no-abs-home-paths"}
                    )
        self.assertFalse(passed)

        criterion_quote = (
            "The no-abs-home-paths steward criterion checks `/Users/rig128gb` "
            "and `/home/operator`."
        )
        safe_item = {
            **unsafe_item,
            "text_matches": [{"fragment": criterion_quote}],
        }

        def safe_hit(query: str):
            return [safe_item] if "/Users/rig128gb" in query else []

        with mock.patch.object(context, "code_search", side_effect=safe_hit):
            with mock.patch.object(
                context,
                "blob_text",
                side_effect=AssertionError("text matches must avoid blob reads"),
            ):
                with mock.patch.object(
                    context,
                    "file_text",
                    side_effect=AssertionError("text matches must avoid path reads"),
                ):
                    passed, evidence = context.evaluate(
                        {"id": "no-abs-home-paths"}
                    )
        self.assertTrue(passed, evidence)

        fallback_item = {
            "path": "docs/internal.md",
            "sha": sha,
            "repository": {"name": "rigforge"},
        }

        def fallback_hit(query: str):
            return [fallback_item] if "/Users/rig128gb" in query else []

        with mock.patch.object(context, "code_search", side_effect=fallback_hit):
            with mock.patch.object(
                context,
                "blob_text",
                return_value="Install from /Users/rig128gb/Developer/rigforge.",
            ) as blob_text:
                with mock.patch.object(
                    context,
                    "file_text",
                    side_effect=AssertionError("fallback must use immutable blob"),
                ):
                    passed, _ = context.evaluate(
                        {"id": "no-abs-home-paths"}
                    )
        self.assertFalse(passed)
        blob_text.assert_called_once_with("rigforge", sha)

    def test_code_search_requests_and_validates_text_matches(self) -> None:
        context = self.context()
        seen = {}
        response = {
            "items": [
                {
                    "path": "docs/internal.md",
                    "sha": "a" * 40,
                    "repository": {"name": "rigforge"},
                    "text_matches": [{"fragment": "/Users/rig128gb"}],
                }
            ]
        }

        def api(endpoint: str, headers=None):
            seen["endpoint"] = endpoint
            seen["headers"] = headers
            return response

        with mock.patch.object(context, "api", side_effect=api):
            rows = context.code_search('"/Users/rig128gb"')
        self.assertEqual(
            seen["headers"],
            {"Accept": "application/vnd.github.text-match+json"},
        )
        self.assertEqual(
            rows[0]["text_matches"],
            [{"fragment": "/Users/rig128gb"}],
        )

        malformed = {
            "items": [
                {
                    "path": "docs/internal.md",
                    "sha": "a" * 40,
                    "repository": {"name": "rigforge"},
                    "text_matches": [{"fragment": 123}],
                }
            ]
        }
        with mock.patch.object(
            context,
            "api",
            side_effect=lambda endpoint, headers=None: malformed,
        ):
            with self.assertRaises(subject.ScoreError):
                context.code_search("home path")

    def test_blob_text_rejects_bad_sha_encoding_and_non_utf8(self) -> None:
        context = self.context()
        sha = "b" * 40
        with self.assertRaises(subject.ScoreError):
            context.blob_text("rigforge", "not-a-sha")

        cases = {
            "encoding": {
                "sha": sha,
                "encoding": "utf-16",
                "content": "",
            },
            "non-utf8": {
                "sha": sha,
                "encoding": "base64",
                "content": "/w==",
            },
        }
        for name, response in cases.items():
            with self.subTest(name=name):
                with mock.patch.object(context, "api", return_value=response):
                    with self.assertRaises(subject.ScoreError):
                        context.blob_text("rigforge", sha)

    def test_clone_check_rejects_other_owners_as_well_as_other_repositories(
        self,
    ) -> None:
        context = self.context()
        with mock.patch.object(
            context,
            "all_readmes",
            return_value=[
                (
                    "rigforge",
                    "git clone https://github.com/someone-else/rigforge.git",
                )
            ],
        ):
            passed, _ = context.evaluate({"id": "clone-url-self"})
        self.assertFalse(passed)

    def test_continue_on_error_detects_yaml_and_expression_true_forms(
        self,
    ) -> None:
        context = self.context()
        for source in (
            "continue-on-error: TRUE",
            "continue-on-error: ${{ true }}",
        ):
            with self.subTest(source=source):
                with mock.patch.object(
                    context, "pins", return_value=("rigforge",)
                ):
                    with mock.patch.object(
                        context,
                        "workflows",
                        return_value=[
                            {
                                "path": ".github/workflows/smoke.yml",
                                "name": "smoke",
                            }
                        ],
                    ):
                        with mock.patch.object(
                            context, "file_text", return_value=source
                        ):
                            passed, _ = context.evaluate(
                                {"id": "no-continue-on-error"}
                            )
                self.assertFalse(passed)

    def test_planted_failure_criterion_uses_pure_in_memory_evaluator(
        self,
    ) -> None:
        definitions = subject.load_criteria(CRITERIA_PATH)
        normal = tuple(
            {
                "id": row["id"],
                "check": row["check"],
                "description": row["description"],
                "status": None if row["check"] == "llm" else "green",
                "evidence": None if row["check"] == "llm" else "verified",
            }
            for row in definitions
        )
        planted_rows = [dict(row) for row in normal]
        planted_rows[14]["status"] = "red"
        planted_rows[14]["evidence"] = "PLANTED"
        plants: list[object] = []

        def pure_evaluate(criteria, evaluator, *, plant=None):
            plants.append(plant)
            return tuple(planted_rows) if plant else normal

        context = self.context()
        with mock.patch.object(
            subject, "evaluate_criteria", side_effect=pure_evaluate
        ):
            with mock.patch.object(context, "public_repos", return_value=[]):
                passed, evidence = context.evaluate(
                    {"id": "planted-failure"}
                )
        self.assertTrue(passed, evidence)
        self.assertEqual(plants, [None, "missing-license"])

    def test_resume_pdf_accepts_a_live_readme_pdf_link(self) -> None:
        context = self.context()
        pdf_url = (
            "https://github.com/mrodgersjs-web/resume/raw/main/"
            "Mike-Rodgers-Forward-Deployed-Engineer.pdf"
        )
        with mock.patch.object(context, "tree", return_value=[]):
            with mock.patch.object(
                context,
                "readme",
                return_value=f"[Download the resume PDF]({pdf_url})",
            ):
                with mock.patch.object(
                    context, "http", return_value=(200, b"pdf")
                ) as http:
                    passed, evidence = context.evaluate({"id": "resume-pdf"})
        self.assertTrue(passed, evidence)
        http.assert_called_once_with(pdf_url)

    def test_activity_accepts_recent_actions_without_push_event(self) -> None:
        context = self.context()

        def api(endpoint: str):
            if endpoint.endswith("/events?per_page=100"):
                return []
            if endpoint.endswith("/actions/runs?per_page=100"):
                return {
                    "workflow_runs": [
                        {
                            "id": 101,
                            "event": "workflow_dispatch",
                            "created_at": "2026-09-08T10:00:00Z",
                        }
                    ]
                }
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        with mock.patch.object(context, "api", side_effect=api):
            passed, evidence = context.evaluate({"id": "activity-7d"})
        self.assertTrue(passed, evidence)

    def test_proof_gate_tag_requires_annotated_time_after_first_green(
        self,
    ) -> None:
        context = self.context()
        runs = [
            {
                "id": 1,
                "conclusion": "success",
                "created_at": "2026-09-01T10:00:00Z",
                "updated_at": "2026-09-01T12:00:00Z",
            }
        ]

        def lightweight(endpoint: str):
            return {
                "ref": "refs/tags/v1",
                "object": {"type": "commit", "sha": "commit-sha"},
            }

        with mock.patch.object(context, "api", side_effect=lightweight):
            with mock.patch.object(context, "runs", return_value=runs):
                passed, _ = context.evaluate({"id": "proof-gate-tag"})
        self.assertFalse(passed)

        def annotated(endpoint: str):
            if endpoint.endswith("/git/ref/tags/v1"):
                return {
                    "ref": "refs/tags/v1",
                    "object": {"type": "tag", "sha": "tag-sha"},
                }
            if endpoint.endswith("/git/tags/tag-sha"):
                return {"tagger": {"date": "2026-09-02T10:00:00Z"}}
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        with mock.patch.object(context, "api", side_effect=annotated):
            with mock.patch.object(context, "runs", return_value=runs):
                passed, evidence = context.evaluate({"id": "proof-gate-tag"})
        self.assertTrue(passed, evidence)

    def test_install_registry_skips_flags_but_checks_package_operands(
        self,
    ) -> None:
        context = self.context()
        readme = "\n".join(
            (
                "pip install --upgrade alpha-package",
                "pip install --disable-pip-version-check beta-package",
                "npx @scope/tool --yes",
            )
        )
        urls: list[str] = []

        def http(url: str):
            urls.append(url)
            return 200, b"ok"

        with mock.patch.object(
            context, "all_readmes", return_value=[("rigforge", readme)]
        ):
            with mock.patch.object(context, "http", side_effect=http):
                passed, evidence = context.evaluate({"id": "install-registry"})
        self.assertTrue(passed, evidence)
        self.assertEqual(
            urls,
            [
                "https://pypi.org/pypi/alpha-package/json",
                "https://pypi.org/pypi/beta-package/json",
                "https://registry.npmjs.org/%40scope%2Ftool",
            ],
        )

    def test_catalog_transport_parser_accepts_only_stdio(self) -> None:
        cases = {
            "stdio-single-quotes": (
                "server.run( transport = 'stdio' )",
                True,
            ),
            "sse-mixed-with-stdio": (
                'server.run(transport="stdio")\n'
                "server.run( transport = 'sse' )",
                False,
            ),
            "streamable-http": (
                'server.run( transport = "streamable-http" )',
                False,
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            steward = root / "steward"
            steward.mkdir()
            context = self.context(root)
            for name, (source, expected) in cases.items():
                with self.subTest(name=name):
                    (steward / "catalog_mcp.py").write_text(
                        source, encoding="utf-8"
                    )
                    passed, _ = context.evaluate(
                        {"id": "no-public-mcp-port"}
                    )
                    self.assertEqual(passed, expected)


    def test_judge_uses_current_definitions_and_rejects_scoreboard_drift(
        self,
    ) -> None:
        definitions = subject.load_criteria(CRITERIA_PATH)
        rows = tuple(
            {
                "id": row["id"],
                "check": row["check"],
                "description": row["description"],
                "status": None if row["check"] == "llm" else "green",
                "evidence": None if row["check"] == "llm" else "verified",
            }
            for row in definitions
        )
        digest = subject.criteria_sha256(CRITERIA_PATH)
        valid = subject.build_scoreboard(digest, rows, NOW)

        copied = json.loads(json.dumps(valid))
        copied["criteria"][32]["description"] = "scoreboard-controlled prompt"
        pending = judge.pending_llm_rows(definitions, copied)
        self.assertEqual(
            pending[0]["description"],
            definitions[32]["description"],
        )

        altered = json.loads(json.dumps(valid))
        altered["criteria"][0]["description"] = "altered definition"
        extra = json.loads(json.dumps(valid))
        extra["criteria"][0]["target"] = "scoreboard override"
        for name, scoreboard in (("altered", altered), ("extra", extra)):
            with self.subTest(name=name):
                with self.assertRaises(judge.JudgeError):
                    judge.validate_scoreboard(
                        scoreboard,
                        definitions,
                        digest,
                        today=NOW.date(),
                    )

    def test_token_check_rejects_colon_assignments_but_accepts_env_values(
        self,
    ) -> None:
        context = self.context()
        unsafe = (
            "GH_TOKEN: literal-secret",
            '"GH_TOKEN": "literal-secret"',
        )
        safe = (
            "GH_TOKEN: ${env:GH_TOKEN}",
            '"GH_TOKEN": "${env:GH_TOKEN}"',
        )
        for text in unsafe:
            with self.subTest(text=text):
                with mock.patch.object(
                    context, "all_readmes", return_value=[("rigforge", text)]
                ):
                    passed, _ = context.evaluate(
                        {"id": "mcp-no-plaintext-tokens"}
                    )
                self.assertFalse(passed)
        for text in safe:
            with self.subTest(text=text):
                with mock.patch.object(
                    context, "all_readmes", return_value=[("rigforge", text)]
                ):
                    passed, evidence = context.evaluate(
                        {"id": "mcp-no-plaintext-tokens"}
                    )
                self.assertTrue(passed, evidence)

    def test_each_home_path_fragment_must_be_independently_safe(self) -> None:
        context = self.context()
        item = {
            "path": "docs/internal.md",
            "sha": "a" * 40,
            "repository": {"name": "rigforge"},
            "text_matches": [
                {
                    "fragment": (
                        "The no-abs-home-paths steward criterion checks "
                        "`/Users/rig128gb` and `/home/operator`."
                    )
                },
                {
                    "fragment": (
                        "Actual install path: "
                        "/Users/rig128gb/Developer/private-project"
                    )
                },
            ],
        }

        def one_hit(query: str):
            return [item] if "/Users/rig128gb" in query else []

        with mock.patch.object(context, "code_search", side_effect=one_hit):
            with mock.patch.object(
                context,
                "blob_text",
                side_effect=AssertionError("text matches must avoid blob reads"),
            ):
                passed, _ = context.evaluate({"id": "no-abs-home-paths"})
        self.assertFalse(passed)

    def test_workflow_scan_ignores_comments_and_run_strings(self) -> None:
        context = self.context()
        safe = "\n".join(
            (
                "# continue-on-error: true",
                'run: echo "continue-on-error: true"',
                "continue-on-error: false",
            )
        )
        actual = "jobs:\n  test:\n    continue-on-error: true\n"
        inline_mapping = "steps: [{run: pytest, continue-on-error: true}]"
        dynamic_expression = "continue-on-error: ${{ matrix.experimental }}"
        cases = (
            (safe, True),
            (actual, False),
            (inline_mapping, False),
            (dynamic_expression, False),
        )
        for source, expected in cases:
            with self.subTest(source=source):
                with mock.patch.object(
                    context, "pins", return_value=("rigforge",)
                ):
                    with mock.patch.object(
                        context,
                        "workflows",
                        return_value=[
                            {
                                "path": ".github/workflows/smoke.yml",
                                "name": "smoke",
                            }
                        ],
                    ):
                        with mock.patch.object(
                            context, "file_text", return_value=source
                        ):
                            passed, evidence = context.evaluate(
                                {"id": "no-continue-on-error"}
                            )
                self.assertEqual(passed, expected, evidence)

    def test_tag_chronology_uses_updated_at_and_requires_strictly_after(
        self,
    ) -> None:
        context = self.context()
        runs = [
            {
                "id": 1,
                "conclusion": "success",
                "created_at": "2026-09-01T10:00:00Z",
                "updated_at": "2026-09-03T10:00:00Z",
            }
        ]

        def api_for(tagger_date: str):
            def api(endpoint: str):
                if endpoint.endswith("/git/ref/tags/v1"):
                    return {
                        "object": {"type": "tag", "sha": "tag-sha"}
                    }
                if endpoint.endswith("/git/tags/tag-sha"):
                    return {"tagger": {"date": tagger_date}}
                raise AssertionError(f"unexpected endpoint: {endpoint}")

            return api

        for tagger_date, expected in (
            ("2026-09-02T10:00:00Z", False),
            ("2026-09-03T10:00:00Z", False),
            ("2026-09-04T10:00:00Z", True),
        ):
            with self.subTest(tagger_date=tagger_date):
                with mock.patch.object(
                    context, "api", side_effect=api_for(tagger_date)
                ):
                    with mock.patch.object(
                        context, "runs", return_value=runs
                    ):
                        passed, evidence = context.evaluate(
                            {"id": "proof-gate-tag"}
                        )
                self.assertEqual(passed, expected, evidence)

    def test_activity_short_circuits_when_either_source_is_recent(self) -> None:
        context = self.context()

        def recent_event(endpoint: str):
            if endpoint.endswith("/events?per_page=100"):
                return [
                    {
                        "type": "PushEvent",
                        "created_at": "2026-09-08T10:00:00Z",
                    }
                ]
            raise AssertionError("Actions must not run after a recent event")

        with mock.patch.object(context, "api", side_effect=recent_event):
            passed, evidence = context.evaluate({"id": "activity-7d"})
        self.assertTrue(passed, evidence)

        def recent_action(endpoint: str):
            if endpoint.endswith("/events?per_page=100"):
                raise subject.ScoreError("events provider unavailable")
            if endpoint.endswith("/actions/runs?per_page=100"):
                return {
                    "workflow_runs": [
                        {
                            "id": 101,
                            "created_at": "2026-09-08T10:00:00Z",
                        }
                    ]
                }
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        with mock.patch.object(context, "api", side_effect=recent_action):
            passed, evidence = context.evaluate({"id": "activity-7d"})
        self.assertTrue(passed, evidence)

    def test_npx_versions_query_only_registry_package_names(self) -> None:
        context = self.context()
        readme = "\n".join(
            (
                "npx package-name@latest --yes",
                "npx @scope/tool@1.2.3 --yes",
            )
        )
        urls: list[str] = []

        def http(url: str):
            urls.append(url)
            return 200, b"ok"

        with mock.patch.object(
            context, "all_readmes", return_value=[("rigforge", readme)]
        ):
            with mock.patch.object(context, "http", side_effect=http):
                passed, evidence = context.evaluate({"id": "install-registry"})
        self.assertTrue(passed, evidence)
        self.assertEqual(
            urls,
            [
                "https://registry.npmjs.org/package-name",
                "https://registry.npmjs.org/%40scope%2Ftool",
            ],
        )

    def test_catalog_transport_uses_python_ast_not_comments_or_docstrings(
        self,
    ) -> None:
        cases = {
            "comments-and-docstrings": (
                '"""server.run(transport="sse")"""\n'
                '# server.run(transport="streamable-http")\n'
                "server.run( transport = 'stdio' )\n",
                True,
            ),
            "actual-sse": (
                'server.run(transport="stdio")\n'
                'server.run(transport="sse")\n',
                False,
            ),
            "dynamic": (
                'server.run(transport="stdio")\n'
                "server.run(transport=selected_transport)\n",
                False,
            ),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            steward = root / "steward"
            steward.mkdir()
            context = self.context(root)
            for name, (source, expected) in cases.items():
                with self.subTest(name=name):
                    (steward / "catalog_mcp.py").write_text(
                        source, encoding="utf-8"
                    )
                    passed, evidence = context.evaluate(
                        {"id": "no-public-mcp-port"}
                    )
                    self.assertEqual(passed, expected, evidence)


    def test_compact_nested_json_token_assignments_are_classified(self) -> None:
        context = self.context()
        cases = (
            ('{"env":{"GH_TOKEN":"literal-secret"}}', False),
            ('{"env":{"GH_TOKEN":"${env:GH_TOKEN}"}}', True),
        )
        for text, expected in cases:
            with self.subTest(text=text):
                with mock.patch.object(
                    context, "all_readmes", return_value=[("rigforge", text)]
                ):
                    passed, evidence = context.evaluate(
                        {"id": "mcp-no-plaintext-tokens"}
                    )
                self.assertEqual(passed, expected, evidence)

    def test_mixed_home_path_fragment_cannot_hide_behind_criterion_quote(
        self,
    ) -> None:
        context = self.context()
        item = {
            "path": "docs/internal.md",
            "sha": "a" * 40,
            "repository": {"name": "rigforge"},
            "text_matches": [
                {
                    "fragment": (
                        "The no-abs-home-paths steward criterion checks "
                        "`/Users/rig128gb` and `/home/operator`.\n"
                        "Install from /Users/rig128gb/Developer/private-project."
                    )
                }
            ],
        }

        def one_hit(query: str):
            return [item] if "/Users/rig128gb" in query else []

        with mock.patch.object(context, "code_search", side_effect=one_hit):
            with mock.patch.object(
                context,
                "blob_text",
                side_effect=AssertionError("validated text matches are sufficient"),
            ):
                with mock.patch.object(
                    context,
                    "file_text",
                    side_effect=AssertionError("path traversal is forbidden"),
                ):
                    passed, _ = context.evaluate(
                        {"id": "no-abs-home-paths"}
                    )
        self.assertFalse(passed)

    def test_workflow_scan_detects_quoted_continue_on_error_keys(self) -> None:
        context = self.context()
        for source in (
            "'continue-on-error': true",
            '"continue-on-error": true',
        ):
            with self.subTest(source=source):
                with mock.patch.object(
                    context, "pins", return_value=("rigforge",)
                ):
                    with mock.patch.object(
                        context,
                        "workflows",
                        return_value=[
                            {
                                "path": ".github/workflows/smoke.yml",
                                "name": "smoke",
                            }
                        ],
                    ):
                        with mock.patch.object(
                            context, "file_text", return_value=source
                        ):
                            passed, _ = context.evaluate(
                                {"id": "no-continue-on-error"}
                            )
                self.assertFalse(passed)


    def test_orca_automation_accepts_supported_response_envelopes(self) -> None:
        context = self.context()
        automation = {"name": "GitHub FDE steward", "enabled": True}
        payloads = (
            [automation],
            {"automations": [automation]},
            {"ok": True, "result": {"automations": [automation]}},
        )
        for payload in payloads:
            with self.subTest(payload=payload):
                completed = subprocess.CompletedProcess(
                    ("orca", "automations", "list", "--json"),
                    0,
                    json.dumps(payload),
                    "",
                )
                with mock.patch.object(
                    context, "command", return_value=completed
                ):
                    passed, evidence = context.evaluate(
                        {"id": "orca-automation"}
                    )
                self.assertTrue(passed, evidence)

    def test_no_direct_main_reads_only_committed_steward_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            steward = root / "steward"
            steward.mkdir()
            context = self.context(root)
            committed = steward / "ORCA_PROMPT.md"
            root_copy = root / "ORCA_PROMPT.md"

            committed.write_text(
                "Do not git push to main", encoding="utf-8"
            )
            root_copy.write_text("stale root copy", encoding="utf-8")
            passed, evidence = context.evaluate(
                {"id": "no-direct-main-from-orca"}
            )
            self.assertTrue(passed, evidence)

            committed.unlink()
            root_copy.write_text(
                "Do not git push to main", encoding="utf-8"
            )
            passed, _ = context.evaluate(
                {"id": "no-direct-main-from-orca"}
            )
            self.assertFalse(passed)


class JudgeContractTests(unittest.TestCase):
    def test_judge_selects_first_local_model_before_any_remote_attempt(self) -> None:
        calls: list[tuple[str, ...]] = []

        def run(argv, input_text=None):
            calls.append(argv)
            return subprocess.CompletedProcess(
                argv,
                0,
                "NAME ID SIZE MODIFIED\nqwen3:latest abc 8GB now\nsecond:def 123 4GB now\n",
                "",
            )

        self.assertEqual(judge.select_backend(run), ("local", "qwen3:latest"))
        self.assertEqual(calls, [("ollama", "list")])

    def test_judge_uses_128gb_ssh_only_after_local_then_falls_back_without_write(
        self,
    ) -> None:
        calls: list[tuple[str, ...]] = []

        def run(argv, input_text=None):
            calls.append(argv)
            return subprocess.CompletedProcess(argv, 1, "", "unavailable")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scoreboard_dir = root / "steward" / "scoreboard"
            scoreboard_dir.mkdir(parents=True)
            latest = scoreboard_dir / "latest.json"
            latest.write_text('{"sentinel":"unchanged"}', encoding="utf-8")
            before = latest.read_bytes()
            emitted: list[str] = []
            self.assertFalse(judge.judge(root, run=run, emit=emitted.append))
            self.assertEqual(emitted, [judge.FALLBACK_PAID])
            self.assertEqual(
                calls,
                [
                    ("ollama", "list"),
                    ("ssh", judge.SSH_HOST, "ollama", "list"),
                ],
            )
            self.assertEqual(latest.read_bytes(), before)
            self.assertEqual(list(scoreboard_dir.iterdir()), [latest])

    def test_pending_rows_are_only_the_five_llm_criteria(self) -> None:
        definitions = subject.load_criteria(CRITERIA_PATH)
        scoreboard = {
            "criteria": [
                {"id": row["id"], "status": None, "evidence": None}
                for row in definitions
            ]
        }
        pending = judge.pending_llm_rows(definitions, scoreboard)
        self.assertEqual(
            tuple(row["id"] for row in pending),
            tuple(EXPECTED_IDS[index - 1] for index in LLM_ORDINALS),
        )


if __name__ == "__main__":
    unittest.main()
