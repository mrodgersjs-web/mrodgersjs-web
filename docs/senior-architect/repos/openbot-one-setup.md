# Senior Architect Scan-Mode Note — `openbot-one-setup`

## Synthesis (Reader Priority — Rule 19)
- **Critical/High Findings:** None identified at remote root/README/manifest inspection depth.
- **Primary Recommendation:** Address the top Medium finding first — committed backup files (6 `.bak*` artifacts) tracked in git — by cloning `openbot-one-setup` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/openbot-one-setup` (https://github.com/mrodgersjs-web/openbot-one-setup)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** None — remain in Scan Mode (no Critical/High trigger observed at root/manifest level; clone locally if active modification is planned).
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/openbot-one-setup.md`

## Architecture Area Classification
- **Frontend:** Not observed
- **Backend:** Observed (language Python)
- **Database:** Not observed
- **AI or background processes:** Not observed
- **External services:** Not observed
- **Infrastructure:** Not observed
- **Shared modules:** Not observed
- **Tests and quality gates:** Observed (`verify.py`, `evidence/`/`proof/`)
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `private`, primary language: `Python`, default branch: `main`, last pushed: `2026-11-09T23:54:52Z`).
- Root directory listing (35 entries: `.gitignore`, `CUTOVER-DESK-NOTES.md`, `CUTOVER/`, `DEDUPE.json`, `DONE.txt`, `GOOGLE-SSO.md`, `INBOX.md`, `INBOX.md.bak-20261027-claimtopo`, `JOB.md`, `JOB.md.bak-20261027-relaunch`, `JOB.src.md`, `LINKED-QUEUE.md`, `OPENBOT-AUDIT.md`, `PARALLEL-RUN.md`, `PARITY-LOG.md`, `PROGRESS.md`, `READ-ONLY-CUTOVER.md`, `ROOM-MAP.json`, ... (+17 more)).
- README head (not present / empty).

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/openbot-one-setup` (https://github.com/mrodgersjs-web/openbot-one-setup), private, default branch `main`, primary language `Python`, last pushed `2026-11-09T23:54:52Z`.
- **Description / Topics (`Direct`):** No GitHub description set. No topics set.
- **Root surface (`Direct`):** 35 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `No MCP surface observed` (no `mcp/` directory or `.mcp.json` at root).

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Inferred from repository name `openbot-one-setup` and root layout (.gitignore, CUTOVER-DESK-NOTES.md, CUTOVER/, DEDUPE.json, DONE.txt, GOOGLE-SSO.md). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard Python module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

## Findings
### 1. Committed backup files (6 `.bak*` artifacts) tracked in git
- **Dimension:** Project convention drift / Architecture debt
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct GitHub API listing shows committed backup file(s): INBOX.md.bak-20261027-claimtopo, JOB.md.bak-20261027-relaunch, bulk_import.py.bak-20261028-shim, import_cutover.py.bak-20261028-persona, import_cutover.py.bak-20261028-shim (+1 more).
- **Impact:** Creates competing copies of specs/scripts in the working tree, increases confusion for agents/humans over which file is authoritative, and duplicates git history.
- **Smallest Safe Correction:** Proposed (requires approval): Remove committed `.bak*` files (relying on git history instead) and add `*.bak-*` to `.gitignore`.

### 2. No `README.md` at repository root
- **Dimension:** Architecture debt (handoff readiness)
- **Severity:** `Low`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing (35 entries) contains no `README.md` (entry context is split across `JOB.md`, `DONE.txt`, or unlisted files).
- **Impact:** Slows human and AI-agent orientation when inspecting or cloning the repository.
- **Smallest Safe Correction:** Proposed (requires approval): Add a concise root `README.md` documenting purpose, entry points, and verification command.

## Open Questions
- Is this repository actively deployed or superseded by a newer consolidated studio/monorepo?

## Risks
- **Inspection blind spot:** Because this repository was not cloned locally, internal coupling, dead paths, secret sprawl inside subdirectories, and test pass rates remain unobserved.

## Safe Next Actions
- **Read-only next step:** Keep this note as the Scan-Mode baseline; promote to Focus or Full Mode only after cloning locally and confirming an active work trigger.

## Step-8 Validation Gate Answers
1. **Claim traceability:** Yes. Every fact and finding traces directly to `shard_remote_4.json` metadata, root listings, README heads, or targeted read-only `gh api` GET responses (`Direct`), with non-inspected details explicitly labeled `Inferred`, `Assumed`, or `Not observed`.
2. **Scope alignment:** Yes. Output remains strictly within Scan Mode (one compact architecture note, read-only against GitHub) and explicitly notes that cloning locally is required before any Focus/Full promotion.
3. **Handoff readiness:** Yes. Unknowns, inspection limitations, MCP 2 status, and Gate-D-compliant safe next actions are explicitly documented with no blank sections.
