# Agent Integration — Systems Thinking Studio

## Jake PAI Prime (`/jake`) — "Jake, I need this"

The request pattern: human states a need in one sentence. The flow:
1. `/jake` (or any prime session) recognizes an architectural/why-does-this-
   keep-happening ask → invokes `/systems-studio "<need>"`.
2. The harness plays all 7 phases autonomously (agent calls + checks).
3. Jake surfaces: `DELIVERABLE.md` path + the falsifier + the leverage rank
   of the chosen intervention. Human decides; studio does not ship outward
   actions (Gate-D untouched).
4. Owner routing per architecture.md: strategy asks also inform `/iris`;
   GTM/LinkedIn variants pull the recall domain packs.

## Specialist sub-agents (agent_team mode)

When the harness runs as a swarm instead of sequential react phases:

| Sub-agent | Loads | Produces |
|---|---|---|
| framer | templates/system-frame.md + archetypes.json | frame.md |
| diagnostician | `studio map` output + archetype detail | diagnosis.md |
| leverage-analyst | `studio leverage` + authority constraints | leverage.md |
| researcher | `studio search`/`cards` + knowledge/ library | grounding.md |
| synthesizer | all prior artifacts | DELIVERABLE.md |
| verifier (deterministic) | harness checks only | verify.log |

Each sub-agent gets: file paths in, file paths out, the phase contract from
processes/phases.md, and the citation rule (zero invented sources). A
sub-agent without its skill is a fresh model loop with a vague job — the
Skills Masterclass rule; that is why every role names its inputs.

## Coding agents (Claude/Codex/Hermes/omp)

Skill `systems-thinking-studio` is symlinked into every harness skills dir.
Light path: load skill → run `studio` commands inline in the session.
Full path: `/systems-studio "<problem>"` → harness → deliverable in
`~/.rig/systems-studio/runs/`.
