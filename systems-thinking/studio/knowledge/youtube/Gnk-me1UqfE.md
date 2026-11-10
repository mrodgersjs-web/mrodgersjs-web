---
source: https://www.youtube.com/watch?v=Gnk-me1UqfE
video_id: Gnk-me1UqfE
channel: Discover AI
title: "WHAT? Qwen3.6-A3B Could Solve This?"
scraped: 2026-08-28
tags: [tools, reasoning, model-harnessing, prompt-engineering, small-models]
---
# WHAT? Qwen3.6-A3B Could Solve This?

The presenter runs the tiny 3B-active-parameter Qwen 3.6-A3B MoE model through a complex causal-reasoning elevator puzzle, reads its live reasoning summaries, and uses soft instruction tuning to steer it from a valid-but-suboptimal 18-step answer to the optimal 8-step shortcut solution.

## Procedure / models distilled
- Read the model's live reasoning-trace summary to infer its current strategy, risk assessment, and constraint handling.
- Apply "AI harnessing": external steering through soft instruction tuning rather than hard-coding the answer.
- Probe for unexplored alternatives by asking what other routes were considered.
- Distinguish a valid solution from an optimal solution; don't accept the first working answer.
- Identify puzzle linchpins such as the floor-33 mirror trigger and the floor-29 emergency exit.
- Work backward from the goal state to map prerequisite chains and required code cards.
- Segment the solution: acquire prerequisites, execute combo sequences, then invoke the shortcut.
- Use code-card synergy to bypass traps instead of navigating through them.
- Verify every step against explicit rules and state transitions.
- Treat constraints as filters for candidate paths, not merely as obstacles to avoid.
- Prefer deterministic, low-risk shortcuts over probabilistic or tedious climbs.
- Produce a final deliverable with rule-by-rule compliance and a state summary.

## Failure modes named
- Stopping at exploitation too soon and accepting a valid but far-from-optimal 18-step solution.
- Missing hidden shortcuts that appear in the reasoning trace but are not fully explored.
- Treating redundant code cards as necessary and overcomplicating the route.
- Mis-routing by incorrectly labeling a suboptimal route as "most interesting."
- Skipping step-by-step validation and deploying an unchecked sequence.

## Studio relevance
04 leverage - using reasoning-trace reading and soft instruction tuning to extract near-frontier performance from a small active-parameter model.
