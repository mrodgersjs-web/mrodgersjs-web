# Plan: v0 → v2 RIG + fleet operating-system upgrade

Depth: tree 3   Mode: orchestrated
Budget note: research + live measurement + one integration report. Not an implementation sprint.

## Contract

- Interfaces: each leaf writes one JSON file under `docs/v2-upgrade/`. Integration reads those four files only plus `~/Developer/jake-workflows/docs/JAKE-PAI-V2.md` as *prior opinion*, never as evidence.
- Data ownership:
  - leaf-v0 → `docs/v2-upgrade/leaf-v0-measured.json`
  - leaf-consulting → `docs/v2-upgrade/leaf-consulting.json`
  - leaf-1000x → `docs/v2-upgrade/leaf-1000x-process.json`
  - leaf-fleet → `docs/v2-upgrade/leaf-fleet.json`
  - driver → `docs/v2-upgrade/REPORT.md`, `GATES.md` evidence, `proof/`
- Naming: JSON keys snake_case. Every count has `source` (command or path). Unverified numbers labeled `[UNVERIFIED]`.
- No Gate-D promotions. No outbound send/publish.

## Tree

- 1 v0→v2 operating-system brief .......... GATES.md
  - 1.1 Measure live v0 .................. docs/v2-upgrade/leaf-v0-measured.json
  - 1.2 Consulting-firm primary sources .. docs/v2-upgrade/leaf-consulting.json
  - 1.3 1000x process already on disk ..... docs/v2-upgrade/leaf-1000x-process.json
  - 1.4 Fleet + systems inventory ......... docs/v2-upgrade/leaf-fleet.json

## Status log

- 2026-08-30T19:40Z leaves persisted by driver (scouts write-blocked on xd://)
- 2026-08-30T19:45Z REPORT.md written; gate-check 6/7 then G7 filled
- 2026-08-30T18:20Z plan written, contract fixed
