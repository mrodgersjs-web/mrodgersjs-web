---
source: https://www.youtube.com/watch?v=0Rpy-xSsAo8
video_id: 0Rpy-xSsAo8
channel: Jason Bramburger
title: "The Lorenz Equations - Dynamical Systems | Lecture 27"
scraped: 2026-08-28
tags: [physics, chaos, dynamical-systems, lorenz-attractor]
---
# The Lorenz Equations - Dynamical Systems | Lecture 27

This lecture introduces the three-dimensional Lorenz system as a deceptively simple model of convection, derives its symmetries, fixed points, pitchfork and subcritical Hopf bifurcations, and explains how volume contraction and homoclinic orbits give rise to transient and fully developed chaos.

## Procedure / models distilled
- Start by writing the Lorenz system as a 3D ODE with parameters σ (Prandtl number), r (Rayleigh number), and b (aspect ratio), and note that only two quadratic nonlinear terms are present.
- Exploit the flip symmetry (x, y, z) → (−x, −y, z) to conclude that solutions come in symmetric pairs or lie on the invariant z-axis.
- Compute the divergence of the vector field to show volume contraction, then use it to conclude the flow is dissipative, phase-space volumes shrink to zero, and no fully unstable repellers can exist.
- Locate fixed points: the origin always exists, plus a pair C± that appear for r > 1 at a pitchfork bifurcation.
- Linearize at the origin to get eigenvalues −b and roots λ² + (σ + 1)λ + σ(1 − r) = 0, showing the origin loses stability as r crosses 1.
- Linearize at C± and track their eigenvalues to find a subcritical Hopf bifurcation at r = r_H, where C± lose stability and an unstable limit cycle is born.
- Build a reduced bifurcation diagram with r on the horizontal axis and x on the vertical axis, because a full six-dimensional plot is impossible.
- Trace the unstable limit cycle backward in r: it grows and attaches to the origin as a homoclinic orbit near r = 1, then disconnects as r increases.
- Identify transient chaos in the window 1 < r < r_H with standard σ and b: trajectories look chaotic before eventually settling to C+ or C−.
- Identify the full butterfly chaotic attractor for r > r_H, where no stable fixed points or simple limit cycles exist.
- Use the standard values σ = 10, b = 8/3, r_H ≈ 24.74, and simulate at r = 28, recognizing that computer simulation becomes essential beyond local bifurcation analysis.
- Reference Tucker's 1999 computer-assisted proof as the accepted demonstration that the standard Lorenz attractor is chaotic.

## Failure modes named
- The "looks simple" trap: assuming low-degree polynomial equations guarantee easy analysis.
- Trying to plot a full six-dimensional bifurcation diagram instead of fixing σ and b and projecting onto x versus r.
- Believing chaos has a single universally agreed-upon definition; the lecture notes there is no single agreed definition.
- Attempting to fully analyze the chaotic regime with pencil and paper alone; numerical/computational investigation is required.
- Overlooking volume contraction and then expecting repellers or volume-filling attractors in phase space.

## Studio relevance
06 synthesize - this card synthesizes 1D/2D dynamical-systems concepts into the canonical 3D Lorenz example and maps where analytical, numerical, and computer-assisted methods each take over.
