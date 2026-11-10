---
source: https://www.youtube.com/watch?v=DWWrLlM3gwQ
video_id: DWWrLlM3gwQ
channel: Eero Alvar
title: "Pi Coding Agent Setup After 2 Months"
scraped: 2026-08-28
tags: [ai-agents, pi-ai, custom-tools, agent-extensions, sub-agents]
---
# Pi Coding Agent Setup After 2 Months

After two months of using Pi as his main AI interface, the author walks through his evolving configuration of custom tools, sub-agents, extensions, skills, and workflows for coding and content research.

## Procedure / models distilled
- Build a custom web search tool with a schema that supports Google modifiers (exact-phrase quotes, exclusion terms, batched queries) instead of passing raw quoted strings through a single query parameter.
- Pair web fetch with a separate markdown parser so fetched pages are efficient and readable for the agent.
- Add an ask-user-question tool so the agent can fill missing context mid-turn without stopping to list questions in its response.
- Keep the sub-agent loadout minimal (scout, researcher, worker) for context hygiene, and define each agent as a markdown file listing tools and model instructions.
- Add a video extraction tool that supports multiple surgical analysis modes (frame, timestamp, time range, full analysis) for both local files and YouTube links.
- Implement persistent memory per project with a `memory.md` file and an injected context block that tells the agent when to read and update it.
- Route agent outputs to a markdown file via an MD-link command to render LaTeX or math-heavy content that the terminal cannot display.
- Install a bash guard extension that intercepts potentially destructive commands and asks for explicit confirmation before execution.
- Use a file changes extension to log create and edit operations with deltas and line counts, and to undo changes in directories without git.
- Load skills as modular markdown instructions on demand (YouTube transcripts, PDF reading, orchestrator behavior, Reddit browsing) rather than putting everything in global context.
- Apply a surgical PDF parsing strategy: choose text extraction, page rendering, or image rendering based on content type instead of dumping the whole PDF into context.
- Constrain research agents with explicit quality criteria, such as narrative completeness, protagonist/antagonist, quantified stakes, clear outcome, visual potential, and low existing coverage on YouTube.

## Failure modes named
- JSON parsing breaks when quoted exact phrases are passed inside a single search query parameter, requiring the search schema to be split into separate fields.
- Keeping narrow tools or skills in the global config bloats the orchestrator context window; tools like YouTube search, image search, and Reddit browsing should live in local agent configs instead.
- A project `memory.md` can become bloated and messy over time, requiring periodic refactoring into multiple markdown files.
- Bash guard confirmation pop-ups do not scale to fully autonomous headless or background operation.
- A file changes logger only captures edits made through the agent's write/edit tools, missing any file modifications performed by raw bash commands.
- Dumping an entire PDF into the context window quickly bloats it and fails with math symbols and images; surgical extraction is required.
- Pi's default Yolo mode has no guard against destructive shell commands, so a bash guard or equivalent safety layer is essential.

## Studio relevance
04 leverage - practical patterns for composing custom Pi tools, sub-agents, skills, and guardrails into a personalized coding assistant.
