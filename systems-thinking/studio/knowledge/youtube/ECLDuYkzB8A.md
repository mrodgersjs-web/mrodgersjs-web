---
source: https://www.youtube.com/watch?v=ECLDuYkzB8A
video_id: ECLDuYkzB8A
channel: Hak
title: "20-year-old approach more relevant now for building with AI"
scraped: 2026-08-28
tags: [engineering, domain-driven-design, ai-coding, systems-thinking, software-architecture]
---
# 20-year-old approach more relevant now for building with AI

Domain-Driven Design's three core artifacts—a shared language, bounded contexts, and explicit contracts—become essential disciplines for AI-assisted building because every coding session starts with no memory of prior shared understanding.

## Procedure / models distilled
- Treat Domain-Driven Design as a lightweight blueprinting method rather than a heavyweight framework; extract only the artifacts that create shared understanding between you and the AI.
- Build a ubiquitous-language glossary: define every important domain term in a single, unambiguous sentence (e.g., "a change is a persistent set of DOM mutations applied to a customer's website").
- Map the system into bounded contexts—distinct rooms with their own rules and data—so the AI only needs to load the relevant slice instead of reasoning across the whole codebase.
- Document contracts at every boundary where contexts touch, recording dependencies so "what breaks if I delete this?" is always answerable.
- Start each AI coding session by anchoring the agent in the glossary, the current bounded context, and any contracts it touches rather than prompting from a blank slate.
- Adopt a slow-down discipline for architecture, contracts, data models, and anything future-you or future-AI will need to read; update artifacts immediately when the domain changes.
- Reuse old-school engineering artifacts with renewed urgency: PRDs for what/why, ADRs for decision rationale, and TDD for defining behavior before code generation.
- Act as the conductor, not the instrument: steer, read diffs, push back, and own architectural decisions instead of letting an agent ship without human judgment.
- Slice work so each AI interaction stays inside one bounded context; avoid asking the AI to reason across the whole monolith at once.
- Review generated code against the domain glossary and contracts to catch cases where the AI used the right name for the wrong concept.

## Failure modes named
- The speed trap / AI honeymoon phase: continuously adding features without a proper blueprint until the system becomes unshippable around month 5-6.
- Missing shared vocabulary between human and AI, causing the agent to guess the meaning of domain terms.
- Building the wrong thing with the right name: generated code looks correct but implements an unintended concept.
- Knowledge-gap drift: AI appears strongest where you know least, using your blind spots as free space to produce incorrect code.
- Cross-session amnesia: AI does not remember previous decisions across sessions or agents, so undocumented rationale disappears.
- Burning tokens and context chasing bugs that nobody on the team remembers writing.
- Misalignment bugs stemming from poor communication rather than bad code.
- Overengineered DDD: creating dozens of bounded contexts and nested layers nobody can navigate, replacing substance with structure.
- One-shot prompting and shipping fast for parts that actually need architectural discipline.
- Letting agents write 100% of the code without steering, reading, or pushing back.
- Vibe-coded slop: low-quality output that lacks craft and shared understanding.

## Studio relevance
02 frame - used during framing to co-create a shared domain language, bounded contexts, and boundary contracts before delegating work to AI agents.
