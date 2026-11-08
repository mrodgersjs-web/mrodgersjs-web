---
source: https://arxiv.org/abs/2006.05048
paper_id: arXiv:2006.05048
title: "Policy-focused Agent-based Modeling using RL Behavioral Models"
authors: "Osonde A. Osoba, Raffaele Vardavas, Justin Grana, Rushil Zutshi, Amber Jaycocks"
year: 2020
venue: "arXiv"
citation_count: null
tags: [systems-thinking, agent-based-modeling, reinforcement-learning, policy-analysis]
type: paper-note
---
# Policy-focused Agent-based Modeling using RL Behavioral Models

## Claim

The validity of policy inferences from agent-based models depends on the quality of the agents' behavioral models. Standard specifications — heuristic decision rules or regressions on past data — are limited. Reinforcement-learning agents are adaptive, high-performing, and behaviorally valid models of utility-maximizing agents, and improve policy ABMs.

## Method

Hypothesis test: instantiate ABM agents as RL learners (rather than fixed heuristics or fitted regressions), evaluate their effectiveness as utility-maximizing behavioral models in policy-exploration ABMs, and compare against the standard specification modes.

## Studio relevance

- **frame**: a recipe for the agent layer of any simulated system: when the real actors adapt (users, competitors, other agents), static rule agents understate the dynamics; adaptive agents are the honest choice.
- **leverage**: policy ABMs exist to explore emergent consequences of interventions — this is the studio's "simulate the intervention, watch emergence" step, with guidance on what to put inside the agents.
- **ground**: methodological citation for RL-in-ABM validity claims.
