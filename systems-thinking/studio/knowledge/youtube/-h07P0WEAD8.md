---
source: https://www.youtube.com/watch?v=-h07P0WEAD8
video_id: -h07P0WEAD8
channel: ⭐ The Geometry Code   --Ananta Geometry ⭐
title: "Designing LLM Systems — Part III Search → RAG Systems Top-K → Graph Expansion: Smarter AI Retrieval"
scraped: 2026-08-28
tags: [engineering, rag, graph-based-retrieval, multi-hop-reasoning]
---
# Designing LLM Systems — Part III Search → RAG Systems Top-K → Graph Expansion: Smarter AI Retrieval

The video reframes RAG as a planner-driven, multi-step reasoning system that combines graph-based chunking with dynamic multi-hop retrieval to synthesize connected answers instead of isolated search results.

## Procedure / models distilled
- Model RAG not as a one-shot search but as a planner-driven multi-step workflow that orchestrates context gathering and synthesis.
- Treat every chunk as a node and every explicit relationship as an edge, converting flat data into a hierarchical knowledge graph.
- Use graph traversal retrieval to expand from an initial chunk into its pre-built neighborhood and pull related context for a query.
- Decompose complex queries with multi-hop reasoning: parse the query, identify the first logical hop, retrieve data, evaluate context, then formulate the next query iteratively.
- Contrast graph-based chunking (single-step, pre-built structure, faster, medium flexibility) with multi-hop linking (multi-step, dynamic chain, slower, high flexibility).
- Implement a production orchestration flow: planner retrieves initial data, expands via the graph, reasons through nodes with multi-hop logic, assembles full context, and sends it to the LLM.
- Prioritize link quality in graph construction because good links enable powerful reasoning and bad links inject noise.
- Cap planner depth at an optimal two to three hops to keep orchestration fast and efficient.
- Apply a scoring strategy that ranks chunks by relevance, connectivity, and confidence.
- Offset graph-traversal latency with caching so retrieval remains performant.
- Adopt the mindset shift that flat chunks store data while connected chunks create knowledge, engineering relationships so the system can reason.

## Failure modes named
- One-shot RAG requests inherently miss context and lead to hallucinations.
- Flat, isolated chunks lack relational context and produce incomplete answers.
- Bad-quality graph links pump noise into the retrieval pipeline instead of enabling reasoning.
- Uncapped multi-hop depth inflates latency and can dilute the final context.
- Firing a single-step LLM query and hoping for the best produces far more errors than planner-driven multi-step orchestration.

## Studio relevance
04 leverage - use this card to design RAG pipelines that replace flat retrieval with graph expansion and multi-hop planners.
