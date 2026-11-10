---
source: https://www.youtube.com/watch?v=e59q9y0rmFo
video_id: e59q9y0rmFo
channel: Prism Labs
title: "Hermes Workspace: A Real Command Center for AI Agents"
scraped: 2026-08-28
tags: [ai-agents, control-plane, open-source, swarm-orchestration, terminal-ui]
---
# Hermes Workspace: A Real Command Center for AI Agents

Hermes Workspace is the open-source web cockpit for the Hermes Agent framework, providing a multi-pane control plane that turns AI agents from chatbots into supervised, long-lived processes with chat, terminal, memory, skills, and swarm orchestration.

## Procedure / models distilled
- Treat agents as long-lived processes you supervise, not as chatbots that respond once per message; a control-plane mental model is required once agents run code, spawn sub-agents, and hold state for hours.
- Deploy the three-process architecture: Hermes Agent Gateway (port 8642), Workspace UI (port 3000), and optional dashboard/operations API (port 9119) that sources fleet data.
- Install with a single curl command that pulls the agent framework, clones the workspace repo, creates the .env file, and runs pnpm install.
- Configure deployments entirely through a single .env file: set HERMES_APP_URL to the gateway (loopback or Tailscale node), add only the provider keys you need, set HERMES_PASSWORD for non-loopback access, and optionally point HERMES_DASHBOARD_URL to port 9119 for fleet mode.
- Connect any model provider without committing to one: Anthropic, OpenAI, OpenRouter, Google, Ollama, LM Studio, vLLM, Atomic Chat, and llama.cpp/OpenAI-compatible endpoints.
- Switch models mid-thread while carrying context, enabling a single conversation to move from cloud to local or across providers.
- Supervise agents across four panes simultaneously: chat, real PTY terminal, Monaco-based file browser, and persistent memory inspector without changing windows.
- Inspect and edit agent memory directly in a markdown editor inside the workspace to observe and correct what an agent is storing.
- Use real-time tool cards that stream every tool call and let you approve or abort actions mid-flight.
- Load skills from a built-in marketplace of over 2,000 community-contributed entries and inspect which skill an agent just loaded.
- Run Conductor mode to dispatch missions to parallel sub-agents, and monitor them from the Operations panel for fleet-style visibility.
- Operate Swarm mode through a Kanban task board backed by persistent tmux workers; drag tasks to In Progress, and the orchestrator routes them to role-matched worker pools such as builders, reviewers, docs, research, ops, and QA.
- Keep workers warm across tasks to avoid paying context-rebuild costs on every dispatch.
- SSH into any tmux worker session manually for full transparency and avoid black-box agent execution.
- Install the progressive web app from Chrome/Edge automatically, or add to the iOS home screen via the share sheet, for desktop-to-mobile feature parity and offline capability.
- Deploy headlessly by running the gateway as a systemd service, fronting the UI with nginx/Caddy and TLS, and optionally using Tailscale for private mobile access.
- Maintain production posture with the built-in fail-closed defaults: auth middleware on all API routes, HTTP-only same-site strict secure cookies, content security policy, path traversal prevention, rate limiting, and mandatory HERMES_PASSWORD when binding beyond 127.0.0.1.

## Failure modes named
- Treating agents as chatbots rather than long-lived processes, which breaks once agents perform long-running work, spawn sub-agents, and mutate state.
- Accidentally exposing an agent dashboard to the internet with weak or no authentication.
- Weekend-hackathon-style projects shipping open ports and bolting security on afterward.
- Black-box agent execution where you cannot inspect running worker sessions.
- Paying repeated context-rebuild costs because agent state is not persisted across tasks.
- Routing a task to the wrong agent role, such as handing a code refactor to the docs writer.

## Studio relevance
04 leverage - how the studio uses this card
