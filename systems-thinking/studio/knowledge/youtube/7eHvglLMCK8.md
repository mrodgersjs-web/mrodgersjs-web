---
source: https://www.youtube.com/watch?v=7eHvglLMCK8
video_id: 7eHvglLMCK8
channel: Reinhard Diestel: Graph theory lectures
title: "Graph Theory, Lecture 1: Introduction"
scraped: 2026-08-28
tags: [mathematics, graph theory, combinatorics, proofs, mathematical-modeling]
---
# Graph Theory, Lecture 1: Introduction

The lecture introduces graph theory by motivating the formal definition of a graph through concrete problems (wire cube, map coloring, committee scheduling), then presents and proves the Euler tour theorem using a maximal non-repeating walk argument.

## Procedure / models distilled
- Model a concrete relationship problem as a graph by identifying objects as vertices and adjacency or incidence as edges.
- Define a graph formally as an ordered pair G = (V, E) where V is a set of vertices and E is a set of two-element subsets of V, i.e., edges are unordered pairs of vertices.
- Recognize that the same intuitive situation admits multiple equivalent formalizations; choose one definitive definition and translate others as needed.
- Use graph coloring to encode resource scheduling or map coloring: adjacent vertices must receive different colors, and the chromatic number gives a lower bound on required resources.
- Verify Euler tour existence by checking that the graph is connected and that every vertex has even degree.
- Build a non-repeating walk greedily from any edge; because all vertex degrees are even, any maximal such walk is automatically closed.
- Extend a closed non-repeating walk to cover all edges by splicing in a walk from an uncovered edge to the existing tour, exploiting connectedness.
- Cast a graph theorem as induction over the natural number n by stating it as: for every n, every graph with exactly n edges satisfying some property has some conclusion.
- When an attempted inductive decomposition breaks a premise such as connectedness, pivot to a direct proof using an extremal principle such as a longest walk.
- Practice precision by treating definitions literally rather than relying on the intuitive picture, because graph-theoretic statements are fragile to small wording changes.
- Distinguish real-world plausibility arguments from mathematical proofs by first formalizing the situation into a mathematical model.

## Failure modes named
- Confusing a real-world plausibility argument with a mathematical proof before the situation has been formalized in a model.
- Letting pictures replace precise definitions and assuming "I can see how it goes" is sufficient.
- Making small wording changes in statements or definitions without noticing that graph theory is not robust against them.
- Deleting edges in an induction step and assuming all premises, especially connectedness, are preserved without checking.
- Assuming an inductive decomposition automatically produces a common vertex between substructures when it may not.
- Treating induction as a mechanical algebraic "n to n+1" trick rather than a universally quantified statement over all objects of size n.
- Copying uncritically from the board when the speaker flags that an error is present.
- Confusing a closed non-repeating walk with an Euler tour without verifying that every edge is covered.

## Studio relevance
05 ground - foundational definitions and proof patterns for modeling relationships, paths, and constraints as graphs.
