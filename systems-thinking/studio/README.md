# Systems Thinking Studio

Deterministic systems-thinking toolkit for every RIG coding agent — Jake PAI
prime agents, Claude Code, Codex, Hermes, and frontier runs.

- **CLI**: `studio` (on PATH via `~/.local/bin/studio`) — framing scaffold,
  archetype detection, Meadows leverage points, tagged-corpus access, live
  Recall KB search. Stdlib-only Python; sandbox-allowlist friendly.
- **Corpus snapshot**: `data/card-index.json` — all 853 Recall cards with the
  17-tag vocabulary (built 2026-08-28 by the tagging swarm;
  regenerating pipeline lives in the Systems-Thinking workspace:
  `scripts/recall_fetch_all.py` → tag → `scripts/recall_merge_tags.py`).
- **Distillation**: `references/recall-pack.md` — the 122-card
  systems-thinking knowledge pack.

## Quick use

```bash
studio doctor
studio map "quick fix works but problem returns worse every month"
studio archetype limits-to-growth
studio leverage --rank 6
studio frame "outbound pipeline"
studio cards gtm | head
studio search "feedback loops org design" exhaustive
```

## Why deterministic

The archetype table, leverage ranks, and framing scaffold are data — not
model output. Agents reason over stable structure instead of re-deriving (or
hallucinating) Meadows and Senge per session. The Recall corpus is the same:
citations resolve to real card ids and source URLs.

## Skill surfaces

Symlinked as `systems-thinking-studio` into `~/.prime/agent/skills`,
`~/.codex/skills`, `~/.hermes/skills`, `~/.claude/skills`, and
`~/.agents/skills`. Slash command `/systems-thinking` dispatches the CLI
via rig-slash.

## Refreshing the snapshot

After rerunning the tagging pipeline in the Systems-Thinking workspace:

```bash
cp <workspace>/knowledge/recall/card-index.json data/card-index.json
cp <workspace>/knowledge/recall/domains/systems-thinking.md references/recall-pack.md
studio doctor
```
