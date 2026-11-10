---
source: https://www.youtube.com/watch?v=Gd7XuuFNnt4
video_id: Gd7XuuFNnt4
channel: Quick Tutorials
title: "Diffusion Models versus Generative Adversarial Networks (GANs) | AI Image Generation Models"
scraped: 2026-08-28
tags: [network-science, generative-ai, image-synthesis, diffusion-models, gans]
---
# Diffusion Models versus Generative Adversarial Networks (GANs) | AI Image Generation Models

The video contrasts GANs and diffusion models for image generation, highlighting GAN mode collapse and why diffusion models now dominate the field.

## Procedure / models distilled
- GANs use a generator deep-learning model that takes random noise as input and produces a synthetic image.
- In GANs, changing the input noise should ideally produce a different image, but it often does not.
- GANs can suffer from mode collapse, where many different noise inputs map to nearly identical outputs.
- Mode collapse is framed as an undesirable many-to-one mapping rather than a many-to-many mapping.
- Diffusion models offer an alternative built around a forward diffusion process that progressively adds small amounts of noise to an input image.
- A denoising neural network is trained to predict the amount of noise injected during the forward process.
- After training, a random noise sample is fed through the reverse denoising process to synthesize a new image.
- OpenAI’s May 2021 paper demonstrated that diffusion models can outperform GANs on image synthesis.
- FID score is the standard metric for evaluating image generation quality and diversity.
- A lower FID score indicates more realistic, higher-quality, and more diverse generated images.
- Stable Diffusion and OpenAI DALL·E 3 are leading image generation systems built on diffusion models.

## Failure modes named
- Mode collapse in GANs causes poor output diversity by mapping many noise inputs to the same or very similar images.

## Studio relevance
02 frame - clarifies the generative-model trade-off between GANs and diffusion models when framing AI image-synthesis system choices.
---
