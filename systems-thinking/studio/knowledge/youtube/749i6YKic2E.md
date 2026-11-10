---
source: https://www.youtube.com/watch?v=749i6YKic2E
video_id: 749i6YKic2E
channel: Adrien | AI Designer
title: "The AI Website Design Process (2026)"
scraped: 2026-08-28
tags: [engineering, ai-assisted-design, web-development, design-systems]
---
# The AI Website Design Process (2026)

A walkthrough of a 4-hour AI-assisted workflow to go from brand identity to a live, animated, booking-integrated website using Claude, Cursor, Limora, Re Motion, GitHub, and Vercel.

## Procedure / models distilled
- Anchor the workflow with a clear brand identity, exported as a `.fig` file, so every AI-generated downstream asset stays on brand.
- Use Claude Design to generate a complete design system (typography, scales, primary/neutral colors, gradients) by describing the company and attaching the brand `.fig` file.
- Export Claude Design’s generated design system as a shareable zip, unzip it, and add the folder to the project workspace so Claude Code can consume the assets and README instructions.
- Configure Claude Code inside Cursor and load the design-system assets before writing any site code.
- Write a markdown strategy brief covering site sections, copy, and business goals before coding, so the AI has site architecture and purpose, not just a vague prompt.
- Generate HTML/CSS with the best available coding model (Opus 4.7 in the video), iterating by describing changes or uploading screenshots into the Claude Code chat.
- Use a Figma-like preview tool (Paper) for manual visual edits when Claude Code cannot make direct visual adjustments.
- Generate custom on-brand illustrations, hero images, or product visuals with Limora using logo, colors, and typography, then have Claude Code integrate them into the site.
- Use Re Motion to animate SVG elements and add hover interactions that lift the site above static, generic results.
- Treat site layout as iterative: generate multiple hero-section variations, compare them, and refine the strongest option.
- Collaborate with teammates by pushing the codebase to a GitHub repository and syncing changes through Claude Code, since Claude Code lacks live multiplayer like Figma or Framer.
- Deploy the site by connecting the GitHub repo to Vercel, enabling free hosting, custom-domain mapping, and near-instant publish-on-push.
- Maximize output quality by feeding the AI rich context—complete brand guidelines, a documented design system, and a strategy brief—rather than minimal prompts.

## Failure modes named
- Starting AI generation without a clear brand identity produces off-brand, inconsistent assets.
- Asking the coding model to “build me a website using the design system” without a strategy brief yields weak site architecture and copy.
- Claude Design’s limited credit allowance makes heavy iteration inside that tool expensive or impractical.
- Claude Code cannot perform direct visual/manual edits, creating friction for quick visual tweaks.
- The toolchain has no live multiplayer editing; teammates only see updates if changes are pushed and pulled through GitHub.

## Studio relevance
05 ground - the studio uses this card to translate a client’s brand strategy and design system into a built, animated, and deployed website via an AI-assisted toolchain.
