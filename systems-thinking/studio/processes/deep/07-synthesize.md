# Deep Process 07 — SYNTHESIZE → `DELIVERABLE.md`

> Deepens `processes/phases.md` §06 (artifact name and gates unchanged as the
> phase shifts to slot 07 in the 8-phase chain). Harness gate:
> `run_phase 07 SYNTHESIZE DELIVERABLE.md` greps `## What is happening`,
> `## What to do`, `## Falsifier`, `## Rejected` (case-insensitive). Doctrine
> line from the phase prompt: "No new claims after grounding; synthesis
> organizes, it does not invent."

## Purpose

SYNTHESIZE compresses six prior artifacts into the one document a decision-
maker reads: the system story, the ranked interventions, the kill condition,
and the honest refusals. Its discipline is subtraction under fidelity —
everything must trace to brief/frame/diagnosis/leverage/grounding/polymath,
nothing new enters here, and everything load-bearing must survive. The
deliverable is also the run's public face: phase 08 seals it byte-for-byte,
so a claim that cannot be traced is a liability that ships with a hash on it.

## Entry criteria

- Phases 01-06 GREEN: brief, frame, diagnosis, leverage, grounding, polymath
  all exist and are non-empty in `$RUN` (mounted as `/inputs/`).
- Grounding's verified/unverified split is known; any confidence demotions
  are recorded in grounding.md.
- No open contradiction between leverage.md and diagnosis.md (phase 04 step
  10 reconciled them); if one emerged late, resolve it BEFORE writing here.

## Inputs

| Input | Where | Use |
|---|---|---|
| `brief.md` | `/inputs/brief.md` | success units, authority, forbidden moves, deadline |
| `frame.md` | `/inputs/frame.md` | boundary, stocks, loops R/B, delays — the story's spine |
| `diagnosis.md` | `/inputs/diagnosis.md` | verified archetype, constraint class, discriminator, counterintuitive |
| `leverage.md` | `/inputs/leverage.md` | chosen rank, support cast, rejected-higher rationale |
| `grounding.md` | `/inputs/grounding.md` | verified claims only; gaps; corpus tiering |
| `polymath.md` | `/inputs/polymath.md` | ≤3 top imports w/ metrics, rank tags, kill conditions |

## Procedure

1. [agent] Re-read all six inputs end to end. List every load-bearing claim
   with its source artifact. This claim ledger is your fidelity contract —
   anything not on it cannot appear as fact in the deliverable.
2. [agent] `## What is happening`: the system story in decision-maker
   language. Pattern (proven in the E2E run): the observable change → the
   verified archetype with confidence → inside/outside boundary in one line →
   the loops in play (R/B with one-phrase mechanics, pathology loop flagged)
   → the candidate constraints with the discriminator → the delays that hide
   it → the counterintuitive point, quoted and marked accepted → secondary
   archetypes as "not the diagnosis" → the unverified remainder stated as
   findings, not doubts.
3. [agent] Story discipline: every number and stock motion in the story must
   exist in the ledger (step 1). Where a level is Unknown, say Unknown — the
   phrase "which limiter is tightening is Unknown" is a deliverable-grade
   sentence, not an embarrassment.
4. [agent] `## What to do`: ranked interventions. Rules:
   - each entry: **Rank N — name**, owner, the change, one-line why;
   - order by rank authority (chosen rank first, support cast after);
   - the success criterion restated with its decoupling clause from the brief;
   - the instrument window (discriminator from diagnosis) included as its
     own step — freezing/steering before concluding;
   - polymath imports appear ONLY in their grounded form (metric + unit +
     firing condition), usually as instruments inside the chosen rank.
5. [agent] `## Falsifier`: inherit the diagnosis falsifier verbatim in
   spirit — observation + deadline + the constraint-side-only clause (a
   volume-side "test" that keeps the frame alive is analysis insurance, not
   a falsifier). Fold in polymath kill conditions and the reporting-artifact
   kill condition when the frame flagged one.
6. [agent] `## Rejected`: the honest refusals, each with its reason —
   the existing intervention (with why it is the pathology), the
   rejected-higher rank (from leverage, with the why-not-now), premature
   constraint-picking, metaphor-only polymath imports, boundary widening/
   narrowing, and corpus limitations when degraded.
7. [agent] Anti-invention audit: walk every sentence carrying a number,
   named stock motion, or causal claim; verify each against the ledger.
   Cut or attribute ("per frame.md") anything unreachable.
8. [agent] Length discipline: the deliverable is tight — roughly 60-100
   lines. Depth lives in the prior artifacts; repetition here is noise a
   decision-maker must pay for.
9. [agent] Read it cold: would a person who owns this system know what to
   do Monday, what NOT to do, and how they'll know they were wrong? If any
   of the three is missing, the synthesis is incomplete.
10. [det] Write `outputs/DELIVERABLE.md`; harness greps the four sections.
    On miss, fix exactly the named sections from `feedback-07-<attempt>.txt`.
11. [agent] Rejection-quality pass: for each `## Rejected` entry, confirm
   the reason is a REASON (authority gap, unfalsifiable in window,
   unverified premise), not a restatement of the choice. Weak reasons get
   upgraded from leverage.md's recorded rationale.
12. [agent] Cross-artifact numeral sweep: every number in the deliverable
   must also exist in a prior artifact; numerals appearing ONLY here go
   back to step 7's audit. (The no-new-claims guard below mechanizes this.)
13. [det] Pre-GREEN deep-check run: execute checks 2-6 below against
   `outputs/DELIVERABLE.md` — rank coverage, owner coverage, dated
   constraint-side falsifier, no-new-claims guard, rejection substance.
14. [det] Cross-artifact coherence grep: the archetype name in the
   deliverable matches diagnosis.md's suspect verbatim; the chosen rank
   number matches leverage.md; the success units match brief.md. A
   mismatch means synthesis drifted — fix the story, not the sources.
15. [agent] Freeze declaration: after GREEN, DELIVERABLE.md is immutable —
   phase 08 hashes it. Late insights go to a follow-up run, not an edit;
   append the run date to the header as the freeze stamp.

## Deterministic checks

Mirror of the harness gate:

1. `grep -qi '^## What is happening' DELIVERABLE.md`;
   `grep -qi '^## What to do' DELIVERABLE.md`;
   `grep -qi 'falsifier' DELIVERABLE.md`;
   `grep -qi '^## Rejected' DELIVERABLE.md`.

Deeper gates:

2. Rank coverage — every intervention entry carries a rank:
   `grep -cE 'Rank [0-9]+' DELIVERABLE.md` ≥ (number of intervention
   entries in `## What to do`; minimum 3 in practice: chosen + ≥2 support).
3. Owner coverage — each top entry names an owner: within
   `## What to do` context, `grep -cEi 'owner|requester'` ≥ entries.
4. Falsifier is dated and side-constrained:
   `grep -A6 '^## Falsifier' DELIVERABLE.md | grep -E '[0-9]+ ?weeks?'
   ` hits AND a constraint-side clause
   (`grep -AiE 'not (more|a) (posts|volume)|constraint-side'`).
5. No-new-claims guard — numeric sentences must trace to prior artifacts:
   ```bash
   python3 - <<'PY'
   import re,glob
   prior=' '.join(open(f).read() for f in ['brief.md','frame.md','diagnosis.md',
                                           'leverage.md','grounding.md','polymath.md'])
   d=open('DELIVERABLE.md').read()
   sents=[s for s in re.split(r'(?<=[.!?])\s+',d)
          if re.search(r'\d',s) and not re.search(r'(?i)rank \d|week|falsifier',s)]
   orphan=[s for s in sents if not any(w in prior for w in
           re.findall(r'\b[a-z]{6,}\b',s.lower())[:4])]
   print('NO-NEW-CLAIMS:','PASS' if not orphan else 'FAIL '+str(orphan[:3]))
   PY
   ```
6. Rejection substance — `## Rejected` has ≥3 entries with reasons
   (`grep -A30 '^## Rejected' DELIVERABLE.md | grep -cE '^- |\*\*'` ≥ 3).

## Failure modes

1. **Synthesis invention** — a new statistic or causal claim appears that no
   prior artifact contains (the pressure to sound complete does it).
   Countermeasure: claim ledger (step 1) + no-new-claims guard (check 5);
   when in doubt, attribute or cut.
2. **Falsifier softening** — the kill condition quietly widens ("monitor
   over the next quarter") so the analysis can never lose. Countermeasure:
   check 4 enforces the dated window + constraint-side clause; the deadline
   comes from the brief, not from comfort.
3. **Rank laundering** — interventions listed without ranks, or support-cast
   ranks presented as co-equal plays, diluting the authority logic.
   Countermeasure: check 2 rank coverage; chosen rank leads, support labeled
   as support.
4. **Unknown-scrubbing** — final polish replaces "Unknown" with vague
   assertions ("attention is likely saturated") to sound decisive.
   Countermeasure: keep the Unknown sentences verbatim; decisiveness lives
   in the plan, not in pretend data.
5. **Metaphor resurrection** — a polymath import that was rejected as
   metaphor-only reappears as flavor ("think of it as entropy").
   Countermeasure: polymath.md's rejected list is a blocklist for this
   artifact; grep the deliverable for the rejected mechanism names.
6. **Kitchen-sink deliverable** — every prior artifact pasted in; the reader
   gets 400 lines and reads none. Countermeasure: 60-100 lines (step 8);
   the run dir carries the depth, the deliverable carries the decision.
7. **Orphan instrument** — the discriminator window appears in the story but
   not in the plan (or vice versa), so the test never runs. Countermeasure:
   the instrument window is a numbered entry in `## What to do` (step 4).
8. **Post-GREEN editing** — deliverable touched after phase 08 sealed it,
   breaking the ProofPacket silently. Countermeasure: freeze rule (step 11);
   phase 08's verify.py turns any drift into a hard FAIL.

## Worked example

From `~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/DELIVERABLE.md`:

- Story opens with observation, then verified label with confidence
  (`DELIVERABLE.md` §What is happening):
  > "The engine removed the posting constraint. Output is ~3× prior
  > run-rate. Replies and qualified inbound leads have not followed —
  > plateaued ~6 weeks… **Limits to Growth [likely].** … Observed: posts/
  > effort moving; yield flat as predicted; which limiter is tightening is
  > **Unknown**."
- Loops compressed to one phrase each (`DELIVERABLE.md`):
  > "R3 (pathology): volume praised → templates/cadence → more posts
  > shipped → rewarded → more volume. This is the loop still being pushed
  > (Meadows rank 12)."
- Intervention with rank + owner + success clause (`DELIVERABLE.md` §What to do):
  > "1. **Rank 3 — Goals.** Owner: engine owner (requester). Restate the
  > operating goal as conversation / qualified-lead yield with output held
  > or reduced — not posts shipped. Pin the lead definition. Freeze cadence
  > for the two-week instrument window."
- Falsifier with both kill conditions (`DELIVERABLE.md` §Falsifier):
  > "After a **constraint-side** change (goal / information / reply slack /
  > relevance bar — **not** more posts), if replies and qualified inbound
  > leads remain flat **four weeks**, this frame is wrong."
- Rejected doing real work (`DELIVERABLE.md` §Rejected):
  > "**Rank 2 paradigm** … Paradigm work is slow, unfalsifiable inside four
  > weeks, and will not stick while dashboards still score posts."

## Depth extensions

- **Decision-theater variant**: add a one-page decision memo on top (option
   set, irreversibility, cost of delay) for executives; the systems story
   stays, the ranking becomes a choice architecture.
- **Intervention sequencing map**: order the support-cast ranks into weeks
   (what must precede what for the chosen rank to hold); a rank-3 goal
   change without its rank-6 signal on day one is a slow failure.
- **Pre-mortem paragraph**: "it is N weeks later and yield is still flat —
   the three most likely reasons, in order" drawn ONLY from prior artifacts
   (wrong constraint picked, reporting artifact, outside-boundary shift);
   each gets a tell-tale so the failure is diagnosable when it happens.
- **Adversarial red-team pass**: spawn a reviewer prompt that argues the
   deliverable is wrong using ONLY the run's own artifacts; surviving
   objections get folded into Rejected/Falsifier before phase 08.
- **Traceability footnotes**: line-cite each load-bearing claim to its
   source artifact (`frame.md §5`); costs 10 lines, buys audit speed when
   the ProofPacket is challenged.
- **Instrument-first deliverable**: when the discriminator dominates (most
   Unknowns), invert the plan: the deliverable's `## What to do` leads with
   the 2-week instrument and defers all structure changes to its readout —
   explicitly refuse to prescribe before measuring.

## Handoff

Phase 08 VERIFY receives `$RUN/DELIVERABLE.md` plus the full artifact set:
- the complete chain brief → frame → diagnosis → leverage → grounding →
  polymath → DELIVERABLE, all GREEN, all frozen;
- the falsifier (dates + clauses) that verify greps for;
- rank tags that the structure check (`\[[0-9]+\]|rank` on leverage.md,
  falsifier on DELIVERABLE.md) confirms;
- nothing else: VERIFY is deterministic only — it reads, it does not reason,
  and its output (verify.log + proofpacket.json) is the run's seal.
