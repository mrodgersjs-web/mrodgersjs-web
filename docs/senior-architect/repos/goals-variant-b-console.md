# Senior Architect Scan-Mode Note — `goals-variant-b-console`

## Synthesis (Reader Priority — Rule 19)
- **Critical/High Findings:** None identified at remote root/README/manifest inspection depth.
- **Primary Recommendation:** Address the top Medium finding first — hardcoded local machine path and unpinned mcp sdk version in `mcp/server.py` — by cloning `goals-variant-b-console` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/goals-variant-b-console` (https://github.com/mrodgersjs-web/goals-variant-b-console)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** None — remain in Scan Mode (no Critical/High trigger observed at root/manifest level; clone locally if active modification is planned).
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `MCP surface present — verify protocol after clone`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/goals-variant-b-console.md`

## Architecture Area Classification
- **Frontend:** Observed (`next.config.ts`)
- **Backend:** Observed (language TypeScript, `src/`, `mcp/`)
- **Database:** Observed (`drizzle.config.ts`)
- **AI or background processes:** Observed (`mcp/`)
- **External services:** Observed (`.env.example`)
- **Infrastructure:** Observed (2 GitHub Actions workflow(s))
- **Shared modules:** Observed (`scripts/`)
- **Tests and quality gates:** Observed (`tests/`, `e2e/`, `evidence/`/`proof/`, CI/lattice workflows)
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `private`, primary language: `TypeScript`, default branch: `main`, last pushed: `2026-10-10T23:38:08Z`).
- Root directory listing (32 entries: `.env.example`, `.github/`, `.gitignore`, `.rig/`, `AGENTS.md`, `DESIGN-NOTES.md`, `ENGINEERING-REPORT.md`, `KICKOFF-CORE.md`, `KICKOFF.md`, `README.md`, `context/`, `docs/`, `drizzle.config.ts`, `e2e/`, `eslint.config.mjs`, `mcp/`, `measure/`, `next.config.ts`, ... (+14 more)).
- README head (1200 chars inspected).
- Read-only `gh api` listing of `.github/workflows` (2 workflow(s): `ci.yml`, `rig-lattice.yml`).
- Read-only `gh api` inspection of MCP files: `mcp/server.py`.
- Read-only `gh api` inspection of manifests: `package.json`.

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/goals-variant-b-console` (https://github.com/mrodgersjs-web/goals-variant-b-console), private, default branch `main`, primary language `TypeScript`, last pushed `2026-10-10T23:38:08Z`.
- **Description / Topics (`Direct`):** "Goals 1000x — Variant B console: Agent Accountability Score (the Measure) + BGP workflow docs" No topics set.
- **Root surface (`Direct`):** 32 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `MCP surface present — verify protocol after clone` (inspected `mcp/server.py`).
- **CI / Automation workflows (`Direct`):** 2 workflow file(s) in `.github/workflows/`.
- **README opening (`Direct`):** # GOALS — Variant B, "Console" — A Company Alignment OS for a founder-led 10–50-person company. Every goal in the

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Aligned with stated purpose ("Goals 1000x — Variant B console: Agent Accountability Score (the Measure) + BGP workflow docs"). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard TypeScript module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

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
