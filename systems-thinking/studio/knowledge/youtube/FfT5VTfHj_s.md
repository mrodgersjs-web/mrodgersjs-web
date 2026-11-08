---
source: https://www.youtube.com/watch?v=FfT5VTfHj_s
video_id: FfT5VTfHj_s
channel: Stanford Online
title: "Stanford AA228 Decision Making Under Uncertainty | Autumn 2025 | Bayesian Structure Learning"
scraped: 2026-08-28
tags: [decisions, bayesian networks, structure learning, parameter learning, markov equivalence]
---
# Stanford AA228 Decision Making Under Uncertainty | Autumn 2025 | Bayesian Structure Learning

This lecture teaches how to learn both the parameters and the directed structure of a Bayesian network from data, using maximum likelihood estimation, Bayesian scoring, local search algorithms, and Markov equivalence classes.

## Procedure / models distilled
- A Bayesian network compactly represents a joint distribution by encoding conditional independence assumptions as a directed acyclic graph (DAG).
- Use the notation: $X_i$ is a discrete random variable; $R_i$ is the number of possible instantiations of $X_i$; $Q_i$ is the number of parental instantiations of $X_i$; and $\pi_{ij}$ is the $j$-th parental instantiation of $X_i$'s parents.
- Compute $Q_i$ as the product of $R$ values of $X_i$'s parents; if $X_i$ has no parents, then $Q_i = 1$.
- Network parameters are $\theta_{ijk} = P(X_i = k \mid \pi_{ij})$; total parameters are $\sum_i R_i Q_i$ and independent parameters are $\sum_i (R_i - 1) Q_i$.
- For parameter learning with known structure, maximum likelihood estimate is $\hat{\theta}_{ijk} = \frac{m_{ijk}}{\sum_{k'} m_{ijk'}}$, where $m_{ijk}$ counts observations of $X_i = k$ under parental instantiation $j$.
- Use Bayesian parameter learning with Dirichlet priors to avoid assigning zero probability to events absent from the observed data.
- The Bayesian score for structure learning decomposes additively over nodes as the product of each node's marginal likelihood given its parents, enabling efficient local scoring.
- K2 search is a greedy hill-climbing structure-learning algorithm that starts from an empty graph and iteratively adds the edge that most improves the Bayesian score.
- General local search over DAGs uses three graph operations: add an edge, delete an edge, or flip an edge; each operation must be checked to preserve acyclicity.
- Escape local optima in structure search with randomized restarts, simulated annealing (occasionally accepting lower-scoring neighbors with decreasing probability), or genetic algorithms (population-based crossover and mutation of adjacency matrices).
- Two DAGs are Markov equivalent if and only if they share the same undirected edges and the same set of immoral v-structures (v-structures whose two parents are not connected).
- Because Markov equivalence classes are far smaller than the space of all DAGs, structure search can operate over equivalence classes rather than individual graphs for computational savings.
- Markov equivalent graphs can still receive different Bayesian scores unless the prior hyperparameter $\kappa = \sum_j \sum_k \alpha_{ijk}$ is constant across the equivalence class.

## Failure modes named
- Maximum likelihood estimation can assign zero probability to plausible but unobserved events, especially with sparse data.
- Greedy local search is prone to getting stuck in local optima rather than finding the globally best graph.
- Genetic-algorithm reproduction of adjacency matrices can produce cyclic graphs, so offspring must be checked or resampled until acyclicity is restored.
- Markov equivalence does not guarantee identical Bayesian scores across equivalent graphs.

## Studio relevance
04 leverage - how the studio uses this card
