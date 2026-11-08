# v0 is a governed engine. v2 is the firm OS.

Measured 2026-08-30. `docs/JAKE-PAI-V2.md` is prior opinion (it still says 6 workflows). Live CLI says **21**. Do not treat that blueprint as proof.

---

## 1. Live v0 (not the brochure)

| Surface | Live count | Source |
|---|---|---|
| Workflows | **21** (13 det-only, 8 mixed) | `jake-workflow list` |
| Agent specs | **24** | `~/Developer/jake-workflows/agents/specs/*.json` |
| MCP tools | **16** | `jake-pai-mcp/server.py` `_t_*` |
| Run index | **7744** lines | `~/.jake/workflows/runs/index.jsonl` |
| Hermes jobs | **146** | `~/.hermes/cron/jobs.json` `jobs` array |
| Test battery | **86/87 PASS**, exit 1 | LeafV0: `.venv/bin/python tests/run_tests.py` |
| Sole test fail | `seal_proof skeleton status` | same run |
| Fleet probe | **7** nodes: 4 READY, 2 WEDGED, 1 DOWN | `xd://rig_fleet status` |
| Inventory file | **8** named hosts (includes 48GB/28GB/QNAP not in live table) | `~/.rig/mesh/fleet-inventory.json` |

v0 in one line: **a det-first workflow engine with schema-gated LLM stages, replay-by-hash, planted-RED gates, and an MCP attach.** The company still runs on 146 Hermes jobs, three other schedulers, four desktop shells, and a knowledge stack that is not the default context for those 24 agents.

What v0 is *not*: a knowledge operating system, a durable HITL loop, an eval factory, a cost-controlled fleet, or a consulting delivery system.

---

## 2. What v2 looks like

Steal the shape the firms actually shipped, not their adjectives.

```
Knowledge OS (Lilli/Sage analog)
    → Intelligence layer owned separately from the model (BCG EnterpriseIQ analog)
        → Domain worker catalog (Zora / AI Refinery analog)
            → Orchestration + governance plane (PwC agent OS analog)
                → Graduated autonomy + eval flywheel + error budgets
```

### v1 bridge (make the engine real)

1. **Kernel** — budgets in every spec (`max_steps`, `max_cost`, `max_duration`); `task` subagents; compaction + notes.
2. **Durability** — every model/tool call is a Temporal journaled activity. Kill -9 mid-run resumes. `seal_proof` under `model=none` is RED today; fix that before claiming durability.
3. **Gate-D = suspend, not abort** — LeafV0: `wait_for_signal` is docstring-only in `engine/temporal_runtime.py`. v1 is a real `@workflow.signal` that parks the run until `APPROVE <run_id>`.
4. **Observability + cost** — `engine/observability.py` exists but export is conditional. Wire OTLP → Langfuse. Cost-per-task on every run record. No run without tokens.
5. **Eval** — per-department end-state task sets; pass^k (k=8); trajectory match; judge audited by Mike. Capability evals that pass graduate into CI.

### v2 flywheel (make the firm real)

6. **Knowledge OS** — Recall 853 + GBrain become Lilli: every workflow stage retrieves before generating. Nightly dreaming cron writes git-backed per-agent memory.
7. **Domain catalog** — 8 RIG verticals get Zora-style *workers* (invoice, lead-score, briefing) not chat personas. Catalog > roster.
8. **One scheduler of record per job class** — 146 Hermes jobs + Prefect + Temporal + Kestra is not robustness. Freeze extras (emergency-freeze doctrine already exists).
9. **One operator shell** — Adler is the cockpit that *calls* Jake workflows. OpenBot / Agent OS / Agency either compose or get killed. Two control planes is how v0 stays v0.
10. **Termination** — Jake cannot mark himself improved. Only the eval harness can. Same rule as JAKE-PAI-V2.md §5, now binding on the firm, not just the kernel.

---

## 3. What top consulting firms are actually doing

Using agent-reach/web (Jina) + first-party pages. McKinsey Lilli long-form timed out; that claim is flagged.

| Firm | What they built | Move to copy | Primary |
|---|---|---|---|
| **McKinsey** | Lilli = internal knowledge OS over 40+ sources; QuantumBlack productizes “agents at scale” for clients | Knowledge OS *first*, client suite *second* | [Lilli](https://www.mckinsey.com/capabilities/mckinsey-digital/how-we-help-clients/rewiring-the-way-mckinsey-works-with-lilli) (fetch timeout 2026-08-30 — snippet only) |
| **BCG** | BCG X product library + **EnterpriseIQ** intelligence layer; 2026 CIO playbook | Own context separately from agents; graduated autonomy; 70% change | [Agentic leadership 2026](https://www.bcg.com/publications/2026/agentic-ai-strategy-cio-cto) |
| **Bain** | Sage internal GPT; Vector for clients; OpenAI/Anthropic/Palantir; claimed 19k custom GPTs | Every employee builds on a platform, not a permission | [Five ways](https://www.bain.com/careers/life-at-bain/careers-blog/five-ways-bain-is-leading-with-ai/) |
| **Deloitte** | **Zora AI** digital workers for finance/tax/HR/IT; FDEs + global delivery; NVIDIA | Domain workers + FDE, not a chatbot | [Zora](https://www.deloitte.com/us/en/services/consulting/services/zora-generative-ai-agent.html) |
| **Accenture** | **AI Refinery** + industry agent catalog (50→100) + no-code builder | Process library you can click, with guardrails | [18 Mar 2025](https://newsroom.accenture.com/news/2025/accenture-expands-ai-refinery-and-launches-new-industry-agent-solutions-to-accelerate-agentic-ai-adoption) |
| **PwC** | **agent OS** = orchestration/governance plane over heterogeneous agents | Nervous system, not another model | [agent OS](https://www.pwc.com/us/en/services/ai/agent-os.html) |

BCG, quoted: “Only 5% of companies are truly agent-first.” “Success with agentic AI implementation is 70% people and change management, not algorithms.” “Keep the core system minimalist… move all the custom logic into the agentic layer.” Graduated autonomy: shadow → supervised → guided → full.

They are not racing to a smarter chat. They are racing to **(1) a knowledge OS, (2) a domain catalog, (3) an orchestration plane, (4) change at the value stream**. RIG already has pieces of (1) and a det engine. It does not have (2)–(4) as the default.

---

## 4. Robustness (fail-closed, not more retries)

| Risk | v0 state | v2 rule |
|---|---|---|
| Green theater | planted RED battery exists; `seal_proof` is live RED | no promote while any skeleton is RED |
| Outward action | Gate-D request/check | Gate-D **suspends** the durable run |
| Crash | Temporal file present; local artifact post-hoc | kill -9 drill is a gate, not a blog |
| Model swap | intelligence mixed into prompts | BCG move: intelligence layer owned; models are sockets |
| Cost blowup | uncosted | budget in spec; burn-rate FREEZE |
| Scheduler chaos | 146 Hermes + Prefect + Temporal + Kestra | one owner per class; freeze the rest |
| Fleet lies | 96GB WEDGED, proxy WEDGED, blackwell DOWN | route only READY; WEDGED ≠ live |
| Two desktops | Adler + OpenBot + Agent OS + Agency | one cockpit |
| Self-scoring | RLM quality_score is self-reported | eval harness is the only improvement authority |

Robust means: **a green that cannot go red is illegal.** That is already doctrine (`rig-adversarial-verification`). v2 is making it the runtime, not a skill.

---

## 5. Formal process that is 1000x — compose, do not slogan

Machinery already on disk (paths verified): IQRSQPI, Gate-D, ProofPacket, doctrine-forge, excellence-ingestion, operator doctrine, TAC closed-loop, adversarial verification, department PAI, Adler receipts, unlazy gates. Leaf1000x found more (SSSF gates, foundry_core, 22-department registry, Recall NOT_READY discipline).

**Do not invent a 9th methodology.** Wire this loop as the only way work ships:

1. **Issue tree** — MECE + named falsifier. Kill: cannot state the decision in one sentence.
2. **Charter** — owner, BMS band, verifier, Gate-D types. Kill: no verifier.
3. **Evidence** — IntelPacket, every number has a path. Kill: unsourced number.
4. **Produce** — Jake workflow or SSSF ADW, planted-RED on every new gate. Kill: green that cannot go red.
5. **Quantify** — repeat n≥3 or honest UNAVAILABLE; cost on the receipt. Kill: self-scored 97.
6. **Knowledge object** — entity page + GBrain + sha256 sidecar. Kill: chat-only residue.
7. **Graduate** — passing capability evals enter CI forever. Kill: one-off heroics.
8. **Cadence** — weekly error-budget + cost Pareto. Kill: no SLO.

Consulting analog: issue tree → workstream → quality gate → knowledge object → reuse. That *is* McKinsey/BCG delivery, minus the deck.

Anti-patterns: more agents without an orchestration plane; new slogans duplicating IQRSQPI; client agents before the internal knowledge OS works; autonomy without tiers; 146 crons; scoring the scorer.

Deviation-engine split (40 vs 42) and missing `Startup-Intelligence-OS` runtime are real composition blockers — fix the registry before preaching ±30σ.

---

## 6. Upgrade all RIG systems + the fleet

Priority is **repair and collapse**, not buy another node.

### Fleet (live probe)

- READY: `local-128gb`, `mimo-8655`, `rig-256gb`, `rig-36gb`
- WEDGED (reachable, unusable): `rig-96gb`, `proxy-8317`
- DOWN: `blackwell`
- Inventory-only, not in live table: 48GB, 28GB, QNAP

Workstreams: unwedge 96GB; restore blackwell or decommission; stop routing through WEDGED; treat inventory-only hosts as **unproven**.

### Systems

| System | Move |
|---|---|
| jake-workflows | Fix `seal_proof`; Temporal journal; Gate-D signal; cost fields |
| 24 specs | Add budgets + eval task set or the spec is a persona, not an employee |
| Hermes 146 | Registry of record; freeze undeclared; one cadence owner |
| Prefect OmniScout | Live watchdog; no stale auto-schedule (already a known gap) |
| Adler | Cockpit over Jake CLI/MCP — do not grow a second engine |
| OpenBot / Agent OS / Agency | Compose or kill |
| Recall / GBrain | Default retrieve-before-generate; dreaming cron |
| Systems Thinking v3 | Stays `STAGED_NOT_PROMOTED` until two-source-class topics exist |
| Department registry (22) | Daily cycle must seal ProofPackets or the department is theater |

### Sequence (90 days, kill criteria on each)

- **Days 1–14:** Fix `seal_proof` RED. Freeze undeclared Hermes jobs. Route only READY nodes. Adler → Jake `workflow_list/run/status` only.
- **Days 15–45:** Temporal journal + Gate-D signal. Cost on receipts. First 3 department eval task sets (Darius, Otto, Steve).
- **Days 46–90:** Knowledge OS retrieve-before-generate. Graduate evals into CI. Error-budget dashboard. Kill or merge one desktop shell.

Kill the whole v2 bet if: (a) `seal_proof` still RED after day 14, (b) WEDGED nodes still receive work, (c) any outward action bypasses Gate-D, (d) Jake self-reports improvement without an eval.

---

## 7. What not to do

- Do not “upgrade to v2” by writing another doctrine file.
- Do not stand up a 25th agent.
- Do not treat JAKE-PAI-V2.md 9✔/8~/13✘ as current — workflow count already drifted 6→21.
- Do not promote Systems Thinking v3 in this tranche.

---

Evidence files: `docs/v2-upgrade/leaf-v0-measured.json`, `leaf-consulting.json`, `leaf-1000x-process.json`, `leaf-fleet.json`.
