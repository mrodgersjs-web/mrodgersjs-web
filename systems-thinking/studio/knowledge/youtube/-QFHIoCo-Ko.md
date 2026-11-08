---
source: https://www.youtube.com/watch?v=-QFHIoCo-Ko
video_id: -QFHIoCo-Ko
channel: AI Engineer
title: "Full Walkthrough: Workflow for AI Coding — Matt Pocock"
scraped: 2026-08-28
tags: [tools, ai-coding, context-management, workflow]
---
# Full Walkthrough: Workflow for AI Coding — Matt Pocock

Matt Pocock presents an agent-assisted coding workflow that treats LLMs as forgetful, context-limited collaborators: align the idea first, capture the destination in a lightweight PRD, split work into small parallel issues, and enforce quality with pull-based implementers and push-based reviewers.

## Procedure / models distilled
- Model LLM context as a smart zone and a dumb zone: attention relationships strain quadratically as tokens accumulate, so keep each task small enough to stay inside the smart zone.
- Treat every LLM session as a reproducible cycle of system prompt → explore → implement → test, and prefer clearing context to a known base state over compacting it.
- Keep the system prompt tiny and monitor the live token count so you always know how close you are to the dumb-zone threshold.
- Use a “grill me” skill to interrogate and align an idea with the AI before any implementation begins.
- Capture the destination in a product requirements document (PRD) as a directional hint, not as a perfect or immutable specification.
- Convert the PRD into a phase-N loop where a planner repeatedly selects small changes that move the code closer to the target state.
- Decompose work into small, parallel GitHub issues with explicit blocking relationships so agents can work on independent branches at the same time.
- Run implementers in isolated sandboxes, have a separate reviewer inspect the resulting commits, then use a merger agent to resolve conflicts and merge.
- Make coding standards available to implementers via pull (skills they can consult when unsure) and push them explicitly to reviewers so standards are applied to finished code.
- Use the QA phase to generate new issues for the board, not merely to validate existing work; treat the Kanban as the living control surface.
- Preserve architectural intentionality by asking the agent to find coupled modules and extraction candidates, rather than treating the PRD as a spec-to-code compiler.
- Close or archive planning artifacts once implementation is done to avoid doc rot, while keeping deterministic artifacts such as database migrations.

## Failure modes named
- Letting context grow into the dumb zone by chaining long sessions instead of sizing tasks for the smart zone.
- Trusting compacted conversation summaries instead of clearing to a known, reproducible base state.
- Over-optimizing the PRD before implementation, which yields far less value than iterating through QA loops.
- Leaving stale PRDs or planning markdown in the repo, where doc rot misleads future agent runs.
- Treating AI coding as spec-to-code compilation and ignoring the evolving shape of the codebase.
- Pushing all coding standards to the implementer instead of using pull for the builder and push for the reviewer.

## Studio relevance
04 leverage - use the smart-zone, phase-N loop, and push/pull distinction to design agent-assisted coding workflows.
