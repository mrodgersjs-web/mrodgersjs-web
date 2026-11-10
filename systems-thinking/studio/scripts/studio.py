#!/usr/bin/env python3
"""studio — Systems Thinking Studio CLI.

Usage:
  studio doctor
  studio frame [system-name] [--domain gtm|linkedin|sales|founder|mike-os]
  studio map "<symptom text>"
  studio archetype [id|all]
  studio leverage [--rank N|all]
  studio crosspoll "<target structure>" [domain]
  studio cards [tag] [--grep s]
  studio card "<title>"
  studio mechanisms [query]
  studio context [clear|complicated|complex|chaotic|disorder|all]
  studio operating [daily|weekly|agents|gaps]
  studio search "<query>" [focused|exhaustive]
  studio pack
  studio run "<problem>" [--domain gtm|linkedin|sales|founder|mike-os] [--context clear|complicated|complex|chaotic]
"""
from __future__ import annotations

import json
import os
import signal
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from engine import retrieve_knowledge, score_crosspoll, score_map, simulate as euler


PKG = Path(__file__).resolve().parent.parent
DATA = PKG / "data"
BASE_URL = "https://backend.getrecall.ai/api/v1"
VOCAB = {
    "systems-thinking", "psychology", "startup", "founder", "growth",
    "linkedin", "sales", "gtm", "tools", "ai-agents", "marketing",
    "content", "productivity", "strategy", "engineering", "finance", "other",
}


def load(name: str):
    return json.loads((DATA / name).read_text())


def api_key() -> str:
    k = os.environ.get("RECALL_API_KEY", "")
    if not k:
        p = Path.home() / ".hermes" / ".env"
        if p.is_file():
            for line in p.read_text().splitlines():
                if line.startswith("RECALL_API_KEY="):
                    k = line.split("=", 1)[1].strip()
    return k


def card_index() -> dict:
    f = DATA / "card-index.json"
    return json.loads(f.read_text()) if f.is_file() else {}


def cmd_doctor() -> int:
    ok = True
    for f in (
        "archetypes.json",
        "leverage-points.json",
        "card-index.json",
        "polymath-domains.json",
        "theory-spine-20260830.json",
        "decision-contexts.json",
    ):
        p = DATA / f
        n = ""
        if f == "card-index.json" and p.is_file():
            n = f" ({len(json.loads(p.read_text()))} cards)"
        print(f"{'PASS' if p.is_file() else 'FAIL'} data/{f}{n}")
        ok &= p.is_file()
    theory_ok = False
    try:
        spine = load("theory-spine-20260830.json")
        contexts = load("decision-contexts.json")
        source_ids = {item.get("id") for item in spine.get("sources") or []}
        theory_ok = (
            spine.get("schema") == "rig.systems-thinking-studio.theory-spine.v1"
            and {
                "cynefin-snowden-boone-2007",
                "meadows-leverage-1999",
                "kim-systems-archetypes-2000",
            }
            <= source_ids
            and contexts.get("source_id") == "cynefin-snowden-boone-2007"
            and len(contexts.get("contexts") or []) == 5
        )
    except (OSError, ValueError):
        theory_ok = False
    print(f"{'PASS' if theory_ok else 'FAIL'} source-anchored theory spine")
    ok &= theory_ok
    pack = PKG / "references" / "recall-pack.md"
    print(f"{'PASS' if pack.is_file() else 'WARN'} references/recall-pack.md")
    k = api_key()
    print(f"{'PASS' if k else 'WARN'} live Recall search: {'key present' if k else 'no key'}")
    print(f"INFO mirror-backed cards: {sum(1 for v in card_index().values() if v.get('mirror_path'))}")

    curated = DATA / "curated-mechanisms-20260830.json"
    curated_ok = False
    if curated.is_file():
        try:
            value = json.loads(curated.read_text())
            cutoff = value.get("source_cutoff") or {}
            mechanisms = value.get("mechanisms") or []
            topics = {item.get("source_topic") for item in mechanisms}
            hashes = {item.get("source_card_sha256") for item in mechanisms}
            curated_ok = (
                value.get("schema") == "rig.systems-thinking-studio.mechanisms.v1"
                and value.get("authority_state") == "STAGED_NOT_PROMOTED"
                and len(mechanisms) == 18
                and int(cutoff.get("raw_artifact_bytes") or 0)
                >= int(cutoff.get("raw_target_bytes") or 1)
                and int(cutoff.get("l2_pass_cards") or 0) == 18
                and int(cutoff.get("l2_quarantined_cards", -1)) == 0
                and cutoff.get("l2_not_ready_topics") == []
                and len(topics) == len(mechanisms)
                and len(hashes) == len(mechanisms)
                and all(
                    isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value)
                    for value in hashes
                )
            )
        except (OSError, ValueError):
            curated_ok = False
    print(f"{'PASS' if curated_ok else 'FAIL'} data/curated-mechanisms-20260830.json")
    ok &= curated_ok

    operating = DATA / "operating-cadence-20260830.json"
    operating_map = PKG / "process-maps" / "systems-thinking-operating-system.excalidraw"
    operating_ok = False
    if operating.is_file():
        try:
            value = json.loads(operating.read_text())
            operating_ok = (
                value.get("schema") == "rig.systems-thinking-studio.operating-cadence.v1"
                and len(value.get("gaps") or []) == 30
                and len(value.get("agents") or []) >= 8
                and len(value.get("daily_outcomes") or []) >= 7
                and len(value.get("weekly_schedule") or []) == 7
            )
        except (OSError, ValueError):
            operating_ok = False
    print(f"{'PASS' if operating_ok else 'FAIL'} data/operating-cadence-20260830.json")
    print(f"{'PASS' if operating_map.is_file() else 'FAIL'} process-maps/systems-thinking-operating-system.excalidraw")
    ok &= operating_ok and operating_map.is_file()

    phases = (PKG / "processes" / "phases.md").read_text() if (PKG / "processes" / "phases.md").is_file() else ""
    skill = (PKG / "SKILL.md").read_text() if (PKG / "SKILL.md").is_file() else ""
    harness = (PKG / "harness" / "systems-studio.sh").read_text() if (PKG / "harness" / "systems-studio.sh").is_file() else ""
    eight = "Eight Phases" in phases and "08 VERIFY" in phases
    skill8 = "8-phase" in skill
    har8 = "run_phase 06 POLYMATH" in harness and "Phase 08 VERIFY" in harness
    print(f"{'PASS' if eight else 'FAIL'} processes/phases.md is 8-phase")
    print(f"{'PASS' if skill8 else 'FAIL'} SKILL.md is 8-phase")
    print(f"{'PASS' if har8 else 'FAIL'} harness walks 01–08 including POLYMATH")
    ok &= eight and skill8 and har8

    frames_dir = PKG / "templates" / "frames"
    have = {p.stem for p in frames_dir.glob("*.md")} if frames_dir.is_dir() else set()
    need = {"gtm", "linkedin", "sales", "founder", "mike-os"}
    missing = sorted(need - have)
    print(f"{'PASS' if not missing else 'FAIL'} domain frames {sorted(have)} missing={missing}")
    ok &= not missing

    src = (PKG / "scripts" / "studio.py").read_text()
    search_wired = 'if cmd == "search"' in src
    run_wired = 'if cmd == "run"' in src
    sim_wired = 'if cmd == "simulate"' in src
    mechanisms_wired = 'if cmd == "mechanisms"' in src
    operating_wired = 'if cmd == "operating"' in src
    context_wired = 'if cmd == "context"' in src
    engine_ok = (PKG / "scripts" / "engine.py").is_file()
    models_ok = (DATA / "stock-flow-models.json").is_file()
    tranche_ok = (PKG / "processes" / "source-gated-tranche.md").is_file()
    print(f"{'PASS' if search_wired else 'FAIL'} studio search is dispatched")
    print(f"{'PASS' if run_wired else 'FAIL'} studio run is dispatched")
    print(f"{'PASS' if sim_wired else 'FAIL'} studio simulate is dispatched")
    print(f"{'PASS' if mechanisms_wired else 'FAIL'} studio mechanisms is dispatched")
    print(f"{'PASS' if operating_wired else 'FAIL'} studio operating is dispatched")
    print(f"{'PASS' if context_wired else 'FAIL'} studio context is dispatched")
    print(f"{'PASS' if engine_ok else 'FAIL'} scripts/engine.py")
    print(f"{'PASS' if models_ok else 'FAIL'} data/stock-flow-models.json")
    print(f"{'PASS' if tranche_ok else 'FAIL'} processes/source-gated-tranche.md")
    ok &= (
        search_wired
        and run_wired
        and sim_wired
        and mechanisms_wired
        and context_wired
        and operating_wired
        and engine_ok
        and models_ok
        and tranche_ok
    )
    return 0 if ok else 1


def cmd_frame(name: str = "", domain: str = "") -> int:
    if domain:
        p = PKG / "templates" / "frames" / f"{domain}.md"
        if not p.is_file():
            have = sorted(x.stem for x in (PKG / "templates" / "frames").glob("*.md"))
            print(f"unknown domain {domain!r}; have {have}")
            return 2
        print(p.read_text().replace("<SYSTEM>", name or domain))
        return 0
    tpl = (PKG / "templates" / "system-frame.md").read_text()
    print(tpl.replace("<SYSTEM>", name or "<SYSTEM>"))
    return 0


def cmd_map(text: str) -> int:
    scored = score_map(text)
    if not scored:
        print("No archetype symptom matches. Widen the symptom description "
              "(verbs + nouns: 'quick fix', 'keeps coming back', 'plateau', 'arms race'...).")
        return 1
    for i, a in enumerate(scored[:3], 1):
        print(f"{i}. {a['name']} [{a['confidence']}] — matched: {', '.join(a['hits'][:5])}")
        print(f"   diagnosis: {a['diagnosis']}")
        if i == 1:
            print(f"   intervention: {a['intervention']}")
            print(f"   counterintuitive: {a['counterintuitive']}")
    return 0


def cmd_archetype(ident: str = "all") -> int:
    arts = load("archetypes.json")["archetypes"]
    sel = [a for a in arts if ident in ("all", a["id"], a["name"].lower())]
    if not sel:
        print(f"unknown archetype {ident!r}; ids: " + ", ".join(a["id"] for a in arts))
        return 2
    for a in sel:
        print(f"== {a['name']} ({a['id']})")
        print(f"story: {a['story']}")
        print(f"symptoms: {', '.join(a['symptoms'])}")
        print(f"diagnosis: {a['diagnosis']}")
        print(f"intervention: {a['intervention']}")
        print(f"counterintuitive: {a['counterintuitive']}\n")
    return 0


def cmd_leverage(rank: str = "all") -> int:
    pts = load("leverage-points.json")["leverage_points"]
    if rank not in ("all",):
        try:
            r = int(rank)
        except ValueError:
            print("--rank takes 1..12 or 'all'")
            return 2
        pts = [p for p in pts if p["rank"] == r] or [f"no rank {r}"]
    for p in pts:  # already ordered weak -> strong? stored rank desc; sort asc rank = weakest first? keep file order (12->1)
        print(f"[{p['rank']:>2}] {p['name']}")
        print(f"     ask: {p['question']}")
        print(f"     note: {p['note']}")
    print("\n(12 = weakest, 1 = strongest — Meadows 1999)")
    return 0


def cmd_mechanisms(query: str = "") -> int:
    path = DATA / "curated-mechanisms-20260830.json"
    if not path.is_file():
        print("no curated mechanism registry; run studio doctor")
        return 1
    value = json.loads(path.read_text())
    q = query.lower().strip()
    rows = []
    for mechanism in value.get("mechanisms") or []:
        searchable = " ".join(
            [
                mechanism.get("id", ""),
                mechanism.get("source_topic", ""),
                mechanism.get("rule", ""),
                mechanism.get("studio_change", ""),
                " ".join(mechanism.get("applies_to") or []),
            ]
        ).lower()
        if not q or q in searchable:
            rows.append(mechanism)
    if not rows:
        print(f"no curated mechanism matches {query!r}")
        return 1
    cutoff = value.get("source_cutoff") or {}
    print(
        f"{len(rows)} staged mechanisms | "
        f"cutoff={cutoff.get('raw_artifact_bytes')} bytes | "
        f"source_l2={cutoff.get('l2_pass_cards')} PASS"
    )
    for mechanism in rows:
        print(f"== {mechanism['id']} [{mechanism['transfer']}]")
        print(f"   rule: {mechanism['rule']}")
        print(f"   change: {mechanism['studio_change']}")
        print(f"   gate: {mechanism['gate']}")
        print(f"   proof: {mechanism['source_card_sha256']}")
    return 0


def cmd_context(ident: str = "all") -> int:
    data = load("decision-contexts.json")
    contexts = data.get("contexts") or []
    selected = contexts
    if ident != "all":
        needle = ident.strip().lower()
        selected = [
            item
            for item in contexts
            if needle == item.get("id") or needle in (item.get("aliases") or [])
        ]
    if not selected:
        print("usage: studio context [clear|complicated|complex|chaotic|disorder|all]")
        return 2
    print(f"source={data['source_id']} | {data['classification_rule']}")
    for item in selected:
        print(f"== {item['id'].upper()} — {item['response']}")
        print(f"   cause/effect: {item['cause_effect']}")
        print(f"   method: {item['method']}")
        print(f"   danger: {item['danger']}")
        print(f"   required: {item['required_artifact']}")
    return 0


def cmd_operating(view: str = "") -> int:
    path = DATA / "operating-cadence-20260830.json"
    if not path.is_file():
        print("no operating cadence contract; run studio doctor")
        return 1
    data = json.loads(path.read_text())
    view = view or "daily"
    if view == "daily":
        for row in data["daily_outcomes"]:
            print(f"{row['time']} | {row['owner']} | {row['outcome']}\n  gate: {row['gate']}")
        return 0
    if view == "weekly":
        for row in data["weekly_schedule"]:
            print(f"{row['day']} | {row['theme']} | {row['owner']}\n  outcome: {row['outcome']}")
        return 0
    if view == "agents":
        for row in data["agents"]:
            print(f"== {row['id']} — {row['role']}\n  do: {row['does']}\n  not: {row['does_not']}")
        return 0
    if view == "gaps":
        for row in data["gaps"]:
            print(f"{row['id']} [{row['status']}] {row['gap']}\n  owner: {row['owner']}\n  durable: {row['durable_setup']}\n  gate: {row['verification']}")
        return 0
    print("usage: studio operating [daily|weekly|agents|gaps]")
    return 2


def cmd_cards(tag: str = "", grep: str = "") -> int:
    idx = card_index()
    if not idx:
        print("no card-index.json snapshot; see package README")
        return 1
    tag = tag.strip().lower()
    if tag and tag not in VOCAB:
        print(f"unknown tag {tag!r}; vocabulary: {', '.join(sorted(VOCAB))}")
        return 2
    rows = [(cid, m) for cid, m in idx.items() if (not tag or tag in m["tags"])
            and (not grep or grep.lower() in m["title"].lower())]
    print(f"{len(rows)} cards" + (f" tagged {tag}" if tag else "") + (f" matching {grep!r}" if grep else ""))
    for cid, m in rows[:200]:
        print(f"- {m['title'][:110]} | {','.join(m['tags'])} | {m.get('source_url','')[:70]}")
    if len(rows) > 200:
        print(f"... and {len(rows)-200} more (narrow with a tag or --grep)")
    return 0


def cmd_card(query: str) -> int:
    idx = card_index()
    q = query.lower()
    hits = [(cid, m) for cid, m in idx.items()
            if q in m["title"].lower() or q == cid or m["title"].lower().startswith(q)]
    if not hits:
        print(f"no index hit for {query!r}; try 'studio search \"{query}\"'")
        return 1
    for cid, m in hits[:5]:
        print(f"== {m['title']}\n   id {cid} | tags {','.join(m['tags'])} | {m.get('source_url','')}")
        mp = m.get("mirror_path")
        if mp and Path(mp).is_file():
            body = Path(mp).read_text(errors="replace")
            body = re.sub(r"^---.*?---\s*", "", body, flags=re.S)[:1600]
            print("   --- mirror content (first 1600 chars) ---")
            for line in body.splitlines()[:28]:
                print(f"   {line}")
        else:
            print("   (no local mirror; live fetch: python3 scripts/recall_api-style GET /cards/" + cid + ")")
    return 0


def cmd_search(q: str, mode: str = "focused") -> int:
    k = api_key()
    if not k:
        print("no RECALL_API_KEY (env or ~/.hermes/.env)")
        return 1
    url = BASE_URL + "/search?" + urllib.parse.urlencode({"q": q, "mode": mode})
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {k}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    print(f"total_cards: {d.get('total_cards')}")
    for doc in d.get("documents", [])[:20]:
        print(f"\n== {doc.get('title')}\n   {doc.get('source_url','')}")
        for ch in doc.get("chunks", [])[:3]:
            c = " ".join(ch.get("content", "").split())[:300]
            print(f"   - {c}")
    return 0
def cmd_crosspoll(text: str, domain: str = "") -> int:
    result = score_crosspoll(text)
    if domain:
        result["kept"] = [r for r in result["kept"] if r["domain"] == domain]
        result["rejected"] = [r for r in result["rejected"] if r["domain"] == domain]
    print(f"kept {len(result['kept'])} (score>=0.60) across {result['n_domains']} domains; "
          f"rejected {len(result['rejected'])} metaphor/low-score")
    print("## Top imports")
    for r in result["kept"][:8]:
        print(f"  [{r['domain']}] {r['score']:.2f}  {r['mechanism'][:140]}")
    print("## Rejected (metaphor-only)")
    for r in result["rejected"][:5]:
        print(f"  [{r['domain']}] {r['score']:.2f}  {r['mechanism'][:120]}")
    return 0 if result["ok"] else 1


def cmd_simulate(domain: str = "gtm", scenario: str = "") -> int:
    out = euler(domain, scenario or None)
    if not out.get("ok"):
        print(out.get("error", "simulate failed"))
        return 1
    print(f"domain={out['domain']} dt={out['dt']}d horizon={out['horizon']}d")
    print(out["note"])
    for name, run in out["runs"].items():
        h = run["health"]
        print(f"  {name:20} {h}: {run['health_start']:.3f} → {run['health_end']:.3f}")
    print(f"volume-is-trap: {out['trap']}  rank6-beats-volume: {out['rank6_beats_volume']}")
    return 0





def cmd_pack() -> int:
    p = PKG / "references" / "recall-pack.md"
    if not p.is_file():
        print("recall-pack.md missing")
        return 1
    print(p)
    print("=" * 60)
    print("\n".join(p.read_text().splitlines()[:60]))
    return 0


def _capture(fn, *a, **kw) -> str:
    import io
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        fn(*a, **kw)
    finally:
        sys.stdout = old
    return buf.getvalue()


def cmd_run(
    problem: str,
    domain: str = "",
    choose_rank: int = 6,
    context: str = "disorder",
) -> int:
    """8-phase DET path. An unclassified decision context remains red."""
    from datetime import datetime
    slug = re.sub(r"[^a-z0-9]+", "-", problem.lower())[:40].strip("-") or "run"
    run = Path.home() / ".rig" / "systems-studio" / "runs" / f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-det-{slug}"
    run.mkdir(parents=True, exist_ok=True)
    (run / "problem.txt").write_text(problem + "\n")
    findings: list[str] = []

    (run / "brief.md").write_text(
        f"## Problem\n{problem}\n\n## Success looks like\n"
        f"Named archetype, ranked leverage (not 12), cited knowledge, "
        f"polymath imports with transfer >= 0.60, Euler on the health stock, dated falsifier.\n"
        f"Domain: {domain or 'generic'}\n"
    )

    frame_src = PKG / "templates" / "frames" / f"{domain}.md" if domain else PKG / "templates" / "system-frame.md"
    if not frame_src.is_file():
        frame_src = PKG / "templates" / "system-frame.md"
    (run / "frame.md").write_text(
        frame_src.read_text().replace("<SYSTEM>", problem[:80])
        + f"\n\n## Run note\nDET fill from `{frame_src.name}` for: {problem}\n"
    )
    contexts = {item["id"]: item for item in load("decision-contexts.json")["contexts"]}
    context_item = contexts.get(context)
    if context_item is None:
        findings.append(f"FAIL context: unknown context {context!r}")
        context_item = contexts["disorder"]
    elif context == "disorder":
        findings.append("FAIL context: DISORDER must be decomposed before leverage")
    else:
        findings.append(f"PASS context: {context} → {context_item['response']}")
    (run / "context.md").write_text(
        f"## Context\n{context_item['id']}\n\n"
        f"## Confidence\nDeclared by requester; validate against observed causal evidence before action.\n\n"
        f"## Response mode\n{context_item['response']}\n\n"
        f"## Required artifacts\n{context_item['required_artifact']}\n\n"
        f"## Rationale\n{context_item['method']}\n"
    )

    mapped = score_map(problem)
    if not mapped:
        findings.append("FAIL diagnosis: zero archetype matches")
        (run / "diagnosis.md").write_text(
            "## Suspect\nNONE — zero symptom matches.\n\n## Evidence\n"
            "data/archetypes.json returned no hits.\n\n## Counterintuitive\n"
            "A map with no suspect is not a diagnosis. Widen verbs+nouns.\n"
        )
    else:
        top = mapped[0]
        findings.append(f"PASS diagnosis: {top['name']} n={top['n']} {top['confidence']}")
        body = "\n".join(
            f"- {a['name']} [{a['confidence']}] hits={a['hits'][:5]}" for a in mapped[:3]
        )
        (run / "diagnosis.md").write_text(
            f"## Suspect\n{top['name']} ({top['id']}) — {top['confidence']}\n\n"
            f"## Evidence\n{body}\n\n"
            f"## Counterintuitive\n{top['counterintuitive']}\n\n"
            f"Intervention: {top['intervention']}\n"
        )

    chosen_rank = choose_rank
    rejected_12 = chosen_rank != 12
    if chosen_rank == 12:
        findings.append("FAIL leverage: Chosen is rank 12 with no rejection")
    else:
        findings.append(f"PASS leverage: Chosen rank {chosen_rank}; rank 12 rejected")
    (run / "leverage.md").write_text(
        f"## Current rank\nDefault trap is rank 12 (parameters / more volume).\n\n"
        f"## Chosen\nRank {chosen_rank} — information flows (who sees the delayed consequence).\n"
        f"Authority: advise only, Gate-D untouched.\n\n"
        f"## Rejected\nRank 12 (more volume / more agents / more parameters) — "
        f"{'explicitly rejected' if rejected_12 else 'NOT REJECTED — RED'}.\n"
        f"\n## Decision context\n{context_item['id']} → {context_item['response']}. "
        f"Required: {context_item['required_artifact']}.\n"
    )

    know = retrieve_knowledge(problem, k=5)
    cites = []
    for h in know["hits"]:
        url = h["source"] or h["path"]
        cites.append(f"- [{h['kind']}: {h['title']}]({url}) overlap={h['overlap']}")
    if not know["ok"]:
        findings.append(f"FAIL grounding: only {len(know['hits'])} knowledge hits (need >=2)")
    else:
        findings.append(f"PASS grounding: {len(know['hits'])} knowledge hits scanned={know['n_scanned']}")
    cards = _capture(cmd_cards, domain if domain in VOCAB else "systems-thinking")
    (run / "grounding.md").write_text(
        f"## Citations\n" + ("\n".join(cites) if cites else "(none)") + "\n\n"
        f"## Index snapshot\n```\n{cards[:1800]}```\n\n"
        f"## Gaps\nLive Recall not invoked on DET path. "
        f"{'Knowledge library covered this.' if know['ok'] else 'Knowledge library too thin — RED.'}\n"
    )

    xp = score_crosspoll(problem)
    top_lines = [
        f"| {r['domain']} | {r['score']:.2f} | {r['structural']:.2f} | {r['clarity']:.2f} | {r['testability']:.2f} | {r['mechanism'][:100]} |"
        for r in xp["kept"][:8]
    ]
    rej_lines = [
        f"- [{r['domain']}] {r['score']:.2f} {r['mechanism'][:120]}"
        for r in xp["rejected"][:6]
    ]
    if not xp["ok"]:
        findings.append(f"FAIL polymath: kept={xp['n_kept']} domains={xp['n_domains']} (need >=3 each, score>=0.60)")
    else:
        findings.append(f"PASS polymath: kept={xp['n_kept']} domains={xp['n_domains']}")
    (run / "polymath.md").write_text(
        f"## Target structure\n{problem}\n\n"
        f"## Candidate imports\n| domain | score | struct | clarity | test | mechanism |\n"
        f"|---|---|---|---|---|---|\n" + "\n".join(top_lines) + "\n\n"
        f"## Top imports\nTransfer = structural × clarity × testability. Keep >= 0.60.\n"
        + "\n".join(f"- {r['domain']}: {r['score']:.2f}" for r in xp["kept"][:3]) + "\n\n"
        f"## Rejected (metaphor-only)\n" + ("\n".join(rej_lines) or "- none") + "\n"
    )

    sim_block = "no domain model — skipped"
    if domain:
        sim = euler(domain)
        if sim.get("ok"):
            rows = [
                f"- {name}: {r['health']} {r['health_start']:.3f} → {r['health_end']:.3f}"
                for name, r in sim["runs"].items()
            ]
            sim_block = (
                f"{sim['note']}\n" + "\n".join(rows)
                + f"\nvolume-is-trap: {sim['trap']}\nrank6-beats-volume: {sim['rank6_beats_volume']}"
            )
            if sim["trap"]:
                findings.append("PASS simulate: +40% volume does not raise the health stock (trap confirmed)")
            else:
                findings.append("WATCH simulate: volume was not a trap in this model")
            if sim["rank6_beats_volume"]:
                findings.append("PASS simulate: rank-6 information beats volume")
        else:
            findings.append(f"FAIL simulate: {sim.get('error')}")
            sim_block = str(sim)

    (run / "DELIVERABLE.md").write_text(
        f"## What is happening\n{problem}\n\n"
        + (f"Suspect: {mapped[0]['name']}.\n" if mapped else "Suspect: NONE.\n")
        + f"\n## What to do\n1. Chosen leverage rank {chosen_rank} (information), not 12.\n"
        f"2. Do not add volume until the named balancing loop is instrumented.\n"
        f"3. Owner: requester. Studio advises; Gate-D still owns outward action.\n\n"
        f"## Simulation\n{sim_block}\n\n"
        f"## Falsifier\nIf the health stock does not move within 14 days of the intervention, "
        f"this analysis is wrong. Date: run `{run.name}`.\n\n"
        f"## Rejected\nRank-12 parameter tweaks. Metaphor-only polymath imports (score < 0.60).\n"
    )

    required = ["brief.md", "frame.md", "context.md", "diagnosis.md", "leverage.md",
                "grounding.md", "polymath.md", "DELIVERABLE.md"]
    headings = {
        "brief.md": ["## Problem", "## Success looks like"],
        "context.md": ["## Context", "## Confidence", "## Response mode", "## Required artifacts"],
        "diagnosis.md": ["## Suspect", "## Evidence", "## Counterintuitive"],
        "leverage.md": ["## Chosen", "## Rejected"],
        "grounding.md": ["## Citations", "## Gaps"],
        "polymath.md": ["## Target structure", "## Top imports", "## Rejected (metaphor-only)"],
        "DELIVERABLE.md": ["## What is happening", "## What to do", "## Falsifier", "## Rejected"],
    }
    lines = [f"== systems-studio DET verify {run.name}"]
    ok = True
    for f in required:
        p = run / f
        if not p.is_file() or p.stat().st_size == 0:
            lines.append(f"FAIL {f} missing/empty")
            ok = False
            continue
        body = p.read_text()
        miss = [h for h in headings.get(f, []) if h not in body]
        if miss:
            lines.append(f"FAIL {f} missing {miss}")
            ok = False
        else:
            lines.append(f"PASS {f} ({len(body.splitlines())} lines)")
    for note in findings:
        lines.append(note)
        if note.startswith("FAIL"):
            ok = False
    lines.append("RUN GREEN" if ok else "RUN RED")
    (run / "verify.log").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"run dir: {run}")
    return 0 if ok else 1


def main() -> int:
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 0
    cmd, args = a[0], a[1:]
    if cmd == "doctor":
        return cmd_doctor()
    if cmd == "frame":
        domain = ""
        name_parts = []
        i = 0
        while i < len(args):
            if args[i] == "--domain" and i + 1 < len(args):
                domain = args[i + 1]
                i += 2
                continue
            name_parts.append(args[i])
            i += 1
        return cmd_frame(" ".join(name_parts), domain)
    if cmd == "map":
        return cmd_map(" ".join(args)) if args else (print("usage: studio map \"<symptom text>\""), 2)[1]
    if cmd == "archetype":
        return cmd_archetype(args[0] if args else "all")
    if cmd == "leverage":
        r = "all"
        if "--rank" in args:
            i = args.index("--rank")
            r = args[i + 1] if i + 1 < len(args) else "all"
        return cmd_leverage(r)
    if cmd == "cards":
        grep = ""
        if "--grep" in args:
            i = args.index("--grep")
            grep = args[i + 1] if i + 1 < len(args) else ""
            del args[i:i + 2]
        return cmd_cards(args[0] if args else "", grep)
    if cmd == "card":
        return cmd_card(" ".join(args)) if args else (
            print('usage: studio card "<title fragment>"'),
            2,
        )[1]
    if cmd == "mechanisms":
        return cmd_mechanisms(" ".join(args))
    if cmd == "context":
        return cmd_context(args[0] if args else "all")
    if cmd == "operating":
        return cmd_operating(args[0] if args else "daily")
    if cmd == "search":
        if not args:
            print("usage: studio search \"<query>\" [focused|exhaustive]")
            return 2
        if args[-1] in ("focused", "exhaustive"):
            q = " ".join(args[:-1])
            mode = args[-1]
        else:
            q = " ".join(args)
            mode = "focused"
        return cmd_search(q, mode)
    if cmd == "crosspoll":
        return cmd_crosspoll(" ".join(args[:-1]), args[-1]) if len(args) > 1 else (cmd_crosspoll(" ".join(args)) if args else (print("usage: studio crosspoll \"<target structure>\" [domain]"), 2)[1])
    if cmd == "pack":
        return cmd_pack()
    if cmd == "simulate":
        domain = args[0] if args else "gtm"
        scenario = args[1] if len(args) > 1 else ""
        return cmd_simulate(domain, scenario)
    if cmd == "run":
        domain = ""
        choose_rank = 6
        context = "disorder"
        parts = []
        i = 0
        while i < len(args):
            if args[i] == "--domain" and i + 1 < len(args):
                domain = args[i + 1]
                i += 2
                continue
            if args[i] == "--choose-rank" and i + 1 < len(args):
                choose_rank = int(args[i + 1])
                i += 2
                continue
            if args[i] == "--context" and i + 1 < len(args):
                context = args[i + 1]
                i += 2
                continue
            parts.append(args[i])
            i += 1
        if not parts:
            print(
                "usage: studio run \"<problem>\" "
                "[--domain gtm|linkedin|sales|founder|mike-os] "
                "[--context clear|complicated|complex|chaotic] [--choose-rank N]"
            )
            return 2
        return cmd_run(" ".join(parts), domain, choose_rank, context)
    print(__doc__)
    return 2


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
