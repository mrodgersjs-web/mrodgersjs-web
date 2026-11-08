# Lattice Mode A1 — PYTHON ONLY (deterministic, zero LLM)

> Build-mode contract for band B1 work. Canonical definition:
> `RIG_A1_A4_ARCHETYPES.md` §"A1 Python Only" and `RIG_DOCTRINE.md` §3 row
> A1. In lattice coordinates this mode is the Z-axis floor — every cell
> `L{n}-D{m}-A1-{step}` executes under this contract. The studio's entire
> deterministic spine (CLI, data, harness checks, seal) is A1.

## Purpose

A1 executes known tasks with fixed rules and no model in the decision path.
Its value is not speed alone but **accountability**: the same input replays
to the same output, a failing check fails loudly, and `UNKNOWN` is a legal
return value. A1 is the mode every other mode falls back to (universal rule
11: A2/A3/A4 failure must never break the A1 fallback) and the mode the
A1-first doctrine says you must start from. Inside the studio, A1 owns:
corpus transforms, archetype/leverage lookups, symptom-phrase scoring,
card indexing, all phase gates, retry accounting, and the ProofPacket seal.

## Entry criteria

- Router (`processes/lattice/router.md`) emitted `mode: a1`, OR a higher
  mode de-escalated into A1 with a recorded trigger, OR a fallback fired.
- The task is rule-expressible: a fixed procedure over present inputs
  produces the artifact. If any required judgment has no rule, that
  judgment returns `UNKNOWN` — it does not get guessed.
- Inputs are on disk and versioned (data files, corpus, problem text).

## Allowed / forbidden (canonical, enforced by checks)

Allowed: stdlib Python, typed contracts/Pydantic, Jinja-style templates,
fixed rules and thresholds, fixed source connectors, golden replay,
property tests, sealed binary build.

Forbidden: open-ended LLM reasoning, agentic planning, autonomous external
side effects, unbounded retries, hidden fallback, implicit schema changes.

## Inputs

| Input | Where | Use |
|---|---|---|
| routing record | `band.json` / mission packet | band, gates, trace — re-checked, not trusted blindly |
| task inputs | files on disk | the only facts; nothing invented |
| `data/*.json` | studio data layer | archetypes, leverage points, card index, bms-bands |
| `scripts/studio.py` | CLI | doctor/frame/map/archetype/leverage/cards/card/crosspoll/pack |

## Procedure

1. [det] Re-verify the routing record parses and the band is B1 (or a
   de-escalation note exists). A1 executing a B3/B4 task without one is a
   contract violation — stop.
2. [det] Prelude (universal rule 1 — never skip A1, even inside A1):
   inputs exist, non-empty, parse. `studio doctor` for corpus tasks.
3. [det] Express the task as a fixed procedure: enumerate the input set,
   the transform, the output contract (filename + schema + sections).
   If the transform cannot be written as rules, identify the exact
   judgment that blocks it and return `UNKNOWN` for that judgment.
4. [det] Implement stdlib-only. No network unless the task IS a fixed
   connector (Recall search wrapper is the A2 boundary, not A1).
5. [det] Execute. Print the command + exit code into the run log — the
   log line IS the evidence (no source, no number).
6. [det] Validate the output against the contract: sections present,
   counts sane (e.g. 853 cards in → N tagged out, N ≤ 853), no empty
   required fields, `Unknown` markers allowed where facts are absent.
7. [det] Idempotency probe: run twice, `diff` the outputs. Drift on
   unchanged inputs = non-determinism bug = RED (mtime-only diffs excluded).
8. [det] Golden replay when a prior output exists: diff against it; any
   change must trace to an input change, else it is an implicit schema
   change (forbidden) — halt and surface.
9. [det] On `UNKNOWN`: do NOT guess, do NOT silently fall back to a model.
   Emit `UNKNOWN: <judgment>` and route per the canonical rule — A1
   UNKNOWN routes to A3.1 (a bounded probe). If the UNKNOWN is a single
   schema-shaped judgment, record that an A2 wrapper is the cheaper
   intermediate and route there instead; the routing record must show
   which was chosen and why.
10. [det] Write the ProofPacket row: command, exit code, output hash,
    input hashes. A1 work is done when this exists — not before.

## Deterministic checks

1. Zero-model check — the run log contains no LLM endpoint calls:
   `grep -c '127.0.0.1:8317\|api\|chat/completions' run.log` == 0.
2. Replay check — two executions, `diff` clean (check 7 above).
3. Contract check — output schema/sections validated by a grep or stdlib
   JSON parse with required keys; missing key = RED.
4. Exit-code honesty — every invoked command's exit code appears in the
   log; a missing code for a run command = incomplete evidence = RED.
5. UNKNOWN routing — every `UNKNOWN:` line is followed (within the run) by
   a routing record to a3.1/a2; an UNKNOWN that just disappears = RED.

## Failure modes

1. **Silent guessing** — a missing value gets a plausible default because
   the schema demands it. Countermeasure: contracts treat `Unknown` as a
   first-class value; check 3 requires the key, not a non-null value.
2. **Hidden fallback** — except-path swallows a failure and returns the
   last known good output. Countermeasure: fallbacks print `FALLBACK:
   <reason>` and still write the failure to the log (never hide failures).
3. **Implicit schema change** — a "small fix" adds a field and breaks every
   golden replay downstream. Countermeasure: check 8; schema changes are
   explicit, versioned, and re-golden the corpus.
4. **Unbounded retry disguised as diligence** — retry loops without caps.
   Countermeasure: retries ≤2 with logged reasons (the harness's own
   budget); 3rd failure = RED, surfaced, not looped.
5. **Determinism theater** — code looks deterministic but sorts a dict,
   walks a directory, or hashes in insertion order that varies. On this
   box Python dicts are ordered, but `os.listdir` is not: sort explicitly.
6. **Boundary-blind rounding** — `round(0.5)` banker's-rounds to 0 and
   flips a band. Countermeasure: `floor(x+0.5)` everywhere a threshold
   boundary is computed (bms-bands bucket rule).

## Studio mapping (default band A1)

| Studio surface | Why A1 |
|---|---|
| Router (phase 00) | pure arithmetic over `data/bms-bands.json` |
| `studio doctor/frame/map/archetype/leverage/cards/card/pack` | data lookup + literal phrase scoring, no model |
| `studio crosspoll` (seed) | deterministic mechanism ranking; the printed PROTOCOL is agent work (A3), the seed is not |
| Phase 08 VERIFY + `proofpacket/seal.py` | checks + sha256/HMAC — sealed binary build, canonical A1 |
| Harness mechanics: `latest_output`, `salvage_answer`, grep gates, retry/feedback loop, DEGRADED logging | control flow, no reasoning |
| Evidence gates on any branch (per rig-phase-discipline) | commit only on green checks |

Deep-agent loop steps owned by A1: the `while :; attempt` loop, the check
loop (`grep -qi` per required section), feedback-file writes, RED exits,
and the verify block. The frontier react call inside each phase is A3;
everything around it is A1 — that split is the architecture.

## Handoff

- To A2 (when a judgment is schema-shaped): the exact judgment text, the
  proposed output schema, the deterministic validator A2 must satisfy, and
  the A1 fallback output (what ships if the model call fails).
- To A3.1 (canonical UNKNOWN route): the blocking judgment plus the bounded
  probe's question, tool allowlist (read-only first), and budget.
- Downstream studio phases: A1 outputs are given facts — grep-verified,
  hash-sealed, citable with no epistemic discount.
