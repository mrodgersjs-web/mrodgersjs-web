---
source: https://www.youtube.com/watch?v=uJO5mzNb9Xs
video_id: uJO5mzNb9Xs
channel: Matt Johnston | AI Engineer
title: "This AI Agent Swarm Lets Me do the Work of 25 Devs - Here's My Setup (Open Source)"
scraped: 2026-08-28
tags: [tools, ai-agents, tailscale, self-hosting, cli-automation]
---
# This AI Agent Swarm Lets Me do the Work of 25 Devs - Here's My Setup (Open Source)

Matt Johnston demonstrates his open-source setup of three specialized AI “employees” (a dashboard assistant, an auto-fix pipeline, and a mobile CLI agent) running on a Tailscale-connected Mac mini with Claude Code and Codex so a solo developer can work from any device and automate code fixes, reviews, and deployments.

## Procedure / models distilled
- Split an AI agent swarm into three specialized roles rather than one general assistant: Elrond (dashboard assistant), Auto Sam (auto-fix pipeline), and Samwise (mobile CLI agent).
- Turn a local Mac mini into a private node server and expose CLI tools over Tailscale so they are reachable from any device without cloud-tool latency.
- Wrap the Claude Code and OpenAI Codex CLIs in thin node servers and present them through a single web dashboard with tabbed, persistent chat sessions.
- Keep agent sessions “warm” for responsiveness, but provide a fresh-thread option to clear context bloat and run cron jobs to kill dead node processes before they become resource-zombies.
- Build a unified dashboard that puts tasks, Kanban boards, docs, P&L tracker, cron jobs, session status, and activity logs next to the agent chat interfaces.
- Run an auto-fix pipeline where Claude Code implements a ticket, Codex with GPT-5.5 reviews the resulting PR, and the card is routed to ready-to-merge or back to human review.
- Remove or defer brittle automation steps (like visual QA) when the debug/maintenance cost exceeds the time they save.
- Create slash commands such as `match` (make local look like remote) and `push` (push to main) so hot fixes can be issued from a phone in one tap.
- Give the mobile CLI agent access to the full local tool suite, MCPs, GitHub, Supabase, and Railway so it can code, generate PRs, and deploy from anywhere.
- Bake system instructions about the agent’s identity, environment, and location into the prompt so the agent can debug its own setup.
- Treat the three open-source repos as a customizable framework: rename agents, swap in local LLMs, add cron jobs, and extend the dashboard to fit personal workflows.

## Failure modes named
- A visual QA step had to be removed because it was too hard to debug and maintain compared with the value it provided.
- Cloud-based toolchains introduce friction and failure modes when doing urgent fixes away from the main machine.
- Long-lived agent sessions can leave zombie node processes that gradually slow down the host machine.
- Building full editing into the web app for synced documents is low-value because the native file system is a simpler, sufficient interface.

## Studio relevance
04 leverage - reference architecture for assembling a private, multi-agent CLI automation swarm that extends a single developer's reach across devices and deployment targets.
