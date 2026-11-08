---
source: https://www.youtube.com/watch?v=UsB70Tf5zcE
video_id: UsB70Tf5zcE
channel: AI Engineer
title: "Training an LLM from Scratch, Locally — Angelos Perivolaropoulos, ElevenLabs"
scraped: 2026-08-28
tags: [engineering, llm-training, tokenization, audio-models, transformer-architecture]
---
# Training an LLM from Scratch, Locally — Angelos Perivolaropoulos, ElevenLabs

A hands-on walkthrough of training a tiny GPT-2-style causal transformer from scratch in PyTorch, emphasizing tokenizer choice, architecture, training loop, and how the same principles extend to audio and multimodal models.

## Procedure / models distilled
- Train a small decoder-only causal language model from scratch using pure PyTorch, with no pretrained weights, to learn the full LLM stack end to end.
- Pick a tokenizer whose vocabulary size matches your data scale; for tiny datasets use character-level tokenization to keep the token space small and ensure bigram coverage.
- Implement the tokenizer as a simple string-to-integer lookup, then feed those integer token ids into an embedding layer to create model inputs.
- Build a GPT-2-style architecture: decoder-only transformer with causal self-attention, MLP blocks, residual connections, and layer normalization.
- Run the training loop on CPU, Apple Silicon MPS, or CUDA, adjusting batch size to available RAM; 16 GB is sufficient for this small model.
- Treat the training loop—data mix, optimization, and post-training—as the primary performance lever, since architecture differences between model generations are often smaller than training differences.
- Recognize that vocabulary size drives data requirements: with N tokens you need roughly N² examples to cover bigrams, so a large tokenizer on small data will not converge.
- Perform inference directly from the trained checkpoint; at this scale the model is small enough to run locally on any supported device.
- Set a random seed for reproducibility even with greedy decoding, because sampling operations and other non-obvious RNG calls can still vary.
- Learn audio tokenizers from data representations such as mel spectrograms rather than hand-designing tokens, and match the tokenizer domain to the training set (speech vs. music).
- Choose task-appropriate loss functions: cross-entropy for text, L2 on spectrograms for TTS, KL divergence for distillation, and other specialized losses for post-training.
- Handle multimodal inputs by routing each modality through a domain encoder and injecting its final hidden states as embedding vectors into the text transformer's input sequence.

## Failure modes named
- Adopting a large/subword tokenizer with too little data so the model never sees enough token co-occurrences to converge.
- Focusing on architecture while underestimating the impact of the training loop, data mix, and post-training recipe.
- Skipping random seed setup because you assume greedy decoding is fully deterministic.
- Using cross-entropy loss for audio or other non-text modalities where L2, KL divergence, or domain-specific losses are needed.
- Trying to hand-craft audio tokens instead of training a tokenizer on learned spectral representations.
- Expecting a character-level model to scale beyond toy settings, since individual characters carry weaker semantic correlations than subwords.

## Studio relevance
06 synthesize - the studio uses this card as a compact end-to-end reference for building minimal LLMs from scratch and for mapping tokenization and loss choices across text, audio, and multimodal domains.
