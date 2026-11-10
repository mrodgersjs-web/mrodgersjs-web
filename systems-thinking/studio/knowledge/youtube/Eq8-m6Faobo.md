---
source: https://www.youtube.com/watch?v=Eq8-m6Faobo
video_id: Eq8-m6Faobo
channel: The Open Educator
title: "Fault Tree Analysis FTA Explained With Example Calculation"
scraped: 2026-08-28
tags: [risk-safety, reliability-engineering, probability, safety-analysis, systems-engineering]
---
# Fault Tree Analysis FTA Explained With Example Calculation

A concise walkthrough of Fault Tree Analysis as a top-down, probabilistic method for quantifying system safety by combining basic event probabilities through AND/OR logic gates.

## Procedure / models distilled
- Start with a top-level undesired event (e.g., "fire burns down the plant") and decompose it downward into contributing causes and basic events.
- Use an AND gate when all input events must occur simultaneously for the top event to happen; mathematically, multiply the probabilities of the input events.
- Use an OR gate when any one input event is sufficient to produce the output event; mathematically, calculate 1 minus the product of (1 − P) for each input event.
- Identify "basic events" — the lowest-level failures or conditions for which raw probabilities are available (e.g., smoking, spark, short-circuit, fuel present, oxygen present).
- Ensure all probabilities refer to the same time frame or mission interval before combining them.
- Propagate probabilities upward gate by gate, starting from the leaves and moving toward the top event.
- Interpret the final top-event probability as a quantitative measure of system risk or unreliability for the chosen scenario.
- Recognize that FTA was originally developed at Bell Labs in the 1960s for U.S. Air Force missile reliability and later adopted by NASA for safety analysis.
- Keep the tree structure readable by using standard gate symbols (AND / OR) and clearly labeling each intermediate and basic event.

## Failure modes named
- Treating OR-gate probabilities as simple sums instead of using the complement-of-no-failure rule (1 − product of complements).
- Confusing AND and OR logic, which respectively require all inputs or any single input to trigger the next event.
- Combining probabilities that are defined over inconsistent time horizons.
- Assuming independence of basic events when real-world failures may be correlated.

## Studio relevance
03 diagnose - maps how subsystem failures combine probabilistically to produce a top-level system hazard.
