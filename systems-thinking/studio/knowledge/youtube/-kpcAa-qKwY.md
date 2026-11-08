---
source: https://www.youtube.com/watch?v=-kpcAa-qKwY
video_id: -kpcAa-qKwY
channel: The Programming Piglet
title: "Genetic algorithms explained in 6 minutes (...and 28 seconds)"
scraped: 2026-08-28
tags: [biology, genetic algorithms, optimization, machine learning, evolutionary computation]
---
# Genetic algorithms explained in 6 minutes (...and 28 seconds)

The video explains genetic algorithms as a survival-of-the-fittest optimization method that evolves a population of candidate solutions through fitness selection, crossover, and mutation to solve problems faster than random guessing.

## Procedure / models distilled
- Genetic algorithms replace pure random guessing with an evolutionary search that favors better partial solutions.
- A candidate solution is encoded as a DNA strand made of discrete genes, such as a sequence of movement actions.
- The first step is to create an initial population by randomly combining available genes.
- A fitness function measures how close each candidate gets to the goal, e.g., distance traveled toward the park exit.
- The fittest members of the population are selected to become parents for the next generation.
- Crossover combines parent DNA to produce child DNA, taking information from both parents.
- Any crossover scheme works as long as children inherit genes from multiple parents.
- Mutation randomly changes some genes after crossover to introduce variation that parents did not have.
- Repeating selection, crossover, and mutation creates successive generations that improve over time.
- The loop stops when a candidate reaches a solution that solves the problem.
- Mutation rate is a tunable balance between exploration and exploitation.

## Failure modes named
- Without mutation, the population can get stuck in a local minimum because children can never inherit genes the parents lacked.
- A mutation rate that is too high makes the search explore too much and ignore good parent solutions, slowing competence.
- A mutation rate that is too low makes learning fast but also makes it hard to escape local minima once nearby.

## Studio relevance
04 leverage - use this card as a step-by-step template for designing evolutionary search loops and tuning mutation rates.
