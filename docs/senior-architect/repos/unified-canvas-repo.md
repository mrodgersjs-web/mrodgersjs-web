# Senior Architect Scan-Mode Note: `unified-canvas-repo`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Remove the .pre-theme-parity.bak files in web/ and add a minimal package.json so node --test scripts are discoverable.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Critical / High Findings:** None identified.

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `unified-canvas-repo` at `/Users/rig128gb/rig-builds/unified-canvas-repo` (`lang=JavaScript`, `private=True`)
- **Focus/Full Promotion Trigger:** None (clean P2 Node canvas server; 0 dirty files)
- **Architecture Areas Classified:** Frontend (web/index.html, app.js, canvas.css, rig-theme.js), Backend (ucanvas/server.mjs, cli.mjs), Infrastructure (launchd/com.rig.unified-canvas.plist), Tests & Quality Gates (tests/unit.test.mjs, acceptance.test.mjs, snapshots.test.mjs)

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (4):** `README.md`, `tests/`, `web/`, `tools/`
- **Root Entries:** 13 items | **Last Commit:** `f55ecb7 2026-11-09 19:22:02 -0600 Initial import: unified-canvas-repo (consolidation 2026-11-09)` | **Dirty Files:** `0`
- **Workflows:** Not observed
- **MCP Files:** Not observed
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line module bodies, runtime execution, and external service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/rig-builds/unified-canvas-repo` with 13 top-level entries.
- Build/package manifests observed: Not observed.
- Top-level code/tool directories observed: `web/`, `tools/`.
- Test directories observed: `tests/`.
- MCP 2 (`2026-07-28`) status: `No MCP surface observed`.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- Inferred: Zero-dependency Node ESM server managed by launchd on 127.0.0.1:4919.

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  Web[web/app.js & rig-theme.js] --> Server[ucanvas/server.mjs :4919]
  CLI[ucanvas/cli.mjs] --> Server
  Tests[tests/*.test.mjs] --> Server
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts)
- **[Low | Direct] Convention Drift — Backup Files & Missing package.json**
  - *Evidence:* web/ contains index.html.pre-theme-parity.bak and canvas.css.pre-theme-parity.bak; root lacks package.json.
  - *Impact & Proposed Smallest Safe Correction:* Minor clutter and missing standard Node manifest; proposed: remove .bak files and add package.json.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** None identified
- **Risks:** None identified
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Run node --test tests/*.test.mjs.
  - Remove web/*.pre-theme-parity.bak files.

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test directory, and MCP 2 status (`No MCP surface observed`) traces directly to inspected local files at `/Users/rig128gb/rig-builds/unified-canvas-repo`; inferences are explicitly labeled `Inferred`.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of this single repository; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
