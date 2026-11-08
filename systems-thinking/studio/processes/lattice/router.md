# Lattice Router — TASK → band + mode + gates

> The lattice's phase 00. Runs BEFORE `harness/systems-studio.sh` creates a
> run dir and before any agent is invoked. Pure arithmetic over
> `data/bms-bands.json` — no model in the routing decision path (A1 by
> construction). Deepens the studio's `processes/` layer with the canonical
> RIG Z-axis (BMS Confidence / Build Mode A1-A4).

## Purpose

ROUTER converts any incoming task into a four-part assignment —
**band (B1-B4), mode (A1-A4), required gates, and the scoring trace** — so
that low-stakes reversible work stays fast and high-stakes one-way-door work
gets the full gated treatment. It is the studio-local implementation of
RIG_DOCTRINE.md §4 ("every task must be scored or classified into a BMS mode
before acting") and of the `rig-bms-band-calculator` arithmetic, extended
with the doctrine's routing signatures as a deterministic `shape_floor`
lookup. The A1-first doctrine lives here: the computed mode is the MINIMUM
that satisfies both the task's shape and its consequences; starting above it
without a recorded reason is a routing violation, not ambition.

Canonical sources this router aligns with (read before editing):

- `~/RIG-Transfer/rig-128gb-agent-os-20260621/payload/rig-agent-doctrine/rig-agent-doctrine/RIG_DOCTRINE.md` §3-4
- `~/RIG-Transfer/rig-128gb-agent-os-20260621/payload/rig-agent-doctrine/rig-agent-doctrine/RIG_A1_A4_ARCHETYPES.md`
- `~/RIG-Transfer/rig-128gb-agent-os-20260621/payload/rig-agent-doctrine/rig-agent-doctrine/RIG_LATTICE.md`
- `~/.hermes/skills/rig-bms-band-calculator/SKILL.md`

## Entry criteria

- A task exists as one or more sentences (the same object that would become
  `problem.txt`). A topic with no observable task is routed anyway, flagged
  `topic-intake` — fixing that is phase 01's job, not the router's.
- `data/bms-bands.json` is present and parses (router self-checks).
- No run dir exists yet; the router's output PRECEDES `01-intake`.

## Inputs

| Input | Where | Determination |
|---|---|---|
| `stakes` low/med/high | requester statement or cost-of-wrong analysis | [agent] judgment, recorded with one-line reason |
| `reversibility` yes/partial/no | artifact + blast radius | [agent] judgment; `no` for any deploy/send/publish/pay/migrate |
| `evidence_density` 0.0-1.0 | share of grounding already on disk | [det] start from corpus presence (`studio doctor`), adjust for requester-given facts |
| `outward_action` bool | does the task END in an external side effect | [det] keyword scan of the task text (deploy/publish/send/pay/delete/migrate) + [agent] confirm |
| `shape_floor` a1-a4 | routing-signature lookup (RIG_DOCTRINE.md §4) | [agent] pick the signature row that matches; ties resolve DOWN (A1-first) |

Only `stakes`, `reversibility`, `evidence_density`, `outward_action` feed the
gate arithmetic. `shape_floor` is the doctrine's capability selector; it can
raise the mode above the gate floor, never lower it.

## Procedure

1. [det] Load `data/bms-bands.json`; fail closed (exit non-zero) if the file
   is missing or the `table` array has ≠ 18 rows.
2. [det] Outward scan: `grep -oiE 'deploy|publish|send|pay|delete|migrate|ship|dm|post'`
   over the task text. Any hit sets `outward_action_candidate=true`.
3. [agent] Confirm or clear `outward_action_candidate` — a hit inside a
   quoted refusal ("do not post more") is not an outward act. Record the
   confirmation one-liner; an unconfirmed `true` fails the audit check.
4. [agent] Score `stakes` and `reversibility` per the JSON definitions, each
   with a one-line reason. If the requester already stated stakes, that
   statement is the given fact — do not re-derive.
5. [det] Compute `evidence_bucket = floor(evidence_density + 0.5)` (round
   half UP — never Python `round()`, see failure mode 4).
6. [det] `gate_index = stakes_score + reversibility_score - evidence_bucket`.
7. [det] Band: `<=1 → B1, 2 → B2, 3 → B3, >=4 → B4`; if `outward_action`
   then band := B4 unconditionally.
8. [agent] Select `shape_floor` by signature:
   - a1: known task, fixed rules produce the artifact, repeatable script possible
   - a2: drafting/transformation, Python can validate output against a schema
   - a3: multi-step, tool use required, mechanism map needed
   - a4: novel strategy, contradictory evidence, red-team/falsification needed
   Ambiguity between two rows resolves to the LOWER row (A1-first bias).
9. [det] `mode = max(shape_floor, gate_mode_floor)` where gate floors are
   B1→a1, B2→a2, B3→a3, B4→a4. If a BMS confidence score (0-1) already
   exists in the mission packet, cross-check per RIG_DOCTRINE.md §4
   (≥0.75→a1, 0.45-0.74→a2, 0.25-0.44→a3, <0.25→a4); disagreement takes the
   higher floor and records why.
10. [det] Emit gates: B4 or any `outward_action` → **Gate-D mandatory**
    (typed `APPROVE <run_id>`, exact target/scope/values); B3 → guardrail
    result + audit row + approval packet on transitions; B2 → schema
    validation + output diffing; B1 → phase checks only.
11. [det] Write the routing record into the run dir as `band.json` (or into
    the mission packet when no run dir exists):
    `{task, inputs, evidence_bucket, gate_index, band, shape_floor, mode,
    gates, trace, timestamp}`. The trace is the arithmetic verbatim —
    rerunning the router on the same inputs must reproduce it byte-for-byte.
12. [agent] A1-first attestation: if the mode is a3/a4, write one sentence
    naming what A1/A2 could NOT do (which UNKNOWN, which validation failure,
    which ambiguity). No sentence → routing violation.
13. [det] Hand off to the mode doc: `processes/lattice/A{1,2,3,4}-*.md`, and
    for studio problems continue into `harness/systems-studio.sh` phase 01.

## Deterministic checks

1. Table integrity — 18 rows, every combination present:
   ```bash
   python3 - <<'PY'
   import json, itertools
   t=json.load(open('data/bms-bands.json'))['table']
   combos={(r['stakes'],r['reversibility'],r['evidence_bucket']) for r in t}
   want={(s,rv,e) for s in (0,1,2) for rv in (0,1,2) for e in (0,1)}
   names=[('low','medium','high'),('yes','partial','no')]
   want={(names[0][s],names[1][rv],e) for s,rv,e in want}
   print('TABLE:','PASS' if combos==want and len(t)==18 else 'FAIL')
   PY
   ```
2. Index consistency — every row's `gate_index` equals its scores minus bucket:
   ```bash
   python3 - <<'PY'
   import json
   d=json.load(open('data/bms-bands.json'))
   S={'low':0,'medium':1,'high':2}; R={'yes':0,'partial':1,'no':2}
   bad=[r for r in d['table'] if S[r['stakes']]+R[r['reversibility']]-r['evidence_bucket']!=r['gate_index']]
   B=lambda i:'B1' if i<=1 else 'B2' if i==2 else 'B3' if i==3 else 'B4'
   bad+=[r for r in d['table'] if B(r['gate_index'])!=r['band']]
   print('INDEX:','PASS' if not bad else f'FAIL {bad}')
   PY
   ```
3. Examples replay — the three canonical cases reproduce their published modes:
   ```bash
   python3 - <<'PY'
   import json, math
   d=json.load(open('data/bms-bands.json'))
   S={'low':0,'medium':1,'high':2}; R={'yes':0,'partial':1,'no':2}
   G={'B1':'a1','B2':'a2','B3':'a3','B4':'a4'}; N={'a1':1,'a2':2,'a3':3,'a4':4}
   for ex in d['examples']:
       i=ex['inputs']; idx=S[i['stakes']]+R[i['reversibility']]-math.floor(i['evidence_density']+0.5)
       band='B4' if i['outward_action'] else ('B1' if idx<=1 else 'B2' if idx==2 else 'B3' if idx==3 else 'B4')
       mode='a'+str(max(N[G[band]],N[i['shape_floor']]))
       ok = mode==ex['mode'] and (band=='B4')==i['outward_action'] and (('Gate-D' in str(ex.get('gates',[]))) == i['outward_action'])
       print(f"{ex['case'][:40]:42s} idx={idx:2d} band={band} mode={mode} -> {'PASS' if ok else 'FAIL'}")
   PY
   ```
4. Outward override — no row of the 18, nor any runtime input, yields a band
   below B4 when `outward_action` is true (enforced in code path step 7;
   audit: grep the emitted `band.json` for `"outward_action": true` and
   assert `"band": "B4"` on the same object).
5. Rerun determinism — route the same task twice; `diff` the two `band.json`
   files ignoring `timestamp`; any drift is a fail.

## Failure modes

1. **Stakes inflation** — everything is "high stakes" so everything routes
   B3/B4 and the lattice becomes ceremony. Countermeasure: stakes needs a
   one-line cost-of-wrong reason citing money/brand/contract/compounding
   stock; "feels important" is not a reason.
2. **Reversibility optimism** — "we can always revert" said about a public
   URL (screenshots, RSS, archives live forever). Countermeasure:
   reversibility `yes` requires naming the restore mechanism (branch,
   backup, re-run) in the reason line.
3. **Shape-floor grade inflation** — a3/a4 chosen because the agent prefers
   free exploration. Countermeasure: A1-first attestation (step 12) + the
   tie-resolves-down rule; a missing attestation fails the audit.
4. **Banker's rounding drift** — Python `round(0.5)==0` silently shifts the
   evidence bucket and flips bands at the boundary. Countermeasure:
   `floor(e+0.5)` only, everywhere; the check-2 script would catch a table
   built on `round()`.
5. **Outward-action blindness** — the deploy hides two steps downstream
   ("update the config" → CI pushes to prod). Countermeasure: keyword scan
   runs on the FULL task text including quoted subtasks; confirmation step
   asks "what does the LAST step of this task touch?"
6. **Routing theater** — band recorded, then execution ignores it (an A2
   task run with a free agent because it was convenient). Countermeasure:
   mode docs' deterministic checks each grep the run artifacts for
   mode-appropriate evidence (schema validation log for A2, audit rows for
   A3, approval packet for A4).
7. **Stale band** — mid-flight scope growth (new outward step, evidence
   collapsed) leaves the original band in force. Countermeasure:
   re-route on material scope change (the band-calculator skill's own
   trigger); escalation triggers in `bms-bands.json` name the concrete
   thresholds (decomposition > 3, evidence < 0.40, 2 schema failures).

## Worked example

"Redesign the public marketing site hero" →

- outward scan hits `publish/ship` context → `outward_action=true`
- stakes high (brand surface, lead flow), reversibility no (public one-way door)
- evidence 0.5 → bucket 1 → `gate_index = 2+2-1 = 3` → B3, **overridden to
  B4 by outward** → gate floor a4; shape a4 (novel strategy, red-team) →
- mode **a4**, gates **[Gate-D]**; A1-first attestation: "no fixed rule
  produces a brand judgment; A2 cannot red-team its own output."
- Contrast: the same redesign on a preview branch (outward=false,
  reversibility=yes) scores `2+0-1=1` → B1 → mode = max(a4, a1) = a4 for
  the creative work, but the GATE weight collapses — checks only, no
  Gate-D until merge-to-public is proposed (which re-routes outward=true).

## Handoff

- Mode doc `A{mode}-*.md` receives: the band, the mode, the gates, the
  trace, and the A1-first attestation. Each mode doc's entry criteria
  re-state them as hard requirements.
- For studio problems, phase 01 INTAKE receives the routing record as an
  input constraint: `## Stakes` in the brief must agree with the router's
  `stakes` (disagreement = re-route, not silent edit).
- Gate-D (when required) receives the exact outward action, target, scope,
  and values — approval is typed against `APPROVE <run_id>`, never implied
  by silence or by a prior run's approval.
- Escalation/de-escalation mid-run writes a NEW routing record (append,
  never overwrite) — the band history is the audit trail.
