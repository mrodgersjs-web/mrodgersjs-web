# GitHub steward

## Copilot code review settings probe, 2026-09-08

- `PUT /repos/mrodgersjs-web/rigforge/copilot/code-review/settings` returned `404`.
- The logged-in `rigforge` **Settings > Copilot** page showed only **Cloud agent**, **Internet access**, and **MCP servers**.
- No code-review or custom-instructions toggle was available in that UI.

The unavailable code review setting is not claimed as enabled.

## Repository instructions

`.github/copilot-instructions.md` is present in the profile repository and all six pinned repositories: `rigforge`, `proof-studio`, `proof-gate-action`, `mesh-studio`, `doctrine`, and `fde-portfolio`.

## Claude Desktop stdio

Install `uv`, clone the profile repository, and replace the example `cwd` with that clone's path. `uv` supplies the MCP package for the otherwise stdlib catalog server.

```json
{
  "mcpServers": {
    "github-public-catalog": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]<2",
        "python",
        "steward/catalog_mcp.py"
      ],
      "cwd": "/path/to/mrodgersjs-web"
    }
  }
}
```

The resulting stdio command is `uv run --with "mcp[cli]<2" python steward/catalog_mcp.py`, launched from the profile clone.

## Per-repo scorecard (Measure + Pick)

`steward/repo_scorecard.py` scores every repo listed in `steward/scorecard.json` on ten dimensions, each 0 to 1 with its raw evidence: latest non-skipped default-branch CI run, test files, runnable entrypoint, code vs markdown lines (scaffold check), GitHub release, README demo GIF, LICENSE and SECURITY.md, topics and description, days since last push, and open issues older than 30 days. Skipped CI runs are neutral: they are passed over, never counted as pass or fail.

File facts come from an anonymous shallow `git clone`, so they cost no API quota. REST reads use `GH_TOKEN` when set and stop at the `api_reserve` quota floor; anything not measured is `n/a` and is left out of the average.

The Pick step names the lowest dimension per repo (ties go to the earlier dimension in the table) with one concrete action. Outputs: `steward/scoreboard/repos.json` and `steward/scoreboard/SCORECARD.md`.

```bash
python3 -m unittest steward.test_repo_scorecard   # no network; uses steward/fixtures/scorecard/
python3 steward/repo_scorecard.py --repo rigforge --no-write   # one repo, print JSON only
python3 steward/repo_scorecard.py --no-api        # file facts only, zero API calls
```
