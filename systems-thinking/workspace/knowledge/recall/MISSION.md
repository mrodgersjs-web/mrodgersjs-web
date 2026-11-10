# MISSION — Recall Card Intelligence for Jake PAI Prime (sandbox edition)

You are executing a staged swarm mission over Mike's Recall.it knowledge base
(853 cards). You run in a sandbox: all inputs are mounted READ-ONLY under
`/inputs/`; write every output under `outputs/` (create subdirs as needed).
The Recall API is READ-ONLY — never attempt writes to it. No outward actions.
All network calls go to `backend.getrecall.ai`.

## Inputs (read-only, under /inputs/)

- `MISSION.md` — this file
- `all-cards.json` — full inventory (853: id, title, source_url, created_at)
- `batch-01.jsonl … batch-06.jsonl` — batches of ~143. Each line:
  `{id, title, source_url, mirror_tags?, mirror_path?}` where `mirror_tags`
  are Mike's earlier free-form tags and `mirror_path` is an ABSOLUTE path to a
  local markdown file with the card's full content (66% coverage; readable).
- `mirror-join.json` — id -> mirror markdown path
- `recall_api.py` — stdlib-only API client (copy it OUT of /inputs before use:
  `cp /inputs/recall_api.py .` then `python3 recall_api.py …`). It reads the
  key from env RECALL_API_KEY or ~/.hermes/.env. Subcommands:
  - `python3 recall_api.py status`
  - `python3 recall_api.py search "query" exhaustive` → JSON documents+chunks
  - `python3 recall_api.py card <card_id> "focus query" 50`
- `recall_merge_tags.py` — deterministic merge + verification gate (also copy
  out before running; it reads `all-cards.json`, `tags/batch-*.out.jsonl`,
  `raw/mirror-join.json` relative to cwd — arrange your outputs/ tree to match:
  `outputs/raw/all-cards.json`, `outputs/raw/mirror-join.json`,
  `outputs/tags/batch-*.out.jsonl` — copy the inputs into that layout first).

## Fixed tag vocabulary (nothing outside this set)

CORE: `systems-thinking` `psychology` `startup` `founder` `growth` `linkedin` `sales` `gtm` `tools`
EXTENDED: `ai-agents` `marketing` `content` `productivity` `strategy` `engineering` `finance` `other`

Rules: 1–3 tags per card. Prefer CORE. Use EXTENDED to keep `other` small.
`tools` = named software/tools/CLIs/workflows a working agent could adopt.
Multi-tag honestly (LinkedIn growth funnels = `linkedin`+`growth`). Map
`mirror_tags` into this vocabulary ("gtm, go to market" → `gtm`;
"strategic thinking" → `systems-thinking`/`strategy`), but title+content
decides, not the old tag alone.

## Stage A — Tagging swarm (6 parallel sub-agents)

One sub-agent per batch. Sub-agent N:
1. Read `/inputs/batch-NN.jsonl`.
2. Classify each card from title + URL domain + mirror_tags (and, only when
   genuinely ambiguous, `head -40` of mirror_path). No API calls in this stage.
3. Write `outputs/tags/batch-NN.out.jsonl` — SAME line order as input:
   `{"id": "<id>", "tags": ["<tag>", ...], "reason": "<=8 words"}`
4. Final message: `batch-NN: N cards tagged` only.

## Stage B — Merge gate (main agent, after ALL Stage A files exist)

1. Lay out: `mkdir -p outputs/raw outputs/tags outputs/by-domain outputs/domains`
   `cp /inputs/all-cards.json outputs/raw/` ; `cp /inputs/mirror-join.json outputs/raw/`
   `cp /inputs/recall_merge_tags.py .`
2. Run `python3 recall_merge_tags.py` from a cwd where `knowledge/recall/…`
   resolves — simplest: create `knowledge/recall` as a symlink to `outputs`
   (`mkdir -p knowledge && ln -sfn ../outputs knowledge/recall` from repo root
   of the sandbox) so the script's hardcoded relative paths work.
3. It must print `VERIFIED 853/853 cards tagged`. Fix flagged batches and
   rerun. Do not proceed on red.

## Stage C — Domain knowledge packs (9 parallel sub-agents, after Stage B)

One sub-agent per CORE domain. Sub-agent for domain D:
1. Read `outputs/by-domain/D.json` — the tagged card spine.
2. Content: for cards with `mirror_path`, read those files. For the rest, run
   2–4 `python3 recall_api.py search "<variants>" exhaustive` calls (e.g. gtm:
   "go-to-market strategy", "ICP positioning", "demand generation") and/or
   `card <id> "<focus>" 50`. Save raw JSON to `outputs/raw/<domain>-search.json`.
3. Write `outputs/domains/<domain>.md`:
   - Lead line: `> Cards tagged: N · Content sources: mirror X / API Y`
   - `## <Sub-theme>` sections; one insight per bullet; keep specifics
     (numbers, steps, named tactics); no filler
   - Cite as `[Card: <title>](<source_url>)`; only real cards, zero invented sources
   - End with `## Open gaps` if coverage is thin
4. Final message: one-paragraph summary of the domain's strongest material.

## Stage D — Jake PAI master index (main agent, after Stage C)

Write `outputs/README.md`:
- Purpose: operating knowledge for Jake PAI Prime's 23-agent fleet
- Table: domain → pack file → cards tagged → top 5 takeaways → owning agent:
  - `gtm`, `sales` → /darius (GTM Studio), /darius-jr (Sales Studio)
  - `linkedin` → /ralph (LinkedIn Studio)
  - `systems-thinking`, `strategy` → /iris (Strategy Studio)
  - `startup`, `founder`, `growth` → /opal (Product Studio)
  - `tools`, `psychology` → /jake (Prime Conductor) — cross-fleet
  - `content` → /steve (Content Studio)
- Stats from `outputs/card-index.json` (cards per domain, mirror coverage)
- Live access: `python3 scripts/recall_api.py search "<q>" exhaustive`
  (in the repo: `scripts/recall_api.py`); tagged index at
  `knowledge/recall/card-index.json` in the destination repo
- Note: tags live in the repo because the Recall API is read-only

## Success criteria (verify before finishing)

1. 6 `outputs/tags/batch-*.out.jsonl` pass the merge gate (853/853)
2. 9 `outputs/domains/*.md` files, each non-trivial and citation-backed
3. `outputs/README.md` master index with the table and stats
4. Final report: per-domain card counts + the 5 highest-value cards fleet-wide
