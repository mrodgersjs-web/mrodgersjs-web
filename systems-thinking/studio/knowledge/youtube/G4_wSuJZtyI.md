---
source: https://www.youtube.com/watch?v=G4_wSuJZtyI
video_id: G4_wSuJZtyI
channel: Mansel Scheffel
title: "Every AIOS Tutorial Is Wrong - Here's What Actually Works"
scraped: 2026-08-28
tags: [ai-agents, ai-operating-system, business-automation, context-engineering, systems-design]
---
# Every AIOS Tutorial Is Wrong - Here's What Actually Works

Business AI systems should prioritize reliability, accuracy, and predictability by starting with actual constraints rather than copying flashy agent architectures from YouTube tutorials.

## Procedure / models distilled
- Anchor every AI build on three pillars: reliability, accuracy, and predictability; everything else is subordinate to these constraints.
- Treat simplicity as the meta-rule: reduce the system to the minimum needed for the actual business workflow, just as Michelin-star kitchens limit menu choice to ensure consistent output.
- Distinguish skills from agents: a skill is a deterministic A-to-B workflow, while an agent is only appropriate when the path to the goal is genuinely unpredictable.
- Default to skills on a schedule first; only introduce agents after a workflow is mapped and still contains exploratory gaps.
- Map workflows by interviewing the person doing the work, then write standard operating procedures mixed with scripts, references, and examples so the AI knows the "definition of good."
- Separate memory into distinct components: knowledge (curated business context), state (dynamic task/lead/pipeline data), and learned memory (rules the AI discovers from repetition).
- Store state in databases (Airtable, SQLite, Supabase, Excel) rather than markdown context files, because databases are purpose-built for trackable, queryable state.
- Keep knowledge context inside the skill folder so each skill is self-contained and portable; avoid centralizing operational context in Obsidian or separate vaults.
- Treat RAG as a last resort for semantic search across thousands of documents, not as a default memory layer; for simple lookups like name-equals-value, use a database instead.
- Choose tools by separating the human layer from the AI layer: use Obsidian or visual tools only if humans actually need to read and collaborate visually; otherwise keep assets where the AI executes.
- Prefer Notion over Obsidian for team collaboration, comments, tagging, and readability when humans need a visual documentation layer.
- Follow a constraint-build stack: foundation context first, then skills, then agents only for unknown paths, then databases for state, then learned memory rules, and finally RAG or system replacements only when a real roadblock demands it.
- Use context engineering to give each skill exactly the references, assets, and examples it needs to reach a clear definition of done.
- Make every tool decision stem from how the business and team actually work, not from hype, FOMO, or influencer demonstrations.

## Failure modes named
- Building elaborate agent front ends for workflows that already have predictable paths, which increases maintenance and bugs without adding value.
- Conflating memory, state, and context into a single concept, leading to misplaced data and unreliable retrieval.
- Stashing state inside markdown files instead of databases, causing fragility as soon as the data needs to be tracked or updated.
- Defaulting to RAG for every memory use case even when simple database lookups would be more accurate and reliable.
- Migrating all business documentation to Obsidian because it uses markdown, ignoring that most of those features are for human visualization rather than AI consumption.
- Believing Obsidian backlinks and semantic-search plugins are tools Claude can reliably use, when they are currently designed for humans.
- Letting YouTube demos drive architecture decisions instead of mapping real employee workflows and constraints first.
- Automating a workflow before the underlying process and "definition of good" are clear, which automates confusion rather than value.

## Studio relevance
02 frame - use this card to reframe client AI builds away from flashy agent hype and toward constraint-driven, deterministic skill architectures.
