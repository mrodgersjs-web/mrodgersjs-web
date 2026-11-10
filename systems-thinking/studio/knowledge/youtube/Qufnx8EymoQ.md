---
source: https://www.youtube.com/watch?v=Qufnx8EymoQ
video_id: Qufnx8EymoQ
channel: INI Seminar Room 1
title: "Prof. Maximilian Kasy | Machine learning, causal inference, and economics"
scraped: 2026-08-28
tags: [statistics-causality, machine-learning, mechanism-design, reinforcement-learning, welfare-economics]
---
# Prof. Maximilian Kasy | Machine learning, causal inference, and economics

Kasy argues that reinforcement learning and bandits already perform causal inference by construction, but economic policy questions add unobserved welfare objectives and externalities that require merging adaptive experimentation with incentive-compatible preference elicitation.

## Procedure / models distilled
- Distinguish supervised learning (one-way data flow, conditional prediction) from reinforcement learning and bandits (two-way flow: algorithm acts, observes consequences, updates).
- Use construction exogeneity in adaptive algorithms: because the algorithm chooses actions based only on its own information, causal effects of those actions are identified without instrumental variables or regression discontinuity.
- Treat causality formalisms as shared primitives: structural equations, potential outcomes, and do-calculus all define causality via an exogenous intervention, the same primitive as decision theory.
- Recognize welfare as an unobserved objective: social welfare is a weighted sum of utilities that are never directly observed, only revealed through choices.
- Infer welfare by integrating response functions such as demand or labor-supply curves, rather than evaluating behavior at a single point.
- Adapt the exploration-exploitation trade-off for welfare objectives: when the objective is an integral over counterfactual policies, optimal experimentation must explore away from the myopically best policy.
- Apply mechanism design as a counterfactual generator: incentive-compatible auctions or preference-elicitation mechanisms can make truthful reporting a dominant strategy and recover entire individual-level response functions.
- Model binary choice as a threshold decision: an individual chooses yi = 1 when willingness-to-pay vi exceeds the assigned price or tax ti.
- Extend the binary-choice model to externalities by asking individuals both their private action value and their disutility from others' actions, using a quadratic payment scheme to preserve truth-telling incentives.
- Combine elicited preference and externality information with bandit-style updating to learn socially optimal taxes, prices, or congestion charges.
- Treat the choice of what an automated decision system optimizes, and who chooses it, as a political and institutional design question rather than a purely technical one.

## Failure modes named
- Treating all machine learning as purely correlational and ignoring that reinforcement learning and bandits already do causal inference by construction.
- Assuming the fundamental problem of causal inference is universal in economics, when mechanism design can elicit full individual response functions.
- Treating incentivized stated preferences as a panacea without acknowledging the external-validity gap between what people say and what they do.
- Optimizing adaptive policies using observed rewards alone when the true social-welfare objective is an unobserved integral over counterfactual behavior.
- Inferring social welfare from individual choices while ignoring externalities, since my choices reveal my utility over my actions but not over others' actions.
- Reinforcement-learning practitioners neglecting statistical estimation issues that the causal-inference literature has already developed.

## Studio relevance
02 frame - use this card to reframe predictive-ML projects as decision-making and welfare-estimation problems, and to identify where mechanism design or adaptive experimentation is needed.
