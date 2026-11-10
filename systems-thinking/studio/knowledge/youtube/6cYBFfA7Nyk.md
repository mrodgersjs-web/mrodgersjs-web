---
source: https://www.youtube.com/watch?v=6cYBFfA7Nyk
video_id: 6cYBFfA7Nyk
channel: Chase AI
title: "Top 10 NEW Open Source Claude Code Tools (May)"
scraped: 2026-08-28
tags: [tools, claude-code, open-source, ai-agents]
---
# Top 10 NEW Open Source Claude Code Tools (May)

Chase AI reviews ten recently released open-source tools and skills that extend Claude Code with memory, video input, design, cost control, browser automation, and job-search workflows.

## Procedure / models distilled
- Install the **Caveman Skill** into Claude Code/Codex and pick a verbosity level (light, full, ultra) to force shorter, more direct agent responses.
- Use Caveman as a token-saving and quality-shaping device based on the finding that forcing powerful models to be concise can improve correctness by reducing verbose wrong turns.
- Deploy **Graphify** to read project files and build a structured knowledge graph, lowering per-query token consumption compared with raw-file reading.
- Feed Graphify multimodal inputs such as PDFs, screenshots, diagrams, and video audio (via Whisper) without relying on vector embeddings.
- Run **Claude video** by passing it a video file so FFmpeg extracts a duration-based frame budget and Whisper extracts audio, letting Claude Code "watch" video through frames plus transcript.
- Use **Open Design** to replicate Claude Design locally with any coding agent, creating prototypes, slide decks, images, and videos via API calls.
- Add **Codeburn** across AI coding tools to track token usage, cost, and performance by activity, project, model, core tool, shell command, and MCP server, then act on its optimization suggestions.
- Apply the **Impeccable** skill to front-end work, using its 23 commands, before/after example gallery, and live browser mode to iterate on component variations.
- Point **Design Extract** at any website with a headless browser to capture layout, responsiveness, motion, interaction states, component anatomy, and brand voice as a build spec for Claude Code.
- Use **Career Ops** as a job-search command center: paste a job URL, let Playwright navigate and classify the listing, match it against your CV, generate a tailored PDF/report, and update a tracker.
- Run **Browser Harness** as an autonomous browser agent that writes and updates its own skill file after each site-specific run, self-healing from what worked and what failed.
- Connect the official **n8n MCP server** by describing an automation in Claude Code so it generates TypeScript, validates the node logic, converts to JSON, and deploys into your n8n instance.

## Failure modes named
- Caveman's claimed output-token savings are overstated for total cost: it only shortens visible words, not thinking or ingestion, so real overall savings are roughly ~5%.
- Treating Obsidian as a true knowledge graph/RAG system is a misconception; it is a markdown interface and lacks multimodal ingestion and graph-RAG mechanics.
- Claude video degrades for longer videos because frame budgets become sparse, so usefulness depends heavily on the task and duration.
- Career Ops can be mistaken for a mass-application spam tool, but it is intended as a scalpel for matching and tailoring rather than spraying applications.

## Studio relevance
04 leverage - select open-source Claude Code add-ons and integration patterns to amplify agent workflows.
