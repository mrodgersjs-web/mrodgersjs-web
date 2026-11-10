#!/usr/bin/env python3
"""aops — operator-attention ledger, cap, scoreboard, and spawn gate.

The binding stock of the ONE system (RIG + life) is Mike's attention.
This measures it, publishes the cap, and records B4 justifications for
anything new that wants to consume it. Measurement only — enforcement (B3)
is a separately-gated control-plane change (see REVERSIBILITY-ASSESSMENT.md).

Usage:
  aops log <minutes> "<what/who caused it>" [--agent <name>]   charge attention
  aops cap [get|set <h-hours|unlimited>]                        publish the cap
  aops status                                                   scoreboard
  aops gate "<new spawn/cron/node>" --why "<Δoperator-hours or ΔARR/op-h>"   B4 record
  aops tail [n]                                                 recent charges
  aops collect [--day YYYY-MM-DD]   scan telemetry (claude/hermes/codex), charge ESTIMATE rows (deduped per day+source)
  aops predict [--day YYYY-MM-DD]   weekday-profile prediction from trailing 14d ledger
  aops score                        score elapsed predictions (MAE, trend, calibration)
  aops doctor                       v1 status + collector/prediction/falsifier health checks
  aops daily                        collect(yday)→predict(today)→score→daily note+vault copy+ALERT.md
  aops install                      install com.rig.aops LaunchAgent (06:05 daily → aops daily)
"""
from __future__ import annotations

import calendar
import json
import os
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path.home() / ".rig" / "aops"
LEDGER = ROOT / "ledger.jsonl"
CONFIG = ROOT / "config.json"
GATES = ROOT / "gates.jsonl"
PREDICTIONS = ROOT / "predictions.jsonl"
SCORES = ROOT / "scores.jsonl"
DAILY_DIR = ROOT / "daily"
ALERT = ROOT / "ALERT.md"
VAULT_LATEST = Path.home() / "Documents" / "JakeStudio" / "Memory" / "aops-latest.md"
PLIST = Path.home() / "Library" / "LaunchAgents" / "com.rig.aops.plist"
WRAPPER = Path.home() / ".local" / "bin" / "aops"


def ensure() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG.is_file():
        CONFIG.write_text(json.dumps({"cap_hours_per_day": 3.0, "installed": datetime.now().isoformat(timespec="seconds"), "enforcement": "measurement-only (B3 deferred)", "weights": DEFAULT_WEIGHTS}, indent=1))
    else:
        cfg = json.loads(CONFIG.read_text())
        if "weights" not in cfg:
            cfg["weights"] = dict(DEFAULT_WEIGHTS)
            CONFIG.write_text(json.dumps(cfg, indent=1))


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def cmd_log(minutes: float, note: str, agent: str = "operator") -> int:
    ensure()
    with LEDGER.open("a") as f:
        f.write(json.dumps({"ts": now(), "date": date.today().isoformat(),
                            "minutes": round(float(minutes), 1), "note": note, "agent": agent}) + "\n")
    used, cap = today_used()
    flag = ""
    if cap and used > cap * 60:
        flag = f"  ⚠ OVER CAP ({used:.0f}/{cap*60:.0f} min) — B3 not enforced, but this is the number"
    print(f"charged {minutes:.0f} min to {agent}: {note}{flag}")
    return 0


def charges(days: int = 1) -> list[dict]:
    if not LEDGER.is_file():
        return []
    cutoff = (date.today() - timedelta(days=days - 1)).isoformat()
    out = []
    for line in LEDGER.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if r["date"] >= cutoff:
                out.append(r)
    return out


def today_used() -> tuple[float, float | None]:
    rows = [r for r in charges(1)]
    used = sum(r["minutes"] for r in rows)
    cfg = json.loads(CONFIG.read_text()) if CONFIG.is_file() else {}
    cap = cfg.get("cap_hours_per_day")
    return used, (float(cap) if cap and cap != "unlimited" else None)


def fleet_job_count() -> int | None:
    p = Path.home() / ".hermes" / "jobs.json"
    try:
        d = json.loads(p.read_text())
        return len(d) if isinstance(d, list) else len(d.get("jobs", d))
    except Exception:
        return None


def cmd_status() -> int:
    ensure()
    used, cap = today_used()
    rows7 = charges(7)
    print(f"== A_ops {date.today()} ==")
    if cap:
        pct = used / (cap * 60) * 100
        print(f"today: {used:.0f}/{cap*60:.0f} charged min ({pct:.0f}% of cap) — measurement only")
        print(f"       stress rule: shed at p95 load > 70% of cap (polymath import #1)")
    else:
        print(f"today: {used:.0f} charged min (no cap set)")
    if rows7:
        by_day: dict[str, float] = {}
        by_agent: dict[str, float] = {}
        for r in rows7:
            by_day[r["date"]] = by_day.get(r["date"], 0) + r["minutes"]
            by_agent[r["agent"]] = by_agent.get(r["agent"], 0) + r["minutes"]
        print("7-day by day: " + "  ".join(f"{d[5:]}:{v:.0f}m" for d, v in sorted(by_day.items())))
        top = sorted(by_agent.items(), key=lambda x: -x[1])[:5]
        print("7-day top chargers: " + "  ".join(f"{a}:{v:.0f}m" for a, v in top))
        pages = sum(1 for r in rows7 if r.get("agent") != "operator")
        print(f"interrupt-type events (non-operator charges): {pages} in 7d")
    n = fleet_job_count()
    if n is not None:
        print(f"fleet jobs registered (hermes): {n}")
    print("cap: " + str(json.loads(CONFIG.read_text()).get("cap_hours_per_day")) + " h/day — enforcement: measurement-only")
    return 0


def cmd_cap(arg: str = "get", value: str = "") -> int:
    ensure()
    cfg = json.loads(CONFIG.read_text())
    if arg == "set":
        cfg["cap_hours_per_day"] = "unlimited" if value == "unlimited" else float(value)
        CONFIG.write_text(json.dumps(cfg, indent=1))
        print(f"cap set: {cfg['cap_hours_per_day']}")
    else:
        print(f"cap: {cfg.get('cap_hours_per_day')} h/day")
    return 0


def cmd_gate(what: str, why: str = "") -> int:
    ensure()
    w = why.lower()
    has_claim = ("hour" in w or "arr" in w) and any(
        k in w for k in ("delta", "Δ", "reduces", "cuts", "lowers", "raises", "improves", "less", "fewer", "up"))
    negated = any(k in w for k in ("no operator", "not ", "without ", "zero ", "0 delta", "none"))
    ok = has_claim and not negated
    rec = {"ts": now(), "what": what, "why": why,
           "verdict": "JUSTIFIED" if ok else "REJECTED — no Δoperator-hours or ΔARR-per-operator-hour stated (B4 rule)"}
    with GATES.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(f"[B4] {rec['verdict']}")
    if not ok:
        print("     state the debit justification: predicted Δoperator-hours < 0 or Δ(ARR/operator-hour) > 0")
    return 0 if ok else 1


def cmd_tail(n: int = 10) -> int:
    rows = charges(30)[-n:]
    for r in rows:
        print(f"{r['ts']}  {r['minutes']:>6.1f}m  {r['agent']:<18} {r['note'][:70]}")
    return 0

# --------------------------------------------------------------------- v2: telemetry

DEFAULT_WEIGHTS = {"claude_turn_min": 3.0, "hermes_session_min": 5.0, "codex_turn_min": 3.0}
CLAUDE_ROOT = Path.home() / ".claude" / "projects"
HERMES_SESSIONS = Path.home() / ".hermes" / "sessions"
CODEX_SESSIONS = Path.home() / ".codex" / "sessions"
HERMES_IGNORE = {"INDEX.md", "README.md", "recall.sh", "schema.yaml"}
MAX_LINE = 1 << 20        # skip >1MB single lines (pasted blobs / base64)
MAX_SCAN = 64 << 20       # per-file forward-scan cap


def _cfg() -> dict:
    return json.loads(CONFIG.read_text()) if CONFIG.is_file() else {}


def _ledger_rows() -> list[dict]:
    if not LEDGER.is_file():
        return []
    out = []
    for line in LEDGER.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _day_epoch(day: str) -> tuple[int, int]:
    """[start, end) UTC epoch seconds of a LOCAL calendar day."""
    y, m, d = (int(x) for x in day.split("-"))
    start = int(time.mktime((y, m, d, 0, 0, 0, 0, 0, -1)))
    return start, start + 86400


def _line_epoch(line: bytes) -> int | None:
    i = line.find(b'"timestamp":"')
    if i < 0:
        return None
    b = line[i + 13:i + 32]
    try:
        return calendar.timegm((int(b[0:4]), int(b[5:7]), int(b[8:10]),
                                int(b[11:13]), int(b[14:16]), int(b[17:19]), 0, 0, 0))
    except ValueError:
        return None


def _seek_window(f, size: int, lo_ep: int) -> int:
    """Byte offset of the first append-ordered line with timestamp >= lo_ep."""
    lo, hi = 0, size
    while lo < hi:
        mid = (lo + hi) // 2
        f.seek(mid)
        f.readline()          # discard partial line
        line = f.readline()
        if not line:
            hi = mid
            continue
        ep = _line_epoch(line)
        if ep is None or ep < lo_ep:
            lo = f.tell()
        else:
            hi = mid
    return lo


def _count_turns(path: Path, lo_ep: int, hi_ep: int, is_turn) -> int:
    n = 0
    try:
        with open(path, "rb") as f:
            size = os.fstat(f.fileno()).st_size
            if size == 0:
                return 0
            f.seek(_seek_window(f, size, lo_ep))
            scanned = 0
            for line in f:
                scanned += len(line)
                if scanned > MAX_SCAN:
                    break
                if len(line) > MAX_LINE or b'"timestamp"' not in line:
                    continue
                ep = _line_epoch(line)
                if ep is None:
                    continue
                if ep >= hi_ep:
                    break
                if ep >= lo_ep and is_turn(line):
                    n += 1
    except OSError:
        pass
    return n


def _is_claude_turn(line: bytes) -> bool:
    return (b'"type":"user"' in line
            and b'"tool_use_id"' not in line
            and b'"isSidechain":true' not in line
            and b'"isMeta":true' not in line
            and b'<command-name>' not in line)


def _is_codex_turn(line: bytes) -> bool:
    return (b'"type":"response_item"' in line
            and b'"role":"user"' in line
            and b'<environment_context>' not in line
            and b'<user_instructions>' not in line)


def _count_claude(lo_ep: int, hi_ep: int) -> tuple[int, bool]:
    if not CLAUDE_ROOT.is_dir():
        return 0, False
    n = 0
    for dp, _dirs, fns in os.walk(CLAUDE_ROOT):
        for fn in fns:
            if not fn.endswith(".jsonl"):
                continue
            p = os.path.join(dp, fn)
            try:
                if os.stat(p).st_mtime < lo_ep:
                    continue
            except OSError:
                continue
            n += _count_turns(Path(p), lo_ep, hi_ep, _is_claude_turn)
    return n, True


def _count_hermes(lo_ep: int, hi_ep: int) -> tuple[int, bool]:
    if not HERMES_SESSIONS.is_dir():
        return 0, False
    n = 0
    try:
        with os.scandir(HERMES_SESSIONS) as it:
            for e in it:
                if e.name.startswith(".") or e.name in HERMES_IGNORE or not e.is_file():
                    continue
                try:
                    if lo_ep <= e.stat().st_mtime < hi_ep:
                        n += 1
                except OSError:
                    continue
    except OSError:
        return 0, False
    return n, True


def _count_codex(lo_ep: int, hi_ep: int) -> tuple[int, bool]:
    if not CODEX_SESSIONS.is_dir():
        return 0, False
    d0 = datetime.fromtimestamp(lo_ep, tz=timezone.utc).date()
    d1 = datetime.fromtimestamp(hi_ep - 1, tz=timezone.utc).date()
    n = 0
    for dd in {d0 - timedelta(days=1), d0, d1}:   # sessions may spill in from the prior UTC day
        p = CODEX_SESSIONS / dd.strftime("%Y/%m/%d")
        if not p.is_dir():
            continue
        for fn in os.listdir(p):
            if fn.endswith(".jsonl"):
                n += _count_turns(p / fn, lo_ep, hi_ep, _is_codex_turn)
    return n, True


def cmd_collect(day: str = "") -> int:
    ensure()
    day = day or (date.today() - timedelta(days=1)).isoformat()
    lo_ep, hi_ep = _day_epoch(day)
    w = _cfg().get("weights", DEFAULT_WEIGHTS)
    weight = {"claude": w.get("claude_turn_min", 3.0),
              "hermes": w.get("hermes_session_min", 5.0),
              "codex": w.get("codex_turn_min", 3.0)}
    counts = {"claude": _count_claude(lo_ep, hi_ep),
              "hermes": _count_hermes(lo_ep, hi_ep),
              "codex": _count_codex(lo_ep, hi_ep)}
    have = {(r.get("agent"), r.get("date")) for r in _ledger_rows()}
    for src in ("claude", "hermes", "codex"):
        n, ok = counts[src]
        if not ok:
            print(f"{day} {src}: source not readable — skipped")
            continue
        if n == 0:
            print(f"{day} {src}: 0 events — nothing to charge")
            continue
        if (src, day) in have:
            print(f"{day} {src}: {n} events × {weight[src]} min — already collected (dedupe, no write)")
            continue
        minutes = round(n * weight[src], 1)
        with LEDGER.open("a") as f:
            f.write(json.dumps({"ts": now(), "date": day, "minutes": minutes,
                                "note": f"ESTIMATE(collector: {n} events × {weight[src]} min)",
                                "agent": src}) + "\n")
        print(f"{day} {src}: charged {minutes} min — ESTIMATE(collector: {n} events × {weight[src]} min)")
    return 0


def _last_prediction(day: str) -> dict | None:
    if not PREDICTIONS.is_file():
        return None
    hit = None
    for line in PREDICTIONS.read_text().splitlines():
        if line.strip():
            try:
                p = json.loads(line)
            except json.JSONDecodeError:
                continue
            if p.get("day") == day:
                hit = p
    return hit


def cmd_predict(day: str = "") -> int:
    ensure()
    day = day or date.today().isoformat()
    lo = (date.fromisoformat(day) - timedelta(days=14)).isoformat()
    hi = (date.fromisoformat(day) - timedelta(days=1)).isoformat()
    totals: dict[str, float] = {}
    for r in _ledger_rows():
        d = r.get("date", "")
        if lo <= d <= hi:
            totals[d] = totals.get(d, 0.0) + float(r.get("minutes", 0))
    wd = date.fromisoformat(day).weekday()
    same = [v for d, v in totals.items() if date.fromisoformat(d).weekday() == wd]
    if same:
        pred = sum(same) / len(same)
        basis = f"weekday profile n={len(same)} (trailing 14d)"
    elif totals:
        pred = sum(totals.values()) / len(totals)
        basis = "overall mean (trailing 14d, no same-weekday sample)"
    else:
        pred = 0.0
        basis = "no ledger data (trailing 14d empty)"
    low, high = round(max(0.0, pred * 0.6), 1), round(pred * 1.4, 1)
    with PREDICTIONS.open("a") as f:
        f.write(json.dumps({"ts": now(), "day": day, "predicted_min": round(pred, 1),
                            "band_low": low, "band_high": high, "basis": basis}) + "\n")
    print(f"predict {day}: {pred:.0f} min (band {low:.0f}–{high:.0f}) — {basis}")
    return 0


def _score_rows() -> list[dict]:
    if not SCORES.is_file():
        return []
    out = []
    for line in SCORES.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def cmd_score() -> int:
    ensure()
    today = date.today().isoformat()
    last_pred: dict[str, dict] = {}
    if PREDICTIONS.is_file():
        for line in PREDICTIONS.read_text().splitlines():
            if line.strip():
                try:
                    p = json.loads(line)
                except json.JSONDecodeError:
                    continue
                last_pred[p["day"]] = p      # last prediction of the day wins
    scored = {s["day"] for s in _score_rows()}
    rows = _ledger_rows()
    fresh = 0
    for day in sorted(last_pred):
        if day >= today or day in scored:
            continue
        p = last_pred[day]
        actual = round(sum(float(r.get("minutes", 0)) for r in rows if r.get("date") == day), 1)
        with SCORES.open("a") as f:
            f.write(json.dumps({"ts": now(), "day": day, "predicted_min": p["predicted_min"],
                                "actual_min": actual, "error_min": round(actual - float(p["predicted_min"]), 1),
                                "in_band": bool(float(p["band_low"]) <= actual <= float(p["band_high"])),
                                "basis": p.get("basis", "")}) + "\n")
        fresh += 1
    print(f"score: {fresh} new prediction(s) scored")
    prev = _score_rows()
    if not prev:
        print("score: no scored predictions yet")
        return 0
    errs = [s["error_min"] for s in prev]
    mae = sum(abs(e) for e in errs) / len(errs)
    last5 = errs[-5:]
    mae5 = sum(abs(e) for e in last5) / len(last5)
    trend = "improving" if mae5 < mae * 0.9 else ("worsening" if mae5 > mae * 1.1 else "stable")
    mean_err = sum(errs) / len(errs)
    cal = (f"calibration: predictions under-estimate by {mean_err:.0f} min on average" if mean_err > 5
           else f"calibration: predictions over-estimate by {-mean_err:.0f} min on average" if mean_err < -5
           else "calibration: balanced (mean error within ±5 min)")
    print(f"score: MAE {mae:.0f} min over {len(prev)} scored | last-5 MAE {mae5:.0f} ({trend})")
    print(f"score: {cal}")
    return 0


def _yesterday_gate_rows(yday: str) -> list[str]:
    out = []
    if GATES.is_file():
        for line in GATES.read_text().splitlines():
            if not line.strip():
                continue
            try:
                g = json.loads(line)
            except json.JSONDecodeError:
                continue
            if g.get("ts", "")[:10] == yday:
                out.append(f"- [{str(g.get('verdict', '')).split(' ')[0]}] {str(g.get('what', ''))[:80]}")
    return out


def _scoreboard_md(today: str) -> str:
    cfg = _cfg()
    cap = cfg.get("cap_hours_per_day")
    capmin = float(cap) * 60 if cap and cap != "unlimited" else None
    rows = _ledger_rows()
    yday = (date.fromisoformat(today) - timedelta(days=1)).isoformat()
    days = [(date.fromisoformat(today) - timedelta(days=i)).isoformat() for i in range(7, -1, -1)]
    L = [f"# A_ops daily — {today}", "",
         f"cap: {cap} h/day" + (f" ({capmin:.0f} min)" if capmin else "") + " — enforcement: measurement-only", "",
         "## today + 7d", "", "| day | charged | est | manual | %cap |", "|---|---|---|---|---|"]
    for d in days:
        dr = [r for r in rows if r.get("date") == d]
        tot = sum(float(r.get("minutes", 0)) for r in dr)
        est = sum(float(r.get("minutes", 0)) for r in dr if str(r.get("note", "")).startswith("ESTIMATE"))
        pct = f"{tot / capmin * 100:.0f}%" if capmin else "—"
        mark = " (today)" if d == today else ""
        L.append(f"| {d}{mark} | {tot:.0f} | {est:.0f} | {tot - est:.0f} | {pct} |")
    week = [r for r in rows if r.get("date", "") >= days[0]]
    by_agent: dict[str, float] = {}
    for r in week:
        a = r.get("agent", "?")
        by_agent[a] = by_agent.get(a, 0.0) + float(r.get("minutes", 0))
    L += ["", "## top chargers (8d)", ""]
    L += [f"- {a}: {v:.0f} min" for a, v in sorted(by_agent.items(), key=lambda x: -x[1])[:5]] or ["- none"]
    L += ["", f"## prediction vs actual — {yday}", ""]
    p, s = _last_prediction(yday), next((x for x in reversed(_score_rows()) if x.get("day") == yday), None)
    if s:
        band = "in band" if s["in_band"] else "OUT OF band"
        L.append(f"- predicted {s['predicted_min']} min → actual {s['actual_min']} min (error {s['error_min']:+.0f}, {band}) — {s.get('basis', '')}")
    elif p:
        L.append(f"- predicted {p['predicted_min']} min (band {p['band_low']}–{p['band_high']}) — not scored yet")
    else:
        L.append("- no prediction recorded")
    self_y = sum(float(r.get("minutes", 0)) for r in rows if r.get("date") == yday and r.get("agent") == "aops-maintenance")
    notes_y = {r.get("note") for r in rows if r.get("date") == yday}
    L += ["", "## falsifiers (REVERSIBILITY-ASSESSMENT.md)", "",
          f"- metering self-cost {yday}: {self_y:.1f} min (kill criterion: >15 min/day → uninstall)",
          f"- noise {yday}: {len(notes_y)} distinct notes"]
    L += ["", "## gates logged yesterday", ""] + (_yesterday_gate_rows(yday) or ["- none"]) + [""]
    return "\n".join(L)


def cmd_daily() -> int:
    ensure()
    t0 = time.time()
    today = date.today().isoformat()
    yday = (date.today() - timedelta(days=1)).isoformat()
    print(f"== aops daily {today} (collect {yday}) ==")
    cmd_collect(yday)
    cmd_predict(today)
    cmd_score()
    if not any(r.get("agent") == "aops-maintenance" and r.get("date") == today for r in _ledger_rows()):
        mins = max(0.1, round((time.time() - t0) / 60, 1))
        with LEDGER.open("a") as f:
            f.write(json.dumps({"ts": now(), "date": today, "minutes": mins,
                                "note": "aops daily run (collect+predict+score+report)", "agent": "aops-maintenance"}) + "\n")
        print(f"self-charge: {mins} min → aops-maintenance")
    md = _scoreboard_md(today)
    note_path = DAILY_DIR / f"{today}.md"
    note_path.write_text(md)
    vault_ok = True
    try:
        VAULT_LATEST.parent.mkdir(parents=True, exist_ok=True)
        VAULT_LATEST.write_text(md)
    except OSError as e:
        vault_ok = False
        print(f"WARN: vault copy failed ({e.__class__.__name__}) — launchd lacks ~/Documents TCC; "
              f"daily note is authoritative: {note_path}")
    cap = _cfg().get("cap_hours_per_day")
    total_y = sum(float(r.get("minutes", 0)) for r in _ledger_rows() if r.get("date") == yday)
    alert = None
    if cap and cap != "unlimited":
        capmin = float(cap) * 60
        if total_y > capmin:
            alert = "CAP BREACHED"
        elif total_y > 0.7 * capmin:
            alert = "OVER STRESS THRESHOLD (p95 proxy = daily total > 70% of cap)"
    if alert:
        ALERT.write_text(f"# A_ops ALERT — {yday}\n\n{alert}\n\n- yesterday total: {total_y:.0f} min "
                         f"({'over' if total_y > float(cap) * 60 else 'at'} cap {cap} h/day)\n"
                         f"- stress rule: shed at p95 load > 70% of cap (polymath import #1)\n"
                         f"- action: shed lowest-ARR-per-operator-hour load before adding anything new (B4)\n")
        print(f"ALERT: {yday} {total_y:.0f} min — {alert} → {ALERT}")
    elif ALERT.exists():
        ALERT.unlink()
    print(f"daily note: {note_path}")
    if vault_ok:
        print(f"vault copy:  {VAULT_LATEST}")
    return 0


def cmd_doctor() -> int:
    ensure()
    cmd_status()
    print("== doctor ==")
    yday = (date.today() - timedelta(days=1)).isoformat()
    lo_ep, hi_ep = _day_epoch(yday)
    for src, counter in (("claude", _count_claude), ("hermes", _count_hermes), ("codex", _count_codex)):
        n, ok = counter(lo_ep, hi_ep)
        v = "PASS" if (ok and n) else ("WATCH" if ok else "FAIL")
        print(f"[{v}] source {src}: readable={ok} events_yesterday={n}")
    sc = _score_rows()
    if sc:
        mae = sum(abs(s["error_min"]) for s in sc) / len(sc)
        v = "PASS" if mae <= 30 else ("WATCH" if mae <= 60 else "FAIL")
        print(f"[{v}] prediction MAE {mae:.0f} min over {len(sc)} scored (PASS≤30, WATCH≤60)")
    else:
        print("[WATCH] prediction MAE: no scored predictions yet")
    rows = _ledger_rows()
    week = [r for r in rows if r.get("date", "") >= (date.today() - timedelta(days=7)).isoformat()]
    self_cost: dict[str, float] = {}
    notes: dict[str, set] = {}
    for r in week:
        d = r.get("date", "")
        if r.get("agent") == "aops-maintenance":
            self_cost[d] = self_cost.get(d, 0.0) + float(r.get("minutes", 0))
        notes.setdefault(d, set()).add(r.get("note", ""))
    worst = max(self_cost.values(), default=0.0)
    v = "FAIL" if worst > 15 else ("WATCH" if worst > 8 else "PASS")
    print(f"[{v}] falsifier self-cost: max {worst:.1f} min/day charged to aops-maintenance (kill criterion >15)")
    avg_notes = (sum(len(s) for s in notes.values()) / len(notes)) if notes else 0.0
    v = "FAIL" if avg_notes >= 25 else ("WATCH" if avg_notes >= 15 else "PASS")
    print(f"[{v}] falsifier noise: {avg_notes:.1f} distinct notes/day avg (7d) — signal vs fragmentation")
    try:
        out = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=15).stdout
        reg = "com.rig.aops" in out
    except Exception:
        reg = False
    print(f"[{'PASS' if reg else 'WATCH'}] launchd com.rig.aops registered={reg} (06:05 daily)")
    return 0


def cmd_install() -> int:
    ensure()
    log = DAILY_DIR / "launchd.log"
    prog = [str(WRAPPER), "daily"] if WRAPPER.is_file() else [sys.executable, str(Path(__file__).resolve()), "daily"]
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.rig.aops</string>
    <key>ProgramArguments</key>
    <array>
        <string>{prog[0]}</string>
        <string>{prog[1]}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict><key>Hour</key><integer>6</integer><key>Minute</key><integer>5</integer></dict>
    <key>StandardOutPath</key><string>{log}</string>
    <key>StandardErrorPath</key><string>{log}</string>
</dict>
</plist>
"""
    PLIST.parent.mkdir(parents=True, exist_ok=True)
    PLIST.write_text(xml)
    uid = os.getuid()
    subprocess.run(["launchctl", "bootout", f"gui/{uid}", str(PLIST)], capture_output=True)
    r = subprocess.run(["launchctl", "bootstrap", f"gui/{uid}", str(PLIST)], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"install: bootstrap failed — {(r.stderr or r.stdout).strip()}")
        return 1
    v = subprocess.run(["launchctl", "list"], capture_output=True, text=True)
    hit = [l for l in v.stdout.splitlines() if "com.rig.aops" in l]
    print(f"install: wrote {PLIST} and bootstrapped gui/{uid}")
    print("install: launchctl list → " + (hit[0] if hit else "NOT FOUND"))
    return 0 if hit else 1


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    cmd = a[0]
    if cmd == "log" and len(a) >= 3:
        agent = ""
        if "--agent" in a:
            i = a.index("--agent")
            agent = a[i + 1] if i + 1 < len(a) else ""
        return cmd_log(float(a[1]), a[2], agent or "operator")
    if cmd == "cap":
        return cmd_cap(a[1] if len(a) > 1 else "get", a[2] if len(a) > 2 else "")
    if cmd == "status":
        return cmd_status()
    if cmd == "gate" and len(a) >= 2:
        why = ""
        if "--why" in a:
            i = a.index("--why")
            why = a[i + 1] if i + 1 < len(a) else ""
        return cmd_gate(a[1], why)
    if cmd == "tail":
        return cmd_tail(abs(int(a[1])) if len(a) > 1 else 10)
    if cmd in ("collect", "predict"):
        day = ""
        if "--day" in a:
            i = a.index("--day")
            day = a[i + 1] if i + 1 < len(a) else ""
        return cmd_collect(day) if cmd == "collect" else cmd_predict(day)
    if cmd == "score":
        return cmd_score()
    if cmd == "doctor":
        return cmd_doctor()
    if cmd == "daily":
        return cmd_daily()
    if cmd == "install":
        return cmd_install()
    return 2
if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
