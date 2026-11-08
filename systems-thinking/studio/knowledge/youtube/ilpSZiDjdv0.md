---
source: https://www.youtube.com/watch?v=ilpSZiDjdv0
video_id: ilpSZiDjdv0
channel: PyCon AU
title: "An introduction to Causal Inference with Python – making accurate estimates of cause and effect from"
scraped: 2026-08-28
tags: [statistics-causality, python, observational-studies, data-science, machine-learning]
---
# An introduction to Causal Inference with Python – making accurate estimates of cause and effect from

A PyCon AU talk making the case for explicit causal reasoning and demonstrating DoWhy's four-step workflow (model, identify, estimate, refute) on the Lalonde training-program dataset.

## Procedure / models distilled
- Treat questions phrased as "what would happen if…" or "why did this happen…" as inherently causal, requiring causal—not just associative—models.
- Build the causal model as a Directed Acyclic Graph (DAG) whose nodes are variables and whose directed edges encode assumed cause-effect relationships.
- Encode domain knowledge as an explicit DAG so assumptions are documented and contestable rather than left implicit.
- Construct the DoWhy graph string by declaring variables and using arrow operators to represent direct and indirect causal edges.
- Instantiate a DoWhy `CausalModel` by supplying the data, graph string, treatment variable, and outcome variable.
- Run `identify_effect` to derive an estimand (e.g., a backdoor estimand)—a valid strategy for computing the desired causal quantity from the data.
- Use the graph structure to decide which variables to condition on and, crucially, which variables to avoid conditioning on because control can introduce bias.
- Run `estimate_effect` to compute the causal effect using DoWhy's built-in estimators or models from the econml package.
- Run `refute_estimate` to stress-test the result, for example with a placebo-treatment test that randomizes treatment and expects the effect to disappear.
- Apply the `do` operator to simulate interventions and compute counterfactual outcomes (e.g., average wage if everyone or no one had received training).
- Compare multiple candidate DAGs to assess sensitivity of conclusions to the assumptions encoded in each graph.

## Failure modes named
- Using predictive/associative models to answer causal questions about interventions or changed contexts.
- Stating causal claims such as "X reduces risk of Y" while simultaneously dismissing the study as merely associational.
- Controlling for every available variable instead of conditioning only on variables identified by the causal graph.
- Simpson's paradox, where an omitted or mishandled grouping variable reverses the apparent direction of an effect.
- Assuming causality can only be inferred from randomized controlled trials and cannot be modeled from observational data.

## Studio relevance
02 frame - how the studio uses this card
