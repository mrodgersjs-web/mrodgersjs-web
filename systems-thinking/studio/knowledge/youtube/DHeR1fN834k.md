---
source: https://www.youtube.com/watch?v=DHeR1fN834k
video_id: DHeR1fN834k
channel: Fengqi You
title: "Plenary Lecture of ESCAPE 28 - Prof. Fengqi You (Cornell Univ)"
scraped: 2026-08-28
tags: [decisions, resilience, process-design, robust-optimization, chemical-engineering]
---
# Plenary Lecture of ESCAPE 28 - Prof. Fengqi You (Cornell Univ)

The lecture presents a design-and-synthesis perspective on resilience for chemical process systems, using a quantitative resilience metric and a multi-level adaptive robust optimization framework that integrates optimal design, capacity expansion, parallel units, backup units, and adaptive operation to trade off economics against disruption recovery.

## Procedure / models distilled
- Quantify resilience as the ratio of actual post-disruption performance area to nominal performance area over time, bounded between 0 (no recovery) and 1 (fully resilient).
- Model process unit capacity as discrete step functions so the continuous resilience integral reduces to summations over time and units.
- Frame resilience-enhanced design as a here-and-now decision problem using binary variables to select units, pathways, and configurations before disruptions are observed.
- Enhance resilience by installing extra capacity on downstream units so they can absorb rerouted feed when upstream units fail.
- Introduce redundancy through parallel units: splitting capacity across smaller units improves partial survival and faster recovery.
- Deploy protected or sheltered backup units to hedge against correlated site-wide hazards such as floods and hurricanes.
- Use optimal operating levels as a recourse strategy to adapt flows and loads after a disruption is realized.
- Formulate the integrated problem as a multi-level adaptive robust optimization that simultaneously optimizes economics and resilience.
- Solve the problem with a combination of a parametric algorithm and column-and-constraint generation to produce converging upper and lower bounds.
- Generate Pareto curves of cost versus resilience to support decision makers in choosing an acceptable trade-off.
- Treat resilience analysis as an add-on decision-support layer rather than a mandatory requirement, avoiding dependence on precise event probabilities.

## Failure modes named
- Designing only for minimum cost yields processes whose resilience can drop to zero after a disruption and require full recovery time before any production resumes.
- Assuming backup units can simply be placed next to primary units ignores correlated site-wide hazards like flooding; backup units need physical shelter or geographic separation.
- Requiring accurate probability distributions for rare high-impact events can block resilience analysis, because data scarcity makes stochastic-programming-style probability estimates unreliable.
- Treating resilience as solely a process-control problem misses the opportunity to embed recoverability into the design and synthesis stage.
- Assuming that any single resilience enhancement strategy dominates; different designs may need different combinations of extra capacity, parallel units, and backups.

## Studio relevance
06 synthesize - the studio uses this card to integrate resilience trade-offs, robust optimization framing, and multi-level design decisions into systems-level recommendations.
