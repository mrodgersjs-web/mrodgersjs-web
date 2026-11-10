# Deep Process 01 — INTAKE → `brief.md`

> Deepens `processes/phases.md` §01. Harness gate: `run_phase 01 INTAKE brief.md`
> greps for `## Problem` and `## Success looks like` (case-insensitive). Retry ≤2
> with written feedback (`feedback-01-<attempt>.txt`); 3rd failure = RED = run
> stops. A phase that produces no artifact logs DEGRADED — never silently skipped.

## Purpose

INTAKE converts a one-line ask into the run's contract. Everything downstream
(frame, diagnosis, leverage, grounding, synthesis) is checked against this
brief; later phases may tighten it but never silently shrink it. The brief's
real job is threefold: (1) separate what was *observed* from what is *inferred*,
(2) pin the requester's authority (which caps the leverage rank chosen in phase
04), and (3) declare the unknowns now, so no later phase invents facts to fill
them. A weak intake produces a confident analysis of the wrong problem; a strong
intake makes invention downstream structurally hard.

## Entry criteria

- `harness/systems-studio.sh "<problem statement>"` has created
  `$RUN` (`~/.rig/systems-studio/runs/<ts-slug>/`) and written `problem.txt`.
- The problem statement names an observable symptom (something moving or
  stuck), not just a topic. If it names only a topic ("our GTM"), ask for the
  symptom before proceeding — intake of a topic is a red flag, not a blocker.
- No prior artifacts exist in `$RUN` (intake is first).

## Inputs

| Input | Where | Use |
|---|---|---|
| `problem.txt` | `$RUN/problem.txt` | raw one-line ask — the only source of given facts |
| Requester identity / authority | conversation or inference | caps leverage rank; `Unknown` allowed |
| `studio doctor` | `scripts/studio.py` | corpus availability: card-index, Recall key, data files |
| `data/archetypes.json`, `data/leverage-points.json` | `/inputs/` (mounted) | vocabulary for symptom restatement and rank-12 spotting |
| Deadline / cadence context | conversation | `## Deadline` section; `Unknown` allowed |

Given facts are ONLY those in `problem.txt` plus what the requester states in
conversation. Everything else is `Unknown` until measured.

## Procedure

1. [det] `cat $RUN/problem.txt` — read the raw ask verbatim; do not paraphrase yet.
2. [agent] Restate the problem in `## Problem` as a system question: name the
   thing that changed (or stalled), over what window, and what the naive
   intervention has been. One tight paragraph, no solutions.
3. [agent] Split observation from interpretation. Observations (from
   `problem.txt`) get stated as numbers/trends; interpretations get marked
   "suspected" or "inferred". If a fact is absent, write `Unknown` — never a
   plausible filler number.
4. [agent] Extract the symptom words in plain verbs+nouns ("plateau",
   "keeps coming back", "quick fix", "arms race") — these feed `studio map`
   in phases 02/03. Record them in the brief's problem paragraph.
5. [agent] Name the requester and, critically, their authority: what can this
   person change alone (parameters? information flows? rules? the goal?).
   This becomes the ceiling for phase 04's chosen rank. `Unknown` allowed,
   but then phase 04 must reason from the inferred owner.
6. [agent] Write `## Success looks like` as 3-5 observable outcomes with units
   and a decoupling clause (what must NOT rise for success to count — e.g.
   "yield resumes while output is held or reduced").
7. [agent] Write `## Stakes`: cost of being wrong, cost of another quarter of
   the current intervention, what compounds while unsolved.
8. [agent] Write `## Constraints`: boundary hints, forbidden moves, data
   availability, org realities. Include corpus availability from step 9.
9. [det] `python3 studio.py doctor` — record PASS/FAIL/WARN per line. If
   card-index or Recall key is missing, the brief MUST say so (it constrains
   phase 05 to archetypes+leverage data and makes absent evidence a finding,
   not a surprise).
10. [agent] Write `## Deadline`: decision horizon and the measurement window
    the requester can tolerate. If absent, infer from the symptom window
    ("the six-week stall is already the delay window — treat as now").
11. [agent] Write `## Requester`: who owns the outcome; if unknown, the
    inferred owner and what owning it implies for authority.
12. [agent] Scan the brief for invented quantities. Any number that is not in
    `problem.txt`, not from the requester, and not marked `Unknown`-adjacent
    is a fabrication — delete it or mark it.
13. [agent] Add a "forbidden next experiments" line when the naive
    intervention is already identifiable as the pathology (e.g. "do not add
    posting volume"). This pre-commits phase 04 against the obvious wrong move.
14. [det] Write the artifact to `outputs/brief.md` (harness copies it to
    `$RUN/brief.md`). Keep it tight: the brief only.
15. [det] Harness greps `## Problem` and `## Success looks like`. On miss,
    read `feedback-01-<attempt>.txt` and fix exactly the named sections.
16. [agent] Self-audit against the checks below BEFORE the harness runs —
    the retry budget (2) is for surprises, not for skipping this list.

## Deterministic checks

Mirror of the harness gate (must pass before deeper checks matter):

1. `grep -qi '^## Problem' brief.md` — problem section present.
2. `grep -qi '^## Success looks like' brief.md` — success section present.

Deeper gates (add to any CI/harness wiring of this phase):

3. Full section set: `grep -c '^## ' brief.md` ≥ 6 and each of
   `Stakes`, `Constraints`, `Deadline`, `Requester` matches case-insensitively.
4. Unknowns declared, not hidden: `grep -ci 'unknown' brief.md` ≥ 1.
5. Numbers guard — every numeral in the brief either appears in `problem.txt`
   or sits on a line flagged as unmeasured:
   ```bash
   python3 - <<'PY'
   import re
   brief=open('brief.md').read(); prob=open('problem.txt').read()
   pn=set(re.findall(r'\d+(?:\.\d+)?',prob))
   bad=[l.strip() for l in brief.splitlines()
        if set(re.findall(r'\d+(?:\.\d+)?',l))-pn
        and not re.search(r'(?i)unknown|not invent|unmeasured|do not|window|week',l)]
   print('NUMBERS GUARD:','PASS' if not bad else 'FAIL '+str(bad))
   PY
   ```
6. Symptom vocabulary present for downstream `studio map`: the problem
   paragraph contains ≥2 plain-words symptom tokens (manual check; the map
   scorer matches symptom phrases like "plateau", "quick fix", "arms race").

## Failure modes

1. **Topic intake** — the ask names a domain ("our GTM engine") with no
   observable symptom. Countermeasure: require the changed/stuck variable and
   its window before writing `## Problem`; a brief without a symptom sends
   phase 03 noise that maps to nothing.
2. **Fabricated baseline** — plausible funnel numbers invented to make the
   brief look analytical. Countermeasure: numbers guard (check 5); only
   `problem.txt` and requester statements are given facts.
3. **Solution smuggling** — `## Success looks like` names an intervention
   ("successfully migrate to X") instead of an outcome. Countermeasure:
   success must be an observable stock/flow state with units, decoupled from
   the suspect intervention; write the decoupling clause explicitly.
4. **Authority amnesia** — requester's authority unrecorded, so phase 04
   chooses a rank nobody can hold. Countermeasure: `## Requester` must state
   what this person can change alone; phase 04 re-reads it as a hard cap.
5. **Silent corpus fiction** — brief assumes cards/search exist; phase 05
   then "cites" a corpus that was never mounted. Countermeasure: embed the
   `studio doctor` verdict in `## Constraints` (see worked example).
6. **Deadline drift** — no time box, so the falsifier in later phases gets
   no date. Countermeasure: `## Deadline` may say Unknown, but must then
   bind the measurement window to the symptom window already observed.
7. **Contract bloat** — brief grows into an essay; every later phase re-litigates
   it. Countermeasure: brief ≤ ~40 lines; detail belongs in frame.md.

## Worked example

From `~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/brief.md`
(problem: "Our LinkedIn content engine tripled output but replies and leads
have plateaued for 6 weeks - figure out why from a systems perspective and
what to do"):

- Observation/interpretation split, with the naive intervention named and
  refused up front (`brief.md` §Problem):
  > "The content engine tripled posting output. Replies and leads have been
  > flat for six weeks. Volume is no longer the binding constraint; a
  > balancing loop (audience attention, relevance, distribution, or conversion
  > capacity) is offsetting the growth loop."
- Success with units AND a decoupling clause (`brief.md` §Success):
  > "Replies and qualified inbound leads resume growth while output is held
  > or reduced (volume decoupled from the KPI)."
- Corpus honesty from `studio doctor` baked into constraints (`brief.md`):
  > "No live corpus/cards this run (studio doctor: no card-index / Recall
  > key). Use archetypes + leverage points only."
- Pre-committed anti-move (`brief.md` §Constraints):
  > "Do not add posting volume as the next experiment."
- Deadline bound to the symptom window (`brief.md` §Deadline):
  > "Unknown. Treat the six-week stall as now … testable inside the next
  > two-week window."

That brief held: the run's later phases never invented funnel numbers and
never proposed more volume.

## Depth extensions

- **Authority ladder pre-fill**: map the requester onto Meadows ranks now
  (can they change parameters only? information flows? rules? the goal? the
  paradigm?) and record it as a one-line ladder; phase 04 then argues rank
  choice against a written ceiling instead of vibes.
- **Two-symptom split**: when the ask contains two symptoms (here: replies
  flat AND leads flat), record each with its own stock and window; divergent
  windows are the cheapest early discriminator between candidate archetypes.
- **Stakeholder pre-inventory**: list actors who pull the stocks (feeds frame
  §4); 5 minutes here saves a phase-02 retry.
- **Falsifier seed**: draft the kill-condition in the brief ("if X within N
  weeks, this framing is wrong"); phases 02/07 only refine and inherit it.
- **Prior-run diff**: if `$RUNS/` contains earlier runs on the same system,
  diff their briefs — a recurring problem statement is itself archetype
  evidence (Fixes That Fail / Shifting the Burden vocabulary).

## Handoff

Phase 02 FRAME receives, via `/inputs/brief.md`:
- the precise problem restatement + symptom vocabulary for `studio map`;
- constraint list (boundary hints, forbidden moves, corpus availability);
- requester + authority ceiling (phase 04 reads this as its rank cap);
- success outcomes with units (become frame §9 stock-health metrics);
- deadline/measurement window (becomes the falsifier's N weeks).
The brief is frozen at GREEN: later phases cite it, they do not edit it.
