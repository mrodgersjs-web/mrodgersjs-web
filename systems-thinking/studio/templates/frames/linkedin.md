# System Frame — LinkedIn engine (domain)

## 1. Boundary
- System of interest: idea → published post → qualified inbound
- Inside: draft, image, schedule, comment SLA, scoreboard
- Outside: algorithm, audience mood, competitor feed
- Boundary rationale: impressions without inbound are a vanity stock

## 2. Stocks
| Stock | Unit | Current | Owner |
|---|---|---|---|
| unpublished drafts | posts | | Ralph / Alfred |
| scheduled queue | posts | | Postiz |
| published (7d window) | posts | | Ralph |
| comments unanswered | threads | | Ralph |
| inbound conversations | people | | Darius |

## 3. Flows
draft → schedule → publish → comment → inbound
Kill: post ships with no image / no question / generic hook (AntiGenericForce)

## 4. Actors
| Actor | Wants | Pulls |
|---|---|---|
| Ralph | cadence without thirst | published |
| Alfred | tomorrow's draft | unpublished |
| Algorithm | dwell + comments | published quality |
| Mike | inbound that can close | conversations |

## 5. Loops
- R1: specific posts → comments → dwell → distribution → more comments
- B1: cadence pressure → generic posts → distribution dies
- B2: comment SLA (90 min) — unanswered comments decay R1

## 6. Delays
publish → inbound: 24–72h. Do not retune the hook on hour-1 impressions.

## 7. Archetype suspects
`studio map "posting more engagement flat inbound zero"`
Typical: Limits to Growth (distribution constraint) or Fixes that Fail (more posts).

## 8. Leverage
Stop adding volume (rank 12). Move information (rank 6): scoreboard of inbound, not likes.
Rules (rank 5): AGF ≥ 85, ≥2 numbers, ≥1 question, Gate-D on send.

## 9. Measurement
- Health: inbound conversations / 7 published
- Lead: comments in first 90 min
- Falsifier: 8 posts, 0 inbound → kill this frame

## 10. Corpus
`studio cards linkedin` · `studio search "linkedin comment SLA hook"`
