# Senior Architect Scan-Mode Note — `agentic-workflows`

## Synthesis (Reader Priority — Rule 19)
- **High:** Legacy MCP v1 protocol version (`2024-11-05`) in `mcp/agentic_mcp.py` (Direct — Direct inspection of `mcp/agentic_mcp.py` via GitHub API confirmed protocol string `2024-11-05` in the custom stdio JSON-RPC 2.0 shim.)
- **Primary Recommendation:** Address the top High finding first — legacy mcp v1 protocol version (`2024-11-05`) in `mcp/agentic_mcp.py` — by cloning `agentic-workflows` locally for direct verification before applying the proposed smallest safe correction (subject to owner approval).

## Intake, Pass Control & Inspection Scope
- **Repository:** `mrodgersjs-web/agentic-workflows` (https://github.com/mrodgersjs-web/agentic-workflows)
- **Pass Level:** `Scan Mode` (default per Rule 0)
- **Promotion Trigger:** Focus Promotion Triggered (clone locally first): Direct Legacy MCP v1 (`2024-11-05`) protocol finding requires local clone to upgrade and verify MCP 2 (`2026-07-28`) compliance.
- **Inspection Limitation:** Remote GitHub API root/README/manifest inspection only; not cloned locally.
- **MCP 2 (`2026-07-28`) Status:** `Legacy MCP v1 (upgrade needed)`
- **Output Path:** `/Users/rig128gb/Desktop/Projects/mrodgersjs-web/docs/senior-architect/repos/agentic-workflows.md`

## Architecture Area Classification
- **Frontend:** Not observed
- **Backend:** Observed (language Python, `mcp/`)
- **Database:** Not observed
- **AI or background processes:** Observed (`mcp/`)
- **External services:** Observed (self-hosted designer HTTP APIs over tailnet)
- **Infrastructure:** Not observed
- **Shared modules:** Observed (`scripts/`)
- **Tests and quality gates:** Not observed
- **Unknown or unclear areas:** Internal source modules, runtime call graphs, dependency trees, and live deployment bindings were not inspected (remote GitHub API root/README/manifest inspection only; not cloned locally).

## Evidence Checked & Skipped Areas
### Evidence Checked
- GitHub repository metadata via `shard_remote_4.json` (visibility: `public`, primary language: `Python`, default branch: `main`, last pushed: `2026-10-30T02:11:23Z`).
- Root directory listing (9 entries: `.github/`, `AGENTS.md`, `LICENSE`, `README.md`, `assets/`, `designers/`, `mcp/`, `results/`, `scripts/`).
- README head (1200 chars inspected).
- Read-only `gh api` inspection of MCP files: `mcp/agentic_mcp.py`.

### Skipped Areas
- Source file internals, git commit history, local runtime execution, test execution, and full lockfile/dependency trees were skipped because this is a read-only remote Scan-Mode pass (not cloned locally).

## Confirmed Facts (`Direct`)
- **Repository identity (`Direct`):** `mrodgersjs-web/agentic-workflows` (https://github.com/mrodgersjs-web/agentic-workflows), public, default branch `main`, primary language `Python`, last pushed `2026-10-30T02:11:23Z`.
- **Description / Topics (`Direct`):** "Six self-hosted agentic designers (n8n, Flowise, Dify, Trigger.dev, LangGraph, CrewAI) run against one local model router, with checked-in run proofs and one MCP server to drive them all." Topics: `agent-governance`, `ai-agents`, `crewai`, `dify`, `evals`, `flowise`, `forward-deployed-engineer`, `langgraph`, `llm`, `mcp`, `mlops`, `n8n`, `proof-gates`, `self-hosted`, `trigger-dev`.
- **Root surface (`Direct`):** 9 top-level entries observed.
- **MCP 2 (2026-07-28) status (`Direct`):** `Legacy MCP v1 (upgrade needed)` (inspected `mcp/agentic_mcp.py`).
- **README opening (`Direct`):** # agentic-workflows — The same hello-agent, built once per designer, run across six agentic workflow

## Inferences & Assumptions (`Inferred` / `Assumed`)
- **Operational role (`Inferred`):** Aligned with stated purpose ("Six self-hosted agentic designers (n8n, Flowise, Dify, Trigger.dev, LangGraph, CrewAI) run against one local model router, with checked-in r"). Verify first: Yes.
- **Internal module boundaries (`Assumed`):** Standard Python module boundaries are assumed inside uninspected subdirectories until a local clone permits direct file reading.

## Findings
### 1. Legacy MCP v1 protocol version (`2024-11-05`) in `mcp/agentic_mcp.py`
- **Dimension:** Framework convention drift
- **Severity:** `High`
- **Confidence:** `Direct`
- **Evidence:** Direct inspection of `mcp/agentic_mcp.py` via GitHub API confirmed protocol string `2024-11-05` in the custom stdio JSON-RPC 2.0 shim.
- **Impact:** Drifts from the MCP 2 (`2026-07-28`) standard and may lose compatibility with MCP 2 clients or capability negotiation.
- **Smallest Safe Correction:** Proposed (requires approval): Upgrade `mcp/agentic_mcp.py` to MCP 2 (`2026-07-28`) protocol negotiation and verify against an MCP 2 test harness after cloning locally.

## Open Questions
- Is this repository actively deployed or superseded by a newer consolidated studio/monorepo?
- Are any credentials or runtime data files flagged above still active in production or third-party services?

## Risks
- **Inspection blind spot:** Because this repository was not cloned locally, internal coupling, dead paths, secret sprawl inside subdirectories, and test pass rates remain unobserved.
- **Active defect risk:** 1 Critical/High finding(s) observed at root/manifest level could impact security, data hygiene, or MCP 2 compatibility if left unaddressed.

## Safe Next Actions
- **Proposed (Gate-D approval required):** Clone the repository locally and remediate the Critical/High finding(s) listed above using the smallest safe correction.
- **Proposed (Gate-D approval required):** Upgrade the MCP shim from `2024-11-05` to strict MCP 2 (`2026-07-28`) after cloning locally.
- **Read-only next step:** Keep this note as the Scan-Mode baseline; promote to Focus or Full Mode only after cloning locally and confirming an active work trigger.

## Step-8 Validation Gate Answers
1. **Claim traceability:** Yes. Every fact and finding traces directly to `shard_remote_4.json` metadata, root listings, README heads, or targeted read-only `gh api` GET responses (`Direct`), with non-inspected details explicitly labeled `Inferred`, `Assumed`, or `Not observed`.
2. **Scope alignment:** Yes. Output remains strictly within Scan Mode (one compact architecture note, read-only against GitHub) and explicitly notes that cloning locally is required before any Focus/Full promotion.
3. **Handoff readiness:** Yes. Unknowns, inspection limitations, MCP 2 status, and Gate-D-compliant safe next actions are explicitly documented with no blank sections.
