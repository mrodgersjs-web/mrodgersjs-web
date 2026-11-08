---
source: https://www.youtube.com/watch?v=-_aQquBH5PU
video_id: -_aQquBH5PU
channel: Simon Scrapes
title: "Master Claude Design in One Video (Complete Build)"
scraped: 2026-08-28
tags: [tools, ai-design, claude, design-systems, workflow]
---
# Master Claude Design in One Video (Complete Build)

A practical build-along showing how to treat Claude Design as a system-design coding assistant rather than a canvas tool, using a structured design system to escape default "AI slop" aesthetics and blend Claude Design's 90% speed with Claude Code/skills for the final 10% polish.

## Procedure / models distilled
- Frame Claude Design as code under the hood, not a drag-and-drop canvas; it behaves like Claude Code and rewards prompting, action, and iteration rather than pixel editing.
- Distinguish asset design (single posts/flyers, Canva territory) from system design (websites/apps with consistent screens, Figma/Claude Design territory).
- Apply the 90/10 rule: expect Claude Design to deliver roughly 90% of the output quickly, but reserve budget for human taste, custom microcopy, exact icons, and logos in the final 10%.
- Build the design system first, before any production screens; front-load one to two hours setting up tokens, typography, color, components, and reference screens to avoid the default Anthropic house style.
- Feed Claude Design a design system using one of three paths: upload 3–5 reference screenshots, use an external skill like Skill UI to extract a system from a website, or paste skill content directly into Claude Design.
- Use a "taste skill" or explicit ban list to suppress default AI aesthetics (e.g., no Roboto, no generic gradients, no teal) and capture your own brand voice.
- Keep design-system setup in a single focused session to protect the separate Claude Design token quota from draining across multiple chats.
- For production screens, use inline comments or the element-targeting tools to iterate on specific parts rather than rewriting the entire prompt.
- Start with a video/animation brief inside Claude Design when building dynamic slide decks or carousels, then duplicate the project and convert it into a clickable slide deck.
- Export the 90% Claude Design output to Claude Code and apply custom skills for the final brand polish, custom graphics, or developer handoff.
- Use regular Claude (chat) for copy and structural planning to save Claude Design tokens for visual work.
- Capture and reuse approved design-system screens as templates by duplicating projects inside Claude Design.

## Failure modes named
- Opening Claude Design expecting a Figma/Canva replacement and getting frustrated by the lack of drag-and-drop control.
- Skipping the design system setup, which produces the default "AI slop" look: warm cream backgrounds, serif fonts, colored accent bars, and the blinking green dot.
- Writing loose prompts without design specifications, causing Claude to fall back to its baked-in default presets.
- Treating Claude Design output as final-ship-ready and neglecting the final 10% of human taste and brand assets.
- Spreading design-system creation across multiple sessions, burning through the separate Claude Design token quota without finishing the system.
- Fully re-prompting instead of using inline comments/element edits for targeted changes.
- Trying to create custom graphics, icons, or logos inside Claude Design rather than handing those off to Figma, a designer, or Claude Code skills.
- Relying on custom Claude skills inside Claude Design, which currently are not supported; requiring a hybrid Claude Code + Claude Design workflow.

## Studio relevance
04 leverage - how the studio uses this card to hybridize Claude Design rapid system prototyping with Claude Code/skills for brand-specific final polish and design-system handoff.
