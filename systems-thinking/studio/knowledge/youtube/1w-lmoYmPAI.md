---
source: https://www.youtube.com/watch?v=1w-lmoYmPAI
video_id: 1w-lmoYmPAI
channel: Agentic Development - Ben Fellows
title: "This 1-Hour Dashboard Saves You $1000s in QA Labor"
scraped: 2026-08-28
tags: [engineering, qa, test-pyramid, test-coverage, automation]
---
# This 1-Hour Dashboard Saves You $1000s in QA Labor

Map every user story to the unit, integration, API, and end-to-end tests that cover it so the test pyramid becomes a visible, optimizable system instead of an opaque coverage percentage.

## Procedure / models distilled
- Maintain the test pyramid as an efficiency model: each layer should verify only what is unique to that layer, minimizing duplicate work across unit, integration, API, contract, and end-to-end tests.
- Build a single source-of-truth by listing user stories and acceptance criteria in a markdown file, assigning each story a stable ID.
- Ingest existing test cases from the codebase and any third-party systems into the same workspace so AI can reason across both stories and tests.
- Tag each existing test case with the user-story ID it covers, leaving unmatched tests blank so they surface as orphan tests.
- Run an AI-assisted scanner to scrape all tagged tests and stories, then roll them up into a dashboard view.
- Read the dashboard by feature/user story to see coverage distribution across layers, not by aggregate coverage percentage.
- Treat the dashboard as a first diagnostic step, then manually verify that test cases actually do what their names claim.
- Use the rolled-up view to identify gaps where a story lacks lower-layer tests and where a story is over-covered by API or end-to-end tests.
- Shift expensive API and end-to-end tests toward unit and integration tests where business logic and data interactions can be verified more cheaply.
- Package the scanner/dashboard as a reusable module or CLI tool if needed, so it can live outside the main codebase.
- Extend the dashboard incrementally with version history, scan-time trends, authentication, or hosted access as organizational needs grow.

## Failure modes named
- Inverted pyramid: 222 API tests and only 76 unit tests, which is the exact cost signal the dashboard is designed to expose.
- Mapping user stories only to browser-level or end-to-end tests, ignoring unit and integration coverage.
- Treating aggregate coverage percentage as meaningful, instead of coverage-by-feature across layers.
- Treating the automated dashboard as the final answer rather than a first step that still requires human verification of test intent.
- Using API or end-to-end tests as a permanent default instead of a starting point that should migrate logic downward.
- Leaving unmatched tests unclassified, hiding orphan tests that no longer map to real user stories.

## Studio relevance
03 diagnose - the studio uses this card to reveal test pyramid misalignment, orphan tests, and feature-level coverage gaps before optimizing QA labor.
