---
source: https://www.youtube.com/watch?v=9eJQQVrUUoI
video_id: 9eJQQVrUUoI
channel: Peter Holderrieth
title: "MIT 6.S184: Flow Matching and Diffusion Models - Lecture 01 - Flow and Diffusion Models (2026)"
scraped: 2026-08-28
tags: [network-science, generative-models, flow-matching, diffusion-models, stochastic-differential-equations]
---
# MIT 6.S184: Flow Matching and Diffusion Models - Lecture 01 - Flow and Diffusion Models (2026)

This lecture formalizes generative modeling as sampling from a data distribution by transporting samples from a standard Gaussian through continuous-time flow (ODE) or diffusion (SDE) dynamics, establishing the mathematical objects that later lectures will train.

## Procedure / models distilled
- Represent images, videos, and protein structures as high-dimensional vectors by flattening their numerical arrays so that “generating an object” becomes “generating a vector.”
- Frame successful generation as sampling from the data distribution, where the quality of a generated sample is approximated by its likelihood under that distribution.
- Use a finite dataset as an empirical approximation of the true data distribution, and treat drawing a training example as sampling from it.
- Build a generative model by mapping a simple initial distribution—usually a standard multivariate Gaussian—through a learned transformation so that the output follows the data distribution.
- Construct a flow model as an ordinary differential equation x_dot = v_t(x) where v_t is a time-dependent neural-network vector field that deterministically evolves noise into data.
- Sample from a flow model by discretizing the ODE, starting from Gaussian noise and iteratively stepping in the direction of the learned vector field until the endpoint resembles a data sample.
- Extend a flow model to a diffusion model by replacing the ODE with a stochastic differential equation dx = v_t(x)dt + σ_t dW, adding scaled Gaussian noise at each step to the deterministic drift.
- Set the diffusion coefficient σ_t as a fixed, time-dependent schedule rather than a learned neural network; setting σ_t to zero recovers the deterministic flow ODE.
- Simulate a diffusion model with the same vector-field steps as a flow model, but with an added Gaussian noise term scaled by √h σ_t at each discretization step.
- Treat the vector field as the core object and the diffusion term as an optional extension that can increase trajectory diversity; an SDE produces a distribution over trajectories, not a single path.
- Defer conditional generation p_data(x|y)—for example, text-conditioned image generation—until after unconditional generation is understood, because conditioning is easier once the base distribution is modeled.

## Failure modes named
- Evaluating generated samples by subjective quality instead of formalizing quality as likelihood under the data distribution.
- Expecting a single noise-to-data neural-network call to train stably at scale; current practice relies on iterative flow or diffusion simulation because efficient one-step training algorithms remain elusive.
- Treating diffusion as a separate core mechanism rather than as a stochastic extension of the underlying flow vector field.
- Learning the diffusion coefficient with a neural network or making it state-dependent when standard flow and diffusion models use a fixed, time-dependent schedule.
- Assuming ODE and SDE final distributions differ in entropy; in principle both target the same data distribution, and observed differences come from training or simulation error.
- Confusing the finite training set with the true data distribution, which obscures questions of memorization versus true novelty in generated samples.

## Studio relevance
02 frame - use this card to frame generative modeling as continuous probability transport between a Gaussian prior and a data distribution via ODE/SDE dynamics.
