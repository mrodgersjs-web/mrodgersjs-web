---
source: https://www.youtube.com/watch?v=D1RzvXDXyqA
video_id: D1RzvXDXyqA
channel: Stanford
title: "Statistical Mechanics Lecture 1"
scraped: 2026-08-28
tags: [physics, statistical mechanics, entropy, probability, thermodynamics]
---
# Statistical Mechanics Lecture 1

This opening lecture frames statistical mechanics as probability theory applied to physical systems with incomplete information, introduces the rules of probability and entropy as a measure of ignorance, and maps entropy into both discrete and continuous phase-space settings.

## Procedure / models distilled
- When exact initial conditions and the laws of evolution for a closed system are known, deterministic prediction is possible; otherwise, resort to probabilistic/statistical prediction.
- Treat statistical mechanics as basic probability theory applied to systems whose components are too numerous, too small, or too coupled to track individually.
- Assign probabilities P(i) over a discrete space of outcomes or states; enforce P(i) ≥ 0 and Σ_i P(i) = 1.
- Use the law of large numbers as the physical bridge between probability and frequency: P(i) ≈ N_i/N for a very large number of trials or replicas.
- Compute the expected value of a state-dependent quantity as ⟨f⟩ = Σ_i P(i) f(i), which corresponds to an ensemble or long-run average.
- Measure ignorance by entropy: for M equally likely states, S = log M; for a general discrete distribution, S = −Σ_i P(i) log P(i).
- Entropy is additive only when subsystems are uncorrelated; correlations reduce conditional uncertainty and make entropy non-additive.
- For continuous classical phase space, normalize the probability density so its integral over all coordinates and momenta equals one, and define entropy as S = −∫ ρ(p,q) log ρ(p,q) dp dq.
- In the special case of a uniform probability blob in phase space, entropy reduces to the logarithm of the occupied phase-space volume.
- Adopt the principle of indifference: knowing nothing about the system means assigning equal probability to all accessible states, which implies no correlations between subsystems.
- Update probabilities when new information or conserved quantities are known; this introduces correlations among variables.
- Recognize that the base of the logarithm in entropy is a convention: base 2 gives bits (Shannon), base e is common in physics; they differ by a constant factor.
- Keep statistical entropy distinct from quantum uncertainty: it concerns ignorance of mixed/unknown states, not Heisenberg uncertainty of pure quantum states.

## Failure modes named
- Attempting exact microstate prediction for macroscopic systems yields useless, rapidly changing lists of positions and velocities.
- Expecting probability to hold for small trial counts; the law of large numbers fails when N is not large enough.
- Allowing or interpreting negative probabilities.
- Treating entropy as inherently quantized in integer bits; it is log n for n equally likely states and the base is conventional.
- Conflating information (without the minus sign) with entropy or lack of information (with the minus sign).
- Trying to sum rather than integrate over continuous phase-space probabilities.
- Confusing statistical entropy with Heisenberg quantum uncertainty.

## Studio relevance
02 frame - establishes a probabilistic frame for reasoning about macroscopic systems when microscopic details are unknowable, with entropy as the central measure of ignorance.
