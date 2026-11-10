---
source: https://www.youtube.com/watch?v=TkwXa7Cvfr8
video_id: TkwXa7Cvfr8
channel: unknown
title: "Watching Neural Networks Learn"
scraped: 2026-08-28
tags: [engineering, neural-networks, function-approximation, machine-learning, dimensionality]
---
# Watching Neural Networks Learn

The video demonstrates, through visual experiments on curves, images, parametric surfaces, fractals, and MNIST, how neural networks approximate functions, and how practical choices like activation functions, normalization, learning-rate decay, Taylor features, and Fourier features interact with dimensionality to determine approximation quality.

## Procedure / models distilled
- Treat a neural network as a composite function: layers of neurons compute weighted sums of inputs plus a bias, pass the result through a non-linear activation, and feed the output vector forward to the next layer.
- Understand neurons as simple shape builders: the activation function defines a neuron’s mathematical shape, while weights shift, squeeze, and stretch that shape; stacking many neurons builds increasingly intricate functions.
- Frame supervised learning as curve fitting from finite samples: given input-output data points, adjust weights to minimize a loss function measuring the difference between predicted and true outputs.
- Use backpropagation as the training algorithm to iteratively reduce loss; the network should improve as loss decreases.
- Visualize learned functions by querying the network on a dense grid and plotting every output value at once, which works because low-dimensional functions can be rendered as images or surfaces.
- Normalize inputs to a small, zero-centered range (e.g., [−1, 1]) with a linear shift and scale so the network learns more easily.
- Decay the learning rate during training so large early steps capture coarse structure and smaller later steps refine fine details.
- Choose activation functions empirically rather than relying on universality alone: use Leaky ReLU in hidden layers for non-linearity and negative outputs; use a sigmoid or tanh in the final layer when outputs must be bounded, with tanh often performing better because it is zero-centered.
- Construct a Taylor-feature network by computing polynomial powers of the inputs and treating them as extra features in a single-layer or deep network, giving the network polynomial building blocks.
- Construct Fourier-feature networks by computing sine and cosine features at multiple frequencies and feeding them into a multi-layer network; normalize inputs to [−π, π] to match one full period.
- For multi-dimensional inputs, use separate 1D Fourier features per input instead of full multidimensional Fourier series to avoid an exploding number of terms, even though it is less theoretically complete.
- Evaluate models empirically by comparing error or accuracy on held-out data rather than relying on formal proofs; treat machine-learning engineering as an experimental science.
- Apply networks to real high-dimensional data by flattening inputs and measuring test accuracy, e.g., mapping MNIST’s 784-dimensional image vectors to 10-dimensional label outputs.

## Failure modes named
- Universality does not guarantee practical accuracy; a network can be a universal approximator yet still miss infinite detail in functions like the Mandelbrot set.
- A network learning a sphere parametric surface may never fully close the surface around the poles.
- Plain networks can struggle with complex low-dimensional shapes such as the spiral shell, getting confused and leaving artifacts.
- Polynomial/Taylor features alone are unstable because polynomial values can explode, making it hard for backpropagation to find good coefficients.
- The curse of dimensionality makes full multidimensional Fourier or Taylor series computationally impractical as input dimensionality grows.
- Fourier features can cause overfitting on high-dimensional problems, where the model memorizes training data too closely and performs worse on unseen data, shown with MNIST as Fourier orders increase.
- No single architecture or feature expansion is best for every task; Fourier features excel on low-dimensional periodic/structured problems but can harm high-dimensional problems.
- Toy approximations of known functions are not real-world solutions; use toy visualizations only to gain insight into approximation methods before applying them to real data.

## Studio relevance
03 diagnose - the studio uses this card to judge whether a function-approximation problem is low-dimensional and structured enough to benefit from Fourier/Taylor feature expansion, or high-dimensional enough to require plain networks with strong regularization to avoid overfitting.
