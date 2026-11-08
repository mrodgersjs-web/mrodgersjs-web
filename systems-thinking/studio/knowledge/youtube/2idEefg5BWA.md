---
source: https://www.youtube.com/watch?v=2idEefg5BWA
video_id: 2idEefg5BWA
channel: Building Intuition
title: "Dynamical Systems"
scraped: 2026-08-28
tags: [mathematics, state-space, linear-systems, control-theory]
---
# Dynamical Systems

A dynamical system is a rule for updating a state vector over time, from simple one-dimensional exponential models to multidimensional linear dynamical systems and beyond.

## Procedure / models distilled
- Define a dynamical system as a rule that updates the state over time.
- Start with the simplest one-dimensional model: the rate of change of V is proportional to V (dV/dt = cV).
- Recognize that the one-dimensional exponential-growth model is analytically solvable.
- Generalize to a multidimensional state vector X whose rate of change is given by X-dot = AX, where A is a matrix.
- Identify this matrix form as a linear dynamical system (LDS), a broad class for modeling state evolution.
- Treat the state as an n-dimensional vector of variables that together describe what is happening in the system.
- Choose state variables to represent concrete, measurable aspects of a real system (e.g., position, velocity, engine RPM, gear, fuel level, distance to destination).
- Model control as an update policy that repeatedly takes the current state and computes the next state at fixed intervals to move toward a goal.
- Check whether the relationships among state variables are linear before using an LDS; if they are not, use a nonlinear model instead.
- Use LDS when the entire state evolution can be expressed as a linear matrix transformation of the current state.
- Distinguish between analytically tractable one-dimensional systems and more complex multidimensional or nonlinear systems.

## Failure modes named
- Modeling a clearly nonlinear task with a linear dynamical system because the LDS framework is convenient.
- Trying to linearly relate state variables that have no natural linear relationship, such as distance to destination and engine RPM.
- Forgetting that the matrix A in an LDS is constrained to linear, n-by-n transformations of the state vector.

## Studio relevance

02 frame - use this card to frame real-world systems as evolving state vectors and to judge when linear update rules are appropriate versus when nonlinear dynamics are required.
