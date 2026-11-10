---
source: https://www.youtube.com/watch?v=4go2X5If31A
video_id: 4go2X5If31A
channel: Damian Galarza
title: "Your AI Assistant Doesn't Need a Bigger Model. It Needs Colleagues"
scraped: 2026-08-28
tags: [ai-agents, supervisor-pattern, multi-agent-systems, tool-sprawl]
---
# Your AI Assistant Doesn't Need a Bigger Model. It Needs Colleagues

Damian Galarza explains how he replaced a monolithic personal AI assistant with a supervisor-led team of specialized agents to reduce tool sprawl, improve delegation, and isolate sensitive data.

## Procedure / models distilled
- Use the supervisor pattern: one top-level agent coordinates a team of domain-specific sub-agents rather than doing everything itself.
- Apply the single-responsibility principle to agent design by extracting domains that have a large tool set, a distinct role, and a need for their own memory.
- Define each agent with a clear identity, description, memory scope, and dedicated tools.
- Build an AGENTS.md routing table for the supervisor that maps keywords and intents to the correct sub-agent, including notes on when not to delegate.
- Start incrementally with one sub-agent at a time instead of extracting too many agents too quickly.
- Use evals to test whether the supervisor delegates correctly, fails to delegate, delegates to the wrong agent, or over-delegates.
- Adjust prompts and the supervisor’s available tools to enforce desired behavior; for example, strip out tools that should belong only to a sub-agent.
- Model agent boundaries after real-world roles and constraints, such as a chief of staff handling calendar scheduling directly.
- Give each specialist its own SOUL.md, AGENTS.md, and USER.md so domain knowledge stays scoped and refined.
- Isolate untrusted or community-facing agents in a sandbox so they cannot access CRM, vault, or personal data.
- Use Mastra supervisor features such as delegation hooks, message filtering, sub-agent result context, and iteration monitoring to control the orchestration loop.
- Keep the supervisor’s own tool set minimal so it focuses on coordination and only handles tasks appropriate to its role.

## Failure modes named
- Tool sprawl from giving one agent too many tools, degrading its ability to pick the right tool.
- Over-delegating by extracting too many agents, making responsibilities hard to trace and debug.
- Under-delegating or delegating to the wrong agent due to ambiguous routing instructions.
- Conflicting duplicate tools between supervisor and sub-agent, causing friction over which should execute a task.
- Overly fine-grained agents, such as one agent per tool, that do not represent a real domain or role.
- Degraded memory usage when all memory is centralized instead of scoped per specialist.
- Sensitive-data exposure when external-facing agents are not isolated from personal systems like CRM or vaults.

## Studio relevance
04 leverage - use as a design reference for decomposing monolithic assistants into supervised, domain-specialist agent teams and tuning delegation behavior.
