---
source: https://www.youtube.com/watch?v=aircAruvnKk
video_id: aircAruvnKk
channel: 3Blue1Brown
title: "But what is a neural network? | Deep learning chapter 1"
scraped: 2026-08-28
tags: [mathematics, deep learning, neural networks, machine learning]
---
# But what is a neural network? | Deep learning chapter 1

This video introduces a neural network as a layered mathematical function built from neurons holding activation values between 0 and 1, where weights and biases transform pixel patterns through weighted sums and a sigmoid squish function to recognize handwritten digits.

## Procedure / models distilled
- Treat each neuron as a container holding an activation number between 0 and 1.
- Structure the network into layers: an input layer (784 neurons for a 28×28 grayscale image), one or more hidden layers, and an output layer (10 neurons for digits 0–9).
- Propagate activations forward: each layer’s activations determine the next layer’s activations through weighted sums, biases, and a nonlinear squashing function.
- Use weights on connections to encode which pixel patterns a neuron responds to, with positive weights encouraging activation and negative weights discouraging it.
- Add a bias term to shift the threshold so a neuron only becomes meaningfully active when the weighted sum is high enough.
- Apply a sigmoid function to squash the weighted sum plus bias into the 0–1 activation range.
- Compose layers hierarchically so early layers can detect edges, middle layers can detect subcomponents like loops or lines, and the output layer combines subcomponents into digit classifications.
- Express the transition between two layers compactly as σ(Wx + b): a matrix-vector product of weights and activations, plus a bias vector, then element-wise application of the sigmoid.
- View the entire network as a single function mapping 784 input numbers to 10 output numbers, governed by its weights and biases.
- Count the adjustable parameters: the example network has roughly 13,000 weights and biases that can be tweaked to change behavior.
- Understand “learning” as searching for a setting of all weights and biases that solves the task at hand.
- Interpret each neuron as a function of the previous layer’s outputs rather than a fixed value, because its activation depends on the input image.
- Prefer ReLU over sigmoid in modern deep networks because ReLU is easier to train.

## Failure modes named
- Expecting hidden layers to automatically correspond to clean human-interpretable subcomponents such as edges, loops, or lines, when the trained network may not actually organize itself that way.
- Treating a chosen architecture such as two hidden layers of 16 neurons as principled, when it is often an arbitrary starting point that requires experimentation.
- Viewing the network as an opaque black box, which prevents diagnosing unexpected behavior or challenging assumptions about why it works.
- Attempting to hand-tune all 13,000 weights and biases, which is infeasible and error-prone.
- Using sigmoid activations in deep networks, which historically made training difficult and has largely been replaced by ReLU.
- Underestimating the network because it is “just a function”; its complexity is necessary for tasks like handwritten-digit recognition.

## Studio relevance
02 frame - use as a conceptual scaffold for mapping layered abstraction, weights/biases, and activation functions in neural networks.
