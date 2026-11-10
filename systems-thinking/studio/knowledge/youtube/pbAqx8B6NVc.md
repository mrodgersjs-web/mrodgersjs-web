---
source: https://www.youtube.com/watch?v=pbAqx8B6NVc
video_id: pbAqx8B6NVc
channel: Damian Galarza
title: "Build Your Own AI Agent from Scratch (Mastra + TypeScript)"
scraped: 2026-08-28
tags: [ai-agents, mastra, typescript, slack-integration, scheduler]
---
# Build Your Own AI Agent from Scratch (Mastra + TypeScript)

This video demonstrates how to build an event-driven personal meeting-assistant agent with Mastra and TypeScript, wiring it to Slack, cal.com, Exa, and a custom scheduler for follow-ups.

## Procedure / models distilled
- Bootstrap a Mastra project with `npx create-mastra`, select a provider and model, enable coding-agent skills, and initialize Git for change tracking.
- Define an agent by assigning a unique ID, name, system instructions, and a chosen LLM to scope its behavior.
- Wire the Mastra instance in a central index file by registering agents, attaching a Pino logger, and configuring libSQL/SQLite storage.
- Use Mastra Studio at `localhost:4111` to inspect agents, view prompts and model settings, and test conversations before adding tools.
- Expose a local dev server to external services with Ngrok, then configure a Slack app from a manifest to receive webhook events.
- Integrate Vercel's Chat SDK with the Slack adapter and a memory state source to build a unified chatbot interface across channels.
- Store Slack bot tokens and signing secrets in `.env` and never commit credentials to Git.
- Distinguish chatbot state memory (thread history) from agent memory (working and semantic memory) to avoid mismatched recall behavior.
- Implement working memory as a persistent scratchpad with a custom template so the agent accumulates facts about the user over time.
- Add semantic memory with libSQL vector storage and a local FastEmbed embedding model, configuring top-K retrieval and message-range context.
- Build a custom scheduler with a dedicated SQLite database and Drizzle ORM to avoid coupling custom tables to Mastra's internal store.
- Register task handlers in a type-keyed map and poll every 30 seconds for due tasks, transitioning statuses through pending, running, completed, or failed.
- Trigger workflows from external events such as cal.com booking webhooks and schedule follow-up tasks based on event end times.
- Design the whole system as event-driven: an external trigger causes the agent to act and delivers the result where the user already works.

## Failure modes named
- Committing API keys and Slack secrets to version control instead of keeping them in `.env`.
- Coupling custom scheduled-task tables to Mastra's default database, risking breakage on framework updates.
- Missing task handlers causing scheduled jobs to fail silently unless explicitly marked failed.
- Prior webhooks arriving before memory is configured, leaving the agent unable to recall earlier context.
- Agent hallucination when not instructed to say "I don't know" or when memory retrieval returns insufficient context.
- Confusing chatbot state memory with agent memory, leading to incomplete or incorrect conversation context.

## Studio relevance
04 leverage - how the studio uses this card
