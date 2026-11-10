---
source: https://www.youtube.com/watch?v=zOmhHE2xctw
video_id: zOmhHE2xctw
channel: unknown
title: "The Core Equation Of Neuroscience"
scraped: 2026-08-28
tags: [psychology, neuroscience, biophysics, computational-modeling]
---
# The Core Equation Of Neuroscience

The video derives the Hodgkin–Huxley model by treating the neuronal membrane as a leaky capacitor, decomposing ionic currents into voltage-dependent conductances controlled by gating-variable kinetics, and assembling four coupled differential equations that reproduce the action potential.

## Procedure / models distilled
- Treat membrane voltage as the primary state variable for modeling a neuron’s electrical behavior.
- Model the cell membrane as a capacitor that stores charge across an otherwise impermeable lipid barrier.
- Write the capacitor equation and take its time derivative to relate the rate of change of voltage to membrane current.
- Add ion-specific membrane channels as parallel resistive/conductive pathways, so total ionic current drives voltage change.
- Describe an action potential as a threshold-triggered sequence: voltage-gated sodium channels open and depolarize the cell, then sodium channels close while potassium channels open to repolarize it.
- Explain ionic driving force as the competition between diffusion (concentration gradient) and electrical force (charge attraction/repulsion).
- Define the equilibrium (reversal) potential as the voltage at which diffusion and electrical forces balance, yielding zero net current for a given ion.
- Express ionic current through open channels with Ohm’s-law form: current equals conductance times the difference between membrane voltage and the ion’s equilibrium potential.
- Decompose conductance into a maximal conductance constant and a voltage-dependent open-probability factor representing the fraction of open channels.
- Model each voltage-sensitive gate as a two-state permissive/non-permissive probability whose dynamics follow a first-order differential equation with voltage-dependent opening and closing rates.
- Recognize that channels requiring multiple independent gates produce conductances proportional to powers of the gate probability (e.g., n⁴ for potassium, m³h for sodium).
- Add a small leak current with constant conductance to account for always-open channels and improve realism.
- Extend the point-neuron model spatially by dividing the neuron into coupled compartments, applying Hodgkin–Huxley dynamics locally and adding inter-compartment currents.

## Failure modes named
- Thinking of ion channels as simple permanently open holes with fixed conductance, rather than voltage-dependent protein gates.
- Imagining a “doorman” or external coordinator that opens and closes channels during an action potential, instead of emergent voltage-dependent kinetics.
- Treating the neuron as a single spatial point with uniform membrane voltage when studying dendritic or axonal signaling.
- Trying to use the full four-equation Hodgkin–Huxley model for direct phase-space visualization or intuitive geometric reasoning, because its high dimensionality hides the underlying bifurcation structure.

## Studio relevance
02 frame - provides a biophysical state-variable framework for mapping neuronal excitability onto capacitor–resistor–gate dynamics.
