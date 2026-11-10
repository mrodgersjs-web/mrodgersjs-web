---
source: https://www.youtube.com/watch?v=8jwrX3o_MNk
video_id: 8jwrX3o_MNk
channel: SSD(Physics,Math and Engineering)
title: "Intuitively know the behaviour of this 1st order ODE.Part1:intuitive (more on description)"
scraped: 2026-08-28
tags: [mathematics, differential equations, exponential decay, time constant, first-order systems]
---
# Intuitively know the behaviour of this 1st order ODE.Part1:intuitive (more on description)

The video reads the qualitative behavior of the first-order linear ODE `dv/dt = -v/τ`, confirms it by integration to `V(t) = V₀e^(-t/τ)`, and interprets the time constant τ and the 5τ rule.

## Procedure / models distilled
- Identify a first-order ODE by checking that no second- or higher-order derivatives appear.
- Rearrange the equation to `dv/dt = -(1/τ)v` so the rate is visible as a multiple of the state.
- Read the sign of the rate: if `v` is positive, `dv/dt` is negative, so `v` must decrease.
- Interpret `dv/dt` as the slope of the `v` versus `t` graph.
- Notice that the slope magnitude `|dv/dt| = |v|/τ` shrinks as `v` shrinks, so the curve flattens rather than staying straight.
- Reject a straight-line decay graph because a straight line has constant slope, while the equation demands a decreasing slope.
- Check the axis crossing: when `v = 0`, `dv/dt = 0`, so the state cannot change sign; for a positive initial value, `v` stays non-negative and approaches zero asymptotically.
- Solve by separation of variables: integrate `dv/v = -(1/τ)dt` from `V₀` at `t=0` to `V` at `t` to obtain `ln(V/V₀) = -t/τ`.
- Write the explicit solution `V(t) = V₀e^(-t/τ)`, an exponential decay function.
- Graph the solution as a curve starting at `V₀`, falling monotonically, and asymptotically approaching the time axis without ever touching it in finite time.
- Define the time constant τ: at `t = τ`, `V = V₀/e ≈ 0.367 V₀` (36.7% of the initial value).
- Use the 5τ rule of thumb: at `t = 5τ`, `V ≈ 0.00673 V₀`, so engineers conventionally treat the transient as finished.
- Map the equation to a physical example: a charged capacitor discharging through a resistor.

## Failure modes named
- Treating the decay as linear (constant slope) instead of slope-proportional.
- Extrapolating the curve below zero and assuming `v` becomes negative.
- Believing the variable reaches exactly zero in finite time.
- Using `5τ` as mathematically zero rather than “practically zero.”
- Treating the time constant τ as an arbitrary constant without the 36.7% reference.

## Studio relevance
03 diagnose - the studio uses this card to infer the qualitative trajectory of a first-order stock from its rate equation before integrating, checking sign, slope change, and asymptote.
