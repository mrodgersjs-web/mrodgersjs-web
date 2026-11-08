---
source: https://www.youtube.com/watch?v=1zIIcYfp5QA
video_id: 1zIIcYfp5QA
channel: Christopher Lum
title: "Introduction to Full State Feedback Control"
scraped: 2026-08-28
tags: [engineering, control-theory, state-space, pole-placement, linear-systems]
---
# Introduction to Full State Feedback Control

Full-state feedback uses the simple static control law **u = –Kx** on a linear state-space plant, producing closed-loop dynamics **ẋ = (A – BK)x** whose eigenvalues can be placed almost anywhere if the pair (A, B) is controllable.

## Procedure / models distilled
- Represent the plant in linear state-space form: **ẋ = Ax + Bu**, **y = Cx + Du**.
- Assume full state measurement: **C = I** and **D = 0**, so the output equals the entire state vector.
- Define the full-state feedback control law as **u = –Kx**, where K is a constant gain matrix.
- Close the loop by substituting the control law into the plant to get **ẋ = (A – BK)x**.
- Label the closed-loop system matrix **A_CL = A – BK** and treat it as an autonomous/homogeneous system.
- Recognize that the transient behavior of the closed-loop system is governed by the eigenvalues of **A_CL**.
- Check controllability of the pair (A, B) before attempting pole placement.
- Use pole placement to choose K so that **eig(A – BK)** match desired closed-loop pole locations.
- For single-input systems, the K that achieves a given pole set is unique.
- For multi-input systems, many K matrices can place the same poles, leaving extra design freedom.
- Exploit the extra freedom in multi-input systems to weight or limit individual control inputs/actuator efforts.
- Compute K numerically with tools such as MATLAB’s `place(A, B, p)` and verify with `eig(A - B*K)`.
- Compare full-state feedback to PID/root locus: there is no constrained root-locus path; poles can be moved directly to arbitrary locations.
- View full-state feedback first as a **regulator**, since it drives nonzero initial conditions to zero without a reference input.
- Note that the architecture is purely proportional in the state: the current control depends only on the current state.

## Failure modes named
- Assuming all states are measurable when in practice only a subset or noisy combinations are available.
- Attempting pole placement on an uncontrollable pair (A, B), which cannot achieve arbitrary eigenvalue locations.
- Ignoring actuator saturation, control effort, or cost when choosing K, especially with multi-input systems.
- Treating any arbitrary pole location as physically achievable without considering unmodeled dynamics, delays, or nonlinearities.
- Assuming the K returned by a numerical solver is the only valid K when multiple solutions exist.
- Confusing the regulator form with a tracking controller that follows a reference signal.
- Forgetting to verify that the computed K actually places the poles at the desired locations.

## Studio relevance
04 leverage - how the studio uses this card
