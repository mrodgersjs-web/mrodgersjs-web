---
source: https://www.youtube.com/watch?v=94AmzeR9n2w
video_id: 94AmzeR9n2w
channel: The Organic Chemistry Tutor
title: "Multiplication & Addition Rule - Probability - Mutually Exclusive & Independent Events"
scraped: 2026-08-28
tags: [mathematics, probability, statistics, rules]
---
# Multiplication & Addition Rule - Probability - Mutually Exclusive & Independent Events

A tutorial on the addition and multiplication rules of probability, including how to handle mutually exclusive and independent events, followed by a worked example combining all four concepts.

## Procedure / models distilled
- **Addition rule for unions:** The probability of A or B occurring is $P(A \cup B) = P(A) + P(B) - P(A \cap B)$; this formula always works regardless of event relationship.
- **Mutually exclusive simplification:** When A and B cannot occur together, $P(A \cap B) = 0$, so the addition rule collapses to $P(A \cup B) = P(A) + P(B)$.
- **Conditional probability definition:** The probability of A given B is $P(A|B) = \frac{P(A \cap B)}{P(B)}$.
- **Multiplication rule via conditioning:** Rearrange conditional probability to get $P(A \cap B) = P(A|B) \times P(B)$, or equivalently $P(A \cap B) = P(B|A) \times P(A)$; choose the form matching the given conditional probability.
- **Independence test and shortcut:** Events are independent if and only if $P(A|B) = P(A)$ (and likewise $P(B|A) = P(B)$); when independent, the multiplication rule simplifies to $P(A \cap B) = P(A) \times P(B)$.
- **"And" means simultaneous, not sequential:** $A \cap B$ represents both events occurring at the same time, so order is irrelevant and $P(A \cap B) = P(B \cap A)$.
- **Worked-example workflow:** (1) list the given probabilities, (2) identify whether the question asks for a union ("or") or intersection ("and"), (3) select the appropriate formula, (4) substitute and compute, and (5) check independence/mutual exclusivity by comparing $P(A|B)$ to $P(A)$ and $P(A \cap B)$ to zero.

## Failure modes named
- Treating "A and B" as a sequence (A then B) rather than simultaneous occurrence, which can mislead formula selection.
- Forgetting to subtract the joint probability $P(A \cap B)$ when using the general addition rule, causing double-counting.
- Conflating "mutually exclusive" with "independent": mutually exclusive means the joint probability is zero; independence means conditioning has no effect.
- Declaring independence without checking whether $P(A|B) = P(A)$; simply because two probabilities are given does not make events independent.

## Studio relevance
07 verify - the studio uses this card to check probabilistic reasoning for union, intersection, independence, and mutual exclusivity in any model that relies on event probabilities.
