---
source: https://www.youtube.com/watch?v=eieYagEYr3k
video_id: eieYagEYr3k
channel: Andrew
title: "The 6 Principles That Make My OpenClaw AI Agents Think Like a CEO THINKING md"
scraped: 2026-08-28
tags: [systems-thinking, ai-agents, decision-frameworks, agent-operations]
---
# The 6 Principles That Make My OpenClaw AI Agents Think Like a CEO (thinking.md)

An operator's method for programming decision-making — not prompts — into a fleet of 11 business agents via a thinking.md file.

## Procedure / models distilled
- Diagnosis: untrained agents decide like first-day interns — first idea wins, symptoms get patched, every task weighted equally (0:02–1:25); the fix is not better prompts but a programmed decision framework (4:05–4:21).
- Delivery mechanism: write the six principles once into a `thinking.md` per agent, loaded every session **and reloaded after every context compaction**, with `agents.md` carrying a rule that forces consultation before any significant decision (3:00–3:14, 13:16–13:42, 15:06–15:13).
- **P1 — map all options first**: before recommending anything, enumerate every option, evaluate each on effectiveness / efficiency / sustainability, present the best path with explicit tradeoffs and the rejected alternatives; tiebreak rule: when effectiveness and efficiency conflict, effectiveness always wins (4:32–5:35).
- **P2 — fix root causes, not symptoms** (break-fix protocol): peel layers until the actual root cause, ask "what else did this break?", fix the root, then sweep the whole system for the same gap (5:38–6:23). Worked example: daily "API timeout" → layer 2: too many concurrent Slack channels → layer 3: agent polling 65 channels every cycle → root: the architecture itself; fixing it surfaced three other agents with the same polling waste (6:23–7:08).
- **P3 — priority filter**: rank by system/infrastructure health first, client-facing operations second, internal third; meta-rule: whatever consistently eats the owner's time is top priority regardless of category (7:09–8:04).
- **P4 — resource philosophy (protect the base)**: automation exists to return the owner's finite time/energy/headspace to revenue-generating work; the agent's question shifts from "what's broken?" to "what is costing the owner the most time?" (8:46–9:49).
- **P5 — the done standard**: done = the owner never has to think about it again; validation test: can it run one full week unattended? If not, the agent reports why and proposes fixes (9:51–11:21).
- **P6 — input over output**: debug forward through the input chain step by step instead of patching bad outputs — perfect input guarantees output; example: booking bug traced to step 2 (availability parsing of "after 9:30") before it ever became a bad booking (11:28–13:11).
- File format: six H2 headers; under each, the rule in plain English + the reason behind it + the test the agent runs when applying it (14:37–14:53).
- Consistency is the point: same six principles, same structure, same standards across all agents in the operation (14:22–14:31).

## Failure modes named
- Shipping the first plausible idea without enumerating alternatives (0:51–0:59, 4:36–4:44).
- Fixing the same bug three ways across three sessions — patching symptoms while the root cause persists (1:00–1:08, 2:04–2:31).
- Treating every task/failure as equally important (1:13–1:19).
- Declaring done at "built it, seems to work" — halfway done (10:02–10:11).
- Reactive output-watching that keeps the agent one step behind (11:32–11:46).
- Writing thinking.md once and never referencing it again — principles become decoration (15:50–16:04).

## Studio relevance
- leverage — encoding decision rules into the acting system so interventions persist without supervision.
