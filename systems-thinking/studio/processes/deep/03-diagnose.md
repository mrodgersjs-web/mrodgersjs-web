# Deep Process 03 — DIAGNOSE → `diagnosis.md`

> Deepens `processes/phases.md` §03 and `workflows/diagnose-archetype.md`.
> Harness: `run_phase 03 DIAGNOSE diagnosis.md` ships the section requirements
> in its prompt (`## Suspect`, `## Evidence`, `## Counterintuitive point`) but
> NO grep checks — the deep gates below close that hole. Diagnosis is where
> the studio earns its name: the archetype's predicted stock must be verified
> as actually moving before the label sticks.

## Purpose

DIAGNOSE tests the frame against the canonical system archetypes
(`data/archetypes.json`, 10 entries) and converts a suspect into a verified
structural diagnosis or an honest rejection. The archetype is a falsifiable
prediction machine: each one predicts specific stock motions (Limits to
Growth predicts an accelerating growth stock, a plateauing performance stock,
and a tightening constraint). The phase's core discipline is stock
verification — if the archetype's predicted stock is not measurably moving,
suspect a different archetype, however good the story feels. Second
discipline: the counterintuitive point must be quoted and explicitly accepted
or rejected, because it is the sentence most likely to be true and least
likely to be believed.

## Entry criteria

- Phase 02 GREEN: `$RUN/frame.md` exists with loops, stocks, delays, and a
  seeded §7 suspect (mounted at `/inputs/frame.md`).
- Symptom words available (from brief + frame §7).
- `studio.py` copied into the working directory (harness convention:
  `cp /inputs/studio.py .`).

## Inputs

| Input | Where | Use |
|---|---|---|
| `frame.md` | `/inputs/frame.md` | loops/stocks to verify predictions against |
| `brief.md` | `/inputs/brief.md` | given facts only — no numbers beyond it |
| `studio map "<symptoms>"` | CLI | deterministic archetype ranking + matched symptoms |
| `studio archetype <id>` | CLI | full story/diagnosis/intervention/counterintuitive for one archetype |
| `data/archetypes.json` | `/inputs/archetypes.json` | the 10 canonical templates (ids: limits-to-growth, shifting-the-burden, eroding-goals, fixes-that-fail, tragedy-of-the-commons, growth-and-underinvestment, success-to-the-successful, escalation, policy-resistance, addiction) |

## Procedure

1. [det] Assemble the symptom text: plain verbs+nouns from the brief plus the
   frame's constraint language ("plateau", "quick fix", "keeps coming back",
   "arms race"). Do NOT use jargon or your hypothesis as the query — the map
   scores literal symptom-phrase matches.
2. [det] `python3 studio.py map "<symptom text>"` — output ranks the top 3
   archetypes with hit lists and a confidence of `likely` (rank 1, ≥2 hits)
   or `possible`. Paste the command and its matched-symptom list into the
   artifact as evidence.
3. [agent] If the map returns "No archetype symptom matches": widen the
   description with symptom vocabulary from `archetypes.json` symptom arrays
   (loop, delay, stock, constraint words). Two failed widenings = the
   situation may be multi-archetype or not archetypal — say so and diagnose
   from the frame's loops directly.
4. [det] `python3 studio.py archetype <top-id>` — pull the full record:
   story, diagnosis, intervention, counterintuitive.
5. [agent] Build the prediction table: for the suspect archetype, list each
   stock it predicts (growth stock accelerating, performance stock
   plateauing, constraint tightening; or atrophying capability; or drifting
   goal variable…) with its predicted motion.
6. [agent] Verify each predicted stock against observations from
   brief/frame ONLY. Mark each row **Moving**, **Moving as predicted**, or
   **Unknown — must measure**. An invented "moving" is the cardinal error of
   this phase.
7. [agent] Falsification branch: if a predicted stock is observably NOT
   moving (or moving the wrong way), demote the suspect, re-run `map` with
   different symptom emphasis, and promote the next candidate. Record the
   demotion and its reason — a rejected archetype is load-bearing evidence.
8. [agent] List secondary suspects from the map's ranks 2-3 explicitly as
   "not the diagnosis", each with the observation that would promote it
   (e.g. Growth and Underinvestment promotes only if a backlog exists).
9. [agent] Name which candidate constraint stock is binding INSIDE the
   boundary, and the discriminating instrumentation: "if X is high → B2;
   if Y falls while Z holds → B1/B3; if distribution collapsed → outside".
   Do not pick one from vanity metrics.
10. [agent] Quote the archetype's `counterintuitive` sentence VERBATIM from
    `archetypes.json`, then rule: **Accept** or **Reject**, with the
    operational consequence of accepting (what we stop doing, what we start).
11. [agent] Restate the intervention direction implied by the archetype's
    `intervention` field, tagged with the leverage ranks it implies
    (phase 04 details the walk). Include the sunset clause discipline when a
    symptomatic fix is unavoidable.
12. [agent] Write the diagnosis falsifier: the observation + deadline that
    kills THIS diagnosis (inherited from frame §9; sharpen it to the
    constraint-side change, not a volume/parameter change).
13. [det] Write `outputs/diagnosis.md` with exactly: `## Suspect`
    (archetype + confidence + matched symptoms), `## Evidence` (prediction
    table + verifications + what cannot be verified yet), `## Counterintuitive
    point` (quote + accept/reject + consequence).
14. [agent] Self-audit: does any Evidence row assert motion for a stock with
    no given fact behind it? Demote to Unknown. Does the quoted sentence
    match `archetypes.json` byte-for-byte (check 3 below)?
15. [det] Pre-GREEN deep-check run: execute checks 1-6 below against
    `outputs/diagnosis.md` — especially the quote guard (3); a paraphrased
    counterintuitive sentence is fixed before GREEN, not after.
16. [agent] Boundary cross-check: confirm the leading constraint candidate
    sits INSIDE the frame's boundary. An outside constraint (platform
    ranking, macro demand) flips the intervention class from "change our
    structure" to "adapt topic/ICP and stop pushing" — state which case
    holds, and inherit the frame's boundary rationale as the proof.

## Deterministic checks

The harness ships none for this phase — these are the deep gate:

1. `grep -qi '^## Suspect' diagnosis.md` and `grep -qi '^## Evidence'
   diagnosis.md` and `grep -qi '^## Counterintuitive' diagnosis.md`.
2. Named-suspect guard — the suspect line names one of the 10 canonical
   archetypes verbatim:
   ```bash
   python3 - <<'PY'
   import json
   names=[a['name'] for a in json.load(open('/inputs/archetypes.json'))['archetypes']]
   d=open('diagnosis.md').read()
   hit=[n for n in names if n.lower() in d.lower()]
   print('SUSPECT GUARD:','PASS' if hit else 'FAIL no canonical archetype named')
   PY
   ```
3. Quote guard — the quoted counterintuitive sentence exists verbatim in the
   named archetype's record (catches paraphrase-drift, which quietly reverses
   meaning):
   ```bash
   python3 - <<'PY'
   import json,re
   arts={a['name']:a for a in json.load(open('/inputs/archetypes.json'))['archetypes']}
   d=open('diagnosis.md').read()
   q=re.findall(r'[“"]([^“”"]+)[”"]',d.split('## Counterintuitive')[1])
   named=[n for n in arts if n.lower() in d.lower()]
   ok=any(x in arts[n]['counterintuitive'] for n in named for x in q if n)
   print('QUOTE GUARD:','PASS' if ok else 'FAIL quote not verbatim in archetypes.json')
   PY
   ```
4. Motion honesty — the Evidence table contains at least one `Unknown` or
   "must measure" marker unless every predicted stock has a given-fact
   citation: `grep -ci 'unknown' diagnosis.md` ≥ 1 (with brief-only facts,
   Unknowns are the default, and their absence is the smell).
5. Discriminator present — the artifact names an if/then instrumentation
   split (`grep -Ei 'if .* (high|falls|hold|collapse).*(→|->)|high →|→ B[0-9]'`).
6. Confidence discipline — `likely` only when the map shows ≥2 matched
   symptoms; otherwise `possible` (manual check against the pasted map output).

## Failure modes

1. **Story theft** — the archetype's narrative is adopted because it is
   compelling, with no predicted stock verified. Countermeasure: prediction
   table is mandatory (steps 5-6); every row cites brief/frame or says Unknown.
2. **Stock invention** — "attention is clearly exhausted" asserted to make
   the constraint row say Moving. Countermeasure: check 4 + the rule that
   only `problem.txt`/requester facts count; directionally-consistent ≠ moving.
3. **Single-archetype monogamy** — secondary suspects dropped, so the
   instrumentation can't discriminate. Countermeasure: secondaries listed
   with promotion conditions (step 8); the if/then discriminator (check 5).
4. **Counterintuitive nod-through** — the quote is accepted in one line and
   contradicted by the proposed intervention two lines later. Countermeasure:
   acceptance must state the operational consequence (what we STOP doing);
   phase 04 cross-checks that the chosen rank honors it.
5. **Paraphrase drift** — the "quote" is a paraphrase that reverses the
   original's meaning ("ease off" → "push smarter"). Countermeasure: quote
   guard (check 3) enforces verbatim.
6. **Map gaming** — symptom text engineered (loaded with one archetype's
   phrases) to force the preferred diagnosis. Countermeasure: symptom text
   must be drawn from brief/frame language; paste the exact query used.
7. **Premature precision** — picking B1-vs-B2-vs-B3 from vanity metrics
   because "Unknown" feels unfinished. Countermeasure: the diagnosis names
   the CLASS of constraint and the discriminator, never the instance without
   measurement.
8. **Unfalsifiable diagnosis** — no kill condition, so the label can never
   lose. Countermeasure: falsifier with a dated, constraint-side observation
   (step 12) — phase 08 greps for it downstream.

## Worked example

From `~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/diagnosis.md`:

- Suspect with confidence and matched symptoms (`diagnosis.md` §Suspect):
  > "**Limits to Growth** — confidence **likely**.
  > Matched symptoms (studio map on the stall language): growth stalled,
  > plateau, ceiling, capacity, diminishing returns."
- The prediction table with honest verifications (`diagnosis.md` §Evidence):
  > "| Constraining stock (the limiter that strengthens as you grow) |
  > tightening | **Directionally consistent; which stock is Unknown.**
  > Candidates inside the boundary: audience attention (commons),
  > relevance/trust of voice, unanswered inbound backlog, reply-capacity
  > slack. None of these have measured levels. Do not invent funnel numbers. |"
- The discriminator (`diagnosis.md` §Evidence):
  > "If unanswered-thread age and reply lag are high → limiter is **B2 reply
  > capacity** … If impressions hold but replies-per-post / ICP conversations
  > fall → limiter is **B1 attention commons** and/or **B3 relevance**."
- Verbatim quote + explicit acceptance (`diagnosis.md` §Counterintuitive):
  > "Quote: **'Pushing the growth loop harder tightens the constraint faster.
  > Ease off, remove the limiter, then resume.'**
  > **Accept.** Another volume push would strengthen the balancer … and hide
  > the limiter longer."

## Depth extensions

- **Archetype pair analysis**: run the full verification for the top TWO
   suspects and write the discriminating observation for each; mixed
   structures (Limits to Growth riding a Tragedy of the Commons) are the norm
   in GTM systems, not the exception.
- **Counterfactual stock history**: reconstruct the trend of the performance
   stock BEFORE the intervention tripped (here: yield before the 3×) — the
   inflection date is evidence for which delay row in frame §6 is binding.
- **Archetype intervention diff**: compare the suspect's `intervention`
   field with what the org has actually been doing; the delta is the phase-04
   agenda, pre-ranked by the ranks it implies.
- **Sensitivity probe**: for each Unknown stock, ask "which diagnosis would
   flip if this measured high vs low?" — Unknowns that flip nothing are
   dropped from instrumentation; the rest become the measurement plan.
- **Pre-mortem on the label**: assume the diagnosis is wrong in N weeks —
   write the most likely wrong-reason (wrong constraint, wrong boundary,
   reporting artifact) and add it to the falsifier as a second kill condition.
- **Map audit**: run `studio map` on 3 paraphrases of the symptom; if the
   top suspect changes across paraphrases, confidence drops one notch — the
   label is vocabulary-sensitive and must be verified harder.

## Handoff

Phase 04 LEVERAGE receives `/inputs/diagnosis.md`:
- the verified archetype + intervention direction (its implied ranks seed
  the leverage walk);
- the accepted counterintuitive point (a constraint on which interventions
  are admissible — rank 12 pushes are usually the exact violation);
- the constraint-class + discriminator (the instrument window the chosen
  intervention must fund, not block);
- secondaries with promotion conditions (rank choice must not foreclose them);
- the diagnosis falsifier (phase 07's DELIVERABLE inherits it verbatim).
