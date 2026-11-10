---
source: https://www.youtube.com/watch?v=0aqvVbTyEmc
video_id: 0aqvVbTyEmc
channel: Mod•U: Powerful Concepts in Social Science
title: "Closeness Centrality & Betweenness Centrality: A Social Network Lab in R for Beginners"
scraped: 2026-08-28
tags: [network-science, centrality, sna, r, social-networks]
---
# Closeness Centrality & Betweenness Centrality: A Social Network Lab in R for Beginners

This tutorial explains and contrasts closeness centrality (average shortest-path reach) and betweenness centrality (brokerage over shortest paths) as two distinct ways to identify strategically important positions in a social network.

## Procedure / models distilled
- Define closeness centrality as how close a node is to all other nodes in terms of average shortest-path length.
- Distinguish undirected global closeness from directed variants based on incoming or outgoing ties.
- Calculate closeness centrality only within a single connected component, because it requires reachable paths to all nodes.
- Define betweenness centrality as the summed fraction of all shortest paths between pairs of nodes that pass through a focal node.
- Identify high-betweenness nodes as bridges or brokers that connect otherwise separated subgroups.
- Compare degree, closeness, and betweenness results on the same network to see how each measure highlights different actors.
- Interpret each centrality score as a positional property rather than as a property of the named individual alone.
- Aggregate or composite multiple centrality results to form generalizable conclusions about network roles.
- Use R network-analysis tools to compute these centrality scores on a graph object.
- Report centrality findings as averages or patterns, emphasizing the impact of position over the specific person occupying it.

## Failure modes named
- Treating one centrality measure as the single definition of "importance" in a network.
- Assuming the same actor will be central across degree, closeness, and betweenness measures.
- Focusing on named individuals instead of the structural position they occupy.
- Reporting isolated raw scores without connecting them to generalizable positional patterns.
- Running global closeness centrality on a network with multiple disconnected components.
- Confusing directed in-closeness or out-closeness with the undirected global measure.

## Studio relevance
03 diagnose - the studio uses this card to diagnose positional importance, reach, and brokerage roles in a network before deciding where to intervene or leverage influence.
