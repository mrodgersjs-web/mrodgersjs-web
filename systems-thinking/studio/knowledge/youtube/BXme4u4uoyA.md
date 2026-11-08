---
source: https://www.youtube.com/watch?v=BXme4u4uoyA
video_id: BXme4u4uoyA
channel: Better Stack
title: "I Cut My AI Agent Costs 70% With One Change (Manifest)"
scraped: 2026-08-28
tags: [ai-agents, cost-optimization, model-routing, llm-infrastructure]
---
# I Cut My AI Agent Costs 70% With One Change (Manifest)

Manifest is a self-hosted LLM gateway that intercepts agent requests, scores them across 23 dimensions using deterministic routing, and sends each request to the cheapest capable model—cutting token costs by up to 70% without changing agent code.

## Procedure / models distilled
- Model over-provisioning inflates agent bills because simple calls such as tool selection, classification, and summaries are often sent to expensive frontier models.
- Manifest sits between the agent and provider endpoints as a local gateway with a single OpenAI-compatible endpoint.
- Deploy it with Docker using `docker compose up` and point the existing OpenAI SDK base URL to the Manifest instance.
- Provider keys are configured once inside Manifest; the agent only needs a Manifest API key.
- Routing decisions are made by deterministic scoring across 23 dimensions, not by another LLM, keeping overhead under 2 milliseconds.
- Each request is routed to the cheapest model capable of handling it, including paid APIs, local Ollama/Llama.cpp, or existing subscription models.
- The built-in dashboard tracks token usage, cost per agent, and budgets in real time.
- Multi-agent workflows, plugin support, and observability are included out of the box.
- Existing clients work without rewrites because Manifest uses the standard OpenAI API shape.
- Routing requests through existing subscription services converts per-token spend into already-paid usage.
- Automatic fallbacks keep agents running when a chosen provider or model fails.
- Manual overrides are available when the deterministic scorer routes requests cheaper than desired.

## Failure modes named
- Sending every agent call to the most capable model makes the bill 3-5× higher than necessary.
- Hand-coded if/else routing logic breaks as soon as prompts or tasks change.
- Using Open Router adds fees and sends prompts outside your machine.
- LiteLLM unifies interfaces but still leaves routing decisions manual.
- Routing via another LLM adds latency and cost, defeating the purpose.
- Paying per token for models when you already have a subscription is double-paying.
- Not monitoring cost per agent, model, or task hides where the money goes.
- Expecting zero setup will lead you to pick a simpler cloud router like Open Router instead.
- Opinionated scoring can route requests to cheaper models than expected unless you override it.

## Studio relevance
04 leverage - use Manifest as a drop-in routing gateway to reduce recurring per-token costs while keeping existing agent logic unchanged.
