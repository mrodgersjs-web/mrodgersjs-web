---
source: https://www.youtube.com/watch?v=647pSnX5H_Y
video_id: 647pSnX5H_Y
channel: AI News & Strategy Daily | Nate B Jones
title: "You're Wasting 40% Of Your AI Time On Something Fixable"
scraped: 2026-08-28
tags: [productivity, ai agents, scaffolding, workflow automation]
---
# You're Wasting 40% Of Your AI Time On Something Fixable

The video maps the agentic scaffolding stack—prompts, skills, plugins, MCPs/connectors, scripts, and hooks—and teaches how choosing the right component for each kind of work lets non-engineers encode repeatable, multi-system workflows and stop wasting time on one-off prompting.

## Procedure / models distilled
- Use a prompt only for temporary, highly specific, one-off tasks that you do once and don't need to repeat, share, or carry permissions or tools.
- Promote a repeated, reusable process into a skill: a clear markdown document that captures your house style, steps, and standards so any LLM can invoke it consistently.
- Apply the power-law lens to skills: identify the ~20% of processes that are repeated often, high-stakes, and sensitive to errors, and skill those first.
- Treat a plugin as an installable workflow package that bundles skills, prompts, scripts, hooks, connectors, MCP servers, assets, commands, and metadata for a complete multi-step job.
- Use MCP servers or app connectors whenever an agent needs live access to external systems such as Salesforce, Slack, Figma, or GitHub.
- Add scripts and hooks for deterministic, predictable checks that should not be left to the LLM's judgment, such as validation or formatting steps.
- Audit a workflow before scaffolding it: classify whether it is one-off, repeatable, cross-tool, live-data-dependent, or verification-heavy, then choose the smallest matching component.
- Build plugins from domain expertise rather than only engineering: the person who knows what good output looks like should design the workflow, even if they are not a coder.
- Distinguish scopes with the decision rule: prompt = once; skill = repeated; plugin = repeatable workflow that needs to travel, install, or include tools/assets/connectors; MCP/connector = needs another system's data.
- Design plugins around a single coherent job or workflow (e.g., editorial first pass, weekly business report, hiring readout) instead of trying to make one plugin cover an entire department.
- Verify agent output with a deterministic check or human review step rather than trusting the model to evaluate itself.
- Treat marketplaces as the distribution layer for plugins, but don't wait for marketplace plugins to match your workflow; build custom scaffolding for your own work.

## Failure modes named
- Wasting hours each week by stuffing repeatable, multi-step work into heavy one-off prompts.
- Acting as the "human plugin" by manually copying data between apps, re-prompting, and re-checking instead of packaging the workflow.
- Building a plugin when a prompt or skill is enough, or asking engineers for an MCP/API when the work is local and repeatable.
- Waiting for OpenAI, Anthropic, or another vendor to release your ideal plugin instead of creating it yourself.
- Turning the workspace into a "museum of plugins" by scaffolding everything instead of only high-value, repeated workflows.
- Letting non-technical leadership remain confused about deterministic scripts versus LLM judgment, causing misguided pressure to "use AI."
- Trusting the LLM to check its own work rather than adding a deterministic verification script or human review.

## Studio relevance
04 leverage - how the studio uses this card
