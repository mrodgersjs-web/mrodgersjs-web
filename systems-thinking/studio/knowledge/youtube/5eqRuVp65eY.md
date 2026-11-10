---
source: https://www.youtube.com/watch?v=5eqRuVp65eY
video_id: 5eqRuVp65eY
channel: Welch Labs
title: "AI can't cross this line and we don't know why."
scraped: 2026-08-28
tags: [engineering, ai, scaling-laws, deep-learning]
---
# AI can't cross this line and we don't know why.

The video explains neural scaling laws—empirical power-law relationships between compute, data, model size, and cross-entropy loss—and explores the manifold hypothesis as a theoretical explanation, while noting limits like irreducible entropy and the unpredictable emergence of capabilities.

## Procedure / models distilled
- As models scale, error vs. compute forms a family of curves; on log-log axes these define a straight compute-optimal frontier that no individual model can cross.
- Neural scaling laws state that cross-entropy loss scales as a power law with compute, model size, and dataset size, largely independent of architecture when reasonable choices are made.
- Autoregressive language models are trained to predict the next token by outputting a probability vector over the vocabulary, normalized with softmax.
- Cross-entropy loss is computed as the negative natural logarithm of the model’s assigned probability at the index of the true next token.
- Cross-entropy loss cannot reach zero because natural data, especially language, has irreducible entropy—many valid next tokens exist for the same context.
- To account for flattening curves, fit a power law plus an irreducible error term; the constant estimates the entropy of the data distribution.
- Empirical scaling-law fits were used to forecast GPT-3 and GPT-4 performance across roughly 13 orders of magnitude of training compute.
- A three-term decomposition separates loss into a model-size term, a data-size term, and an irreducible entropy term; DeepMind estimated an irreducible text entropy near 1.69 nats.
- The manifold hypothesis treats natural data as a lower-dimensional surface embedded in high-dimensional input space, where nearby points are semantically similar.
- A neural network can be viewed as learning to map high-dimensional inputs onto a lower-dimensional manifold whose geometry encodes meaning.
- Resolution-limited scaling argues that more data or larger models let the network resolve the data manifold more finely; worst-case error scales as D^(-2/d) and cross-entropy as D^(-4/d), where d is the manifold’s intrinsic dimension.
- Theory matches observed exponents for synthetic data and small image datasets, but natural-language scaling implies an intrinsic dimension (~42) below empirical manifold estimates (~100), showing weaker agreement.
- Scaling laws reliably predict next-token loss but do not predict when specific capabilities such as arithmetic, reasoning, or word unscrambling will emerge.

## Failure modes named
- Treating empirical scaling laws as discovered fundamental laws of nature rather than artifacts of current deep-learning practice.
- Expecting cross-entropy loss to reach zero while ignoring the irreducible entropy of natural language and other data.
- Reading a linear-scale scaling plot as strong evidence of curvature without remapping to the appropriate log-log view.
- Using next-token loss scaling as a proxy for predicting the emergence of specific model behaviors or capabilities.
- Assuming that because aggregate loss improves smoothly, all important model abilities will improve smoothly and predictably.

## Studio relevance
03 diagnose - the studio uses this card to distinguish scaling-limited performance gaps from irreducible-entropy and manifold-structure limits before committing resources.
