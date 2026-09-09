from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from steward import build_readme as subject


EXPECTED_PINS = (
    "mrodgersjs-web/rigforge",
    "mrodgersjs-web/proof-studio",
    "mrodgersjs-web/proof-gate-action",
    "mrodgersjs-web/mesh-studio",
    "mrodgersjs-web/doctrine",
    "mrodgersjs-web/fde-portfolio",
)


def receipt(
    repo: str,
    *,
    release: dict[str, str] | None = None,
    smoke: dict[str, str] | None = None,
) -> dict[str, object]:
    return {"repo": repo, "release": release, "smoke": smoke}


class StaticReadmeContractTests(unittest.TestCase):
    def test_readme_has_the_ten_blocks_and_six_public_pins(self) -> None:
        root = Path(__file__).resolve().parents[1]
        readme = (root / "README.md").read_text(encoding="utf-8")

        sentinels = (
            "assets/profile-banner-v2.jpg",
            "Forward Deployed Engineer · Denver ·",
            "[![public repositories]",
            "> **One operator. One machine. Every receipt public.**",
            "## Pinned systems",
            "## How a recruiter should spend 10 minutes",
            "## Recent receipts",
            "## Competencies",
            "## Credentials",
            "[**rodgersintelligence.com**](https://rodgersintelligence.com/)",
        )
        positions = [readme.index(sentinel) for sentinel in sentinels]
        self.assertEqual(positions, sorted(positions))
        self.assertTrue(all(readme.count(sentinel) == 1 for sentinel in sentinels))
        self.assertEqual(
            readme.count("I turn AI pilots into production systems you can defend in a board meeting."),
            1,
        )
        self.assertEqual(readme.count("[!["), 3)
        self.assertIn(
            "https%3A%2F%2Fapi.github.com%2Fusers%2Fmrodgersjs-web&query=%24.public_repos",
            readme,
        )
        self.assertIn(
            "steward%2Fscoreboard%2Fbadge.json",
            readme,
        )
        self.assertIn(
            "rigforge/actions/workflows/smoke.yml/badge.svg?branch=main",
            readme,
        )
        self.assertEqual(readme.count(subject.START), 1)
        self.assertEqual(readme.count(subject.END), 1)

        headings = [line for line in readme.splitlines() if line.startswith("## ")]
        self.assertEqual(
            headings,
            [
                "## Pinned systems",
                "## How a recruiter should spend 10 minutes",
                "## Recent receipts",
                "## Competencies",
                "## Credentials",
            ],
        )

        pinned = readme.split("## Pinned systems\n", 1)[1].split(
            "## How a recruiter should spend 10 minutes\n", 1
        )[0]
        pin_rows = [
            line for line in pinned.splitlines() if line.startswith("| [**")
        ]
        self.assertEqual(
            [row.split("**", 2)[1] for row in pin_rows],
            [slug.rsplit("/", 1)[1] for slug in EXPECTED_PINS],
        )

        competencies = readme.split("## Competencies\n", 1)[1].split(
            "## Credentials\n", 1
        )[0]
        competency_rows = [
            line for line in competencies.splitlines() if line.startswith("| **")
        ]
        self.assertEqual(
            [row.split("**", 2)[1] for row in competency_rows],
            ["Python", "TypeScript", "Postgres"],
        )
        credentials = readme.split("## Credentials\n", 1)[1]
        credential_lines = [
            line for line in credentials.splitlines() if line.startswith("- ")
        ]
        self.assertEqual(
            credential_lines,
            [
                "- U.S. Army Counterintelligence veteran",
                "- B.S. Industrial Engineering, Iowa State University",
                "- Six Sigma Black Belt",
                "- Project Management Professional (PMP)",
            ],
        )
        self.assertNotIn("clearance", credentials.lower())

        badge = json.loads(
            (root / "steward" / "scoreboard" / "badge.json").read_text(encoding="utf-8")
        )
        self.assertEqual(badge["schemaVersion"], 1)
        self.assertEqual(badge["label"], "steward")
        latest_path = root / "steward" / "scoreboard" / "latest.json"
        if latest_path.exists():
            latest = json.loads(latest_path.read_text(encoding="utf-8"))
            summary = latest["summary"]
            self.assertEqual(
                badge["message"], f"{summary['green']}/{summary['total']}"
            )
            self.assertNotEqual(badge["color"], "lightgrey")
        else:
            self.assertEqual(badge["message"], "not measured")
            self.assertEqual(badge["color"], "lightgrey")

    def test_pin_file_is_the_single_ordered_source(self) -> None:
        pin_path = Path(__file__).with_name("PINNED.txt")
        self.assertEqual(tuple(pin_path.read_text(encoding="utf-8").splitlines()), EXPECTED_PINS)
        self.assertEqual(subject.load_pins(pin_path), EXPECTED_PINS)
        self.assertEqual(subject.PINNED_REPOS, EXPECTED_PINS)

    def test_pin_loader_rejects_invalid_files(self) -> None:
        cases = {
            "blank": (*EXPECTED_PINS[:2], "", *EXPECTED_PINS[2:]),
            "duplicate": (*EXPECTED_PINS[:-1], EXPECTED_PINS[0]),
            "malformed": (*EXPECTED_PINS[:-1], "not-a-repository"),
            "wrong-owner": (*EXPECTED_PINS[:-1], "someone-else/fde-portfolio"),
            "missing": EXPECTED_PINS[:-1],
            "extra": (*EXPECTED_PINS, "mrodgersjs-web/extra"),
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "PINNED.txt"
            for name, pins in cases.items():
                with self.subTest(name=name):
                    path.write_text("\n".join(pins) + "\n", encoding="utf-8")
                    with self.assertRaises(subject.BuildError):
                        subject.load_pins(path)


class ScoreboardAndRenderingTests(unittest.TestCase):
    def test_missing_scoreboard_is_distinct_from_malformed_scoreboard(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "latest.json"
            self.assertIsNone(subject.load_scoreboard(path))
            path.write_text(
                json.dumps(
                    {
                        "date": "2026-09-07",
                        "summary": {"total": 100, "green": 83, "red": 17, "null": 0},
                        "criteria": [],
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                subject.load_scoreboard(path),
                {"date": "2026-09-07", "total": 100, "green": 83, "red": 17, "null": 0},
            )
            path.write_text("{not json", encoding="utf-8")
            with self.assertRaises(subject.BuildError):
                subject.load_scoreboard(path)

    def test_partial_scoreboard_counts_null_and_renders_green_score(self) -> None:
        payload = {
            "schema": 1,
            "date": "2026-09-08",
            "generated_at": "2026-09-08T12:30:00Z",
            "criteria_sha256": "a" * 64,
            "summary": {
                "total": 100,
                "green": 84,
                "red": 11,
                "null": 5,
            },
            "criteria": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "latest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            parsed = subject.load_scoreboard(path)
            self.assertIsNotNone(parsed)
            self.assertEqual(
                parsed["green"] + parsed["red"] + parsed["null"],
                parsed["total"],
            )
            rendered = subject.render_recent_receipts(
                parsed,
                tuple(receipt(repo) for repo in EXPECTED_PINS),
            )
            self.assertTrue(
                rendered.startswith(
                    "Steward score. **84/100 green**. Measured `2026-09-08`."
                )
            )

            payload["summary"]["null"] = 4
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(subject.BuildError):
                subject.load_scoreboard(path)

    def test_receipt_rendering_is_deterministic_and_truthful_about_absence(self) -> None:
        receipts = (
            receipt(
                EXPECTED_PINS[0],
                release={
                    "tag": "v1.2.3",
                    "date": "2026-09-01",
                    "url": "https://github.com/mrodgersjs-web/rigforge/releases/tag/v1.2.3",
                },
                smoke={
                    "state": "success",
                    "date": "2026-09-02",
                    "sha": "abcdef0123456789abcdef0123456789abcdef01",
                    "url": "https://github.com/mrodgersjs-web/rigforge/actions/runs/101",
                },
            ),
            receipt(
                EXPECTED_PINS[1],
                smoke={
                    "state": "failure",
                    "date": "2026-09-03",
                    "sha": "1234567890abcdef1234567890abcdef12345678",
                    "url": "https://github.com/mrodgersjs-web/proof-studio/actions/runs/102",
                },
            ),
            receipt(
                EXPECTED_PINS[2],
                release={
                    "tag": "v2.0.0",
                    "date": "2026-08-29",
                    "url": "https://github.com/mrodgersjs-web/proof-gate-action/releases/tag/v2.0.0",
                },
                smoke={
                    "state": "in_progress",
                    "date": "2026-09-04",
                    "sha": "fedcba9876543210fedcba9876543210fedcba98",
                    "url": "https://github.com/mrodgersjs-web/proof-gate-action/actions/runs/103",
                },
            ),
            receipt(EXPECTED_PINS[3]),
            receipt(
                EXPECTED_PINS[4],
                release={
                    "tag": "2026.09",
                    "date": "2026-09-05",
                    "url": "https://github.com/mrodgersjs-web/doctrine/releases/tag/2026.09",
                },
                smoke={
                    "state": "queued",
                    "date": "2026-09-05",
                    "sha": "00112233445566778899aabbccddeeff00112233",
                    "url": "https://github.com/mrodgersjs-web/doctrine/actions/runs/104",
                },
            ),
            receipt(
                EXPECTED_PINS[5],
                smoke={
                    "state": "cancelled",
                    "date": "2026-09-06",
                    "sha": "ffeeddccbbaa99887766554433221100ffeeddcc",
                    "url": "https://github.com/mrodgersjs-web/fde-portfolio/actions/runs/105",
                },
            ),
        )
        expected = "\n".join(
            (
                "Steward score. **not measured**",
                "",
                "| Pinned system | Latest release | Latest smoke run |",
                "| --- | --- | --- |",
                "| [rigforge](https://github.com/mrodgersjs-web/rigforge) | [v1.2.3](https://github.com/mrodgersjs-web/rigforge/releases/tag/v1.2.3) · `2026-09-01` | [success](https://github.com/mrodgersjs-web/rigforge/actions/runs/101) · `2026-09-02` · `abcdef0` |",
                "| [proof-studio](https://github.com/mrodgersjs-web/proof-studio) | no release | [failure](https://github.com/mrodgersjs-web/proof-studio/actions/runs/102) · `2026-09-03` · `1234567` |",
                "| [proof-gate-action](https://github.com/mrodgersjs-web/proof-gate-action) | [v2.0.0](https://github.com/mrodgersjs-web/proof-gate-action/releases/tag/v2.0.0) · `2026-08-29` | [in_progress](https://github.com/mrodgersjs-web/proof-gate-action/actions/runs/103) · `2026-09-04` · `fedcba9` |",
                "| [mesh-studio](https://github.com/mrodgersjs-web/mesh-studio) | no release | no smoke run |",
                "| [doctrine](https://github.com/mrodgersjs-web/doctrine) | [2026.09](https://github.com/mrodgersjs-web/doctrine/releases/tag/2026.09) · `2026-09-05` | [queued](https://github.com/mrodgersjs-web/doctrine/actions/runs/104) · `2026-09-05` · `0011223` |",
                "| [fde-portfolio](https://github.com/mrodgersjs-web/fde-portfolio) | no release | [cancelled](https://github.com/mrodgersjs-web/fde-portfolio/actions/runs/105) · `2026-09-06` · `ffeeddc` |",
            )
        )
        self.assertEqual(subject.render_recent_receipts(None, receipts), expected)
        self.assertEqual(subject.render_recent_receipts(None, receipts), expected)
        measured = subject.render_recent_receipts(
            {"date": "2026-09-07", "total": 100, "green": 83, "red": 17, "null": 0},
            receipts,
        )
        self.assertTrue(
            measured.startswith(
                "Steward score. **83/100 green**. Measured `2026-09-07`.\n\n"
            )
        )
        with self.assertRaises(subject.BuildError):
            subject.render_recent_receipts(None, tuple(reversed(receipts)))


    def test_option_like_release_tag_follows_fixed_flags_and_argv_terminator(
        self,
    ) -> None:
        calls: list[tuple[str, ...]] = []

        def fake_gh(args: tuple[str, ...]) -> object:
            calls.append(args)
            repo = args[args.index("--repo") + 1]
            if args[:2] == ("release", "list") and repo == EXPECTED_PINS[0]:
                return [
                    {
                        "name": "option-like tag",
                        "tagName": "--help",
                        "publishedAt": "2026-09-07T12:00:00Z",
                    }
                ]
            if args[:2] == ("release", "view"):
                return {
                    "tagName": "--help",
                    "publishedAt": "2026-09-07T12:00:00Z",
                    "url": (
                        "https://github.com/mrodgersjs-web/rigforge/"
                        "releases/tag/--help"
                    ),
                }
            return []

        subject.collect_receipts(fake_gh)
        self.assertIn(
            (
                "release",
                "view",
                "--repo",
                EXPECTED_PINS[0],
                "--json",
                "tagName,publishedAt,url",
                "--",
                "--help",
            ),
            calls,
        )

    def test_malformed_bracketed_github_url_is_wrapped_as_build_error(self) -> None:
        receipts = [receipt(repo) for repo in EXPECTED_PINS]
        receipts[0] = receipt(
            EXPECTED_PINS[0],
            release={
                "tag": "v1.0.0",
                "date": "2026-09-07",
                "url": (
                    "https://[github.com/mrodgersjs-web/rigforge/"
                    "releases/tag/v1.0.0"
                ),
            },
        )
        with self.assertRaises(subject.BuildError):
            subject.render_recent_receipts(None, receipts)

    def test_receipt_urls_must_match_row_repository_and_route(self) -> None:
        release = {
            "tag": "v1.0.0",
            "date": "2026-09-07",
            "url": "",
        }
        smoke = {
            "state": "success",
            "date": "2026-09-07",
            "sha": "a" * 40,
            "url": "",
        }
        cases = {
            "release-other-repository": (
                {
                    **release,
                    "url": (
                        "https://github.com/mrodgersjs-web/proof-studio/"
                        "releases/tag/v1.0.0"
                    ),
                },
                None,
            ),
            "release-wrong-route": (
                {
                    **release,
                    "url": (
                        "https://github.com/mrodgersjs-web/rigforge/"
                        "actions/runs/101"
                    ),
                },
                None,
            ),
            "smoke-other-repository": (
                None,
                {
                    **smoke,
                    "url": (
                        "https://github.com/mrodgersjs-web/proof-studio/"
                        "actions/runs/101"
                    ),
                },
            ),
            "smoke-wrong-route": (
                None,
                {
                    **smoke,
                    "url": (
                        "https://github.com/mrodgersjs-web/rigforge/"
                        "releases/tag/v1.0.0"
                    ),
                },
            ),
        }

        for name, (release_row, smoke_row) in cases.items():
            with self.subTest(name=name):
                receipts = [receipt(repo) for repo in EXPECTED_PINS]
                receipts[0] = receipt(
                    EXPECTED_PINS[0],
                    release=release_row,
                    smoke=smoke_row,
                )
                with self.assertRaises(subject.BuildError):
                    subject.render_recent_receipts(None, receipts)


class MarkerAndBuildTests(unittest.TestCase):
    def test_replacement_preserves_everything_outside_one_marker_pair(self) -> None:
        source = f"prefix\r\n{subject.START}\nold\n{subject.END}\r\nsuffix\r\n"
        expected = f"prefix\r\n{subject.START}\nnew body\n{subject.END}\r\nsuffix\r\n"
        self.assertEqual(subject.replace_recent_receipts(source, "new body"), expected)

        invalid_sources = {
            "missing-start": f"prefix\n{subject.END}\n",
            "missing-end": f"{subject.START}\nold\n",
            "duplicate-start": f"{subject.START}\n{subject.START}\n{subject.END}\n",
            "duplicate-end": f"{subject.START}\n{subject.END}\n{subject.END}\n",
            "reversed": f"{subject.END}\n{subject.START}\n",
            "inline": f"prefix {subject.START}\nold\n{subject.END}\n",
        }
        for name, invalid in invalid_sources.items():
            with self.subTest(name=name):
                with self.assertRaises(subject.BuildError):
                    subject.replace_recent_receipts(invalid, "new body")
        with self.assertRaises(subject.BuildError):
            subject.replace_recent_receipts(source, f"body {subject.START}")

    def test_github_failure_propagates_without_rewriting_readme(self) -> None:
        failure = subject.BuildError("proof-gate-action release query failed")

        def failing_gh(args: tuple[str, ...]) -> object:
            repo = args[args.index("--repo") + 1]
            if repo == EXPECTED_PINS[2]:
                raise failure
            return []

        with self.assertRaises(subject.BuildError) as caught:
            subject.collect_receipts(failing_gh)
        self.assertIs(caught.exception, failure)

        with tempfile.TemporaryDirectory() as directory:
            root = self._write_project(Path(directory), "stale")
            before = (root / "README.md").read_bytes()
            with self.assertRaises(subject.BuildError):
                subject.build_readme(root, failing_gh)
            self.assertEqual((root / "README.md").read_bytes(), before)

    def test_second_identical_build_does_not_write(self) -> None:
        def empty_gh(args: tuple[str, ...]) -> object:
            return []

        with tempfile.TemporaryDirectory() as directory:
            root = self._write_project(Path(directory), "stale")
            self.assertTrue(subject.build_readme(root, empty_gh))
            readme = root / "README.md"
            first_bytes = readme.read_bytes()
            first_mtime = readme.stat().st_mtime_ns
            self.assertFalse(subject.build_readme(root, empty_gh))
            self.assertEqual(readme.read_bytes(), first_bytes)
            self.assertEqual(readme.stat().st_mtime_ns, first_mtime)

    @staticmethod
    def _write_project(root: Path, body: str) -> Path:
        (root / "steward" / "scoreboard").mkdir(parents=True)
        (root / "steward" / "PINNED.txt").write_text(
            "\n".join(EXPECTED_PINS) + "\n", encoding="utf-8"
        )
        (root / "README.md").write_text(
            f"before\n{subject.START}\n{body}\n{subject.END}\nafter\n",
            encoding="utf-8",
        )
        return root


if __name__ == "__main__":
    unittest.main()
