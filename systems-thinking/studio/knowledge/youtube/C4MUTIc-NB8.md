---
source: https://www.youtube.com/watch?v=C4MUTIc-NB8
video_id: C4MUTIc-NB8
channel: giant_neural_network
title: "today I tried: Evolution Strategies"
scraped: 2026-08-28
tags: [biology, reinforcement learning, evolution strategies, optimization, finite differences]
---
# today I tried: Evolution Strategies

A hands-on introduction to Evolution Strategies as a simple, gradient-free, highly parallelizable reinforcement-learning method that uses random parameter perturbations and reward-weighted averaging to climb reward landscapes.

## Procedure / models distilled
- Evolution Strategies (ES) train an agent by adding random noise to policy parameters, measuring the reward for each noisy variant, and shifting the parameters toward the directions that produced higher reward.
- Classic policy-gradient RL maps a state to a probability distribution over actions through a differentiable neural network, then uses cross-entropy loss gradients to raise the probability of actions that received positive reward.
- ES skips the differentiable policy and instead starts from a parameter vector, samples many Gaussian perturbations around it, evaluates reward for each perturbed vector, and takes a reward-weighted average of the perturbations as the update.
- This update approximates the finite-difference slope of the reward function, letting the search move toward local reward peaks without using explicit gradients or backpropagation.
- The standard deviation of the added noise acts like the step size H in finite differences, determining how far around the current parameters the algorithm probes.
- ES is inherently parallel because each noisy parameter evaluation is independent, making it attractive when thousands of workers are available.
- Because ES only needs scalar rewards, the controller can be any function of state and parameters; it does not have to be a differentiable neural network.
- In the 2D reward demo, parameters are coordinates, Gaussian samples are scattered around the current point, blue background color is interpreted as reward, and the agent migrates toward darker blue regions.
- In the robot arm demo, the task is inverse kinematics: network weights map the mouse position to joint angles, and reward comes from the perturbed end effector moving closer to the target point.
- Each training step samples a batch of random target points, perturbs the weights, records the applied noise and the resulting reward, and updates weights by the reward-weighted average of the noises.
- Lowering the learning rate or the standard deviation of exploration noise narrows the search and lets the policy hone in for more precise tracking.
- ES is indifferent to controller architecture changes such as segment count, segment length, or feature transforms, so the same procedure applies without modification.

## Failure modes named
- Too large an exploration standard deviation or too high a learning rate can prevent the policy from converging tightly, leaving tracking imprecise.
- The ES update is a noisy finite-difference approximation of the true reward gradient, not an exact gradient.
- The method’s parallelization advantage assumes access to substantial distributed compute; without it, sample efficiency can be poor compared to gradient-based methods.

## Studio relevance
04 leverage - provides a gradient-free, massively parallel optimization mechanism for training agents when gradients are unavailable, expensive, or unnecessary.
