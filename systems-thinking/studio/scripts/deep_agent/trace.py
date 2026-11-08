#!/usr/bin/env python3
"""trace — LangSmith-compatible local trace sidecar for the Systems Thinking Studio.

Stdlib only. Writes JSONL where each line is one completed run record whose
field names and shapes mirror the LangSmith run schema (`POST /runs` body):
id / name / run_type / trace_id / parent_run_id / dotted_order / start_time /
end_time / inputs / outputs / error / extra / token_usage / model / tags.
A future exporter with LANGSMITH_API_KEY can therefore ingest the file
unchanged; until then it is a local, greppable audit trail. Schema contract:
`processes/deep-agent/trace-schema.md`.

Two ways to use it:
  1. Python (deep-agent runner):  TraceWriter(...)  with phase()/step()/llm_call().
  2. Anywhere else (incl. harness/systems-studio.sh phases): the emit_trace()
     helper or its CLI wrapper:
       python3 trace.py emit --trace <dir>/trace.jsonl --name "phase-03-diagnose" \
         --run-type chain --input-file <dir>/diagnosis.md --note "GREEN attempt 1"
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

SCHEMA_VERSION = "1.0.0"
RUN_TYPES = ("chain", "llm", "tool", "retrieval", "embedding", "prompt")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _dotted_component(dt: datetime, run_id: str) -> str:
    return dt.strftime("%Y%m%dT%H%M%S%fZ") + "-" + run_id


def _load_existing_root(path: Path) -> dict | None:
    """Return the first (root) run record in a trace file, if any."""
    if not path.is_file():
        return None
    with path.open(errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(rec, dict) and rec.get("id"):
                    return rec
    return None


def _write_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def _record(
    *,
    name: str,
    run_type: str,
    trace_id: str,
    parent_run_id: str | None,
    start_time: datetime,
    end_time: datetime,
    inputs: Any,
    outputs: Any,
    error: str | None,
    model: str | None,
    token_usage: dict | None,
    tags: list[str] | None,
    metadata: dict | None,
    parent_dotted: str | None,
) -> dict:
    run_id = str(uuid.uuid4())
    dotted = (_dotted_component(start_time, run_id)
              if parent_dotted is None
              else parent_dotted + "." + _dotted_component(start_time, run_id))
    rec: dict[str, Any] = {
        "id": run_id,
        "name": name,
        "run_type": run_type,
        "trace_id": trace_id,
        "parent_run_id": parent_run_id,
        "dotted_order": dotted,
        "start_time": _iso(start_time),
        "end_time": _iso(end_time),
        "inputs": inputs,
        "outputs": outputs,
        "error": error,
        "tags": tags or [],
        "extra": {
            "metadata": {**(metadata or {}), "trace_schema_version": SCHEMA_VERSION},
            "session_name": trace_id,
        },
    }
    if run_type == "llm":
        rec["model"] = model or "unknown"
        rec["extra"]["invocation_params"] = {"model": model or "unknown"}
        rec["token_usage"] = token_usage or {}
    return rec


def emit_trace(
    trace_path: str | Path,
    name: str,
    run_type: str = "chain",
    inputs: Any = None,
    outputs: Any = None,
    error: str | None = None,
    model: str | None = None,
    token_usage: dict | None = None,
    tags: list[str] | None = None,
    metadata: dict | None = None,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
) -> str:
    """Append ONE completed run record; attach to an existing root if present.

    This is the documented adapter any harness phase (systems-studio.sh,
    future studios) calls — from Python directly or via the CLI below.
    Returns the new run id.
    """
    path = Path(trace_path)
    root = _load_existing_root(path)
    trace_id = root["id"] if root else str(uuid.uuid4())
    parent_dotted = root.get("dotted_order") if root else None
    end = end_time or _now()
    start = start_time or end
    rec = _record(
        name=name, run_type=run_type, trace_id=trace_id,
        parent_run_id=None, start_time=start, end_time=end,
        inputs=inputs, outputs=outputs, error=error, model=model,
        token_usage=token_usage, tags=tags, metadata=metadata,
        parent_dotted=parent_dotted,
    )
    _write_record(path, rec)
    return rec["id"]


class TraceWriter:
    """Hierarchical writer for the deep-agent runner: root -> phases -> steps/llm_calls."""

    def __init__(self, path: str | Path, session_name: str, metadata: dict | None = None):
        self.path = Path(path)
        self.session_name = session_name
        self._stack: list[dict] = []  # open runs: {id, dotted, start}
        self.root_id: str | None = None
        self._root_start: datetime | None = None
        self._root_meta = metadata or {}

    # -- root -------------------------------------------------------------
    def start(self) -> str:
        assert not self._stack and self.root_id is None, "root already started"
        self.root_id = str(uuid.uuid4())
        self._root_start = _now()
        self._stack.append({
            "id": self.root_id,
            "dotted": _dotted_component(self._root_start, self.root_id),
            "start": self._root_start,
            "name": self.session_name,
            "run_type": "chain",
        })
        return self.root_id

    def finish(self, outputs: Any = None, error: str | None = None) -> None:
        frame = self._stack.pop()
        rec = _record(
            name=frame["name"], run_type=frame["run_type"], trace_id=self.root_id,
            parent_run_id=None, start_time=frame["start"], end_time=_now(),
            inputs=frame.get("inputs"), outputs=outputs, error=error,
            model=None, token_usage=None, tags=frame.get("tags"),
            metadata={**self._root_meta, **(frame.get("metadata") or {})},
            parent_dotted=None,
        )
        # the root record keeps the id announced to every child as trace_id
        rec["id"] = self.root_id
        # root keeps its own dotted component (no parent)
        rec["dotted_order"] = frame["dotted"]
        _write_record(self.path, rec)

    # -- nested runs --------------------------------------------------------
    @contextmanager
    def span(
        self,
        name: str,
        run_type: str = "chain",
        inputs: Any = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
    ) -> Iterator[dict]:
        """Open a phase (chain) or step (tool) under the current parent."""
        if run_type not in RUN_TYPES:
            raise ValueError(f"run_type must be one of {RUN_TYPES}")
        parent = self._stack[-1]
        start = _now()
        run_id = str(uuid.uuid4())
        frame = {
            "id": run_id,
            "dotted": parent["dotted"] + "." + _dotted_component(start, run_id),
            "start": start,
            "name": name,
            "run_type": run_type,
            "inputs": inputs,
            "tags": tags,
            "metadata": metadata,
        }
        self._stack.append(frame)
        try:
            yield frame
        except Exception as exc:  # noqa: BLE001 — record, then re-raise
            self._close(outputs=None, error=f"{type(exc).__name__}: {exc}")
            raise
        else:
            self._close(outputs=frame.get("pending_outputs"), error=None)

    def phase(self, name: str, inputs: Any = None, **kw: Any) -> Any:
        """Alias kept for readability: a phase is a chain-run span."""
        return self.span(name, run_type="chain", inputs=inputs, **kw)

    def step(self, name: str, inputs: Any = None, **kw: Any) -> Any:
        """A deterministic step is a tool-run span."""
        return self.span(name, run_type="tool", inputs=inputs, **kw)

    def set_outputs(self, outputs: Any) -> None:
        """Set outputs on the innermost open span before it closes."""
        self._stack[-1]["pending_outputs"] = outputs

    def _close(self, outputs: Any, error: str | None) -> None:
        frame = self._stack.pop()
        parent = self._stack[-1]
        rec = _record(
            name=frame["name"], run_type=frame["run_type"], trace_id=self.root_id,
            parent_run_id=parent["id"], start_time=frame["start"], end_time=_now(),
            inputs=frame.get("inputs"), outputs=outputs, error=error,
            model=None, token_usage=None, tags=frame.get("tags"),
            metadata={**self._root_meta, **(frame.get("metadata") or {})},
            parent_dotted=parent["dotted"],
        )
        _write_record(self.path, rec)

    # -- llm calls ----------------------------------------------------------
    def llm_call(
        self,
        name: str,
        model: str,
        messages: list[dict],
        output_text: str,
        usage: dict | None = None,
        error: str | None = None,
        parent: dict | None = None,
        start_time: datetime | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Record one completed LLM call as an llm-run under the current (or given) span."""
        p = parent or self._stack[-1]
        start = start_time or _now()
        end = _now()
        run_id = str(uuid.uuid4())
        pt = p["dotted"] + "." + _dotted_component(start, run_id)
        tu = usage or {}
        rec = {
            "id": run_id,
            "name": name,
            "run_type": "llm",
            "trace_id": self.root_id,
            "parent_run_id": p["id"],
            "dotted_order": pt,
            "start_time": _iso(start),
            "end_time": _iso(end),
            "inputs": {"messages": messages},
            "outputs": {"generations": [{"text": output_text}] if not error else None,
                        "output_text": output_text or ""},
            "error": error,
            "model": model,
            "token_usage": {
                "input": tu.get("prompt_tokens", 0),
                "output": tu.get("completion_tokens", 0),
                "total": tu.get("total_tokens", 0),
                "prompt_tokens": tu.get("prompt_tokens", 0),
                "completion_tokens": tu.get("completion_tokens", 0),
                "total_tokens": tu.get("total_tokens", 0),
            },
            "tags": tags or [],
            "extra": {
                "invocation_params": {"model": model},
                "metadata": {"session_name": self.session_name,
                             "trace_schema_version": SCHEMA_VERSION},
            },
        }
        _write_record(self.path, rec)
        return run_id


# --------------------------------------------------------------------------
# CLI adapter — lets bash harness phases emit the same trace format verbatim.
# --------------------------------------------------------------------------
def _cli() -> int:
    p = argparse.ArgumentParser(description="Emit one run record to a trace sidecar.")
    sub = p.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("emit", help="append one completed run record")
    e.add_argument("--trace", required=True, help="trace.jsonl path")
    e.add_argument("--name", required=True)
    e.add_argument("--run-type", default="chain", choices=RUN_TYPES)
    e.add_argument("--input-file", help="path whose contents become inputs.content")
    e.add_argument("--output-file", help="path whose contents become outputs.content")
    e.add_argument("--note", help="free-text note stored in extra.metadata.note")
    e.add_argument("--error", help="error message, if the step failed")
    e.add_argument("--tags", default="", help="comma-separated tags")
    args = p.parse_args()

    def slurp(fp: str | None) -> Any:
        if not fp:
            return None
        f = Path(fp)
        return f.read_text(errors="replace")[:20000] if f.is_file() else f"(missing: {fp})"

    run_id = emit_trace(
        args.trace, args.name, run_type=args.run_type,
        inputs={"content": slurp(args.input_file)},
        outputs={"content": slurp(args.output_file)},
        error=args.error,
        tags=[t for t in args.tags.split(",") if t],
        metadata={"note": args.note} if args.note else None,
    )
    print(f"[trace] emitted {args.name} run_id={run_id} -> {args.trace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
