---
source: https://www.youtube.com/watch?v=_QAVExf_1uw
video_id: _QAVExf_1uw
channel: AI Engineer
title: "Demand-Driven Context: A Methodology for Coherent Knowledge Bases Through Agent Failure"
scraped: 2026-08-28
tags: [systems-thinking, ai-agents, knowledge-management, context-engineering]
---
# Demand-Driven Context: Coherent Knowledge Bases Through Agent Failure

A conference talk + workshop: grow an enterprise knowledge base by letting coding agents fail against real work items, then curating what the failures reveal.

## Procedure / models distilled
- Framing via *Memento*: agents have ~15-minute memory; every session restarts cold — context is the only durable layer you control (3:05–3:51).
- Three-layer stack: model quality (provider's problem) → retrieval (RAG/MCP, industry's focus) → **institutional knowledge** (nobody's problem) — the layer that actually gates enterprise agents (7:02–7:30, 8:52–9:18).
- Diagnostic pie chart of agent time: ~40% lost to missing/outdated context; the knowledge base is a monolith nobody decomposes (10:24–11:02).
- Core move: break the monolith knowledge base into **context blocks** the way monoliths are broken into microservices (11:02–11:20, 12:19–12:38).
- **Demand-driven cycle** (the workshop's method): assign the agent a real work item → it works from existing context → hits gaps → asks a person targeted questions (the person fills gaps like an expert onboarding a junior) → answers are curated back into the blocks (13:11–15:06).
- TDD analogy: each agent failure is a failed test case; iterate until the knowledge base "passes" — knowledge score climbs cycle over cycle (15:52–16:42).
- Measured result: running the loop across 14 real incidents raised knowledge scores from ~1.4 to the 4.4–5 range; 15+ cycles in, the agent keeps asking productive questions instead of hallucinating (23:00–25:15).
- Role inversion: the agent graduates from knowledge **consumer** to knowledge **manager** — it maintains the base as a side effect of doing work (25:15–25:44).
- **Context gap scanner**: point it at incidents/Jira/cases; it generates probes (little tests per incident), scores the connected knowledge base stale/incomplete/missing, and ranks what to fix first — "knowing the unknown" is the top value (27:11–32:10, 36:30–37:02).
- 80/20 curation: mark the ~20% high-value blocks as always-load; leave the rest as links resolved on demand (39:43–40:05).
- Storage: plain flat files (or JSON) work; a GitHub repo gives versioning, multi-team contribution, and built-in review — agents and experts commit to the same base (23:00–23:16, 33:54–34:29).
- Sizing note: ~96K-token context windows mean curated blocks comfortably fit — quality of context, not window size, is the binding constraint (50:12–51:12).

## Failure modes named
- Fixing retrieval before fixing context: RAG over a stale monolith returns confident garbage (9:18–9:27, 49:06–49:34).
- No evals on the retrieval/context layer — teams ship MCP servers without testing whether they help (8:52–9:10).
- Assuming documentation is complete; the tacit knowledge in people's heads never surfaces unless agent questions force it out (20:58–21:28).
- Hand-curating everything up front instead of letting demand (real work items) select what gets documented (13:20–13:47).
- Doing context repair only after retrieval/at runtime instead of before (50:02–50:35).

## Studio relevance
- ground — feedback-loop discipline for keeping the studio's own knowledge substrate honest: demand selects what gets curated.
