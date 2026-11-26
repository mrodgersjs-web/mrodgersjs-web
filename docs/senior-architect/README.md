# SeniorArchitect Portfolio Architecture Index (`mrodgersjs-web`)

Generated: `2026-11-26` | Pass level: **Scan Mode (Rule 0)** across all **149 active owned non-fork repositories** (`103` local full-filesystem inspections + `46` remote GitHub API root/README/manifest inspections). `421` upstream forks and `5` archived repos (`rig-ds-*`) are tracked in inventory and excluded from architecture mutation.

## Layer 1: Executive Synthesis (Reader Priority First)

- **Immediate Security & Secret-Hygiene Findings (`Critical`):**
  - `Startup-Intelligence-OS` (remote): hardcoded Bearer credential observed in `.mcp.json` (redacted in report) + `.env.clawswarm`/`.env.langfuse` files committed.
  - `rig-capabilities` (local, public): untracked `.signing.key` in repo root.
  - `rig-intelligence` (local): 14 untracked `.env`/`.env.bak-*` files under `platform/*` and 1,746 dirty working-tree entries.
- **MCP 2 (`2026-07-28`) Rollout Status:**
  - **10/10** core RIG estate MCP servers + **31/31** template-stamped repos + **11/11** additional custom local servers (`robonuggets-rpa`, `rig-site-transform`, `design-studio`, `rig-actor`, `rig-ai-engineering-forge`, `job-search-os`, `rigforge`, `proof-studio`, `rig-intelligence/rig_media_lab`, `rig-intelligence/lakeos`, `rig-intelligence/fleet_mcp`) are now **strict MCP 2 (`2026-07-28`) verified**.
  - **1** custom SDK server (`rig-gtm-studio-v2/mcp/server.py`) is intentionally preserved for a dedicated SDK v2 migration so its 124 passing pytest tests remain green.
  - **2** remote-only repos (`agentic-designers`, `agentic-workflows`) still carry legacy MCP v1 (`2024-11-05`) and require local clone before upgrade.
- **Primary Recommendation:** Rotate/quarantine the exposed credentials (`Startup-Intelligence-OS`, `rig-capabilities/.signing.key`, `rig-intelligence` `.env` files) FIRST, then approve Gate-D pushes in `blueprints/mcp2-estate-standard/GATE-D-PUSH-MANIFEST.json` starting with `mrodgersjs-web`, `doctrine`, and the verified MCP 2 repos.

## Portfolio Totals

| Metric | Count |
|---|---:|
| Active owned repos designed (Scan Mode) | **149** |
| Inspected locally (full tree + manifests) | 103 |
| Inspected via GitHub API (remote-only, limitation noted) | 46 |
| Repos with Critical/High findings | 33 (41 findings) |
| Total Medium/Low findings | 155 |
| Promotion triggers flagged (Focus/Full candidate) | 149 |
| Archived repos excluded | 5 |
| Public upstream forks tracked (untouched) | 421 |

## Priority Queue: Repos with Critical/High Findings

| Repository | Source | C/H Count | MCP 2 Status | Primary Recommendation | Architecture Note |
|---|---|---:|---|---|---|
| `rig-intelligence` | local | 3 | Strict MCP 2 | Immediately secure/purge the 14 untracked `.env`/`.env.bak-*` files under `platform/`, upgrade `platform/fleet-mcp/` to Strict MCP 2 (`2026- | [note](repos/rig-intelligence.md) |
| `rig-ai-engineering-forge` | local | 2 | Strict MCP 2 | Upgrade `python/rig/rig-mcp-server.py` to Strict MCP 2 (`2026-07-28`), commit the 22 dirty extension/workbench files, and wire existing `vit | [note](repos/rig-ai-engineering-forge.md) |
| `rig-capabilities` | local | 2 | Legacy MCP v1 (upgrade needed) | Immediately relocate untracked `.signing.key` out of this public repo root, then upgrade `rig_capabilities/mcp_stdio.py` from legacy v1 (`20 | [note](repos/rig-capabilities.md) |
| `rig-gtm-studio-v2` | local | 2 | Legacy MCP v1 (upgrade needed) | Upgrade `mcp/server.py` to Strict MCP 2 (`2026-07-28`), wire existing pytest suites into CI, and promote to Full Mode before refactoring the | [note](repos/rig-gtm-studio-v2.md) |
| `rig-linkedin-studio-luca` | local | 2 | Legacy MCP v1 (upgrade needed) | Consolidate root sprawl (86 root files, 84 root dirs) and align root mcp_server.py with the Strict MCP 2 (2026-07-28) contract enforced by . | [note](repos/rig-linkedin-studio-luca.md) |
| `rig-memory-os` | local | 2 | Legacy MCP v1 (upgrade needed) | Resolve the 92-file dirty working tree and dual MCP server split (founder_runtime/mcp_server.py vs products/rig-memory-os/src/rig_memory_os/ | [note](repos/rig-memory-os.md) |
| `Startup-Intelligence-OS` | remote_api | 2 | MCP surface present — verify protocol after clone | Address the top Critical finding first — hardcoded bearer credential committed in `.mcp.json` — by cloning `Startup-Intelligence-OS` locally | [note](repos/Startup-Intelligence-OS.md) |
| `agentic-designers` | remote_api | 1 | Legacy MCP v1 (upgrade needed) | Address the top High finding first — legacy mcp v1 protocol version (`2024-11-05`) in `mcp/ad_mcp.py` — by cloning `agentic-designers` local | [note](repos/agentic-designers.md) |
| `agentic-workflows` | remote_api | 1 | Legacy MCP v1 (upgrade needed) | Address the top High finding first — legacy mcp v1 protocol version (`2024-11-05`) in `mcp/agentic_mcp.py` — by cloning `agentic-workflows`  | [note](repos/agentic-workflows.md) |
| `aside-ui-build-repo` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check. | [note](repos/aside-ui-build-repo.md) |
| `behavioral-science-studio` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check. | [note](repos/behavioral-science-studio.md) |
| `billion-context` | remote_api | 1 | No MCP surface observed | Address the top High finding first — empty remote repository with zero branches and zero files — by cloning `billion-context` locally for di | [note](repos/billion-context.md) |
| `gbrain` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check. | [note](repos/gbrain.md) |
| `gtm-open-outreach` | remote_api | 1 | No MCP surface observed | Address the top High finding first — runtime sqlite database files and backups committed at repo root (app.db.bak-20261028t135046z, jobsflow | [note](repos/gtm-open-outreach.md) |
| `jake-brain-wire` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check. | [note](repos/jake-brain-wire.md) |
| `jakebrain` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check. | [note](repos/jakebrain.md) |
| `job-search-os` | local | 1 | Strict MCP 2 | Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check. | [note](repos/job-search-os.md) |
| `mrodgersjs-web` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade MCP server/client surface to Strict MCP 2 (2026-07-28) with server/discover and add rig-lattice MCP2 CI check. | [note](repos/mrodgersjs-web.md) |
| `NeoMatrix` | local | 1 | Strict MCP 2 | Resolve the dual-purpose repo boundary by adding a root `pyproject.toml` + pytest CI for `RIG_v100`/`rig_orca` (or splitting from the legacy | [note](repos/NeoMatrix.md) |
| `openwork` | remote_api | 1 | MCP surface present — verify protocol after clone | Address the top High finding first — non-example environment file(s) committed at repo root (.env.dev) — by cloning `openwork` locally for d | [note](repos/openwork.md) |
| `proof-studio` | local | 1 | Strict MCP 2 | Resolve the dual-MCP protocol mismatch by upgrading or retiring `packages/rigforge/rigforge/mcp_server.py` to match Strict MCP 2 (`2026-07-2 | [note](repos/proof-studio.md) |
| `recruiting-calendar` | local | 1 | No MCP surface observed | Triage and commit the 152 uncommitted files in bounded slices, clarify `app/` vs `site/` routing ownership, and add a CI build/test workflow | [note](repos/recruiting-calendar.md) |
| `rig-omniscout-l2` | local | 1 | Strict MCP 2 | Add a dedicated tests/ suite to cover the Prefect pipeline and consensus_mcp.py, and reconcile the 3 dirty working-tree files. | [note](repos/rig-omniscout-l2.md) |
| `rig-os-agency` | local | 1 | Strict MCP 2 | Isolate root-level operational/OAuth scripts and markdown handoffs out of the Next.js root and add automated smoke/unit tests. | [note](repos/rig-os-agency.md) |
| `rig-site-transform` | local | 1 | Strict MCP 2 | Upgrade stx/mcp_server.py from legacy JSON-RPC 2.0 v1 to Strict MCP 2 (2026-07-28), add pyproject.toml + GitHub CI, and clean .bak files in  | [note](repos/rig-site-transform.md) |
| `rig-studios` | local | 1 | Legacy MCP v1 (upgrade needed) | Audit MCP-SERVERS.json and scripts/mcp-serve against Strict MCP 2 (2026-07-28) and add a local/CI workflow to run tests/test_invariants.py + | [note](repos/rig-studios.md) |
| `rig-website` | local | 1 | No MCP surface observed | Triage the 66 dirty working-tree files and separate transient QA/report outputs (test-results/, jev-seo-reports/) from source/overlay files. | [note](repos/rig-website.md) |
| `robonuggets-rpa` | local | 1 | Strict MCP 2 | Upgrade rnpa.mcp_server and mcp.json to Strict MCP 2 (2026-07-28), add .github/workflows/ CI, and verify .env is gitignored. | [note](repos/robonuggets-rpa.md) |
| `traject-jen-rodgers` | local | 1 | No MCP surface observed | Add automated CI running typecheck + owner-isolation verification scripts, and clean up .scratch-probe.mts at root. | [note](repos/traject-jen-rodgers.md) |
| `transformfit-flutter` | local | 1 | Strict MCP 2 | Archive or consolidate the 25+ root-level status/audit markdown files under docs/ so root stays focused on Flutter, Supabase, and release co | [note](repos/transformfit-flutter.md) |
| `transformfit-full-testing` | remote_api | 1 | No MCP surface observed | Address the top High finding first — committed `.magic-link` and `.sim-udid` runtime artifacts at repo root — by cloning `transformfit-full- | [note](repos/transformfit-full-testing.md) |
| `unified-engines-repo` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade pyproject.toml (`mcp>=1.2,<2` pin) and rigengines/mcp_server.py (FastMCP) to Strict MCP 2 (2026-07-28), and fix the hardcoded .mcp.j | [note](repos/unified-engines-repo.md) |
| `upwork-mcp` | local | 1 | Legacy MCP v1 (upgrade needed) | Upgrade pyproject.toml (`mcp>=1.2,<2`) and src/upwork_mcp/server.py (FastMCP) to Strict MCP 2 (2026-07-28) when ready to drop v1 pin. | [note](repos/upwork-mcp.md) |

## Complete 149-Repository Scan-Mode Directory

| # | Repository | Source | Pass | MCP 2 Status | C/H | M/L | Note |
|---:|---|---|---|---|---:|---:|---|
| 1 | `agency-studio` | local | Scan Mode | Strict MCP 2 | 0 | 0 | [agency-studio.md](repos/agency-studio.md) |
| 2 | `agentic-designers` | remote_api | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 2 | [agentic-designers.md](repos/agentic-designers.md) |
| 3 | `agentic-workflows` | remote_api | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 0 | [agentic-workflows.md](repos/agentic-workflows.md) |
| 4 | `ai-user-testing-mcp` | local | Scan Mode | Strict MCP 2 | 0 | 0 | [ai-user-testing-mcp.md](repos/ai-user-testing-mcp.md) |
| 5 | `alex-recruiting-rebuilt` | local | Scan Mode | No MCP surface observed | 0 | 2 | [alex-recruiting-rebuilt.md](repos/alex-recruiting-rebuilt.md) |
| 6 | `app-factory-studio` | local | Scan Mode | No MCP surface observed | 0 | 0 | [app-factory-studio.md](repos/app-factory-studio.md) |
| 7 | `aside` | local | Scan Mode | No MCP surface observed | 0 | 0 | [aside.md](repos/aside.md) |
| 8 | `aside-ui-build-repo` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 2 | [aside-ui-build-repo.md](repos/aside-ui-build-repo.md) |
| 9 | `autark-boring-consumables` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-boring-consumables.md](repos/autark-boring-consumables.md) |
| 10 | `autark-leadership` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-leadership.md](repos/autark-leadership.md) |
| 11 | `autark-rig-ai-products-devtools` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-rig-ai-products-devtools.md](repos/autark-rig-ai-products-devtools.md) |
| 12 | `autark-rig-enterprise-prime-contracting` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-rig-enterprise-prime-contracting.md](repos/autark-rig-enterprise-prime-contracting.md) |
| 13 | `autark-rig-federal-defense` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-rig-federal-defense.md](repos/autark-rig-federal-defense.md) |
| 14 | `autark-rig-field-clinic-systems` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-rig-field-clinic-systems.md](repos/autark-rig-field-clinic-systems.md) |
| 15 | `autark-traject-career-grokbots` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-traject-career-grokbots.md](repos/autark-traject-career-grokbots.md) |
| 16 | `autark-transformfit` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-transformfit.md](repos/autark-transformfit.md) |
| 17 | `autark-webforge-site-transform` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [autark-webforge-site-transform.md](repos/autark-webforge-site-transform.md) |
| 18 | `behavioral-science-studio` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 2 | [behavioral-science-studio.md](repos/behavioral-science-studio.md) |
| 19 | `billion-context` | remote_api | Scan Mode | No MCP surface observed | 1 | 0 | [billion-context.md](repos/billion-context.md) |
| 20 | `birch-rig-boots` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [birch-rig-boots.md](repos/birch-rig-boots.md) |
| 21 | `bravesales` | local | Scan Mode | No MCP surface observed | 0 | 1 | [bravesales.md](repos/bravesales.md) |
| 22 | `cards-sprint` | remote_api | Scan Mode | No MCP surface observed | 0 | 3 | [cards-sprint.md](repos/cards-sprint.md) |
| 23 | `client-engine-4` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [client-engine-4.md](repos/client-engine-4.md) |
| 24 | `clients-ai-jobs` | local | Scan Mode | No MCP surface observed | 0 | 3 | [clients-ai-jobs.md](repos/clients-ai-jobs.md) |
| 25 | `commit-book` | local | Scan Mode | No MCP surface observed | 0 | 0 | [commit-book.md](repos/commit-book.md) |
| 26 | `communications-studio` | local | Scan Mode | Strict MCP 2 | 0 | 0 | [communications-studio.md](repos/communications-studio.md) |
| 27 | `design-studio` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [design-studio.md](repos/design-studio.md) |
| 28 | `deviatrix-genesis` | local | Scan Mode | Strict MCP 2 | 0 | 0 | [deviatrix-genesis.md](repos/deviatrix-genesis.md) |
| 29 | `doctrine` | local | Scan Mode | No MCP surface observed | 0 | 0 | [doctrine.md](repos/doctrine.md) |
| 30 | `doneseal` | local | Scan Mode | No MCP surface observed | 0 | 0 | [doneseal.md](repos/doneseal.md) |
| 31 | `fde` | local | Scan Mode | No MCP surface observed | 0 | 0 | [fde.md](repos/fde.md) |
| 32 | `fde-portfolio` | local | Scan Mode | Strict MCP 2 | 0 | 0 | [fde-portfolio.md](repos/fde-portfolio.md) |
| 33 | `gbrain` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 0 | [gbrain.md](repos/gbrain.md) |
| 34 | `getnewideas` | local | Scan Mode | No MCP surface observed | 0 | 0 | [getnewideas.md](repos/getnewideas.md) |
| 35 | `goals-variant-b-console` | remote_api | Scan Mode | MCP surface present — verify protocol after clone | 0 | 1 | [goals-variant-b-console.md](repos/goals-variant-b-console.md) |
| 36 | `golive-runtime` | local | Scan Mode | No MCP surface observed | 0 | 2 | [golive-runtime.md](repos/golive-runtime.md) |
| 37 | `grokbot-academy` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [grokbot-academy.md](repos/grokbot-academy.md) |
| 38 | `gtm-open-outreach` | remote_api | Scan Mode | No MCP surface observed | 1 | 3 | [gtm-open-outreach.md](repos/gtm-open-outreach.md) |
| 39 | `harness-optimizer-fleet-20261025` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [harness-optimizer-fleet-20261025.md](repos/harness-optimizer-fleet-20261025.md) |
| 40 | `heycatch` | local | Scan Mode | No MCP surface observed | 0 | 0 | [heycatch.md](repos/heycatch.md) |
| 41 | `heycatch-clone` | remote_api | Scan Mode | No MCP surface observed | 0 | 2 | [heycatch-clone.md](repos/heycatch-clone.md) |
| 42 | `higgsfield-studio-os` | remote_api | Scan Mode | MCP surface present — verify protocol after clone | 0 | 1 | [higgsfield-studio-os.md](repos/higgsfield-studio-os.md) |
| 43 | `home-assistant-big-birch` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [home-assistant-big-birch.md](repos/home-assistant-big-birch.md) |
| 44 | `human-agency-goals` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [human-agency-goals.md](repos/human-agency-goals.md) |
| 45 | `jacob-film-studio` | local | Scan Mode | No MCP surface observed | 0 | 0 | [jacob-film-studio.md](repos/jacob-film-studio.md) |
| 46 | `jacob-x-studio` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [jacob-x-studio.md](repos/jacob-x-studio.md) |
| 47 | `jacob-x-weekly` | local | Scan Mode | No MCP surface observed | 0 | 1 | [jacob-x-weekly.md](repos/jacob-x-weekly.md) |
| 48 | `jake-brain-wire` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 2 | [jake-brain-wire.md](repos/jake-brain-wire.md) |
| 49 | `jake-pai-mcp` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [jake-pai-mcp.md](repos/jake-pai-mcp.md) |
| 50 | `jake-studio` | local | Scan Mode | Strict MCP 2 | 0 | 0 | [jake-studio.md](repos/jake-studio.md) |
| 51 | `jakebrain` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 1 | [jakebrain.md](repos/jakebrain.md) |
| 52 | `jev-route` | remote_api | Scan Mode | No MCP surface observed | 0 | 0 | [jev-route.md](repos/jev-route.md) |
| 53 | `job-campaign-buildout-repo` | remote_api | Scan Mode | No MCP surface observed | 0 | 0 | [job-campaign-buildout-repo.md](repos/job-campaign-buildout-repo.md) |
| 54 | `job-plays` | remote_api | Scan Mode | No MCP surface observed | 0 | 2 | [job-plays.md](repos/job-plays.md) |
| 55 | `job-search-os` | local | Scan Mode | Strict MCP 2 | 1 | 1 | [job-search-os.md](repos/job-search-os.md) |
| 56 | `latency-probe` | remote_api | Scan Mode | No MCP surface observed | 0 | 0 | [latency-probe.md](repos/latency-probe.md) |
| 57 | `mesh-studio` | local | Scan Mode | Strict MCP 2 | 0 | 0 | [mesh-studio.md](repos/mesh-studio.md) |
| 58 | `mike-personal-brand` | local | Scan Mode | No MCP surface observed | 0 | 0 | [mike-personal-brand.md](repos/mike-personal-brand.md) |
| 59 | `mike-rodgers-site` | remote_api | Scan Mode | MCP surface present — verify protocol after clone | 0 | 2 | [mike-rodgers-site.md](repos/mike-rodgers-site.md) |
| 60 | `mrodgersjs-web` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 0 | [mrodgersjs-web.md](repos/mrodgersjs-web.md) |
| 61 | `mrodgersjs-web-teammate` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [mrodgersjs-web-teammate.md](repos/mrodgersjs-web-teammate.md) |
| 62 | `n8n` | local | Scan Mode | No MCP surface observed | 0 | 1 | [n8n.md](repos/n8n.md) |
| 63 | `nanobrowser` | local | Scan Mode | No MCP surface observed | 0 | 3 | [nanobrowser.md](repos/nanobrowser.md) |
| 64 | `NeoMatrix` | local | Scan Mode | Strict MCP 2 | 1 | 2 | [NeoMatrix.md](repos/NeoMatrix.md) |
| 65 | `openbot-channel` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [openbot-channel.md](repos/openbot-channel.md) |
| 66 | `openbot-one-setup` | remote_api | Scan Mode | No MCP surface observed | 0 | 2 | [openbot-one-setup.md](repos/openbot-one-setup.md) |
| 67 | `openseo-library` | local | Scan Mode | No MCP surface observed | 0 | 1 | [openseo-library.md](repos/openseo-library.md) |
| 68 | `openseo-os` | local | Scan Mode | No MCP surface observed | 0 | 2 | [openseo-os.md](repos/openseo-os.md) |
| 69 | `openwork` | remote_api | Scan Mode | MCP surface present — verify protocol after clone | 1 | 2 | [openwork.md](repos/openwork.md) |
| 70 | `operation-get-a-job` | remote_api | Scan Mode | MCP surface present — verify protocol after clone | 0 | 1 | [operation-get-a-job.md](repos/operation-get-a-job.md) |
| 71 | `patents` | local | Scan Mode | No MCP surface observed | 0 | 0 | [patents.md](repos/patents.md) |
| 72 | `patents-vault` | local | Scan Mode | No MCP surface observed | 0 | 1 | [patents-vault.md](repos/patents-vault.md) |
| 73 | `proof-gate-action` | local | Scan Mode | No MCP surface observed | 0 | 0 | [proof-gate-action.md](repos/proof-gate-action.md) |
| 74 | `proof-studio` | local | Scan Mode | Strict MCP 2 | 1 | 1 | [proof-studio.md](repos/proof-studio.md) |
| 75 | `recruiting-calendar` | local | Scan Mode | No MCP surface observed | 1 | 1 | [recruiting-calendar.md](repos/recruiting-calendar.md) |
| 76 | `resume` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [resume.md](repos/resume.md) |
| 77 | `resume-doctrine-gate` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [resume-doctrine-gate.md](repos/resume-doctrine-gate.md) |
| 78 | `rig-academy` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [rig-academy.md](repos/rig-academy.md) |
| 79 | `rig-actor` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [rig-actor.md](repos/rig-actor.md) |
| 80 | `rig-agent-directory` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [rig-agent-directory.md](repos/rig-agent-directory.md) |
| 81 | `rig-agent-firm` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [rig-agent-firm.md](repos/rig-agent-firm.md) |
| 82 | `rig-ai-engineering` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [rig-ai-engineering.md](repos/rig-ai-engineering.md) |
| 83 | `rig-ai-engineering-forge` | local | Scan Mode | Strict MCP 2 | 2 | 0 | [rig-ai-engineering-forge.md](repos/rig-ai-engineering-forge.md) |
| 84 | `rig-build` | local | Scan Mode | No MCP surface observed | 0 | 1 | [rig-build.md](repos/rig-build.md) |
| 85 | `rig-capabilities` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 2 | 1 | [rig-capabilities.md](repos/rig-capabilities.md) |
| 86 | `rig-community-skool` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [rig-community-skool.md](repos/rig-community-skool.md) |
| 87 | `rig-company-os` | local | Scan Mode | No MCP surface observed | 0 | 0 | [rig-company-os.md](repos/rig-company-os.md) |
| 88 | `rig-d87da613-be7e-4175-945d-d0237a2526ee` | remote_api | Scan Mode | No MCP surface observed | 0 | 0 | [rig-d87da613-be7e-4175-945d-d0237a2526ee.md](repos/rig-d87da613-be7e-4175-945d-d0237a2526ee.md) |
| 89 | `rig-design-studio-corpus` | local | Scan Mode | No MCP surface observed | 0 | 2 | [rig-design-studio-corpus.md](repos/rig-design-studio-corpus.md) |
| 90 | `rig-deviate` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [rig-deviate.md](repos/rig-deviate.md) |
| 91 | `rig-doctrine-overlay` | local | Scan Mode | No MCP surface observed | 0 | 0 | [rig-doctrine-overlay.md](repos/rig-doctrine-overlay.md) |
| 92 | `rig-domain-agents` | local | Scan Mode | No MCP surface observed | 0 | 2 | [rig-domain-agents.md](repos/rig-domain-agents.md) |
| 93 | `rig-enhanced-agent-ops` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [rig-enhanced-agent-ops.md](repos/rig-enhanced-agent-ops.md) |
| 94 | `rig-enhanced-evals` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [rig-enhanced-evals.md](repos/rig-enhanced-evals.md) |
| 95 | `rig-enhanced-guardrails` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [rig-enhanced-guardrails.md](repos/rig-enhanced-guardrails.md) |
| 96 | `rig-free-agent-kit` | local | Scan Mode | No MCP surface observed | 0 | 0 | [rig-free-agent-kit.md](repos/rig-free-agent-kit.md) |
| 97 | `rig-grokbots-delivery` | local | Scan Mode | No MCP surface observed | 0 | 2 | [rig-grokbots-delivery.md](repos/rig-grokbots-delivery.md) |
| 98 | `rig-gtm-studio-v2` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 2 | 1 | [rig-gtm-studio-v2.md](repos/rig-gtm-studio-v2.md) |
| 99 | `rig-harness-tools` | local | Scan Mode | No MCP surface observed | 0 | 1 | [rig-harness-tools.md](repos/rig-harness-tools.md) |
| 100 | `rig-intelligence` | local | Scan Mode | Strict MCP 2 | 3 | 0 | [rig-intelligence.md](repos/rig-intelligence.md) |
| 101 | `rig-jevrouter` | remote_api | Scan Mode | No MCP surface observed | 0 | 2 | [rig-jevrouter.md](repos/rig-jevrouter.md) |
| 102 | `rig-jobsearch-grokbots` | local | Scan Mode | No MCP surface observed | 0 | 1 | [rig-jobsearch-grokbots.md](repos/rig-jobsearch-grokbots.md) |
| 103 | `rig-jobsearch-strategy` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [rig-jobsearch-strategy.md](repos/rig-jobsearch-strategy.md) |
| 104 | `rig-linkedin-studio-luca` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 2 | 1 | [rig-linkedin-studio-luca.md](repos/rig-linkedin-studio-luca.md) |
| 105 | `rig-marketplace` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [rig-marketplace.md](repos/rig-marketplace.md) |
| 106 | `rig-memory-fabric` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [rig-memory-fabric.md](repos/rig-memory-fabric.md) |
| 107 | `rig-memory-os` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 2 | 1 | [rig-memory-os.md](repos/rig-memory-os.md) |
| 108 | `rig-model-router` | remote_api | Scan Mode | No MCP surface observed | 0 | 3 | [rig-model-router.md](repos/rig-model-router.md) |
| 109 | `rig-omniscout-l2` | local | Scan Mode | Strict MCP 2 | 1 | 1 | [rig-omniscout-l2.md](repos/rig-omniscout-l2.md) |
| 110 | `rig-os-agency` | local | Scan Mode | Strict MCP 2 | 1 | 1 | [rig-os-agency.md](repos/rig-os-agency.md) |
| 111 | `rig-pattern-engines` | local | Scan Mode | No MCP surface observed | 0 | 0 | [rig-pattern-engines.md](repos/rig-pattern-engines.md) |
| 112 | `rig-site-transform` | local | Scan Mode | Strict MCP 2 | 1 | 1 | [rig-site-transform.md](repos/rig-site-transform.md) |
| 113 | `rig-skills` | local | Scan Mode | No MCP surface observed | 0 | 2 | [rig-skills.md](repos/rig-skills.md) |
| 114 | `rig-soar-intelligent-ui` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [rig-soar-intelligent-ui.md](repos/rig-soar-intelligent-ui.md) |
| 115 | `rig-soar-switch` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [rig-soar-switch.md](repos/rig-soar-switch.md) |
| 116 | `rig-studio-factory` | local | Scan Mode | No MCP surface observed | 0 | 1 | [rig-studio-factory.md](repos/rig-studio-factory.md) |
| 117 | `rig-studios` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 1 | [rig-studios.md](repos/rig-studios.md) |
| 118 | `rig-swan` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [rig-swan.md](repos/rig-swan.md) |
| 119 | `rig-tac-system` | local | Scan Mode | No MCP surface observed | 0 | 2 | [rig-tac-system.md](repos/rig-tac-system.md) |
| 120 | `rig-vote` | local | Scan Mode | No MCP surface observed | 0 | 1 | [rig-vote.md](repos/rig-vote.md) |
| 121 | `rig-website` | local | Scan Mode | No MCP surface observed | 1 | 1 | [rig-website.md](repos/rig-website.md) |
| 122 | `rigdots-company` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [rigdots-company.md](repos/rigdots-company.md) |
| 123 | `rigdots-soar` | local | Scan Mode | No MCP surface observed | 0 | 1 | [rigdots-soar.md](repos/rigdots-soar.md) |
| 124 | `rigforge` | local | Scan Mode | Strict MCP 2 | 0 | 1 | [rigforge.md](repos/rigforge.md) |
| 125 | `RIGTaste` | local | Scan Mode | No MCP surface observed | 0 | 1 | [RIGTaste.md](repos/RIGTaste.md) |
| 126 | `robonuggets-rpa` | local | Scan Mode | Strict MCP 2 | 1 | 1 | [robonuggets-rpa.md](repos/robonuggets-rpa.md) |
| 127 | `robonuggets-vault` | local | Scan Mode | No MCP surface observed | 0 | 1 | [robonuggets-vault.md](repos/robonuggets-vault.md) |
| 128 | `route-check` | local | Scan Mode | No MCP surface observed | 0 | 0 | [route-check.md](repos/route-check.md) |
| 129 | `scrappers` | local | Scan Mode | No MCP surface observed | 0 | 1 | [scrappers.md](repos/scrappers.md) |
| 130 | `soar-live-20261027` | remote_api | Scan Mode | No MCP surface observed | 0 | 2 | [soar-live-20261027.md](repos/soar-live-20261027.md) |
| 131 | `Startup-Intelligence-OS` | remote_api | Scan Mode | MCP surface present — verify protocol after clone | 2 | 3 | [Startup-Intelligence-OS.md](repos/Startup-Intelligence-OS.md) |
| 132 | `strategy-studio` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [strategy-studio.md](repos/strategy-studio.md) |
| 133 | `traject-jen-rodgers` | local | Scan Mode | No MCP surface observed | 1 | 1 | [traject-jen-rodgers.md](repos/traject-jen-rodgers.md) |
| 134 | `transformfit-agent` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [transformfit-agent.md](repos/transformfit-agent.md) |
| 135 | `transformfit-flutter` | local | Scan Mode | Strict MCP 2 | 1 | 1 | [transformfit-flutter.md](repos/transformfit-flutter.md) |
| 136 | `transformfit-full-testing` | remote_api | Scan Mode | No MCP surface observed | 1 | 2 | [transformfit-full-testing.md](repos/transformfit-full-testing.md) |
| 137 | `transformfit-landing` | local | Scan Mode | No MCP surface observed | 0 | 1 | [transformfit-landing.md](repos/transformfit-landing.md) |
| 138 | `unified-business-repo` | local | Scan Mode | No MCP surface observed | 0 | 1 | [unified-business-repo.md](repos/unified-business-repo.md) |
| 139 | `unified-canvas-repo` | local | Scan Mode | No MCP surface observed | 0 | 1 | [unified-canvas-repo.md](repos/unified-canvas-repo.md) |
| 140 | `unified-engines-repo` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 1 | [unified-engines-repo.md](repos/unified-engines-repo.md) |
| 141 | `unified-governance-repo` | local | Scan Mode | No MCP surface observed | 0 | 1 | [unified-governance-repo.md](repos/unified-governance-repo.md) |
| 142 | `unified-media-repo` | remote_api | Scan Mode | No MCP surface observed | 0 | 0 | [unified-media-repo.md](repos/unified-media-repo.md) |
| 143 | `unified-org-repo` | remote_api | Scan Mode | No MCP surface observed | 0 | 1 | [unified-org-repo.md](repos/unified-org-repo.md) |
| 144 | `unified-shell-repo` | local | Scan Mode | No MCP surface observed | 0 | 2 | [unified-shell-repo.md](repos/unified-shell-repo.md) |
| 145 | `unified-voice-repo` | local | Scan Mode | No MCP surface observed | 0 | 1 | [unified-voice-repo.md](repos/unified-voice-repo.md) |
| 146 | `unified-workspaces-repo` | local | Scan Mode | No MCP surface observed | 0 | 1 | [unified-workspaces-repo.md](repos/unified-workspaces-repo.md) |
| 147 | `upwork-mcp` | local | Scan Mode | Legacy MCP v1 (upgrade needed) | 1 | 1 | [upwork-mcp.md](repos/upwork-mcp.md) |
| 148 | `vibe-production-gauntlet` | local | Scan Mode | Strict MCP 2 | 0 | 2 | [vibe-production-gauntlet.md](repos/vibe-production-gauntlet.md) |
| 149 | `workflow-design-studio-repo` | remote_api | Scan Mode | No MCP surface observed | 0 | 0 | [workflow-design-studio-repo.md](repos/workflow-design-studio-repo.md) |

## Step 8 Validation Gate (Portfolio Level)

1. **Claim traceability:** Every repository note traces directly to inspected local filesystem trees/manifests (`103` repos) or live GitHub API metadata/root trees/READMEs (`46` repos). All uninspected categories are explicitly marked `Not observed` and remote-only limitations are stated.
2. **Scope alignment:** Covers 100% of active owned non-fork `mrodgersjs-web` repositories (`149/149`) in Scan Mode (Rule 0). No unapproved pushes or production edits were made.
3. **Handoff readiness:** Every note includes open questions, risks, promotion triggers, and smallest safe next actions; all local MCP 2 upgrades are staged in `GATE-D-PUSH-MANIFEST.json` awaiting explicit Gate-D push approval.
