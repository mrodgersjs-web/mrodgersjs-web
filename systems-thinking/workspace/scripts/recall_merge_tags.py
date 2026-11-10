#!/usr/bin/env python3
"""Merge + verify swarm tagging output for the Recall card inventory.

Contract:
- Input : knowledge/recall/raw/all-cards.json (ground truth, 853 cards)
- Inputs: knowledge/recall/tags/batch-*.out.jsonl — one line per card,
          same ids as the matching input batch, {"id","tags":[...],"reason"}
- Output: knowledge/recall/card-index.json      — id -> {title, source_url, tags, mirror_path?}
          knowledge/recall/by-domain/<tag>.json — card lists per tag

Hard verification (exit 1 on any failure):
- every input batch file has a matching .out file
- union of output ids == set of inventory ids, no duplicates
- 1..3 tags per card, all tags from the fixed vocabulary
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

VOCAB = {
    # core domains (Mike's named set)
    "systems-thinking", "psychology", "startup", "founder", "growth",
    "linkedin", "sales", "gtm", "tools",
    # extensions to keep 'other' small
    "ai-agents", "marketing", "content", "productivity", "strategy",
    "engineering", "finance", "other",
}
INV = Path("knowledge/recall/raw/all-cards.json")
TAGS = Path("knowledge/recall/tags")
BY_DOMAIN = Path("knowledge/recall/by-domain")


def main() -> None:
    inv = json.loads(INV.read_text())
    inventory = {c["id"]: c for c in inv["results"]}
    problems: list[str] = []

    inputs = sorted(TAGS.glob("input/batch-*.jsonl"))
    outputs = sorted(TAGS.glob("batch-*.out.jsonl"))
    if len(inputs) != len(outputs):
        problems.append(f"batch count mismatch: {len(inputs)} inputs vs {len(outputs)} outputs")

    tagged: dict[str, list[str]] = {}
    for inp in inputs:
        out = TAGS / inp.name.replace("input/", "").replace(".jsonl", ".out.jsonl")
        if not out.is_file():
            problems.append(f"missing output for {inp.name}")
            continue
        in_ids = [json.loads(l)["id"] for l in inp.read_text().splitlines() if l.strip()]
        out_lines = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
        out_ids = [r.get("id") for r in out_lines]
        if in_ids != out_ids:
            problems.append(f"{out.name}: id set/order differs from {inp.name}")
        for r in out_lines:
            cid = r.get("id")
            tags = r.get("tags")
            if cid in tagged:
                problems.append(f"{out.name}: duplicate id {cid}")
            if not isinstance(tags, list) or not (1 <= len(tags) <= 3):
                problems.append(f"{cid}: tags must be a list of 1-3, got {tags!r}")
                continue
            bad = [t for t in tags if t not in VOCAB]
            if bad:
                problems.append(f"{cid}: unknown tags {bad}")
            tagged[cid] = tags

    missing = set(inventory) - set(tagged)
    extra = set(tagged) - set(inventory)
    if missing:
        problems.append(f"{len(missing)} inventory ids never tagged (e.g. {list(missing)[:3]})")
    if extra:
        problems.append(f"{len(extra)} tagged ids not in inventory")

    if problems:
        print("VERIFY FAILED:")
        for p in problems:
            print(" -", p)
        sys.exit(1)

    join = {}
    mj = Path("knowledge/recall/raw/mirror-join.json")
    if mj.is_file():
        join = json.loads(mj.read_text())

    index = {
        c["id"]: {
            "title": c.get("title", ""),
            "source_url": c.get("source_url", ""),
            "created_at": c.get("created_at", ""),
            "tags": tagged[c["id"]],
            **({"mirror_path": join[c["id"]]} if c["id"] in join else {}),
        }
        for c in inv["results"]
    }
    Path("knowledge/recall/card-index.json").write_text(json.dumps(index, indent=1))

    BY_DOMAIN.mkdir(parents=True, exist_ok=True)
    counts: Counter[str] = Counter()
    for tag in VOCAB:
        cards = [
            {"id": cid, "title": m["title"], "source_url": m["source_url"],
             **({"mirror_path": m["mirror_path"]} if "mirror_path" in m else {})}
            for cid, m in index.items() if tag in m["tags"]
        ]
        counts[tag] = len(cards)
        (BY_DOMAIN / f"{tag}.json").write_text(
            json.dumps({"domain": tag, "count": len(cards), "cards": cards}, indent=1)
        )

    print(f"VERIFIED {len(tagged)}/{len(inventory)} cards tagged")
    for tag, n in counts.most_common():
        print(f"  {tag:18s} {n}")
    total_assignments = sum(counts.values())
    print(f"tag assignments: {total_assignments} ({total_assignments/len(inventory):.2f} per card)")


if __name__ == "__main__":
    main()
