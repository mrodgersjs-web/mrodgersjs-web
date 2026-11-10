---
source: https://www.youtube.com/watch?v=FUqzdvlaoRk
video_id: FUqzdvlaoRk
channel: New Machina
title: "What are LLM Scaling Laws ?"
scraped: 2026-08-28
tags: [engineering, llm-scaling, compute-optimal-training, resource-allocation, ai-research]
---
# What are LLM Scaling Laws ?

LLM scaling laws describe the predictable relationship between model performance and three scaled resources—parameters, training data, and compute—while noting that bottlenecks in any one dimension are historically overcome by innovations in compute or architecture.

## Procedure / models distilled
- Define LLM scaling laws as predictable performance improvements that follow scaling curves when model size, training data, or compute is increased.
- Identify the three scalable resources: number of model parameters, size of the training dataset, and total training compute.
- Recognize that scaling laws primarily apply to large models trained from scratch, though their principles can inform small-model and distilled-model training.
- Distinguish distilled models from standard scaled models: they bypass strict scaling laws because teacher-student transfer lets them outperform equivalently sized non-distilled models.
- Apply the principle of balanced scaling: maximizing performance requires jointly increasing parameters, data, and compute rather than pushing one dimension alone.
- Use the Chinchilla paper’s finding that, for a fixed compute budget, smaller models trained on much more data can outperform larger models trained on less data.
- Treat the Chinchilla result as evidence that optimal training requires balancing model size against training data volume.
- Expect larger, more-data-rich models to generalize better and to need fewer downstream examples for high task performance.
- When scaling slows, diagnose whether the bottleneck is compute capacity, data availability, or model architecture rather than assuming the law has broken.
- Overcome compute bottlenecks by adopting new hardware paradigms, as the shift from CPUs to GPUs did in the early 2000s.
- Overcome architecture bottlenecks by introducing new model architectures, as the Transformer did in 2017.
- Extend scaling-law thinking beyond LLMs to deep learning models in general.
- Evaluate future architectures like Mixture of Experts (MoE)—e.g., DeepSeek’s 256-expert MoE with 8 active experts per token—as potential ways to push the scaling curve further.
- Monitor data availability as a future bottleneck, since current LLMs increasingly train on all available real-world text, and consider synthetic data as one mitigation.
- Track compute investment trends as an indicator of continued frontier-model scaling, noting heavy hyperscaler and startup spending into early 2025.

## Failure modes named
- Scaling only one or two of parameters, data, or compute while neglecting the others, causing diminishing returns.
- Training a very large model on a limited dataset, which underperforms a smaller model trained on more data for the same compute budget.
- Assuming scaling laws hold strictly for distilled or small models without accounting for teacher-student transfer effects.
- Treating temporary slowdowns in scaling gains as permanent limits rather than as bottlenecks addressable by compute or architecture innovation.
- Overlooking data exhaustion as an emerging bottleneck as available real-world training data is consumed.

## Studio relevance
02 frame - how the studio uses this card
