# Senior Architect Scan-Mode Note — `rig-model-router`

## Synthesis (Reader Priority — Rule 19)
- **Critical/High Findings:** None identified at remote root/README/manifest inspection depth.
- **Primary Recommendation:** Address the top Medium finding first — committed backup files (27 `.bak*` artifacts) tracked in git — by cloning `rig-model-router` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/rig-model-router` (https://github.com/mrodgersjs-web/rig-model-router)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** None — remain in Scan Mode (no Critical/High trigger observed at root/manifest level; clone locally if active modification is planned).
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/rig-model-router.md`

## Architecture Area Classification
- **Frontend:** Not observed
- **Backend:** Observed (language Python)
- **Database:** Not observed
- **AI or background processes:** Observed (`launchd/`)
- **External services:** Not observed
- **Infrastructure:** Observed (`launchd/`, `deploy.sh`)
- **Shared modules:** Not observed
- **Tests and quality gates:** Observed (`tests/`, `verify.py`, `evidence/`/`proof/`)
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `private`, primary language: `Python`, default branch: `main`, last pushed: `2026-11-09T23:59:52Z`).
- Root directory listing (48 entries: `.gitignore`, `DONE.txt`, `INBOX.md`, `INBOX.md.bak-20261027-claimtopo`, `INBOX.md.bak-20261028-gateway`, `JOB.md`, `JOB.md.bak-20261027-relaunch`, `JOB.src.md`, `MODELS.md`, `MODELS.md.bak-20261028-b96`, `MODELS.md.bak-20261028-gateway`, `MODELS.md.bak-20261029-fn3`, `MODELS.md.bak-20261101-48ornith`, `MODELS.md.bak-20261101-dedicate`, `MODELS.md.bak-20261101-noclefvl`, `MODELS.md.bak-20261106-sticky`, `PROGRESS.md`, `UPGRADES.md`, ... (+30 more)).
- README head (not present / empty).

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/rig-model-router` (https://github.com/mrodgersjs-web/rig-model-router), private, default branch `main`, primary language `Python`, last pushed `2026-11-09T23:59:52Z`.
- **Description / Topics (`Direct`):** No GitHub description set. No topics set.
- **Root surface (`Direct`):** 48 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `No MCP surface observed` (no `mcp/` directory or `.mcp.json` at root).

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Inferred from repository name `rig-model-router` and root layout (.gitignore, DONE.txt, INBOX.md, INBOX.md.bak-20261027-claimtopo, INBOX.md.bak-20261028-gateway, JOB.md). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard Python module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

## Findings
### 1. Committed backup files (27 `.bak*` artifacts) tracked in git
- **Dimension:** Project convention drift / Architecture debt
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct GitHub API listing shows committed backup file(s): INBOX.md.bak-20261027-claimtopo, INBOX.md.bak-20261028-gateway, JOB.md.bak-20261027-relaunch, MODELS.md.bak-20261028-b96, MODELS.md.bak-20261028-gateway (+22 more).
- **Impact:** Creates competing copies of specs/scripts in the working tree, increases confusion for agents/humans over which file is authoritative, and duplicates git history.
- **Smallest Safe Correction:** Proposed (requires approval): Remove committed `.bak*` files (relying on git history instead) and add `*.bak-*` to `.gitignore`.

### 2. High root directory sprawl (48 top-level entries)
- **Dimension:** Separation of concerns / Architecture debt
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing contains 48 top-level files and directories, mixing code, operational reports, logs/backups, and configuration.
- **Impact:** Raises cognitive load for onboarding and makes module boundaries and ownership harder to enforce.
- **Smallest Safe Correction:** Proposed (requires approval): After cloning locally, group operational artifacts, evidence snapshots, and scripts into dedicated subdirectories (`docs/`, `artifacts/`, `scripts/`) while keeping entrypoints clear.

### 3. No `README.md` at repository root
- **Dimension:** Architecture debt (handoff readiness)
- **Severity:** `Low`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing (48 entries) contains no `README.md` (entry context is split across `JOB.md`, `DONE.txt`, or unlisted files).
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
