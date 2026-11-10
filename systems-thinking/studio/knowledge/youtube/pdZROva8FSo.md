---
source: https://www.youtube.com/watch?v=pdZROva8FSo
video_id: pdZROva8FSo
channel: LocalM™ Tuts
title: "1.7M Tokens Later: Qwen via vLLM Crushes GPT-5.4 on Complex Code!"
scraped: 2026-08-28
tags: [tools, local llm, qwen, multi-agent]
---
# 1.7M Tokens Later: Qwen via vLLM Crushes GPT-5.4 on Complex Code!

A local Qwen 3.6 27B stack running through vLLM and LiteLLM handled a 1.7M-token, 1.5-hour session to fix complex Next.js dependency issues that GPT-5.4 failed on first attempt, demonstrating a viable hybrid local-plus-premium coding-agent architecture.

## Procedure / models distilled
- Deploy Qwen 3.6 27B dense locally with vLLM as the inference backend.
- Put LiteLLM in front of vLLM as an OpenAI/Anthropic-compatible proxy and endpoint-alias layer.
- Store LiteLLM metadata in PostgreSQL for request tracking, routing, and usage visibility.
- Expose local endpoints through VS Code port forwarding so remote clients and agents can reach them.
- Create model aliases that map Anthropic-style and OpenAI-style client calls onto the same local Qwen backend.
- Tune vLLM for the target hardware by locking context length to 128K tokens and enabling four concurrent worker/agent slots.
- Keep the model in BF16 precision with MTP (multi-token prediction) heads active for higher throughput.
- Use multi-token prediction with MTP=3 to raise aggregate throughput to roughly 560–600 tokens/s and coding acceptance ratios to about 90–92%.
- Split work across multiple local sub-agents/concurrent workers rather than a single long-context call.
- Manage context explicitly with custom skills, prompt hooks, and precise MCP tool selection before invoking the model.
- Validate model-generated changes with local tests before committing; confirm via the CI/CD pipeline run.
- Use the local model for inner-loop coding agents while reserving premium models (Opus 7, GPT-5.4/5.5) for outer orchestration.
- Track token throughput and MTP acceptance rates as the primary local-serving health metrics.

## Failure modes named
- GPT-5.4 with the same three-line prompt failed on the first attempt and would have required additional tweaking.
- A large, tightly coupled monolithic repository with shared submodules can create immensely complex dependency graphs that obscure root causes.
- Feeding the core problem to Qwen without proper prompts, skills, hooks, and MCP context management can cause local models to underperform.
- vLLM is not reliably out-of-the-box for 128K context on this hardware; it required manual configuration tweaks.
- Single-agent local runs may feel slower than a high-memory-bandwidth MacBook if concurrency is not used.
- Relying solely on top-tier cloud models can become economically unsustainable at high token volume.

## Studio relevance
04 leverage - use the vLLM + LiteLLM + Qwen stack and hybrid agent pattern to reduce premium API dependency on complex coding tasks.
