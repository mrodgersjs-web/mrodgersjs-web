#!/usr/bin/env python3
"""100x YouTube intel scraper for the Systems Thinking Studio.

Phase 1 ENUMERATE candidates (metadata only, fast):
  - every youtube URL in the tagged Recall corpus (all domains — polymath breadth)
  - yt-dlp ytsearch sweeps across 12 polymath domains
Phase 2 FETCH subtitles (parallel workers) -> knowledge/youtube/raw/<id>.txt
  - dedupes against existing raw files; manifest updated per video
Rerunnable: picks up where it left off. Distillation is a separate step
(studio_distill.py).

Usage: python3 studio_scrape_youtube.py [--max N] [--workers N] [--search-only]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import concurrent.futures as cf
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
RAW = PKG / "knowledge" / "youtube" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
MANIFEST = PKG / "knowledge" / "youtube" / "scrape-manifest.jsonl"
YTDLP = "/Users/rig128gb/.local/bin/yt-dlp"

DOMAIN_QUERIES = {
    "systems-thinking": [
        "systems thinking lecture", "system archetypes explained", "stocks and flows system dynamics tutorial",
        "donella meadows thinking in systems", "causal loop diagram tutorial", "feedback loops explained",
    ],
    "psychology": [
        "cognitive biases decision making", "behavioral psychology lecture", "prospect theory explained",
        "habit formation science", "motivation dopamine lecture", "psychology of persuasion",
    ],
    "physics": [
        "thermodynamics intuition lecture", "emergence complexity physics", "statistical mechanics explained",
        "network science lecture", "dynamical systems chaos tutorial", "physics thinking principles",
    ],
    "biology": [
        "evolutionary strategies explained", "ecosystems feedback loops", "ant colony swarm intelligence",
        "immune system principles", "how cells compute", "resilience in nature biology",
    ],
    "economics": [
        "complexity economics lecture", "game theory lecture", "incentive design explained",
        "market dynamics feedback", "eric beinhocker complexity economics", "institutional economics lecture",
    ],
    "mathematics": [
        "graph theory lecture", "probability for decision making", "dynamical systems mathematical intuition",
        "network mathematics explained", "bayesian reasoning tutorial", "systems of differential equations intuition",
    ],
    "engineering": [
        "control systems feedback lecture", "resilience engineering", "site reliability engineering principles",
        "systems engineering lecture", "redundancy fault tolerance explained", "infrastructure as system design",
    ],
    "philosophy": [
        "epistemology how we know lecture", "first principles thinking", "stoic decision making",
        "philosophy of science explanation", "pragmatism lecture", "mental models charlie munger",
    ],
    "strategy": [
        "systems thinking strategy business", "john boyd OODA loop", "military strategy as systems",
        "competitive dynamics strategy lecture", "asymmetric strategy explained", "deterrence and signaling",
    ],
    "learning": [
        "how to learn anything metalearning", "spaced repetition science", "deliberate practice explained",
        "building mental model lattices", "transfer of learning explained", "polymath how to think",
    ],
    "decisions": [
        "decision making under uncertainty", "ole pettersen decision science", "judgment in judgment decision making",
        "risk vs uncertainty lecture", "forecasting superforecasting lecture", "premortem decision technique",
    ],
    "complexity": [
        "complex adaptive systems lecture", " santa fe institute complexity", "emergence explained",
        "network effects explained", "scaling laws biology cities", "agent based modeling tutorial",
    ],
    "negotiation": [
        "negotiation systems thinking", "harvard negotiation principles lecture", "batna explained",
        "negotiation game theory practice", "chris voss negotiation tactics",
    ],
    "organizations": [
        "organizational design systems", "conways law explained", "team topologies lecture",
        "coordination costs scaling", "amazon two pizza teams", "functional vs divisional structure",
    ],
    "network-science": [
        "small world networks explained", "scale free networks lecture", "weak ties strength granovetter",
        "brokers and structural holes", "network diffusion models", "centrality measures explained",
    ],
    "risk-safety": [
        "normal accidents charles perrow", "high reliability organizations", "safety culture lecture",
        "black swans and heavy tails", "premortem risk analysis", "fault tree analysis tutorial",
    ],
    "statistics-causality": [
        "causal inference lecture", "correlation is not causation deep dive", "bayesian networks tutorial",
        "goodhart law explained", "simpson paradox explained", "measurement validity lecture",
    ],
    "product-growth": [
        "growth loops explained", "product market fit systems", "retention curves explained",
        "north star metric lecture", "activation funnel systems", "viral coefficient mechanics",
    ],
    "history-cases": [
        "why empires collapse systems", "industrial revolution systems analysis", "standard oil strategy analysis",
        "manhattan project organization", "apollo program systems engineering", "toyota production system deep dive",
    ],
}
SEARCH_DEPTH = 12         # results per query
MAX_DURATION_S = 3 * 3600


def run(cmd: list[str], timeout: int = 120) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout


def existing_ids() -> set[str]:
    return {p.stem for p in RAW.glob("*.txt")}


def load_manifest() -> dict[str, dict]:
    m: dict[str, dict] = {}
    if MANIFEST.is_file():
        for line in MANIFEST.read_text().splitlines():
            if line.strip():
                try:
                    r = json.loads(line)
                    m[r["id"]] = r
                except json.JSONDecodeError:
                    pass
    return m


def enumerate_corpus() -> list[dict]:
    idx = json.loads((PKG / "data" / "card-index.json").read_text())
    out = []
    for cid, meta in idx.items():
        u = meta.get("source_url", "")
        m = re.search(r"youtube\.com/watch\?v=([\w-]{6,})", u)
        if m:
            out.append({"id": m.group(1), "title": meta.get("title", ""), "channel": "",
                        "domain": meta["tags"][0] if meta.get("tags") else "systems-thinking",
                        "origin": "corpus"})
    return out


def enumerate_search() -> list[dict]:
    out = []
    for domain, queries in DOMAIN_QUERIES.items():
        for q in queries:
            try:
                raw = run([YTDLP, "-J", "--flat-playlist", "--no-warnings",
                           f"ytsearch{SEARCH_DEPTH}:{q}"], timeout=90)
                for e in json.loads(raw).get("entries", []):
                    if not e or not e.get("id"):
                        continue
                    out.append({"id": e["id"], "title": e.get("title", ""),
                                "channel": (e.get("channel") or e.get("uploader") or ""),
                                "domain": domain, "origin": f"search:{q}"})
            except Exception as ex:
                print(f"[enumerate] {domain}/{q}: {ex}", file=sys.stderr)
    return out


def vtt_to_txt(vtt: str) -> str:
    lines, seen, out = vtt.splitlines(), set(), []
    for ln in lines:
        if "-->" in ln or ln.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or ln.strip().isdigit():
            continue
        ln = re.sub(r"<[^>]+>", "", ln).strip()
        if ln and ln not in seen:
            seen.add(ln)
            out.append(ln)
    return "\n".join(out)


def fetch(cand: dict) -> dict:
    vid = cand["id"]
    rec = {**cand, "status": "pending"}
    import random
    import time
    time.sleep(random.uniform(1.0, 2.5))  # polite throttle (bot-block mitigation)
    try:
        meta = json.loads(run([YTDLP, "-J", "--no-warnings", "--cookies-from-browser", "chrome",
                               f"https://www.youtube.com/watch?v={vid}"], 90) or "{}") or {}
        if not isinstance(meta, dict):
            rec["status"] = "skip:unavailable"
            return rec
        dur = meta.get("duration") or 0
        if dur > MAX_DURATION_S:
            rec["status"] = "skip:too-long"
            return rec
        rec["channel"] = rec["channel"] or meta.get("channel") or meta.get("uploader") or ""
        rec["title"] = rec["title"] or meta.get("title") or ""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            run([YTDLP, "--skip-download", "--write-auto-subs", "--write-subs",
                 "--sub-langs", "en.*,en", "--sub-format", "vtt/srt",
                 "--cookies-from-browser", "chrome",
                 "-o", f"{td}/{vid}", f"https://www.youtube.com/watch?v={vid}"], 180)
            subs = sorted(Path(td).glob(f"{vid}*"))
            if not subs:
                rec["status"] = "skip:no-subs"
                return rec
            txt = vtt_to_txt(subs[0].read_text(errors="replace"))
            if len(txt.split()) < 120:
                rec["status"] = "skip:garbage"
                return rec
            (RAW / f"{vid}.txt").write_text(txt)
            rec["status"] = "ok"
            rec["words"] = len(txt.split())
    except Exception as ex:
        rec["status"] = f"error:{str(ex)[:60]}"
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=800)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--search-only", action="store_true")
    a = ap.parse_args()

    have = existing_ids()
    manifest = load_manifest()
    cands = [] if a.search_only else enumerate_corpus()
    cands += enumerate_search()
    uniq: dict[str, dict] = {}
    for c in cands:
        if c["id"] not in have and c["id"] not in uniq:
            uniq[c["id"]] = c
    todo = list(uniq.values())[: a.max]
    print(f"corpus+search candidates: {len(uniq)} new (existing raw: {len(have)}); fetching {len(todo)}")

    counts: dict[str, int] = {}
    with MANIFEST.open("a") as mf, cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for rec in ex.map(fetch, todo):
            counts[rec["status"].split(":")[0]] = counts.get(rec["status"].split(":")[0], 0) + 1
            mf.write(json.dumps(rec, ensure_ascii=False) + "\n")
            mf.flush()
    total_now = len(existing_ids())
    print(f"done: {counts}; raw transcripts on disk now: {total_now}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
