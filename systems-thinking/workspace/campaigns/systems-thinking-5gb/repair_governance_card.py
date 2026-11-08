#!/usr/bin/env python3
"""Repair one verified model schema typo without changing mechanism content."""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path.home() / ".rig/omniscout-campaigns/systems-thinking-5gb-20260829"
TOPIC = "governance-auditability"


def stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
    card_path = root / "l2" / f"{TOPIC}.json"
    synthesis_path = root / "l2" / "SYNTHESIS.json"
    card = json.loads(card_path.read_text())
    before = card["card_sha256"]
    source_hashes = [source["sha256"] for source in card["sources"]]
    synthesis = card["synthesis"]
    if "citation_sha256" in synthesis or "citation_sha25" not in synthesis:
        raise RuntimeError("expected only citation_sha25 typo")
    typo_values = synthesis["citation_sha25"]
    if not isinstance(typo_values, list) or set(typo_values) != set(source_hashes):
        raise RuntimeError("typo values do not exactly match source hashes")
    synthesis["citation_sha256"] = synthesis.pop("citation_sha25")

    distill_path = root / "distill.py"
    spec = importlib.util.spec_from_file_location("distill", distill_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    gate = module.gate_card(synthesis, card["sources"], card["rig_processes"])
    if not gate["ok"]:
        raise RuntimeError(f"repaired card remains red: {gate['checks']}")
    card["gate"] = gate
    card["schema_repair"] = {
        "kind": "model_key_typo",
        "from_key": "citation_sha25",
        "to_key": "citation_sha256",
        "before_card_sha256": before,
        "source_hashes_verified": source_hashes,
        "authority_state": "STAGED_NOT_PROMOTED",
    }
    card["card_sha256"] = stable_hash({k: v for k, v in card.items() if k != "card_sha256"})
    atomic_json(card_path, card)
    repair = {
        "schema": "rig.omniscout.l2-schema-repair.v1",
        "topic": TOPIC,
        "before_card_sha256": before,
        "after_card_sha256": card["card_sha256"],
        "gate": gate,
        "authority_state": "STAGED_NOT_PROMOTED",
    }
    atomic_json(root / "l2" / f"{TOPIC}.schema-repair.json", repair)

    summary = json.loads(synthesis_path.read_text())
    for row in summary["results"]:
        if row.get("topic") == TOPIC:
            row.update({
                "status": "PASS",
                "card_sha256": card["card_sha256"],
                "source_count": len(card["sources"]),
                "source_classes": sorted({source["source_class"] for source in card["sources"]}),
            })
    summary["pass"] = sum(row["status"] == "PASS" for row in summary["results"])
    summary["quarantined"] = sum(row["status"] == "QUARANTINED" for row in summary["results"])
    summary["not_ready"] = sum(row["status"] == "NOT_READY" for row in summary["results"])
    summary["summary_sha256"] = stable_hash({k: v for k, v in summary.items() if k != "summary_sha256"})
    atomic_json(synthesis_path, summary)
    print(json.dumps(repair, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
