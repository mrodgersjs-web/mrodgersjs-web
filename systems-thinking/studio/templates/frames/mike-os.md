# System Frame — Mike OS (installed regulators)

Grounded in jake-load / jake-greet / Gate-D / A_ops. Fill currents; do not invent.

## 1. Boundary
- System of interest: Mike + Jake across sessions (not the whole fleet)
- Inside: capacity.yaml, greet, observe, session-end, A_ops cap, Gate-D
- Outside: OpenBot, Hermes crons, LinkedIn algorithm, family
- Boundary rationale: if it does not change a counted stock this week, it is outside

## 2. Stocks
| Stock | Unit | Current | Owner |
|---|---|---|---|
| open loops | items | | jake-load |
| context | fresh→rotten | | jake-session-end |
| A_ops remaining | min/day | | aops |
| recorded deals | count | | sales |
| observations of Mike | notes | | jake-observe |

## 3. Flows
`jake-greet` resets context. `jake-load` gates new starts.
`aops gate` charges minutes. Gate-D holds outward action.

## 4. Actors
Mike, Jake, A_ops, Gate-D, department heads (Ralph/Darius/Cora).

## 5. Loops
- R1 polymath engine (curiosity compounding)
- B1 jake-load regulator (too weak if `over` never fires)
- R2 revenue compounding (starved if deals = 0)
- B_aops: predicted load > 70% cap → shed BEFORE first page

## 6. Delays
context rot across overnight. Prediction MAE on A_ops (doctor reports it).

## 7. Archetype suspects
Shifting the Burden (build crons vs sell). Fixes that Fail (new project).
Limits to Growth (≤2 high-touch). Escalation (fleet vs imaginary competitor).

## 8. Leverage (already installed — tune, don't rebuild)
1. Parameters — `~/.jake/systems/capacity.yaml`
2. Information — `jake-greet` every session
3. Delays — `.last_session`
4. Rules — pushback, Gate-D, finish-before-start
5. Structure — Jake on 4 surfaces
6. Goals — JAKE_DIRECTION
7. Paradigm — breadth compounds through SYSTEMS

## 9. Measurement
- `jake-load` verdict
- A_ops `aops doctor` (honest RED on MAE is a finding)
- recorded deals ≠ 0
- Falsifier: greet skipped 3 sessions OR load `over` ignored → regulators are theater

## 10. Corpus
This frame + `studio cards systems-thinking` + MIKE_MODEL.md
