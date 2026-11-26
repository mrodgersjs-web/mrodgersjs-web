# Senior Architect Scan-Mode Note: `aside-ui-build-repo`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check.
- **MCP 2 (`2026-07-28`) Status:** `Legacy MCP v1 (upgrade needed)`
- **Critical / High Findings:** [High] MCP 2 Protocol Drift

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `aside-ui-build-repo` at `/Users/rig128gb/Developer/aside-rig-os` (`lang=CSS`, `private=True`)
- **Focus/Full Promotion Trigger:** Focus/Full Mode candidate — 5 architecture areas, 282 files, or High/Critical findings (1).
- **Architecture Areas Classified:** Frontend, Backend/CLI, AI/Agents, MCP Surface, Tests & Quality Gates

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (17):** `package.json`, `tsconfig.json`, `vite.config.ts`, `services/engines-media/uem/cli.py`, `services/engines-media/uem/server.py`, `services/src/server.ts`, `docs/ADE-V2-DESIGN.md`, `openspec/changes/aside-audit-133-repairs/design.md`, `openspec/changes/omp-aside-harness/design.md`, `openspec/schemas/behavior-driven/templates/design.md`, `services/engines-media/uem/mcp_engines.py`, `services/engines-media/uem/mcp_media.py`
- **Root Entries:** 28 items | **Tracked Files:** 282 | **Last Commit:** `372b06a 2026-10-30 09:41:05 -0500 correction: the 401 was the wrong port, and the documented thread route renders nothing in a detached tab` | **Dirty Entries:** `258`
- **Workflows:** Not observed
- **MCP Files:** `services/engines-media/uem/mcp_engines.py`, `services/engines-media/uem/mcp_media.py`, `services/engines-media/uem/server.py`
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line module bodies, runtime execution, and external service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/Developer/aside-rig-os` on branch `codex/omp-aside-harness-20261015` with 28 top-level entries.
- Build/package manifests observed: `package.json`, `tsconfig.json`, `vite.config.ts`.
- Entrypoints observed: `services/engines-media/uem/cli.py`, `services/engines-media/uem/server.py`, `services/src/server.ts`.
- Test files/suites observed: 25 (`qa/rig-rowboat-dyad.test.mjs`, `services/engines-media/tests/__init__.py`, `services/engines-media/tests/__pycache__/__init__.cpython-312.pyc`, `services/engines-media/tests/__pycache__/conftest.cpython-312-pytest-9.2.0.pyc`).
- Existing architecture docs observed: `docs/ADE-V2-DESIGN.md`, `openspec/changes/aside-audit-133-repairs/design.md`, `openspec/changes/omp-aside-harness/design.md`, `openspec/schemas/behavior-driven/templates/design.md`.
- MCP 2 (`2026-07-28`) status: `Legacy MCP v1 (upgrade needed)`.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- `Inferred`: Primary runtime behavior aligns with the observed manifests and entrypoint layout.

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  Entry["Entrypoints (services/engines-media/uem/cli.py)"] --> Core["Core (src/)"]
  Core["Core (src/)"] --> MCP["MCP (services/engines-media/uem/mcp_engines.py)"]
  MCP["MCP (services/engines-media/uem/mcp_engines.py)"] --> QA["Tests & CI (25 tests, 0 workflows)"]
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts)
- **[High | Direct] MCP 2 Protocol Drift**
  - *Evidence:* MCP files (services/engines-media/uem/mcp_engines.py, services/engines-media/uem/mcp_media.py, services/engines-media/uem/server.py) use legacy MCP v1/FastMCP or 2024-11-05 protocol without Strict MCP 2 (2026-07-28) server/discover and _meta enforcement.
  - *Impact & Proposed Smallest Safe Correction:* Breaks forward compatibility with Strict MCP 2 hosts and lacks protocolVersion 2026-07-28 contract gating. Proposed: Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check.
- **[Medium | Direct] Architecture Debt — Uncommitted Workspace Drift**
  - *Evidence:* Working tree has 258 uncommitted/untracked entries in git status.
  - *Impact & Proposed Smallest Safe Correction:* High uncommitted surface increases risk of drift between local state and pushed repo. Proposed: Triage, commit, or gitignore uncommitted files before handoff.
- **[Medium | Direct] Architecture Debt — Missing CI Workflow**
  - *Evidence:* No .github/workflows/ CI files observed despite executable entrypoints/manifests (package.json, tsconfig.json, vite.config.ts).
  - *Impact & Proposed Smallest Safe Correction:* Changes lack automated CI verification on push/PR. Proposed: Add minimal CI workflow running tests/linting.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** What is the target timeline for migrating legacy MCP v1/FastMCP endpoints to Strict MCP 2 (`2026-07-28`)?
- **Risks:** 258 uncommitted/untracked workspace entries may diverge from remote state.
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Run the existing test suite locally to verify baseline health.
  - Upgrade MCP endpoints to Strict MCP 2 (`2026-07-28`) and add `rig-lattice.yml` CI verification (requires approval).
  - Review and commit or clean uncommitted local changes (requires approval).

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test directory, and MCP 2 status (`Legacy MCP v1 (upgrade needed)`) traces directly to inspected local files at `/Users/rig128gb/Developer/aside-rig-os`; inferences are explicitly labeled `Inferred`.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of this single repository; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
