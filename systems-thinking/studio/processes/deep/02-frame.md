# Deep Process 02 — FRAME → `frame.md`

> Deepens `processes/phases.md` §02 and `workflows/frame-system.md`. Harness
> gate: `run_phase 02 FRAME frame.md` greps `Stocks`, `Reinforcing`, `Balancing`,
> `Delay` (case-insensitive). Template: `templates/system-frame.md` (10 numbered
> sections), printed by `studio frame "<system>"`. "Unknown is an answer; blank
> is not."

## Purpose

FRAME turns the intake contract into the run's structural model: boundary,
stocks, flows, actors, loops, delays, measurement. It is the artifact every
later phase reasons over — diagnosis matches archetypes against its loops,
leverage rewrites its structure, grounding checks its claims, polymath imports
into its constraint. The frame's discipline is accumulation-first: name what
persists (stocks) before rates (flows), and name the time between action and
observable effect (delays) before proposing any action. Most bad interventions
are frames that never named the delay or the hidden balancing loop.

## Entry criteria

- Phase 01 GREEN: `$RUN/brief.md` exists (harness mounts it at `/inputs/brief.md`).
- The brief contains at least one observable symptom with a window.
- Template and data mounted at `/inputs/`: `system-frame.md`,
  `archetypes.json`, `leverage-points.json`.

## Inputs

| Input | Where | Use |
|---|---|---|
| `brief.md` | `/inputs/brief.md` | contract: boundary hints, units, forbidden moves |
| `templates/system-frame.md` | `/inputs/system-frame.md` | the 10-section scaffold to fill (copy, don't reimagine) |
| `data/archetypes.json` | `/inputs/archetypes.json` | symptom vocabulary; suspects for §7 |
| `data/leverage-points.json` | `/inputs/leverage-points.json` | rank semantics for §8 |
| `studio map "<symptoms>"` | CLI (copy studio.py out first) | archetype ranking to seed §7 |
| `studio leverage` | CLI | 12 ranks for §8's one-rank-higher |

## Procedure

1. [det] Scaffold: `cp /inputs/studio.py . && python3 studio.py frame "LinkedIn
   content engine"` (or copy `/inputs/system-frame.md`). Work IN the copy —
   the 10 numbered headings are the contract.
2. [agent] §1 Boundary: list inside (what we control/account for) vs outside
   (environment to adapt to), then write the boundary RATIONALE — why here and
   not one step wider or narrower. Test both directions explicitly: wider
   mixes confounds in, narrower drops the suspected limiter out.
3. [agent] §2 Stocks: every accumulation that persists, one table row each,
   with unit, current level (`Unknown` allowed), and owner. Stocks to hunt:
   work-in-progress, trust, backlog, attention, capacity/skill, belief. If a
   row's unit column is empty you have a topic, not a stock — fix or cut.
4. [agent] §3 Flows: for each stock, the inflow and outflow with rates
   (`Unknown` allowed, "3× prior" counts as a rate statement when given).
   Rule: every flow row must name which stock it fills/drains.
5. [agent] §4 Actors & incentives: who wants what, and which stock each actor
   pulls toward which level. Include the platform/algorithm as an actor when
   relevant — it is outside the boundary but routes the flows.
6. [agent] §5 Loops — the analytical core:
   - ≥1 reinforcing loop R (cause → effect → more cause). Name each (R1, R2…)
     and say what it compounds.
   - ≥1 balancing loop B with an explicit GOAL ("B1 (goal: finite audience
     attention)"). If only R loops appear, ask what limits them — that
     constraint IS a hidden B loop; write it down.
   - Flag the pathology loop separately when the current intervention is a
     loop (e.g. "R3 (pathology): volume praised → more shipped → rewarded").
7. [agent] §6 Delays: table of between/and/delay-length/consequence
   (overshoot? oscillation?). Minimum two rows; every loop from §5 should
   have its action→effect delay represented somewhere here.
8. [det] §7 seed: `python3 studio.py map "<symptom words from brief>"` —
   paste top suspect + matched symptoms + confidence; add evidence for/against
   from §2/§3 stock motions. Full verification is phase 03's job; here it is a
   suspect with evidence, not a conclusion.
9. [det] §8 seed: `python3 studio.py leverage` — record where current
   interventions sit (rank number) and the one-rank-higher option as a
   hypothesis. Phase 04 will own the full walk; do not skip the seeding.
10. [agent] §9 Measurement plan: stock-health metric (from brief's success
    units), a LEAD indicator that moves BEFORE the longest §6 delay elapses,
    and a falsifier with an N-week deadline inherited from the brief.
11. [det] §10 Corpus check: `python3 studio.py cards systems-thinking` and
    `python3 studio.py search "<topic>" exhaustive` (if key present). Record
    hits or record their absence honestly ("none this run" + doctor verdict).
12. [agent] Consistency pass: every stock in §2 appears in §3 (flow) and §5
    (loop) or is explicitly labeled dangling; every B loop's goal names a
    stock level; every delay row's consequence says overshoot/oscillation or
    "hides the causal link".
13. [agent] Honesty pass: scan for blank cells and filler ("TBD", "various",
    "n/a") — replace with `Unknown` + what measurement would resolve it.
14. [det] Write to `outputs/frame.md`; harness greps the four gate words.
    On miss, fix exactly the sections named in `feedback-02-<attempt>.txt`.
15. [det] Pre-GREEN deep-check run: execute checks 2-6 below against
    `outputs/frame.md` (unit guard, loop-goal guard, delay consequences,
    dated falsifier, blank-cell ban) BEFORE spending a harness retry.
16. [agent] Loop-ID lint: the R/B identifiers minted in §5 are the tokens
    every later phase cites (diagnosis's B1/B2 discriminator, leverage's
    loop-arming, synthesis's story). Rename any generic label ("the feedback
    loop", "vicious cycle") to an ID now, and confirm each ID appears in
    both §5 and the delay table or §9's indicator list.

## Deterministic checks

Mirror of the harness gate:

1. `grep -qi 'stocks' frame.md` / `grep -qi 'reinforcing' frame.md` /
   `grep -qi 'balancing' frame.md` / `grep -qi 'delay' frame.md`.

Deeper gates:

2. No blank stock units — every §2 table row has a non-empty unit cell:
   ```bash
   python3 - <<'PY'
   import re
   rows=[r for r in open('frame.md').read().splitlines() if re.match(r'^\|[^|]+\|',r)]
   bad=[r for r in rows[2:] if len([c for c in r.split('|') if c.strip()])<4
        and not re.search(r'(?i)unknown',r)]
   print('UNIT GUARD:','PASS' if not bad else 'FAIL '+str(bad))
   PY
   ```
   (table separator rows and header exempted; "Unknown" counts as filled).
3. Loop naming: `grep -cE '\bR[0-9]' frame.md` ≥ 1 and `grep -cE '\bB[0-9]'
   frame.md` ≥ 1; every B loop carries a goal: `grep -E 'B[0-9].*\(goal'
   frame.md` returns ≥1 line.
4. Delay consequence present: ≥2 rows in the §6 table (`grep -A4 '^## 6'`),
   and at least one mentions overshoot, oscillation, or hidden-link effect.
5. Falsifier is dated: §9 contains a number + week/day horizon
   (`grep -E '[0-9]+ ?weeks?' frame.md`).
6. Blank-cell ban: `grep -nE '\|\s*\|' frame.md` returns no table row with an
   empty middle cell except allowed `Unknown` rows (manual confirm of any hit).

## Failure modes

1. **Frame theater** — all ten sections filled with restatements of the brief;
   no stock ever named with a unit. Countermeasure: unit guard (check 2);
   a unit forces the stock to be a countable accumulation.
2. **Loop decoration** — R/B loops drawn as prose arrows that never touch a
   stock ("morale improves → things get better"). Countermeasure: each loop
   sentence must name which stock rises/falls at each arrow; B loops must
   state the goal level they defend.
3. **Boundary convenience** — boundary drawn to make the requester look
   all-powerful (everything inside) or blameless (limiter outside).
   Countermeasure: §1 must argue BOTH the wider and narrower cut and why this
   line wins; the rationale is graded in review.
4. **Delay blindness** — delays table filled with "immediate" or omitted;
   later interventions then chase last month's signal. Countermeasure:
   check 4 requires ≥2 rows with consequences; ask per loop "how long before
   the loop's effect is observable?".
5. **Measurement without a lead** — §9 names only the lagging outcome metric.
   Countermeasure: require one indicator that moves before the longest delay
   (a flow, pre-delay); if none exists, the frame must instrument first.
6. **Suspect laundering** — §7 states the archetype as fact, prejudging phase
   03. Countermeasure: §7 language is "suspect + evidence + confidence from
   map output"; verification of predicted-stock motion belongs to diagnosis.
7. **Template mutation** — agent invents its own section names, breaking the
   grep gates and downstream readers. Countermeasure: copy
   `/inputs/system-frame.md`; keep the 10 numbered headings verbatim.
8. **Unknown-shyness** — blanks replaced by guesses because Unknown feels
   sloppy. Countermeasure: doctrine line in the template header ("Unknown is
   an answer; blank is not") plus honesty pass step 13.

## Worked example

From `~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/frame.md`:

- Boundary argued in both directions (`frame.md` §1):
  > "Wider (all demand gen / sales pipeline) mixes LinkedIn with other
  > channels and hides the volume→yield mismatch. Narrower (posting calendar
  > only) excludes the conversion stocks (replies, reply capacity, lead
  > definition) that are the suspected limiter. The stall is at yield, not at
  > 'content shipped.'"
- Stocks with units and honest levels (`frame.md` §2):
  > "| Unanswered inbound (comment/DM backlog) | threads waiting | Unknown;
  > suspected rising with volume | Whoever replies |"
  > "| Team belief 'activity = demand' | implicit operating goal | High
  > (volume still the intervention) | Engine owner |"
- The hidden balancer made explicit, goal stated (`frame.md` §5):
  > "B1 (goal: finite audience attention): more posts per unit attention →
  > skip/mute/fatigue → less attention per post → replies/leads flat.
  > Strengthens as R3 runs. **Primary limiter suspect.**"
- Delay with consequence (`frame.md` §6):
  > "| Thin-post volume | Trust / mute / reach decay | Weeks (here: ~6
  > already) | Side-effect of R3 hidden until plateau; overshoot of posting |"
- Suspect kept a suspect (`frame.md` §7):
  > "Primary suspect: **Limits to Growth** [likely — matched: plateau,
  > ceiling, capacity, diminishing returns, more effort same result]."

## Depth extensions

- **Loop dominance over time**: annotate each loop with when it dominates
  (R1 early, B1 after attention saturates); dominance shifts are where phase
  transitions and regime changes live.
- **Stock-flow consistency math**: for the 2-3 load-bearing stocks, write
  net-rate = inflow − outflow and state the sign; a plateaued stock with a
  positive net rate is a contradiction that kills the frame.
- **Second-order loops**: add B-loops that regulate the R-loops' regulators
  (e.g. algorithm damping as a B on R2); archetype mixes (Limits to Growth +
  Tragedy of the Commons) usually need them.
- **Counter-frame**: write the strongest alternative boundary/loop set and
  what observation would favor it; hand both to phase 03 as competing
  hypotheses rather than one pet theory.
- **Instrument map**: per `Unknown` stock cell, name the exact query/log/
  export that would fill it and its cost — phase 05's Gaps section inherits
  this list verbatim.
- **Actor pull-weights**: rank actors by pull strength on the contested
  stock; weak-strong misordering is the root of policy-resistance diagnoses.

## Handoff

Phase 03 DIAGNOSE receives `/inputs/frame.md`:
- the loop set (R/B with goals) to match against archetype templates;
- stock motion claims (§2/§3) to verify predicted stocks against;
- §7's seeded suspects + matched symptom words for `studio map`;
- §6 delay table (the archetype's "after a delay" clause lands here);
- the instrument map of unresolved Unknowns (feeds diagnosis's
  "what we cannot verify yet" and phase 05's Gaps).
The frame is frozen at GREEN; diagnosis may falsify it but not edit it.
