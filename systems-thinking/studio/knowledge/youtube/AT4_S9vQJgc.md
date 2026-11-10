---
source: https://www.youtube.com/watch?v=AT4_S9vQJgc
video_id: AT4_S9vQJgc
channel: Stanford
title: "Statistical Mechanics Lecture 9"
scraped: 2026-08-28
tags: [physics, statistical mechanics, ising model, phase transitions, mean-field theory]
---
# Statistical Mechanics Lecture 9

Lecture 9 reviews the one-dimensional Ising model, introduces a self-consistent mean-field approximation to show that phase transitions can emerge in higher dimensions, and uses the graphical solution of the mean-field equation to explain spontaneous symmetry breaking and the instability of the unmagnetized state.

## Procedure / models distilled
- Treat a single non-interacting spin in a field by writing its partition function as the sum over two states, \(Z = e^{\beta J} + e^{-\beta J} = 2\cosh(\beta J)\), and compute average energy and magnetization from derivatives or direct averaging.
- Interpret the average magnetization of one spin as \(\langle\sigma\rangle = \tanh(\beta J)\): saturated at low temperature, zero at infinite temperature, and symmetric between up and down.
- Model the one-dimensional Ising model as a chain of spins \(\sigma_i=\pm1\) with nearest-neighbor energy \(-J\sum_i \sigma_i\sigma_{i+1}\), where the minus sign favors parallel alignment.
- Recognize that in one dimension the Ising model has no phase transition at non-zero temperature because thermal fluctuations disrupt long-range order.
- Use the mean-field approximation for higher-dimensional Ising systems by replacing each neighbor's actual spin with the average magnetization \(m\), turning interactions into an effective external field \(J z m\) where \(z\) is the number of neighbors.
- Write the self-consistency equation for the mean-field Ising model: \(m = \tanh[\beta(J z m + b)]\), where \(b\) is an external magnetic field.
- Solve the self-consistency equation graphically by plotting \(y=m\) against \(y=\tanh[\beta(J z m)]\) and looking for intersections.
- Identify the critical behavior: for \(\beta J z < 1\) (high temperature) the only solution is \(m=0\); for \(\beta J z > 1\) (low temperature) two non-zero magnetized solutions appear.
- Interpret the non-zero solutions below the critical temperature as spontaneous symmetry breaking: the system chooses a preferred direction even though the underlying Hamiltonian is symmetric under spin flip.
- Explain why the symmetric \(m=0\) solution is unstable by adding an infinitesimal magnetic field \(b\): it shifts the hyperbolic tangent and removes the zero-magnetization solution, biasing the whole sample toward one sign.
- Connect instability to system size: a macroscopic number of aligned spins makes the energy difference due to a tiny field enormous, so the symmetric state is easily tipped.
- Distinguish exact 1D solution from mean-field approximation: exact 1D has no phase transition, while mean-field captures the phase transition that occurs in sufficiently high dimensions.

## Failure modes named
- Ising's extrapolation fallacy: correctly solving the one-dimensional model and then incorrectly concluding that no phase transition exists in any dimension.
- Assuming independent-spin behavior carries over to interacting systems without accounting for correlations between neighbors.
- Treating the symmetric \(m=0\) solution as stable below the critical temperature, when an infinitesimal external field or fluctuation collapses it to a magnetized state.
- Confusing the exact high-dimensional Ising model, which is very hard to solve, with the physically intuitive mean-field approximation that captures phase transitions but neglects fluctuations.

## Studio relevance
03 diagnose - the card provides a quick diagnostic for when collective interactions produce emergent order versus when thermal fluctuations or dimensionality prevent phase transitions.
