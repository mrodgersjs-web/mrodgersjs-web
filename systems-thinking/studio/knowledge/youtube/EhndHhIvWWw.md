---
source: https://www.youtube.com/watch?v=EhndHhIvWWw
video_id: EhndHhIvWWw
channel: Deepia
title: "Diffusion Models: DDPM | Generative AI Animated"
scraped: 2026-08-28
tags: [network-science, generative-ai, diffusion-models, deep-learning, probabilistic-modeling]
---
# Diffusion Models: DDPM | Generative AI Animated

The video derives the DDPM framework: a variance-preserving forward noising process, an ELBO-derived MSE noise-prediction loss for training a U-Net denoiser, and an iterative reverse-sampling loop that generates images from pure Gaussian noise.

## Procedure / models distilled
- Treat data generation as sampling from an intractable data distribution p(x) that has no closed-form expression, and use a learned diffusion process to approximate it.
- Forward diffusion: corrupt a clean image x0 by repeatedly adding Gaussian noise; DDPM uses a variance-preserving transition q(x_t | x_{t-1}) that scales the mean by sqrt(1 - beta_t) and adds noise with variance beta_t.
- Distinguish variance-exploding diffusion—where the mean stays fixed and variance grows without bound—from variance-preserving diffusion, where the mean goes to 0 and the variance goes to 1; DDPM chooses the latter.
- Compute any noisy step in closed form: x_t ~ N(sqrt(alpha_bar_t) x0, (1 - alpha_bar_t) I), with alpha_bar_t defined as the product of (1 - beta_s) for s = 1 to t.
- Use a learnable noise schedule (e.g., linear or cosine) with each beta in (0,1), ensuring alpha_bar_t converges to 0 and the final distribution becomes standard normal.
- Reverse process: parameterize p_theta(x_{t-1} | x_t) as Gaussians and train neural-network weights theta to remove noise step by step.
- Replace the intractable negative log-likelihood of x0 with the ELBO (evidence lower bound), derived via Bayes' theorem and the Markov-chain structure of the forward process.
- Show that the ELBO reduces to a sum of KL divergences between the true posterior q(x_{t-1} | x_t, x0) and the approximate posterior p_theta(x_{t-1} | x_t).
- When both posteriors are Gaussian with fixed variance, each KL divergence becomes a weighted L2 distance between the true posterior mean and the network-predicted posterior mean.
- Reparameterize x_t as sqrt(alpha_bar_t) x0 + sqrt(1 - alpha_bar_t) epsilon and have the network predict epsilon_theta(x_t, t); the L2 mean loss collapses to MSE between epsilon and epsilon_theta.
- Avoid summing over all timesteps per sample by sampling one random timestep t per training example; this converges to the full objective and is far cheaper.
- Implement with a Diffusion U-Net, Adam optimizer, and simple MSE loss in PyTorch/DeepInverse, so the code directly matches the derived equations.
- Inference: start from pure Gaussian noise x_T, repeatedly predict epsilon_theta, compute the posterior mean, add the prescribed amount of noise to obtain x_{t-1}, and iterate until a clean sample emerges.
- Ensure the diffusion constants—noise schedule, alphas, alpha_bar, and related terms—match exactly between training and inference.

## Failure modes named
- Variance-exploding diffusion: leaving the mean unscaled each step causes variance to grow without bound, so the process never converges to a standard normal distribution.
- The misconception that DDPM invented diffusion models; it popularized them and simplified the training objective, building on the 2015 nonequilibrium-thermodynamics paper.
- Mismatching training and inference constants breaks the correspondence between the noise level added during training and the noise level assumed during sampling.
- Summing the loss over every timestep for each sample is prohibitively expensive; the practical remedy is random-timestep sampling.
- A denoiser that performs poorly at very high noise levels during training can still generate high-quality samples, so poor high-timestep denoising should not be mistaken for total failure.

## Studio relevance
06 synthesize - integrate the DDPM probabilistic generative pipeline and its training/inference equations into the studio's models of generative-AI systems.
