---
source: https://www.youtube.com/watch?v=Gib_kiXgnvA
video_id: Gib_kiXgnvA
channel: Normalized Nerd
title: "The Math Behind Generative Adversarial Networks Clearly Explained!"
scraped: 2026-08-28
tags: [mathematics, generative adversarial networks, minimax optimization, jensen-shannon divergence]
---
# The Math Behind Generative Adversarial Networks Clearly Explained!

A walkthrough of GANs as a two-player minimax game, deriving the value function as an expected binary cross-entropy and proving that the global optimum makes the generator's distribution match the real data by minimizing Jensen–Shannon divergence.

## Procedure / models distilled
- A GAN is not a single model; it is an adversarial pair of networks: a generator G and a discriminator D.
- Generative models learn the joint distribution of data and can synthesize new instances, while discriminative models learn the conditional distribution of labels given inputs.
- The generator receives random noise z drawn from p_Z and outputs a fake sample G(z), whose distribution p_G lives in the same space as the real data distribution p_data.
- The discriminator D(x) is a binary classifier that estimates the probability that an input x came from the real data rather than the generator.
- The two networks play a minimax game with value function V(D,G) = E_{x~p_data}[ln D(x)] + E_{z~p_Z}[ln(1 - D(G(z)))].
- This value function is simply the expected binary cross-entropy over real and fake samples.
- Expectations generalize sums to continuous distributions, and can be written as integrals over p_data and p_Z.
- In practice, training alternates: run k gradient-ascent updates on D to maximize V, then one gradient-descent update on G to minimize V.
- The generator update uses only the fake-data term because the real-data term has zero gradient with respect to the generator's parameters.
- For a fixed generator, the optimal discriminator is D*(x) = p_data(x) / [p_data(x) + p_G(x)].
- Plugging D*(x) back into the value function yields 2·JS(p_data || p_G) - 2 ln 2.
- Hence the generator's implicit objective is to minimize the Jensen–Shannon divergence between p_data and p_G.
- The global minimum occurs when p_G = p_data, JS divergence is zero, and the discriminator outputs 0.5 for every input.
- Training evolves through phases: both networks are weak at first, the discriminator improves, the generator pushes p_G toward p_data, and finally the fake distribution becomes indistinguishable from the real one.

## Failure modes named
- Misconception: treating a GAN as a single model instead of a competing generator–discriminator pair.
- Intimidation trap: the value function looks like gibberish until recognized as an expected binary cross-entropy.
- Practical instability: real-world GAN training is hard even though the theoretical global optimum is clean.

## Studio relevance
02 frame - provides a mathematical framing of GANs as a two-player minimax game optimizing a Jensen-Shannon divergence objective.
