---
source: https://www.youtube.com/watch?v=7wwWRph3Jls
video_id: 7wwWRph3Jls
channel: Latent Space
title: "Agent Engineering with Pydantic + Graphs — with Samuel Colvin, CEO of Pydantic Logfire"
scraped: 2026-08-28
tags: [ai-agents, pydantic, python-ecosystem, observability, structured-output]
---
# Agent Engineering with Pydantic + Graphs — with Samuel Colvin, CEO of Pydantic Logfire

Samuel Colvin explains how Pydantic’s validation and schema generation became foundational for LLM structured outputs, why Pydantic AI prioritizes production-grade engineering over framework hype, and how disciplined documentation, browser-based demos, and observability reduce adoption friction.

## Procedure / models distilled
- Treat Pydantic as a typed schema, validation, and coercion layer that also generates JSON Schema, making it the single source of truth for LLM structured outputs and tool definitions.
- Choose strict mode when you need pure validation without coercion; leave coercion on by default to robustly parse loosely typed inputs.
- Optimize validation-to-serialization hot paths by keeping validated data in Rust-backed types instead of round-tripping through Python objects.
- Model agents as composable primitives (system prompt + tools + structured return type) rather than as monolithic black-box frameworks.
- Prioritize production readiness over toy-framework ergonomics by enforcing type checking, test coverage, linting, and runnable documentation.
- Make every documentation example a real test that asserts exact output, so docs cannot drift from the implementation.
- Reduce evaluator friction by letting users run examples directly in the browser against live models instead of forcing a local dev-environment setup.
- Treat observability as a first-class, general-purpose product while keeping foundational libraries open source.
- Continuously extract and execute code from docstrings and Markdown docs to keep examples up to date, linted, and type-checked.
- Use repeated customer pain across roughly 10–20 in-person conversations as the signal for what to build, rather than relying on social-media volume.
- Guard engineering time against the gravity of events and networking, because the failure mode is becoming a scene personality who stops shipping code.
- Replace Jupyter notebooks with text-based, deterministic notebook successors or plain scripts when reproducibility and LLM-friendliness matter.

## Failure modes named
- Agent frameworks shipping with engineering quality far below the broader Python ecosystem, lacking type checking, tests, coverage, and linting.
- Opportunistic AI frameworks from otherwise respected names that ride the hype cycle without production discipline.
- Documentation examples going stale because they are not automatically executed and verified against current code.
- User drop-off during evaluation when the tool requires opening a local editor, installing dependencies, and managing API tokens.
- Jupyter notebooks producing non-reproducible state, encouraging out-of-order execution, and being poor input for LLMs.
- Treating Pydantic as “only validation” while ignoring its default coercion behavior and subtle conversion semantics.
- Mistaking strident Twitter or LinkedIn opinions for real production signal, since early learners and serious operators can sound equally confident.
- Hiring too quickly and burning runway before commercial traction justifies the cost.

## Studio relevance
04 leverage - how the studio uses this card to choose production-grade validation, agent primitives, tested documentation, and observability practices when building observable AI systems.
