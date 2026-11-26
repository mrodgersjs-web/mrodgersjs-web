# Senior Architect Scan-Mode Note: `rig-deviate`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Review and commit the 6 uncommitted MCP 2 / lattice retrofit files after running `pytest test/`.
- **MCP 2 (`2026-07-28`) Status:** `Strict MCP 2`
- **Critical / High Findings:** None identified.

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `rig-deviate` at `/Users/rig128gb/Developer/rig-deviate` (`lang=Python`, `private=False`, `inManifest38=True`)
- **Focus/Full Promotion Trigger:** None (clean, tested Python CLI + Strict MCP 2 server; Scan Mode sufficient)
- **Architecture Areas Classified:** Backend / CLI (`rig_deviate/cli.py`, `pyproject.toml`); MCP Surface (`mcp/server.py` Strict MCP 2); Tests & CI (`test/` 5 suites, `ci.yml`, `smoke.yml`, `rig-lattice.yml`); Documentation (`docs/architecture.md`, `AGENTS.md`, `examples/`); Frontend / Database (Not observed)

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (8):** `.github/workflows/ci.yml`, `.github/workflows/rig-lattice.yml`, `.github/workflows/smoke.yml`, `AGENTS.md`, `README.md`, `docs/architecture.md`, `mcp/server.py`, `pyproject.toml`
- **Root Entries:** 20 items (`.coverage, .github/, .pytest_cache/, .rig/, .ruff_cache/, AGENTS.md, CHANGELOG.md, CODE_OF_CONDUCT.md, CONTRIBUTING.md, LICENSE, README.md, SECURITY.md...`)
- **Last Commit:** `9a6c0d5 2026-10-20 01:20:02 -0600 test: add repo hygiene checks for code owners, docs, and workflows`
- **Git Working Tree:** `6` dirty/untracked entries (`M .github/workflows/rig-lattice.yml`, `M mcp/server.py`, `M rig.repos.json`, `?? .coverage`)
- **Workflows:** `.github/workflows/ci.yml`, `.github/workflows/rig-lattice.yml`, `.github/workflows/smoke.yml`
- **MCP Files:** `mcp/server.py`
- **Existing Architecture Docs:** `AGENTS.md`, `docs/architecture.md`
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line function bodies, runtime execution, and external network/service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/Developer/rig-deviate` (branch `ghup/2026-10-19`) with 20 top-level entries and 49 sampled files (depth <= 3).
- Build/package manifests observed: `pyproject.toml`.
- Top-level source/tool directories observed: `mcp/`.
- Entrypoints observed: `mcp/server.py`, `rig_deviate/cli.py`.
- Tests observed: 5 sampled test file(s) (`test/test_engines.py`, `test/test_ladder_truth.py`, `test/test_packaging_config.py`, `test/test_readme_truth.py`).
- MCP 2 (`2026-07-28`) status: `Strict MCP 2`.
- Committed/untracked secret-file candidates observed: None identified.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- Inferred: 40-engine draft-rewriting and generic-AI-distance scoring CLI (`rig_deviate/cli.py`) exposed over Strict MCP 2 (`mcp/server.py`).

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  CLI[rig_deviate/cli.py] --> Engines[40 Deviation Engines + Scorer]
  MCP[mcp/server.py Strict MCP 2] --> CLI
  Tests[test/ 5 suites + 3 GH Workflows] --> Engines
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts, MCP 2)
- **[Medium | Direct] Convention Drift — Uncommitted MCP 2 & Lattice Retrofit**
  - *Evidence:* 6 dirty files including `M .github/workflows/rig-lattice.yml`, `M mcp/server.py`, `M rig.repos.json`.
  - *Impact:* Local Strict MCP 2 and hygiene updates are uncommitted.
  - *Proposed Smallest Safe Correction (Requires Approval):* Review `git diff`, run `pytest test/`, and commit the 6 modified files.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** None identified
- **Risks:** Uncommitted changes to `mcp/server.py` could drift from published package/remote.
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Review and commit the 6 dirty files after running `test/`.

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test file, git status count, and MCP 2 status (`Strict MCP 2`) traces directly to inspected local files at `/Users/rig128gb/Developer/rig-deviate`; inferences and assumptions are explicitly labeled.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of `rig-deviate`; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, promotion gate status, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
