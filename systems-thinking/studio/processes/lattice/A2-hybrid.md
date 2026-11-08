# Lattice Mode A2 — HYBRID (deterministic core + bounded LLM calls)

> Build-mode contract for band B2 work. Canonical definition:
> `RIG_A1_A4_ARCHETYPES.md` §"A2 Hybrid"; escalation rule
> `RIG_DOCTRINE.md` §4: "A2 confidence collapse -> A3". In the studio, A2 is
> the workhorse for phases that DRAFT against a template and are CHECKED by
> grep: intake briefs, frames, diagnoses, leverage choices, grounding.

## Purpose

A2 does the one thing A1 cannot — generate natural-language structure
(restate, fill, classify, transform) — while Python owns everything that
matters: the prompt template, the call, the validation, the persistence,
and the fallback. The model never sees a free-form output path: every call
carries a forced schema, every output is validated before it is written,
and every failure degrades to a deterministic fallback that the run can
ship honestly. A2's discipline is boundedness — one judgment (or a small
chained set), fixed templates, capped tokens, diffable outputs.

## Entry criteria

- Router emitted `mode: a2` — typically `shape_floor: a2` sitting above a
  B1/B2 gate floor (drafting/transformation where Python can validate the
  output) — OR A1 returned a single schema-shaped `UNKNOWN` and routed here
  as the cheaper alternative to A3.1, OR A3/A4 de-escalated a stabilized
  procedure into A2.
- An output contract exists BEFORE the call: target file, required
  sections/keys, value types, and the validator that will judge it.
- A deterministic fallback exists and is named (what ships if the call
  fails or the validation rejects twice).
- Proxy reachable (`curl 127.0.0.1:8317/v1/models`) or the run degrades
  per `models.md` — CLI outputs plus a "needs-agent-reasoning" marker,
  honest failure, never silent.

## Allowed / forbidden (canonical)

Allowed: LLM callouts only behind typed schemas; forced JSON; strict
Pydantic-style validation; deterministic fallback to A1; capped token
budget; fixed prompt templates; output diffing.

Forbidden: free-form model outputs; unvalidated persistence; silent
fallback; LLM-modified contracts; model-only decisions without
deterministic guardrails.

Note on temperature: the canonical A2 contract says `temperature=0`. This
studio's local proxy REJECTS any temperature other than 1 — omit the
parameter entirely and compensate with forced structure + validation +
output diffing (the deterministic wrapper, not the sampler, is the
reliability mechanism here). Record the omission in the run log.

## Inputs

| Input | Where | Use |
|---|---|---|
| routing record | `band.json` | band B2 gates: schema validation + diffing + token cap |
| A1 prelude outputs | deterministic layer | given facts: brief, frame, map results, corpus cards |
| fixed prompt template | versioned in the run dir | the ONLY prompt surface; ad-hoc prompting is forbidden |
| model routing | `models.md` | default `grok-4.6`; haiku for cheap summarize; never a paid cloud unless named |
| validator | stdlib python | json schema / required sections / value checks |

## Procedure

1. [det] Re-verify band + gates from the routing record; confirm the A1
   prelude ran (inputs present, `studio doctor` recorded). Never skip A1.
2. [agent] Draft the output contract: sections/keys, types, length caps,
   required `Unknown` markers where facts are absent. This is agent work;
   the CONTRACT is then frozen — the model may not modify it mid-call.
3. [det] Materialize the fixed prompt template: task + inputs + contract +
   "return ONLY the schema". Hash the template into the log.
4. [det] Call the model with a capped token budget (default ≤ 4096 out),
   forced JSON where the artifact is structured. No temperature field
   (proxy contract). Log endpoint, model, latency, token counts.
5. [det] Validate: parse, check every required key/section, type-check,
   length caps, citation format where the contract demands `[Card: ...]`.
   Validation failure → structured error, attempt 2 with the validation
   errors appended to the prompt. Two consecutive failures = **A2
   confidence collapse → escalate to A3** (canonical), carrying the failed
   attempts as A3's starting evidence.
6. [agent] Post-validate semantics the schema can't see: invented numbers
   (numbers guard, cf. deep 01 check 5), quote drift (cf. deep 03 check
   3), solution smuggling. Mark or delete violations; re-run step 5 once.
7. [det] Output diffing: diff against the template scaffold and against
   any prior version of the artifact. The diff is the review surface.
8. [det] Persist the VALIDATED object only. Unvalidated persistence is
   forbidden — write happens after validation passes, atomically.
9. [det] Escalation watch (concrete thresholds from `bms-bands.json`):
   - decomposition count > 3 (the task chains more than three sub-judgments
     → multi-step workflow → A3)
   - evidence_density drops below 0.40 mid-flight (grounding eroded)
   - schema validation failed twice (step 5)
   Each trigger appends a new routing record — never edits the old one.
10. [det] Fallback path: if the proxy is down or collapse escalates and A3
    is unavailable, ship the A1 fallback artifact with the
    "needs-agent-reasoning" marker and log DEGRADED. The run fails honestly
    rather than shipping unreasoned output as reasoned.
11. [det] ProofPacket row: template hash, call log, validation verdict,
    final artifact hash.

## Deterministic checks

1. Schema check — validator exit 0 on the final artifact; the validator
   itself is stdlib and versioned (changing it = explicit version bump).
2. Diff presence — `git`-less diff: the run dir contains
   `<artifact>.diff` against scaffold/prior; empty diff on a drafting task
   means the model returned the template — reject.
3. Budget check — logged output tokens ≤ cap; call count ≤ 2 per judgment.
4. Template immutability — prompt template hash in the log matches the
   versioned file; an in-call template edit = contract violation = RED.
5. Fallback honesty — every DEGRADED/fallback line appears in verify.log;
   `grep -c 'needs-agent-reasoning'` matches the count of failed judgments.
6. No-freeform check — the persisted artifact parses against the contract
   (JSON) or matches its required sections (markdown grep), i.e. nothing
   was written that the schema did not describe.

## Failure modes

1. **Freeform leak** — model returns beautiful prose, code writes it to the
   artifact because it "looks right". Countermeasure: persistence is
   post-validation only (step 8); check 6.
2. **Prompt drift** — the "fixed" template grows ad-hoc clauses per retry
   until it is a new prompt every call. Countermeasure: template hash
   (check 4); retries append VALIDATION ERRORS, not new instructions.
3. **Validation theater** — validator checks key presence, model fills
   keys with lorem. Countermeasure: length caps + semantic guards (step 6)
   + the downstream deep-phase checks (numbers guard, quote guard).
4. **Silent fallback** — call fails, except-path writes the scaffold filled
   with `Unknown`, run continues as if reasoned. Countermeasure: fallbacks
   are loud (DEGRADED + marker + verify.log line).
5. **Chain creep** — "just one more call" turns a single judgment into an
   unplanned agent. Countermeasure: decomposition counter in the routing
   record; >3 = re-route to A3 with the chain as its plan.
6. **Sampler complacency** — trusting the proxy's forced temperature=1
   because validation passed twice. Countermeasure: output diffing across
   re-runs (check 2) is the drift detector; divergence across identical
   inputs = treat as collapse, escalate.
7. **Evidence erosion unnoticed** — grounding thins mid-task (a corpus
   mount fails) and the model happily continues. Countermeasure:
   evidence_density re-estimate at each escalation watch (step 9).

## Studio mapping (default band A2)

| Studio phase | A2 shape |
|---|---|
| 01 INTAKE | agent drafts brief sections; A1 grep gates (`## Problem`, `## Success looks like`) validate |
| 02 FRAME | agent fills the numbered scaffold; A1 checks Stocks/Reinforcing/Balancing/Delay |
| 03 DIAGNOSE | `studio map` seed is A1; prediction-table reasoning + counterintuitive accept/reject is a bounded judgment; quote guard validates |
| 04 LEVERAGE | `studio leverage` is A1; rank choice + one-rank-higher rejection is the bounded judgment |
| 05 GROUND | `studio cards`/`cards index` A1; `studio search` is the fixed-connector boundary case (external REST behind a key, deterministic wrapper, graceful absence) — A2 by capability, A1 when key absent |
| 06 POLYMATH | the transfer-validity SCORING pass may run as A2 behind the numeric contract (≥0.60 rule); the full 7-step protocol is A3 |

Deep-agent loop steps owned by A2: each single frontier call that produces
one artifact section set and is immediately grep-gated — bounded by the
harness's own turn cap (--max-turns 16) and retry budget (≤2).

## Handoff

- To A1: the validated artifact becomes a given fact (hash-cited).
- To A3 (on collapse): the failed call log, validation errors, the frozen
  contract, and the exact ambiguity — A3 starts from the wreckage, not
  from zero.
- To phase 07 SYNTHESIZE: A2 artifacts carry their validation verdicts so
  synthesis inherits epistemic status, not just text.
