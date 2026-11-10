# Deep Agent Trace Schema — LangSmith-compatible local JSONL sidecar

> Contract for `$RUN/trace.jsonl`, written by `scripts/deep_agent/trace.py`
> (the shared `emit_trace()` helper + `TraceWriter`). Local-first today,
> exportable tomorrow: every record's field names and shapes mirror the
> LangSmith run schema (`POST /runs` body / trace-export format), so a later
> exporter can ingest the file UNCHANGED when `LANGSMITH_API_KEY` exists.
> No LangSmith dependency now — the file must stay readable with
> `grep`/`jq`/stdlib alone. Schema version: `1.0.0`
> (`extra.metadata.trace_schema_version` on every record).

## Design rules

1. **One JSON object per line, one completed run per line.** Records are
   emitted on completion (start_time + end_time both known). A crash
   mid-call loses that line, never corrupts the file — append-only.
2. **Tree by reference, not by nesting.** Hierarchy is `parent_run_id` +
   `dotted_order`; the file is a flat stream any reader can replay in any
   order. Root record is the first line; every other record's `trace_id`
   equals the root's `id`.
3. **No secrets, no giant blobs.** Prompts/outputs are the actual strings
   (capped where huge); the proxy key never appears (it lives only in the
   runner's memory, read from `~/.hermes/.env`).

## The hierarchy

```
run (chain, name=deep-agent-run)                    ← the whole investigation
 ├─ phase (chain)  D0-question
 │   └─ llm_call (llm) question-restatement
 ├─ phase (chain)  D1-decompose
 │   └─ llm_call (llm) decompose
 ├─ phase (chain)  D2-gather-pass1
 │   ├─ step (tool) gather-p1-sq1-det        ← deterministic CLI pulls
 │   ├─ step (tool) gap-queries-p1           ← pass≥2 only
 │   ├─ llm_call (llm) extract-p1-sq1
 │   └─ llm_call (llm) ...sqN                ← parallel extractions
 ├─ phase (chain)  D3-adversarial-verify
 │   ├─ llm_call (llm) verify-c1-v1          ← votes, parallel
 │   └─ llm_call (llm) verify-c1-v2 ...
 ├─ phase (chain)  D4-synthesize
 │   └─ llm_call (llm) synthesize-deliverable
 └─ phase (chain)  D5-seal                    ← verify.log freeze check results
```

## Record contract (all record types)

| Field | Type | Present | LangSmith meaning |
|---|---|---|---|
| `id` | uuid str | always | run id |
| `name` | str | always | run name (`D2-gather-pass1`, `extract-p1-sq3`) |
| `run_type` | enum | always | `chain` (root/phases) · `tool` (det steps) · `llm` (model calls) |
| `trace_id` | uuid str | always | root run's id — the whole tree's session key |
| `parent_run_id` | uuid \| null | always | null on root only |
| `dotted_order` | str | always | `<ts>-<uuid>` chains from root to this run (ingest ordering) |
| `start_time` / `end_time` | ISO-8601 UTC (`...%fZ`) | always | span bounds |
| `inputs` | any | always | phase: `{"question": ...}` / `{"subquestions": N}`; step: sub-question + keywords; llm: `{"messages": [...]}` |
| `outputs` | any \| null | on success | phase: `{"check": "PASS"}`; step: artifact + bytes; llm: `{"generations":[{"text":...}], "output_text": ...}` |
| `error` | str \| null | always | null, or `"LLMError: truncated JSON..."` |
| `tags` | [str] | always | e.g. `["pass:2","sq:3"]`, `["phase:verify","failed"]` |
| `extra.metadata` | obj | always | `trace_schema_version`, run flags (`dry_run`, `max_passes`, `votes`) |
| `extra.invocation_params` | obj | llm only | `{"model": "claude-haiku-4-5"}` (no temperature — proxy pins it) |
| `token_usage` | obj | llm only | dual-named: `input`/`output`/`total` AND `prompt_tokens`/`completion_tokens`/`total_tokens` (both naming conventions accepted by ingest) |
| `model` | str | llm only | proxy model id |

## Example lines (abridged)

```json
{"id": "9af0...", "name": "D3-adversarial-verify", "run_type": "chain",
 "trace_id": "9af0...", "parent_run_id": "9af0...", "dotted_order": "20260828T215913039667Z-9af0....20260828T215914012003Z-77b1...",
 "start_time": "2026-08-28T21:59:14.012003Z", "end_time": "2026-08-28T21:59:41.884001Z",
 "inputs": {"findings": 11, "votes": 2}, "outputs": {"claims": 6, "check": "PASS"},
 "error": null, "tags": [], "extra": {"metadata": {"trace_schema_version": "1.0.0"}}}
{"id": "c31d...", "name": "verify-c1-v1", "run_type": "llm",
 "inputs": {"messages": [{"role": "system", "content": "You are an adversarial reviewer. Default stance: the claim is WRONG."}, ...]},
 "outputs": {"generations": [{"text": "{\"verdict\": \"REFUTED\", ...}"}], "output_text": "..."},
 "error": null, "model": "claude-haiku-4-5",
 "token_usage": {"input": 312, "output": 96, "total": 408, "prompt_tokens": 312, "completion_tokens": 96, "total_tokens": 408},
 "extra": {"invocation_params": {"model": "claude-haiku-4-5"}, "metadata": {...}}}
```

## Future LangSmith exporter (when `LANGSMITH_API_KEY` exists)

No schema change needed. The exporter is a thin shim:

```python
# sketch — do NOT add langsmith as a dependency today
import json, os, urllib.request
for line in open(f"{run_dir}/trace.jsonl"):
    rec = json.loads(line)                    # already the create_run body shape
    rec["session_name"] = rec["extra"]["metadata"].get("session_name")
    # POST https://api.smith.langchain.com/runs  (batch endpoint accepts
    # exactly these records; dotted_order preserves tree order on ingest)
```

Until then the same file answers locally:
cost audit (`jq` sum of `token_usage.total` where `run_type=="llm"`),
failure audit (`grep '"error": "LLMError'`), per-phase latency
(`end_time - start_time` per chain record).

## Harness adapter — emitting this format from `systems-studio.sh` phases

The 8-phase harness does not need the deep-agent runner to speak this
format. `scripts/deep_agent/trace.py` exposes the shared helper:

```python
emit_trace(trace_path, name, run_type="chain", inputs=None, outputs=None,
           error=None, model=None, token_usage=None, tags=None, metadata=None) -> run_id
```

- Appends ONE completed run record; if the trace file already has records,
  the new record attaches to the existing root (`trace_id` reuse, null
  parent); otherwise it becomes the root.
- CLI wrapper (bash-friendly, this is the documented one-liner per phase):

```bash
# in harness/systems-studio.sh run_phase(), after the grep gate decides:
python3 "$STUDIO/scripts/deep_agent/trace.py" emit \
  --trace "$RUN/trace.jsonl" \
  --name   "phase-$num-$name" --run-type chain \
  --input-file  "$RUN/problem.txt" \
  --output-file "$RUN/$artifact" \
  --note "attempt $attempt: $([ $ok = 1 ] && echo GREEN || echo RED)" \
  --tags "harness,phase-$num"
# on failure add: --error "checks failed:$missing"
```

Because `emit_trace()` reuses the first line's id as root, a harness run
and its per-phase records form one tree exactly like a deep-agent run —
same schema, same exporter later. `--input-file/--output-file` cap content
at 20 000 chars per record to keep the sidecar greppable.

## Deterministic checks

1. Every line parses: `python3 -c "import json,sys;
   [json.loads(l) for l in open(sys.argv[1])]" trace.jsonl` exits 0.
2. Single root: exactly one record has `parent_run_id == null`; every other
   `trace_id` equals that record's `id`.
3. Ordering sanity: every record's `dotted_order` starts with the root's
   `dotted_order` + ".".
4. LLM records complete: every `run_type=="llm"` line carries `model`
   (non-empty), `token_usage` object, and either `outputs` or `error`.
5. Version pin: every record's `extra.metadata.trace_schema_version` ==
   `"1.0.0"` (a mismatch is a schema drift, not data drift).
6. No secret leakage: `grep -c -i 'bearer\|api_key\|sk-' trace.jsonl` == 0
   beyond the schema's own field names (`invocation_params` holds model only).

## Failure modes

1. **Post-seal trace growth** — appending after the packet hashed
   `trace.jsonl` breaks `proofpacket/verify.py` ARTIFACTS. Countermeasure:
   the runner closes the trace BEFORE sealing (procedure.md D5 step 16);
   the harness adapter must likewise emit its last record before its seal.
2. **Blob bloat** — full evidence files pasted into `inputs` make the file
   unopenable in editors. Countermeasure: inputs carry references and
   counts; the CLI adapter caps file content at 20 000 chars.
3. **Orphan records** — a record whose parent was lost to a crash.
   Countermeasure: flat-stream replay tolerates orphans (order by
   `dotted_order`, not by arrival); root check (2 above) still holds.
4. **Clock skew** — `dotted_order` timestamps from a machine clock jump.
   Countermeasure: order within a record is uuid-suffixed; skew degrades
   to cosmetic.
5. **Schema drift** — exporter expects a renamed field. Countermeasure:
   version pin (check 5) + the exporter refuses non-`1.0.0` streams loudly.

## Handoff

Consumers of the sidecar, in order of likelihood:
- the run's own SEAL phase (hashes `trace.jsonl` frozen — see check 1 in
  procedure.md's Deterministic checks);
- a human debugging a RED run (grep `error`, read the vote prompts verbatim);
- the future LangSmith exporter (above) when `LANGSMITH_API_KEY` exists;
- cost/latency audit jobs (`token_usage` sums, per-phase spans) — the same
  query works across deep-agent runs AND harness runs once the adapter is
  wired into `systems-studio.sh`.
