---
source: https://www.youtube.com/watch?v=3yqVGWLXhk8
video_id: 3yqVGWLXhk8
channel: CabbageCat
title: "Natural Evolution Strategy (NES) part 1: Evolution gradient; the log-likelihood trick"
scraped: 2026-08-28
tags: [biology, optimization, evolutionary-algorithms, machine-learning, gradient-estimation]
---
# Natural Evolution Strategy (NES) part 1: Evolution gradient; the log-likelihood trick

This video explains the Evolution Gradient algorithm, which explicitly maximizes expected fitness under a search distribution by deriving a Monte Carlo gradient estimate via the log-likelihood trick, and notes that the Natural Evolution Strategy will address its update instability.

## Procedure / models distilled
- Evolution Gradient is a population-based optimizer that alternates between sampling from a probability distribution and updating its parameters.
- Unlike simple Evolution Strategies, which implicitly improves the distribution by selecting high-fitness elites, Evolution Gradient treats the problem as an explicit objective maximization problem.
- The objective is to maximize expected fitness: J(θ) = E_{z~p(z|θ)}[f(z)] = ∫ f(z) p(z|θ) dz, where θ parameterizes the search distribution.
- θ can represent any distribution parameters; for a Gaussian it is the mean μ and covariance Σ, which can be flattened into one vector or updated separately.
- The fitness function f(z) is treated as a black box: we can query inputs and outputs but do not know its internal mathematical form.
- Directly computing the gradient is intractable because p(z|θ) is a product term and the integral over the unknown black-box f cannot be solved analytically.
- The log-likelihood trick rewrites ∇_θ p(z|θ) as p(z|θ) ∇_θ log p(z|θ), converting the integral into an expectation.
- The gradient is estimated by Monte Carlo sampling: (1/λ) Σ_{i=1}^λ f(z_i) ∇_θ log p(z_i|θ).
- Taking the log converts products into sums, simplifying gradient computation and avoiding the need for product or quotient rules.
- For a Gaussian distribution, the general formula specializes to updates for the mean and covariance by substituting the Gaussian PDF.
- The update rule shifts the distribution to make high-fitness samples more probable and low-fitness samples less probable.
- The final update is structurally analogous to policy gradient in reinforcement learning, with fitness replaced by Q-value and the PDF replaced by policy.

## Failure modes named
- Unstable updates, especially the covariance matrix swirling around before eventually shrinking and converging on the optimum.
- Confusion between representing θ as one long flattened vector versus separate mean and covariance updates; both are equivalent.
- Attempting to solve the integral analytically for a black-box fitness function is a trap; the algorithm must rely on sampling instead.

## Studio relevance
06 synthesize - bridges population-based evolutionary search with explicit gradient-based optimization via the log-likelihood trick.
