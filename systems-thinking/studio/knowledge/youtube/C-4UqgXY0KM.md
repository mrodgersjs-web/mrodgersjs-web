---
source: https://www.youtube.com/watch?v=C-4UqgXY0KM
video_id: C-4UqgXY0KM
channel: Tonbi's AI Garage
title: "Kimi K2.6 + Hermes Agent: The Coding Duo that Built My Dashboard Frontend Studio"
scraped: 2026-08-28
tags: [ai-agents, dashboard-plugins, frontend-development, git-worktrees]
---
# Kimi K2.6 + Hermes Agent: The Coding Duo that Built My Dashboard Frontend Studio

The video demonstrates building a Hermes Canvas dashboard plugin that turns an existing Hermes web dashboard into a live frontend creation studio, where a Kimi K2.6-powered Hermes agent edits project files via chat and the results render in an iframe preview.

## Procedure / models distilled
- Build a dashboard plugin for Hermes Agent that adds a split-pane Canvas tab with a chat panel on one side and an iframe frontend preview on the other.
- Reuse the existing Hermes dashboard plugin system for theming, shell navigation, and backend route mounting instead of rebuilding those primitives.
- Write a plugin manifest that registers the new Canvas/Frontend tab and implement the UI with plain JS/React.createElement, avoiding a bundler for rapid prototyping.
- Spawn Hermes Chat as a sub-process with a frontend-editing system prompt so the agent can reason about and edit the previewed project.
- Start a local Vite dev server inside the project and render it inside the dashboard iframe so changes hot-reload automatically.
- Create or open a project from the dashboard and auto-initialize a Git repository so the agent can use isolated git worktrees for each editing job.
- Use git worktrees to sandbox each agent request while syncing completed edits back to the main project directory.
- Commit agent-made changes back to the main repo after each job so the next worktree starts from the latest state and does not revert previous edits.
- Enable element selection mode in the preview so users can click a specific DOM node and prompt the agent to change only that element.
- Iterate through natural-language prompts: the agent edits files, the changes sync to the main directory, and the iframe preview updates.
- Test the plugin by dropping existing static or Vite-based sites into the agent project directory and opening them inside the dashboard.
- Force the agent to stay scoped to the project directory to prevent it from editing wrong files or folders.
- Keep API costs low by doing upfront planning and using Kimi K2.6 via OpenRouter for both coding and visual analysis of the frontend.

## Failure modes named
- Agent edits the wrong directory because of its own project-detection logic, requiring explicit path scoping.
- Each git worktree creates a new isolated branch from the original HEAD, so later prompts revert earlier changes unless each job is committed back to main.
- Tool-usage budget can force the agent to stop and summarize before continuing work.
- LLM tendency to build the smallest possible MVP instead of a genuinely useful implementation.
- Uncertainty whether a local-server/web-UI dashboard plugin is feasible within the Hermes plugin system.
- Backend fixes may require restarting the Hermes dashboard before the frontend preview reflects them.

## Studio relevance
04 leverage - use this card to prototype agent-driven dashboard plugins where an LLM edits a live frontend preview through isolated git worktrees and targeted element-level prompts.
