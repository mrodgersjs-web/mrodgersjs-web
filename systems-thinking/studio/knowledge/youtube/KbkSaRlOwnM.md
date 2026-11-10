---
source: https://www.youtube.com/watch?v=KbkSaRlOwnM
video_id: KbkSaRlOwnM
channel: Panda Making Money
title: "This Tiny Tool Makes Claude Code Actually Listen to You"
scraped: 2026-08-28
tags: [tools, ai-agents, spec-framework, open-source, documentation]
---
# This Tiny Tool Makes Claude Code Actually Listen to You

Open Spec is an open-source spec framework that replaces drifting chat-context with a persistent, version-controlled contract so AI coding agents build against a stable source of truth across sessions.

## Procedure / models distilled
- Treat chat history as volatile context, not a spec; the real bottleneck in agentic coding is underspecification, not model quality.
- Insert a spec layer between intent and code: a structured, persistent, repository-resident source of truth that survives session resets.
- Initialize Open Spec to create `OpenSpec/specs` (the living spec library) and `OpenSpec/changes` (the active development workspace).
- Organize the spec library as capability-based markdown documents describing how the system actually works right now, updated as features ship.
- Start every change with `propose`: write a plain-language idea and let the agent generate a self-contained change folder with proposal, requirements, design, and task list.
- Review the proposal before `apply`; catching misalignment during planning costs minutes, while catching it in code review costs hours of rework.
- Run `apply` so the agent executes the approved task list against an explicit contract rather than improvising from prompt context.
- Use `sync` to merge delta-spec changes into the main spec library at the requirement level, keeping living documentation accurate without manual maintenance.
- Archive completed changes so every future session starts from a fully documented, traceable system state.
- Write delta specs with three markers—`added`, `modified`, `removed`—to make the scope of a change readable in seconds before any code is written.
- Shift review from "code review" to "plan review" by evaluating the delta spec when feedback is cheapest and intent is clearest.
- Match Open Spec to your existing agent: it auto-detects tool directories and installs tool-specific skills and slash commands for 25+ assistants including Claude Code, Cursor, Codex, GitHub Copilot, and Open Code.
- Preserve tool-agnostic investment: the spec library lives in `OpenSpec/` and transfers cleanly if you switch agents later.
- Reserve Open Spec for multi-session, multi-contributor, or architecturally complex codebases; skip it for quick one-off prototypes where the planning overhead exceeds the value.

## Failure modes named
- **Agent drift across sessions**: when chat context resets, the agent reconstructs intent by guessing, and guesses compound until output diverges from original purpose.
- **Vibe coding / improvisation**: without a persistent contract, the agent invents requirements every session, producing impressive but unstable code.
- **Prompt-length trap**: longer prompts or more examples cannot fix underspecification if the requirements still vanish when the session ends.
- **Reverse-engineering code review**: reviewing large diffs to reconstruct intent is slow, error-prone, and scales poorly with change size.
- **Treating specs as generated artifacts**: approving proposals without reading or pushing back turns Open Spec into ceremonial overhead instead of a working contract.

## Studio relevance
03 diagnose - how the studio uses this card to identify and counter agent drift, underspecification, and context-loss failure modes in AI-assisted builds.
