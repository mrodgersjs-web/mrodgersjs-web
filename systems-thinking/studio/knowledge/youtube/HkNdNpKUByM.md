---
source: https://www.youtube.com/watch?v=HkNdNpKUByM
video_id: HkNdNpKUByM
channel: TrevTutor
title: "INTRODUCTION to GRAPH THEORY - DISCRETE MATHEMATICS"
scraped: 2026-08-28
tags: [mathematics, graph theory, discrete mathematics, networks]
---
# INTRODUCTION to GRAPH THEORY - DISCRETE MATHEMATICS

The video introduces the foundational vocabulary and proof techniques of graph theory by defining graphs as vertex-edge structures and distinguishing incidence, adjacency, directionality, walks, trails, paths, cycles, connectedness, components, and simple graphs.

## Procedure / models distilled
- Define a graph G as an ordered pair (V,E): a set of vertices (dots) and a set of edges (lines or arrows) connecting them.
- Distinguish incidence (an edge is incident to the two vertices it joins) from adjacency (two vertices are adjacent when an edge directly connects them) and isolation (a vertex with no incident edges).
- Classify graphs as undirected, where each edge is an unordered set {a,b} = {b,a}, or directed, where each edge is an ordered pair (a,b) with a tail at a and a head at b so direction matters.
- Model multiple edges between the same vertices as multiplicity in undirected graphs or as distinct ordered pairs in directed graphs; keep multigraphs separate from simple graphs.
- Define a walk from x to y as an alternating sequence of vertices and edges that follows the graph; a closed walk has x=y, and the trivial walk stays at one vertex with no edges.
- Define a trail as a walk that never repeats an edge, and a circuit as a closed trail; crossing the same edge twice disqualifies a trail.
- Define a path as a walk that never repeats a vertex, and a cycle as a closed path where only the start/end vertex may repeat.
- Check connectivity by verifying that an xy-path exists for every pair of vertices x,y; decompose disconnected graphs into components (κ(G)) by counting maximal connected subgraphs.
- Prefer paths over arbitrary walks when testing connectivity because any walk contains a shortest path once repeated vertices are removed.
- Prove that an xy-walk implies an xy-path by contradiction: take a minimal walk and, if a vertex repeats, delete the loop between its first and second appearance to obtain a shorter walk.
- Identify a simple graph as undirected, loop-free, and without multiple edges; every other case is a multigraph (or pseudograph) and analyzed separately.
- Bound edges in a simple graph by e ≤ C(v,2), because each edge chooses two distinct vertices from v, giving 2e ≤ v²−v.
- Carry out separate proofs for directed and undirected properties because the edge objects differ even when the intuition looks similar.

## Failure modes named
- Treating "walk," "trail," "path," "circuit," and "cycle" as interchangeable in everyday language, causing formal errors.
- Counting the shared start/end vertex of a cycle as a repeated vertex violation; it is allowed in a cycle.
- Assuming edge AB equals edge BA in a directed graph; (a,b) and (b,a) are distinct.
- Reusing an edge back and forth and calling it a trail; trails forbid repeated edges.
- Calling a graph connected because walks exist; connectedness requires paths (no repeated vertices) for every pair.
- Forgetting that loops and multiple edges disqualify a graph from being simple.
- Trying to prove directed-graph statements with undirected arguments (or vice versa) without checking edge definitions.
- Wasting computation by enumerating all walks instead of trimming repeated vertices to extract a path.

## Studio relevance
02 frame - models systems as vertices and edges, then selects the right walk/trail/path/cycle abstraction to frame connectivity and constraints.
