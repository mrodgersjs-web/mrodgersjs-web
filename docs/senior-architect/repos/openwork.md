# Senior Architect Scan-Mode Note — `openwork`

## Synthesis (Reader Priority — Rule 19)
- **High:** Non-example environment file(s) committed at repo root (.env.dev) (Inferred (Verify first: Yes) — Direct root listing contains `.env.dev`.)
- **Primary Recommendation:** Address the top High finding first — non-example environment file(s) committed at repo root (.env.dev) — by cloning `openwork` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/openwork` (https://github.com/mrodgersjs-web/openwork)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** Focus Promotion Triggered (clone locally first): 24 CI workflows, 45 root entries, committed `.env.dev`, and MCP surface require local clone before making architecture changes.
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `MCP surface present — verify protocol after clone`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/openwork.md`

## Architecture Area Classification
- **Frontend:** Observed (UI surface signals in root/README)
- **Backend:** Observed (language TypeScript, `mcp/`)
- **Database:** Not observed
- **AI or background processes:** Observed (`mcp/`)
- **External services:** Observed (`.infisical.json`)
- **Infrastructure:** Observed (24 GitHub Actions workflow(s), `.dockerignore`)
- **Shared modules:** Observed (`packages/`, `scripts/`)
- **Tests and quality gates:** Observed (CI/lattice workflows)
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `private`, primary language: `TypeScript`, default branch: `openwork-power-v1`, last pushed: `2026-10-10T23:41:37Z`).
- Root directory listing (45 entries: `.devcontainer/`, `.dockerignore`, `.env.dev`, `.github/`, `.gitignore`, `.infisical.json`, `.nvmrc`, `.opencode/`, `.rig/`, `.vercelignore`, `.warden/`, `AGENTS.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `LICENSE`, `README.md`, `SECURITY.md`, `STATS.md`, ... (+27 more)).
- README head (1200 chars inspected).
- Read-only `gh api` listing of `.github/workflows` (24 workflow(s): `alpha-macos-aarch64.yml`, `aur-validate.yml`, `build-electron-desktop.yml`, `changelog.yml`, `ci-enterprise-mcp-mock.yml`, `ci-i18n.yml`, `ci-no-new-eval-flows.yml`, `ci-openwork-ui-mcp.yml`, `ci-tests.yml`, `daytona-eval-image.yml`, ... (+14 more)).
- Read-only `gh api` inspection of MCP files: `mcp/server.py`.
- Read-only `gh api` inspection of manifests: `package.json`.

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/openwork` (https://github.com/mrodgersjs-web/openwork), private, default branch `openwork-power-v1`, primary language `TypeScript`, last pushed `2026-10-10T23:41:37Z`.
- **Description / Topics (`Direct`):** "Operator workstation shell — evaluated/adapted OpenWork (upstream: different-ai/openwork-workspace, MIT/Fair-Source) for RIG workflow review." Topics: `agent-governance`, `ai-agents`, `evals`, `forward-deployed-engineer`, `llm`, `mlops`, `proof-gates`.
- **Root surface (`Direct`):** 45 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `MCP surface present — verify protocol after clone` (inspected `mcp/server.py`).
- **CI / Automation workflows (`Direct`):** 24 workflow file(s) in `.github/workflows/`.
- **README opening (`Direct`):** # openwork — > Power-user agent workstation — desktop shell + MCP capability bridge for serious operator sessions.

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Aligned with stated purpose ("Operator workstation shell — evaluated/adapted OpenWork (upstream: different-ai/openwork-workspace, MIT/Fair-Source) for RIG workflow review"). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard TypeScript module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

## Findings
### 1. Non-example environment file(s) committed at repo root (.env.dev)
- **Dimension:** Security / Architecture debt
- **Severity:** `High`
- **Confidence:** `Inferred (Verify first: Yes)`
- **Evidence:** Direct root listing contains `.env.dev`.
- **Impact:** Risks leaking environment-specific secrets or endpoints and couples repository state to machine-local configuration.
- **Smallest Safe Correction:** Proposed (requires approval): Clone locally to audit contents for secrets, move templates to `.env.example`, and add live `.env*` files to `.gitignore`.

### 2. Hardcoded local machine path and unpinned MCP SDK version in `mcp/server.py`
- **Dimension:** Architecture debt / Environment coupling
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct inspection of `mcp/server.py` shows `RIG_LOOP = Path.home() / "Developer/rig-capabilities/bin/rig-loop"` and `from mcp.server.fastmcp import FastMCP` without a declared MCP 2 (`2026-07-28`) version pin.
- **Impact:** Couples the MCP server to a single workstation directory layout and leaves MCP 2 protocol compliance dependent on ambient Python environment packages.
- **Smallest Safe Correction:** Proposed (requires approval): Resolve `RIG_LOOP` via an environment variable with PATH fallback, pin the `mcp` dependency in a manifest, and verify MCP 2 (`2026-07-28`) compliance after cloning.

### 3. High root directory sprawl (45 top-level entries)
- **Dimension:** Separation of concerns / Architecture debt
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct root listing contains 45 top-level files and directories, mixing code, operational reports, logs/backups, and configuration.
- **Impact:** Raises cognitive load for onboarding and makes module boundaries and ownership harder to enforce.
- **Smallest Safe Correction:** Proposed (requires approval): After cloning locally, group operational artifacts, evidence snapshots, and scripts into dedicated subdirectories (`docs/`, `artifacts/`, `scripts/`) while keeping entrypoints clear.

## Open Questions
- Is this repository actively deployed or superseded by a newer consolidated studio/monorepo?
- Which exact `mcp` SDK version and protocol version (`2026-07-28` vs v1) are locked in the full dependency graph once cloned locally?
- Are any credentials or runtime data files flagged above still active in production or third-party services?

## Risks
- **Inspection blind spot:** Because this repository was not cloned locally, internal coupling, dead paths, secret sprawl inside subdirectories, and test pass rates remain unobserved.
- **Active defect risk:** 1 Critical/High finding(s) observed at root/manifest level could impact security, data hygiene, or MCP 2 compatibility if left unaddressed.

## Safe Next Actions
- **Proposed (Gate-D approval required):** Clone the repository locally and remediate the Critical/High finding(s) listed above using the smallest safe correction.
- **Read-only next step:** Clone locally and verify `mcp` SDK lockfile versions and `initialize` protocol version (`2026-07-28`).
- **Read-only next step:** Keep this note as the Scan-Mode baseline; promote to Focus or Full Mode only after cloning locally and confirming an active work trigger.

## Step-8 Validation Gate Answers
1. **Claim traceability:** Yes. Every fact and finding traces directly to `shard_remote_4.json` metadata, root listings, README heads, or targeted read-only `gh api` GET responses (`Direct`), with non-inspected details explicitly labeled `Inferred`, `Assumed`, or `Not observed`.
2. **Scope alignment:** Yes. Output remains strictly within Scan Mode (one compact architecture note, read-only against GitHub) and explicitly notes that cloning locally is required before any Focus/Full promotion.
3. **Handoff readiness:** Yes. Unknowns, inspection limitations, MCP 2 status, and Gate-D-compliant safe next actions are explicitly documented with no blank sections.
