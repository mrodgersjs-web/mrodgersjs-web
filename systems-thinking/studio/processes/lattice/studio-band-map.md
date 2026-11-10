# Studio Band Map — every CLI command and harness phase → its band

> Companion to `processes/lattice/router.md` and `data/bms-bands.json`.
> This file does not change any code; it records the band assignment of
> every surface the studio already has (verified against
> `scripts/studio.py` and `harness/systems-studio.sh` as of 2026-08-28).
> When a command or phase changes, update this map in the same commit.

## CLI commands (`scripts/studio.py`)

| Command | Band / mode | Why |
|---|---|---|
| `studio doctor` | **A1** | file/key presence checks — pure stdlib, no model, no network beyond key presence |
| `studio frame "<system>"` | **A1** | prints the framing scaffold template — fixed template lookup |
| `studio map "<symptoms>"` | **A1** | literal symptom-phrase scoring over `data/archetypes.json` — deterministic ranking |
| `studio archetype [id]` | **A1** | data lookup, full record print |
| `studio leverage [--rank N]` | **A1** | data lookup over `data/leverage-points.json` |
| `studio cards [tag] [--grep]` | **A1** | index filter over `data/card-index.json` |
| `studio card "<title>"` | **A1** | index title search with keyword fallback hint |
| `studio crosspoll "<structure>" [domain]` | **A1** (seed) / **A3** (protocol) | the mechanism ranking is deterministic; the printed 7-step PROTOCOL is completed by a governed agent — the command itself prints "deterministic seed — agent must complete the import protocol" |
| `studio pack` | **A1** | prints `references/recall-pack.md` head |
| `studio search "<query>"` | **A2** | external Recall REST behind a key, deterministic wrapper, graceful absence (falls back to index hits); no key → A1 degradation. **Observed dispatch gap (2026-08-28):** `search` is documented in the module docstring and `cmd_search` exists, but `main()` has no `"search"` branch — the call falls through to usage (exit 2). One-line A1 fix in `studio.py` `main()` when ownership allows; until then treat as A1-unavailable. |

## Harness phases (`harness/systems-studio.sh`)

| Phase | Default band / mode | Basis (stakes / reversibility / evidence / shape) | Escalates when |
|---|---|---|---|
| 00 ROUTE (this lattice) | **A1** | router is pure arithmetic | A1 UNKNOWN → A3.1; shape a2+ floors the mode up |
| 01 INTAKE → brief.md | **A2** | medium / yes (artifact editable) / 0.6-0.9 / drafting behind section gates | invented numbers → numbers guard RED; topic-intake → ask for symptom |
| 02 FRAME → frame.md | **A2** | medium / yes / 0.6 / template fill behind grep gates | blank sections ≠ Unknown → check fails |
| 03 DIAGNOSE → diagnosis.md | **A2 → A3** | medium / yes / 0.5-0.7 / map seed A1 + verification judgment | two failed map widenings → A3 probe branch (deep 03 step 3); high stakes + ambiguity → A4 |
| 04 LEVERAGE → leverage.md | **A2** | medium / yes (advisory artifact) / 0.7 / rank choice validated by section gates | rank exceeds requester authority ceiling → RED, re-choose |
| 05 GROUND → grounding.md | **A2** | medium / yes / varies with corpus / citations + gaps contract | key absent → A1 corpus-only + `## Gaps` records it; external slots fail soft |
| 06 POLYMATH → polymath.md | **A3** | medium / yes / 0.6 / 7-step protocol: multi-step, tool use, scoring ≥0.60, rejection path | metaphor-only imports → REJECTED section gate |
| 07 SYNTHESIZE → DELIVERABLE.md | **A3** | medium-high / partial (feeds action) / 0.6 / six-artifact bounded reasoning, no-new-claims guardrail | deliverable feeds outward act → Gate-D on the ACT (B4), doc stays A3 |
| 08 VERIFY + seal | **A1** | deterministic only — presence, sections, structure grep, sha256+HMAC | any missing/thin artifact (incl. DEGRADED) → RUN RED |

## Harness mechanics → band

| Mechanic | Band | Why |
|---|---|---|
| `run_phase` attempt loop (retry ≤2, 3rd = RED) | **A1** | control flow with hard caps |
| frontier react call (`--max-turns 16`, `--input` allowlist, `--cwd` scoped) | **A3** | bounded engine: turns, allowlist, scoped writes |
| `latest_output` artifact discovery | **A1** | newest-file sort |
| `salvage_answer` prose recovery | **A1** | regex salvage — the canonical "A3 failure must not break A1 fallback" |
| grep check loop + feedback-`N`.txt | **A1** | deterministic gates |
| DEGRADED logging (no artifact) | **A1** | honest failure, never silent skip |
| verify block + `proofpacket/seal.py` | **A1** | checks + sha256/HMAC seal |

## Routing quick-reference

- Everything above assumes default stakes. The router
  (`processes/lattice/router.md`) recomputes from the actual task: a
  `studio cards` run feeding a public claim inherits the CLAIM's band at
  the outward step (B4 + Gate-D), not the command's A1.
- A1-first: no phase launches its agent call before its A1 prelude
  (inputs present, CLI copied, doctor recorded) — universal rule 1.
- Outward override: any phase whose artifact triggers deploy/send/publish/
  pay/delete/migrate re-routes to B4 BEFORE the act; the artifact's
  band does not launder the act's band.
