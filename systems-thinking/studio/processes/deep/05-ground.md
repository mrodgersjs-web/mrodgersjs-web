# Deep Process 05 — GROUND → `grounding.md`

> Deepens `processes/phases.md` §05. Harness gate: `run_phase 05 GROUND
> grounding.md` greps `Citations` and `## Gaps` (case-insensitive). Corpus
> layers: `data/card-index.json` (853-card index via `studio cards`/`studio
> card`), live Recall search (`studio search` — needs `RECALL_API_KEY`),
> distilled `knowledge/{youtube,papers}/manifest.md`, and arXiv/S2 when
> relevant. Extension slots (Parallel AI, Consensus MCP) fail soft.

## Purpose

GROUND puts the analysis in contact with prior art and measured reality, and
— just as important — writes down where it could not. Two products: citations
that support or CHALLENGE the frame/diagnosis/leverage chain, and a `## Gaps`
section that treats absent evidence as a finding. The phase enforces the
studio's zero-invention doctrine: after grounding, synthesis may organize
what exists, never invent what's missing. A degraded corpus (no card-index,
no API key) is recorded honestly and shipped as such — the run prefers honest
failure over silently unreasoned output.

## Entry criteria

- Phases 01-04 GREEN: `brief.md`, `frame.md`, `diagnosis.md`, `leverage.md`
  exist in `$RUN` (mounted as `/inputs/`).
- `studio.py` in the working directory.
- Corpus state known or about to be known via `studio doctor` (a FAIL on
  card-index/key does NOT block this phase — it constrains it).

## Inputs

| Input | Where | Use |
|---|---|---|
| Prior artifacts | `/inputs/{brief,frame,diagnosis,leverage}.md` | the claims to ground |
| `studio doctor` | CLI | corpus availability: which layers are live |
| `studio cards [tag] [--grep X]` | CLI + `data/card-index.json` | local tagged corpus (122 systems-thinking cards when the index snapshot is present) |
| `studio card "<query>"` | CLI | detail on one card |
| `studio search "<q>" [focused\|exhaustive]` | CLI → Recall API | live semantic search, 853-card KB (needs `RECALL_API_KEY`) |
| `knowledge/youtube/manifest.md`, `knowledge/papers/manifest.md` | `/inputs/manifest.md` | distilled source cards from the scrape pipeline |
| `references/recall-pack.md` | package | curated pack (`studio pack` prints the head) |
| arXiv / Semantic Scholar | web | when the problem is literature-bearing |
| Extension slots: `PARALLEL_API_KEY`, Consensus MCP | env/MCP | web-scale + academic search; fail soft to the layers above |

## Procedure

1. [det] `python3 studio.py doctor` — record every PASS/FAIL/WARN line
   verbatim in the artifact's method note. This is the corpus's bill of
   health and the justification for whatever could not be cited.
2. [det] Extract the claim inventory from prior artifacts: the archetype
   label + confidence, each loop's existence claim, each predicted-stock
   motion, the chosen/rejected leverage ranks, the counterintuitive
   acceptance. These are WHAT gets grounded.
3. [det] `python3 studio.py cards systems-thinking` — if the index is
   present, list matching cards; refine with
   `python3 studio.py cards systems-thinking --grep "<domain word>"`.
   If absent: record `no card-index.json snapshot` verbatim (exit 1) — that
   sentence belongs in the artifact, not in your memory.
4. [det] `python3 studio.py search "<archetype + domain terms>" exhaustive`
   (and 2-3 variant queries: constraint language, mechanism language). With
   no key, record `no RECALL_API_KEY` per query. Never fabricate cards the
   API did not return.
5. [det] Read the knowledge manifests mounted at `/inputs/manifest.md`
   (YouTube + papers) and pull the cards relevant to the claim inventory.
6. [agent] Web layer when literature-bearing: arXiv/S2 queries for the
   mechanism (e.g. attention economics, content-marketing decay curves,
   response-time conversion effects). Cite paper ids/URLs.
7. [agent] Classify each citation: SUPPORTS / CHALLENGES / CONTEXT for a
   specific named claim. A grounding with only SUPPORTS citations is a red
   flag — the corpus almost always contains a counter-case worth honoring.
8. [agent] Ground the chosen leverage rank's MECHANISM specifically (e.g.
   evidence that information-flow interventions change producer behavior;
   that goal restatements re-orient loops), not just the archetype's story.
9. [agent] Ground the discriminator: any evidence bearing on which candidate
   constraint typically binds in systems shaped like this one (industry
   norms, benchmark posts, prior studio packs via `studio pack`).
10. [agent] Ground the falsifier: is the N-week window consistent with the
    delays cited anywhere in the corpus? If corpus says the effect lags
    longer, say so — better to widen the falsifier than to guarantee a
    false kill.
11. [agent] `## Citations`: every entry as `[Card: title](url)` for corpus
    cards, `paper-id`/URL for literature, or local paths (`archetypes.json#…`,
    `/inputs/frame.md`) for prior-phase artifacts. Include the doctor output
    and the exact CLI calls with their results (including failures).
12. [agent] `## Gaps`: what the corpus does NOT cover — unmeasured stocks
    (inherit frame's instrument map), absent domains, dead extension slots,
    missing time series. Absent evidence is a finding: write what claim is
    therefore UNVERIFIED, and what measurement would close it.
13. [agent] Upgrade/downgrade: based on evidence, adjust the diagnosis's
    confidence wording IF the corpus moves it (e.g. a strong counter-case
    demotes `likely` → `possible`) — and say so explicitly; grounding may
    not silently rewrite the diagnosis, only annotate it.
14. [det] Write `outputs/grounding.md`: method note (doctor + commands run),
    `## What is grounded` (claims × citations × supports/challenges),
    `## Citations`, `## Gaps`.
15. [agent] Self-audit: every citation resolves (check 3 below); no
    invented sources; gaps name their unverified claim; the artifact never
    states as fact what a Gap says is unmeasured.

## Deterministic checks

Mirror of the harness gate:

1. `grep -qi 'citations' grounding.md` and `grep -qi '^## gaps' grounding.md`.

Deeper gates:

2. Corpus honesty — the artifact records the doctor verdict and per-layer
   results: `grep -ci 'doctor' grounding.md` ≥ 1; if any layer failed, its
   failure string appears (`no RECALL_API_KEY` / `no card-index.json`).
3. Citation resolution — every `[Card: title](url)` title exists in the
   card index when the index is present:
   ```bash
   python3 - <<'PY'
   import re,os
   g=open('grounding.md').read()
   cards=re.findall(r'\[Card: ([^\]]+)\]\(([^)]+)\)',g)
   if not cards: print('RESOLVE GUARD: PASS (no [Card:] citations claimed)')
   else:
       raw=open('/Users/rig128gb/Developer/rig-intelligence/packages/'
                'systems-thinking-studio/data/card-index.json').read().lower()
       bad=[t for t,u in cards if t.lower() not in raw]
       print('RESOLVE GUARD:','PASS' if not bad else 'FAIL '+str(bad))
   PY
   ```
   (no index on disk ⇒ claiming `[Card:]` citations is itself the failure).
4. Gap depth — `## Gaps` contains ≥3 bullet lines AND at least one
   `Unknown`/`unmeasured`/`not cover` marker: `grep -A20 '^## Gaps'
   grounding.md | grep -c '^- \|^\* '`.
5. Claim coverage — the artifact names the diagnosis's archetype and the
   chosen rank (grep both); grounding that never re-touches the load-bearing
   claims is decoration.
6. No silent rewrite — diagnosis.md and leverage.md unchanged by this phase
   (`git`/`diff` style compare if run under version control; in the harness,
   prior artifacts are read-only `/inputs`).

## Failure modes

1. **Citation decoration** — sources piled on the general topic, none mapped
   to a named claim; the analysis is untouched by anything cited.
   Countermeasure: claim inventory (step 2) + per-citation
   SUPPORTS/CHALLENGES tag (step 7).
2. **Confirmation corpus** — only supporting evidence collected; the
   counter-case is never searched. Countermeasure: require ≥1 CHALLENGES-or-
   CONTEXT citation or an explicit note that none exists in the corpus.
3. **Ghost cards** — plausible `[Card: …]` citations invented when the index
   or key is down. Countermeasure: resolution guard (check 3) + verbatim
   failure strings from the CLI (check 2).
4. **Gap laundering** — `## Gaps` lists generic limitations ("more research
   needed") instead of named unverified claims. Countermeasure: each gap
   names the claim it leaves unverified and the measurement that closes it.
5. **Silent diagnosis rewrite** — grounding quietly changes the story so
   artifacts disagree downstream. Countermeasure: upgrades/downgrades are
   annotations with receipts (step 13); phase 07 synthesizes from the
   annotated, not the edited, chain.
6. **Degraded-run amnesia** — corpus down, artifact written as if grounded.
   Countermeasure: doctor output embedded; DEGRADED language mandatory when
   layers are down ("archetypes + leverage points only").
7. **Falsifier starvation** — corpus says the effect lags 8 weeks; the
   falsifier still kills at 4. Countermeasure: step 10 lag-check against
   cited delays; widen the window or note the risk.
8. **Search-query monoculture** — one query, one phrasing, zero recall.
   Countermeasure: ≥3 variant queries (archetype language, constraint
   language, mechanism language); record each.

## Worked example

From `~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/grounding.md`
(a degraded-corpus run, handled honestly):

- Method recorded with failures verbatim (`grounding.md` §Citations):
  > "doctor: PASS `data/archetypes.json`, PASS `data/leverage-points.json`;
  > FAIL `data/card-index.json`; WARN no `references/recall-pack.md`; WARN
  > no `RECALL_API_KEY`; mirror-backed cards = 0."
  > "`cards systems-thinking` → `no card-index.json snapshot; see package
  > README` (exit 1)."
- Local citations with anchors instead of ghost cards (`grounding.md`):
  > "[Limits to Growth](archetypes.json#limits-to-growth) — story, symptoms,
  > diagnosis, intervention, counterintuitive."
  > "[Meadows 12 leverage points](https://donellameadows.org/archives/
  > leverage-points-places-to-intervene-in-a-system/) — ranks 12→1"
- Gaps as findings, each naming what stays unverified (`grounding.md` §Gaps):
  > "Measured levels of the constraining stocks: attention per post, replies
  > per post, unanswered-thread age, reply-capacity hours, lead-definition
  > history, impression trend vs 3× volume."
  > "Which balancer is binding (B1 vs B2 vs B3 vs ranking-outside). Diagnosis
  > names the *class* of constraint, not the stock."
- And the honesty rule that closes the phase:
  > "Until those stocks are instrumented, do not treat 'attention is
  > exhausted' or 'nobody is replying because we're slow' as confirmed."

## Depth extensions

- **Claim-evidence matrix**: full table claim × source × verdict
   (supports/challenges/unverified) — the unverified column becomes the
   measurement backlog handed to phase 07's instrument window.
- **Prior-run mining**: search `$RUNS/` for earlier runs on the same system
   or archetype; a repeat diagnosis with a failed falsifier is the strongest
   challenge evidence the studio can produce.
- **Quantitative grounding**: when the corpus carries numbers (conversion
   decay rates, response-time effects), attach them to the frame's flow
   `Unknown`s as priors, marked as priors — never as observations.
- **Counter-case hunt**: dedicate one search variant purely to disconfirming
   the diagnosis ("volume DID work when…", "plateau reversed by…"); record
   what the found counter-cases had that this system lacks.
- **Extension-slot activation**: with `PARALLEL_API_KEY` (web-scale) or
   Consensus MCP (academic), run the same claim inventory through them and
   diff the citation sets — coverage deltas go straight into `## Gaps`.
- **Source-quality tiering**: tag each citation local-canonical
   (archetypes/leverage JSON) / distilled (knowledge manifests) / live
   (Recall) / primary (paper) — synthesis weights them in that order when
   they conflict.

## Handoff

Phase 06 POLYMATH receives `/inputs/grounding.md` (plus frame/diagnosis):
- the verified claim set (only these may be built on) and the unverified
  column (imports must not presuppose them);
- the gap list — each gap is a slot where a cross-domain mechanism might
  supply an instrument or an intervention the corpus could not;
- corpus tiering, so imported mechanisms are grounded to the same standard
  before phase 07 will carry them;
- annotated confidence changes (any `likely`→`possible` demotions).
