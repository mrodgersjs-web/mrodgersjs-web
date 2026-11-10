---
source: https://www.youtube.com/watch?v=CJi-Km-hSP0
video_id: CJi-Km-hSP0
channel: Prompt Engineer
title: "Paperclip AI Company Tutorial (Step by Step) – Crash Course – Local and VPS"
scraped: 2026-08-28
tags: [tools, ai agents, agent orchestration, vps deployment]
---
# Paperclip AI Company Tutorial (Step by Step) – Crash Course – Local and VPS

A hands-on walkthrough of installing and running Paperclip, an open-source multi-agent AI company framework, both locally with `npx` and on a Hostinger VPS via Docker, using Codex as the default agent adapter.

## Procedure / models distilled
- Install Paperclip locally with `npx paperclip onboard yes` to bootstrap the framework and verify that tests pass.
- Create a company, name it, and define the mission and high-level goal that all agents will work toward.
- Build an org chart of AI employees (e.g., CEO, CTO, CMO, UX designer) and assign each an LLM adapter such as Codex, Claude, Gemini CLI, Open Code, Pi, Cursor, or Hermes.
- Configure each agent through `agent.md` (role, delegation rules, memory, planning), `soul.md` (persona, voice, tone), tools/skills, and heartbeat interval.
- Deploy Paperclip on a Hostinger VPS using the provided Docker orchestration template, selecting a plan such as KVM 2 with 8 GB RAM and 2 vCPUs.
- Set admin credentials and optional API keys in the VPS Docker deploy panel, then open the running instance's management console.
- Access the VPS terminal or SSH in as root, run `docker ps` to identify the Paperclip container, then `docker exec -it <container_id> /bin/bash` to enter it.
- Authenticate Codex inside the Docker container with `codex login` and device-code flow after enabling device code authorization in the linked ChatGPT account's security settings.
- Switch to a different OpenAI/Codex account if the current account hits its usage limit, then retry failed tasks.
- Operate as the board member: create issues/tasks, assign them to the CEO or other agents, and let the CEO delegate to the appropriate role.
- Review and approve agent actions (e.g., hiring new agents) from the inbox before they execute.
- Track per-agent costs, input/output/cache tokens, runs, and set per-agent budgets to cap spending.
- Use heartbeat scheduling so agents periodically wake, scan for pending tasks, and continue work without manual prompting.
- Add custom skills via the skills panel and run multiple projects inside the same company instance.

## Failure modes named
- Codex authentication fails until device code authorization is explicitly enabled in the linked ChatGPT account's security settings.
- Running out of credits or hitting rate/usage limits causes agent runs to fail until an account with available credits is linked.
- Logging into Codex on the host machine instead of inside the Docker container leaves the Paperclip deployment unauthenticated.
- Relying on a local machine risks downtime from power loss, reboots, or instability compared with a VPS.
- Skipping the inbox review step blocks agent actions that require board approval, such as hiring new team members.

## Studio relevance
04 leverage - how the studio uses this card to evaluate and deploy multi-agent orchestration infrastructure for autonomous project execution.
