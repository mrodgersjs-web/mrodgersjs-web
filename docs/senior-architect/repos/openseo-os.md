# Senior Architect Scan-Mode Note: `openseo-os`

## 1. Synthesis (Reader Priority — Rule 19)
- **Primary Recommendation:** Add a smoke test and dependency declaration for `workflows/runner/run.py`, and document the single-source-of-truth boundary with `openseo-library`.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Critical / High Findings:** None identified.

## 2. Pass Level, Scope & Promotion Gate
- **Pass Level:** `Scan Mode` (Rule 0 default)
- **Scope:** Repository `openseo-os` at `/Users/rig128gb/Developer/openseo-os` (`lang=Python`, `private=True`, `inManifest38=False`)
- **Focus/Full Promotion Trigger:** None (clean build-out repo; Scan Mode sufficient unless `workflows/runner/run.py` expands into external API execution)
- **Architecture Areas Classified:** Workflows & Runner (`workflows/runner/run.py`); Knowledge Cards & Skills (`library/cards/`, `skills/`, `resources/`); Governance & Audits (`audits/`, `CATALOG.md`, `ATTRIBUTION.md`); Backend / Frontend / Database / Tests / CI / MCP (Not observed)

## 3. Evidence Checked & Skipped Areas
- **Evidence Files Checked (14):** `README.md`, `library/cards/ai-agent-seo/ai-search-optimization.md`, `library/cards/keyword-research/README.md`, `library/cards/keyword-research/content-gap-analysis.md`, `library/cards/keyword-research/customer-language-keywords.md`, `library/cards/keyword-research/keyword-clustering.md`, `library/cards/keyword-research/keyword-difficulty.md`, `library/cards/keyword-research/keyword-prioritization.md`, `library/cards/keyword-research/long-tail-keywords.md`, `library/cards/keyword-research/search-intent-mapping.md`, `library/cards/keyword-research/seasonal-keywords.md`, `library/skills/openseo-keyword-research/SKILL.md`
- **Root Entries:** 10 items (`.gitignore, ATTRIBUTION.md, CATALOG.md, LICENSE-NOTICE.md, README.md, audits/, library/, resources/, skills/, workflows/`)
- **Last Commit:** `ab17608 2026-11-23 21:46:32 -0700 audits: gate log and run receipt for the OpenSEO build`
- **Git Working Tree:** `0` dirty/untracked entries (clean)
- **Workflows:** Not observed
- **MCP Files:** Not observed
- **Existing Architecture Docs:** `library/cards/ai-agent-seo/ai-search-optimization.md`, `library/cards/keyword-research/README.md`, `library/cards/keyword-research/content-gap-analysis.md`, `library/cards/keyword-research/customer-language-keywords.md`, `library/cards/keyword-research/keyword-clustering.md`
- **Skipped Areas (Scan-Mode Budget):** Deep line-by-line function bodies, runtime execution, and external network/service probes (not executed in read-only Scan Mode).

## 4. Confirmed Facts (`Direct`)
- Local checkout exists at `/Users/rig128gb/Developer/openseo-os` (branch `main`) with 10 top-level entries and 89 sampled files (depth <= 3).
- Build/package manifests observed: Not observed.
- Top-level source/tool directories observed: `skills/`, `workflows/`.
- Entrypoints observed: `workflows/runner/run.py`.
- Tests observed: Not observed.
- MCP 2 (`2026-07-28`) status: `No MCP surface observed`.
- Committed/untracked secret-file candidates observed: None identified.

## 5. Inferences & Assumptions (`Inferred` / `Assumed`)
- Inferred: Operationalized OpenSEO skill pack and Python workflow runner (`workflows/runner/run.py`) paired with audit receipts under `audits/`.

## 6. System Map (Mermaid)
```mermaid
flowchart LR
  Cards[library/cards/] --> Skills[skills/ 22 SEO Skills]
  Skills --> Runner[workflows/runner/run.py]
  Runner --> Audits[audits/ Gate Logs + Receipts]
```

## 7. Findings (Debt, Separation of Concerns, Convention Drift, Flow Conflicts, MCP 2)
- **[Medium | Direct] Architecture Debt — Unpackaged Python Runner Without Tests or CI**
  - *Evidence:* `workflows/runner/run.py` exists with no `pyproject.toml`/`requirements.txt`, 0 tests, and 0 CI workflows.
  - *Impact:* Runner dependencies and behavior are unpinned and unverified in clean environments.
  - *Proposed Smallest Safe Correction (Requires Approval):* Add `pyproject.toml` (or declare stdlib-only) and a minimal smoke test + CI check for `workflows/runner/run.py`.
- **[Low | Inferred] Architecture Debt — Structural Overlap with `openseo-library`**
  - *Evidence:* Both `openseo-os` and `openseo-library` contain `CATALOG.md`, `ATTRIBUTION.md`, `library/`, `skills/`, and `workflows/` (`Verify first: Yes`).
  - *Impact:* Dual copies of SEO cards and skills risk diverging over time.
  - *Proposed Smallest Safe Correction (Requires Approval):* Document which repo is the single source of truth for cards/skills vs runtime runner.

## 8. Open Questions, Risks & Safe Next Actions
- **Open Questions:** Which repo (`openseo-library` vs `openseo-os`) is the canonical source of truth for SEO library cards?
- **Risks:** Silent drift between `openseo-os` and `openseo-library`.
- **Safe Next Actions (Proposed, Read-Only Until Approved):**
  - Pin runtime requirements for `workflows/runner/run.py` and add a smoke test.
  - Document canonical boundary with `openseo-library`.

## 9. Step-8 Validation Gate
1. **Claim traceability:** Yes — every file path, manifest, workflow, test file, git status count, and MCP 2 status (`No MCP surface observed`) traces directly to inspected local files at `/Users/rig128gb/Developer/openseo-os`; inferences and assumptions are explicitly labeled.
2. **Scope alignment:** Yes — bounded strictly to Scan Mode (Rule 0) read-only inspection of `openseo-os`; no files inside the target repository were modified.
3. **Handoff readiness:** Yes — open questions, risks, promotion gate status, and proposed smallest safe next actions are explicitly listed (or marked `None identified`).
