---
source: https://www.youtube.com/watch?v=-rE3DfeZ_jE
video_id: -rE3DfeZ_jE
channel: SciPy
title: "Allen Downey - Long-tailed distributions in the natural and engineered world | SciPy 2023"
scraped: 2026-08-28
tags: [risk-safety, statistics, distributions, modeling, visualization]
---
# Allen Downey - Long-tailed distributions in the natural and engineered world | SciPy 2023

Long-tailed distributions are common in natural and engineered systems, and naïve models that look fine on linear scales can massively underestimate the probability of extreme, high-impact events.

## Procedure / models distilled
- Plot the tail distribution (survival function: % exceeding a threshold) rather than relying only on a histogram, because tails are where rare disasters live.
- When data spans many orders of magnitude, put the x-axis on a log scale so the distribution moves into the middle of the plot instead of mashing against the axes.
- Put the y-axis on a log scale to act as a "microscope" for extreme values and reveal tail behavior that linear plots hide.
- Use paired linear/log-y plots: linear for the body/normal cases, log-y for the extremes, since each view exposes different model-data discrepancies.
- Start with a log-normal fit, but treat a good-looking linear-scale fit as insufficient evidence; check it on log-log scales.
- Fit a log-T distribution (Student's t applied to the logarithms of values) as an alternative; its degrees of freedom ν controls tail thickness (ν ≈ 1 → very long tails, ν → ∞ → Gaussian).
- Estimate ν from data to match both the body and the tail; e.g., ν ≈ 3.5 fit disaster costs and earthquake magnitudes well.
- Predict extreme quantiles only after validating the model in the tail, not just the center of the distribution.
- Look for generative mechanisms that produce long tails: preferential attachment / Matthew effect, self-organized criticality, and mixtures of distributions with different variances.
- Propagate uncertainty through simulations of physical processes with variable filters (e.g., asteroid-size distribution → crater-size distribution) to understand why tails persist.
- Distinguish "tameable" Black Swans (gray swans) from untameable ones by assessing whether you have enough data, the right model shape, and relevant physical theory.
- Check log-log plots for curvature as a diagnostic that your chosen distribution shape is misspecified.
- Add physical bounds or filters when domain knowledge supports them (e.g., an upper limit on solar flare energy) to trim unrealistic tails.
- Recognize that Student-T models can under- or over-predict tails depending on curvature, so neither error direction is automatically safer.

## Failure modes named
- Linear-scale plots hide tail risk by compressing extreme events against the axis, making models look adequate when they are not.
- Log-normal models drastically underestimate the probability of rare, large disasters and earthquakes when evaluated on log-log scales.
- Concluding that a model fits the data because it looks reasonable on a linear scale.
- Extrapolating many orders of magnitude beyond the data without mechanistic grounding.
- Treating all Black Swan events as equally predictable or equally impossible to predict.
- Over-relying on purely statistical models when the underlying physics is unknown.
- Treating over-prediction of tail risk as harmless when it can lead to over-budgeting and misallocated resources.
- Ignoring systematic curvature on log-log plots as a signal of model misspecification.
- Applying models with infinite support to strictly positive quantities without a log transform or domain constraint.

## Studio relevance
03 diagnose - the studio uses this card to detect when a system that appears normal on linear scales may actually harbor underestimated extreme-event risk in its tail.
