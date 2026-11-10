---
source: https://www.youtube.com/watch?v=EusEoN9aQ-Q
video_id: EusEoN9aQ-Q
channel: Marythmatics
title: "how to use probability to make decisions?"
scraped: 2026-08-28
tags: [mathematics, probability, decision theory, quiz show]
---
# how to use probability to make decisions?

A father-son quiz team, each independently correct with probability q, evaluates two answer strategies and finds both yield exactly the same success probability q, so either strategy is equally good.

## Procedure / models distilled
- Define events: C = the team answers correctly, S = the son answers, F = the father answers.
- Record the known probabilities: each individual answers correctly with P(C|S)=P(C|F)=q.
- Strategy 1: choose one person uniformly at random, so P(S)=P(F)=1/2.
- Apply the total probability theorem across the partition {S, F}: P(C)=P(C|S)P(S)+P(C|F)P(F).
- Compute Strategy 1 success: P(C)=q·1/2+q·1/2=q.
- Strategy 2: partition the sample space into match (answers agree) and mismatch (answers disagree).
- Write success probability as P(C)=P(C∧match)+P(C∧mismatch), valid because match and mismatch are disjoint.
- If answers match and are correct, both must be correct: P(C∧match)=q·q=q² using independence.
- Compute mismatch probability: son correct and father wrong, or son wrong and father correct: q(1−q)+(1−q)q=2q(1−q).
- Given a mismatch, exactly one of the two is correct and a fair coin is flipped, so P(C|mismatch)=1/2.
- Compute Strategy 2 success: P(C)=q²+(1/2)·2q(1−q)=q²+q−q²=q.
- Compare strategies: since both give success probability q, probability alone does not favor one strategy over the other.

## Failure modes named
- Treating mismatch as including both-correct or both-wrong cases, when mismatch forces exactly one correct and one incorrect.
- Adding probabilities of events before checking that they are disjoint.
- Multiplying probabilities of events without confirming they are independent.
- Assuming the two strategies must give different success probabilities when the math shows they are identical.

## Studio relevance
04 leverage - uses total-probability and event-partitioning to evaluate competing decision strategies under uncertainty.
