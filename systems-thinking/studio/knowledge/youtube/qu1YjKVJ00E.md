---
source: https://www.youtube.com/watch?v=qu1YjKVJ00E
video_id: qu1YjKVJ00E
channel: Computational Linguistics
title: "Link Analysis: Betweenness centrality"
scraped: 2026-08-28
tags: [network-science, centrality, graph-theory, shortest-paths, directed-graphs]
---
# Link Analysis: Betweenness centrality

Betweenness centrality measures a node's importance by summing, over all pairs of other nodes, the fraction of shortest paths that pass through that node, with worked examples for undirected and directed graphs.

## Procedure / models distilled
- Treat a node's importance as proportional to how much information or flow passes through it along shortest paths.
- Use the formula BC(i) = Σ (σ_jk(i) / σ_jk) over all node pairs j and k with j ≠ k, where σ_jk is the total number of shortest paths from j to k and σ_jk(i) is the number of those paths that pass through i.
- Exclude the target node i itself from every node pair in the summation.
- For undirected graphs, count each unordered node pair only once; reverse-direction paths are identical.
- If a pair of nodes is disconnected and has no path, skip that pair because it contributes zero.
- For every connected pair, enumerate all shortest paths, not just a single one.
- For each pair, compute the ratio of shortest paths containing i to the total number of shortest paths.
- Add those ratios across all eligible pairs to obtain the node's betweenness centrality score.
- In directed graphs, apply the same formula but only count paths that follow the direction of edges.
- For directed graphs, drop any ordered source-target pair where the source cannot reach the target.
- A smoothing value can be used for unreachable pairs, but it does not change relative node differentiation and is usually omitted to reduce computation.
- Remember that this is one classical formulation from around the 1970s; several variants exist.

## Failure modes named
- Double-counting reverse paths in undirected graphs.
- Including the target node itself in the pair enumeration.
- Counting only one shortest path when multiple equally short paths exist.
- Treating directed edges as undirected when computing paths.
- Including unreachable node pairs in directed graphs instead of ignoring them.
- Expecting smoothing values for unreachable pairs to affect node ranking.

## Studio relevance
03 diagnose - maps gatekeeper and bottleneck nodes by measuring how much of a network's shortest-path traffic flows through each actor.
