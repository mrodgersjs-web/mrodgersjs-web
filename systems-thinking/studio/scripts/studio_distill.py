#!/usr/bin/env python3
"""Distill raw YouTube transcripts into knowledge cards.

Input:  knowledge/youtube/raw/<id>.txt  (auto-caption text from the scraper)
        knowledge/youtube/scrape-manifest.jsonl  ({id,title,channel,domain,origin,status})
Output: knowledge/youtube/<id>.md  (one card per video)

Card contract (validated; one repair retry, then parked in undistilled/):
  frontmatter keys: source, video_id, channel, title, scraped, tags (tags incl domain)
  sections: '# title' + '## Procedure / models distilled' (8-15 bullets,
  timestamped only if timestamps are recoverable from the text) +
  '## Failure modes named' + '## Studio relevance' (one line: phase 01-08).

Resume-safe: ids with an existing <id>.md card or listed in manifest.md are
skipped. knowledge/youtube/manifest.md gets an appended run line
(date, attempted, distilled, pending).

Usage:
  python3 studio_distill.py [--workers N] [--model ID] [--max N] [--domain D] [--dry-run]
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
KY = PKG / "knowledge" / "youtube"
RAW = KY / "raw"
UNDISTILLED = KY / "undistilled"
SCRAPE_MANIFEST = KY / "scrape-manifest.jsonl"
CARD_MANIFEST = KY / "manifest.md"

API_BASE = "http://127.0.0.1:8317/v1"
DEFAULT_CHAIN = ["claude-haiku-4-5", "claude-sonnet-4-5", "grok-4.6"]
HTTP_TIMEOUT = 90          # per request, seconds
TRANSCRIPT_BUDGET = 24_000  # chars fed to the model (head+tail halves)
PER_VIDEO_TIMEOUT = 120     # seconds per LLM generation call
RETRYABLE_HTTP = {408, 429, 500, 502, 503, 504}

PHASES = ("01 intake", "02 frame", "03 diagnose", "04 leverage",
          "05 ground", "06 synthesize", "07 verify", "08 seal")
REQUIRED_FM_KEYS = ("source", "video_id", "channel", "title", "scraped", "tags")
REQUIRED_SECTIONS = ("## Procedure / models distilled",
                     "## Failure modes named",
                     "## Studio relevance")

SYSTEM_PROMPT = (
    "You distill YouTube transcripts into knowledge cards for a systems-thinking "
    "studio. You return STRICT markdown only - no commentary, no code fences, "
    "nothing before the opening '---' or after the last section."
)


class DistillError(Exception):
    pass


# --------------------------------------------------------------------------- IO

def api_key() -> str:
    key = os.environ.get("KIMI_SUB_API_KEY", "")
    if key:
        return key
    env = Path.home() / ".hermes" / ".env"
    if env.is_file():
        for line in env.read_text().splitlines():
            if line.startswith("KIMI_SUB_API_KEY="):
                return line.split("=", 1)[1].strip()
    raise DistillError("KIMI_SUB_API_KEY not found in env or ~/.hermes/.env")


def load_scrape_meta() -> dict[str, dict]:
    meta: dict[str, dict] = {}
    if SCRAPE_MANIFEST.is_file():
        for line in SCRAPE_MANIFEST.read_text().splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                meta[rec["id"]] = rec  # last record wins (freshest status)
            except (json.JSONDecodeError, KeyError):
                continue
    return meta


def distilled_ids() -> set[str]:
    """Ids that already have a card: <id>.md files plus ids listed in manifest.md."""
    ids = {p.stem for p in KY.glob("*.md") if p.name != "manifest.md"}
    if CARD_MANIFEST.is_file():
        text = CARD_MANIFEST.read_text()
        for m in re.finditer(r"^\|\s*([\w-]{11})\s*\|", text, re.M):
            ids.add(m.group(1))
    return ids


def candidates(meta: dict[str, dict], domain: str) -> list[dict]:
    done = distilled_ids()
    out = []
    for p in sorted(RAW.glob("*.txt")):
        vid = p.stem
        if vid in done:
            continue
        rec = meta.get(vid, {})
        d = (rec.get("domain") or "systems-thinking").strip()
        if domain and d != domain:
            continue
        out.append({
            "id": vid,
            "path": p,
            "title": (rec.get("title") or f"YouTube video {vid}").strip(),
            "channel": (rec.get("channel") or "unknown").strip() or "unknown",
            "domain": d,
            "words": len(p.read_text(errors="replace").split()),
        })
    return out


def truncate(text: str, budget: int = TRANSCRIPT_BUDGET) -> str:
    if len(text) <= budget:
        return text
    half = budget // 2
    return (text[:half] + "\n\n[... middle of transcript truncated ...]\n\n"
            + text[-half:])


# ----------------------------------------------------------------------- LLM

def chat(messages: list[dict], chain: list[str], key: str) -> tuple[str, str]:
    """One completion with backoff + model fallback. Raises DistillError."""
    deadline = time.monotonic() + PER_VIDEO_TIMEOUT
    last = "no attempt made"
    attempt = 0
    while time.monotonic() < deadline:
        model = chain[min(attempt, len(chain) - 1)]
        payload = {"model": model, "messages": messages,
                   "max_tokens": 4000}
        req = urllib.request.Request(
            API_BASE + "/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {key}"})
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
            content = data["choices"][0]["message"]["content"]
            if not content or not content.strip():
                raise ValueError("empty completion")
            return content.strip(), model
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:200]
            except Exception:
                pass
            last = f"HTTP {e.code} model={model} {body}".strip()
            if e.code not in RETRYABLE_HTTP:
                raise DistillError(last)
        except (urllib.error.URLError, TimeoutError, socket.timeout,
                ValueError, json.JSONDecodeError, KeyError, IndexError) as e:
            last = f"{type(e).__name__}: {e} model={model}"
        attempt += 1
        if attempt >= len(chain) + 3:
            break
        time.sleep(min(1.5 ** attempt, 10))
    raise DistillError(last)


# ------------------------------------------------------------------ validation

def strip_fences(md: str) -> str:
    md = md.strip()
    if md.startswith("```"):
        md = re.sub(r"^```[a-zA-Z]*\n", "", md)
        md = re.sub(r"\n```\s*$", "", md)
    return md.strip()


def validate(md: str, cand: dict) -> list[str]:
    """Return a list of contract violations (empty list = valid card)."""
    errs: list[str] = []
    vid = cand["id"]
    md = strip_fences(md)
    if not md.startswith("---"):
        return ["output must open with a '---' frontmatter fence"]
    parts = md.split("---", 2)
    if len(parts) < 3:
        return ["frontmatter fence not closed"]
    fm = {}
    for line in parts[1].strip().splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.+)$", line.strip())
        if m:
            fm[m.group(1)] = m.group(2).strip()
    for k in REQUIRED_FM_KEYS:
        if not fm.get(k):
            errs.append(f"missing frontmatter key: {k}")
    if fm.get("video_id") and fm["video_id"] != vid:
        errs.append(f"video_id {fm['video_id']!r} != {vid!r}")
    if fm.get("source") and vid not in fm["source"]:
        errs.append(f"source does not contain video id {vid}")
    if fm.get("tags") and cand["domain"].lower() not in fm["tags"].lower():
        errs.append(f"tags should include domain {cand['domain']!r}")
    body = parts[2]
    if not re.search(r"^# .+", body, re.M):
        errs.append("missing '# <title>' heading")
    for header in REQUIRED_SECTIONS:
        idx = body.find(header)
        if idx < 0:
            errs.append(f"missing section: {header}")
            continue
        chunk = body[idx + len(header):]
        nxt = re.search(r"^## ", chunk, re.M)
        content = chunk[:nxt.start()] if nxt else chunk
        if not [l for l in content.splitlines() if l.strip() and not l.strip() == "---"]:
            errs.append(f"section is empty: {header}")
    return errs


# ------------------------------------------------------------------ distillation

def build_prompt(cand: dict, transcript: str) -> str:
    return f"""Distill the transcript below into ONE knowledge card.

Return STRICT markdown only, exactly this structure (fill <...> placeholders):

---
source: https://www.youtube.com/watch?v={cand['id']}
video_id: {cand['id']}
channel: {cand['channel']}
title: "{cand['title']}"
scraped: {date.today().isoformat()}
tags: [{cand['domain']}, plus 2-4 lowercase topic tags you choose]
---
# {cand['title']}

<one-sentence summary of the whole video>

## Procedure / models distilled
- <8 to 15 bullets; each a self-contained procedure, mental model, or mechanism
  the video actually teaches. Append a (M:SS-M:SS) or (H:MM:SS) range to a bullet
  ONLY if timestamps are recoverable from the transcript text below - if the text
  has no timestamps, use plain bullets and never invent timestamps.>

## Failure modes named
- <bullets: failure modes, anti-patterns, traps, or misconceptions the video
  explicitly names>

## Studio relevance
<ONE line, format "NN phase - how the studio uses this card", where NN phase is
one of: {", ".join(PHASES)}.>

VIDEO METADATA
id: {cand['id']}
title: {cand['title']}
channel: {cand['channel']}
domain: {cand['domain']}

TRANSCRIPT (auto-captions; may be truncated head+tail)
{transcript}"""


def distill_one(cand: dict, chain: list[str], key: str) -> tuple[str, str, str]:
    """Returns (status, model_used, detail). status in {ok, pending}."""
    vid = cand["id"]
    transcript = truncate(cand["path"].read_text(errors="replace"))
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_prompt(cand, transcript)}]
    try:
        md, model = chat(messages, chain, key)
        errs = validate(md, cand)
        if errs:
            repair = [{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content":
                       f"Your previous card for video {vid} violated the contract:\n"
                       + "\n".join(f"- {e}" for e in errs)
                       + "\n\nFix ONLY the listed problems and return the complete "
                         "corrected markdown card.\n\nPREVIOUS OUTPUT:\n" + md}]
            md, model2 = chat(repair, chain, key)
            model = f"{model} + repair({model2})"
            errs = validate(md, cand)
        if errs:
            UNDISTILLED.mkdir(parents=True, exist_ok=True)
            (UNDISTILLED / f"{vid}.txt.pending").write_text(
                f"video_id: {vid}\ntitle: {cand['title']}\n"
                f"channel: {cand['channel']}\ndomain: {cand['domain']}\n"
                f"failed validation twice; errors:\n"
                + "\n".join(f"- {e}" for e in errs)
                + f"\n(raw transcript: raw/{vid}.txt)\n")
        (KY / f"{vid}.md").write_text(strip_fences(md) + "\n")
        stale = UNDISTILLED / f"{vid}.txt.pending"
        if stale.is_file():
            stale.unlink()
        return "ok", model, cand["title"]
    except DistillError as e:
        UNDISTILLED.mkdir(parents=True, exist_ok=True)
        (UNDISTILLED / f"{vid}.txt.pending").write_text(
            f"video_id: {vid}\ntitle: {cand['title']}\n"
            f"channel: {cand['channel']}\ndomain: {cand['domain']}\n"
            f"llm error: {e}\n(raw transcript: raw/{vid}.txt)\n")
        return "pending", "-", str(e)


def append_run_line(attempted: int, distilled: int, pending: int) -> None:
    stamp = time.strftime("%Y-%m-%d %H:%M")
    header = "## Distillation runs"
    text = CARD_MANIFEST.read_text() if CARD_MANIFEST.is_file() else "# YouTube Knowledge Cards — Manifest\n"
    if header not in text:
        if not text.endswith("\n"):
            text += "\n"
        text += (f"\n{header}\n\n| date | attempted | distilled | pending |\n"
                 f"|---|---|---|---|\n")
    text += f"| {stamp} | {attempted} | {distilled} | {pending} |\n"
    CARD_MANIFEST.write_text(text)


# ------------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--workers", type=int, default=6,
                    help="parallel distillation workers (default 6, max 8 enforced)")
    ap.add_argument("--model", default=None,
                    help="primary model id (default claude-haiku-4-5)")
    ap.add_argument("--max", type=int, default=0,
                    help="distill at most N videos (0 = unlimited)")
    ap.add_argument("--domain", default=None,
                    help="only distill videos whose scrape-manifest domain equals D")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and exit without calling the LLM")
    args = ap.parse_args()
    workers = max(1, min(args.workers, 8))

    meta = load_scrape_meta()
    cands = candidates(meta, args.domain or "")
    raw_total = len(list(RAW.glob("*.txt")))
    done = distilled_ids()
    primary = args.model or DEFAULT_CHAIN[0]
    chain = [primary] + [m for m in DEFAULT_CHAIN if m != primary]

    selected = cands[: args.max] if args.max and args.max > 0 else cands
    print(f"== studio_distill ==")
    print(f"raw transcripts:           {raw_total}")
    print(f"already distilled (cards): {len(done)}")
    print(f"pending distillation:      {len(cands)}"
          + (f" (domain={args.domain!r})" if args.domain else ""))
    print(f"selected for this run:     {len(selected)}"
          + (f" (--max {args.max})" if args.max else ""))
    print(f"workers: {workers}  model chain: {', '.join(chain)}")
    if selected:
        preview = ", ".join(f"{c['id']} [{c['domain']}] {c['title'][:40]}"
                            for c in selected[:5])
        print(f"first: {preview}"
              + (" ..." if len(selected) > 5 else ""))
    if args.dry_run:
        print("dry-run: no LLM calls, nothing written")
        return 0

    key = api_key()
    attempted = distilled = pending_n = 0
    titles: list[str] = []
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(distill_one, c, chain, key): c for c in selected}
        for fut in cf.as_completed(futs):
            cand = futs[fut]
            attempted += 1
            try:
                status, model, detail = fut.result()
            except Exception as e:  # never crash the batch
                status, model, detail = "pending", "-", f"unexpected: {e}"
                UNDISTILLED.mkdir(parents=True, exist_ok=True)
                (UNDISTILLED / f"{cand['id']}.txt.pending").write_text(
                    f"video_id: {cand['id']}\nunexpected error: {e}\n")
            if status == "ok":
                distilled += 1
                titles.append(detail)
                print(f"[ok]      {cand['id']}  ({model})  {detail[:70]}",
                      flush=True)
            else:
                pending_n += 1
                print(f"[pending] {cand['id']}  ({model})  {detail[:70]}",
                      file=sys.stderr, flush=True)

    append_run_line(attempted, distilled, pending_n)
    print(f"== run complete: attempted={attempted} distilled={distilled} "
          f"pending={pending_n} (manifest.md updated) ==")
    return 0 if pending_n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
