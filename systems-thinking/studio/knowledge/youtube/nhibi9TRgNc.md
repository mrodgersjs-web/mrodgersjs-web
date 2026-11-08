---
source: https://www.youtube.com/watch?v=nhibi9TRgNc
video_id: nhibi9TRgNc
channel: Jack Roberts
title: "AntiGravity + Spline = INSANE 3D Websites (NEW Skill)"
scraped: 2026-08-28
tags: [tools, 3d-websites, no-code, ai-coding, design-intelligence, web-hosting]
---
# AntiGravity + Spline = INSANE 3D Websites (NEW Skill)

Jack Roberts demonstrates how to combine AntiGravity's AI coding agent with Spline's community 3D assets, design-intelligence workflows, lead-capture integrations, and one-click Vercel publishing to build and ship animated 3D websites without writing code.

## Procedure / models distilled
- Treat each page as having one "hero feature" — a single focal 3D element — and design everything else around it.
- Source ready-made interactive 3D scenes from Spline's Discover > Community section, then remix them to get a reusable URL/export.
- Use the AntiGravity Spline skill (a pre-packaged integration) to ingest Spline assets into an AntiGravity project via file upload.
- Prompt AntiGravity to build a landing page but leave the hero section empty so the Spline asset can be inserted later.
- Export the chosen Spline scene via Code Export, typically as vanilla.js, and copy the generated embed URL.
- Instruct AntiGravity to place the Spline asset as a full-viewport hero that owns the first screen rather than being pushed to a side column.
- Apply "design intelligence" / "vibe design" by collecting references, images, and concepts and letting the agent synthesize a coherent visual outcome from prompts.
- Snipe UI components and visual styles from reference sites, then instruct AntiGravity to remix those micro-patterns into the live page.
- Store form submissions in Supabase as a backend bridge because front-end code cannot directly push data to email/CRM APIs.
- Connect Supabase-stored leads to Beehiiv (for email deliverability) by providing the Beehiiv API key and letting AntiGravity discover the correct list ID.
- Connect the same lead data to Go High Level via an inbound webhook trigger so the CRM auto-creates contacts and can start nurture sequences.
- Add the Vercel MCP and GitHub CLI integrations to AntiGravity so the agent can push code to GitHub and deploy to Vercel.
- Use the "instant publish" skill to deploy the finished site and return a live Vercel URL without manual deployment steps.

## Failure modes named
- Trying to make every element the hero so no element stands out.
- Letting AntiGravity relegate a full-screen Spline asset to a side panel instead of anchoring it as the hero.
- Attempting to send lead data directly from the front end to Beehiiv, which Beehiiv blocks.
- Publishing without validating inbound webhook payloads in Go High Level.
- Missing the need for a backend/database layer between the form and external services.

## Studio relevance
05 ground - how the studio uses this card
