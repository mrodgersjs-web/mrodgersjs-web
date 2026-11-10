---
name: systems-thinking-studio
description: Map a problem as a system — stocks, flows, loops, archetypes, Meadows leverage, polymath import — then ship a falsifiable plan. Use for /systems-thinking, /systems-studio, plateau, "why does this keep happening", GTM/LinkedIn/sales/founder architecture, Jake PAI prime.
version: 2.2.0
tags: [rig, jake, systems, leverage, archetypes, cynefin, process-map, evidence]
---

# Systems Thinking Studio

Filesystem agents pull from. Deterministic CLI first; LLM only where judgment
is required; verification always. Gate-D untouched — the studio advises.

## Load this, then run

```bash
studio doctor          # contract + data. RED = do not proceed.
studio run "<problem>" --domain gtm --context complex  # 8-phase DET. GREEN only if classified, map hits, rank≠12, knowledge≥2, polymath≥0.60
studio run "<problem>" --context disorder  # planted RED
studio simulate gtm    # Euler 14d: baseline vs +40% volume vs rank-6 information
systems-studio "<problem>"  # 8-phase AGENT path (frontier react per phase)
studio context complex  # context → required response mode/artifacts; disorder stays RED
```

Light path: `studio map` / `studio context` / `studio leverage` / `studio crosspoll` /
`studio mechanisms [query]` / `studio operating [daily|weekly|agents|gaps]` /
`studio cards <tag>` / `studio search "<q>"` / `studio simulate <domain>`.

## The 8-phase swim lane

Orchestrator on top. One agent (or a program) per step. Tools under the step.

```
01 INTAKE → 02 FRAME → 03 DIAGNOSE → 04 LEVERAGE
        → 05 GROUND → 06 POLYMATH → 07 SYNTHESIZE → 08 VERIFY
```

| Phase | Kind | Agent | Tool |
|---|---|---|---|
| 01 INTAKE | mix | studio-intake | brief template |
| 02 FRAME | mix | studio-framer | `studio frame` / domain frame |
| 03 DIAGNOSE | det+judge | studio-diagnostician | `studio map` |
| 04 LEVERAGE | det+judge | studio-leverage | `studio leverage` |
| 05 GROUND | mix | studio-researcher | `studio cards` `search` |
| 06 POLYMATH | mix | studio-collider | `studio crosspoll` |
| 07 SYNTHESIZE | agent | studio-synthesizer | assemble |
| 08 VERIFY | det | studio-verifier | seal.py |

Maps: `process-maps/studio-8-phase.excalidraw` and `diagrams/phases-flow.svg`.
Contract: `processes/phases.md`. Per-step agents: `process-maps/agents/`.

**Rule:** an agent owns one phase. Det stages run a program. Never invent a
citation. Never skip VERIFY. Never ship outward action.

## Domain frames (do not start from a blank template)

```bash
studio frame --domain gtm
studio frame --domain linkedin
studio frame --domain sales
studio frame --domain founder
studio frame --domain mike-os
```

Mike OS (open loops, context rot, R1 polymath vs B1 jake-load vs R2 deals)
lives in `--domain mike-os`. It is one framed system, not the whole studio.

## Data that must not be re-derived

- 10 archetypes — `data/archetypes.json` (source-bound to Kim 2000)
- 12 leverage points — `data/leverage-points.json` (source-bound to Meadows 1999)
- Decision contexts — `data/decision-contexts.json` (Cynefin, source-bound)
- Theory provenance — `data/theory-spine-20260830.json`; verify with
  `scripts/verify_theory_spine.py`
- 10 polymath domains — `data/polymath-domains.json`
- 853 Recall cards — `data/card-index.json`
- BMS bands — `data/bms-bands.json`
- Domain Euler models — `data/stock-flow-models.json` (`scripts/engine.py`)
- Source-gated transfers — `data/curated-mechanisms-20260830.json`; its
  own `source_cutoff` field is authoritative until the next ProofPacket reseal.

DET VERIFY goes **RED** on: zero archetype matches, Chosen rank 12 with no
rejection, <2 knowledge hits, polymath kept<3 or domains<3, missing headings.
A green that cannot go red is theater.

The Studio v2.2 control additions require decision-context classification before
leverage; controller observability/UNKNOWN behavior; WIP/queue constraints; causal
counterfactuals; shadow thresholds; typed approval boundaries; planted failures; and
visible-degradation + restore evidence. Details: `processes/source-gated-tranche.md`
and `processes/phases.md`.

## What this studio is NOT

Not OpenBot. Not a content factory. Not a substitute for Gate-D. A red
VERIFY is a result — do not salvage it into a green deliverable.
