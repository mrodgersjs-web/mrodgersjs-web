#!/usr/bin/env python3
"""Resumable, byte-budgeted OmniScout systems-thinking campaign.

Public sources only. Stores OA PDFs, Hacker News thread JSON, and YouTube
captions/metadata; never video media. SQLite owns checkpoints. The deterministic
gate decides whether the exact byte/diversity contract is satisfied.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import contextlib
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "RIG-OmniScout/2.0 (public research corpus; operator@rig.local)"
DEFAULT_ROOT = Path.home() / ".rig/omniscout-campaigns/systems-thinking-5gb-20260829"
DEFAULT_LATTICE = DEFAULT_ROOT / "lattice.json"
OPENALEX = "https://api.openalex.org/works"
HN_SEARCH = "https://hn.algolia.com/api/v1/search"
HN_ITEM = "https://hn.algolia.com/api/v1/items"
ALLOWED_SCHEMES = {"http", "https"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def safe_url(value: str) -> str:
    parsed = urllib.parse.urlsplit(value.strip())
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.hostname:
        raise ValueError("unsupported public URL")
    if parsed.username or parsed.password:
        raise ValueError("credential-bearing URL")
    blocked = {"token", "api_key", "apikey", "auth", "password", "secret", "signature"}
    if any(k.lower() in blocked for k, _ in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)):
        raise ValueError("credential-like query parameter")
    return urllib.parse.urlunsplit(parsed)


def request_bytes(url: str, *, max_bytes: int, timeout: int = 45) -> tuple[bytes, str]:
    """Fetch with a hard whole-transfer deadline; socket timeouts alone can hang."""

    safe = safe_url(url)
    with tempfile.TemporaryDirectory(prefix="rig-http-") as tmp:
        body = Path(tmp) / "body"
        headers = Path(tmp) / "headers"
        result = subprocess.run(
            [
                "curl",
                "--location",
                "--silent",
                "--show-error",
                "--connect-timeout",
                "15",
                "--max-time",
                str(timeout),
                "--user-agent",
                USER_AGENT,
                "--header",
                "Accept: */*",
                "--dump-header",
                str(headers),
                "--output",
                str(body),
                "--write-out",
                "%{http_code}",
                safe,
            ],
            capture_output=True,
            text=True,
            timeout=timeout + 15,
        )
        status = result.stdout.strip()
        if result.returncode != 0 or not status.isdigit() or int(status) >= 400:
            raise RuntimeError(
                f"HTTP {status or 'transport'}: {(result.stderr or '')[-300:]}"
            )
        data = body.read_bytes()
        if len(data) > max_bytes:
            raise ValueError(f"artifact exceeds byte ceiling {max_bytes}")
        content_type = ""
        for line in headers.read_text(errors="replace").splitlines():
            if line.lower().startswith("content-type:"):
                content_type = line.split(":", 1)[1].strip().split(";", 1)[0].lower()
        return data, content_type


TERMINAL_CAPTURE_MARKERS = (
    "HTTP 400:",
    "HTTP 401:",
    "HTTP 403:",
    "HTTP 404:",
    "not a PDF",
)


def is_terminal_capture_error(error: Exception) -> bool:
    return any(marker in str(error) for marker in TERMINAL_CAPTURE_MARKERS)


def db(root: Path) -> sqlite3.Connection:
    root.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(root / "campaign.sqlite")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS items (
          id INTEGER PRIMARY KEY,
          unique_key TEXT NOT NULL UNIQUE,
          topic TEXT NOT NULL,
          source_class TEXT NOT NULL CHECK(source_class IN ('paper','hn','youtube')),
          url TEXT NOT NULL,
          title TEXT,
          metadata_json TEXT NOT NULL,
          state TEXT NOT NULL DEFAULT 'queued',
          attempts INTEGER NOT NULL DEFAULT 0,
          bytes INTEGER NOT NULL DEFAULT 0,
          sha256 TEXT,
          artifact_path TEXT,
          error TEXT,
          discovered_at TEXT NOT NULL,
          completed_at TEXT
        );
        CREATE INDEX IF NOT EXISTS items_state_class ON items(state,source_class,id);
        CREATE INDEX IF NOT EXISTS items_topic ON items(topic,state);
        CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        """
    )
    conn.commit()
    return conn


def load_lattice(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema") != "rig.omniscout.systems-thinking-campaign.v1":
        raise ValueError("wrong lattice schema")
    if int(value["target_bytes"]) < 1:
        raise ValueError("target_bytes must be positive")
    if len(value.get("topics") or []) < int(value["policy"]["min_topics_with_artifacts"]):
        raise ValueError("topic lattice smaller than diversity floor")
    return value


def add_item(conn: sqlite3.Connection, *, key: str, topic: str, source_class: str,
             url: str, title: str, metadata: dict) -> bool:
    try:
        conn.execute(
            """INSERT INTO items(unique_key,topic,source_class,url,title,metadata_json,discovered_at)
               VALUES(?,?,?,?,?,?,?)""",
            (key, topic, source_class, safe_url(url), title[:1000],
             json.dumps(metadata, sort_keys=True), utc_now()),
        )
        return True
    except sqlite3.IntegrityError:
        return False


def choose_pdf(work: dict) -> str | None:
    locations = work.get("locations") or []
    candidates = [str(x.get("pdf_url")) for x in locations if x.get("pdf_url")]
    candidates.sort(key=lambda url: ("arxiv.org" not in url, "openalex" not in url, len(url)))
    return candidates[0] if candidates else None
RELEVANCE_STOPWORDS = {
    "systems",
    "system",
    "thinking",
    "organizational",
    "organizations",
    "operational",
    "engineering",
}
NON_OPERATOR_DOMAIN_TOKENS = (
    "agricultur",
    "biodivers",
    "cancer",
    "carbon",
    "climate",
    "ecosystem",
    "forest",
    "genetic",
    "mendelian",
    "obesity",
    "ozone",
    "vitamin",
)


def operator_domain_allowed(title: str) -> bool:
    lowered = title.lower()
    return not any(token in lowered for token in NON_OPERATOR_DOMAIN_TOKENS)


def title_relevant(title: str, topic: str) -> bool:
    if not operator_domain_allowed(title):
        return False
    lowered = title.lower()
    words = [
        word
        for word in topic.lower().split("-")
        if len(word) >= 4 and word not in RELEVANCE_STOPWORDS
    ]
    return bool(words) and any(
        re.search(rf"\b{re.escape(word)}\w*\b", lowered) for word in words
    )


def prune_irrelevant(root: Path, conn: sqlite3.Connection) -> dict:
    removed_items = 0
    removed_bytes = 0
    rows = conn.execute(
        "SELECT * FROM items WHERE source_class='paper' AND state!='rejected'"
    ).fetchall()
    for row in rows:
        if title_relevant(str(row["title"] or ""), str(row["topic"])):
            continue
        path = Path(row["artifact_path"]) if row["artifact_path"] else None
        if path and path.exists():
            removed_bytes += path.stat().st_size
            path.unlink()
            path.with_suffix(path.suffix + ".meta.json").unlink(missing_ok=True)
        conn.execute(
            """UPDATE items SET state='rejected',bytes=0,sha256=NULL,
               artifact_path=NULL,error='title outside topic admission lexicon'
               WHERE id=?""",
            (row["id"],),
        )
        removed_items += 1
    conn.commit()
    return {"ok": True, "removed_items": removed_items, "removed_bytes": removed_bytes}

def discover_openalex(conn: sqlite3.Connection, lattice: dict, *, pages: int) -> int:
    added = 0
    existing = conn.execute(
        "SELECT count(*) FROM items WHERE source_class='paper' AND state!='rejected'"
    ).fetchone()[0]
    if existing >= 3_000:
        return 0
    for topic in lattice["topics"]:
        query = topic["queries"][0]
        for page in range(1, pages + 1):
            params = urllib.parse.urlencode({
                "search": query,
                "filter": "is_oa:true,has_fulltext:true,from_publication_date:1990-01-01",
                "per-page": 200,
                "page": page,
                "select": "id,doi,title,publication_year,authorships,locations,open_access,primary_topic",
            })
            try:
                data, _ = request_bytes(
                    f"{OPENALEX}?{params}", max_bytes=15_000_000, timeout=60
                )
            except RuntimeError as exc:
                if "HTTP 429" in str(exc) and added:
                    conn.commit()
                    return added
                raise
            value = json.loads(data)
            results = value.get("results") or []
            if not results:
                break
            for work in results:
                pdf = choose_pdf(work)
                title = str(work.get("title") or "Untitled")
                if not pdf or not title_relevant(title, topic["id"]):
                    continue
                key = f"paper:{work.get('id') or pdf}"
                added += add_item(
                    conn, key=key, topic=topic["id"], source_class="paper", url=pdf,
                    title=title, metadata={
                        "openalex_id": work.get("id"), "doi": work.get("doi"),
                        "publication_year": work.get("publication_year"),
                        "open_access": work.get("open_access"),
                        "rig_processes": topic["rig_processes"], "query": query,
                    },
                )
            conn.commit()
            time.sleep(1.0)
    return added


def discover_hn(conn: sqlite3.Connection, lattice: dict, *, pages: int) -> int:
    added = 0
    for topic in lattice["topics"]:
        query = topic["queries"][1]
        for page in range(pages):
            params = urllib.parse.urlencode({"query": query, "tags": "story", "hitsPerPage": 100, "page": page})
            data, _ = request_bytes(f"{HN_SEARCH}?{params}", max_bytes=10_000_000)
            hits = (json.loads(data).get("hits") or [])
            if not hits:
                break
            for hit in hits:
                object_id = hit.get("objectID")
                if not object_id:
                    continue
                added += add_item(
                    conn, key=f"hn:{object_id}", topic=topic["id"], source_class="hn",
                    url=f"{HN_ITEM}/{object_id}", title=str(hit.get("title") or "HN thread"),
                    metadata={"object_id": object_id, "story_url": hit.get("url"),
                              "points": hit.get("points"), "comments": hit.get("num_comments"),
                              "rig_processes": topic["rig_processes"], "query": query},
                )
            conn.commit()
            time.sleep(0.25)
    return added


def discover_youtube(conn: sqlite3.Connection, lattice: dict, *, limit_per_topic: int) -> int:
    if not shutil.which("yt-dlp"):
        return 0
    added = 0
    for topic in lattice["topics"]:
        query = topic["queries"][2]
        command = ["yt-dlp", "--ignore-config", "--flat-playlist", "--dump-single-json",
                   "--playlist-end", str(limit_per_topic), f"ytsearch{limit_per_topic}:{query}"]
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            continue
        with contextlib.suppress(json.JSONDecodeError):
            for entry in json.loads(result.stdout).get("entries") or []:
                video_id = entry.get("id")
                if not video_id:
                    continue
                added += add_item(
                    conn, key=f"youtube:{video_id}", topic=topic["id"], source_class="youtube",
                    url=f"https://www.youtube.com/watch?v={video_id}",
                    title=str(entry.get("title") or query),
                    metadata={"video_id": video_id, "channel": entry.get("channel"),
                              "rig_processes": topic["rig_processes"], "query": query},
                )
        conn.commit()
        time.sleep(1)
    return added


def clean_vtt(text: str) -> str:
    lines: list[str] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        line = re.sub(r"<[^>]+>", "", raw).strip()
        if not line or "-->" in line or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        if re.fullmatch(r"\d+", line) or line in seen:
            continue
        seen.add(line)
        lines.append(line)
    return "\n".join(lines)


def artifact_path(root: Path, row: sqlite3.Row, suffix: str) -> Path:
    name = hashlib.sha256(row["unique_key"].encode()).hexdigest()
    path = root / "raw" / row["source_class"] / row["topic"] / f"{name}{suffix}"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def capture_paper(root: Path, row: sqlite3.Row, max_bytes: int) -> tuple[Path, int, str]:
    data, content_type = request_bytes(row["url"], max_bytes=max_bytes, timeout=90)
    if not data.startswith(b"%PDF") and content_type != "application/pdf":
        raise ValueError(f"not a PDF ({content_type or 'unknown'})")
    path = artifact_path(root, row, ".pdf")
    path.write_bytes(data)
    return path, len(data), hashlib.sha256(data).hexdigest()


def capture_hn(root: Path, row: sqlite3.Row, max_bytes: int) -> tuple[Path, int, str]:
    data, _ = request_bytes(row["url"], max_bytes=min(max_bytes, 10_000_000))
    json.loads(data)
    path = artifact_path(root, row, ".json")
    path.write_bytes(data)
    return path, len(data), hashlib.sha256(data).hexdigest()


def capture_youtube(root: Path, row: sqlite3.Row, max_bytes: int) -> tuple[Path, int, str]:
    with tempfile.TemporaryDirectory(prefix="rig-systems-youtube-") as tmp:
        template = str(Path(tmp) / "%(id)s.%(ext)s")
        command = [
            "yt-dlp", "--ignore-config", "--skip-download", "--write-subs", "--write-auto-subs",
            "--sub-langs", "en.*,en", "--sub-format", "vtt", "--sleep-requests", "2",
            "--min-sleep-interval", "2", "--max-sleep-interval", "5", "--dump-single-json",
            "-o", template, row["url"],
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=240)
        if result.returncode != 0:
            raise RuntimeError(result.stderr[-700:] or "YouTube metadata/captions failed")
        metadata = json.loads(result.stdout)
        subtitles = sorted(Path(tmp).glob("*.vtt"))
        transcript = clean_vtt(subtitles[0].read_text(errors="replace")) if subtitles else ""
        if not transcript:
            transcript = str(metadata.get("description") or "")
        if len(transcript.strip()) < 80:
            raise ValueError("no useful public captions or description")
        data = (json.dumps({"metadata": metadata, "transcript": transcript}, sort_keys=True) + "\n").encode()
        if len(data) > max_bytes:
            raise ValueError("caption artifact exceeds ceiling")
        path = artifact_path(root, row, ".json")
        path.write_bytes(data)
        return path, len(data), hashlib.sha256(data).hexdigest()


def totals(conn: sqlite3.Connection) -> dict:
    total = conn.execute("SELECT coalesce(sum(bytes),0) FROM items WHERE state='done'").fetchone()[0]
    classes = {r[0]: {"items": r[1], "bytes": r[2]} for r in conn.execute(
        "SELECT source_class,count(*),coalesce(sum(bytes),0) FROM items WHERE state='done' GROUP BY source_class")}
    topics = {r[0]: {"items": r[1], "bytes": r[2]} for r in conn.execute(
        "SELECT topic,count(*),coalesce(sum(bytes),0) FROM items WHERE state='done' GROUP BY topic")}
    states = {r[0]: r[1] for r in conn.execute("SELECT state,count(*) FROM items GROUP BY state")}
    return {"artifact_bytes": int(total), "source_classes": classes, "topics": topics, "states": states}


def write_status(root: Path, conn: sqlite3.Connection, lattice: dict, target: int) -> dict:
    stats = totals(conn)
    usage = shutil.disk_usage(root)
    value = {
        "schema": "rig.omniscout.systems-thinking-campaign-status.v1",
        "campaign_id": lattice["campaign_id"],
        "updated_at": utc_now(),
        "root": str(root),
        "target_bytes": target,
        "artifact_bytes": stats["artifact_bytes"],
        "progress": round(stats["artifact_bytes"] / target, 6) if target else 1,
        "source_classes": stats["source_classes"],
        "topics": stats["topics"],
        "states": stats["states"],
        "disk_free_bytes": usage.free,
        "authority_state": "STAGED_NOT_PROMOTED",
    }
    atomic_json(root / "status.json", value)
    return value


def topic_source_class_counts(conn: sqlite3.Connection) -> dict[str, int]:
    return {
        str(row["topic"]): int(row["n"])
        for row in conn.execute(
            """SELECT topic,count(DISTINCT source_class) AS n
               FROM items WHERE state='done' GROUP BY topic"""
        )
    }


def preferred_class(conn: sqlite3.Connection, lattice: dict) -> str:
    targeted = conn.execute(
        """SELECT source_class FROM items
           WHERE state='queued' AND metadata_json LIKE ?
           ORDER BY id LIMIT 1""",
        ('%"targeted_gap_repair": true%',),
    ).fetchone()
    if targeted is not None:
        return str(targeted["source_class"])

    policy = lattice["policy"]
    two_class_topics = sum(
        count >= 2 for count in topic_source_class_counts(conn).values()
    )
    required_two_class_topics = int(policy.get("min_topics_two_source_classes", 0))
    if two_class_topics < required_two_class_topics:
        for source_class in ("youtube", "hn"):
            row = conn.execute(
                """SELECT q.id FROM items q
                   LEFT JOIN (
                     SELECT topic,count(DISTINCT source_class) AS n
                     FROM items WHERE state='done' GROUP BY topic
                   ) d ON d.topic=q.topic
                   WHERE q.state='queued' AND q.source_class=?
                   AND coalesce(d.n,0)<2 LIMIT 1""",
                (source_class,),
            ).fetchone()
            if row is not None:
                return source_class
    classes = totals(conn)["source_classes"]
    floors = policy["source_class_floors_bytes"]
    deficits = [
        (classes.get(name, {}).get("bytes", 0) / floor if floor else 1, name)
        for name, floor in floors.items()
    ]
    deficits.sort()
    return deficits[0][1] if deficits and deficits[0][0] < 1 else "paper"


def run_campaign(root: Path, conn: sqlite3.Connection, lattice: dict, *, target: int,
                 max_items: int | None) -> dict:
    policy = lattice["policy"]
    lock = (root / "writer.lock").open("w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError as exc:
        lock.close()
        raise RuntimeError("another campaign writer owns the lock") from exc
    done_items = 0
    conn.execute(
        "UPDATE items SET state='queued',error='recovered after interrupted writer' "
        "WHERE state='processing'"
    )
    conn.commit()
    while totals(conn)["artifact_bytes"] < target:
        if max_items is not None and done_items >= max_items:
            break
        if shutil.disk_usage(root).free < int(policy["free_disk_floor_bytes"]):
            raise RuntimeError("free disk below campaign floor")
        source_class = preferred_class(conn, lattice)
        remaining_items = (
            max_items - done_items if max_items is not None else None
        )
        paper_workers = int(policy.get("paper_download_concurrency", 1))
        batch_limit = paper_workers if source_class == "paper" else 1
        if remaining_items is not None:
            batch_limit = min(batch_limit, remaining_items)
        if target - totals(conn)["artifact_bytes"] <= int(
            policy["max_single_artifact_bytes"]
        ):
            batch_limit = 1
        candidate_rows = conn.execute(
            """SELECT q.* FROM items q
               LEFT JOIN (
                 SELECT topic,count(*) AS n FROM items
                 WHERE state='done' AND source_class=? GROUP BY topic
               ) d ON d.topic=q.topic
               WHERE q.state='queued' AND q.source_class=?
               ORDER BY CASE WHEN q.metadata_json LIKE '%"targeted_gap_repair": true%'
                            THEN 0 ELSE 1 END,
                        coalesce(d.n,0),q.attempts,q.id LIMIT ?""",
            (source_class, source_class, max(batch_limit * 4, 1)),
        ).fetchall()
        if not candidate_rows:
            candidate_rows = conn.execute(
                """SELECT q.* FROM items q
                   LEFT JOIN (
                     SELECT topic,count(*) AS n FROM items
                     WHERE state='done' GROUP BY topic
                   ) d ON d.topic=q.topic
                   WHERE q.state='queued'
                   ORDER BY coalesce(d.n,0),q.attempts,q.id LIMIT ?""",
                (max(batch_limit * 4, 1),),
            ).fetchall()
        if not candidate_rows:
            break
        rows = []
        selected_topics: set[str] = set()
        for row in candidate_rows:
            if row["topic"] in selected_topics:
                continue
            if row["source_class"] == "paper" and not title_relevant(
                str(row["title"] or ""), str(row["topic"])
            ):
                conn.execute(
                    """UPDATE items SET state='rejected',
                       error='title outside topic admission lexicon' WHERE id=?""",
                    (row["id"],),
                )
                continue
            selected_topics.add(str(row["topic"]))
            rows.append(row)
            if len(rows) == batch_limit:
                break
        conn.commit()
        if not rows:
            continue
        for row in rows:
            conn.execute(
                "UPDATE items SET state='processing',attempts=attempts+1 WHERE id=?",
                (row["id"],),
            )
        conn.commit()
        max_bytes = int(policy["max_single_artifact_bytes"])

        def capture(row: sqlite3.Row) -> tuple[Path, int, str]:
            if row["source_class"] == "paper":
                return capture_paper(root, row, max_bytes)
            if row["source_class"] == "hn":
                return capture_hn(root, row, max_bytes)
            return capture_youtube(root, row, max_bytes)

        outcomes: dict[int, tuple[Path, int, str] | Exception] = {}
        if len(rows) == 1:
            try:
                outcomes[int(rows[0]["id"])] = capture(rows[0])
            except Exception as exc:
                outcomes[int(rows[0]["id"])] = exc
        else:
            with ThreadPoolExecutor(max_workers=len(rows)) as executor:
                futures = {executor.submit(capture, row): row for row in rows}
                for future in as_completed(futures):
                    row = futures[future]
                    try:
                        outcomes[int(row["id"])] = future.result()
                    except Exception as exc:
                        outcomes[int(row["id"])] = exc
        for row in rows:
            outcome = outcomes[int(row["id"])]
            if isinstance(outcome, Exception):
                state = (
                    "failed"
                    if is_terminal_capture_error(outcome) or int(row["attempts"]) + 1 >= 3
                    else "queued"
                )
                conn.execute(
                    "UPDATE items SET state=?,error=? WHERE id=?",
                    (state, f"{type(outcome).__name__}: {str(outcome)[:700]}", row["id"]),
                )
                continue
            path, size, digest = outcome
            sidecar = path.with_suffix(path.suffix + ".meta.json")
            atomic_json(
                sidecar,
                {
                    "schema": "rig.omniscout.source-artifact.v1",
                    "campaign_id": lattice["campaign_id"],
                    "source_url": row["url"],
                    "source_class": row["source_class"],
                    "topic": row["topic"],
                    "title": row["title"],
                    "retrieved_at": utc_now(),
                    "artifact_bytes": size,
                    "sha256": digest,
                    "metadata": json.loads(row["metadata_json"]),
                    "authority_state": "STAGED_NOT_PROMOTED",
                },
            )
            conn.execute(
                """UPDATE items SET state='done',bytes=?,sha256=?,artifact_path=?,
                   completed_at=?,error=NULL WHERE id=?""",
                (size, digest, str(path), utc_now(), row["id"]),
            )
            done_items += 1
        conn.commit()
        write_status(root, conn, lattice, target)
        time.sleep(0.4 if source_class == "hn" else 0.8)
    return write_status(root, conn, lattice, target)


def topic_anchor_checks(conn: sqlite3.Connection, lattice: dict) -> dict[str, bool]:
    anchors_by_topic = lattice.get("topic_domain_anchor_floors") or {}
    checks: dict[str, bool] = {}
    for topic, anchors in anchors_by_topic.items():
        titles = [
            str(row[0] or "").lower()
            for row in conn.execute(
                "SELECT title FROM items WHERE state='done' AND topic=?",
                (topic,),
            )
        ]
        checks[topic] = any(
            any(str(anchor).lower() in title for anchor in anchors)
            for title in titles
        )
    return checks


def gate(root: Path, conn: sqlite3.Connection, lattice: dict, target: int) -> tuple[bool, dict]:
    status = write_status(root, conn, lattice, target)
    floors = lattice["policy"]["source_class_floors_bytes"]
    class_checks = {name: status["source_classes"].get(name, {}).get("bytes", 0) >= floor
                    for name, floor in floors.items()}
    topic_count = sum(1 for value in status["topics"].values() if value["items"] > 0)
    source_mix = topic_source_class_counts(conn)
    two_class_topics = sum(count >= 2 for count in source_mix.values())
    required_two_class_topics = int(
        lattice["policy"].get("min_topics_two_source_classes", 0)
    )
    anchors = topic_anchor_checks(conn, lattice)
    checks = {
        "target_bytes": status["artifact_bytes"] >= target,
        "source_class_floors": class_checks,
        "min_source_classes": len([x for x in status["source_classes"].values() if x["items"]])
        >= int(lattice["policy"]["min_source_classes"]),
        "min_topics": topic_count >= int(lattice["policy"]["min_topics_with_artifacts"]),
        "min_topics_two_source_classes": {
            "actual": two_class_topics,
            "required": required_two_class_topics,
            "by_topic": source_mix,
        },
        "topic_domain_anchors": anchors,
        "disk_floor": status["disk_free_bytes"] >= int(lattice["policy"]["free_disk_floor_bytes"]),
    }
    ok = bool(
        checks["target_bytes"]
        and all(class_checks.values())
        and checks["min_source_classes"]
        and checks["min_topics"]
        and two_class_topics >= required_two_class_topics
        and all(anchors.values())
        and checks["disk_floor"]
    )
    receipt = {"schema": "rig.omniscout.systems-thinking-campaign-gate.v1", "at": utc_now(),
               "ok": ok, "checks": checks, "status": status}
    atomic_json(root / "gate.json", receipt)
    return ok, receipt


def proof(root: Path, conn: sqlite3.Connection, lattice: dict, target: int) -> dict:
    ok, receipt = gate(root, conn, lattice, target)
    if not ok:
        raise RuntimeError("campaign gate is RED")
    rows = conn.execute("SELECT sha256,bytes FROM items WHERE state='done' ORDER BY sha256").fetchall()
    chain = hashlib.sha256("\n".join(f"{r['sha256']} {r['bytes']}" for r in rows).encode()).hexdigest()
    value = {"schema": "rig.omniscout.systems-thinking-campaign-proof.v1", "sealed_at": utc_now(),
             "campaign_id": lattice["campaign_id"], "gate": receipt, "artifact_chain_sha256": chain,
             "artifact_count": len(rows), "lattice_sha256": hashlib.sha256(
                 DEFAULT_LATTICE.read_bytes() if DEFAULT_LATTICE.exists() else json.dumps(lattice,sort_keys=True).encode()
             ).hexdigest(), "authority_state": "STAGED_NOT_PROMOTED"}
    atomic_json(root / "PROOF.json", value)
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=["discover", "prune", "run", "status", "gate", "proof"]
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--lattice", type=Path, default=DEFAULT_LATTICE)
    parser.add_argument("--target-bytes", type=int)
    parser.add_argument("--openalex-pages", type=int, default=5)
    parser.add_argument("--hn-pages", type=int, default=3)
    parser.add_argument("--youtube-limit", type=int, default=15)
    parser.add_argument("--max-items", type=int)
    args = parser.parse_args()
    lattice = load_lattice(args.lattice)
    target = args.target_bytes or int(lattice["target_bytes"])
    conn = db(args.root)
    if args.command == "discover":
        value = {"openalex": discover_openalex(conn, lattice, pages=args.openalex_pages),
                 "hn": discover_hn(conn, lattice, pages=args.hn_pages),
                 "youtube": discover_youtube(conn, lattice, limit_per_topic=args.youtube_limit)}
        value["status"] = write_status(args.root, conn, lattice, target)
        print(json.dumps(value, indent=2, sort_keys=True)); return 0
    if args.command == "prune":
        value = prune_irrelevant(args.root, conn)
        value["status"] = write_status(args.root, conn, lattice, target)
        print(json.dumps(value, indent=2, sort_keys=True)); return 0
    if args.command == "run":
        value = run_campaign(args.root, conn, lattice, target=target, max_items=args.max_items)
        print(json.dumps(value, indent=2, sort_keys=True)); return 0
    if args.command == "status":
        print(json.dumps(write_status(args.root, conn, lattice, target), indent=2, sort_keys=True)); return 0
    if args.command == "gate":
        ok, value = gate(args.root, conn, lattice, target)
        print(json.dumps(value, indent=2, sort_keys=True)); return 0 if ok else 4
    value = proof(args.root, conn, lattice, target)
    print(json.dumps(value, indent=2, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
