# Agent guide

## Purpose

This is the public GitHub profile repository for Mike Rodgers. Its executable surface is the stdlib README steward, which validates pinned repositories, collects public GitHub receipts, and updates only the managed receipt block.

## Repository map

- `steward/`: pin source, README builder, tests, and scoreboard assets.
- `assets/`: public profile imagery.
- `.github/`: Copilot repository instructions and the scheduled steward workflow.
- `graft/`: generated cross-repository context. Read it when useful and preserve it unchanged.

## Proven commands

No package bootstrap is required. Use `/usr/bin/python3`; the README refresh also requires an authenticated `gh` CLI.

Run the smoke sequence from the repository root, in this order:

```bash
/usr/bin/python3 -m unittest steward.test_build_readme -v
/usr/bin/python3 steward/build_readme.py
```

The second command is the runtime entry point for refreshing public receipts.

## Constraints

- Keep `steward/PINNED.txt` as the only pin source.
- Keep static README content human-owned; `build_readme.py` owns only the bytes between the receipt markers.
- Keep the steward implementation and tests stdlib-only. GitHub access stays behind the argv-form `gh` adapter and fails closed.
- The scorer, not the README builder, owns scoreboard outputs.
- Preserve public-boundary discipline: no secrets, private data, or unsupported claims.
- Always run the smoke command before claiming done.

## RIG lattice contract (stamped)

This repository runs the shared RIG lattice: loops in `.rig/loop.yaml`, pre-tool
hooks in `.rig/hooks/`, CI gate in `.github/workflows/rig-lattice.yml`, execution
owner routing in `.rig/work-routing.yaml` (operator standard 2026-09-11), and a
results-driven MCP server at `mcp/server.py` returning verified results only.
D85 rules apply: every outward action needs a Gate-D request + typed approval;
durable builds need four ratios >= 0.85 and a sealed proof. Done-claims need TAC
close-gate sealed evidence. Shared agent substrate lives in Supabase schema
`rig_shared` (see PROGRAM.md in rig-lattice-retrofit).
