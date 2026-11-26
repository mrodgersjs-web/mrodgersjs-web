# Senior Architect Scan-Mode Note — `Startup-Intelligence-OS`

## Synthesis (Reader Priority — Rule 19)
- **Critical:** Hardcoded Bearer credential committed in `.mcp.json` (Direct — Direct inspection of `.mcp.json` via GitHub API shows a hardcoded `Authorization: Bearer <redacted>` header for `mcp.instantly.ai/mcp` committed in version control.)
- **High:** Non-example environment file(s) committed at repo root (.env.clawswarm, .env.langfuse) (Inferred (Verify first: Yes) — Direct root listing contains `.env.clawswarm`, `.env.langfuse`.)
- **Primary Recommendation:** Address the top Critical finding first — hardcoded bearer credential committed in `.mcp.json` — by cloning `Startup-Intelligence-OS` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/Startup-Intelligence-OS` (https://github.com/mrodgersjs-web/Startup-Intelligence-OS)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** Focus/Full Promotion Triggered (clone locally first): Critical hardcoded Bearer token in `.mcp.json`, 206 root entries, 8 CI workflows, and committed `.env.*` files require local clone + Focus security/boundary audit.
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `MCP surface present — verify protocol after clone`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/Startup-Intelligence-OS.md`

## Architecture Area Classification
- **Frontend:** Observed (primary language HTML, `next.config.ts`)
- **Backend:** Observed (`src/`, `mcp/`)
- **Database:** Observed (Supabase reference in config/README)
- **AI or background processes:** Observed (`mcp/`, `skills/`, `launchd/`, `workflows/`)
- **External services:** Observed (`.mcp.json` external MCP endpoints)
- **Infrastructure:** Observed (8 GitHub Actions workflow(s), `launchd/`, `.dockerignore`, `Makefile`)
- **Shared modules:** Observed (`packages/`, `vendor/`, `scripts/`)
- **Tests and quality gates:** Observed (`tests/`, `evidence/`/`proof/`, CI/lattice workflows)
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `private`, primary language: `HTML`, default branch: `main`, last pushed: `2026-10-11T03:22:42Z`).
- Root directory listing (206 entries: `.agents/`, `.aider.conf.yml`, `.aiderignore`, `.archon/`, `.claire/`, `.claude/`, `.cursor/`, `.dockerignore`, `.env.clawswarm`, `.env.langfuse`, `.env.production.example`, `.github/`, `.gitignore`, `.gitmodules`, `.gitnexusignore`, `.hermes/`, `.mcp.json`, `.memory-stack-backups/`, ... (+188 more)).
- README head (1200 chars inspected).
- Read-only `gh api` listing of `.github/workflows` (8 workflow(s): `deploy-rig-website.yml`, `deploy-sios.yml`, `full-ci.yml`, `gitnexus.yml`, `memory-tools.yml`, `nightly-canary.yml`, `prompt-tests.yml`, `rig-lattice.yml`).
- Read-only `gh api` inspection of MCP files: `mcp/server.py`.
- Read-only `gh api` inspection of manifests: `.mcp.json`.

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/Startup-Intelligence-OS` (https://github.com/mrodgersjs-web/Startup-Intelligence-OS), private, default branch `main`, primary language `HTML`, last pushed `2026-10-11T03:22:42Z`.
- **Description / Topics (`Direct`):** No GitHub description set. No topics set.
- **Root surface (`Direct`):** 206 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `MCP surface present — verify protocol after clone` (inspected `mcp/server.py`).
- **CI / Automation workflows (`Direct`):** 8 workflow file(s) in `.github/workflows/`.
- **README opening (`Direct`):** # Startup Intelligence OS (Decision & Capability OS) — This repository is the **Decision & Capability OS** for Apex Ventures.

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Inferred from repository name `Startup-Intelligence-OS` and root layout (.agents/, .aider.conf.yml, .aiderignore, .archon/, .claire/, .claude/). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard HTML module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

## Findings
### 1. Hardcoded Bearer credential committed in `.mcp.json`
- **Dimension:** Security / Boundary violation
- **Severity:** `Critical`
- **Confidence:** `Direct`
- **Evidence:** Direct inspection of `.mcp.json` via GitHub API shows a hardcoded `Authorization: Bearer <redacted>` header for `mcp.instantly.ai/mcp` committed in version control.
- **Impact:** Exposes a live third-party API credential to anyone with repo read access and breaks secret-management boundaries.
- **Smallest Safe Correction:** Proposed (requires approval): Revoke/rotate the exposed Instantly token, replace the literal header in `.mcp.json` with an environment/keychain variable reference, and scrub or rotate credentials per security policy.

### 2. Non-example environment file(s) committed at repo root (.env.clawswarm, .env.langfuse)
- **Dimension:** Security / Architecture debt
- **Severity:** `High`
- **Confidence:** `Inferred (Verify first: Yes)`
- **Evidence:** Direct root listing contains `.env.clawswarm`, `.env.langfuse`.
- **Impact:** Risks leaking environment-specific secrets or endpoints and couples repository state to machine-local configuration.
- **Smallest Safe Correction:** Proposed (requires approval): Clone locally to audit contents for secrets, move templates to `.env.example`, and add live `.env*` files to `.gitignore`.

### 3. Hardcoded local machine path and unpinned MCP SDK version in `mcp/server.py`
- **Dimension:** Architecture debt / Environment coupling
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct inspection of `mcp/server.py` shows `RIG_LOOP = Path.home() / "Developer/rig-capabilities/bin/rig-loop"` and `from mcp.server.fastmcp import FastMCP` without a declared MCP 2 (`2026-07-28`) version pin.
- **Impact:** Couples the MCP server to a single workstation directory layout and leaves MCP 2 protocol compliance dependent on ambient Python environment packages.
- **Smallest Safe Correction:** Proposed (requires approval): Resolve `RIG_LOOP` via an environment variable with PATH fallback, pin the `mcp` dependency in a manifest, and verify MCP 2 (`2026-07-28`) compliance after cloning.

### 4. Committed backup files (1 `.bak*` artifact) tracked in git
- **Dimension:** Project convention drift / Architecture debt
- **Severity:** `Low`
- **Confidence:** `Direct`
- **Evidence:** Direct GitHub API listing shows committed backup file(s): claw_config.yaml.clawswarm.bak.
- **Impact:** Creates competing copies of specs/scripts in the working tree, increases confusion for agents/humans over which file is authoritative, and duplicates git history.
- **Smallest Safe Correction:** Proposed (requires approval): Remove committed `.bak*` files (relying on git history instead) and add `*.bak-*` to `.gitignore`.

### 5. High root directory sprawl (206 top-level entries)
- **Dimension:** Separation of concerns / Architecture debt
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing contains 206 top-level files and directories, mixing code, operational reports, logs/backups, and configuration.
- **Impact:** Raises cognitive load for onboarding and makes module boundaries and ownership harder to enforce.
- **Smallest Safe Correction:** Proposed (requires approval): After cloning locally, group operational artifacts, evidence snapshots, and scripts into dedicated subdirectories (`docs/`, `artifacts/`, `scripts/`) while keeping entrypoints clear.

## Open Questions
- Is this repository actively deployed or superseded by a newer consolidated studio/monorepo?
- Which exact `mcp` SDK version and protocol version (`2026-07-28` vs v1) are locked in the full dependency graph once cloned locally?
- Are any credentials or runtime data files flagged above still active in production or third-party services?

## Risks
- **Inspection blind spot:** Because this repository was not cloned locally, internal coupling, dead paths, secret sprawl inside subdirectories, and test pass rates remain unobserved.
- **Active defect risk:** 2 Critical/High finding(s) observed at root/manifest level could impact security, data hygiene, or MCP 2 compatibility if left unaddressed.

## Safe Next Actions
- **Proposed (Gate-D approval required):** Clone the repository locally and remediate the Critical/High finding(s) listed above using the smallest safe correction.
- **Read-only next step:** Clone locally and verify `mcp` SDK lockfile versions and `initialize` protocol version (`2026-07-28`).
- **Read-only next step:** Keep this note as the Scan-Mode baseline; promote to Focus or Full Mode only after cloning locally and confirming an active work trigger.

## Step-8 Validation Gate Answers
1. **Claim traceability:** Yes. Every fact and finding traces directly to `shard_remote_4.json` metadata, root listings, README heads, or targeted read-only `gh api` GET responses (`Direct`), with non-inspected details explicitly labeled `Inferred`, `Assumed`, or `Not observed`.
2. **Scope alignment:** Yes. Output remains strictly within Scan Mode (one compact architecture note, read-only against GitHub) and explicitly notes that cloning locally is required before any Focus/Full promotion.
3. **Handoff readiness:** Yes. Unknowns, inspection limitations, MCP 2 status, and Gate-D-compliant safe next actions are explicitly documented with no blank sections.
