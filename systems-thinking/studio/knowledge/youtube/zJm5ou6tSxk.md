---
source: https://www.youtube.com/watch?v=zJm5ou6tSxk
video_id: zJm5ou6tSxk
channel: PyCon US
title: "Building AI Applications the Pydantic Way (Sponsor: Pydantic)"
scraped: 2026-08-28
tags: [engineering, pydantic, ai-agents, type-safety, observability]
---
# Building AI Applications the Pydantic Way (Sponsor: Pydantic)

Samuel Colvin argues that building reliable, scalable GenAI applications requires treating LLMs as untrusted external services and wrapping them in type-safe contracts, validation feedback loops, and observable telemetry rather than betting on model intelligence alone.

## Procedure / models distilled
- Treat the LLM as a boundary where type safety matters most: declare expected inputs/outputs as Pydantic models so the type checker (and AI agents coding for you) can verify call sites before runtime.
- Define an agent as a loop that reads an environment, exposes tools, runs an LLM on instructions, calls tools, updates state, and decides whether to stop—using the Anthropic/OpenAI/Google definition.
- Use Pydantic validators on output models so validation failures are automatically fed back into the LLM as retry context, closing an agentic loop without hand-written branching.
- Instrument every agent run with an observability tool (e.g., Logfire) so each LLM call, validation failure, retry, latency, and token/cost is visible in a trace.
- Prefer model-agnostic agent frameworks so you can switch providers or models in one line and compare behavior, cost, and latency under the same typed contract.
- Make structured output explicit by setting an agent `output_type`; under the hood this registers a `final_result` tool that the model must call to terminate the run.
- Separate the agent orchestration layer from direct LLM calls—use a direct, un-orchestrated LLM interface when you only need model abstraction, not the full agent loop.
- Design MCP (Model Context Protocol) interactions as server-provided tools plus the ability for the server to ask the client to proxy LLM requests, with careful control over which tools are registered per step.
- Use self-hosted or custom models by implementing the framework's model abstract base class or pointing an OpenAI-compatible client at your own endpoint.
- Keep async as the default execution model and add thin synchronous wrappers only where needed, being aware that thread-heavy sync contexts (e.g., Celery) can conflict with async runtimes.
- Build documentation where every code example is unit-tested and its output is programmatically generated, so examples stay correct and imports are complete.
- Approach eval/observability as first-class concerns, not afterthoughts: you cannot improve what you cannot trace, and you cannot trust what you cannot validate.

## Failure modes named
- Non-type-safe agent frameworks forfeit static analysis help, making both human developers and AI coding agents more likely to ship broken integration code.
- The "while True" agent loop has no guaranteed exit condition; knowing when the agent is done is a genuinely hard and still-partially-undefined problem.
- GenAI is unreliable and hard to work with—treating it as a magic component rather than a validated service increases fragility.
- Models sometimes return near-JSON formats (e.g., JSON5) instead of strict JSON, so parsers that assume perfect schema conformance can fail.
- Extracting entities with a large or ambiguous search space can produce incorrect or hallucinated values if validation only relies on the LLM's response.
- Documentation for rapidly changing AI libraries often becomes outdated or wrong, eroding trust and slowing adoption.

## Studio relevance
04 leverage - how the studio uses this card
