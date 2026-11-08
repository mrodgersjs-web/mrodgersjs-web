---
source: https://www.youtube.com/watch?v=0mOFP2WPQXg
video_id: 0mOFP2WPQXg
channel: easy learning
title: "1  What is a Bayesian network"
scraped: 2026-08-28
tags: [mathematics, bayesian-networks, probability, graphical-models, conditional-independence]
---
# 1  What is a Bayesian network

A Bayesian network is a directed acyclic graph that visualizes the factorization of a joint probability distribution, with nodes as random variables, edges as parent-child conditioning relationships, and attached CPDs that fully encode the distribution and its conditional independencies.

## Procedure / models distilled
- A joint probability distribution over many random variables can be factorized using the chain rule.
- The variables can be ordered differently, producing alternative valid factorizations.
- A factorization simplifies when the distribution satisfies conditional independencies among variables.
- Different independence assumptions or orderings lead to different factorizations of the same joint distribution.
- To build a Bayesian network, assign one node to each random variable.
- Draw a directed edge from every conditioning parent variable to the conditioned child variable in each factor.
- The resulting directed acyclic graph is the Bayesian network structure.
- Reconstruct the joint distribution by multiplying each node’s conditional probability given its parents.
- Conditional independencies can be read from the DAG structure.
- Each node is independent of its non-descendants when conditioned on its parents.
- Conditional probability distributions (CPDs) supply the numerical parameters for each node.
- Adding CPDs to the structure produces a complete Bayesian network.
- A full Bayesian network encodes the original joint probability distribution because it specifies both how to factorize and what each factor is.
- In essence, a Bayesian network is a visualization of the factorization of a joint distribution.

## Failure modes named
- None explicitly named in the transcript.

## Studio relevance
02 frame - maps variables, dependencies, and conditional independencies to make probabilistic system structure explicit.
