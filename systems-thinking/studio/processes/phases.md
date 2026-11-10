# Studio Processes — The Eight Phases

Executable truth is `harness/systems-studio.sh` (agent path) and
`studio run "<problem>"` (deterministic path). This file is the contract.
Every phase: produce the named artifact → check sections → retry ≤2 →
advance only on green. Red = stop.

| # | Phase | Artifact | Kind | Agent | Tool |
|---|---|---|---|---|---|
| 01 | INTAKE | `brief.md` | mix | `studio-intake` | template fill |
| 02 | FRAME | `frame.md` | mix | `studio-framer` | `studio frame` |
| 03 | DIAGNOSE | `diagnosis.md` | det+judge | `studio-diagnostician` | `studio map` |
| 04 | LEVERAGE | `leverage.md` | det+judge | `studio-leverage` | `studio leverage` |
| 05 | GROUND | `grounding.md` | mix | `studio-researcher` | `studio cards` / `search` |
| 06 | POLYMATH | `polymath.md` | mix | `studio-collider` | `studio crosspoll` |
| 07 | SYNTHESIZE | `DELIVERABLE.md` | agent | `studio-synthesizer` | assemble prior |
| 08 | VERIFY | `verify.log` + ProofPacket | det | `studio-verifier` | `proofpacket/seal.py` |

Orchestrator: `systems-studio` — walks 01→08, never silent-drops, never
skips 08, never invents sources.

## 01 INTAKE → `brief.md`
Problem, requester, stakes, constraints, what success looks like, deadline.
Required headings: `## Problem` / `## Success looks like`.
The brief is the contract; later phases may not shrink it silently.

## 02 FRAME → `frame.md`
Fill `templates/system-frame.md` (or a domain frame under
`templates/frames/`). Boundary, stocks, flows, actors, ≥1 R + ≥1 B loop,
≥1 delay, measurement, falsifier. Unknown is an answer; blank is not.

Source-gated control addition: name the controller, observed state, sampling
delay, allowed action, and UNKNOWN route. Missing observation is a BLOCKED
state, never an adaptive guess.

Decision-context gate: classify `clear`, `complicated`, `complex`, `chaotic`, or
`disorder` using `studio context`. Record the classification, confidence, matching
response mode, and required artifact. `disorder` is RED until decomposed; it may
not pass a leverage recommendation.


## 03 DIAGNOSE → `diagnosis.md`
Run `studio map` on the symptom words; verify the suspect's predicted stock
is actually moving. Required: `## Suspect` / `## Evidence` /
`## Counterintuitive`.

## 04 LEVERAGE → `leverage.md`
Run `studio leverage`. Mark where current interventions sit (rank 12–1);
choose the highest rank the requester's authority allows; record the
one-rank-higher option and why it was rejected.
Required: rank number / `## Chosen` / `## Rejected`.

Source-gated control addition: record WIP cap, queue-age signal, drain
condition, and bottleneck owner. More agents/schedules are rejected until the
constraint is evidenced.

## 05 GROUND → `grounding.md`
`studio cards`, `studio search`, `knowledge/` library. Cite as
`[Card: title](url)`. Absent evidence is a finding: `## Gaps` is mandatory.
Required: `## Citations` / `## Gaps`.

When using `data/curated-mechanisms-20260830.json`, cite the mechanism card
hash and transfer type. Domain analogies provide structure only; never import a
literal domain prescription as a RIG change.

## 06 POLYMATH → `polymath.md`
`studio crosspoll` against `data/polymath-domains.json`. Import mechanisms
from ≥3 non-native domains. Transfer score ≥ 0.60. Metaphor-only = REJECTED.
Required: `## Target structure` / `## Top imports` / `## Rejected (metaphor-only)`.

## 07 SYNTHESIZE → `DELIVERABLE.md`
Analysis → ranked interventions (leverage rank + owner) → falsifier with
date → what was rejected. No new claims after grounding.
Required: `## What is happening` / `## What to do` / `## Falsifier` / `## Rejected`.

Every intervention packet also states: causal hypothesis + rival explanation;
shadow baseline and divergence threshold when reversible; approval owner/scope/
expiry for high-impact action; affected human roles/incentives/override route.

## 08 VERIFY → `verify.log`
Deterministic only. Every artifact present, every section check green,
falsifier dated, polymath gate present. Seal ProofPacket. Honest RED if
any phase is missing or thin — including DEGRADED (proxy down).

In addition to file/heading checks, VERIFY requires: a planted-failure result
for the guarded boundary; counterfactual/falsifier; visible-degradation and
restore evidence for fallback claims; and situation coverage (state × boundary
× failure mode) for high-stakes changes.
