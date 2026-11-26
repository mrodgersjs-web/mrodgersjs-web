# Senior Architect Scan-Mode Note — `operation-get-a-job`

## Synthesis (Reader Priority — Rule 19)
- **Critical/High Findings:** None identified at remote root/README/manifest inspection depth.
- **Primary Recommendation:** Address the top Medium finding first — hardcoded local machine path and unpinned mcp sdk version in `mcp/server.py` — by cloning `operation-get-a-job` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/operation-get-a-job` (https://github.com/mrodgersjs-web/operation-get-a-job)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** None — remain in Scan Mode (no Critical/High trigger observed at root/manifest level; clone locally if active modification is planned).
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `MCP surface present — verify protocol after clone`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/operation-get-a-job.md`

## Architecture Area Classification
- **Frontend:** Not observed
- **Backend:** Observed (language Python, `mcp/`)
- **Database:** Not observed
- **AI or background processes:** Observed (`mcp/`)
- **External services:** Not observed
- **Infrastructure:** Observed (1 GitHub Actions workflow(s))
- **Shared modules:** Not observed
- **Tests and quality gates:** Observed (CI/lattice workflows)
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `private`, primary language: `Python`, default branch: `main`, last pushed: `2026-10-10T23:37:19Z`).
- Root directory listing (16 entries: `.github/`, `.gitignore`, `.rig/`, `AGENTS.md`, `EXPORT_MANIFEST.json`, `EXPORT_PROOF.json`, `GATES.md`, `README.md`, `START_OMP_PROMPT.md`, `integration-deliverables/`, `julie-recruiting/`, `lanes/`, `mcp/`, `previous-deliverables/`, `revenue-operation/`, `rig.repos.json`).
- README head (1200 chars inspected).
- Read-only `gh api` listing of `.github/workflows` (1 workflow(s): `rig-lattice.yml`).
- Read-only `gh api` inspection of MCP files: `mcp/server.py`.

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/operation-get-a-job` (https://github.com/mrodgersjs-web/operation-get-a-job), private, default branch `main`, primary language `Python`, last pushed `2026-10-10T23:37:19Z`.
- **Description / Topics (`Direct`):** No GitHub description set. No topics set.
- **Root surface (`Direct`):** 16 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `MCP surface present — verify protocol after clone` (inspected `mcp/server.py`).
- **CI / Automation workflows (`Direct`):** 1 workflow file(s) in `.github/workflows/`.
- **README opening (`Direct`):** # Operation Get a Job — OMP handoff — Paste the contents of START_OMP_PROMPT.md into OMP, or ask OMP to read that absolute file and execute it.

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Inferred from repository name `operation-get-a-job` and root layout (.github/, .gitignore, .rig/, AGENTS.md, EXPORT_MANIFEST.json, EXPORT_PROOF.json). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard Python module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

## Findings
### 1. Hardcoded local machine path and unpinned MCP SDK version in `mcp/server.py`
- **Dimension:** Architecture debt / Environment coupling
- **Severity:** `Medium`
- **Confidence:** `Direct`
- **Evidence:** Direct inspection of `mcp/server.py` shows `RIG_LOOP = Path.home() / "Developer/rig-capabilities/bin/rig-loop"` and `from mcp.server.fastmcp import FastMCP` without a declared MCP 2 (`2026-07-28`) version pin.
- **Impact:** Couples the MCP server to a single workstation directory layout and leaves MCP 2 protocol compliance dependent on ambient Python environment packages.
- **Smallest Safe Correction:** Proposed (requires approval): Resolve `RIG_LOOP` via an environment variable with PATH fallback, pin the `mcp` dependency in a manifest, and verify MCP 2 (`2026-07-28`) compliance after cloning.

## Open Questions
- Is this repository actively deployed or superseded by a newer consolidated studio/monorepo?
- Which exact `mcp` SDK version and protocol version (`2026-07-28` vs v1) are locked in the full dependency graph once cloned locally?

## Risks
- **Inspection blind spot:** Because this repository was not cloned locally, internal coupling, dead paths, secret sprawl inside subdirectories, and test pass rates remain unobserved.

## Safe Next Actions
- **Read-only next step:** Clone locally and verify `mcp` SDK lockfile versions and `initialize` protocol version (`2026-07-28`).
- **Read-only next step:** Keep this note as the Scan-Mode baseline; promote to Focus or Full Mode only after cloning locally and confirming an active work trigger.

## Step-8 Validation Gate Answers
1. **Claim traceability:** Yes. Every fact and finding traces directly to `shard_remote_4.json` metadata, root listings, README heads, or targeted read-only `gh api` GET responses (`Direct`), with non-inspected details explicitly labeled `Inferred`, `Assumed`, or `Not observed`.
2. **Scope alignment:** Yes. Output remains strictly within Scan Mode (one compact architecture note, read-only against GitHub) and explicitly notes that cloning locally is required before any Focus/Full promotion.
3. **Handoff readiness:** Yes. Unknowns, inspection limitations, MCP 2 status, and Gate-D-compliant safe next actions are explicitly documented with no blank sections.
