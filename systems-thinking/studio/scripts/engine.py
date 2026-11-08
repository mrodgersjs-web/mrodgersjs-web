#!/usr/bin/env python3
"""Deterministic engine for the Systems Thinking Studio.

Pure functions. No I/O except reading PKG data/knowledge. studio.py prints.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
DATA = PKG / "data"
KNOW = PKG / "knowledge"
STOP = {
    "the", "and", "for", "that", "with", "this", "from", "into", "your",
    "what", "when", "than", "then", "them", "they", "have", "been", "will",
    "are", "was", "were", "but", "not", "you", "our", "out", "any", "all",
}


def load(name: str):
    return json.loads((DATA / name).read_text())


def tokens(text: str) -> set[str]:
    raw = [w for w in re.findall(r"[a-z]{4,}", text.lower()) if w not in STOP]
    out = set()
    for w in raw:
        out.add(w)
        if w.endswith("ies") and len(w) > 5:
            out.add(w[:-3] + "y")
        elif w.endswith("s") and len(w) > 4:
            out.add(w[:-1])
    return out


def _content_words(phrase: str) -> list[str]:
    return [w for w in phrase.lower().split() if len(w) >= 4]


def score_map(text: str) -> list[dict]:
    t = text.lower()
    tset = tokens(text)
    scored = []
    for a in load("archetypes.json")["archetypes"]:
        hits = []
        for s in a["symptoms"]:
            sl = s.lower()
            if sl in t:
                hits.append(s)
                continue
            ww = _content_words(sl)
            if ww and all(w in tset or w in t for w in ww):
                hits.append(s)
        if hits:
            scored.append({
                "id": a["id"],
                "name": a["name"],
                "hits": hits,
                "n": len(hits),
                "diagnosis": a["diagnosis"],
                "intervention": a["intervention"],
                "counterintuitive": a["counterintuitive"],
            })
    scored.sort(key=lambda x: -x["n"])
    for i, row in enumerate(scored):
        row["confidence"] = "likely" if i == 0 and row["n"] >= 2 else "possible"
    return scored


def score_crosspoll(text: str, min_keep: float = 0.60) -> dict:
    """Transfer = structural_similarity × mechanism_clarity × testability."""
    d = load("polymath-domains.json")
    tset = tokens(text)
    structure = tset | tokens(
        "loop delay stock flow constraint volume reply cap goal feedback "
        "balance reinforce rate queue signal error load measure schedule"
    )
    kept, rejected, domains = [], [], set()
    for dom in d["domains"]:
        for mech in dom["mechanisms"]:
            name, _, source = mech.partition("->")
            mset = tokens(name) | tokens(source)
            overlap = len(mset & structure)
            structural = min(1.0, 0.42 + 0.30 * overlap)
            clarity = 1.0 if "->" in mech and len(source.strip()) > 20 else 0.3
            measurable = bool(mset & tokens(
                "rate count delay stock signal measure schedule goal error load cap queue"
            ))
            testability = 1.0 if measurable else 0.4
            product = round(structural * clarity * testability, 3)
            row = {
                "domain": dom["id"],
                "mechanism": mech,
                "structural": round(structural, 3),
                "clarity": clarity,
                "testability": testability,
                "score": product,
            }
            if product >= min_keep:
                kept.append(row)
                domains.add(dom["id"])
            else:
                rejected.append(row)
    kept.sort(key=lambda x: -x["score"])
    rejected.sort(key=lambda x: -x["score"])
    return {
        "kept": kept[:8],
        "rejected": rejected[:8],
        "n_domains": len(domains),
        "n_kept": len(kept),
        "ok": len(kept) >= 3 and len(domains) >= 3,
    }


def retrieve_knowledge(text: str, k: int = 5) -> dict:
    q = tokens(text)
    hits = []
    for folder, kind in (("papers", "Paper"), ("youtube", "YT"), ("books", "Book")):
        d = KNOW / folder
        if not d.is_dir():
            continue
        for p in d.glob("*.md"):
            if p.name == "manifest.md":
                continue
            body = p.read_text(errors="replace")
            title = next((ln[2:].strip() for ln in body.splitlines() if ln.startswith("# ")), p.stem)
            src = ""
            for ln in body.splitlines()[:12]:
                if ln.startswith("source:"):
                    src = ln.split(":", 1)[1].strip()
            overlap = len(q & tokens(body[:4000]))
            if overlap:
                hits.append({
                    "kind": kind,
                    "title": title[:140],
                    "path": str(p.relative_to(PKG)),
                    "source": src,
                    "overlap": overlap,
                })
    hits.sort(key=lambda x: -x["overlap"])
    top = hits[:k]
    return {"hits": top, "ok": len(top) >= 2, "n_scanned": len(hits)}


def _gtm_step(s: dict, p: dict) -> None:
    send = float(p["send_per_day"])
    if send > 42:
        s["deliverability"] -= 0.022
    else:
        s["deliverability"] -= 0.003
    if p.get("see_bounces"):
        if s["deliverability"] < 0.90:
            send *= 0.45
        s["deliverability"] += 0.014
    s["deliverability"] = max(0.50, min(1.0, s["deliverability"]))
    replies = send * 0.03 * (s["deliverability"] ** 4)
    meetings = s["replies"] * 0.08
    s["sendable"] = max(0.0, s["sendable"] - send)
    s["replies"] += replies
    s["meetings"] += meetings


def _linkedin_step(s: dict, p: dict) -> None:
    posts = p["posts_per_week"] / 7
    cadence = 5.0 / 7.0
    s["published"] += posts
    s["unanswered"] += posts * (8 if not p.get("comment_sla") else 0.3)
    s["unanswered"] = max(0.0, s["unanswered"] - (5 if p.get("comment_sla") else 0.05))
    reach = 1.0 / (1.0 + 0.45 * s["unanswered"])
    counted = posts if p.get("comment_sla") else min(posts, cadence)
    s["inbound"] += counted * 0.22 * reach


def _sales_step(s: dict, p: dict) -> None:
    new = 0.4 * p.get("new_opps", 1.0)
    s["opps"] += new
    close = 0.05 if p.get("next_step_visible") else 0.01
    if p.get("discount"):
        close *= 1.4
        s["opps"] *= 0.99
    moved = min(s["proposals"], s["proposals"] * close)
    s["signed"] += moved
    s["proposals"] = max(0, s["proposals"] - moved + 0.2)
    s["stuck"] += 0.15 if not p.get("next_step_visible") else -0.2
    s["stuck"] = max(0, s["stuck"])


def _founder_step(s: dict, p: dict) -> None:
    starts = p["new_starts"]
    if p.get("pushback") and s["open_loops"] > 25:
        starts = 0
    s["open_loops"] += starts - (0.4 if p.get("pushback") else 0.1)
    s["aops_min"] += starts * 12
    s["energy"] = max(0.2, min(1.0, s["energy"] - 0.02 * starts + (0.03 if p.get("pushback") else 0)))
    s["deals"] += 0.04 * s["energy"] if p.get("pushback") else 0.005


STEP = {
    "gtm": _gtm_step,
    "linkedin": _linkedin_step,
    "sales": _sales_step,
    "founder": _founder_step,
    "mike-os": _founder_step,
}


def simulate(domain: str, scenario: str | None = None) -> dict:
    models = load("stock-flow-models.json")
    if domain not in models["domains"]:
        return {"ok": False, "error": f"no model for {domain}"}
    spec = models["domains"][domain]
    dt = models["dt_days"]
    horizon = models["horizon_days"]
    names = list(spec["scenarios"]) if scenario is None else [scenario]
    out = {"domain": domain, "dt": dt, "horizon": horizon, "note": spec["note"], "runs": {}}
    step = STEP[domain]
    health = {
        "gtm": "meetings",
        "linkedin": "inbound",
        "sales": "signed",
        "founder": "deals",
        "mike-os": "deals",
    }[domain]
    for sc in names:
        s = {k: float(v) for k, v in spec["stocks"].items()}
        params = spec["scenarios"][sc]
        series = [{**s, "t": 0}]
        for t in range(1, horizon + 1):
            step(s, params)
            series.append({k: round(v, 3) if isinstance(v, float) else v for k, v in s.items()} | {"t": t})
        out["runs"][sc] = {
            "final": series[-1],
            "start": series[0],
            "health_start": series[0][health],
            "health_end": series[-1][health],
            "health": health,
        }
    base = out["runs"].get("baseline", {})
    vol = out["runs"].get("volume_plus_40", {})
    info = out["runs"].get("rank6_information", {})
    trap = bool(vol) and bool(base) and vol["health_end"] <= base["health_end"] + 1e-9
    info_wins = bool(info) and bool(vol) and info["health_end"] > vol["health_end"]
    out["trap"] = trap
    out["rank6_beats_volume"] = info_wins
    out["ok"] = True
    return out
