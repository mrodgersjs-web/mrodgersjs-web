# Deep Process 06 — POLYMATH → `polymath.md`

> Deepens the 8-phase chain at its newest joint (the shipped 7-phase harness
> predates it; wiring is `run_phase 06 POLYMATH polymath.md` with the checks
> below, SYNTHESIZE/VERIFY shifting to 07/08, and `polymath.md` joining the
> harness's prior-artifact list). Data: `data/polymath-domains.json` — 11
> domains × mechanisms as `name -> source-structure` pairs, plus the canonical
> protocol and output contract. Doctrine: RIG-COLLIDER — import mechanisms
> from unrelated domains; validity bar SIS-style transfer score ≥ 0.60
> (product of three 0-1 factors); 3+ domains; measurable-change-or-reject.
> A mechanism is only "imported" when the TARGET system's structure is named,
> not just the source metaphor.

## Purpose

POLYMATH breaks the in-field echo chamber. After grounding says what the
corpus knows, this phase asks what a physicist, an ecologist, or a control
engineer would recognize in the frame's structure — a loop shape, a delay
signature, a stock topology — and what intervention their discipline's
mechanism implies HERE. Cross-domain reasoning is where the studio earns
novelty, and also where it is most liable to self-deceive: metaphors feel
profound and transfer nothing. The transfer-validity score exists to force
the difference visible: an import must name a measurable change in the
target system or it is rejected as metaphor-only, however beautiful.

## Entry criteria

- Phases 01-05 GREEN: brief, frame, diagnosis, leverage, grounding exist
  (mounted as `/inputs/`).
- The frame has at least one named constraint/loop to import INTO (a frame
  without named structure has nothing to match mechanisms against).
- `studio.py` in the working directory; `data/polymath-domains.json` mounted.

## Inputs

| Input | Where | Use |
|---|---|---|
| `frame.md` | `/inputs/frame.md` | target structure: stocks, loops (R/B), delays, constraint |
| `diagnosis.md` | `/inputs/diagnosis.md` | constraint class + discriminator to sharpen imports |
| `grounding.md` | `/inputs/grounding.md` | verified claims (imports build only on these); gaps (import slots) |
| `studio crosspoll "<structure text>"` | CLI | deterministic seed: mechanisms whose name/source tokens overlap the text + the full protocol printout |
| `data/polymath-domains.json` | `/inputs/polymath-domains.json` | 11 domains: physics, biology, economics, mathematics, engineering, psychology, strategy-military, learning-meta, complexity, philosophy |

## Procedure

1. [agent] `## Target structure`: state the import target from frame.md in
   mechanism language — the stock under pressure, the loop type (R/B) and
   its gain, the delay, the constraint. Quote the frame's own lines. This
   section is the anchor; every later row must name THESE structures.
2. [det] Seed the candidates: `python3 studio.py crosspoll "<structure in
   loop/delay/stock/constraint words>"`. Feed it structure words ("shared
   depletable stock consumed by reinforcing loop, delay between volume and
   trust decay, capacity constraint"), NOT topic words — the matcher scores
   mechanism-name/source token overlap, and topic language returns nothing.
3. [det] If crosspoll returns "No mechanism matches": re-run with the
   constraint's shape ("compounding loop hitting limiter", "backlog grows
   faster than service rate"). Then ALSO walk `polymath-domains.json`
   manually — the seed is a starter, not a ceiling.
4. [agent] Pick ≥3 domains NOT native to the problem's field (a GTM problem
   may use physics/biology/mathematics/engineering/complexity freely;
   economics/psychology are adjacent — allowed, but mark the adjacency).
   Fewer than 3 domains = the phase has not escaped the field.
5. [agent] For each domain, list mechanisms whose SOURCE structure shares
   the target's shape: same loop type, comparable delay, same stock topology
   (shared pool, queue, network, compounding asset). Match shape, not topic.
6. [agent] Write each import in the canonical form: "in <target system>,
   <mechanism> implies <concrete intervention>". The sentence must contain a
   verb that changes something in the target — measure, cap, split, buffer,
   route, damp. If you cannot finish the sentence with an intervention, the
   mechanism is not an import yet.
7. [agent] Score transfer validity, three factors each 0-1:
   - structural-similarity: does the source structure really share the
     target's loop/delay/stock shape (not just vocabulary)?
   - mechanism-clarity: is the source mechanism's causal machinery explicit
     enough to re-implement (gains, thresholds, state)?
   - testability: can the target change be observed within the brief's
     window with instruments the requester has?
   Product ≥ 0.60 keeps the candidate; below = rejected. Record all three
   factors AND the product in the table — a bare "0.8" is unauditable.
8. [agent] Keep the top 3 imports. EACH must name a measurable change: the
   metric, its unit, and what motion counts as the mechanism firing. "Watch
   it closely" is not a change; "report yield of the marginal post" is.
9. [agent] `## Rejected (metaphor-only)`: every seductive candidate that
   failed the bar, with the specific failure (structure not shared /
   machinery vague / untestable in window). Rejections are the phase's
   integrity — they prove the bar did work.
10. [agent] Cross-check imports against grounding: an import may not
    presuppose a claim grounding listed as unverified; it MAY supply an
    instrument for a gap (say which gap it closes).
11. [agent] Cross-check against leverage: does any import strengthen the
    chosen rank, or smuggle in a rejected-higher move? Tag each top import
    with the leverage rank it operationalizes (usually 6/8/11-flavored).
12. [agent] Honesty pass: strike any row whose "target implication" names
    the SOURCE system's actors instead of the target's (the classic
    metaphor-slip: "the algorithm evolves" is fine, "be a red queen" is not).
13. [det] Write `outputs/polymath.md` per the canonical output contract:
    `## Target structure`, `## Candidate imports` (table: domain, mechanism,
    source structure, target implication, transfer score with all three
    factors), `## Top imports` (≤3, each with metric + unit + firing
    condition), `## Rejected (metaphor-only)` (candidates + failure reason).
14. [det] Pre-GREEN deep-check run: execute checks 1-6 below against
    `outputs/polymath.md` — domain guard (≥3 canonical domains), score
    floor (kept products ≥ 0.60 with all three factors shown),
    measurable-change markers in every top import.
15. [agent] Negative-space check: confirm at least one candidate from a
    domain OUTSIDE the final top set was scored and rejected — a top-3 that
    was never contested is usually pre-ordained, which is the failure this
    phase exists to prevent.
16. [agent] Brevity pass: the candidate table carries only rows actually
    scored; no appendix, no unscored "interesting mentions". A polymath.md
    over ~120 lines is a reading list, not an import protocol.

## Deterministic checks

These are the phase's gate (drop-in for `run_phase 06 POLYMATH polymath.md`):

1. Contract sections present: `grep -qi '^## Target structure' polymath.md`;
   `grep -qi '^## Candidate imports' polymath.md`;
   `grep -qi '^## Top imports' polymath.md`;
   `grep -qi '^## Rejected' polymath.md`.
2. Domain spread — ≥3 distinct canonical domains appear:
   ```bash
   python3 - <<'PY'
   import re
   t=open('polymath.md').read()
   doms=set(re.findall(r'\b(physics|biology|economics|mathematics|engineering|'
        r'psychology|strategy-military|learning-meta|complexity|philosophy)\b',t,re.I))
   print('DOMAIN GUARD:','PASS (%d domains: %s)'%(len(doms),sorted(doms))
         if len(doms)>=3 else 'FAIL <3 domains')
   PY
   ```
3. Score floor — every kept (non-REJECTED) scored row's product ≥ 0.60, and
   the three factors are shown:
   ```bash
   python3 - <<'PY'
   import re
   rows=[r for r in open('polymath.md').read().splitlines()
         if r.startswith('|') and re.search(r'0\.\d',r)]
   def prod(r):
       p=1.0
       for n in map(float,re.findall(r'0\.\d+',r)): p*=n
       return p
   bad=[r for r in rows if prod(r)<0.60 and 'eject' not in r]
   print('SCORE GUARD:','PASS' if not bad else 'FAIL under-0.60 kept: '+str(bad))
   PY
   ```
4. Measurable-change-or-reject — every `## Top imports` entry contains a
   metric marker (unit, number, or instrument verb + object):
   `grep -A30 '^## Top imports' polymath.md | grep -cE 'per |rate|hours|
   weeks|%|metric|measure|report'` ≥ 3.
5. Rejection substance — the rejected section names failure reasons, not
   just candidates: `grep -A10 '^## Rejected' polymath.md | grep -ciE
   'metaphor|vague|untestable|not share|structure'` ≥ 1.
6. Target anchoring — the target-structure section quotes or names the
   frame's own stocks/loops (`grep -qiE 'B[0-9]|R[0-9]|stock|loop'
   polymath.md` within `## Target structure` context).

## Failure modes

1. **Metaphor drift** — "our audience is an ecosystem" with no intervention;
   the artifact reads profound and changes nothing. Countermeasure: import
   sentence form (step 6) + measurable-change check (4) + metaphor-only
   rejection bin.
2. **Topic matching** — crosspoll fed topic words, returns nothing, agent
   free-associates instead. Countermeasure: step 2-3 structure-language
   rule; paste the crosspoll command + output into the artifact.
3. **Score theater** — all factors 0.9, product always ≥ 0.60, bar never
   rejects. Countermeasure: the rejected section MUST be non-empty on any
   real run (you considered more than 3 candidates); audit factors against
   the stated definitions, not vibes.
4. **Native-domain smuggling** — all three "domains" are the problem's own
   field wearing costumes; no escape happens. Countermeasure: domain guard
   (check 2) + the adjacency marking rule (step 4).
5. **Grounding bypass** — import presupposes an unverified claim ("since
   attention is exhausted…"). Countermeasure: step 10 cross-check; each top
   import cites which verified claim or which Gap-instrument it is.
6. **Leverage smuggling** — an import quietly re-litigates the rejected
   higher rank or re-tunes rank-12 parameters. Countermeasure: step 11 rank
   tag per import; reviewers check tags against leverage.md.
7. **Seed worship** — only crosspoll's 12 printed candidates considered;
   the richer mechanisms in the JSON never read. Countermeasure: manual walk
   of at least 3 domains beyond the seed (step 3).
8. **Import sprawl** — 8 top imports dilute into a reading list.
   Countermeasure: hard cap 3 top imports; the cut candidates go to
   Rejected with "scope" as the reason.

## Worked example

The E2E run predates POLYMATH (7-phase harness), so this example runs the
protocol against that run's real artifacts — target structure quoted from
`~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/frame.md`:

- Target structure (quoted `frame.md` §5/§2):
  > "B1 (goal: finite audience attention): more posts per unit attention →
  > skip/mute/fatigue → less attention per post → replies/leads flat."
  > "R3 (pathology): Volume praised → more templates/cadence → more posts
  > shipped → team rewarded → more volume."
  Constraint class from `diagnosis.md`: "B1/B2/B3 — which stock is Unknown."

- Kept import (complexity · preferential attachment — "early winners
  compound connectivity"): in the content engine, feed distribution is a
  preferential-attachment process on early engagement → implies measuring
  replies in the FIRST 90 minutes per post as the yield lead indicator and
  intervening there (boost/reply early or kill the post), not averaging
  lifetime yield. Factors 0.9 × 0.9 × 0.8 = **0.648 ≥ 0.60 → keep**. Closes
  a grounding gap (per-post attention unmeasured) with a cheap instrument.

- Kept import (economics · marginal vs average — "decisions live at the
  margin; dashboards report averages"): implies reporting the yield of the
  MARGINAL post (3rd of the day vs the 1st) instead of average per-post
  yield; if marginal yield ≤ 0, the cadence cut is arithmetic, not taste.
  Factors 0.9 × 0.9 × 0.9 = **0.729 → keep**. Operationalizes the chosen
  rank-6 information-flow intervention.

- Rejected under the bar (physics · critical slowing down — "recovery from
  perturbation slows before regime shift"): implies tracking reply-rate
  recovery time after outlier posts as an early-warning of an attention
  regime shift. Structure shares (balancing loop restoring slower), but
  testability inside the 2-week frozen-cadence window is weak — recovery
  events are rare, noise high. 0.8 × 0.9 × 0.6 = **0.432 < 0.60 → reject
  (untestable in window)**.

- Rejected as metaphor-only: "thermodynamic entropy → attention dissipates"
  — names no intervention, no metric, no firing condition. **REJECTED
  (metaphor-only)** despite being the first idea everyone reaches for.

Three domains (complexity, economics, physics), two imports surviving the
0.60 bar, both naming measurable changes in the target's own stocks.

## Depth extensions

- **Dual-mechanism triangulation**: require each top import to be supported
   by a SECOND domain with an isomorphic mechanism (preferential attachment
   × Red Queen; marginal-yield × stress-strength interference) — cross-domain
   agreement on the same shape is stronger evidence than any single analogy.
- **Counter-mechanism hunt**: deliberately import one mechanism that argues
   AGAINST the chosen intervention (e.g. desirability of buffers vs cost of
   lethargy) and score it with the same bar; surviving counter-mechanisms
   become conditions on the plan, not surprises later.
- **Mechanism→rank mapping table**: extend the candidate table with the
   leverage rank each import operationalizes; clusters reveal whether the
   polymath pass is genuinely multi-rank or just rank-6 cosplay.
- **Falsifiable import contracts**: for each top import, write the kill
   condition ("if first-90-min replies show no distribution skew within 2
   weeks, the preferential-attachment import is wrong for this feed") —
   imports are hypotheses, and phase 07 should inherit their kill conditions.
- **Domain deep-dive**: when one domain dominates the kept set, read its
   full mechanism list and generate 5+ candidates from it alone, then
   re-score — depth in one isomorphic field often beats breadth across ten.
- **SIS-style replication discipline**: re-score the top imports one day
   later without looking at the first scores; disagreement > 0.1 on any
   factor means the factor definitions are being applied by mood — tighten
   the rubric wording before phase 07 relies on it.

## Handoff

Phase 07 SYNTHESIZE receives `/inputs/polymath.md`:
- ≤3 top imports, each with metric + unit + firing condition + rank tag —
  these MAY appear in the deliverable as instruments/interventions, and
  only in this grounded form;
- the rejected list (synthesis must not resurrect metaphor-only imports);
- import kill conditions, folded into the deliverable's falsifier section;
- confirmation that every import built on verified claims only.
The harness's prior-artifact list for phases 07/08 must include
`polymath.md` alongside brief/frame/diagnosis/leverage/grounding.
