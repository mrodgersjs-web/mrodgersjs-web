---
source: https://www.youtube.com/watch?v=-WCNwxz3uoM
video_id: -WCNwxz3uoM
channel: Mark Kashef
title: "Build Your Agentic OS Better Than The 99%"
scraped: 2026-08-28
tags: [tools, agentic-os, data-readiness, claude-code, hooks]
---
# Build Your Agentic OS Better Than The 99%

The real leverage of an agentic OS comes from cleaning and structuring data, defining deterministic context pipelines, and treating agents like hired specialists rather than adding shiny features on top of messy foundations.

## Procedure / models distilled
- Put data readiness before dashboards or features: build a clean, queryable foundation before layering agents on top.
- Use a four-layer architecture: identity/rules at the base, then knowledge/sources, then worker agents, then automations and hooks on top.
- Treat Claude MD as an "air traffic control" document that routes the right context to the right agent at the right time, not as a diary.
- Use project-level skills for folder-specific behavior and global skills for behavior that applies across every project.
- Use hooks as reliable event triggers at session start, in specific folders, or post-compaction to inject memory and keep conversations rich.
- Put prerequisite data on a "silver platter" via summary files and summary tables so agents synthesize instead of spending most of their context window retrieving.
- Give every agent a documented critical path / SOP so it knows where to look, how to pull, how to analyze, and what anomalies to ignore.
- Pre-aggregate KPIs and metrics with deterministic code before asking an agent to analyze them, reducing hallucination and slowness.
- Use an orchestrator or chief-of-staff agent loaded with the roles, responsibilities, and scopes of sub-agents to prevent overlap and cold-start mismatches.
- Add new agents only when an existing agent is overloaded, like hiring a new employee at a bootstrapped company.
- Treat skills as an infinite game: launch a minimal version, run real conversations, learn from wrong turns, then bake the perfected critical path back into the skill.
- Build a living data map with a pantry, prep table, plate, data-flow view, build-ideas list, and a 30-day plan to make the system tangible.
- Choose integrations intentionally: API, CLI, skill, or MCP depending on the data source and security constraints.
- For regulated or confidential domains, isolate each data set with separate Claude MDs, hooks, and rules to keep sensitive context controlled.
- Crystallize repeated workflows into slash commands so one trigger runs an entire SOP chain.

## Failure modes named
- "Sparkly slop on top of slop": building beautiful agents and dashboards on messy, outdated, disorganized data.
- Wasting the context window on raw JSON, metadata, and retrieval, leaving little room for synthesis and causing hallucinations or slowness.
- Treating Claude MD as a diary instead of a contextual routing layer.
- Ignoring hooks because they seem confusing, even though they are straightforward and highly reliable.
- Starting agent teams without an orchestrator, causing role mismatch, overlap, and repeated cold-start friction.
- Creating too many agents at once instead of splitting off specialists only when one agent is overloaded.
- Letting AI agents perform deterministic aggregations instead of pre-computing summary tables with code.
- Telling an agent "don't make mistakes" with sensitive data rather than physically or logically isolating data domains.
- Believing the model is a silver-bullet oracle that can figure everything out from raw, uncurated feeds.

## Studio relevance
02 frame - how the studio uses this card to design agentic operating systems on clean data foundations, deterministic context hooks, and role-scoped agent teams rather than feature-first slop.
