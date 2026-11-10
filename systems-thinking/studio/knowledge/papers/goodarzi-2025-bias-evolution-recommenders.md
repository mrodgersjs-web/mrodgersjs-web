---
source: https://arxiv.org/abs/2510.21728
paper_id: arXiv:2510.21728
title: "Modeling Bias Evolution in Fashion Recommender Systems: A System Dynamics Approach"
authors: "Mahsa Goodarzi, M. Abdullah Canbaz"
year: 2025
venue: "arXiv"
citation_count: null
tags: [systems-thinking, system-dynamics, recommender-systems, feedback, bias]
type: paper-note
---
# Modeling Bias Evolution in Fashion Recommender Systems: A System Dynamics Approach

## Claim

Bias in fashion recommender systems (FRS) is not a static defect but a feedback-driven evolution: it perpetuates and amplifies societal stereotypes over time. Inductive biases (from the model/pipeline) influence system outcomes more than user biases, and current debiasing strategies (data rebalancing, algorithmic regularization) are insufficient — the bias re-activates through the loop.

## Method

System dynamics modeling with experimental simulation: build an SD model of bias activation and reinforcement inside an FRS, simulate temporal evolution of bias and its impact on system performance, and evaluate debiasing interventions within the model.

## Studio relevance

- **diagnose**: canonical modern instance of a reinforcing loop inside an ML system — training → exposure → user behavior → data → training. Any "the model is drifting/getting worse" complaint should be framed this way.
- **leverage**: the finding that parameter-level fixes (rebalancing, regularization) fail while loop structure persists is Meadows rank-12 vs rank-6+ logic applied to ML debiasing.
- **frame**: shows ML systems are legitimately stock-and-flow systems (data stock, exposure flow, bias accumulation).
