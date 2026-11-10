---
source: https://www.youtube.com/watch?v=5IUj1EZwpJY
video_id: 5IUj1EZwpJY
channel: Molly Rocket
title: "The Only Unbreakable Law"
scraped: 2026-08-28
tags: [organizations, software-architecture, conways-law, communication-structures, systems-design]
---
# The Only Unbreakable Law

Conway’s Law is presented as the nearest thing to an unbreakable law in software architecture: the structure of any designed system is a copy of the communication structures of the organization that produced it, including the historical, temporal organization embedded in shipped code.

## Procedure / models distilled
- Apply Conway’s Law as a constraint, not a guideline: “organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations.”
- Map the live org chart onto the system architecture to predict or explain structural boundaries, seams, duplication, and hand-off points in the product.
- Extend Conway’s Law to the “four-dimensional org chart”: past teams that shipped code still shape the product, because reshipping old code is cheaper than re-solving old problems.
- Compare Amdahl’s Law and Brooks’s Law as parallel limit laws: Amdahl bounds speedup by the sequential fraction; Brooks bounds speedup by communication/coordination overhead; Conway bounds design quality by communication structure.
- Treat every artificial code boundary — inheritance hierarchies, classes, modules, libraries, engines, package managers, containers, virtual machines, microservices — as an internal org chart that imposes communication cost and restricts cross-boundary optimization.
- Recognize that decomposition is usually a coping mechanism for limited human cognitive capacity, not an intrinsic good; it eliminates design possibilities and fixes suboptimal structure early.
- Evaluate “best practices” by their communication cost: lean, flexible organizations and codebases minimize unnecessary boundaries; fat, heavily layered stacks maximize them.
- Use Conway’s Law to explain why legacy subsystems persist and why superficially simple features can contain multiple inconsistent implementations produced by temporally separate teams.
- Judge risk-averse technology choices (reusing popular libraries, containers, hypervisors) as defensive coordination shortcuts that often under-optimize the final product.
- Reframe the goal of architecture as minimizing communication constraints — both among people and inside the code — while accepting that some constraints are currently unavoidable given human cognition.

## Failure modes named
- Calling rules of thumb “laws” (Pareto principle, SOLID, Postel’s Law) and treating them as causal or architectural truths.
- Believing delegation, encapsulation, modularity, libraries, or microservices are intrinsically good rather than costly coordination workarounds.
- Ignoring Brooks’s Law and adding people to projects without accounting for the communication overhead that creates a floor on completion time.
- Designing class hierarchies and code modules as org charts that constrain runtime design without representing any true operational necessity.
- Failing to see that the shipped product is authored by every team that ever touched the code, not just the team on the current org chart.
- Replacing the hard work of communication with technology layers (containers, VMs, package managers) that add boundaries instead of removing them.
- Choosing known-but-suboptimal tools over better-but-unproven designs because “no one ever got fired for mitigating risk.”
- Mistaking the necessity of decomposition for an achievement, celebrating artificial boundaries that signal the problem was too complex to hold in mind.

## Studio relevance
03 diagnose - use Conway’s Law to map communication structures across teams, time, and code to explain why an architecture looks the way it does and where hidden coordination costs live.
