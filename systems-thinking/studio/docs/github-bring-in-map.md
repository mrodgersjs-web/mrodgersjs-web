# GitHub Bring-In Map — What We Have and Where It Lands

Surveyed 2026-08-28 via `gh` (accounts: mrodgersjs-web active; org rodgemd1-lgtm;
rig-intelligence canonical local at ~/Developer/rig-intelligence).

## rodgemd1-lgtm org (25 repos) — import status

| Repo | What it holds | Studio import | Status |
|---|---|---|---|
| proofpacket-sealing-template | `seal.py`/`verify.py` — HMAC ProofPackets | VERIFY phase seals every run | **IMPORTED** (vendored `proofpacket/`) |
| RIG-Doctrine-Repo | doctrines/: DETERMINISTIC-BEFORE-AGENTIC, PHASE-DISCIPLINE, PROOF-OR-IT-DIDNT-HAPPEN, ADVERSARIAL-VERIFICATION, GATE-D, IQRSQPI + agent-packs/ + schemas/ | Process doctrine layer for all studios; phase discipline already embedded in harness gates | **PARTIAL** — doctrines referenced; full pack import queued |
| rig-deviate | 40 deviation engines × 14 σ rungs | POLYMATH enrichment (COLLIDER engine = the crosspoll doctrine's origin) | SLOT — crosspoll can call `rig_engines agent-run COLLIDER` when venv present |
| strategy-studio | 147-cell deterministic decision-routing engine | Routing pattern for studio dispatch (which studio owns an ask) | PATTERN — mirror for studio-router (planned) |
| rig-agent-firm | 6 role-agents + forkable constitution + heartbeat telemetry | Studio agent constitution + role spec template | QUEUED for agents/ expansion |
| rig-verticals | 21 agent specs per vertical | Agent spec template for per-studio specialist specs | QUEUED |
| rig-memory-os | Calibrated memory, Brier predictions, 4 closed loops | Post-run learning: falsifier outcomes → memory | QUEUED (local worktree exists) |
| rig-enhanced-evals | L10 self-evolving eval harness | Evals for studio outputs (per Skills-Masterclass: skills need evals) | QUEUED |
| rig-enhanced-guardrails | Schema/factuality gates + signed ProofPackets | Hard-gate artifacts before DELIVERABLE ships | QUEUED |
| rig-ai-engineering | 4-axis prompt scoring | Score phase prompts; keep them Specific/Doctrinal/Contextual/Actionable | QUEUED |
| rigforge / rigforge-legacy | 7-phase deterministic agentic engineering, MCP, OTel | Cross-check our 8-phase chain against their 7-phase contract | REFERENCE |
| rig-communications | V10 communication engine, 8 scoring formulas, 24 hard gates | Gate formulas for content-facing studios | LATER (content studios) |
| rig-os-agency / JakeStudio / ai-company / RIG-Mesh / omniscout-l2 / spend-reduction / rig-demo / rig-prediction-studio / RIG-AI-Engineering / design-studio / persona-os / the-deviation / rusr / crawlee-cli / profile | Operational surfaces, teasers, product sites | Not studio-core; design-studio checklists useful when studios get UIs | MONITOR |

## mrodgersjs-web account (15 repos)

| Repo | What it holds | Studio import | Status |
|---|---|---|---|
| rig-intelligence | This monorepo (canonical) | Home of the studio | **LIVE** |
| human-agency-goals | Altitude — governed alignment loop for founder-led firms | Alignment-loop pattern for INTAKE (founder-goal contract) | QUEUED |
| proof-studio | HMAC-signed ProofPackets, "catch agents lying about done" | Same as sealing template — richer CLI | ALT (template suffices today) |
| rig-enhanced-evals / rig-enhanced-guardrails / rig-ai-engineering / rigforge / rig-deviate | Mirrors/teasers of org repos above | — | — |
| rig-gtm-studio-v2 | GTM ops monorepo | **Next studio to build** on this pattern (domain packs exist) | NEXT |
| rig-marketplace, traject-jen-rodgers, NeoMatrix, rig-os-agency (mirror), design-studio, strategy-studio (public surface) | Product/marketplace surfaces | — | MONITOR |

## Import queue (ordered, next actions)

1. RIG-Doctrine-Repo → vendor the 5 core doctrines into `references/doctrines/` + wire names into process docs
2. rig-agent-firm constitution → `agents/constitution.md`
3. rig-memory-os falsifier feedback loop → post-VERIFY hook: log falsifier + deadline; on outcome, record Brier-style score
4. rig-enhanced-evals → eval set for the studio (seeded problems + expected archetype/leverage answers)
5. rig-deviate COLLIDER → optional deepener for POLYMATH phase
