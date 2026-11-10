---
source: https://www.youtube.com/watch?v=1igHpqYd3Vc
video_id: 1igHpqYd3Vc
channel: Lex Clips
title: "Limits of computation: Can emergent complexity be simulated? | Demis Hassabis and Lex Fridman"
scraped: 2026-08-28
tags: [physics, computation, emergence, ai, complexity]
---
# Limits of computation: Can emergent complexity be simulated? | Demis Hassabis and Lex Fridman

Demis Hassabis argues that many apparently intractable emergent phenomena in physics and biology are likely modelable on classical machines because reality operates on structured, learnable manifolds that neural networks can approximate via gradient descent.

## Procedure / models distilled
- Treat "emergent complexity" as a spectrum rather than a category: simple cellular automata and forward-simulable systems sit near the classical-modelable boundary, while chaotic systems with extreme sensitivity to initial conditions remain open problems.
- Use the "nature does it" heuristic: if a physical or biological process occurs in reality, it suggests an underlying efficient mechanism exists and can potentially be mimicked classically.
- Search for low-dimensional structure in high-dimensional possibility spaces rather than enumerating combinatorial options like 10^300 protein conformations.
- Frame intractable problems as energy-landscape navigation tasks where neural networks can follow gradients rather than as brute-force search problems.
- Assume complex outputs like protein folding, gene function, or fluid behavior are projections from structured latent manifolds that can be learned from data.
- Apply generative models to physical simulation domains traditionally handled by explicit solvers, such as fluid dynamics, Navier-Stokes, weather prediction, lighting, and material deformation.
- Reverse-engineer physical laws by training on observational data rather than hand-coding physics engines or mathematical constraints.
- Test the classical-modelability boundary by probing highly nonlinear dynamical systems, singularities, and chaotic regimes where initial-condition precision dominates outcomes.
- Use correct objective specification as a gating step: gradient following only works once the right target function and loss landscape are defined.
- Distinguish between "surprising classical success" (AlphaFold 3, AlphaGenome, Veo 3) and theoretically hard cases (chaos, singularities) to avoid overgeneralizing modelability.

## Failure modes named
- Equating combinatorial explosion with true intractability without checking for hidden structure or gradients.
- Treating all emergent phenomena as uniformly outside classical computation, ignoring that many emergent systems are efficiently forward-simulable.
- Brute-force enumeration of high-dimensional state spaces instead of learning the lower-dimensional manifold that generates observed behavior.
- Overlooking the importance of precise objective functions and loss landscapes in making complex physical problems tractable.
- Assuming that because fluid dynamics and weather systems are traditionally compute-intensive, they cannot be approximated well by learned generative models.

## Studio relevance
02 frame - recognize that apparent intractability of emergent systems often masks learnable low-dimensional structure, so scope problems by whether nature exposes a gradient rather than by combinatorial size.
