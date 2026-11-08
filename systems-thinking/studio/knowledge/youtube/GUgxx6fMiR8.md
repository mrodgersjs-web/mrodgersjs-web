---
source: https://www.youtube.com/watch?v=GUgxx6fMiR8
video_id: GUgxx6fMiR8
channel: Tech With Tim
title: "How to Build an App With Claude Code - Full Tutorial for Beginners"
scraped: 2026-08-28
tags: [tools, claude-code, web-development, deployment, mcp]
---
# How to Build an App With Claude Code - Full Tutorial for Beginners

A complete beginner-oriented workflow for building, versioning, and deploying a web app with Claude Code inside Cursor, using Hostinger for hosting and an MCP server for natural-language redeployments.

## Procedure / models distilled
- Install the Claude Code terminal CLI via the curl command from Anthropic and authenticate with `claude`.
- Install a VS Code-compatible editor such as Cursor and open a dedicated project folder to view generated files.
- Install the Claude Code extension and the Hostinger extension inside the editor.
- Open Claude Code in its native UI panel inside Cursor, and configure mode, effort level, and model before prompting.
- Start any build by planning: describe the idea, ask Claude clarifying questions, and have it write the spec to a markdown file.
- Use voice dictation (e.g., Whisper Flow) to dump requirements and iterate faster than typing.
- Prompt Claude Code to scaffold the app, then review and approve each command/edit it proposes.
- Initialize a Git repository and instruct Claude to auto-commit changes so you can roll back mistakes.
- Purchase a Hostinger plan plus a free domain, then upload a zip of the project folder to create the initial deployment.
- Generate a Hostinger API token and connect it to Cursor through the Hostinger extension / MCP server.
- If Claude Code in Cursor cannot see the Hostinger MCP server, manually add the MCP config with the token and restart Claude Code.
- Use natural-language commands in Claude Code to list domains and redeploy the site whenever you update it.

## Failure modes named
- Starting code generation without a clear plan or spec produces significantly worse results.
- Mistaking Cursor’s agent tab for Claude Code and trying to use both interchangeably without checking MCP access.
- Not setting up Git commits, making it impossible to roll back broken changes.
- Claude Code sessions inside Cursor sometimes fail to auto-detect the Hostinger MCP server even after installing the extension.
- Sharing or leaking the Hostinger API token, which gives access to your hosting account.
- Choosing maximum effort on every prompt without considering time and credit cost.
- Getting stuck at Hostinger’s forced initial upload step because you did not prepare a zip of the project folder.

## Studio relevance
04 leverage - provides a repeatable Claude Code + Hostinger MCP workflow for rapidly prototyping and shipping client web apps.
