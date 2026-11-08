---
source: https://www.youtube.com/watch?v=BSOOBxPyMcE
video_id: BSOOBxPyMcE
channel: DIBEOS
title: "Here’s How to Read Differential Equations"
scraped: 2026-08-28
tags: [mathematics, differential equations, mathematical modeling, equation reading]
---
# Here’s How to Read Differential Equations

The video teaches how to read a differential equation by first identifying what quantity is changing with respect to what, classifying the equation by type/order/linearity/homogeneity, and interpreting derivatives and right-hand sides geometrically or physically, using exponential growth, heat diffusion, and a forced damped harmonic oscillator as examples.

## Procedure / models distilled
- Start by locating every derivative symbol; a differential equation is, by definition, a statement that something is changing, so ask which variable is being tracked and with respect to which independent variable.
- Read a first derivative as a rate of change, slope, or velocity; read a second derivative as the rate of change of that rate, curvature, or acceleration.
- Distinguish an ODE (derivatives with respect to one independent variable) from a PDE (partial derivatives with respect to multiple independent variables) to determine how many variables the unknown function depends on.
- Determine the equation’s order from the highest derivative, its linearity by checking that the unknown and its derivatives appear only to first power with no nonlinear terms, and its homogeneity by whether the right-hand side equals zero.
- Read a nonzero right-hand side as an external forcing, source, or growth law; decide whether it depends on the unknown itself (internal dynamics) or only on the independent variable (external forcing).
- Interpret `dY/dT = kY` as “the larger Y is, the faster it changes,” giving exponential growth/decay and matching population growth, compound interest, and radioactive decay.
- Interpret the second spatial derivative `∂²U/∂x²` as curvature of U plotted against x, so `∂U/∂t = α ∂²U/∂x²` says U changes over time at a rate proportional to its spatial curvature; this is the heat/diffusion equation.
- Map the mechanical variables in a second-order ODE: `y(t)` is displacement, `y′(t)` is velocity, and `y″(t)` is acceleration; a term like `F₀ cos(ωt)` represents a periodic external force.
- Read the forced damped harmonic oscillator as an energy-balance statement: the external input must be distributed among acceleration, velocity/damping, and displacement/stiffness terms; at turning points velocity is zero so acceleration and displacement dominate.
- Don’t wait for a solution before extracting meaning; classify the equation, name the variables, and state the relationships first, because much of the behavior is already visible in the equation’s structure.
- Treat interpretation as a practiced skill rather than a single recipe: repeatedly ask “what is changing with respect to what?” and connect the symbols to known models (exponential growth, heat diffusion, forced damped harmonic oscillator).

## Failure modes named
- Solving before reading: trying to compute a solution before identifying what variables, derivatives, and relationships the equation expresses.
- Assuming the independent variable is time: treating `T` as time automatically instead of confirming what the variable actually represents in context.
- Confusing perspectives on change: interpreting behavior as periodic or quadratic depending on the chosen variables, while forgetting that “change is relative.”
- Missing the PDE signal: failing to notice partial-derivative symbols and therefore underestimating how many independent variables the unknown function depends on.
- Misclassifying order, linearity, or homogeneity: for example, overlooking that a nonzero right-hand side makes the equation non-homogeneous or that terms like `y²`, `sin y`, or `y·y′` destroy linearity.
- Treating every right-hand side term as internal dynamics: not recognizing an external forcing term when it depends only on the independent variable, such as `F(t)`.

## Studio relevance
03 diagnose - the studio uses this card to inspect differential equations for what changes with respect to what, classify their structure, and catch reading traps before attempting a solution.
