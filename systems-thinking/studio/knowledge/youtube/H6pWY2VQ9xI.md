---
source: https://www.youtube.com/watch?v=H6pWY2VQ9xI
video_id: H6pWY2VQ9xI
channel: Zachary Huang
title: "Give Me 1 Hour, I'll Make Probability Click Forever"
scraped: 2026-08-28
tags: [mathematics, probability, intuition, statistics]
---
# Give Me 1 Hour, I'll Make Probability Click Forever

A one-hour rebuild of probability from intuition upward: treat chance as counting sets of equally likely outcomes, then derive axioms, set operations, conditional/total probability, Bayes' rule, and recursive expectation through concrete physical examples.

## Procedure / models distilled
- Treat probability as counting: for equally likely outcomes, P(E) = (number of outcomes in event E) / (total number of outcomes in the sample space).
- Build the sample space as the complete set of distinct individual possibilities, preserving order and identity (e.g., HT and TH are separate outcomes for two different coins).
- Treat an event as a set of outcomes, not a single outcome; a singleton like {HH} is just a set with one element.
- Use the three axioms as the DNA of every calculation: probabilities are non-negative, P(S) = 1, and P(A ∪ B) = P(A) + P(B) for disjoint events.
- Apply the complement rule: P(not A) = 1 − P(A), because A and its complement partition the whole sample space.
- Compute unions with the addition rule: P(A ∪ B) = P(A) + P(B) − P(A ∩ B), subtracting the overlap to fix double counting; for mutually exclusive events the overlap is zero and the rule collapses to simple addition.
- Interpret conditional probability as living inside a shrunken sample space where the conditioning event is already known to have happened.
- Use the law of total probability to decompose an overall probability across mutually exclusive scenarios and weight each branch by its prior probability.
- Apply Bayes' rule as (likelihood × prior) / total evidence, or equivalently as the probability of the specific pathway divided by the probability of all pathways producing the observed evidence.
- Update beliefs rationally: a positive diagnostic test does not equal the probability of having the disease; the base rate must be weighed against test accuracy.
- Solve expected waiting-time problems recursively by defining the unknown expected value E, conditioning on the first trial, expressing E in terms of itself, and solving the resulting equation instead of summing infinite series.

## Failure modes named
- Teaching probability backwards—formulas and axioms first, intuition later—produces fragile, quickly forgotten knowledge.
- Thinking probability asks about a single outcome rather than a set of outcomes.
- Misidentifying the sample space, such as treating HT and TH as the same outcome when flipping two distinct coins.
- Double-counting overlapping outcomes when computing P(A or B).
- Treating non-mutually exclusive events as mutually exclusive and simply adding their probabilities.
- Confusing P(A|B) with P(B|A) or with the unconditional P(A).
- Equating diagnostic-test accuracy with the posterior probability of having the disease after a positive test.
- Ignoring the base rate when interpreting evidence, leading to massive overestimation of rare conditions.
- Trying to enumerate or sum infinite sequences of outcomes directly instead of using recursive expectation.
- Believing conceptual understanding will stick without deliberate practice, producing "Swiss cheese knowledge."

## Studio relevance
02 frame - use this card to reframe probability as set-counting and recursive belief-updating rather than formula recall.
