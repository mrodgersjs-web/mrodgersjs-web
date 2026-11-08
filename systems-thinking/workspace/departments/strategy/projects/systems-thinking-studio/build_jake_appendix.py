#!/usr/bin/env python3
"""Build a compact, curated Jake v3 appendix from the Studio mechanism registry."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "mechanisms.json"
APPENDIX = ROOT / "JAKE_SYSTEMS_MECHANISMS_V3.md"
PROOF = ROOT / "JAKE_SYSTEMS_MECHANISMS_V3.proof.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    registry = json.loads(REGISTRY.read_text())
    cutoff = registry["source_cutoff"]
    lines = [
        "## Sourced mechanism library (Systems Thinking Studio, v3)",
        "",
        "> Curated structural/direct transfers only. Domain-specific prescriptions were excluded.",
        "> Authority remains STAGED_NOT_PROMOTED; each rule activates only through its gate.",
        "",
    ]
    for item in registry["mechanisms"]:
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"- **Transfer:** `{item['transfer']}`",
                f"- **Rule:** {item['rule']}",
                f"- **Studio change:** {item['studio_change']}",
                f"- **Prove/refute:** {item['gate']}",
                f"- **Card proof:** `{item['source_card_sha256']}`",
                "",
            ]
        )
    payload = "\n".join(lines).rstrip() + "\n"
    APPENDIX.write_text(payload)
    proof = {
        "schema": "rig.jake.curated-systems-appendix.v1",
        "ok": True,
        "cards": len(registry["mechanisms"]),
        "source_l2_pass_cards": cutoff["l2_pass_cards"],
        "source_l2_quarantined_cards": cutoff["l2_quarantined_cards"],
        "source_appendix_sha256": cutoff["appendix_sha256"],
        "registry_sha256": digest(REGISTRY.read_bytes()),
        "sha256": digest(payload.encode()),
        "authority_state": "STAGED_NOT_PROMOTED",
    }
    PROOF.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
    print(json.dumps(proof, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
