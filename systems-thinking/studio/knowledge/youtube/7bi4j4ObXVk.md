---
source: https://www.youtube.com/watch?v=7bi4j4ObXVk
video_id: 7bi4j4ObXVk
channel: AI Stack Engineer
title: "Open Design: The Self Hosted Claude Design Killer Built On Your Coding Agent"
scraped: 2026-08-28
tags: [tools, open-source, design-systems, coding-agents, self-hosting]
---
# Open Design: The Self Hosted Claude Design Killer Built On Your Coding Agent

Open Design is an Apache 2.0, self-hostable alternative to Claude Design that lets you bring your own coding agent and API key to generate visual artifacts and work products from a library of skills and markdown-based design systems.

## Procedure / models distilled
- Clone the repo, run `pnpm install`, then start the local web UI with `pnpm tools dev run web`.
- Configure execution mode on first load by choosing a detected CLI agent (Claude Code, Codex, Cursor, Gemini, Open Code, Qwen, etc.) or the BYOK Anthropic API fallback.
- Submit a brief; the agent returns a discovery form first to lock in surface, audience, tone, brand context, scale, and constraints before writing code.
- Use the direction picker when no brand spec exists to select one of five curated visual directions, each with a deterministic OKLCH palette and font stack.
- Choose a skill/surface (web prototype, SaaS landing, dashboard, pricing, docs, blog, mobile app, slide deck, or work product templates like specs, runbooks, OKRs, invoices).
- Optionally select a design system from 71 markdown-based systems, each a nine-section `design.md` covering color, typography, spacing, layout, components, motion, voice, brand rules, and anti-patterns.
- Let the Node/Express daemon spawn the selected CLI in a per-project `.od` folder with real filesystem, bash, and web-fetch tool access.
- Iterate on generated artifacts by prompting the agent for fixes; export output as PDF, ZIP, standalone HTML, or open in a new tab.
- Import existing Claude Design ZIP projects to migrate off the closed-source tool.
- Swap agents/models for the same skill and design system to compare quality, latency, and cost without workflow lock-in.

## Failure modes named
- Expecting Open Design to match Claude Design's out-of-the-box polish when running against weaker or non-tuned models.
- Assuming a strong design system can compensate for a weak model; output quality is heavily model-dependent.
- Choosing non-Claude Code agents and expecting the same rich streaming experience, since they are line buffered.
- Treating Open Design as a finished product; it is still a research preview with roadmap features like comment mode and an AI tweaks panel missing.
- Falling back into subscription stacking by paying for separate design tools instead of using a BYOK agent you already own.

## Studio relevance
04 leverage - deploy as a self-hosted, BYOK artifact generator for client deliverables and internal work products while keeping model choice and cost under studio control.
