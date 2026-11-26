# Senior Architect Scan-Mode Note: `strategy-studio`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Clarify boundary between src/strategy_studio/ and root rigstrategy/ package, and triage the 3 dirty working-tree files.
- **MCP 2 (`2026-07-28`) Status:** `Strict MCP 2`
- **Critical / High Findings:** None identified.

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `strategy-studio` at `/Users/rig128gb/Developer/strategy-studio` (`lang=JavaScript`, `private=False`)
- **Focus/Full Promotion Trigger:** None (mature, well-tested Python package with Strict MCP 2, CI, and 15 test modules)
- **Architecture Areas Classified:** Backend/CLI (src/strategy_studio/, rigstrategy/), Shared Modules (blueprints/, corpus/, examples/), External Services/MCP (mcp/server.py), Infrastructure (.github/workflows/rig-lattice.yml, smoke.yml, Makefile), Tests & Quality Gates (tests/ with 15 test modules)

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (10):** `pyproject.toml`, `Makefile`, `README.md`, `AGENTS.md`, `.github/workflows/rig-lattice.yml`, `.github/workflows/smoke.yml`, `tests/`, `mcp/server.py`, `src/`, `scripts/`
- **Root Entries:** 27 items | **Last Commit:** `19a56a1 2026-11-24 18:36:10 -0700 chore(rigstrategy): clean ruff lint (unused imports and 140-char line wraps); re-verified with make verify` | **Dirty Files:** `3`
- **Workflows:** `rig-lattice.yml`, `smoke.yml`
- **MCP Files:** `mcp/server.py`
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line module bodies, runtime execution, and external service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/Developer/strategy-studio` with 27 top-level entries.
- Build/package manifests observed: `pyproject.toml`, `Makefile`.
- Top-level code/tool directories observed: `src/`, `scripts/`.
- Test directories observed: `tests/`.
- MCP 2 (`2026-07-28`) status: `Strict MCP 2`.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- Inferred: rigstrategy/ is the orchestrator layer added on top of src/strategy_studio/.

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  CLI[src/strategy_studio/ & rigstrategy/] --> Corpus[corpus/ & blueprints/]
  MCP[mcp/server.py - MCP 2] --> CLI
  CI[.github/workflows/smoke.yml & rig-lattice.yml] --> Tests[tests/]
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts)
- **[Medium | Direct] Separation of Concerns — Dual Top-Level Python Packages**
  - *Evidence:* Both src/strategy_studio/ and top-level rigstrategy/ exist in the same repo.
  - *Impact & Proposed Smallest Safe Correction:* Splits package layout between src-layout and flat-layout; proposed: document ownership or consolidate rigstrategy/ under src/.
- **[Low | Direct] Convention Drift — Uncommitted Local Changes**
  - *Evidence:* git status shows 3 dirty files.
  - *Impact & Proposed Smallest Safe Correction:* Minor local drift; proposed: inspect and commit or clean.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** Are both src/strategy_studio and rigstrategy packaged in pyproject.toml?
- **Risks:** None significant; `make verify` passed at commit 19a56a1.
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Inspect the 3 dirty files.
  - Run `make verify` if local edits touched Python files.

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test directory, and MCP 2 status (`Strict MCP 2`) traces directly to inspected local files at `/Users/rig128gb/Developer/strategy-studio`; inferences are explicitly labeled `Inferred`.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of this single repository; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
