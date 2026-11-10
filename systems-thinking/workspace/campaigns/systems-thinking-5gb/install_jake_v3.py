#!/usr/bin/env python3
"""Install a hash-verified OmniScout mechanism appendix into Jake's module."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

MARKERS = (
    "## Sourced mechanism library (OmniScout 36GB, v3)",
    "## Sourced mechanism library (Systems Thinking Studio, v3)",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        handle.write(data)
        tmp = Path(handle.name)
    os.replace(tmp, path)


def install(module: Path, appendix: Path, appendix_proof: Path, output_proof: Path,
            min_cards: int) -> dict:
    proof = json.loads(appendix_proof.read_text())
    appendix_bytes = appendix.read_bytes()
    if not proof.get("ok"):
        raise RuntimeError("appendix proof is red")
    if int(proof.get("cards") or 0) < min_cards:
        raise RuntimeError(f"appendix has {proof.get('cards')} cards; need {min_cards}")
    if int(proof.get("source_l2_pass_cards") or 0) < min_cards:
        raise RuntimeError(f"curated appendix source L2 floor is below {min_cards}")
    if int(proof.get("source_l2_quarantined_cards") or 0) != 0:
        raise RuntimeError("curated appendix has quarantined source L2 cards")
    if int(proof.get("source_l2_not_ready_cards") or 0) != 0:
        raise RuntimeError("curated appendix has source L2 NOT_READY cards")
    if proof.get("sha256") != digest(appendix_bytes):
        raise RuntimeError("appendix hash mismatch")
    before = module.read_text()
    backup = module.with_name(module.name + ".v2-backup-20260829")
    if not backup.exists():
        shutil.copy2(module, backup)
    prefix = before
    for marker in MARKERS:
        if marker in before:
            prefix = before.split(marker, 1)[0]
            break
    prefix = prefix.rstrip()
    prefix = re.sub(
        r"^Version:.*$",
        "Version: 3.0.0 (2026-08-30, curated Systems Thinking Studio tranche)",
        prefix,
        count=1,
        flags=re.MULTILINE,
    )
    after = prefix + "\n\n---\n\n" + appendix_bytes.decode().strip() + "\n"
    atomic_write(module, after.encode())
    result = {
        "schema": "rig.jake.systems-thinking-v3-install.v1",
        "installed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "module": str(module),
        "backup": str(backup),
        "cards": proof["cards"],
        "source_l2_pass_cards": proof.get("source_l2_pass_cards"),
        "appendix_sha256": proof["sha256"],
        "before_sha256": digest(before.encode()),
        "after_sha256": digest(after.encode()),
        "authority_state": "STAGED_NOT_PROMOTED",
    }
    atomic_write(output_proof, (json.dumps(result, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=Path, default=Path.home() / ".jake/JAKE_SYSTEMS_THINKING.md")
    parser.add_argument("--appendix", type=Path, required=True)
    parser.add_argument("--appendix-proof", type=Path, required=True)
    parser.add_argument("--output-proof", type=Path, required=True)
    parser.add_argument("--min-cards", type=int, default=10)
    args = parser.parse_args()
    install(args.module, args.appendix, args.appendix_proof, args.output_proof, args.min_cards)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
