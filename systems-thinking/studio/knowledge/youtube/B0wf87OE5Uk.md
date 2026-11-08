---
source: https://www.youtube.com/watch?v=B0wf87OE5Uk
video_id: B0wf87OE5Uk
channel: Joshua Martin
title: "Automate LinkedIn Outreach With One Slash Command"
scraped: 2026-08-28
tags: [linkedin, outreach, ai-agents, supabase, mcp]
---
# Automate LinkedIn Outreach With One Slash Command

A LinkedIn outreach system built in Claude code using two slash-command workflows, persistent Supabase tracking, the Unipile LinkedIn API connector, and mandatory human-in-the-loop approval to send high-volume, human-feeling messages in about ten minutes a day.

## Procedure / models distilled
- Run two distinct workflows: an autonomous overnight prospector for connection requests/likes, and a manual `{slash} outreach` workflow for drafting and sending direct messages.
- Segment leads into three pools before writing: newly accepted connections (A), existing network matches that have gone quiet (B), and prior contacts due for a follow-up (C).
- Sub-segment by buyer type (e.g., independent sponsor, broker, PE, institutional investor, real estate investor) so each lead gets the template and offer framing matched to its category.
- Use a “first-line customized hook + rest template” pattern: web-scraped research personalizes the hook while guardrail templates prevent AI from writing the full message from scratch.
- Require human-in-the-loop approval before any bulk send so you can fact-check references, catch wrong industries, and confirm tone before Claude dispatches messages.
- Send approved messages at randomized, human-like cadence (about every 30 seconds with jitter) to reduce the chance of triggering LinkedIn bot detection.
- Treat Supabase as persistent memory: track lead IDs, LinkedIn URLs, segment labels, last action timestamps, templates used, follow-up timing, and a do-not-contact flag for negative responses.
- Store static context in markdown skill files (ICP definition, offer, templates, sequence timing) so Claude does not need to be re-prompted on information that never changes.
- Use a dedicated skill markdown file to define the exact slash command workflow, available tools, and step-by-step actions Claude should follow on each invocation.
- Power LinkedIn actions through the Unipile MCP connector, which exposes LinkedIn API endpoints for profiles, connection requests, post likes, and direct messages.
- Prospect autonomously via Sales Navigator API, qualify leads against the ICP, like one of their posts, then send a connection request, writing each new lead into Supabase for the outreach workflow to use later.

## Failure modes named
- Letting AI write entire messages from scratch, which risks hallucinated facts, wrong industry references, and off-brand tone.
- Sending messages too quickly or at perfectly regular intervals, which can trip LinkedIn’s bot detection.
- Skipping human approval and allowing AI errors to reach prospects unchecked.
- Treating all leads identically instead of matching template and offer framing to the buyer sub-segment.
- Losing track of who has been touched, who accepted, and who is due for follow-up because chat history is ephemeral without a persistent database.
- Failing to flag negative responders as do-not-contact, leading to repeated unwanted outreach.
- Letting the system feel like automated spam at scale rather than targeted, human-feeling outreach.

## Studio relevance
05 ground - reference blueprint for wiring persistent CRM, human-in-loop review, and API connectors into a low-risk automated outreach operation.
