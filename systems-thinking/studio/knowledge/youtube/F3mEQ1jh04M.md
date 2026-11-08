---
source: https://www.youtube.com/watch?v=F3mEQ1jh04M
video_id: F3mEQ1jh04M
channel: Emma Ding
title: "Simpson's Paradox in A/B Testing Made Easy: Intuitive Explanation for Data Scientists"
scraped: 2026-08-28
tags: [statistics-causality, ab-testing, confounding, data-segmentation, conditional-probability]
---
# Simpson's Paradox in A/B Testing Made Easy: Intuitive Explanation for Data Scientists

A tutorial on recognizing, explaining, and deciding how to act when a relationship between two variables reverses direction after aggregating across subgroups, especially in A/B testing.

## Procedure / models distilled
- Define Simpson's paradox as a sign reversal: a subgroup-level inequality (e.g., rate for A vs. B) flips when numerators and denominators are summed across groups.
- Model each subgroup as a 2×2 contingency table with counts a_i, b_i, c_i, d_i, then aggregate by summing each count to form the overall table A, B, C, D.
- Compare the within-group ratio a_i/b_i vs. c_i/d_i with the aggregate ratio A/B vs. C/D to detect the paradox.
- Interpret the paradox in conditional-probability terms: P(A | B, C) and P(A | B, C^c) can both be smaller than the B^c counterparts while P(A | B) is larger.
- Apply the pattern to an A/B test by computing click-through rate as clicks divided by impressions for each treatment in each segment.
- Inspect whether the aggregate CTR contradicts the segment-level CTRs, as in the example where ad 1 wins in both groups but loses overall.
- Decide which view is meaningful by assessing whether the grouping variable (e.g., iOS vs. Android) is a plausible causal influencer of the outcome.
- Use the disaggregated view when subgroups are heterogeneous in factors that affect the metric, and the aggregated view when the groups are homogeneous.
- Check for unbalanced sample sizes across segments, because large disparities in denominators can pull the aggregate rate toward the segment with more observations.
- Look for an underlying confounding variable that influences both group assignment and the outcome to explain why the reversal occurs.
- Treat the paradox as a warning that the obvious conclusion from one level of aggregation may be wrong, and require domain knowledge to choose the right level.

## Failure modes named
- Assuming the disaggregated view is always more trustworthy than the aggregate view.
- Declaring a winner based only on overall CTR without checking per-segment CTRs.
- Ignoring lurking variables such as device type, age, or geography that explain subgroup differences.
- Overlooking large differences in sample size between segments.
- Interpreting a high-level trend as causal without verifying whether subgroups are homogeneous.
- Conflating "more granular data" with "more correct data" when the extra variable is not meaningful.

## Studio relevance
03 diagnose - this card is used to catch reversal effects and aggregation-level contradictions when interpreting experiment results or observational group comparisons.
