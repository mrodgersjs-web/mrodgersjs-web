---
source: https://www.youtube.com/watch?v=J9RDDvt8nlg
video_id: J9RDDvt8nlg
channel: Corey Ganim
title: "Build STUNNING Websites with Claude Code + Google Stitch (full walkthrough)"
scraped: 2026-08-28
tags: [tools, web-design, ai-agents, design-systems, client-work]
---
# Build STUNNING Websites with Claude Code + Google Stitch (full walkthrough)

A no-code workflow for turning a Google Stitch design system into a production-ready Next.js website using Claude Code, complete with optimized images and brand-matched AI-generated visuals.

## Procedure / models distilled
- Use Google Stitch as the first step to generate both a design system and page mockups from a text prompt before writing any code.
- Feed Stitch brand inputs—colors, fonts, logo, and overall vibe—so the resulting system aligns with real client expectations.
- Start from a vanilla Next.js project created with `npx create-next-app` to keep the codebase clean and agent-friendly.
- Prompt Claude Code to implement the Stitch design system inside the Next.js app, treating the exported designs as the source of truth.
- Maintain an `agents.md` file with a critical rule that forces the coding agent to follow the design system for every change, including generated images.
- Export image assets from Stitch and have Claude download, convert, and serve them locally as WebP for performance.
- Replace generic or stock images with custom AI-generated visuals using Nano Banana Pro (via Cursor) that obey the same design system and brand vibe.
- Treat the design-system lock-in as a client milestone to prevent rework after the website has already been built.
- Use plain-language prompts to refine the site after the foundation is in place, such as adjusting image filters or opacity.
- Keep the workflow tool-agnostic: any coding agent (Claude Code, Cursor, etc.) can run the same steps once the design system is defined.

## Failure modes named
- One-shot prompts to coding agents produce obviously AI-generated pages with no images, placeholder blobs, weird spacing, and barely readable text.
- Building the entire website before the client sees the design system leads to expensive rejections and rework.
- Skipping image optimization forces users to download large PNGs or JPEGs, slowing the site and increasing bandwidth costs.
- Letting the agent ignore the design system produces inconsistent colors, fonts, and visuals as pages or components are added.
- Using generic stock photos instead of brand-specific AI images makes the site feel impersonal and less credible.

## Studio relevance
04 leverage - how the studio uses this card to rapidly turn approved design systems into client-ready, image-rich websites with AI coding agents while keeping brand consistency and performance in check.
