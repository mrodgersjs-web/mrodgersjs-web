#!/usr/bin/env python3
"""Seal a user-approved partial corpus without mislabeling it as campaign completion."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path.home() / ".rig/omniscout-campaigns/systems-thinking-5gb-20260829"


def stable_hash(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    root = ROOT
    conn = sqlite3.connect(root / "campaign.sqlite")
    conn.row_factory = sqlite3.Row
    states = {row["state"]: row["n"] for row in conn.execute("SELECT state,count(*) AS n FROM items GROUP BY state")}
    if states.get("processing", 0):
        raise RuntimeError("cannot seal partial cutoff with processing rows")
    done = conn.execute("SELECT sha256,bytes,topic,source_class FROM items WHERE state='done' ORDER BY sha256").fetchall()
    artifact_bytes = sum(int(row["bytes"]) for row in done)
    chain = hashlib.sha256("\n".join(f"{row['sha256']} {row['bytes']}" for row in done).encode()).hexdigest()
    classes = {row["source_class"]: {"items": row["n"], "bytes": row["bytes"]} for row in conn.execute("SELECT source_class,count(*) AS n,sum(bytes) AS bytes FROM items WHERE state='done' GROUP BY source_class")}
    topics = {row["topic"]: {"items": row["n"], "bytes": row["bytes"]} for row in conn.execute("SELECT topic,count(*) AS n,sum(bytes) AS bytes FROM items WHERE state='done' GROUP BY topic")}
    l2 = json.loads((root / "l2" / "SYNTHESIS.json").read_text())
    appendix = json.loads((root / "l2" / "JAKE_SYSTEMS_MECHANISMS_V3.proof.json").read_text())
    value = {
        "schema": "rig.omniscout.systems-thinking-partial-cutoff.v1",
        "campaign_id": "systems-thinking-5gb-20260829",
        "authority_state": "STAGED_NOT_PROMOTED",
        "status": "PARTIAL_CUTOFF_USER_APPROVED",
        "requested_target_bytes": 5000000000,
        "captured_artifact_bytes": artifact_bytes,
        "artifact_count": len(done),
        "artifact_chain_sha256": chain,
        "source_classes": classes,
        "topics": topics,
        "states": states,
        "l2_summary_sha256": l2["summary_sha256"],
        "l2_pass_cards": l2["pass"],
        "l2_quarantined_cards": l2["quarantined"],
        "curated_appendix_sha256": appendix["sha256"],
        "curated_mechanisms": appendix["cards"],
        "cutoff_reason": "User instructed: that is enough; analyze current corpus and bring required changes into Systems Thinking Studio.",
    }
    value["proof_sha256"] = stable_hash(value)
    output = root / "CUTOFF_PROOF.json"
    output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    print(json.dumps(value, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
