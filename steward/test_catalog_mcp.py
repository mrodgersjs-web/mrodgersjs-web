from __future__ import annotations

import base64
import json
import unittest
from collections.abc import Callable

from steward import catalog_mcp as subject


Api = Callable[[str], object]


def raw_repo(
    name: str,
    *,
    private: bool = False,
    owner: str = subject.OWNER,
    visibility: str = "public",
) -> dict[str, object]:
    return {
        "name": name,
        "full_name": f"{owner}/{name}",
        "description": f"{name} description",
        "private": private,
        "visibility": visibility,
        "archived": False,
        "default_branch": "main",
        "html_url": f"https://github.com/{owner}/{name}",
        "updated_at": "2026-09-08T12:00:00Z",
        "language": "Python",
        "owner": {"login": owner},
    }


def score_api(content: str | None) -> Api:
    base = f"repos/{subject.OWNER}/{subject.PROFILE_REPO}"

    def api(endpoint: str) -> object:
        if endpoint == base:
            return raw_repo(subject.PROFILE_REPO)
        if endpoint == f"{base}/git/trees/main":
            return {
                "truncated": False,
                "tree": [
                    {
                        "path": "steward",
                        "type": "tree",
                        "mode": "040000",
                        "sha": "tree-steward",
                    }
                ],
            }
        if endpoint == f"{base}/git/trees/tree-steward":
            return {
                "truncated": False,
                "tree": [
                    {
                        "path": "scoreboard",
                        "type": "tree",
                        "mode": "040000",
                        "sha": "tree-scoreboard",
                    }
                ],
            }
        if endpoint == f"{base}/git/trees/tree-scoreboard":
            entries: list[dict[str, object]] = []
            if content is not None:
                entries.append(
                    {
                        "path": "latest.json",
                        "type": "blob",
                        "mode": "100644",
                        "sha": "blob-score",
                        "size": len(content.encode("utf-8")),
                    }
                )
            return {"truncated": False, "tree": entries}
        if endpoint == f"{base}/git/blobs/blob-score" and content is not None:
            return {
                "sha": "blob-score",
                "encoding": "base64",
                "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
                "size": len(content.encode("utf-8")),
            }
        raise AssertionError(f"unexpected endpoint: {endpoint}")

    return api


class CatalogContractTests(unittest.TestCase):
    def test_list_public_repos_filters_private_and_other_owner_rows(self) -> None:
        def api(endpoint: str) -> object:
            self.assertIn(f"users/{subject.OWNER}/repos?", endpoint)
            return [
                raw_repo("rigforge"),
                raw_repo("private-repo", private=True, visibility="private"),
                raw_repo("other", owner="someone-else"),
            ]

        self.assertEqual(
            subject.list_public_repos(api),
            {
                "repositories": [
                    {
                        "name": "rigforge",
                        "full_name": "mrodgersjs-web/rigforge",
                        "description": "rigforge description",
                        "language": "Python",
                        "default_branch": "main",
                        "archived": False,
                        "url": "https://github.com/mrodgersjs-web/rigforge",
                        "updated_at": "2026-09-08T12:00:00Z",
                    }
                ],
                "next_cursor": None,
            },
        )

    def test_pagination_uses_an_opaque_cursor(self) -> None:
        calls: list[str] = []

        def api(endpoint: str) -> object:
            calls.append(endpoint)
            if "page=1" in endpoint:
                return [raw_repo(f"repo-{index:02d}") for index in range(subject.PAGE_SIZE)]
            if "page=2" in endpoint:
                return [raw_repo("last-repo")]
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        first = subject.list_public_repos(api)
        cursor = first["next_cursor"]
        self.assertIsInstance(cursor, str)
        self.assertNotEqual(cursor, "2")
        self.assertEqual(subject.page_number(cursor), 2)

        second = subject.list_public_repos(api, cursor)
        self.assertEqual([row["name"] for row in second["repositories"]], ["last-repo"])
        self.assertIsNone(second["next_cursor"])
        self.assertTrue(any("page=1" in endpoint for endpoint in calls))
        self.assertTrue(any("page=2" in endpoint for endpoint in calls))
        with self.assertRaises(subject.CatalogError):
            subject.page_number("not-a-cursor")

    def test_repo_and_path_validation_fail_closed(self) -> None:
        for invalid in ("", "owner/repo", "../repo", "--help", "repo name"):
            with self.subTest(repo=invalid):
                with self.assertRaises(subject.CatalogError):
                    subject.valid_repo(invalid)

        for credential_path in (
            ".env",
            "config/.env.production",
            "credentials.json",
            "keys/id_rsa",
            "certs/client.pem",
            "certs/client.key",
            "certs/client.p12",
        ):
            with self.subTest(path=credential_path):
                with self.assertRaises(subject.CatalogError):
                    subject.valid_path(credential_path)

        def private_api(endpoint: str) -> object:
            return raw_repo("private-repo", private=True, visibility="private")

        with self.assertRaises(subject.CatalogError):
            subject.repo_info(private_api, "private-repo")

        def public_api(endpoint: str) -> object:
            return raw_repo("rigforge")

        self.assertEqual(
            subject.repo_info(public_api, "rigforge"),
            {
                "name": "rigforge",
                "full_name": "mrodgersjs-web/rigforge",
                "description": "rigforge description",
                "language": "Python",
                "default_branch": "main",
                "archived": False,
                "url": "https://github.com/mrodgersjs-web/rigforge",
                "updated_at": "2026-09-08T12:00:00Z",
            },
        )

    def test_readme_search_excludes_unsafe_results_and_shapes_public_rows(self) -> None:
        safe = {
            "name": "README.md",
            "path": "README.md",
            "sha": "a" * 40,
            "html_url": "https://github.com/mrodgersjs-web/rigforge/blob/main/README.md",
            "repository": raw_repo("rigforge"),
        }
        private = {
            **safe,
            "repository": raw_repo("private-repo", private=True, visibility="private"),
        }
        credential_like = {
            **safe,
            "path": ".env/README.md",
        }
        other_owner = {
            **safe,
            "repository": raw_repo("rigforge", owner="someone-else"),
        }
        not_readme = {
            **safe,
            "path": "docs/guide.md",
        }

        def api(endpoint: str) -> object:
            self.assertIn("search/code?", endpoint)
            return {
                "total_count": 5,
                "incomplete_results": False,
                "items": [safe, private, credential_like, other_owner, not_readme],
            }

        self.assertEqual(
            subject.search_public_readmes(api, "ProofPacket"),
            {
                "results": [
                    {
                        "repo": "rigforge",
                        "path": "README.md",
                        "sha": "a" * 40,
                        "url": (
                            "https://github.com/mrodgersjs-web/rigforge/"
                            "blob/main/README.md"
                        ),
                    }
                ],
                "next_cursor": None,
                "incomplete_results": False,
            },
        )

    def test_steward_score_distinguishes_absence_from_malformed_data(self) -> None:
        self.assertEqual(
            subject.get_steward_score(score_api(None)),
            {"measured": False, "score": None, "date": None},
        )

        valid = json.dumps(
            {
                "date": "2026-09-08",
                "summary": {"total": 100, "green": 83, "red": 17},
                "criteria": [],
            }
        )
        self.assertEqual(
            subject.get_steward_score(score_api(valid)),
            {
                "measured": True,
                "score": 83,
                "total": 100,
                "green": 83,
                "red": 17,
                "date": "2026-09-08",
            },
        )

        for malformed in (
            "{not json",
            json.dumps(
                {
                    "date": "2026-09-08",
                    "summary": {"total": 100, "green": 90, "red": 9},
                    "criteria": [],
                }
            ),
        ):
            with self.subTest(malformed=malformed):
                with self.assertRaises(subject.CatalogError):
                    subject.get_steward_score(score_api(malformed))

    def test_provider_errors_propagate_without_becoming_empty_results(self) -> None:
        failure = subject.CatalogError(
            "GitHub read failed (HTTP 403). Check authentication and rate limits, then retry."
        )

        def failing_api(endpoint: str) -> object:
            raise failure

        operations = (
            lambda: subject.list_public_repos(failing_api),
            lambda: subject.repo_info(failing_api, "rigforge"),
            lambda: subject.search_public_readmes(failing_api, "proof"),
            lambda: subject.get_steward_score(failing_api),
        )
        for operation in operations:
            with self.subTest(operation=operation):
                with self.assertRaises(subject.CatalogError) as caught:
                    operation()
                self.assertIs(caught.exception, failure)

    def test_regular_file_rejects_symlinks_and_returns_immutable_blob(self) -> None:
        base = f"repos/{subject.OWNER}/rigforge"

        def symlink_api(endpoint: str) -> object:
            if endpoint == f"{base}/git/trees/main":
                return {
                    "truncated": False,
                    "tree": [
                        {
                            "path": "README.md",
                            "type": "blob",
                            "mode": "120000",
                            "sha": "link-sha",
                            "size": 20,
                        }
                    ],
                }
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        with self.assertRaises(subject.CatalogError):
            subject.regular_file(symlink_api, base, "README.md", "main")

        content = "public readme\n"

        def file_api(endpoint: str) -> object:
            if endpoint == f"{base}/git/trees/main":
                return {
                    "truncated": False,
                    "tree": [
                        {
                            "path": "README.md",
                            "type": "blob",
                            "mode": "100644",
                            "sha": "blob-sha",
                            "size": len(content),
                        }
                    ],
                }
            if endpoint == f"{base}/git/blobs/blob-sha":
                return {
                    "sha": "blob-sha",
                    "encoding": "base64",
                    "content": base64.b64encode(content.encode()).decode(),
                    "size": len(content),
                }
            raise AssertionError(f"unexpected endpoint: {endpoint}")

        blob = subject.regular_file(file_api, base, "README.md", "main")
        self.assertEqual(blob["sha"], "blob-sha")
        self.assertEqual(blob["path"], "README.md")
        self.assertEqual(blob["content"], content)

    def test_exactly_four_read_only_tools_have_decision_guiding_descriptions(self) -> None:
        self.assertEqual(
            tuple(subject.TOOL_DESCRIPTIONS),
            (
                "list_public_repos",
                "repo_info",
                "search_public_readmes",
                "get_steward_score",
            ),
        )
        self.assertEqual(
            subject.TOOL_ANNOTATIONS,
            {
                "readOnlyHint": True,
                "destructiveHint": False,
                "openWorldHint": True,
            },
        )
        for name, description in subject.TOOL_DESCRIPTIONS.items():
            with self.subTest(tool=name):
                sentences = description.split(". ")
                self.assertGreaterEqual(len(sentences), 2)
                self.assertLessEqual(len(sentences), 4)
                self.assertIn("Use ", description)


if __name__ == "__main__":
    unittest.main()
