# Senior Architect Scan-Mode Note: `rig-design-studio-corpus`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Add a `package.json` for `build.mjs`/`offer.mjs`, move `*.log` to `.gitignore`, and commit the 2 dirty `sites/blueorbit-ai/` files.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Critical / High Findings:** None identified.

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `rig-design-studio-corpus` at `/Users/rig128gb/Developer/rig-design-studio-corpus` (`lang=JavaScript`, `private=True`, `inManifest38=False`)
- **Focus/Full Promotion Trigger:** None (bounded design-reference corpus and capture scripts; Scan Mode sufficient)
- **Architecture Areas Classified:** Capture Scripts (`build.mjs`, `offer.mjs`); Corpus Data (`sites/` 21+ captured sites, `competitors/lane-1..4/blueprint.md`); Documentation (`INDEX.md`, `PATTERNS.md`, `README.md`); Backend / Frontend / Database / Tests / CI / MCP (Not observed)

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (7):** `README.md`, `competitors/lane-1-ai-consulting/blueprint.md`, `competitors/lane-2-ai-automation-intake/blueprint.md`, `competitors/lane-3-trades-field-answering/blueprint.md`, `competitors/lane-4-legal-cpa-compliance-gov/blueprint.md`, `competitors/lane-5-webforge-apps-devtools/blueprint.md`, `competitors/lane-6-products-consumer-b2b/blueprint.md`
- **Root Entries:** 10 items (`.gitignore, INDEX.md, PATTERNS.md, README.md, build.log, build.mjs, competitors/, offer.log, offer.mjs, sites/`)
- **Last Commit:** `8027603 2026-11-24 17:15:58 -0700 competitors: 60 OpenSEO-ranked competitor captures across 6 RIG lanes (hero, full-page, mobile, tokens, blueprints)`
- **Git Working Tree:** `2` dirty/untracked entries (`M sites/blueorbit-ai/README.md`, `M sites/blueorbit-ai/offerings.md`)
- **Workflows:** Not observed
- **MCP Files:** Not observed
- **Existing Architecture Docs:** `competitors/lane-1-ai-consulting/blueprint.md`, `competitors/lane-2-ai-automation-intake/blueprint.md`, `competitors/lane-3-trades-field-answering/blueprint.md`, `competitors/lane-4-legal-cpa-compliance-gov/blueprint.md`, `competitors/lane-5-webforge-apps-devtools/blueprint.md`
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line function bodies, runtime execution, and external network/service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/Developer/rig-design-studio-corpus` (branch `main`) with 10 top-level entries and 213 sampled files (depth <= 3).
- Build/package manifests observed: Not observed.
- Top-level source/tool directories observed: Not observed.
- Entrypoints observed: Not observed.
- Tests observed: Not observed.
- MCP 2 (`2026-07-28`) status: `No MCP surface observed`.
- Committed/untracked secret-file candidates observed: None identified.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- Inferred: Node ESM scripts (`build.mjs`, `offer.mjs`) capture screenshots/tokens/offerings into `sites/` and `competitors/` and update `INDEX.md`/`PATTERNS.md`.

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  Build[build.mjs + offer.mjs] --> Sites[sites/ Captured Peers]
  Build --> Competitors[competitors/ 4 Lanes]
  Sites --> Index[INDEX.md + PATTERNS.md]
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts, MCP 2)
- **[Medium | Direct] Architecture Debt — Runtime Logs & Unpackaged Scripts at Root**
  - *Evidence:* `build.log` and `offer.log` sit at repo root alongside `build.mjs`/`offer.mjs` with no `package.json` or tests.
  - *Impact:* Script dependencies are undeclared and log artifacts pollute the repository root.
  - *Proposed Smallest Safe Correction (Requires Approval):* Add a minimal `package.json` declaring script dependencies and `.gitignore` `*.log` files.
- **[Low | Direct] Convention Drift — Uncommitted Capture Edits**
  - *Evidence:* 2 dirty files: `M sites/blueorbit-ai/README.md`, `M sites/blueorbit-ai/offerings.md`.
  - *Impact:* Partial site capture updates are uncommitted.
  - *Proposed Smallest Safe Correction (Requires Approval):* Review and commit the 2 modified `sites/blueorbit-ai/` files.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** None identified
- **Risks:** Re-running `build.mjs` on another machine may fail without a `package.json` lockfile.
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Add `package.json`, ignore `*.log`, and commit the 2 dirty `blueorbit-ai` files.

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test file, git status count, and MCP 2 status (`No MCP surface observed`) traces directly to inspected local files at `/Users/rig128gb/Developer/rig-design-studio-corpus`; inferences and assumptions are explicitly labeled.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of `rig-design-studio-corpus`; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, promotion gate status, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
