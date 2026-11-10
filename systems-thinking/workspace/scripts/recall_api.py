#!/usr/bin/env python3
"""recall_api.py — stdlib-only Recall KB API client for sandboxed agents.

The frontier sandbox allowlist permits `python3` but not arbitrary binaries,
so this mirrors ~/.local/bin/recall using only the standard library.

Usage:
  python3 scripts/recall_api.py status
  python3 scripts/recall_api.py search "query" [focused|exhaustive]
  python3 scripts/recall_api.py card <card_id> [focus_query] [max_chunks]
"""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://backend.getrecall.ai/api/v1"


def key() -> str:
    k = os.environ.get("RECALL_API_KEY", "")
    if not k:
        p = Path.home() / ".hermes" / ".env"
        if p.is_file():
            for line in p.read_text().splitlines():
                if line.startswith("RECALL_API_KEY="):
                    k = line.split("=", 1)[1].strip()
    if not k:
        sys.exit("no RECALL_API_KEY")
    return k


def get(path: str, params: dict | None = None) -> dict:
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key()}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    if cmd == "status":
        d = get("/search", {"q": "test", "mode": "focused"})
        print("OK — search reachable, total_cards:", d.get("total_cards"))
    elif cmd == "search":
        q = sys.argv[2]
        mode = sys.argv[3] if len(sys.argv) > 3 else "focused"
        print(json.dumps(get("/search", {"q": q, "mode": mode})))
    elif cmd == "card":
        cid = sys.argv[2]
        params = {"max_chunks": sys.argv[4] if len(sys.argv) > 4 else "20"}
        if len(sys.argv) > 3:
            params["focus_query"] = sys.argv[3]
        print(json.dumps(get(f"/cards/{cid}", params)))
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
