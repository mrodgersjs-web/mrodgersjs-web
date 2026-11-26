# Senior Architect Scan-Mode Note — `gtm-open-outreach`

## Synthesis (Reader Priority — Rule 19)
- **High:** Runtime SQLite database files and backups committed at repo root (app.db.bak-20261028T135046Z, jobsflow.db.bak-20261028T135046Z, openoutreach.sqlite3, send-refusal.sqlite3) (Direct — Direct root listing includes `app.db.bak-20261028T135046Z`, `jobsflow.db.bak-20261028T135046Z`, `openoutreach.sqlite3`, `send-refusal.sqlite3` alongside 108 total root entries.)
- **Primary Recommendation:** Address the top High finding first — runtime sqlite database files and backups committed at repo root (app.db.bak-20261028t135046z, jobsflow.db.bak-20261028t135046z, openoutreach.sqlite3, send-refusal.sqlite3) — by cloning `gtm-open-outreach` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/gtm-open-outreach` (https://github.com/mrodgersjs-web/gtm-open-outreach)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** Focus Promotion Triggered (clone locally first): 4 committed SQLite DB/backup files and 108 root entries require local clone + Focus data/boundary cleanup pass.
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `No MCP surface observed`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/gtm-open-outreach.md`

## Architecture Area Classification
- **Frontend:** Not observed
- **Backend:** Observed (language Python)
- **Database:** Observed (committed DB files (app.db.bak-20261028T135046Z, jobsflow.db.bak-20261028T135046Z, openoutreach.sqlite3, send-refusal.sqlite3))
- **AI or background processes:** Not observed
- **External services:** Observed (outreach/Apollo retirement references)
- **Infrastructure:** Not observed
- **Shared modules:** Observed (`vendor/`)
- **Tests and quality gates:** Observed (`verify.py`)
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `private`, primary language: `Python`, default branch: `main`, last pushed: `2026-11-09T23:26:52Z`).
- Root directory listing (108 entries: `.gitignore`, `APOLLO-RETIRE.md`, `DONE.txt`, `FROM-CLONE-OWNER-y6WK.md`, `JOB.md`, `PIN.txt`, `PROGRESS.md`, `app.db.bak-20261028T135046Z`, `backups.json`, `capture-ui.cjs`, `clone-dash-before.json`, `consolidated_review_report.md`, `dashboard-dark.json`, `dashboard-dark.png`, `dashboard-light.json`, `dashboard-light.png`, `egm-glm-review.md`, `egm-qwen-review.md`, ... (+90 more)).
- README head (not present / empty).

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/gtm-open-outreach` (https://github.com/mrodgersjs-web/gtm-open-outreach), private, default branch `main`, primary language `Python`, last pushed `2026-11-09T23:26:52Z`.
- **Description / Topics (`Direct`):** No GitHub description set. No topics set.
- **Root surface (`Direct`):** 108 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `No MCP surface observed` (no `mcp/` directory or `.mcp.json` at root).

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Inferred from repository name `gtm-open-outreach` and root layout (.gitignore, APOLLO-RETIRE.md, DONE.txt, FROM-CLONE-OWNER-y6WK.md, JOB.md, PIN.txt). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard Python module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

## Findings
### 1. Runtime SQLite database files and backups committed at repo root (app.db.bak-20261028T135046Z, jobsflow.db.bak-20261028T135046Z, openoutreach.sqlite3, send-refusal.sqlite3)
- **Dimension:** Separation of concerns / Architecture debt
- **Severity:** `High`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing includes `app.db.bak-20261028T135046Z`, `jobsflow.db.bak-20261028T135046Z`, `openoutreach.sqlite3`, `send-refusal.sqlite3` alongside 108 total root entries.
- **Impact:** Mixes mutable operational data (potentially including outreach/contact PII) with source control, causes binary merge conflicts, and bloats repository history.
- **Smallest Safe Correction:** Proposed (requires approval): Remove runtime `.sqlite3` / `.db.bak-*` files from git tracking, add them to `.gitignore`, and store operational state outside the source tree.

### 2. Committed backup files (2 `.bak*` artifacts) tracked in git
- **Dimension:** Project convention drift / Architecture debt
- **Severity:** `Low`
- **Confidence:** `Direct`
- **Evidence:** Direct GitHub API listing shows committed backup file(s): app.db.bak-20261028T135046Z, jobsflow.db.bak-20261028T135046Z.
- **Impact:** Creates competing copies of specs/scripts in the working tree, increases confusion for agents/humans over which file is authoritative, and duplicates git history.
- **Smallest Safe Correction:** Proposed (requires approval): Remove committed `.bak*` files (relying on git history instead) and add `*.bak-*` to `.gitignore`.

### 3. High root directory sprawl (108 top-level entries)
- **Dimension:** Separation of concerns / Architecture debt
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing contains 108 top-level files and directories, mixing code, operational reports, logs/backups, and configuration.
- **Impact:** Raises cognitive load for onboarding and makes module boundaries and ownership harder to enforce.
- **Smallest Safe Correction:** Proposed (requires approval): After cloning locally, group operational artifacts, evidence snapshots, and scripts into dedicated subdirectories (`docs/`, `artifacts/`, `scripts/`) while keeping entrypoints clear.

### 4. No `README.md` at repository root
- **Dimension:** Architecture debt (handoff readiness)
- **Severity:** `Low`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing (108 entries) contains no `README.md` (entry context is split across `JOB.md`, `DONE.txt`, or unlisted files).
- **Impact:** Slows human and AI-agent orientation when inspecting or cloning the repository.
- **Smallest Safe Correction:** Proposed (requires approval): Add a concise root `README.md` documenting purpose, entry points, and verification command.

## Open Questions
- Is this repository actively deployed or superseded by a newer consolidated studio/monorepo?
- Are any credentials or runtime data files flagged above still active in production or third-party services?

## Risks
- **Inspection blind spot:** Because this repository was not cloned locally, internal coupling, dead paths, secret sprawl inside subdirectories, and test pass rates remain unobserved.
- **Active defect risk:** 1 Critical/High finding(s) observed at root/manifest level could impact security, data hygiene, or MCP 2 compatibility if left unaddressed.

## Safe Next Actions
- **Proposed (Gate-D approval required):** Clone the repository locally and remediate the Critical/High finding(s) listed above using the smallest safe correction.
- **Read-only next step:** Keep this note as the Scan-Mode baseline; promote to Focus or Full Mode only after cloning locally and confirming an active work trigger.

## Step-8 Validation Gate Answers
1. **Claim traceability:** Yes. Every fact and finding traces directly to `shard_remote_4.json` metadata, root listings, README heads, or targeted read-only `gh api` GET responses (`Direct`), with non-inspected details explicitly labeled `Inferred`, `Assumed`, or `Not observed`.
2. **Scope alignment:** Yes. Output remains strictly within Scan Mode (one compact architecture note, read-only against GitHub) and explicitly notes that cloning locally is required before any Focus/Full promotion.
3. **Handoff readiness:** Yes. Unknowns, inspection limitations, MCP 2 status, and Gate-D-compliant safe next actions are explicitly documented with no blank sections.
