---
source: https://www.youtube.com/watch?v=2ZHuj8uBinM
video_id: 2ZHuj8uBinM
channel: The Alan Turing Institute
title: "Social network analysis - Introduction to structural thinking: Dr Bernie Hogan, University of Oxford"
scraped: 2026-08-28
tags: [physics, social-network-analysis, network-science, graph-theory, structural-thinking]
---
# Social network analysis - Introduction to structural thinking: Dr Bernie Hogan, University of Oxford

An introductory lecture on structural thinking that reframes social science problems from collections of independent individuals to networks of relationships, drawing on both sociological social network analysis and physics-derived network science.

## Procedure / models distilled
- Treat relationships, not isolated individuals, as the primary data: dependencies between cases are the phenomenon to be explained.
- Distinguish the sociology-derived social network analysis tradition from the physics-derived network science tradition, while letting each inform the other.
- Bridge micro-level behavior and macro-level phenomena by specifying concrete network structure rather than relying on abstract metaphors like “culture” or “institutions.”
- Remove the ego from ego-network visualizations because the ego connects to everyone and obscures structure among alters.
- Identify isolates and single-event ties in personal networks as low-structure noise rather than meaningful social structure.
- Use two-mode (bipartite) networks when two classes of entities interact, such as people and posts, or legislators and committees.
- When projecting a two-mode network to a one-mode network, weight edges by co-occurrence frequency and trim low-weight ties to avoid noisy complete graphs.
- Detect communities by exploiting triadic closure: repeated iterations in random networks naturally produce clustered structure through triangle formation.
- Understand community detection as modularity maximization, where communities emerge when internal ties exceed what would be expected at random.
- Assess anomalous or outlier nodes by examining community centrality or by bootstrapping community detection to see which nodes switch allegiance across runs.
- Model diffusion, fads, and epidemics as network phase transitions: estimate the connectivity threshold at which a virus or innovation saturates the network.
- Compare actors using structural equivalence (same neighbors) or regular equivalence (similar roles) when looking for the same actor across time or networks.
- Combine network position with domain context before inferring behavior; structural position alone is rarely sufficient for causal or threat interpretation.

## Failure modes named
- Running standard regression on networked cases as if they were independent observations.
- Treating platform data such as Facebook friendship maps as a perfectly representative map of the world, ignoring bans, real-name policies, and selection bias.
- Adding the ego to an ego-network visualization, which destroys information about ties among alters.
- Projecting a two-mode network to one mode without weighting or trimming, producing a noisy near-complete graph.
- Cutting a community-detection dendrogram at an arbitrary threshold, hiding uncertain or anomalous nodes.
- Using structural equivalence or high betweenness alone to identify threat actors, as in the “pizza guy” problem where high betweenness reflects a social role rather than malicious intent.
- Over-interpreting large-scale network visualizations as complete representations without accounting for missing populations, state intervention, or platform effects.

## Studio relevance
02 frame - reframe aggregates of apparently independent actors as relational systems and choose the right projections, weights, and thresholds before modeling.
