---
source: https://www.youtube.com/watch?v=9SynCu3nxUE
video_id: 9SynCu3nxUE
channel: LearnChemE
title: "Virial Equation of State Introduction"
scraped: 2026-08-28
tags: [product-growth, thermodynamics, equations-of-state, chemical-engineering, ideal-gas]
---
# Virial Equation of State Introduction

The video introduces the virial equation of state as a series correction to the ideal gas law, emphasizing a practical two-term truncation and estimation of the second virial coefficient from critical properties and the acentric factor.

## Procedure / models distilled
- Begin with the ideal gas law written as PV/RT = 1, where V is molar volume and T is absolute temperature.
- Extend to the virial equation of state: PV/RT = 1 + B/V + C/V² + D/V³ + ..., with B, C, D as temperature-dependent virial coefficients.
- Identify the compressibility factor Z as the ratio PV/RT.
- Truncate the virial series after the second virial coefficient: PV/RT ≈ 1 + B/V.
- Substitute 1/V ≈ P/RT into the truncated form to obtain PV/RT ≈ 1 + BP/RT, allowing direct volume calculation from pressure and temperature.
- Estimate the second virial coefficient using a Pitzer-type correlation: B = (RTc/Pc)(B0 + ωB1), where ω is the acentric factor.
- Compute reduced temperature as Tr = T/Tc.
- Evaluate B0 using the correlation B0 = 0.083 - 0.422/Tr^1.6.
- Evaluate B1 using the correlation B1 = 0.139 - 0.172/Tr^4.2.
- Look up critical temperature, critical pressure, and acentric factor for the pure component of interest.
- Solve the resulting truncated virial equation to obtain a volume estimate more accurate than the ideal gas law.

## Failure modes named
- The virial equation is explicitly noted as not suitable for all molecules, particularly polar compounds.
- Truncating the infinite series after the second virial coefficient introduces approximation error.
- Substituting 1/V = P/RT uses an ideal-gas approximation inside a non-ideal equation, adding another layer of error.
- The second virial coefficient obtained from correlations is an estimate, dependent on accurate critical properties and acentric factor data.

## Studio relevance
04 leverage - how the studio uses this card to refine property estimates beyond ideal-gas assumptions by applying a truncated virial correction and correlating molecular parameters.
