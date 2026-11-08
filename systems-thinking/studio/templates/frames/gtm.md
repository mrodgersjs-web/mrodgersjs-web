# System Frame — GTM outbound (domain)

> Fill every blank. Unknown is an answer. Date and own it.

## 1. Boundary
- System of interest: from ICP list → meeting booked (not closed revenue)
- Inside: list, sequence, offer, reply handling, calendar
- Outside: market, competitor noise, inbox filters, warmup limits
- Boundary rationale: mixing close-rate into outbound hides the delay that actually kills the loop

## 2. Stocks
| Stock | Unit | Current level | Owner |
|---|---|---|---|
| sendable ICP | people | | Darius |
| staged emails | drafts | | Darius |
| replies | threads | | Darius |
| meetings | booked | | AE |
| Gate-D holds | slices | | Mike |

## 3. Flows
| Inflow → Stock | Rate | Outflow → where | Rate |
|---|---|---|---|
| enrich → sendable | | reject / exclusion | |
| draft → staged | | Gate-D park | |
| send → replies | | bounce / unsubscribe | |
| reply → meeting | | no-show | |

## 4. Actors & incentives
| Actor | Wants | Pulls which stock |
|---|---|---|
| Darius | meetings without send-risk | sendable, staged |
| Mike | $ without cap blowups | Gate-D holds, A_ops |
| Prospect | relevance, not volume | replies |

## 5. Feedback loops
- R1: meetings → proof → easier next meeting
- B1: send volume → warmup / spam → deliverability ↓ → replies ↓
- B2: Gate-D (goal: zero unapproved sends)

## 6. Delays
| Between | And | Delay | Consequence |
|---|---|---|---|
| send | reply | 1–14d | overshoot sequences |
| meeting | close | 30–90d | R2 looks dead |

## 7. Archetype suspects
Run: `studio map "outbound volume up replies flat deliverability down"`
- Primary suspect:
- Evidence:

## 8. Leverage hypothesis
Current interventions sit at rank: ___ (usually 12 = more volume)
One-rank-higher option: rank 6 information (who sees bounce/reply as it happens)

## 9. Measurement
- Stock health: meetings/week, not emails sent
- Lead indicator: reply rate by sequence day 3
- Falsifier: 14 days of send with reply rate < X kills this frame

## 10. Corpus
`studio cards gtm` · `studio search "cold email deliverability warmup"`
