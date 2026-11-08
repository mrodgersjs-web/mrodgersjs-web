#!/usr/bin/env python3
"""Deterministic admission gate for Systems Thinking Studio mechanisms."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "mechanisms.json"
HASH = re.compile(r"^[0-9a-f]{64}$")
REQUIRED = {"id", "transfer", "source_card_sha256", "source_topic", "rule", "studio_change", "gate", "applies_to"}


def main() -> int:
    value = json.loads(REGISTRY.read_text())
    assert value["schema"] == "rig.systems-thinking-studio.mechanisms.v1"
    assert value["authority_state"] == "STAGED_NOT_PROMOTED"
    cutoff = value["source_cutoff"]
    assert cutoff["l2_pass_cards"] >= 12
    assert cutoff["l2_quarantined_cards"] == 0
    assert HASH.fullmatch(cutoff["appendix_sha256"])
    mechanisms = value["mechanisms"]
    assert len(mechanisms) >= 10
    seen: set[str] = set()
    for mechanism in mechanisms:
        assert REQUIRED <= mechanism.keys(), mechanism.get("id")
        assert mechanism["id"] not in seen
        assert mechanism["transfer"] in {"direct", "structural"}
        assert HASH.fullmatch(mechanism["source_card_sha256"])
        assert all(isinstance(mechanism[key], str) and mechanism[key].strip() for key in ("rule", "studio_change", "gate"))
        assert mechanism["applies_to"]
        seen.add(mechanism["id"])
    digest = hashlib.sha256(REGISTRY.read_bytes()).hexdigest()
    print(json.dumps({"ok": True, "mechanisms": len(mechanisms), "sha256": digest}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
