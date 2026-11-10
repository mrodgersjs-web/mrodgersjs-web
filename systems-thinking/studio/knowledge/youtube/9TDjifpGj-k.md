---
source: https://www.youtube.com/watch?v=9TDjifpGj-k
video_id: 9TDjifpGj-k
channel: CrashCourse
title: "You Know I'm All About that Bayes: Crash Course Statistics #24"
scraped: 2026-08-28
tags: [mathematics, bayesian inference, hypothesis testing, conditional probability]
---
# You Know I'm All About that Bayes: Crash Course Statistics #24

This Crash Course episode introduces Bayes’ Theorem as a formal rule for updating beliefs with new evidence and extends it to Bayesian hypothesis testing via priors, likelihoods, posteriors, and Bayes factors.

## Procedure / models distilled
- **Bayes’ Theorem**: compute a conditional probability as P(A|B) = P(B|A) · P(A) / P(B), noting the numerator equals P(A and B).
- **Quantify gut feelings with base rates**: plug known conditional and marginal probabilities into Bayes’ Theorem to replace intuition with a calculated probability (e.g., P(male | breast cancer)).
- **Belief updating**: treat Bayes’ Theorem as a mechanism for revising a prior belief after observing new data, producing a posterior belief.
- **Bayesian hypothesis testing via ratios**: compare two competing hypotheses by taking the ratio of their posterior probabilities rather than calculating a single probability.
- **Bayes Factor**: measure the strength of evidence by the ratio P(data | H₁) / P(data | H₂), representing how much the observed data favors one hypothesis over another.
- **Posterior odds formula**: update prior odds by multiplying them by the Bayes Factor: posterior odds = prior odds × Bayes Factor.
- **The three core components**: identify the prior (belief before evidence), the likelihood (how probable the evidence is under each hypothesis), and the posterior (belief after evidence).
- **Accommodate subjective priors**: recognize that different people can start with different priors and therefore reach different posteriors from the same evidence.
- **Report Bayes Factors for transparency**: because priors are subjective, researchers should report the Bayes Factor so others can apply their own priors to the same evidence.
- **Convergence under sufficient evidence**: when evidence is strong and neither prior is 0%, divergent priors typically converge toward the same posterior conclusion because the likelihood overwhelms the prior.
- **Iterative updating**: use each posterior as the prior for the next round of evidence, since “yesterday’s posterior is today’s prior.”
- **Natural-world applications**: apply the same update logic to medical diagnosis (flu vs. cold given symptoms), risk assessment (sushi parasite risk from repeated healthy meals), and interpersonal judgment (revising beliefs about a friend’s kindness).

## Failure modes named
- **Base-rate neglect / gut over math**: relying on intuition alone instead of quantifying base rates and computing the conditional probability.
- **Mistaking Bayesian outputs for pure objectivity**: ignoring that the prior is subjective and can drive the final conclusion.
- **Hiding the Bayes Factor**: reporting only posterior odds without the Bayes Factor prevents others from checking the evidence against their own priors.
- **Drawing firm conclusions from weak evidence**: when data are scarce, the posterior remains dominated by the prior, so small samples can produce divergent conclusions.
- **Dogmatic zero-probability priors**: assigning a prior probability of 0% to a hypothesis makes it impossible for any evidence to ever update that belief.

## Studio relevance
03 diagnose - the studio uses this card to trace how priors and evidence combine into posterior beliefs so it can locate why different models or stakeholders diverge and what evidence would make them converge.
