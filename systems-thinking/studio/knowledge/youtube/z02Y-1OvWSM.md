---
source: https://www.youtube.com/watch?v=z02Y-1OvWSM
video_id: z02Y-1OvWSM
channel: AI Impact
title: "Don't Use Karpathy's Second Brain (I BUILT SOMETHING BETTER)"
scraped: 2026-08-28
tags: [productivity, knowledge-management, ai, second-brain]
---
# Don't Use Karpathy's Second Brain (I BUILT SOMETHING BETTER)

The video argues that human-oriented "second brain" PKMs like PARA waste AI tokens and hurt retrieval, then proposes an "infinite brain" knowledge graph built from atomic notes, 16 typed nodes, and 10 semantic edge types so AI can find and reason over only the context it needs.

## Procedure / models distilled
- Treat your personal knowledge graph as the primary knowledge base you feed to AI; without it, AI advice stays generic and mediocre.
- Build the graph from small, interlinked text files so it can scale to thousands or millions of nodes.
- Keep notes atomic: target 50-300 tokens per note, splitting longer topics into numbered parts.
- Replace the four PARA buckets with 16 typed nodes: pillars, decisions, concepts, questions, playbooks, tasks, events, patterns, hypotheses, facts, sources, bookmarks, notes, contacts, references, and custom.
- Add typed edges/relationships between nodes so the AI knows the nature of each link: supports, contradicts, depends on, derived from, related to, part of, preceded by, followed by, authored, and tagging.
- Use node type and edge type as retrieval signals so the AI can scope exactly the knowledge it needs before reading full text.
- Let AI do the setup, organization, classification, and retrieval rather than manually curating the graph.
- Link every decision, hypothesis, and fact back to its sources so the chain of reasoning is traceable.
- Summarize each node in one sentence so the AI can decide in roughly 50 tokens whether to spend more tokens diving deeper.
- Preserve institutional knowledge in the graph so it outlives the current team and can onboard future members.
- Query the graph by starting from a typed node and following relevant edges instead of asking the AI to read long documents.
- Convert existing PARA-style vaults into the infinite-brain structure with migration prompts.

## Failure modes named
- Using PARA (Projects, Areas, Resources, Archives) for AI: it was designed for human folder navigation, not AI retrieval.
- Long, undifferentiated notes that force the AI to consume thousands of tokens and may confuse it with unrelated back-and-forth context.
- Untyped links that hide whether a connection supports, contradicts, depends on, or simply precedes another idea.
- Poor scope retrieval: the AI cannot quickly find "the pricing decision made on this date" inside a giant pricing document.
- Wasted tokens and higher API costs as free tiers disappear and long-context pricing becomes a constraint.
- Trying to manually build and maintain a PKM without enough time, leading to abandonment.
- Asking generic chat AI for advice without giving it your business context, decisions, and industry knowledge.
- Conflating operational grouping (PARA) with semantic/epistemic grouping needed for reasoning.

## Studio relevance
04 leverage - use this card to convert scattered notes and decisions into an AI-readable infinite-brain graph with typed nodes and semantic edges.
