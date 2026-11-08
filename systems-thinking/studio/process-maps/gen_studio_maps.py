#!/usr/bin/env python3
"""Emit Excalidraw/SVG + per-phase agent/tool/harness files for the studio."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG = ROOT.parent
INK = "#1e1e1e"
KIND = {"mix": "#d0ebff", "det": "#d3f9d8", "agent": "#e5dbff", "det+judge": "#fff4e6"}
PHASES = [
    {"n": "01", "id": "intake", "name": "INTAKE", "kind": "mix", "agent": "studio-intake", "tool": "brief-template", "art": "brief.md"},
    {"n": "02", "id": "frame", "name": "FRAME", "kind": "mix", "agent": "studio-framer", "tool": "studio frame", "art": "frame.md"},
    {"n": "03", "id": "diagnose", "name": "DIAGNOSE", "kind": "det+judge", "agent": "studio-diagnostician", "tool": "studio map", "art": "diagnosis.md"},
    {"n": "04", "id": "leverage", "name": "LEVERAGE", "kind": "det+judge", "agent": "studio-leverage", "tool": "studio leverage", "art": "leverage.md"},
    {"n": "05", "id": "ground", "name": "GROUND", "kind": "mix", "agent": "studio-researcher", "tool": "studio cards/search", "art": "grounding.md"},
    {"n": "06", "id": "polymath", "name": "POLYMATH", "kind": "mix", "agent": "studio-collider", "tool": "studio crosspoll", "art": "polymath.md"},
    {"n": "07", "id": "synthesize", "name": "SYNTHESIZE", "kind": "agent", "agent": "studio-synthesizer", "tool": "assemble", "art": "DELIVERABLE.md"},
    {"n": "08", "id": "verify", "name": "VERIFY", "kind": "det", "agent": "studio-verifier", "tool": "seal.py", "art": "verify.log"},
]


def seed(key: str) -> int:
    return int.from_bytes(hashlib.sha256(key.encode()).digest()[:4], "big") % (2**31)


def el(eid, typ, x, y, w, h, **kw):
    d = {
        "id": eid, "type": typ, "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": kw.get("stroke", INK),
        "backgroundColor": kw.get("fill", "transparent"),
        "fillStyle": "solid", "strokeWidth": kw.get("sw", 1.5),
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": {"type": 3} if typ != "text" else None,
        "seed": seed(eid), "version": 1, "versionNonce": seed(eid + "n"),
        "isDeleted": False, "boundElements": [], "updated": 1,
        "link": None, "locked": False,
    }
    if typ == "text":
        txt = kw["text"]
        d.update(text=txt, fontSize=kw.get("size", 16), fontFamily=1,
                 textAlign="left", verticalAlign="middle", originalText=txt,
                 lineHeight=1.25, containerId=None)
    if typ == "arrow":
        d.update(points=[[0, 0], [kw["dx"], kw["dy"]]], lastCommittedPoint=None,
                 startArrowhead=None, endArrowhead="arrow",
                 startBinding=None, endBinding=None)
    return d


def write_excalidraw(path: Path, elements: list, w: int, h: int) -> None:
    path.write_text(json.dumps({
        "type": "excalidraw", "version": 2, "source": "systems-thinking-studio",
        "elements": elements, "appState": {"viewBackgroundColor": "#ffffff"}, "files": {},
    }))
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="system-ui,sans-serif">']
    parts.append(f'<rect width="{w}" height="{h}" fill="#fff"/>')
    parts.append('<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#1e1e1e"/></marker></defs>')
    for e in elements:
        if e["type"] == "rectangle":
            parts.append(f'<rect x="{e["x"]}" y="{e["y"]}" width="{e["width"]}" height="{e["height"]}" fill="{e["backgroundColor"]}" stroke="{e["strokeColor"]}" rx="8"/>')
        elif e["type"] == "text":
            y = e["y"] + e["fontSize"]
            for i, line in enumerate(e["text"].split("\n")):
                parts.append(f'<text x="{e["x"]}" y="{y + i * e["fontSize"] * 1.25}" font-size="{e["fontSize"]}" fill="{e["strokeColor"]}">{line.replace("&", "&amp;")}</text>')
        elif e["type"] == "arrow":
            x2 = e["x"] + e["points"][1][0]
            y2 = e["y"] + e["points"][1][1]
            parts.append(f'<line x1="{e["x"]}" y1="{e["y"]}" x2="{x2}" y2="{y2}" stroke="{e["strokeColor"]}" marker-end="url(#ah)"/>')
    parts.append("</svg>")
    path.with_suffix(".svg").write_text("\n".join(parts))


def diagram() -> None:
    w, h = 1860, 520
    els = [
        el("t", "text", 20, 12, 1200, 28, text="Systems Thinking Studio — 8-phase swim lane", size=20),
        el("o", "rectangle", 20, 50, w - 40, 52, fill="#e5dbff"),
        el("ot", "text", 32, 62, 900, 28, text="ORCH systems-studio  ·  retry≤2  ·  never skip VERIFY  ·  never invent sources", size=14),
        el("u", "rectangle", 20, 380, w - 40, 110, fill="#f1f3f5"),
        el("ut", "text", 32, 392, 800, 24, text="tools / programs under each step", size=13),
    ]
    prev = None
    for i, p in enumerate(PHASES):
        x = 36 + i * 225
        els.append(el(f"b{i}", "rectangle", x, 140, 205, 90, fill=KIND[p["kind"]]))
        els.append(el(f"bt{i}", "text", x + 8, 148, 190, 74,
                      text=f"{p['n']} {p['name']}\n{p['kind']}\n{p['agent']}", size=13))
        els.append(el(f"tl{i}", "text", x + 8, 420, 190, 48, text=f"{p['tool']}\n→ {p['art']}", size=12))
        if prev is not None:
            els.append(el(f"a{i}", "arrow", prev, 185, 10, 10, dx=x - prev, dy=0))
        prev = x + 205
    write_excalidraw(ROOT / "studio-8-phase.excalidraw", els, w, h)


def emit_agents() -> None:
    agents = ROOT / "agents"
    tools = ROOT / "tools"
    harness = ROOT / "harnesses"
    for p in (agents, tools, harness):
        p.mkdir(exist_ok=True)
    for ph in PHASES:
        (agents / f"{ph['agent']}.md").write_text(
            f"---\nname: {ph['agent']}\nprocess: systems-studio\nphase: {ph['n']}\n"
            f"kind: {ph['kind']}\nartifact: {ph['art']}\n---\n\n"
            f"# {ph['agent']}\n\nYou own **one phase**: {ph['n']} {ph['name']}.\n"
            f"Kind: **{ph['kind']}**. Tool: `{ph['tool']}`. Artifact: `{ph['art']}`.\n\n"
            f"Hand back to the orchestrator. Do not start the next phase.\n"
            f"Never invent a citation. Gate-D untouched.\n"
        )
        (tools / f"{ph['id']}.yaml").write_text(
            f"name: studio.{ph['id']}\ntype: tool-agent\nprocess: systems-studio\n"
            f"step: {ph['n']}\nwraps: {ph['tool']}\ndone_test: \"{ph['art']} exists and passes section checks\"\n"
        )
        (harness / f"{ph['n']}-{ph['id']}.sh").write_text(
            f"#!/usr/bin/env bash\nset -euo pipefail\n"
            f"echo \"[{ph['n']} {ph['name']}] kind={ph['kind']} agent={ph['agent']} tool={ph['tool']}\"\n"
            f"echo \"artifact: {ph['art']}\"\n"
        )
    (ROOT / "orchestrator.md").write_text(
        "# Orchestrator: systems-studio\n\nWalks 01→08. Det = `studio run`. "
        "Agent = `systems-studio` (frontier). Red VERIFY is a result.\n"
    )


def main() -> None:
    ROOT.mkdir(exist_ok=True)
    diagram()
    emit_agents()
    print("wrote", ROOT / "studio-8-phase.excalidraw")


if __name__ == "__main__":
    main()
