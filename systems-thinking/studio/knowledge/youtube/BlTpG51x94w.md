---
source: https://www.youtube.com/watch?v=BlTpG51x94w
video_id: BlTpG51x94w
channel: Eric Tech
title: "GStack + GSD + Superpowers Workflow Is Insane!"
scraped: 2026-08-28
tags: [tools, ai-agents, software-development, automation, spec-driven-development]
---
# GStack + GSD + Superpowers Workflow Is Insane!

The video describes how to combine GStack, GSD, and Superpower into one spec-driven, autonomous build workflow that keeps context windows small and uses test-driven execution across headless sessions.

## Procedure / models distilled
- Use GStack's role-based personas (CEO, designer, engineering manager, security manager, etc.) in the brainstorming/spec phase to clarify intent and produce a well-reasoned product spec.
- Use GSD to split the completed spec into discrete phases, each with its own prompt, so every execution stays below roughly 50% of the model's context window.
- Use Superpower as the execution backbone for each phase, following its test-driven loop: plan, dispatch agents, write tests first, implement, then review/verify.
- Run an orchestrator session that maintains a state file of completed/incomplete phases and loops until every phase is finished.
- Delegate each phase to a fresh headless Claude Code session via the non-interactive prompt flag (`claude -p` or equivalent) so the orchestrator never absorbs implementation context.
- Keep the orchestrator's context clean by having each headless session return only a summary/result before the orchestrator triggers the next phase.
- When Superpower encounters design or architectural decisions during execution, hand the question to GStack roles to vote and adopt the majority option, then resume the main flow.
- Implement a "build loop" or route-loop automation that reads the phase state file and repeatedly spawns the next headless session until the project is fully built.
- Reserve the full GStack + GSD + Superpower workflow for large greenfield projects; for brownfield codebases or small features, use a lighter subset such as Superpower alone or GStack + Superpower.
- Include browser/Playwright or equivalent verification steps inside Superpower's review stage to confirm end-to-end behavior before marking a phase complete.

## Failure modes named
- Context rot — model accuracy drops once a conversation exceeds about 50% of the available context window.
- Manual phase handoff — starting a new interactive session for every phase is slow, tedious, and error-prone.
- Over-applying the full stack — using GStack + GSD + Superpower for brownfield or small features is overkill and can waste effort.
- Polluting the orchestrator context — letting the main session accumulate implementation details defeats the purpose of phase splitting and lowers accuracy.

## Studio relevance
06 synthesize - the studio uses this card to compose GStack, GSD, and Superpower into a unified autonomous build workflow for high-accuracy greenfield development.
