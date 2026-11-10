---
source: https://www.youtube.com/watch?v=GncgOIiMII8
video_id: GncgOIiMII8
channel: Hello Interview
title: "Recommendation System Infra Basics 1"
scraped: 2026-08-28
tags: [engineering, recommendation-systems, vector-search, candidate-generation, system-design]
---
# Recommendation System Infra Basics 1

Modern large-scale recommendation systems split the problem into candidate generation, ranking, and reranking so that a full ML score over billions of items becomes tractable.

## Procedure / models distilled
- Treat the core scoring function as a black-box ML ranker that, given a user and an item, returns the probability or score that the user will engage with it.
- Recognize that applying this ranker to every item in a billion-scale catalog is computationally infeasible; it would require an impractical amount of time or resources.
- Split the overall pipeline into three stages: candidate generation, ranking, and reranking, each with a distinct responsibility and cost profile.
- Use candidate generators as heuristic filters that take user or item signals and produce a small, plausible subset of items to be scored by the ranker.
- Combine candidates from multiple generators into a single candidate set before ranking, so the ranker only scores hundreds or thousands of items instead of billions.
- Leverage embedding models to map users and items into dense vectors where proximity corresponds to similarity in taste, content, or behavior.
- Store precomputed item embeddings in a vector database and use approximate-nearest-neighbor algorithms (e.g., HNSW) to retrieve similar items quickly instead of scanning the whole catalog.
- Build separate embeddings and indexes for different semantic notions of similarity, such as “videos similar to this one” or “videos liked by users similar to me.”
- Operationalize the system with many specialized candidate-generator indexes, and treat their management as a core software-engineering problem.
- Reserve the reranking stage for business rules, privacy filters, exploration boosts, and other tweaks that are too expensive or awkward to encode inside candidate generation.
- Over-generate candidates in ranking (e.g., produce 25) and let reranking trim or reorder to the final requested count (e.g., 10).
- Apply the layered-system design pattern: solve the common case well in earlier stages, then add a final adjustment layer rather than forcing one stage to handle every edge case perfectly.

## Failure modes named
- Scoring every user-item pair online is too slow and consumes too many resources for billion-scale catalogs.
- Precomputing all recommendations offline would require impossibly large storage and would still leave new users without fresh results.
- A non-exhaustive candidate generator can omit good items, so the ranker is only as good as the candidates it sees.
- Embedding-based exact nearest-neighbor search over the full catalog is too slow; production systems need approximate indexes.
- Encoding every edge case (e.g., blocked creators, sensitive content, exploration boosts) into candidate generators makes them inefficient and hard to maintain.
- Trying to design a single stage that solves 100% of the problem is usually more expensive than a 99% core solution plus a final correction layer.

## Studio relevance
02 frame - how the studio uses this card to decompose massive recommendation problems into candidate generation, ranking, and reranking stages.
