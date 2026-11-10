# Lattice Mode A3 — AGENT BOUNDED (governed agent workflow)

> Build-mode contract for band B3 work. Canonical definition:
> `RIG_A1_A4_ARCHETYPES.md` §"A3 Agent Bounded" (required: state object,
> nodes and edges, tool allowlist, cost budget, runtime budget, mechanism
> map, guardrail result, approval packet, audit row, failure/escalation
> path). Escalation: "A3 unresolved ambiguity -> A4" and "A3/A4 public
> action -> approval required" (RIG_DOCTRINE.md §4). The studio's harness
> react-loop IS an A3 machine: 8 phases × (bounded agent call → det check →
> retry ≤2 → RED).

## Purpose

A3 runs multi-step agency where a single bounded call cannot hold the task:
tool chains, iterative artifact refinement against checks, ambiguity that
needs probing rather than answering. Its contract is governance, not
cleverness — every transition is a visible edge with an audit row, every
tool is allowlisted, every budget (cost, runtime, turns, retries) is
enforced by the harness rather than the agent's own restraint, and the
failure path is designed before the first call. A3 is also the canonical
destination of A1's `UNKNOWN` (route to A3.1: the first bounded probe node
of the graph, read-only tools only).

## Entry criteria

- Router emitted `mode: a3` — `shape_floor: a3` (multi-step, tool use,
  mechanism map needed) and/or gate floor B3 — OR A2 confidence collapse
  (2 schema failures / decomposition > 3 / evidence < 0.40), OR A1 UNKNOWN
  routed to A3.1, OR A4 de-escalated after strategy fixed.
- The nine canonical requirements exist on disk BEFORE the first call:
  1. state object (`state.json`: phase, node, attempts, artifacts, flags)
  2. nodes and edges (written graph: phase list or node table)
  3. tool allowlist (exact commands/files the agent may touch)
  4. cost budget (max calls, max output tokens total)
  5. runtime budget (max wall time, max turns per node)
  6. mechanism map (what each node does and WHY — the causal chain)
  7. guardrail result slot (the invariant checked between nodes)
  8. approval packet (what A3 may NOT do without Gate-D — any outward act)
  9. failure/escalation path (RED conditions and where they route)
- Mechanism map present: each node's transformation stated as
  input → rule/reasoning → output, so a reviewer can audit the graph
  without re-running it.

## Inputs

| Input | Where | Use |
|---|---|---|
| routing record | `band.json` + escalation history | band B3 gates |
| prior artifacts | brief/frame/diagnosis/... | chain inputs — accumulated by the harness |
| `scripts/studio.py` + `data/*.json` | allowlisted tools | the only external capability surface |
| frontier runner | `frontier --mode react --max-turns 16` | the bounded engine; turn cap is the runtime budget |
| checks | grep gates per phase | the guardrail results |

## Procedure

1. [det] Verify all nine requirements present; a missing one is a RED
   before any model call (the graph ships complete or not at all).
2. [det] Initialize `state.json` at node 1; log the graph version.
3. [agent] Execute the current node within the allowlist. The agent may:
   read inputs, run allowlisted CLI commands, write the node's artifact.
   It may NOT: touch files outside the run dir, call non-allowlisted
   tools, modify the graph, or perform any outward action.
4. [det] Guardrail check between nodes: the deterministic gate for the
   artifact (grep sections, schema validators, quote guard, numbers
   guard). GREEN → advance the edge; miss → feedback file, retry ≤2
   (logged); 3rd failure → RED.
5. [det] Audit row per transition: `{node, attempt, checks, verdict,
   artifact hash, tokens, wall time}` appended to `audit.jsonl`. Unlogged
   retries are forbidden (canonical).
6. [agent] Ambiguity probe (the A3 core skill): when the node's inputs
   are insufficient, formulate the discriminating question and choose a
   read-only probe from the allowlist (e.g. `studio map` on paraphrases).
   Two failed widenings (deep 03 step 3) = unresolved ambiguity.
7. [det] Escalation decision at each node exit:
   - unresolved ambiguity after budget → A4 (with the ambiguity statement,
     the probes tried, and the residual budget)
   - outward action proposed → FREEZE. Re-route B4 + Gate-D. The agent
     does not "notice" an approval; the routing record changes first.
   - guardrail conflict (two checks pass, their conjunction is nonsense —
     e.g. quote guard green but the intervention contradicts the quote)
     → red-team needed → A4 candidate; record the conflict verbatim.
8. [det] Budget enforcement: total calls ≤ cost budget, wall clock ≤
   runtime budget, turns per call ≤ 16. Any breach = RED (budgets are
   switches, not suggestions).
9. [agent] Node completion: the artifact + its mechanism-map row updated
   (what transformed, why). The map stays current or the audit is stale.
10. [det] Terminal node: run the phase-08-style verify (all artifacts,
    all sections, citations resolve), write the ProofPacket with the full
    audit trail, seal.
11. [det] De-escalation review at terminal: which node procedures are now
    stable (same checks green across ≥3 runs)? Those re-implement as A2
    schema chains or A1 rules; the NEXT run's graph shrinks. Agency is a
    residue, not a lifestyle.

## Deterministic checks

1. Completeness — the nine requirements exist as files/sections before
   call 1: `ls`/grep audit; missing = RED before any spend.
2. Allowlist adherence — the audit log's command lines all match the
   allowlist regex; any non-matching invocation = RED.
3. Audit continuity — `audit.jsonl` has one row per transition; gaps or
   out-of-order attempts = RED (the trail is the product).
4. Budget check — totals ≤ budgets; breach = RED even if artifacts are
   green (overrun output is unaccountable output).
5. Retry discipline — no node shows >3 attempts; every retry carries a
   feedback line (unlogged retry = canonical violation).
6. Freeze check — if any outward action appears in the log, a Gate-D
   approval record with matching `run_id` MUST exist and precede it;
   otherwise RED + the outward artifact is quarantined.
7. Graph/audit agreement — the mechanism map's node list equals the
   audit's observed nodes; a node that ran but isn't mapped (or vice
   versa) = RED.

## Failure modes

1. **Infinite loop dressed as persistence** — the agent re-tries a failing
   node with cosmetic variation forever. Countermeasure: retry ≤2 per node,
   RED on 3rd; wall-clock budget as the outer cage.
2. **Unapproved external write** — "it was just a config tweak" on a live
   system mid-node. Countermeasure: allowlist + freeze check; outward
   anything re-routes through Gate-D first.
3. **Agent-created tools** — the agent writes itself a helper script and
   runs it (tool creation without review). Countermeasure: allowlist
   covers scripts too; new tools are a graph change = human review.
4. **Unbounded memory writes** — the agent appends to every artifact it
   reads "for context". Countermeasure: write set = the node's artifact
   + audit/state files; the check-2 regex enforces it.
5. **State divergence** — `state.json` says node 4, artifacts say node 6
   (a crash skipped state writes). Countermeasure: state update is atomic
   with the audit row; check 3 catches divergence on resume.
6. **Governance theater** — the nine requirements exist as boilerplate,
   never consulted. Countermeasure: check 7 ties map to observed nodes;
   mechanism-map rows must reference the audit rows they explain.
7. **Escalation amnesia** — ambiguity resolved by A4-grade reasoning
   silently inside A3. Countermeasure: the escalation decision (step 7)
   is a logged binary per node; "handled it myself" on an A4-shaped
   ambiguity is a RED in review.

## Studio mapping (default band A3)

| Studio surface | Why A3 |
|---|---|
| Phase 06 POLYMATH | 7-step import protocol: multi-step, tool use (`crosspoll`), scoring, rejection path, output contract — the canonical in-studio A3 |
| Phase 07 SYNTHESIZE | six-artifact reasoning under "no new claims" guardrails; bounded by turn cap + section gates |
| Phase 03 DIAGNOSE when map misses ×2 | the doc's own ambiguity branch: widen → re-map → discriminate is a probe graph |
| Each harness `run_phase` react call | bounded engine: --max-turns 16, inputs allowlist (`--input`), cwd-scoped writes, det gates between calls |
| The retry-with-feedback loop as a whole | node = (agent call → check → feedback → retry ≤2 → RED) — state, budgets, audit, escalation all present |

Deep-agent loop steps owned by A3: the react call itself (tools, turns),
the artifact write from agent reasoning, and the ambiguity probes. The
loop's CONTROL (when to retry, when to RED) stays A1 — A3 lives inside an
A1-built cage, which is the whole design.

## Handoff

- To A4 (escalation): the ambiguity statement, probes tried, audit trail,
  residual budget, and the specific red-team/falsification need. A4 must
  not restart the graph; it inherits it.
- To Gate-D: any proposed outward action with exact target/scope/values
  and the audit rows that led to it.
- To A2/A1 (de-escalation): the stabilized node procedures, their frozen
  contracts, and the checks that will keep guarding them.
- To phase 08 VERIFY: the complete audit trail + mechanism map, so the
  seal binds not just artifacts but the PATH that produced them.
