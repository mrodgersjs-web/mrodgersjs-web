# Jake PAI Prime — Recall knowledge index

Operating knowledge for **Jake PAI Prime’s 23-agent fleet**.

This index is the fleet’s map of Mike’s Recall.it library: **853 cards**, tagged into a **fixed 17-word vocabulary**, with **nine CORE domain packs** a working studio can load without rereading the corpus. It is not a dump of titles. It is the operator surface: who owns which domain, which numbers and gates actually ship, and which five cards to load first.

---

## How tags were produced

- **Fixed vocabulary only.** CORE: `systems-thinking`, `psychology`, `startup`, `founder`, `growth`, `linkedin`, `sales`, `gtm`, `tools`. EXTENDED: `ai-agents`, `marketing`, `content`, `productivity`, `strategy`, `engineering`, `finance`, `other`.
- **1–3 tags per card.** Prefer CORE. Use EXTENDED to keep `other` small (it is **39**). `tools` means named software / CLIs / workflows a working agent could adopt. Multi-tag honestly (a LinkedIn growth funnel is `linkedin` + `growth`).
- Six parallel batch taggers wrote `tags/batch-01.out.jsonl` … `batch-06.out.jsonl`. The deterministic merge gate (`recall_merge_tags.py`) verified **853/853**, then wrote `card-index.json` and `by-domain/<tag>.json`.
- **Tags live in this repo because the Recall API is read-only.** Never attempt writes to `backend.getrecall.ai`. The live KB is still searchable; the *classification* is versioned here.

---

## Live access

```bash
python3 scripts/recall_api.py search "<q>" exhaustive
python3 scripts/recall_api.py card <card_id> "<focus query>" 50
python3 scripts/recall_api.py status
```

In the destination repo the client is `scripts/recall_api.py`. The tagged index is `knowledge/recall/card-index.json`. Domain spines are `knowledge/recall/by-domain/<tag>.json`. Packs are `knowledge/recall/domains/<domain>.md`.

---

## Inventory (computed from `card-index.json` + `by-domain/*.json`)

| Metric | Value |
|---|---|
| Unique cards | **853** |
| Tag assignments | **1747** |
| Average tags / card | **2.05** (1747 ÷ 853 = 2.048…) |
| Cards with `mirror_path` | **566 / 853 (66.35%)** |
| `other` (kept small) | **39** |
| Merge gate | **VERIFIED 853/853** |

### Full 17-tag counts

| Tag | Kind | Cards |
|---|---|---:|
| tools | CORE | 436 |
| engineering | EXTENDED | 373 |
| ai-agents | EXTENDED | 282 |
| systems-thinking | CORE | 122 |
| psychology | CORE | 93 |
| strategy | EXTENDED | 91 |
| gtm | CORE | 58 |
| productivity | EXTENDED | 45 |
| other | EXTENDED | 39 |
| linkedin | CORE | 36 |
| content | EXTENDED | 36 |
| startup | CORE | 31 |
| marketing | EXTENDED | 30 |
| sales | CORE | 26 |
| growth | CORE | 23 |
| finance | EXTENDED | 13 |
| founder | CORE | 13 |

Counts match both `card-index.json` (union of tags) and every `by-domain/<tag>.json` `count` field. A card can appear in more than one domain.

---

## CORE domain packs

Nine packs this run. Takeaways are specific atoms from the pack (numbers, named tactics, gates) — not slogans.

| Domain | Pack file | Cards tagged | Top 5 takeaways | Owning agent |
|---|---|---:|---|---|
| systems-thinking | `domains/systems-thinking.md` | 122 | 1. **Ralph loop** = while-loop around a prompt until it ships; point it at a *pile of work*; ~3-day sessions; 200 PRs into a monthly release means review/release is the constraint, not coding. 2. **Robust-MAD-Z** = `0.6745 × (score − median) / rawMAD`; do **not** also multiply `1.4826`; ship only statistically deviant work. 3. **Feynman X-Ray:** MeaningPreservation `< 0.80` or SimplicityGain `< 0.25` → block; `robust-MAD-Z < 3` does not ship. 4. **Information Gap Score** = Forecast Importance × Current Uncertainty × Expected Probability Shift × Actionability ÷ Collection Cost; Brier `BS = (1/N) Σ (pᵢ − oᵢ)²`. 5. Gymreapers **$0 → $100M**: Operations = McDonald’s SOPs (V1/V2/V3); Growth = OKRs; daily Slack numbers *with insight* (mobile conversion −2% is an action); founder **10-80-10**. | `/iris` (Strategy Studio) |
| psychology | `domains/psychology.md` | 93 | 1. Prospect theory: `λ ≈ 2.25`, `α ≈ β ≈ 0.88`, `γ ≈ 0.65`; losses hurt ~**2.25×** equivalent gains. 2. Implementation intentions: goal setters fail **62%**, if-then planners fail **9%**. 3. Gatekeeper + Carpenter 2013 (**42** studies): “but you are free to refuse” *increases* compliance; Fogg `B = MAP`. 4. Reactance `R ∝ FreedomImportance × ThreatMagnitude × FrequencyOfThreat`; restricted desire `= free × (1 + R)`. 5. **PsyShield / HumanOS**: Bias Firewall + Reality Compass; next 10× is protection against *bad conclusions*, not more information. | `/jake` (Prime Conductor) — cross-fleet |
| startup | `domains/startup.md` | 31 | 1. Lean Canvas: “**$10,000 MRR by month 6**” is a metric; “increase revenue” is not; litmus = **10** early adopters you can call next week. 2. Hormozi five advantages: **sticky, high gross margin, expanding market, operationally easy / low capex, unique/moat**; if none, fix retention first. 3. AI wedge in 3 sentences (constraint → mechanism Y → pricing Z breaks); **Harvey $200M ARR in 4 years** selling the legal *deliverable*. 4. Karpathy **3.0**: LLM is the computer, prompt is the code, context window is the lever; strip UI and ship `llm.txt`. 5. Unfair advantage: wrappers are rented land; write **“none yet”** rather than “passionate team / innovative tech.” | `/opal` (Product Studio) |
| founder | `domains/founder.md` | 13 | 1. Gymreapers **10-80-10** still used at **~150 people**; star craftspeople do not own SOPs (Asana + Notion). 2. Hormozi onboarding: month-1 churn **>20%**, next cliff **~10% at month 3**, last big drop **month 6**; job is first 30 days → month 3 → month 6. 3. Fat margin: **$100M @ 10% GM** vs **$20M @ 50% GM** — 5× incremental EBITDA per dollar. 4. YC: sell the *hired employee*, not the dashboard; recruitment SaaS **$15–$100/mo** vs placement **$5k–$15k**; software-like agency **70–90%** margin. 5. Do not sell n8n bricks — sell the **bridge** (leads → booked calendar); **$15k–$25k** Meta ads + AI caller vs $45–$50 Fiverr gigs. | `/opal` (Product Studio) |
| growth | `domains/growth.md` | 23 | 1. A LinkedIn artifact is a **distribution package**, not a post; v5 gate: **MiroFish ≥ 85 AND Distribution Score ≥ 145 AND Manipulation Risk ≤ 35** (145–170 ship / `<120` do not publish). 2. **MentionFish**: 52–60 priority / 42–51 use / 32–41 reply-only / `<32` do not mention; if you tag **7** and **0** respond, the mention strategy failed. 3. First **90 minutes** decide live vs dead; comments weighted **15×** likes; dwell **≥ 60s**; T−30 = **10 Tier-1 DMs** ready. 4. **DM-50 + Tag-20**: 4 waves × 5 tags over 6 hours; DMs **10 / 15 / 15 / 10 = 50**. 5. Early-user stack: mini-tools **10×** free trials; 2/20/200 validation; **23%** more trial signups after paywall redesign; one blurry background = **94%** more conversions. | `/opal` (Product Studio) |
| linkedin | `domains/linkedin.md` | 36 | 1. Decision window **5–15 seconds**; distribution decided in the first **90 minutes**; **LPS ≥ 65/100**; native documents **7.00%** ER vs link posts **~3.25%**. 2. Nothing ships as a naked post — **14-artifact** package (first comment, mention graph, reply bank, 90-min plan, …). 3. Gates: `HookRupture ≥ 0.70`, `DepthScore ≥ 0.80`, `PredictedLinkedInV2Success ≥ 0.85`, `SwarmConsensus ≥ 0.65`, flagship `RobustMADZ ≥ 8.0`. 4. **Tag-20 / DM-50**: main post **0–2** mentions, first comment **2–5**; stagger tags (LinkedIn throttle **~30** mentions); Wave-1 tagged reply **≥2 of 5** within 90 min. 5. Hermes may **draft** and **schedule only after approval**; may **not** mass-comment / mass-DM; banned copy includes “Would love your thoughts” / “Just checking in.” | `/ralph` (LinkedIn Studio) |
| sales | `domains/sales.md` | 26 | 1. Weekly **LAPS** (Leads, Appointments, Presentations, Sales); pitch = **Name, Same, Fame, Pain, Aim, Game**; of every **12** leads, **< half** book. 2. `Sales Velocity = (Qualified Opps × ACV × Win Rate) ÷ Cycle`; RI rewrite uses **Days from First Contact to Signed Sprint**. 3. Sequence **insights → method → solution** (never product-first); follow-up can **double** the business; peak window = first **48 hours**; **≥7** touches; Monday 10:00 lead → follow up **10:01**. 4. Reply arc **Wound → Mirror → Autonomy → Qualification → Open Loop**; rewrite if WoundIdentification `< 0.6`; `CustomerFacingArtifactScore < 82` blocks. 5. Website is a **qualification machine**; CTA = Apply for Access / Diagnose the Pattern — not “book a call” + testimonial carousel. | `/darius-jr` (Sales Studio) |
| gtm | `domains/gtm.md` | 58 | 1. GTM is a **qualification machine**, not a funnel; `AntiGenericForce < 80` is a hard BLOCK; `VoltageReactorMADZ < 3.0` blocks the offer. 2. ICP Fit Score (Manual Workflow **0.18**, AI Urgency **0.15**, …): **≥ 8.0** Tier 1; **< 5.0** avoid. 3. Ship only if `CustomerFacingArtifactScore ≥ 82` **and** AntiGenericForce ≥ 80, IdentityForce ≥ 75, RIGSignature ≥ 75, ArtifactCompleteness ≥ 80. Kill test: “Could any AI automation agency have made this?” 4. Ladder economics: Audit→Sprint→Retainer LTV:CAC **> 3.0**; PE/enterprise **> 5.0**. 5. Sell outcomes: **$2,500/mo for ~15 qualified calls** (600 leads processed `< $30`); AI video ads **$1.5k–$5k**; beginner package **$5k–$10k** for the Meta-ads + AI-caller *bridge*, not n8n bricks. | `/darius` (GTM Studio) |
| tools | `domains/tools.md` | 436 | 1. Default runtime: **Hermes Agent** (slash-command registry + skills) + Mission Control org chart; OpenClaw for hands; AionUi as one desktop. 2. **Claude Code as a business OS**: `CLAUDE.md` + `.mcp.json`; score = hours-saved/week × pain(1–10); proposal writing **4h × 9 = 36** ships first; **STOP for approval**. 3. **Unblocked context engine**: same task **2.5 hours / 21M tokens** → **25 minutes / 10M tokens** (~50% token drop, ~6× wall-clock) because it stops doom-loops. 4. Inner/outer split: outer Opus/GPT-5.x, inner **Qwen 3.6 via vLLM** — **~75% fewer** premium tokens. 5. Memory: **Memori** LoCoMo **81.95%** at **1,294 tokens/query** = **4.97%** of full-context; mattpocock **caveman ~75%** fewer tokens; Cole Medin `local-ai-packaged` for n8n + Open WebUI + Ollama/Qdrant. | `/jake` (Prime Conductor) — cross-fleet |

---

## EXTENDED tags (no full pack this run)

These counts are real and queryable via `by-domain/<tag>.json`. Full markdown packs were **not** built for them in this run.

| Tag | Cards | Owner (even without a pack) |
|---|---:|---|
| ai-agents | 282 | `/jake` (cross-fleet; overlaps heavily with `tools`) |
| engineering | 373 | `/jake` (cross-fleet; overlaps heavily with `tools`) |
| strategy | 91 | `/iris` (Strategy Studio) |
| productivity | 45 | `/jake` |
| content | 36 | `/steve` (Content Studio) |
| marketing | 30 | `/darius` / `/steve` as the work dictates |
| finance | 13 | `/opal` / `/darius` as the work dictates |
| other | 39 | leftover by design — do not grow this bucket |

`strategy` is still owned by `/iris`. `content` is still owned by `/steve`. If a later run adds packs, write `domains/strategy.md` and `domains/content.md` against the existing JSON spines — do not retag.

---

## Pointers (this tree)

| Artifact | Path |
|---|---|
| Tagged index | `outputs/card-index.json` (repo dest: `knowledge/recall/card-index.json`) |
| Per-tag spines | `outputs/by-domain/<tag>.json` (17 files) |
| CORE packs | `outputs/domains/<domain>.md` (9 files) |
| Batch tagger output | `outputs/tags/batch-01.out.jsonl` … `batch-06.out.jsonl` |
| Batch inputs (copy) | `outputs/tags/input/batch-*.jsonl` |
| Inventory + mirror join | `outputs/raw/all-cards.json`, `outputs/raw/mirror-join.json` |
| Domain search dumps | `outputs/raw/<domain>-search.json` (and `psych-s1.json` … `psych-s4.json`, `sales-cards.json`, `tools-search.json`, …) |
| Merge gate | `recall_merge_tags.py` (prints `VERIFIED 853/853`) |
| Read-only API client | `scripts/recall_api.py` in the destination repo; sandbox copy lives next to this tree |

---

## Five highest-value cards fleet-wide

Load these first. Titles and URLs checked against `outputs/card-index.json` (empty `source_url` is shown as such — not invented).

1. **[GTM Mathematical Formula Stack — Rodgers Intelligence Implementation Card](https://www.gtmengineerclub.com/guides/gtm-strategy/)** — `gtm` + `sales` + `strategy`. ICP Fit Score, sales velocity, pipeline coverage, Audit→Sprint→Retainer LTV:CAC **> 3.0**. The GTM/sales math every `/darius` and `/darius-jr` run should score against. (Doctrine companions: *RIG OS Go-To-Market Doctrine V2/V3* — same index; V2/V3 `source_url` is empty in the card index.)
2. **[25 Years of Sales Knowledge in 34 Minutes](https://www.youtube.com/watch?v=tVLnzcoM5LE)** — `sales` + `gtm`. Weekly **LAPS**; Name-Same-Fame-Pain-Aim-Game; insights → method → solution; follow-up in **1 minute**, **≥7** touches, first **48 hours**.
3. **[Mergeable by default: Building the context engine to save time and tokens — Peter Werry, Unblocked](https://www.youtube.com/watch?v=5ID22ACI7IM)** — `tools` + `engineering`. **21M tokens / 2.5 h → 10M tokens / 25 min**. Distill, do not just retrieve. The fleet’s context-engine benchmark.
4. **[Hermes Agent Master Cheat Sheet — Complete Slash Command Registry, Skill Catalog, Super Hermes Prisms, Design Libraries, and Global Capability Prompt](https://github.com/NousResearch/hermes-agent)** — `ai-agents` + `tools`. Default CLI/runtime for the 23-agent fleet (pair with *Claude Code AI Business Operating System* at `https://www.mindstudio.ai/blog/connect-claude-code-notion-gmail-mcp-servers/` when the job is a company OS, not a coding session).
5. **[What Makes The Perfect Business (5 Things)](https://www.youtube.com/watch?v=3fsJFUvA6Ts)** — `startup` + `founder` + `strategy`. Hormozi’s five advantages + onboarding cliffs (month 1 / 3 / 6). Companion operating system: *[Business is hard until you build systems like this](https://www.youtube.com/watch?v=4tV_jwspQAs)* (Gymreapers **10-80-10**).

LinkedIn operators should *also* load **LinkedIn 90-Minute Window Strategy** and **Deviant Doctrine DM-50 & Tag-20 Distribution Playbook** from `by-domain/linkedin.json` (both titles verified in `card-index.json`; both currently have empty `source_url` — cite the card, do not invent a link).

---

*Generated from the Stage B merge (`VERIFIED 853/853`) and the nine Stage C CORE packs. Counts were computed from JSON, not estimated.*
