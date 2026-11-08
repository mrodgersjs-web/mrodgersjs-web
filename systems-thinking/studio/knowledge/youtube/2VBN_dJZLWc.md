---
source: https://www.youtube.com/watch?v=2VBN_dJZLWc
video_id: 2VBN_dJZLWc
channel: Institute for Pure & Applied Mathematics (IPAM)
title: "Steve Brunton: \"Dynamical Systems (Part 1/2)\""
scraped: 2026-08-28
tags: [mathematics, dynamical-systems, control-theory, model-reduction, machine-learning]
---
# Steve Brunton: "Dynamical Systems (Part 1/2)"

An introductory survey of dynamical systems as rule-governed processes that evolve in time, covering state-space formalism, model reduction, and control from classical feedback to modern learning-based methods.

## Procedure / models distilled
- Define a dynamical system as any system that changes in time according to rules, and model it by choosing a state vector that gives the minimal instantaneous description needed to predict future behavior.
- Write continuous-time dynamics as `dx/dt = f(x, t, u, β)` and discrete-time dynamics as `x_{k+1} = f(x_k)`, treating `f` as a vector field that encodes the physics and constraints of the system.
- Treat the state as memoryless: the future (or its derivative) depends only on the current state, not on the full history, so include enough variables to make this true.
- Recognize high-dimensional nonlinear multiscale dynamical systems—fluids, brains, climate, disease spread, social networks—by their evolution in both space and time.
- Simplify such systems by finding effective coordinates or models (mean-field, linear, probabilistic, etc.) that capture dominant patterns and support design, optimization, or control objectives.
- Classify control strategies as passive (no energy input, e.g., a stop sign) versus active (energy input, e.g., a stoplight), and as open-loop versus closed-loop feedback.
- Use closed-loop feedback by measuring outputs, comparing them with model predictions, and adjusting the input to stabilize unstable dynamics, compensate for uncertainty, and reject disturbances.
- Apply PID control as the classical industrial default for feedback regulation.
- Use model predictive control (MPC) by repeatedly solving a finite-horizon constrained optimization, applying only the first control action, then re-optimizing from the new state.
- Tune MPC trade-offs among prediction horizon, control-application interval, and final horizon based on available computation and system time scales, preferring the fastest adequate model over the most accurate slow one.
- Combine deep learning with MPC to build deep model predictive controllers: fast learned models wrapped inside a real-time nonlinear optimization with constraints.
- Apply reinforcement learning to learn a value landscape over states/actions for complex combinatorial tasks, but seed it with known physics or inductive bias to achieve practical sample efficiency.

## Failure modes named
- Modeling a history-dependent system as Markovian by using too small a state, e.g., predicting stock prices from current prices alone without trend or external context.
- Studying an isolated brain or agent outside its body and environment, which misses the coupled dynamics that actually matter for behavior.
- Relying on open-loop control for unstable or uncertain systems: it cannot stabilize an inverted pendulum under disturbances and overreacts to noise, like a toaster that burns the second slice because the model ignores residual heat.
- Running MPC with a poor or too-slow model, producing bad trajectories or missing real-time deadlines.
- Applying reinforcement learning to physical systems without physics-aware inductive bias, leading to extreme sample inefficiency and unstable or unsafe behavior.

## Studio relevance
02 frame - provides the conceptual vocabulary to frame real-world phenomena as state-space dynamical systems with feedback, control, and reduction opportunities.
