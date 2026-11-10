---
source: https://www.youtube.com/watch?v=1wa9lysIaD8
video_id: 1wa9lysIaD8
channel: SAIConference
title: "Tutorial - Agent Based Modelling In Python"
scraped: 2026-08-28
tags: [complexity, agent-based modeling, python, mesa, simulation, emergence]
---
# Tutorial - Agent Based Modelling In Python

A hands-on introduction to agent-based modeling in Python with Mesa, using the Boltzmann wealth model to show how local agent interactions generate emergent system behavior and inform policy interventions.

## Procedure / models distilled
- Frame ABM as generative science: grow a system inside a computer to explain macro behavior from micro interactions rather than relying on closed-form equations.
- Build models with object-oriented classes: define an Agent class for individual behavior and a Model class to orchestrate the simulation.
- Instantiate a model with a scheduler (e.g., random activation) and a spatial grid so agents act, move, and interact in discrete time steps.
- Encode local rules in agents (e.g., the Boltzmann wealth exchange: pick another agent and give one unit of wealth).
- Use Mesa's data collector to record agent-level and model-level variables at each step, creating a virtual laboratory for exploration.
- Run batch simulations and parameter sweeps across ranges of agent counts, grid sizes, and initial conditions to map the search space.
- Analyze output to compare simulated patterns (e.g., wealth distribution, Gini plots) against real-world statistics as a validity check.
- Treat visualization as a diagnostic tool: inspect grid heat maps and time series to spot unexpected dynamics.
- Recognize that recreating real-world statistics is necessary but not sufficient—multiple interaction structures can produce the same outcome.
- Leverage Python's ecosystem to integrate Mesa with machine learning, deep learning, geospatial, and data libraries.
- Use modular add-ons like Mesa-Data and Mesa-Behaviors to pull real-world data (e.g., WorldPop population data, crop-yield datasets, SIR epidemic structures) and reusable agent behaviors.
- Approach model building as the primary learning mechanism: the process reveals which interactions drive emergent behavior.

## Failure modes named
- Equating "growing" the target output with understanding the system, since many different micro-rules can produce the same macro pattern.
- Treating a model's output as a direct policy prescription rather than a tool for probing dynamics.
- Underestimating parameter sensitivity: ABMs are highly parameterized and require sweeps rather than single runs.
- Expecting Python/Mesa to match the raw speed of C++/Java for billions-of-agent simulations because of the GIL.
- Letting ML models that were trained on historical data break when novel system behaviors appear (e.g., pandemic shocks).
- Building invalid synthetic populations from raw data artifacts (e.g., fractional people in a grid cell) without cleaning and smoothing.

## Studio relevance
06 synthesize - the studio uses this card to assemble agent rules, spaces, and data into runnable generative models that reveal how local interactions produce emergent system behavior.
