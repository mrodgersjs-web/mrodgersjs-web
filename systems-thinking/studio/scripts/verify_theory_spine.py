#!/usr/bin/env python3
"""Validate source-to-method bindings without refetching mutable web origins."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
DATA = PKG / "data"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REQUIRED_SOURCES = {
    "cynefin-snowden-boone-2007",
    "meadows-leverage-1999",
    "kim-systems-archetypes-2000",
}


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main() -> int:
    ok = True
    try:
        spine = load("theory-spine-20260830.json")
        contexts = load("decision-contexts.json")
        leverage = load("leverage-points.json")
        archetypes = load("archetypes.json")
    except (OSError, ValueError) as exc:
        print(f"FAIL theory spine parse: {exc}")
        return 1

    sources = {source.get("id"): source for source in spine.get("sources") or []}
    missing = sorted(REQUIRED_SOURCES - set(sources))
    sources_ok = not missing and all(
        source.get("url", "").startswith(("http://", "https://"))
        and SHA256.fullmatch(str(source.get("content_sha256", "")))
        and int(source.get("content_bytes") or 0) > 0
        for source in sources.values()
    )
    print(f"{'PASS' if sources_ok else 'FAIL'} theory sources count={len(sources)} missing={missing}")
    ok &= sources_ok

    contexts_ok = (
        contexts.get("schema") == "rig.systems-thinking-studio.decision-contexts.v1"
        and contexts.get("source_id") == "cynefin-snowden-boone-2007"
        and {item.get("id") for item in contexts.get("contexts") or []}
        == {"clear", "complicated", "complex", "chaotic", "disorder"}
        and all(item.get("response") and item.get("required_artifact") for item in contexts.get("contexts") or [])
    )
    print(f"{'PASS' if contexts_ok else 'FAIL'} decision contexts source-bound five-domain contract")
    ok &= contexts_ok

    leverage_ok = (
        leverage.get("source_id") == "meadows-leverage-1999"
        and [item.get("rank") for item in leverage.get("leverage_points") or []] == list(range(12, 0, -1))
    )
    print(f"{'PASS' if leverage_ok else 'FAIL'} Meadows twelve leverage ranks")
    ok &= leverage_ok

    archetypes_ok = (
        archetypes.get("source_id") == "kim-systems-archetypes-2000"
        and len(archetypes.get("archetypes") or []) >= 10
    )
    print(f"{'PASS' if archetypes_ok else 'FAIL'} archetypes source binding")
    ok &= archetypes_ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
