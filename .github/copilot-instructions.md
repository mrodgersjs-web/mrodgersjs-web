# Copilot instructions

## Repository purpose

This public profile is backed by a stdlib README steward. The steward validates the canonical six pins, collects public release and smoke receipts through `gh`, and replaces only the unique managed block in `README.md`.

## Work map

- `steward/`: `PINNED.txt`, builder, unittest module, and scoreboard assets.
- `assets/`: profile media.
- `.github/`: Copilot repository instructions.
- `graft/`: generated context; read when needed and leave unchanged.

## Commands

There is no dependency bootstrap. Use `/usr/bin/python3`; refreshing receipts also requires an authenticated `gh` CLI.

Run from the repository root, in order:

```bash
/usr/bin/python3 -m unittest steward.test_build_readme -v
/usr/bin/python3 steward/build_readme.py
```

The builder command is the runtime entry point.

## Editing rules

- `steward/PINNED.txt` is the only pin source.
- Preserve exactly one ordered receipt marker pair. Static README bytes outside it are human-owned.
- Keep Python and tests stdlib-only. Keep provider access behind one argv-form `gh` adapter and fail closed on malformed or unavailable data.
- The builder does not write scoreboard badge or score files.
- Keep public claims evidence-backed and exclude secrets or private data.
- Always run the smoke command before claiming done.
