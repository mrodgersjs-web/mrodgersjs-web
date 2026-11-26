# Senior Architect Scan-Mode Note: `rig-skills`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Add a lightweight skill-manifest/frontmatter lint check in CI and triage the 15 uncommitted local changes.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Critical / High Findings:** None identified.

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `rig-skills` at `/Users/rig128gb/Developer/rig-skills` (`lang=Python`, `private=True`)
- **Focus/Full Promotion Trigger:** None (pure markdown/asset skill catalog; 15 dirty files to triage)
- **Architecture Areas Classified:** Shared Modules/Knowledge (doctrine/, engineering/, engines/, fleet/, knowledge/, platform/, pmm-*, studios/, staged/), Assets (assets/), Tests & Quality Gates (Not observed)

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (1):** `README.md`
- **Root Entries:** 19 items | **Last Commit:** `9865117 2026-10-05 20:08:48 -0600 staged(council+forge): 7 corpus-derived skills from the 2026-10-05 framework notebooks` | **Dirty Files:** `15`
- **Workflows:** Not observed
- **MCP Files:** Not observed
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line module bodies, runtime execution, and external service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/Developer/rig-skills` with 19 top-level entries.
- Build/package manifests observed: Not observed.
- Top-level code/tool directories observed: Not observed.
- Test directories observed: Not observed.
- MCP 2 (`2026-07-28`) status: `No MCP surface observed`.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- Inferred: Acts as an upstream skill/doctrine content repository synced into Aside/OMP harnesses.

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts)
- **[Medium | Direct] Architecture Debt — No Validation Gate or CI**
  - *Evidence:* Repository contains 16 topic/skill directories and 15 dirty files with no pyproject.toml, package.json, or .github/workflows/ validation.
  - *Impact & Proposed Smallest Safe Correction:* Broken frontmatter or duplicate skill names go undetected until runtime; proposed: add a CI markdown/frontmatter validator.
- **[Low | Direct] Convention Drift — Staged vs. Active Directories**
  - *Evidence:* Root has both staged/ and domain directories (doctrine/, engineering/, pmm-*) with no documented promotion contract in root.
  - *Impact & Proposed Smallest Safe Correction:* Unclear lifecycle for staged skills; proposed: document promotion rules in README.md.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** How are skills in staged/ promoted to active directories?
- **Risks:** 15 uncommitted files risk diverging from downstream skill consumers.
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Triage the 15 dirty files with git status.
  - Add a minimal CI frontmatter/link check.

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test directory, and MCP 2 status (`No MCP surface observed`) traces directly to inspected local files at `/Users/rig128gb/Developer/rig-skills`; inferences are explicitly labeled `Inferred`.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of this single repository; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
