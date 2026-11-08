---
source: https://www.youtube.com/watch?v=5ID22ACI7IM
video_id: 5ID22ACI7IM
channel: AI Engineer
title: "Mergeable by default: Building the context engine to save time and tokens — Peter Werry, Unblocked"
scraped: 2026-08-28
tags: [tools, ai agents, context engineering, knowledge graphs]
---
# Mergeable by default: Building the context engine to save time and tokens — Peter Werry, Unblocked

Peter Werry argues that moving beyond human-managed agents requires a context engine that captures organizational experience, trust, and historical motivation—not just documents or long context windows—and shows how Unblocked uses an incremental social/experts graph to cut task time and token use.

## Procedure / models distilled
- Define a context engine as a system that supplies an agent with exactly the context it needs and none it doesn’t, shaped by organizational history and best practices.
- Treat organizational context as accumulated experiential knowledge—incidents, mentors, pain, and the reasons behind historical decisions—rather than static documents.
- Build an incremental experts/social graph that maps who knows what and who owns what, weighting its edges by trust and feedback over time.
- Seed agents with pre-hydrated context instead of letting them retrieve and hydrate memories on their own.
- Personalize retrieval to the task, team, and repo to avoid cross-org noise, conflicting information, and irrelevant code.
- Capture user feedback on context quality and distill it into weighted task memories, amplifying corrections from trusted experts and damping noise from unvetted sources.
- Prioritize correctness over retrieval latency; high-quality up-front context shrinks implementation loops far more than fast tool calls.
- Benchmark success by sentiment and workflow outcomes—fewer doom loops, shorter PR cycles—rather than traditional coding benchmarks.
- Update integration data incrementally and in near-real time where possible; rebuild social graphs only as needed because they are relatively stable.
- Refresh best-practices memory at a slower cadence because organizational norms change slowly.
- Preserve legacy context and backwards-compatibility signals, especially when changes affect downstream consumers.

## Failure modes named
- Satisfaction of search: agents loop through searches, burn tokens, and may hit context compaction without reaching the endgame.
- Doom loops: agents repeatedly produce wrong outputs, forcing human correction cycles that inflate wall-clock time and token spend.
- Access mistaken for understanding: wiring MCP servers or RAG without modeling relationships, history, and motivations produces shallow results.
- Naive RAG over docs: vector search alone ignores conflicts, task relevance, personalization, and org-scale noise.
- Long-context window fallacy: bigger windows help needle-in-haystack retrieval but not cross-source reasoning or true understanding.
- Clobbering legacy code: agents without historical context make changes that break existing consumers or backwards compatibility.
- Overweighting unvetted feedback: corrections from untrusted sources should not be distilled into memory with the same weight as expert corrections.

## Studio relevance
02 frame - the studio uses this card to frame agentic context as an organizational-knowledge design problem rather than a retrieval, prompt-engineering, or bigger-context-window problem.
