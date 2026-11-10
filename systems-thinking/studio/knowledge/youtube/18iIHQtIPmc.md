---
source: https://www.youtube.com/watch?v=18iIHQtIPmc
video_id: 18iIHQtIPmc
channel: Mastra
title: "4 Levels of Agent Memory Explained by a Senior AI Engineer"
scraped: 2026-08-28
tags: [ai-agents, agent-memory, llm-context, rag]
---
# 4 Levels of Agent Memory Explained by a Senior AI Engineer

The video walks through four agent memory systems—conversation history, working memory, semantic recall, and observational memory—and how each trades off context limits, recall precision, latency, and long-horizon coherence.

## Procedure / models distilled
- Store short-term continuity by appending prior conversation turns to each LLM request, and cap the window before it exceeds context limits.
- Add working memory as a system-prompt scratchpad with predefined empty fields and an update tool so the agent captures stable facts and preferences across a long single thread.
- Implement semantic recall by embedding every user/agent message into a vector store and retrieving top-K semantically similar messages (plus a surrounding message range) to inject relevant history.
- Build observational memory with an observer agent that triggers when conversation tokens cross a threshold and rewrites messages into dense observations annotated with priority and timestamps.
- Add a reflector agent that compresses older observation blocks once the observations window crosses its own threshold, cycling repeatedly as the conversation grows.
- Run observer/reflector agents asynchronously and non-blocking in the background to avoid interrupting the user flow.
- Keep observation prompts stable across turns so prompt prefixes remain cacheable, unlike dynamic semantic-recall prefixes.
- Tune semantic-recall parameters (top-K and message range) to balance between overwhelming the model with too much context and omitting needed context.
- Benchmark memory systems against Long Mem Eval to measure recall, contradiction handling, and temporal reasoning under fair model conditions.
- Choose the memory level by task horizon: conversation history for brief chats, working memory for stable key-value facts, semantic recall for long histories with cross-thread lookup, and observational memory for noisy tool outputs and very long sessions.
- Use observational memory to strip irrelevant detail from large tool-call responses while preserving the sliver needed for the current goal.

## Failure modes named
- Naive conversation history hits context-window limits, causes context drift, and resets memory for every new thread.
- Working memory cannot store much data or long-term history, and forcing predefined fields makes the agent less autonomous.
- Semantic recall is imprecise and can miss exact matches, while adding embedders/vector stores introduces moving parts, cost, and latency.
- A dynamically changing semantic-recall system prompt prevents stable prompt prefixes, eliminating input-token cache savings.
- Retrieving too much context can overwhelm the model, while retrieving too little leaves out needed information.
- Synchronous compaction (e.g., Claude Code) can drop important information and block the user flow.
- Observational memory still eventually runs out of context, only far more slowly than the other levels.

## Studio relevance
04 leverage - use the four memory levels as a decision ladder for balancing context limits, recall precision, latency, and cacheability in long-horizon agent designs.
