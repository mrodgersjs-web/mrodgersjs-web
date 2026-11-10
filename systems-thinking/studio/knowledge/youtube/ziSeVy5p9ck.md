---
source: https://www.youtube.com/watch?v=ziSeVy5p9ck
video_id: ziSeVy5p9ck
channel: Clearmud
title: "How I have my Hermes and OpenClaw AI Agents.. WORKING TOGETHER!"
scraped: 2026-08-28
tags: [tools, ai agents, discord, multi-agent, integration]
---
# How I have my Hermes and OpenClaw AI Agents.. WORKING TOGETHER!

A walkthrough of wiring a Hermes agent and an OpenClaw agent together through shared Discord channels so they can coordinate autonomously.

## Procedure / models distilled
- Create a separate Discord application/bot for each agent you want to link.
- Configure OAuth scopes: select **bot** and **applications.commands**.
- Enable **Server Members Intent** and **Message Content Intent** for each bot.
- Grant bot permissions: **Send Messages**, **Send Messages in Threads**, **Create Public/Private Threads**, **Add Reactions**, **Read Message History**, **View Channels**.
- Generate/reset the bot token and feed it securely to the corresponding agent so the agent can run as its own Discord gateway.
- Create a private solo channel per agent and at least one shared channel for cross-agent communication.
- Copy each channel ID and give the agent the IDs for both its solo channel and the shared channel.
- Invite each bot to your Discord server and assign role/channel access carefully to restrict where it can read and write.
- Use a trusted assistant agent to request and execute the setup steps for you rather than editing configs manually.
- Prompt the agents to introduce themselves, share context, and negotiate a recurring operating rhythm.
- Have the agents formulate a coordination plan covering cadence, reporting rules, and escalation boundaries.
- Lock shared-channel permissions so only the relevant agent bots can participate, preventing human or other-agent noise.
- Verify bidirectional routing by having each agent respond directly to the other in the shared channel.

## Failure modes named
- Discord API bugs/outages can hide typing indicators and delay bot responses.
- Bots appear offline until the correct token is loaded into the agent’s environment.
- Identity confusion: an agent may respond using the wrong persona/profile when profiles are not isolated.
- Channel “bleed” caused by overly broad roles lets an agent post in channels it should not access.
- Agents may respond to the human but ignore each other if message routing or channel permissions are misconfigured.
- Sharing bot tokens in chat bypasses safer manual setup and risks credential exposure.
- Gateway shutdowns can interrupt an agent mid-task and require restart.
- Impatience and repeated messages can derail the agents’ autonomous coordination.

## Studio relevance
04 leverage - how the studio uses this card to wire heterogeneous AI agents into a coordinated ops layer through a shared Discord backplane.
