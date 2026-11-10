# Deep Agent Process — QUESTION → DECOMPOSE → GATHER → VERIFY → SYNTHESIZE → SEAL

> The studio's deep-research/deep-work loop: a bounded multi-pass investigation
> over one question that ships a sealed deliverable. Runner:
> `scripts/deep_agent/run.py` (stdlib-only Python, deterministic-first A1).
> Trace sidecar contract: `processes/deep-agent/trace-schema.md`
> (LangSmith-compatible JSONL, zero LangSmith dependency). Sealing reuses the
> studio's `proofpacket/seal.py` + `proofpacket/verify.py` unchanged. Where the
> 8-phase chain (`processes/deep/*.md`) answers "what is this system?", the
> deep agent answers "what is the verifiable answer to this question?" —
> same doctrine (deterministic data, LLM reasoning, verification always),
> different shape (multi-pass + adversarial votes instead of phase gates).

## Purpose

The deep agent turns one question into one sealed, evidence-bounded answer
using bounded compute. Four disciplines distinguish it from a chat:

1. **Bounded multi-pass** — the loop runs `--max-passes` (default 3) gather
   passes; pass N+1's queries are generated from pass N's gaps. Depth is a
   budget, not a mood: the run always terminates, always seals.
2. **Deterministic substrate** — every evidence byte comes from the `studio`
   CLI (archetypes, cards), the distilled `knowledge/` library, or the
   optional Recall web layer. The LLM reasons over deterministic pulls; it
   never fabricates the corpus it is quoting.
3. **Refute-default verification** — every extracted claim faces
   `--verify` (default 2) independent adversarial votes whose standing
   instruction is "the claim is WRONG; refute it if you can". Claims survive
   on zero refutations, die on majorities, and hang as UNVERIFIED otherwise.
   A claim nobody tried to kill is not evidence.
4. **Honest degradation** — proxy down, JSON mangled, search silent: each
   failure is recorded (`needs-agent-reasoning`, `UNVERIFIABLE`, empty
   findings with "silence is a finding") and sealed as-is. The run prefers
   honest failure over silently unreasoned output (models.md doctrine).

## Entry criteria

- A question that names something answerable (a mechanism, a comparison, a
  "which/why" with a checkable shape). A topic ("our GTM") is a red flag:
  restate until a question emerges, or route to the 8-phase chain instead.
- `python3 scripts/studio.py doctor` — corpus state known (FAILs constrain,
  they do not block).
- Local proxy reachable (`POST /v1/chat/completions`, key `KIMI_SUB_API_KEY`
  in `~/.hermes/.env` — never printed, never written into artifacts). If
  down, the run degrades per discipline 4; `--dry-run` needs no proxy at all.
- Write access to `~/.rig/systems-studio/runs/deep-agent/` (run dirs land
  there: `<ts>-<slug>/`).

## Inputs

| Input | Where | Use |
|---|---|---|
| `<question>` | argv[1] | the run's contract — the only source of given facts |
| `--dry-run` | flag | full plumbing, zero LLM calls; artifacts marked DRY-RUN |
| `--max-passes N` | flag (default 3) | gather-pass budget |
| `--verify N` | flag (default 2) | adversarial votes per claim |
| `--model / --reason-model` | flags (haiku / sonnet) | proxy models per models.md routing |
| `--max-claims N` | flag (default 8) | claims admitted to adversarial verify |
| `--recall` | flag | optional web layer: `studio search` (Recall KB, fail-soft) |
| `studio` CLI + `knowledge/` + `data/` | package | the deterministic corpus |
| `proofpacket/{seal,verify}.py` | package | the seal |

## Procedure

### D0 QUESTION → `question.md`

1. [det] Write `problem.txt` (the raw ask) and open `trace.jsonl` (root run).
2. [agent] One LLM pass restates the question and writes four sections:
   `## Restated question`, `## Success looks like` (3-4 observable
   outcomes), `## Symptom vocabulary` (plain verbs+nouns — feeds `studio
   map`), `## Unknowns` (what is NOT given; `Unknown` beats invention).
3. [det] Check: both heading greps hit; else the phase rewrites with
   feedback (retry ≤2, then RED). On LLM failure the artifact is written
   DEGRADED with `needs-agent-reasoning` — the check still runs on it.

### D1 DECOMPOSE → `decompose.md` + `decompose.json`

4. [agent] One LLM pass returns strict JSON `{"subquestions": [...]}` —
   3-6 independently answerable sub-questions. Deterministic keywords are
   derived per sub-question (frequency-ranked, stopword-filtered) for the
   corpus greps — the LLM does not choose the grep terms.
5. [det] Validate count 3-6 and JSON shape. On failure: deterministic
   fallback = sentence split, artifact marked DEGRADED with the error.

### D2 PARALLEL GATHER (passes 1..N) → `gather-p<i>-sq<j>.md`, `findings-p<i>-sq<j>.json`

6. [det] Per sub-question, deterministic pulls (recorded with exit codes
   verbatim in the evidence file): `studio map` (archetype symptom match),
   `studio cards systems-thinking --grep <keyword>` (local tagged corpus),
   keyword-scored grep over `knowledge/{youtube,papers,books}` (titles +
   bodies), and — only with `--recall` — `studio search <sq> focused`
   (optional web layer; timeout/unavailable recorded as a finding).
7. [agent] Per sub-question, one extraction pass over the evidence file:
   findings as JSON `{claim, quote, source-layer, subquestion}`, grounded
   ONLY in the pulled bytes. Empty list allowed — silence is a finding.
   Extraction calls run in parallel (thread pool, 4 workers).
8. [agent] Between passes (pass > 1): one gap-query pass proposes, per
   sub-question, ONE follow-up angle in different vocabulary than the
   claims already use; the next pass's extraction prompt carries it.
9. [det] Passes are bounded by `--max-passes`; every artifact of every pass
   is kept (nothing overwritten — drift between passes is inspectable).

### D3 ADVERSARIAL VERIFY → `verify.md`

10. [det] Deduplicate claims (normalized-prefix key), cap at
    `--max-claims` (rank-stable order).
11. [agent] Per claim, `--verify` independent votes, each prompted
    refute-default: "the claim is WRONG; refute it if you can" against the
    claim's own evidence string. Verdict JSON: REFUTED | SUPPORTED |
    UNVERIFIABLE + one-sentence reason. Votes run in parallel.
12. [det] Tally (deterministic, no LLM judgment): VERIFIED = zero REFUTED
    and SUPPORTED majority; REFUTED = REFUTED majority (or tie against);
    else UNVERIFIED. Write `## Method`, `## Claim votes` (table),
    `## Verdicts` (per-claim vote reasons).

### D4 SYNTHESIZE → `DELIVERABLE.md`

13. [agent] One LLM pass over: question.md + verified/refuted/unverified
    claims + evidence digest. Sections EXACTLY: `## Answer` (built from
    VERIFIED claims; UNVERIFIED material explicitly marked; Unknown where
    silent), `## Evidence` (claim → source layer + verdict), `## Refuted or
    unverified`, `## Falsifier` (one observation + a deadline in weeks),
    `## Next questions` (2-3 the evidence could not reach). No new claims
    after verification; synthesis organizes, it does not invent.
14. [det] Check: all five heading greps hit.

### D5 SEAL → `verify.log` + `proofpacket.json` + `seal.log`

15. [det] Freeze `verify.log`: the four phase checks, artifact presence
    with line counts, verdict line, and the two-command re-verify recipe.
    Freeze order matters: verify.log and trace.jsonl are finalized BEFORE
    sealing so the packet never hashes a file that changes after.
16. [det] Close the trace (root run record with verdict + run dir).
17. [det] `proofpacket/seal.py --base $RUN` over problem.txt, question.md,
    decompose.md, gather-*.md, findings-*.json, verify.md, DELIVERABLE.md,
    verify.log, trace.jsonl; then `proofpacket/verify.py` must print
    `=== VERIFIED ===`. Transcript lands in `seal.log` (unsealed by design —
    it is the only file allowed to describe the seal after the seal).
18. [det] Exit code 0 only on GREEN checks AND a verified packet; RED runs
    still seal (forensics over silence) and exit 1.

## Failure modes

1. **Question laundering** — a topic smuggled in as a question; the loop
   then "answers" nothing verifiable. Countermeasure: D0 restatement must
   name an answerable shape; symptom vocabulary must be non-empty.
2. **Reasoning-budget truncation** — the proxy's reasoning tokens eat
   `max_tokens`, JSON returns mid-string and parses as garbage.
   Countermeasure: extraction budgets 1600 tokens; `extract_json` raises a
   labeled error (truncation named), the finding degrades honestly instead
   of crashing the run.
3. **Monoculture gather** — one query phrasing per sub-question, zero
   recall on pass 2+. Countermeasure: gap queries must use different
   vocabulary than existing claims (D2 step 8 prompt + human review of
   gather files).
4. **Sycophantic verification** — votes that agree with claims because the
   prompt reads neutral. Countermeasure: refute-default standing
   instruction; VERIFIED requires zero refutations, not mere majority
   support.
5. **Claim inflation** — 40 me-too claims, verify budget exhausted on
   duplicates. Countermeasure: deterministic dedupe prefix-key + cap
   (`--max-claims`), order stable.
6. **Post-seal mutation** — editing DELIVERABLE.md after sealing breaks
   the packet hash silently. Countermeasure: freeze order (step 15-17);
   re-verify command printed in verify.log and seal.log.
7. **Degraded-run amnesia** — proxy-down run written as if reasoned.
   Countermeasure: every degraded artifact carries `needs-agent-reasoning`;
   verify.log FAILs the phase check so the run is RED, sealed for
   forensics.
8. **Unbounded depth** — "one more pass" forever. Countermeasure:
   `--max-passes` is a hard budget; depth unspent converts into
   `## Next questions`, not into a longer run.

## Worked-example skeleton

```
$ python3 scripts/deep_agent/run.py "Why do our GTM testimonials stall at \
  proposal stage?" --max-passes 2 --verify 2
[run] ~/.rig/systems-studio/runs/deep-agent/<ts>-why-do-our-gtm-testimonials-...
[decompose] 4 sub-questions
[gather] pass 1/2: total findings 7
[gather] pass 2/2: total findings 11     # gap queries re-grepped the corpus
[verify] 6 claims voted                  # dedupe collapsed 11 -> 6
... verify.md: 3 VERIFIED / 1 REFUTED / 2 UNVERIFIED
... DELIVERABLE.md: ## Answer .. ## Falsifier (4 weeks) ..
== deep-agent verify ... (PASS lines)
[1] INTEGRITY PASS / [2] ARTIFACTS PASS === VERIFIED ===
RUN GREEN — sealed sha256:<packet>
```

Real transcripts (both GREEN, both sealed): the self-test section of the
build report — a `--dry-run` on the GTM-testimonials question and a real
`--max-passes 1` run on the Meadows-dashboard question.

## Deterministic checks

1. `grep -qi '^## Restated question' question.md` AND
   `grep -qi '^## Success looks like' question.md`.
2. `decompose.json` parses; `len(subquestions) ≥ 1` (3-6 when LLM-lived;
   sentence-split fallback is marked DEGRADED in `source`).
3. Every `gather-p*-sq*.md` contains the three pull headers
   (`studio map`, `studio cards`, `knowledge/`) with exit codes recorded;
   `--recall` runs record their layer (enabled or explicitly not-enabled).
4. `grep -qi '^## Claim votes' verify.md` AND
   `grep -qi '^## Verdicts' verify.md`; every verdict is one of
   VERIFIED/REFUTED/UNVERIFIED (tally rule in `## Method`).
5. DELIVERABLE greps all five sections;
   `grep -A6 '^## Falsifier' DELIVERABLE.md | grep -E '[0-9]+ ?weeks?'`
   (dated falsifier).
6. `python3 proofpacket/verify.py $RUN/proofpacket.json` exits 0 and prints
   `=== VERIFIED ===`; `grep -E '^RUN (GREEN|RED)' verify.log` is the
   verdict oracle; exit code of the runner equals the verdict's truth.
7. Trace: `python3 -c "import json;[json.loads(l) for l in
   open('$RUN/trace.jsonl')]"` — every line parses; llm lines carry
   model + token_usage (schema: trace-schema.md check 5).

## Depth extensions

- **Vote escalation**: on split votes (R1:S1), spend one extra vote with a
  different model (sonnet judging haiku's split) instead of parking UNVERIFIED.
- **Evidence file pinning**: hash each gather file at gather time so a
  later claim→evidence audit can prove the quote existed in the pull.
- **Cross-run claim memory**: feed prior runs' REFUTED claims into the next
  run's verify prompts as standing counter-evidence.
- **Recall-on-gap-only**: enable `--recall` for pass ≥2 only — spend web
  calls where local corpus already came up silent.
- **Budget-aware passes**: stop early when a pass adds <2 new deduped
  claims (diminishing returns), converting remaining budget to Next questions.

## Handoff

The run is complete; D5 hands to the consumer, not another phase:
- `$RUN/DELIVERABLE.md` — the sealed answer (frozen; edits break the packet);
- `$RUN/verify.md` — the claim × vote table (what survived refutation);
- `$RUN/gather-*.md` + `findings-*.json` — the deterministic evidence and
  per-pass extractions (drift between passes is inspectable);
- `$RUN/trace.jsonl` — the LangSmith-compatible run tree (phases, steps,
  llm_calls with inputs/outputs/tokens/model) — ingestible unchanged by a
  future exporter when `LANGSMITH_API_KEY` exists;
- `$RUN/verify.log` + `seal.log` + `proofpacket.json` — the deterministic
  trail and the tamper-evident seal
  (`python3 proofpacket/verify.py <run>/proofpacket.json` re-proves it);
- `## Next questions` in the deliverable — the seed of the NEXT deep-agent
  run (or, when the answer is "the system is the problem", the entry brief
  for the studio's 8-phase chain: `processes/deep/01-intake.md`).
