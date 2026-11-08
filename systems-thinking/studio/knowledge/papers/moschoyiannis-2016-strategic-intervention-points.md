---
source: https://arxiv.org/abs/1608.00655
paper_id: arXiv:1608.00655
title: "A Web-based Tool for Identifying Strategic Intervention Points in Complex Systems"
authors: "Sotiris Moschoyiannis, Nicholas Elia, Alexandra S. Penn, David J. B. Lloyd, Chris Knight"
year: 2016
venue: "arXiv"
citation_count: null
tags: [systems-thinking, leverage-points, intervention, fuzzy-cognitive-mapping, network-controllability]
type: paper-note
---
# A Web-based Tool for Identifying Strategic Intervention Points in Complex Systems

## Claim

Strategic steering of a complex system is hard because (a) the system's exact architecture is unclear and (b) data to operationalize interaction rules is scarce. Combining Fuzzy Cognitive Mapping (FCM) with network controllability theory addresses both: FCM represents the system as a weighted complex network of factors; controllability analysis then yields minimal control configurations — small subsets of factors (system levers) that suffice to steer the system.

## Method

Analytical pipeline: elicit factors and weighted causal links into an FCM, treat the FCM as a complex network, apply network-controllability results to compute minimal driver-factor sets, and implement the combination in a web-based analysis tool.

## Studio relevance

- **leverage**: this is the computational counterpart to Meadows' leverage points — instead of a philosophical ladder, an algorithm that outputs minimal subsets of factors to act on. Pair both: Meadows ranks *where* qualitatively, controllability picks *which nodes* concretely.
- **frame**: the FCM step is a structured way to capture a framed system (factors + signed weighted links) that is stricter than a freehand CLD.
- **ground**: citable method when an intervention claim needs computational backing.
