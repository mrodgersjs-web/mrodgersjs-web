# Senior Architect Scan-Mode Note: `jakebrain`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check.
- **MCP 2 (`2026-07-28`) Status:** `Legacy MCP v1 (upgrade needed)`
- **Critical / High Findings:** [High] MCP 2 Protocol Drift

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `jakebrain` at `/Users/rig128gb/Developer/jakebrain` (`lang=Python`, `private=True`)
- **Focus/Full Promotion Trigger:** Focus/Full Mode candidate — 4 architecture areas, 85726 files, or High/Critical findings (1).
- **Architecture Areas Classified:** Backend/CLI, AI/Agents, MCP Surface, Tests & Quality Gates

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (60):** `corpus/run_on_host.sh`, `harness/run.py`, `legacy/jake-brain-wire/_ref/cli.py`, `legacy/jake-brain-wire/evidence/_tmp/real2/jake_brain/cli.py`, `memory/runtime.py`, `architecture/JAKEBRAIN-DEDICATED-COMPUTER-BLUEPRINT.md`, `architecture/brain-organs-and-levels.json`, `blueprints/cognitive-architecture/BLUEPRINT.md`, `blueprints/cognitive-architecture/catalog.json`, `legacy/jake-brain-v20/bridge/samples/call_mcp.py`, `legacy/jake-brain-v20/bridge/tests/fixtures/mcp-brain_status.2026-11-10.json`, `legacy/jake-brain-v20/coach-james/_gen/stub/mcp/__init__.py`, `legacy/jake-brain-v20/coach-james/_gen/stub/mcp/server/__init__.py`
- **Root Entries:** 21 items | **Tracked Files:** 85726 | **Last Commit:** `4992b62f5 2026-11-24 23:36:53 -0700 rsi step 18: update locked.json to the 21-file manifest (13 external + 8 self-locked)` | **Dirty Entries:** `2`
- **Workflows:** Not observed
- **MCP Files:** `legacy/jake-brain-v20/bridge/samples/call_mcp.py`, `legacy/jake-brain-v20/bridge/tests/fixtures/mcp-brain_status.2026-11-10.json`, `legacy/jake-brain-v20/coach-james/_gen/stub/mcp/__init__.py`, `legacy/jake-brain-v20/coach-james/_gen/stub/mcp/server/__init__.py`, `legacy/jake-brain-v20/coach-james/_gen/stub/mcp/server/fastmcp/__init__.py`, `legacy/jake-brain-v20/coach-james/_gen/stub/mcp/server/fastmcp/prompts/__init__.py`
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line module bodies, runtime execution, and external service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/Developer/jakebrain` on branch `main` with 21 top-level entries.
- Build/package manifests observed: Not observed.
- Entrypoints observed: `corpus/run_on_host.sh`, `harness/run.py`, `legacy/jake-brain-wire/_ref/cli.py`, `legacy/jake-brain-wire/evidence/_tmp/real2/jake_brain/cli.py`, `memory/runtime.py`, `sources/RIGIntelligence/jake-app/src-tauri/src/lib.rs`.
- Test files/suites observed: 25 (`appliance/test_appliance.py`, `brain/s13-plan/done-test-write/META.md`, `brain/s13-plan/done-test-write/harness/bad.json`, `brain/s13-plan/done-test-write/harness/check.py`).
- Existing architecture docs observed: `architecture/JAKEBRAIN-DEDICATED-COMPUTER-BLUEPRINT.md`, `architecture/brain-organs-and-levels.json`, `blueprints/cognitive-architecture/BLUEPRINT.md`, `blueprints/cognitive-architecture/catalog.json`.
- MCP 2 (`2026-07-28`) status: `Legacy MCP v1 (upgrade needed)`.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- `Inferred`: Repository functions primarily as a documentation, corpus, or script-driven workspace without a standard package manifest.

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  Entry["Entrypoints (corpus/run_on_host.sh)"] --> Core["Core (brain/)"]
  Core["Core (brain/)"] --> MCP["MCP (legacy/jake-brain-v20/bridge/samples/call_mcp.py)"]
  MCP["MCP (legacy/jake-brain-v20/bridge/samples/call_mcp.py)"] --> Data["Specs/Data (blueprints/)"]
  Data["Specs/Data (blueprints/)"] --> QA["Tests & CI (25 tests, 0 workflows)"]
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts)
- **[High | Direct] MCP 2 Protocol Drift**
  - *Evidence:* MCP files (legacy/jake-brain-v20/bridge/samples/call_mcp.py, legacy/jake-brain-v20/bridge/tests/fixtures/mcp-brain_status.2026-11-10.json, legacy/jake-brain-v20/coach-james/_gen/stub/mcp/__init__.py) use legacy MCP v1/FastMCP or 2024-11-05 protocol without Strict MCP 2 (2026-07-28) server/discover and _meta enforcement.
  - *Impact & Proposed Smallest Safe Correction:* Breaks forward compatibility with Strict MCP 2 hosts and lacks protocolVersion 2026-07-28 contract gating. Proposed: Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check.
- **[Medium | Direct] Architecture Debt — Missing CI Workflow**
  - *Evidence:* No .github/workflows/ CI files observed despite executable entrypoints/manifests (corpus/run_on_host.sh).
  - *Impact & Proposed Smallest Safe Correction:* Changes lack automated CI verification on push/PR. Proposed: Add minimal CI workflow running tests/linting.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** What is the target timeline for migrating legacy MCP v1/FastMCP endpoints to Strict MCP 2 (`2026-07-28`)?
- **Risks:** Legacy MCP v1 surface may fail Strict MCP 2 host validation.
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Run the existing test suite locally to verify baseline health.
  - Upgrade MCP endpoints to Strict MCP 2 (`2026-07-28`) and add `rig-lattice.yml` CI verification (requires approval).

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test directory, and MCP 2 status (`Legacy MCP v1 (upgrade needed)`) traces directly to inspected local files at `/Users/rig128gb/Developer/jakebrain`; inferences are explicitly labeled `Inferred`.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of this single repository; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
