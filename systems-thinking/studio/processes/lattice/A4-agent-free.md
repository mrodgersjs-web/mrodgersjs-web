# Lattice Mode A4 — LLM AGENT FREE (autonomous, human-gated)

> Build-mode contract for band B4 work. Canonical definition:
> `RIG_A1_A4_ARCHETYPES.md` §"A4 LLM Agent Free" (allowed: broader
> planning, adaptive tool selection, dynamic subagents, red-team review,
> falsification, Brier-style evaluation; required: A1/A2/A3 fallbacks,
> kill switch, budget switch, audit log, memory hygiene, human override).
> Forced when `outward_action == true` regardless of gate index.
> Gate-D is not optional here: no outward act ships without a typed
> `APPROVE <run_id>` naming exact target, scope, and values.

## Purpose

A4 does the work only free exploration can: novel strategy under
contradictory evidence, one-way-door decisions that deserve red-teaming
before a human signs, open-ended research where the question itself
evolves. Freedom here means freedom of THOUGHT under total accountability
of ACTION — the agent may plan, spawn subagents, and falsify itself
without per-step approval, but nothing crosses the outward boundary
(deploy/send/publish/pay/delete/migrate) and nothing destroys state
without the kill/budget switches being one human gesture away. A4 is also
the only mode whose deliverable must carry its own falsifier and Brier
bookkeeping: an A4 output that cannot lose is not an output, it is a mood.

## Entry criteria

- Router emitted `mode: a4` — gate floor B4 (index ≥4 or outward override)
  and/or `shape_floor: a4` (novel strategy, contradictory evidence,
  red-team needed) — OR A3 escalated on unresolved ambiguity, carrying its
  audit trail.
- The A4 runtime requirements exist BEFORE launch:
  1. A1 fallback (what ships if every model call fails)
  2. A2 bounded fallback (the schema chain that replays the core)
  3. A3 governed fallback (the execution graph once strategy is fixed)
  4. kill switch (one command halts and preserves state)
  5. budget switch (one command freezes spend/turns; auto-freeze at cap)
  6. audit log (every call, tool, subagent, decision — append-only)
  7. memory hygiene (no unbounded context growth; distilled state files)
  8. human override (a human can redirect at any node without a restart)
  9. Gate-D packet (the outward act's target/scope/values, pre-drafted)
- Gate-D approved OR the run is exploration-only (no outward act) with
  Gate-D scheduled at the boundary.

## Inputs

| Input | Where | Use |
|---|---|---|
| routing record + A3 audit trail | `band.json`, `audit.jsonl` | inherited context; A4 never restarts from zero |
| full prior artifacts | run dir | deeper context use is the point |
| dynamic subagent budget | named in the launch packet | each subagent = an audit row + its own allowlist |
| falsifier seed | brief §Deadline / frame §9 | the run must sharpen, never weaken, it |
| human | Mike / the requester | override, Gate-D signer, kill authority |

## Procedure

1. [det] Verify all nine runtime requirements; verify the inherited A3
   audit trail parses. Missing fallbacks = RED before launch (canonical:
   A4 only exists WITH its fallbacks).
2. [agent] Strategic framing: restate the problem as competing hypotheses
   with discriminating evidence, including the inherited ambiguity. Name
   what would make each hypothesis lose.
3. [agent] Adaptive planning: choose the investigation order by expected
   information gain, not habit. Tool selection is adaptive; tool
   ALLOWLIST still applies (adaptive ≠ unrestricted).
4. [agent] Dynamic subagents where the space is wide: spawn bounded probes
   (each with its own mini-contract: question, allowlist, budget, return
   schema). Every spawn is an audit row; subagents never inherit the
   parent's authority to act outward.
5. [agent] Red-team review: attack the emerging conclusion — strongest
   counterargument, most likely wrong-reason, incentive analysis of who
   benefits from the conclusion being true. Write both sides.
6. [agent] Falsification: design the kill condition with a date and a
   measurable observation (inherits the falsifier seed; sharpens it).
   If no observation could kill it, the deliverable is not done.
7. [det] Brier bookkeeping: for each material claim, record probability +
   resolution criteria now (before outcome knowledge); score later. Claims
   without numbers are split or dropped.
8. [det] Memory hygiene pass: distill context to state files at each
   phase boundary; the audit log is append-only, working memory is not.
9. [det] Budget switch: auto-freeze at the cap (calls/tokens/wall). A
   frozen run surfaces its partial state honestly; it does not quietly
   continue on a "small" overage.
10. [agent] Draft the Gate-D packet for ANY outward act: exact target,
    scope, values, rollback path, blast radius, and the audit rows that
    justify it. Human types `APPROVE <run_id>`. Silence is not approval;
    a prior run's approval is not this run's.
11. [det] Kill-switch test on first launch of any new A4 graph: fire the
    switch once in a dry state, verify halt + state preservation. A kill
    switch that has never been fired is a decoration.
12. [det] Terminal: deliverable + falsifier + Brier table + audit log +
    the three fallbacks named and current. Seal the ProofPacket with the
    whole trail.
13. [det] De-escalation (canonical requirement, not a courtesy): strategy
    fixed → execution drops to A3; plan encoded → replayable steps drop
    to A2/A1. Record which parts moved down. A4 that ends still doing
    everything at A4 has failed its own contract.

## Deterministic checks

1. Requirements presence — the nine runtime artifacts exist pre-launch
   (grep/ls audit); missing = RED before spend.
2. No-outward-without-Gate-D — the audit log's outward actions each
   reference a Gate-D record with matching `run_id` that PRECEDES them;
   violation = RED + quarantine.
3. Frozen-artifact protection — frozen stage artifacts (GREEN phases,
   sealed packets) show no post-freeze writes: hash comparison; edits to
   frozen stage artifacts are forbidden (canonical).
4. Kill/budget switches fired — the dry-run kill record exists (check 11)
   and the budget auto-freeze either never tripped or tripped loudly.
5. Falsifier presence — deliverable contains a dated, measurable kill
   condition (`grep -Ei 'falsifier|kill' DELIVERABLE.md` ≥ 1 with a date).
6. Brier table — every material claim has probability + resolution
   criteria at terminal; empty cells = claims that cannot lose = RED.
7. Audit completeness — every call/subagent/decision appears; append-only
   verified (line count monotone across snapshots).
8. De-escalation recorded — the terminal packet names what moved to
   A3/A2/A1; absence = the run kept autonomous mode for governed work.

## Failure modes

1. **Unsupervised destructive operation** — the classic: a "cleanup" pass
   deletes the wrong tree at 3am. Countermeasure: deletes are outward
   actions (Gate-D), kill switch, blast radius in the packet.
2. **Approval laundering** — one APPROVE stretched to cover a batch of
   later, different acts. Countermeasure: per-act packets; run_id scoping;
   the check-2 precedence rule.
3. **Credential exfiltration** — a subagent "helpfully" cats `.env` into
   a log that ships. Countermeasure: allowlists exclude secret files;
   keys never enter prompts/deliverables (`models.md` rule).
4. **Unreviewed production release** — exploration "just ends up"
   deployed because the branch auto-merged. Countermeasure: release =
   outward = Gate-D; frozen artifacts hash-checked.
5. **Infinite red-team** — falsification becomes procrastination; the
   deliverable never converges. Countermeasure: budget switch; the
   falsifier needs a DATE, and terminal requires the Brier table NOW.
6. **Context rot** — the free agent reads everything, remembers nothing
   precisely, hallucinates a citation from paragraph 400. Countermeasure:
   memory hygiene distill pass (step 8); citations re-verified against
   `data/card-index.json` / manifests before terminal.
7. **Fallback rot** — the "fallbacks" exist on paper but reference dead
   scripts. Countermeasure: fallbacks are exercised at de-escalation
   (step 13); an unrun fallback is a missing fallback.
8. **Mode squatting** — A4 kept for work A3 proved it could govern, so
   every future run pays the A4 tax. Countermeasure: check 8 makes
   de-escalation a terminal requirement.

## Studio mapping (default band A4)

| Studio surface | Why A4 |
|---|---|
| Runs whose DELIVERABLE feeds an outward act (site redesign, public claim, pricing) | outward override → B4 → Gate-D before the act |
| Strategy work with contradictory evidence across frames (the RIG+life superset question) | novel synthesis + red-team + falsification signatures |
| Phase 03 → 07 chain escalated after two failed map widenings with high stakes | A3 unresolved ambiguity → A4 |
| The studio itself never LAUNCHES A4 autonomously | the harness's 8-phase chain is A3-governed; A4 enters only via the router with Gate-D pending |

Deep-agent loop steps owned by A4: none by default — the harness loop is
A3's cage. A4 appears when the router says so, ABOVE the loop: dynamic
subagents, red-team passes, and the Gate-D packet. The loop's RED
discipline (3 attempts) still binds every A4 node that runs inside a
phase; freedom lives between nodes, never above the checks.

## Handoff

- To Gate-D: the packet (target/scope/values/rollback/blast radius) +
  audit trail + Brier table + falsifier. The human signs THIS, not a vibe.
- To A3 (post-strategy): the fixed strategy as a governed graph + the
  frozen contracts + residual budgets.
- To A2/A1 (post-encoding): the replayable procedures + their validators.
- To memory (rig-memory-os / run archive): the Brier-resolved claims and
  the falsifier, so the next run starts with the scorecard, not amnesia.
