# Senior Architect Scan-Mode Note: `unified-voice-repo`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Remove web/panel.html.pre-theme-parity.bak and add a root pyproject.toml for uvoice/.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Critical / High Findings:** None identified.

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `unified-voice-repo` at `/Users/rig128gb/rig-builds/unified-voice-repo` (`lang=Python`, `private=True`)
- **Focus/Full Promotion Trigger:** None (clean P5 Jarvis voice layer; 0 dirty files)
- **Architecture Areas Classified:** Frontend (web/panel.html, panel.js, rig-theme.js), Backend/CLI (uvoice/), Infrastructure (launchd/), Tests & Quality Gates (tests/ with 7 test modules, tools/panel_driver.mjs)

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (4):** `README.md`, `tests/`, `web/`, `tools/`
- **Root Entries:** 14 items | **Last Commit:** `b294ace 2026-11-09 19:26:42 -0600 Initial import: unified-voice-repo (consolidation 2026-11-09)` | **Dirty Files:** `0`
- **Workflows:** Not observed
- **MCP Files:** Not observed
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line module bodies, runtime execution, and external service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/rig-builds/unified-voice-repo` with 14 top-level entries.
- Build/package manifests observed: Not observed.
- Top-level code/tool directories observed: `web/`, `tools/`.
- Test directories observed: `tests/`.
- MCP 2 (`2026-07-28`) status: `No MCP surface observed`.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- Inferred: P5 voice I/O shell running on /usr/bin/python3 via launchd.

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  Panel[web/panel.js] --> UVoice[uvoice/ CLI & Server]
  Tools[tools/panel_driver.mjs & snap.mjs] --> Panel
  Tests[tests/] --> UVoice
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts)
- **[Low | Direct] Convention Drift — Backup File & Missing Manifest**
  - *Evidence:* web/panel.html.pre-theme-parity.bak remains in web/, and root lacks pyproject.toml.
  - *Impact & Proposed Smallest Safe Correction:* Minor clutter and implicit Python dependency management; proposed: remove .bak and add pyproject.toml.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** None identified
- **Risks:** None identified
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Remove web/panel.html.pre-theme-parity.bak.
  - Run pytest on tests/.

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test directory, and MCP 2 status (`No MCP surface observed`) traces directly to inspected local files at `/Users/rig128gb/rig-builds/unified-voice-repo`; inferences are explicitly labeled `Inferred`.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of this single repository; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
