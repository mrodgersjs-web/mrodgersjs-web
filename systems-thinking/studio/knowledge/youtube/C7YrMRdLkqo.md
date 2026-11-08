---
source: https://www.youtube.com/watch?v=C7YrMRdLkqo
video_id: C7YrMRdLkqo
channel: Dr. Trefor Bazett
title: "Intro to Graph Theory | Definitions & Ex: 7 Bridges of Konigsberg"
scraped: 2026-08-28
tags: [mathematics, graph theory, combinatorics, networks]
---
# Intro to Graph Theory | Definitions & Ex: 7 Bridges of Konigsberg

Euler's Königsberg bridge puzzle motivates the formal definition of a graph as vertices and edges, the use of multisets for repeated connections, and the invariance of graph structure under relabeling and redrawing.

## Procedure / models distilled
- Model a land-and-bridge puzzle by collapsing each land mass into a single point (vertex) and each bridge into a connection (edge) between two points.
- Define a graph formally as a pair G = (V, E), where V is a set of vertices and E is a collection of edges.
- Treat each edge as a two-element subset of vertices, specifying which two vertices it connects.
- Use a multiset rather than a plain set for E when multiple edges connect the same pair of vertices, because repetitions matter while order does not.
- Strip away geographic details such as exact locations and the shapes of paths, retaining only the abstract connectivity.
- Recognize that the same graph can be drawn in many different ways in the plane without changing its underlying structure.
- Identify graph isomorphism as the process of relabeling or spatially rearranging vertices while preserving every connection.
- Apply graph models to real-world networks, such as representing people as vertices and friendships as edges.
- Defer the full solution to a walkability puzzle until definitions and theorems like vertex degree are established.

## Failure modes named
- Concluding that a path does not exist merely because one has not been found, rather than proving impossibility.
- Treating the particular drawing or labeling of a graph as an intrinsic property of the graph itself.
- Forgetting that edge collections can contain repeated pairs, unlike ordinary sets where duplicates collapse.

## Studio relevance
02 frame - provides a relational-framing vocabulary for turning concrete network puzzles and systems into abstract vertex-edge models that are invariant under relabeling and redrawing.
