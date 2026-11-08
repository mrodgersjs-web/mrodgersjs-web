#!/usr/bin/env python3
"""Turn the 5GB raw lake into citation-bound, staged systems mechanisms.

Selection is deterministic; synthesis is local Ollama with JSON mode. Outputs are
STAGED_NOT_PROMOTED until the campaign gate is green and the exact Jake diff is approved.
"""
from __future__ import annotations

import argparse
import hashlib
import fcntl
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile
import urllib.request

from pypdf import PdfReader

DEFAULT_ROOT = Path.home() / ".rig/omniscout-campaigns/systems-thinking-5gb-20260829"
DEFAULT_LATTICE = DEFAULT_ROOT / "lattice.json"
OLLAMA = "http://127.0.0.1:11434/api/generate"


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def pdf_text(path: Path, limit: int = 35_000) -> str:
    reader = PdfReader(str(path))
    chunks: list[str] = []
    used = 0
    for page in reader.pages[:20]:
        text = page.extract_text() or ""
        chunks.append(text)
        used += len(text)
        if used >= limit:
            break
    return "\n".join(chunks)[:limit]


def flatten_hn(node: object, out: list[str]) -> None:
    if not isinstance(node, dict):
        return
    for key in ("title", "text"):
        value = node.get(key)
        if value:
            out.append(re.sub(r"<[^>]+>", " ", str(value)))
    for child in node.get("children") or []:
        flatten_hn(child, out)


def json_text(path: Path, source_class: str, limit: int = 35_000) -> str:
    value = json.loads(path.read_text(errors="replace"))
    if source_class == "youtube":
        return str(value.get("transcript") or value.get("metadata", {}).get("description") or "")[:limit]
    rows: list[str] = []
    flatten_hn(value, rows)
    return "\n".join(rows)[:limit]


def source_rows(conn: sqlite3.Connection, topic: str, per_class: int) -> list[sqlite3.Row]:
    rows: list[sqlite3.Row] = []
    for source_class in ("paper", "hn", "youtube"):
        rows.extend(conn.execute(
            """SELECT * FROM items WHERE state='done' AND topic=? AND source_class=?
               ORDER BY bytes DESC, id LIMIT ?""", (topic, source_class, per_class)
        ).fetchall())
    return rows


def evidence(row: sqlite3.Row) -> dict | None:
    path = Path(row["artifact_path"])
    try:
        text = pdf_text(path) if row["source_class"] == "paper" else json_text(path, row["source_class"])
    except Exception:
        return None
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 400:
        return None
    return {
        "sha256": row["sha256"],
        "title": row["title"],
        "source_url": row["url"],
        "source_class": row["source_class"],
        "excerpt": text[:12_000],
    }


def synthesize(topic: dict, sources: list[dict], model: str) -> dict:
    compact = [{**source, "excerpt": source["excerpt"][:6_000]} for source in sources]
    prompt = f"""You are RIG's systems-mechanism analyst. Use ONLY the evidence objects below.
Return strict JSON with this schema:
{{
  "mechanism_name":"specific reusable mechanism",
  "system_boundary":"what is in/out",
  "stocks":[{{"name":"...","inflows":["..."],"outflows":["..."]}}],
  "feedback_loops":[{{"name":"...","polarity":"reinforcing|balancing","mechanism":"...","delay":"..."}}],
  "systems_archetypes":["..."],
  "leverage_points":[{{"rank":1,"intervention":"...","why":"..."}}],
  "failure_modes":[{{"mode":"...","early_signal":"...","gate":"..."}}],
  "rig_process_changes":[{{"process":"...","change":"...","done_test":"..."}}],
  "falsification_tests":["..."],
  "confidence":0.0,
  "citation_sha256":["full hashes copied from evidence"]
}}
Topic question: {topic['question']}
Allowed RIG process names (copy EXACTLY into rig_process_changes[].process):
{json.dumps(topic['rig_processes'])}
Evidence: {json.dumps(compact, ensure_ascii=False)}
No evidence means no claim. Every proposed RIG change must target one allowed process name.
Name causal mechanisms, delays, and failure signals; avoid slogans and source-domain detours."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "think": False,
        "options": {"temperature": 0, "num_ctx": 16_384, "num_predict": 1_000},
    }
    request = urllib.request.Request(
        OLLAMA, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        outer = json.load(response)
    return json.loads(outer["response"])

def normalize_card(card: dict) -> dict:
    """Repair the known local-model spelling drift before strict validation."""
    if "citation_sha256" in card or "citation_sha25" not in card:
        return card
    normalized = dict(card)
    normalized["citation_sha256"] = normalized.pop("citation_sha25")
    return normalized



def gate_card(card: dict, sources: list[dict], allowed_processes: list[str]) -> dict:
    available = {source["sha256"] for source in sources}
    cited = set(card.get("citation_sha256") or [])
    classes = {source["source_class"] for source in sources}
    changes = card.get("rig_process_changes") or []
    checks = {
        "three_sources": len(sources) >= 3,
        "two_source_classes": len(classes) >= 2,
        "citations_exist": bool(cited) and cited <= available,
        "feedback_loop": bool(card.get("feedback_loops")),
        "leverage_point": bool(card.get("leverage_points")),
        "rig_process_change": bool(changes),
        "rig_process_alignment": bool(changes)
        and all(change.get("process") in allowed_processes for change in changes),
        "falsification_test": bool(card.get("falsification_tests")),
    }
    return {"ok": all(checks.values()), "checks": checks}


def acquire_distill_lock(root: Path):
    lock_path = root / "l2" / ".distill.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock = lock_path.open("w", encoding="utf-8")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        raise RuntimeError("another systems-thinking distillation owns the L2 writer lock")
    lock.write(f"pid={os.getpid()}\n")
    lock.flush()
    return lock


def run(root: Path, lattice_path: Path, model: str, per_class: int, topic_limit: int | None) -> dict:
    lock = acquire_distill_lock(root)
    try:
        return run_unlocked(root, lattice_path, model, per_class, topic_limit)
    finally:
        lock.close()


def run_unlocked(root: Path, lattice_path: Path, model: str, per_class: int, topic_limit: int | None) -> dict:
    lattice = json.loads(lattice_path.read_text())
    conn = sqlite3.connect(root / "campaign.sqlite"); conn.row_factory = sqlite3.Row
    out = root / "l2"; out.mkdir(parents=True, exist_ok=True)
    results: list[dict] = []
    topics = lattice["topics"][:topic_limit] if topic_limit else lattice["topics"]
    for topic in topics:
        sources = [
            item
            for row in source_rows(conn, topic["id"], per_class)
            if (item := evidence(row))
        ]
        classes = {source["source_class"] for source in sources}
        if len(sources) < 3 or len(classes) < 2:
            results.append(
                {
                    "topic": topic["id"],
                    "status": "NOT_READY",
                    "source_count": len(sources),
                    "source_classes": sorted(classes),
                }
            )
            continue
        card = normalize_card(synthesize(topic, sources, model))
        gate = gate_card(card, sources, topic["rig_processes"])
        value = {
            "schema": "rig.omniscout.systems-mechanism-card.v1", "topic": topic["id"],
            "question": topic["question"], "rig_processes": topic["rig_processes"],
            "sources": [{k: v for k, v in source.items() if k != "excerpt"} for source in sources],
            "synthesis": card, "gate": gate, "authority_state": "STAGED_NOT_PROMOTED",
        }
        value["card_sha256"] = stable_hash(value)
        atomic_json(out / f"{topic['id']}.json", value)
        results.append({"topic": topic["id"], "status": "PASS" if gate["ok"] else "QUARANTINED",
                        "source_count": len(sources), "source_classes": sorted({x["source_class"] for x in sources}),
                        "card_sha256": value["card_sha256"]})
    summary = {"schema": "rig.omniscout.systems-distillation.v1", "model": model,
               "authority_state": "STAGED_NOT_PROMOTED", "results": results,
               "pass": sum(x["status"] == "PASS" for x in results),
               "quarantined": sum(x["status"] == "QUARANTINED" for x in results),
               "not_ready": sum(x["status"] == "NOT_READY" for x in results)}
    summary["summary_sha256"] = stable_hash(summary)
    atomic_json(out / "SYNTHESIS.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--lattice", type=Path, default=DEFAULT_LATTICE)
    parser.add_argument("--model", default="qwen3.8:27b")
    parser.add_argument("--per-class", type=int, default=2)
    parser.add_argument("--topic-limit", type=int)
    args = parser.parse_args()
    result = run(args.root, args.lattice, args.model, args.per_class, args.topic_limit)
    return 0 if result["pass"] > 0 and result["quarantined"] == 0 else 4


if __name__ == "__main__":
    raise SystemExit(main())
