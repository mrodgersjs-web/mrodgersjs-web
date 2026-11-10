---
source: https://www.youtube.com/watch?v=AeGCWCSVwrQ
video_id: AeGCWCSVwrQ
channel: The Next New Thing
title: "OpenAI’s Paperclip & Multica imitation?"
scraped: 2026-08-28
tags: [tools, ai-agents, project-management, linear, developer-tools]
---
# OpenAI’s Paperclip & Multica imitation?

Adam installs and demos OpenAI’s open-source Symphony agent, which watches Linear tickets, spawns isolated Codex agents to code, test, review, and push tasks through a workflow, while comparing it with Multica and Paperclip and flagging its high token use, slowness, and customization trade-offs.

## Procedure / models distilled
- Ticket-triggered agent loop: a new Linear ticket automatically spawns an isolated Codex agent that plans, codes, tests, cross-reviews, and delivers an evidence package before moving the ticket to human review.
- Project-management-as-queue: tickets become the canonical spec and work queue for agents, replacing chat as the interface for multi-step engineering pipelines.
- Two-tier install model: choose a prebuilt Symphony CLI/orchestration layer for quick experiments, or build from scratch using an architecture markdown file to customize integrations and behavior.
- Agentic README install: paste the repo’s install instructions into Claude Code/Codex and answer its questions; it clones the repo, builds, prompts for credentials, and starts the local server.
- Local dashboard observability: a running local dashboard streams the agent’s token count, picked-up tickets, and progress in real time.
- Plan-with-checkboxes workflow: the agent posts a plan as a Linear comment and ticks off steps as it completes them, creating visible progress.
- Human-in-the-loop gate: after finishing work, the agent moves the ticket to a human-review state rather than deploying unilaterally.
- Token-cost asymmetry: the full agentic pipeline can burn hundreds of thousands of tokens for tasks that take a direct Codex assistant only thousands of tokens and seconds.
- Rate-limit exposure: heavy token consumption increases the risk of hitting provider rate limits and interrupting real work.
- Identity/attribution problem: because the agent uses the user’s Linear API key, its comments and state changes appear as if the user performed them, obscuring human vs. agent actions.
- Separate-agent-identity fix: assign tickets or comments to a dedicated “Symphony” user/alias so the history clearly distinguishes agent work from human work.
- Workflow-state coupling: the default agent requires custom Linear states such as “human review” and “rework,” which may conflict with an existing team workflow.
- Customization through rebuild: changing integrations (e.g., Jira), states, agent persona, or tooling requires building your own orchestration layer from the architecture spec rather than using the prebuilt option.
- Comparative evaluation rubric: judge agentic PM tools on setup friction, transparency, control, SaaS lock-in vs. open source, and whether tickets can be assigned to agents vs. only to humans.
- Hello-world smoke test: run the simplest possible task first to observe the tool’s full motion, then measure latency, cost, and quality before trusting it with real work.

## Failure modes named
- Token-hungry and slow: Symphony burned ~582k tokens and several minutes to create two simple markdown files.
- API rate-limit exhaustion from high per-task token use.
- Misattribution in Linear: agent actions look like user actions, making ticket history confusing.
- Inflexible default workflow requiring non-standard Linear states such as “human review” and “rework.”
- Prebuilt agent tightly coupled to Linear; using Jira or other task trackers demands a custom rebuild.
- Broken or awkward local UI, such as streaming raw token counts in the dashboard.
- SaaS alternative (Multica) behaves as a black box and funnels users toward a paid platform with less control.
- Premature reliance: promising vision, but not yet robust enough to bet production workflows on.

## Studio relevance
03 diagnose - the studio uses this card to map token, latency, identity, and workflow-coupling failure modes before embedding ticket-driven AI agents into real engineering pipelines.
