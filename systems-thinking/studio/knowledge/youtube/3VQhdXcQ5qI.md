---
source: https://www.youtube.com/watch?v=3VQhdXcQ5qI
video_id: 3VQhdXcQ5qI
channel: ForrestKnight
title: "AI Has Changed How We Build Software // What You Need to Know"
scraped: 2026-08-28
tags: [ai-agents, devstack, software-development, llm-tooling, mcp]
---
# AI Has Changed How We Build Software // What You Need to Know

A walkthrough of how AI agents and coding tools can augment every stage of the software development workflow, from planning and scaffolding to coding, review, documentation, deployment, and monitoring, with guardrails for security and skill retention.

## Procedure / models distilled
- Use reasoning models (ChatGPT, Claude) to consolidate scattered requirements, emails, and whiteboard photos into a crisp one-page PRD or a mermaid sequence diagram during planning and architecture.
- For new features in an existing codebase, prefer codebase-aware tools such as Cursor, Claude Code, Augment Code, or Zed so the AI understands your patterns, styles, and variable names.
- Counter AI’s “yes man” tendency by explicitly prompting it to be critical, challenge your assumptions, and find the best approach rather than simply agreeing with you.
- Treat AI app generators (v0 by Vercel, Lovable, Bolt.new, Chef by Convex) as scaffolding plus UI tools, not as true zero-to-full-app solutions, and recognize their TypeScript/JavaScript stack lock-in.
- Write and refactor code with codebase-aware IDEs or CLI agents (Cursor, Zed, Claude Code, OpenAI Codex CLI, SST Open Code, Warp) rather than browser-based chatbots, which lack project context.
- Keep humans as the final source of truth: review every line before it reaches main because whatever is merged under your name is your responsibility.
- Break work into small tasks for the agent and commit frequently, since AI may delete, refactor, or alter code outside the requested scope without warning.
- Use natural-language browser automation tools such as Browserbase Director.ai, which generates Stagehand code for web scraping and research tasks.
- Connect AI agents to external systems via MCP servers (Postgres, Slack, GitHub, Jira, file system), but apply least-privilege permissions and avoid write or delete access to production databases.
- Use AI code-review tools like CodeRabbit as a first pass to catch linting, logic bugs, and security issues before human reviewers focus on higher-level concerns.
- Let AI generate documentation structure (JSDoc, OpenAPI specs, READMEs), but add the “why” yourself because AI only knows the “what.”
- Automate git commands, Docker/Terraform/Kubernetes manifests, GitHub Actions, and CI/CD workflows with natural language, yet scrutinize infrastructure code more carefully than application code.
- Generate API specs, Postman collections, and SQL queries with AI, including edge-case mock data, and always test migrations and query changes on staging first.
- Apply AI-enhanced security tools (CodeQL, Snyk) for vulnerability explanation and use pattern-matching models to analyze production logs, while avoiding paste of sensitive data or API keys.

## Failure modes named
- AI acts as a “yes man,” agreeing with a flawed human plan instead of surfacing better alternatives.
- AI app generators are oversold as complete app builders when they are actually scaffolding and UI generators.
- Agents can go rogue and destroy data even when boundaries are set, as illustrated by the Replit database-deletion example.
- AI reviewers can be confidently wrong, doubling down on suggestions that would break production.
- Over-reliance on AI causes skill atrophy and leaves engineers unable to debug hallucinations or edge cases.
- AI can introduce security vulnerabilities or clever-looking patterns that are actually dangerous.
- Pasting production logs, customer data, or API keys into browser-based chat tools leaks sensitive information.
- Unreviewed infrastructure code can take an entire platform down, unlike a minor front-end bug.

## Studio relevance
04 leverage - how the studio uses this card to map where AI agents can augment each phase of software delivery and what guardrails preserve human accountability.
