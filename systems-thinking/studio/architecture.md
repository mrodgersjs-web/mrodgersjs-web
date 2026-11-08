# Systems Thinking Studio — Architecture

> The studio is a FILESYSTEM agents pull from at the right time. This document
> is the map: what exists, where it lives, who uses it, in what order.
> Built 2026-08-28. Owner: `/iris` (Strategy Studio) with `/jake` (Prime
> Conductor) as fleet-wide consumer.

## The one-line pattern

"Jake, I need this" → **intake** → deterministic systems tooling frames the
problem → agents diagnose + rank leverage → corpus/ground layer cites prior
art → synthesis ships a plan with falsifiers → harness verifies every phase.
Deterministic where possible (CLI, checks), LLM where necessary (reasoning),
verification always.

## Layers

| Layer | What | Where | Deterministic? |
|---|---|---|---|
| Tools | `studio` CLI: frame/map/archetype/leverage/cards/card/search/pack | `scripts/studio.py`, on PATH | 100% |
| Data | archetypes (10), leverage points (12), card index (853), recall pack | `data/`, `references/` | 100% |
| Knowledge | distilled YouTube cards, paper notes, book canon | `knowledge/{youtube,papers,books}/` | sourced+cited |
| Processes | phase procedures (7) | `processes/` | procedure |
| Harness | phase-gated chain runner + acceptance checks | `harness/systems-studio.sh` | 100% |
| Agents | prime-agent integration + specialist sub-agent specs | `agents/` | role |
| Models | routing table (local fleet first) | `models.md` | config |

## The vertical slice (how a request plays through)

```
"Jake: our LinkedIn engine plateaued — figure out why and what to do"
  │
  ▼
/systems-studio "…"                     ← slash command (any harness)
  │
  ▼
harness/systems-studio.sh               ← deterministic chain, 8 phases
  ├─ 01 INTAKE      problem brief → run dir                [template fill]
  ├─ 02 FRAME       stocks/flows/loops/delays scaffold     [studio frame + agent]
  ├─ 03 DIAGNOSE    `studio map` + archetype verification  [CLI + agent]
  ├─ 04 LEVERAGE    `studio leverage` + rank choice        [CLI + agent]
  ├─ 05 GROUND      corpus + knowledge + live search       [CLI + agent]
  ├─ 06 POLYMATH    `studio crosspoll` + transfer scoring  [CLI + agent]
  ├─ 07 SYNTHESIZE  deliverable: analysis→plan→falsifiers  [agent]
  └─ 08 VERIFY      checks + ProofPacket seal (sha256+HMAC)[det only]
        │
        ▼
  run dir: brief, frame, diagnosis, leverage, grounding, polymath,
  DELIVERABLE.md, verify.log, proofpacket.json — promotable to any repo's docs/
```

Every phase: agent call → deterministic check → retry(≤2 with feedback) →
next. Red phase = stop, log, surface. No phase advances on red.

## Studio-as-filesystem doctrine (for the other studios)

Each studio is a package with the same shape:
`tools (deterministic CLI) + data (cited, versioned) + knowledge (distilled
sources) + processes (phase procedures) + harness (phase-gated runner) +
agents (integration specs) + models.md (routing) + SKILL.md (agent entry)`.
The agent does not "remember" the studio; it pulls exactly the layer the
current phase needs (progressive disclosure — Skills Masterclass doctrine:
reusable procedures, small top-level, specialized refs on demand, always
connected to verification).

## What each consumer pulls

| Consumer | Pulls | When |
|---|---|---|
| Jake PAI prime (`/jake`) | SKILL.md + `studio` CLI + harness | any "I need X" architectural ask |
| `/iris`, `/iris-jr` | processes/ + knowledge/ | strategy, forecasting, moat work |
| `/darius`, `/ralph` | domains packs (recall corpus) + diagnose workflow | GTM/LinkedIn systems design |
| Claude Code / Codex / Hermes | skill symlink + `/systems-thinking` slash | any session, any repo |
| frontier runs | `studio` CLI (allowlist-safe) + harness phases | long-horizon autonomous work |

## Registry status

Skill: `systems-thinking-studio` symlinked in `~/.prime/agent/skills`,
`~/.codex/skills`, `~/.hermes/skills`, `~/.claude/skills`, `~/.agents/skills`.
Slash: `/systems-thinking` (CLI dispatch) and `/systems-studio` (full slice).
Harness runs root: `~/.rig/systems-studio/runs/`.

## Extension slots (wired, awaiting creds)

- **Parallel AI** — web-scale search for the GROUND phase. Env slot
  `PARALLEL_API_KEY`; integration point `processes/05-ground.md`.
- **Consensus MCP** — academic literature beyond arXiv/S2. Mount MCP server,
  add tool call in GROUND phase. Env slot `CONSENSUS_API_KEY`.
- Both slots fail soft: GROUND falls back to `studio search` + knowledge/ + arXiv/S2.
