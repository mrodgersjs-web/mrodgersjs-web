---
source: https://www.youtube.com/watch?v=3zSANOIBHYw
video_id: 3zSANOIBHYw
channel: Zen van Riel
title: "The Unbeatable Local AI Coding Workflow (Full 2026 Setup)"
scraped: 2026-08-28
tags: [tools, local ai, coding agents, llm inference]
---
# The Unbeatable Local AI Coding Workflow (Full 2026 Setup)

A walkthrough of running quantized local models through LM Studio, linking them across devices, connecting Claude Code via the Anthropic-compatible API, and using plan mode, large context windows, and sub-agents to build a full-stack app while accepting the speed and accuracy trade-offs of local inference.

## Procedure / models distilled
- Run quantized MoE models (e.g., Qwen 3.5 35B) on a powerful local GPU to hit 100+ tokens/sec for coding tasks.
- Verify the entire model fits in GPU VRAM; spilling parameters to system RAM causes severe, unusable slowdowns.
- Use LM Studio's Link feature to expose a model running on a powerful Linux/Windows machine to a weaker MacBook over an encrypted local connection.
- Connect Claude Code to LM Studio by pointing it at the Anthropic-compatible `/v1/messages` endpoint.
- Override `ANTHROPIC_BASE_URL` and `ANTHROPIC_API_KEY` environment variables so Claude Code routes to the local LM Studio server.
- Increase LM Studio's context window to at least 80k–200k tokens because Claude Code injects a multi-thousand-token system prompt.
- Use plan mode with the local model to decompose a project into concrete spec files before implementation.
- Configure context-overflow behavior (e.g., truncate the middle of conversation history) to keep long sessions usable.
- Run Claude Code inside a dev container with "bypass all permissions" mode for autonomous, hands-off execution.
- Spawn sub-agents for each spec so each task gets a fresh context window, mitigating limited local-model context.
- Give agents direct access to the backend APIs they integrate with so they can self-correct against real response formats.
- Iterate and fix bugs manually because local quantized models are less capable than top-tier cloud models.

## Failure modes named
- Model parameters spilling from GPU VRAM into system RAM crushes inference speed.
- Default 4k token context windows cause Claude Code to hang indefinitely with no clear error message.
- Confusing empty-chat token speed with Claude Code speed; the latter is much slower due to system-prompt bloat.
- The injected system prompt can make the local model misidentify itself (e.g., claim to be Claude Sonnet).
- LLMs hallucinate hard-coded details when specifications are incomplete.
- Expecting local models to match the bug-free performance of state-of-the-art cloud models.

## Studio relevance
04 leverage - how the studio selects and configures local GPU/CLI tooling for private, agentic coding workflows.
