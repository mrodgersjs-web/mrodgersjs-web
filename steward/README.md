# GitHub steward

## Copilot code review settings probe, 2026-09-08

- `PUT /repos/mrodgersjs-web/rigforge/copilot/code-review/settings` returned `404`.
- The logged-in `rigforge` **Settings > Copilot** page showed only **Cloud agent**, **Internet access**, and **MCP servers**.
- No code-review or custom-instructions toggle was available in that UI.

The unavailable code review setting is not claimed as enabled.

## Repository instructions

`.github/copilot-instructions.md` is present in the profile repository and all six pinned repositories: `rigforge`, `proof-studio`, `proof-gate-action`, `mesh-studio`, `doctrine`, and `fde-portfolio`.
