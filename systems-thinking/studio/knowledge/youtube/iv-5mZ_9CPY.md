---
source: https://www.youtube.com/watch?v=iv-5mZ_9CPY
video_id: iv-5mZ_9CPY
channel: 3Blue1Brown and Welch Labs
title: "But how do AI images and videos actually work? | Guest video by Welch Labs"
scraped: 2026-08-28
tags: [network-science, diffusion-models, generative-ai, latent-space, contrastive-learning]
---
# But how do AI images and videos actually work? | Guest video by Welch Labs

This video explains how text-to-image and text-to-video diffusion models work by treating generation as reversing a physics-inspired diffusion process, using CLIP to create a shared text-image latent space, and using conditioning plus classifier-free guidance to steer random noise toward prompt-aligned outputs.

## Procedure / models distilled
- Diffusion models generate images or videos by transforming pure random noise into structured outputs through an iterative reverse-time process that is mathematically analogous to running Brownian motion backward in high-dimensional space.
- A concrete video-generation pipeline such as WAN 2.1 begins with frames of random pixel intensities and repeatedly passes them through a transformer that outputs a less-noisy video; that output is added back to the input and fed through the model again for many steps.
- CLIP jointly trains a text encoder and an image encoder on 400 million image-caption pairs using a contrastive objective: matching image-text pairs are pulled together in a 512-dimensional embedding space while non-matching pairs are pushed apart.
- CLIP measures embedding similarity with cosine similarity, so related captions and images end up pointing in similar directions in the shared latent space.
- The geometry of CLIP's latent space supports semantic vector arithmetic: subtracting the embedding of an image without an object from the embedding of the same image with the object yields a vector aligned with the word for that object.
- DDPM training does not teach the network to undo one noise-addition step at a time; instead it predicts the total noise epsilon that was added to a clean image X0, effectively jumping across intermediate steps.
- During DDPM sampling, random noise must be re-added after each denoising prediction before the next iteration; omitting this re-sampling step produces blurry, low-quality outputs.
- Modern diffusion models can be reinterpreted as learning a time-varying vector field whose trajectories form a probability flow ODE that pushes samples from noise toward the data manifold.
- Conditioning injects a text, image, or class embedding into the diffusion model as an extra input so it learns context-dependent denoising, for example through cross-attention or by appending the embedding to the input.
- Classifier-free guidance decouples the generic data-manifold direction from the prompt-specific direction by randomly dropping conditioning during training; at inference it subtracts the unconditional vector field from the conditioned one and scales the difference by a guidance scale alpha.
- Negative prompting extends classifier-free guidance by explicitly encoding unwanted features and subtracting that vector field, as in WAN's standard negative prompt used to suppress artifacts like extra fingers or backward walking.

## Failure modes named
- The naive step-by-step denoising model, where the network is trained to reverse exactly one noise-addition step at a time, does not work well in practice and is not how modern diffusion models are built.
- Removing the re-sampling noise line from the DDPM generation algorithm collapses image quality, producing tiny, sad, blurry outputs.
- Conditioning alone is insufficient for strong prompt adherence; it may produce the right context but omit the requested subject entirely.
- Training with explicit class labels alone forces the model to learn both the global data structure and the class-specific structure simultaneously, which can overpower the class signal and produce confused, misclassified generations.
- Running the model without any conditioning yields a generic average-of-data result rather than the specific concept requested in the prompt.

## Studio relevance
04 leverage - the studio uses this card to apply the diffusion-conditioning-guidance triad as a reusable generative-system design pattern.
