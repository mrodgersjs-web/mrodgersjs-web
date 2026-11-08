---
source: https://www.youtube.com/watch?v=4bfKyZ7hbsU
video_id: 4bfKyZ7hbsU
channel: Sean Kochel
title: "Google’s 7-Step Vibe Engineering Skill Is Incredible"
scraped: 2026-08-28
tags: [engineering, ai coding, vibe coding, agentic workflows, sdlc]
---
# Google’s 7-Step Vibe Engineering Skill Is Incredible

Sean Kochel demos Google's seven slash-command agent skills library for "vibe engineering," walking through refining an idea into a PRD, planning phased tasks, incrementally building vertical slices, verifying, reviewing, and shipping with CI/CD.

## Procedure / models distilled
- Start with `/idea refine` to turn vague concepts into concrete ideas.
- Use `/spec` (spec-driven development) to generate a PRD for a new project, feature, or large change.
- Use `/plan` to decompose the spec into small, verifiable tasks with clear acceptance criteria.
- Use `/build` with incremental implementation to deliver vertical slices (end-to-end feature slices) rather than horizontal layers.
- Run incremental implementation inside a red-green-refactor test-driven development loop: failing test, minimal passing code, refactor.
- Invoke specialized skills as needed: context engineering, frontend UI engineering, and API/interface design.
- Use verification skills such as browser testing and root-cause debugging.
- Run a five-axis review covering correctness, readability/simplicity, architecture fit, security, and performance.
- Apply code simplification, security hardening, and performance optimization skills after the initial build.
- Use the CI/CD skill to scaffold GitHub Actions, a feature/dev/master branching strategy, and test gates before merging.
- Add database indexes and ORM/query safeguards when scaling or hardening.

## Failure modes named
- AI coding orchestration tools growing more complicated without actually producing better outcomes.
- Over-engineering an MVP with routing/intent tools before validating user need.
- Building horizontal slices (all frontend then all backend) instead of end-to-end vertical slices.
- Agents introducing security gaps such as raw SQL without an ORM, raising SQL-injection risk.
- Skipping root-cause debugging and patching symptoms instead of the underlying issue.
- Missing database indexes as data grows, causing performance problems.
- Pushing broken code to production without tests or branch protections.
- Merging directly into `main` without running CI gates.

## Studio relevance
02 frame - provides a structured agent skill workflow to scope, build, verify, and ship features with AI coding agents.
