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
