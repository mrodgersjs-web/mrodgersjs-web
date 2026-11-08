#!/usr/bin/env python3
"""Fetch ALL Recall KB cards despite the undocumented 500-per-response cap.

The /api/v1/cards endpoint ignores limit/offset/page/cursor, but honors the
documented date_from/date_to filters. Strategy: recursive date-window
bisection with MICROSECOND boundaries (second-granularity boundaries drop
cards that share a timestamp). Any window returning >=500 cards is split at
its midpoint; results are deduped by card id.

Writes knowledge/recall/raw/all-cards.json and prints coverage vs total_count.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE = "https://backend.getrecall.ai/api/v1/cards"
CAP = 500
OUT = Path("knowledge/recall/raw/all-cards.json")


def load_key() -> str:
    key = os.environ.get("RECALL_API_KEY", "")
    if not key:
        env = Path.home() / ".hermes" / ".env"
        for line in env.read_text().splitlines():
            if line.startswith("RECALL_API_KEY="):
                key = line.split("=", 1)[1].strip()
    if not key:
        sys.exit("no RECALL_API_KEY")
    return key


KEY = load_key()


def fetch(date_from: str | None, date_to: str | None) -> dict:
    params = {}
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    url = BASE + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {KEY}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def fmt(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def main() -> None:
    first = fetch(None, None)
    total = first["total_count"]
    seen: dict[str, dict] = {c["id"]: c for c in first["results"]}
    print(f"total_count={total} first_window={len(first['results'])}")

    lo = min(parse(c["created_at"]) for c in first["results"])
    queue: list[tuple[str | None, str | None]] = [(None, fmt(lo - timedelta(microseconds=1)))]
    guard = 0
    while queue and len(seen) < total and guard < 300:
        guard += 1
        date_from, date_to = queue.pop(0)
        page = fetch(date_from, date_to)
        rows = page.get("results", [])
        new = [c for c in rows if c["id"] not in seen]
        for c in new:
            seen[c["id"]] = c
        print(f"window {date_from or '…'}→{date_to or '…'}: {len(rows)} rows, {len(new)} new (seen {len(seen)}/{total})")
        if len(rows) >= CAP and new:
            # Dense window: bisect at midpoint between its own bounds.
            w_lo = min(parse(c["created_at"]) for c in rows)
            w_hi = max(parse(c["created_at"]) for c in rows)
            mid = w_lo + (w_hi - w_lo) / 2
            queue.append((date_from, fmt(mid)))
            queue.append((fmt(mid + timedelta(microseconds=1)), date_to))
        elif new:
            w_lo = min(parse(c["created_at"]) for c in new)
            queue.append((date_from, fmt(w_lo - timedelta(microseconds=1))))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cards = sorted(seen.values(), key=lambda c: c["created_at"], reverse=True)
    OUT.write_text(json.dumps({"total_count": total, "fetched": len(cards), "results": cards}, indent=1))
    print(f"wrote {OUT}: {len(cards)}/{total}")
    if len(seen) < total:
        sys.exit(f"MISSING {total - len(seen)} cards — rerun or widen bisection")


if __name__ == "__main__":
    main()
