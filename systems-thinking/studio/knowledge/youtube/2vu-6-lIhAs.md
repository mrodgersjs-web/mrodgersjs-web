---
source: https://www.youtube.com/watch?v=2vu-6-lIhAs
video_id: 2vu-6-lIhAs
channel: Brian Casel
title: "Design OS: The Missing Design Process for AI-First Development"
scraped: 2026-08-28
tags: [tools, ai-first-development, design-systems, front-end]
---
# Design OS: The Missing Design Process for AI-First Development

A free, open-source AI-first design workflow that guides you from product idea through production-ready React components, then hands them off to a coding agent for backend integration.

## Procedure / models distilled
- Run the design process in a standalone project separate from your app codebase, built on React, Vite, ShadCN, and Tailwind CSS.
- Move through three phases: product planning, per-section design, and export for implementation.
- Start with the `/vision` command: paste rough product notes and let the AI ask clarifying questions to shape a clear product overview.
- Run `/roadmap` to break the product concept into self-contained, buildable sections (like dashboard, clients, sales pages).
- Run `/data model` to define the conceptual nouns of the system—entities and relationships—without writing database schemas.
- Establish the global design system in two steps: `/design tokens` (colors, typography) and `/shell` (persistent navigation/layout).
- Design each section by shaping requirements, generating sample data, and designing the actual screens.
- Export a `product plan` package containing a data model summary, design tokens, fonts, shell spec, section readmes, React components, sample data, test instructions, and agent prompts.
- Choose an implementation strategy: incremental (foundation → shell → sections one by one) or oneshot (entire app in one session).
- For incremental builds, reuse the section prompt and update the `{SECTION_NAME}` and `{NN}` variables for each milestone.
- Start implementation in Cloud Code plan mode (Shift+Tab) so the agent can analyze the exported files, inspect the codebase, and ask clarifying questions before writing code.
- Each section ships a `readme.md` (flows and design decisions), `sample-data.json`, React components, and `tests.md` with success/failure paths to guide test-driven development.
- The coding agent's job is to wire up data and integrate the supplied components, not recreate designs from screenshots or mockups.

## Failure modes named
- Generic UIs produced by raw AI coding tools and isolated-looking screens with no shared system or cohesion.
- Reprompting and rebuilding causing each iteration to drift further from a coherent vision.
- Hand-crafting mockups that get lost in translation during implementation.
- Treating data modeling as a technical schema task instead of a conceptual "nouns of the system" exercise.
- Skipping the global design system (tokens + shell) before designing individual screens.
- Mixing incremental and oneshot prompts instead of choosing one strategy.
- Starting agent implementation without plan mode, missing the opportunity to align on backend and integration details.

## Studio relevance
04 leverage - the studio uses this card to structure the design-to-code handoff and ensure coherent, production-ready front-end components are ready before backend implementation begins.
