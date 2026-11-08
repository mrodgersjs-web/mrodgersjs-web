---
source: https://www.youtube.com/watch?v=97KBdmSQEJ0
video_id: 97KBdmSQEJ0
channel: Norman Fenton
title: "What is a Bayesian network?"
scraped: 2026-08-28
tags: [statistics-causality, bayesian-networks, probabilistic-inference, medical-diagnosis]
---
# What is a Bayesian network?

A Bayesian network is a directed graph of variables and causal/influential relationships whose attached probability tables let you update beliefs about unobserved states as new evidence arrives.

## Procedure / models distilled
- Model a decision problem as a set of variables represented by nodes.
- Use directed edges between nodes to encode causal or influential relationships.
- Simplify variables to Boolean yes/no states when starting out.
- Assign a marginal probability table to each root node to capture population-level priors.
- Assign a conditional probability table to each node with parents, conditioned on the parents’ states.
- Treat the network in its marginal state as baseline population knowledge.
- Enter patient-specific observations as evidence into the relevant nodes.
- Run Bayesian inference to propagate evidence and update probabilities across the network.
- Re-run inference each time new evidence is observed.
- Compare posterior probabilities of competing diagnoses to identify the most likely condition.
- Recognize that probabilities update incrementally rather than jumping to a conclusion from one symptom or test.
- Combine multiple observations to disambiguate conditions that share similar symptoms.

## Failure modes named
- Not explicitly named in the transcript.

## Studio relevance
02 frame — the studio uses this card to frame uncertain, multi-factor situations as directed probabilistic graphs and update beliefs as evidence arrives.
