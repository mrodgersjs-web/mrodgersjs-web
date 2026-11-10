---
source: https://www.youtube.com/watch?v=t1bWyk9qVa4
video_id: t1bWyk9qVa4
channel: Jan Marshal
title: "How Senior Developers Actually Code With AI"
scraped: 2026-08-28
tags: [tools, ai-coding, workflow, software-engineering, cursor]
---
# How Senior Developers Actually Code With AI

A senior developer's end-to-end workflow for using AI coding agents to build production features in a controlled, maintainable way.

## Procedure / models distilled
- Start from foundations: your workflow, model choice, and agent interface choice matter more than any single tool.
- Treat model choice as neutral and evolving: most modern LLMs are good enough, so pick what works for your workflow and use case rather than marrying a provider.
- Treat agent interface choice as friction-reduction: evaluate editors (Cursor, Windsurf, Zed), CLI/TUI tools (Claude Code, Codex, Open Code), and wrappers, then pick whatever removes the most friction for you.
- Define the feature idea before prompting: ask who needs it, what pain it solves, what the MVP is, what is in v1 vs later, how it fits existing app primitives, what success looks like, and what is out of scope.
- Maintain a living PRD (Product Requirements Document) so the agent understands the existing application: target users, MVP scope, primary user flow, key features, functional requirements, and target technical shape.
- Provide maximal context to the agent so it assumes nothing; explicitly state constraints like billing logic, permissions, and off-flow edge cases.
- Break each feature into small, chunkable pieces rather than asking one agent to produce thousands of lines at once.
- After generation, manually review the generated code line-by-line or section-by-section before testing or shipping.
- Test the feature in realistic end-to-end scenarios, including edge cases like signed-in, signed-out, and new-account states.
- When bugs appear, instruct the agent to analyze and explain the root cause before asking it to fix anything, avoiding random-solution guessing.
- Use AI code-review tools (e.g., Cursor Bug Bot, Codium, Devin review) as a second layer to catch bugs you missed in large diffs.
- Treat AI reviewer findings as input: validate them, then feed valid bugs back to the agent with precise instructions.
- Commit, push, and open a PR only after code review and real-world verification.

## Failure modes named
- "Prompt, a dream, and a very large git diff" workflows that skip planning and context.
- Believing viral AI coding demos reflect real-world agent behavior.
- Locking into one model provider or one interface because of hype rather than fit.
- Letting the agent assume schema, billing logic, or UI constraints instead of stating them explicitly.
- Skipping the PRD and feeding the agent an under-specified feature.
- Asking the agent to "just fix it" without root-cause analysis, leading to random guesses and more breakage.
- Generating too much code in a single pass, which increases hallucination and errors.
- Shipping without manual review or real-world testing.
- Relying solely on human review for large pull requests and missing subtle bugs.

## Studio relevance
04 leverage - how the studio uses this card
