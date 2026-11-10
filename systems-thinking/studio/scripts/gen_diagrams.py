#!/usr/bin/env python3
"""Generate Excalidraw + SVG diagrams for the Systems Thinking Studio.

Diagrams (written to <out>/, default ./diagrams):
  studio-map        all RIG studios; systems-thinking BUILT + exploded 8-phase chain
  phases-flow       8-phase chain with GREEN/RED gates and retry<=2 loops
  polymath-wheel    10 polymath domains -> TARGET SYSTEM STRUCTURE (transfer gate)
  knowledge-pipeline corpus(853) + ytsearch -> scrape -> raw -> distill -> GROUND

Pure stdlib. Deterministic: every element seed derives from a stable key,
so reruns produce byte-identical output.

Usage: python3 gen_diagrams.py [--out diagrams]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

# ---------------------------------------------------------------- palette ---
INK = "#1e1e1e"
GRAY_TXT = "#495057"
BUILT_FILL, BUILT_STROKE = "#a5d8ff", "#1971c2"
PANEL_FILL = "#e7f5ff"
PHASE_FILL = "#d0ebff"
NEXT_FILL, NEXT_STROKE = "#f1f3f5", "#adb5bd"
GATE_FILL, GATE_STROKE = "#fff9db", "#e8590c"
GREEN = "#2f9e44"
AMBER = "#e8890c"
RED = "#e03131"
PURP_FILL, PURP_STROKE = "#d0bfff", "#6741d9"
DET_C, AGENT_C, MIX_C = "#2f9e44", "#7048e8", "#0b7285"

# Phases of the vertical slice (harness + polymath-domains.json contract).
PHASES = [
    ("01", "INTAKE", "[agent+template]", "brief.md",
     "out: ## Problem · ## Success looks like", "stakes, constraints, deadline, requester"),
    ("02", "FRAME", "[det+agent]", "frame.md",
     "studio frame CLI · Stocks · Reinforcing + Balancing loops · Delay", "'Unknown' is an answer; blank is not"),
    ("03", "DIAGNOSE", "[det+agent]", "diagnosis.md",
     "studio map · ## Suspect · ## Evidence · ## Counterintuitive point", "verify the archetype's predicted stock moves"),
    ("04", "LEVERAGE", "[det+agent]", "leverage.md",
     "studio leverage · rank 12->1 · ## Chosen · ## Rejected higher option", "highest rank the requester's authority allows"),
    ("05", "GROUND", "[det+agent]", "grounding.md",
     "corpus + knowledge/ + live search · ## Citations · ## Gaps", "absent evidence is a finding"),
    ("06", "POLYMATH", "[agent+data]", "polymath.md",
     "10 domains x mechanisms · transfer score >= 0.60 · top 3 imports", "metaphor-only imports REJECTED"),
    ("07", "SYNTHESIZE", "[agent]", "DELIVERABLE.md",
     "## What is happening · ## What to do · ## Falsifier · ## Rejected", "no new claims beyond grounding"),
    ("08", "VERIFY", "[det]", "verify.log",
     "checks only · artifacts present · citations resolve · falsifier dated", "DEGRADED ships honest failure, not silence"),
]

DOMAINS = [
    ("physics", "entropy · phase transitions"),
    ("biology", "selection · Red Queen · niches"),
    ("economics", "incentive gradients · lock-in"),
    ("mathematics", "Perron-Frobenius · spectral gap"),
    ("engineering", "feedback · graceful degradation"),
    ("psychology", "prospect theory · reactance"),
    ("strategy-military", "OODA · Schwerpunkt · Auftrag"),
    ("learning-meta", "deliberate practice · spacing"),
    ("complexity", "power laws · SOC · modularity"),
    ("philosophy", "first principles · via negativa"),
]

NEXT_STUDIOS = ["GTM", "LinkedIn", "Sales", "Content", "Film",
                "Research", "Design", "Data", "Finance"]

FONT = "Virgil, 'Segoe Print', 'Comic Sans MS', cursive"
LH = 1.25


def _seed(key: str) -> int:
    return int.from_bytes(hashlib.sha256(key.encode()).digest()[:4], "big") % (2 ** 31)


def _text_size(lines: list[str], size: int) -> tuple[float, float]:
    w = max(len(ln) for ln in lines) * size * 0.58 + size * 0.6
    h = len(lines) * size * LH
    return round(w, 2), round(h, 2)


def _xml(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


class Canvas:
    """Accumulates elements; renders Excalidraw JSON + SVG with same geometry."""

    def __init__(self, name: str):
        self.name = name
        self.elements: list[dict] = []
        self._n = 0

    def _eid(self, kind: str) -> str:
        self._n += 1
        return f"{self.name}-{kind}-{self._n:03d}"

    def _base(self, eid: str, etype: str) -> dict:
        return {
            "id": eid, "type": etype, "x": 0, "y": 0, "width": 0, "height": 0,
            "angle": 0, "strokeColor": INK, "backgroundColor": "transparent",
            "fillStyle": "solid", "strokeWidth": 2, "roughness": 1, "opacity": 100,
            "groupIds": [], "frameId": None, "roundness": None,
            "seed": _seed(eid), "version": 1, "versionNonce": _seed(eid + ":n"),
            "isDeleted": False, "boundElements": [], "updated": 1,
            "link": None, "locked": False,
        }

    # -- primitives ---------------------------------------------------------
    def rect(self, x, y, w, h, *, fill, stroke=INK, opacity=100, sw=2, rot=0.0):
        eid = self._eid("rect")
        el = self._base(eid, "rectangle")
        el.update(x=round(x, 2), y=round(y, 2), width=round(w, 2), height=round(h, 2),
                  strokeColor=stroke, backgroundColor=fill, strokeWidth=sw,
                  opacity=opacity, angle=rot, roundness={"type": 3})
        self.elements.append(el)
        return el

    def diamond(self, cx, cy, size, *, fill=GATE_FILL, stroke=GATE_STROKE):
        """Decision gate: a 45-deg rotated square."""
        return self.rect(cx - size / 2, cy - size / 2, size, size,
                         fill=fill, stroke=stroke, rot=math.pi / 4)

    def text(self, cx, cy, lines, size=20, color=INK, key=None):
        if isinstance(lines, str):
            lines = lines.split("\n")
        eid = key or self._eid("text")
        w, h = _text_size(lines, size)
        el = self._base(eid, "text")
        el.update(x=round(cx - w / 2, 2), y=round(cy - h / 2, 2), width=w, height=h,
                  strokeColor=color, backgroundColor="transparent",
                  fontSize=size, fontFamily=1, textAlign="center",
                  verticalAlign="middle", text="\n".join(lines),
                  originalText="\n".join(lines), lineHeight=LH, containerId=None)
        self.elements.append(el)
        return el

    def arrow(self, pts: list[tuple[float, float]], *, color=INK, sw=2):
        """pts: absolute polyline, first point is the start."""
        eid = self._eid("arrow")
        el = self._base(eid, "arrow")
        rel = [[round(px - pts[0][0], 2), round(py - pts[0][1], 2)] for px, py in pts]
        xs = [p[0] for p in rel]
        ys = [p[1] for p in rel]
        el.update(x=round(pts[0][0], 2), y=round(pts[0][1], 2),
                  width=round(max(xs) - min(xs), 2), height=round(max(ys) - min(ys), 2),
                  strokeColor=color, backgroundColor="transparent", strokeWidth=sw,
                  points=rel, lastCommittedPoint=None, startArrowhead=None,
                  endArrowhead="arrow", startBinding=None, endBinding=None,
                  roundness={"type": 2})
        self.elements.append(el)
        return el

    # -- derived helpers ----------------------------------------------------
    def box(self, x, y, w, h, lines, *, fill, stroke=INK, opacity=90,
            title_size=20, sub_size=16, sub_color=GRAY_TXT, sw=2):
        """Box with a bold first line + smaller sub-lines, centered."""
        self.rect(x, y, w, h, fill=fill, stroke=stroke, opacity=opacity, sw=sw)
        cx = x + w / 2
        n = len(lines)
        gap = title_size * LH
        top_cy = y + h / 2 - ((n - 1) * (sub_size * LH + 4)) / 2
        self.text(cx, top_cy, lines[0], title_size, color=INK)
        cy = top_cy + gap + 4
        for ln in lines[1:]:
            self.text(cx, cy, ln, sub_size, color=sub_color)
            cy += sub_size * LH + 4

    def link(self, a: dict, b: dict, *, color=INK, sw=2, label=None,
             label_dx=0, label_dy=-16, label_size=16, label_color=GRAY_TXT):
        """Straight arrow from rect a's edge toward rect b's edge."""
        p1 = edge_toward(a, *center(b))
        p2 = edge_toward(b, *center(a))
        self.arrow([p1, p2], color=color, sw=sw)
        if label:
            mx, my = (p1[0] + p2[0]) / 2 + label_dx, (p1[1] + p2[1]) / 2 + label_dy
            self.text(mx, my, label, label_size, color=label_color)

    # -- output -------------------------------------------------------------
    def excalidraw(self) -> dict:
        return {
            "type": "excalidraw", "version": 2,
            "source": "systems-thinking-studio",
            "elements": self.elements,
            "appState": {"viewBackgroundColor": "#ffffff"},
            "files": {},
        }

    def svg(self, pad=50) -> str:
        xs = [e["x"] for e in self.elements] + [e["x"] + e["width"] for e in self.elements]
        ys = [e["y"] for e in self.elements] + [e["y"] + e["height"] for e in self.elements]
        minx, miny = min(xs) - pad, min(ys) - pad
        w, h = max(xs) - min(xs) + 2 * pad, max(ys) - min(ys) + 2 * pad
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{minx:.0f} {miny:.0f} {w:.0f} {h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" font-family="{FONT}">',
            f'<rect x="{minx:.0f}" y="{miny:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#ffffff"/>',
            "<defs>",
        ]
        for c in sorted({e["strokeColor"] for e in self.elements if e["type"] == "arrow"}):
            out.append(
                f'<marker id="ah-{c[1:]}" markerWidth="9" markerHeight="9" refX="7" refY="4" '
                f'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{c}"/></marker>')
        out.append("</defs>")
        for e in self.elements:
            op = e["opacity"] / 100
            if e["type"] == "rectangle":
                fill = e["backgroundColor"]
                t = ""
                if e["angle"]:
                    cx, cy = e["x"] + e["width"] / 2, e["y"] + e["height"] / 2
                    t = f' transform="rotate({math.degrees(e["angle"]):.1f} {cx:.0f} {cy:.0f})"'
                out.append(
                    f'<rect x="{e["x"]:.0f}" y="{e["y"]:.0f}" width="{e["width"]:.0f}" '
                    f'height="{e["height"]:.0f}" rx="10" fill="{fill}" fill-opacity="{op:.2f}" '
                    f'stroke="{e["strokeColor"]}" stroke-width="{e["strokeWidth"]}"{t}/>')
            elif e["type"] == "text":
                lines = e["text"].split("\n")
                fs, lh = e["fontSize"], e["fontSize"] * LH
                y0 = e["y"] + e["height"] / 2 - (len(lines) - 1) * lh / 2 + fs * 0.35
                cx = e["x"] + e["width"] / 2
                spans = "".join(
                    f'<tspan x="{cx:.0f}" dy="{0 if i == 0 else lh:.0f}">{_xml(ln)}</tspan>'
                    for i, ln in enumerate(lines))
                out.append(
                    f'<text x="{cx:.0f}" y="{y0:.0f}" font-size="{fs}" fill="{e["strokeColor"]}" '
                    f'text-anchor="middle">{spans}</text>')
            elif e["type"] == "arrow":
                pts = [(e["x"] + dx, e["y"] + dy) for dx, dy in e["points"]]
                d = "M " + " L ".join(f"{px:.0f} {py:.0f}" for px, py in pts)
                out.append(
                    f'<path d="{d}" fill="none" stroke="{e["strokeColor"]}" '
                    f'stroke-width="{e["strokeWidth"]}" stroke-linecap="round" '
                    f'stroke-linejoin="round" marker-end="url(#ah-{e["strokeColor"][1:]})"/>')
        out.append("</svg>")
        return "\n".join(out)


def center(r: dict) -> tuple[float, float]:
    return r["x"] + r["width"] / 2, r["y"] + r["height"] / 2


def edge_toward(r: dict, tx: float, ty: float) -> tuple[float, float]:
    """Point where the segment rect-center -> (tx,ty) crosses the rect edge."""
    cx, cy = center(r)
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    sx = (r["width"] / 2) / abs(dx) if dx else math.inf
    sy = (r["height"] / 2) / abs(dy) if dy else math.inf
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


# ------------------------------------------------------------- diagrams ----
def studio_map(c: Canvas):
    c.text(330, 60, "RIG STUDIOS — process inventory map", 28)
    c.text(430, 104, "Systems Thinking Studio: BUILT 2026-08-28 · every studio gets the same "
                     "filesystem doctrine", 16, GRAY_TXT)

    # "next" studios: 2-col x 5-row grid of lighter boxes
    for i, name in enumerate(NEXT_STUDIOS):
        col, row = divmod(i, 5)
        x, y = 70 + col * 246, 170 + row * 92
        r = c.rect(x, y, 222, 66, fill=NEXT_FILL, stroke=NEXT_STROKE, opacity=55, sw=1)
        cx, _ = center(r)
        c.text(cx, y + 26, f"{name} Studio", 20)
        c.text(cx, y + 50, "next", 16, GRAY_TXT)

    # systems-thinking panel with exploded 8-phase chain
    c.rect(620, 170, 640, 1010, fill=PANEL_FILL, stroke=BUILT_STROKE, opacity=70, sw=2)
    c.text(940, 214, "SYSTEMS THINKING STUDIO — BUILT", 24, BUILT_STROKE)
    c.text(940, 246, "harness/systems-studio.sh · 8 phases · ~/.rig/systems-studio/runs/",
           16, GRAY_TXT)
    for i, (num, name, _m, artifact, _c1, _c2) in enumerate(PHASES):
        y = 286 + i * 106
        r = c.rect(690, y, 500, 74, fill=PHASE_FILL, stroke=BUILT_STROKE, opacity=90)
        cx, _ = center(r)
        c.text(cx, y + 37, f"{num} {name}  →  {artifact}", 20)
        if i < 7:
            c.arrow([(940, y + 74), (940, y + 106)], color=BUILT_STROKE)

    # legend + doctrine
    c.rect(70, 700, 40, 28, fill=BUILT_FILL, stroke=BUILT_STROKE)
    c.text(300, 714, "BUILT — this package (highlighted)", 16)
    c.rect(70, 744, 40, 28, fill=NEXT_FILL, stroke=NEXT_STROKE, opacity=55)
    c.text(300, 758, "NEXT — same shape, awaiting build", 16)
    c.text(340, 830, "studio-as-filesystem doctrine (each studio):\n"
                     "tools (deterministic CLI) + data (cited, versioned)\n"
                     "+ knowledge (distilled sources) + processes (phases)\n"
                     "+ harness (phase-gated runner) + agents (integration)\n"
                     "+ models.md (routing) + SKILL.md (agent entry)", 16, GRAY_TXT)
    c.text(340, 985, "every phase: agent call → deterministic check\n"
                     "→ retry ≤2 with feedback → advance only on GREEN", 16, BUILT_STROKE)


def phases_flow(c: Canvas):
    c.text(700, 46, "SYSTEMS-STUDIO VERTICAL SLICE — 8 phases, gated", 28)
    c.text(700, 88, "each phase receives all prior artifacts as inputs · gates run the "
                    "deterministic checks on each artifact", 16, GRAY_TXT)

    cx, bw, bh = 700, 660, 132
    pitch, top0 = 272, 130
    for i, (num, name, marker, artifact, checks, note) in enumerate(PHASES):
        top = top0 + i * pitch
        x = cx - bw / 2
        fill = "#fff3bf" if num == "08" else PHASE_FILL
        stroke = GATE_STROKE if num == "08" else BUILT_STROKE
        c.rect(x, top, bw, bh, fill=fill, stroke=stroke)
        mcolor = DET_C if marker == "[det]" else AGENT_C if marker == "[agent]" else MIX_C
        tw = _text_size([f"{num} {name}"], 26)[0]
        c.text(cx, top + 30, f"{num} {name}", 26)
        c.text(cx + tw / 2 + 100, top + 30, marker, 16, mcolor)
        c.text(cx, top + 68, f"→ {artifact}", 16, GRAY_TXT)
        c.text(cx, top + 94, checks, 16, GRAY_TXT)
        c.text(cx, top + 116, note, 16, GRAY_TXT)
        if i == 7:
            c.text(cx, top + 185, "output: run dir (brief … DELIVERABLE, verify.log) — "
                                  "promotable to any repo's docs/", 16, BUILT_STROKE)
            continue
        # gate diamond between this phase and the next
        gy = top + bh + 72
        c.diamond(cx, gy, 64)
        c.text(cx, gy, str(i + 1), 16, GATE_STROKE)
        c.arrow([(cx, gy + 47), (cx, top + pitch)], color=GREEN)          # GREEN advance
        c.text(cx + 96, gy + 14, "GREEN → advance", 16, GREEN)
        # retry loop (elbow, left side, back into this phase)
        dy = (top + bh / 2) - gy
        c.arrow([(cx - 46, gy), (cx - 156, gy), (cx - 156, gy + dy), (x - 6, gy + dy)],
                color=AMBER)
        c.text(cx - 216, gy + 26, "retry ≤2\n(+feedback)", 16, AMBER)
        # RED exit (right side)
        c.arrow([(cx + 46, gy), (cx + 150, gy)], color=RED)
        c.text(cx + 400, gy, "RED after 3 — stop · log · surface\n"
                             "no phase advances on red", 16, RED)


def polymath_wheel(c: Canvas):
    ccx, ccy, R = 800, 680, 420
    c.text(800, 50, "POLYMATH WHEEL — cross-domain mechanism import (phase 06)", 28)
    c.text(800, 92, "RIG-COLLIDER: import mechanisms from unrelated domains; "
                    "name the TARGET system's structure, not just the metaphor", 16, GRAY_TXT)

    node = c.rect(ccx - 190, ccy - 68, 380, 136, fill=PURP_FILL, stroke=PURP_STROKE, sw=3)
    c.text(ccx, ccy - 30, "TARGET SYSTEM STRUCTURE", 22, PURP_STROKE)
    c.text(ccx, ccy + 6, "from frame.md", 16, GRAY_TXT)
    c.text(ccx, ccy + 34, "the stock · the loop · the constraint", 16, GRAY_TXT)

    for i, (dom, mechs) in enumerate(DOMAINS):
        theta = math.radians(-90 + i * 36)
        bx, by = ccx + R * math.cos(theta), ccy + R * math.sin(theta)
        r = c.rect(bx - 150, by - 36, 300, 72, fill=PHASE_FILL, stroke=BUILT_STROKE, opacity=90)
        c.text(bx, by - 13, dom, 20)
        c.text(bx, by + 15, mechs, 16, GRAY_TXT)
        c.link(r, node, sw=2)

    c.rect(70, 1180, 600, 150, fill="#fff4e6", stroke=AMBER, opacity=80)
    c.text(370, 1210, "TRANSFER-SCORE GATE (SIS)", 20, AMBER)
    c.text(370, 1238, "structural-similarity × mechanism-clarity × testability", 16)
    c.text(370, 1264, "keep candidates with product ≥ 0.60", 16)
    c.text(370, 1290, "3+ non-native domains · keep top 3 imports", 16, GRAY_TXT)
    c.text(370, 1316, "each import names a measurable change", 16, GRAY_TXT)

    c.rect(930, 1180, 600, 150, fill="#f8f9fa", stroke=NEXT_STROKE, opacity=80)
    c.text(1230, 1210, "PROTOCOL — data/polymath-domains.json", 20)
    c.text(1230, 1238, "state target structure → pick 3+ domains", 16, GRAY_TXT)
    c.text(1230, 1264, "import: 'in <target>, <mechanism> implies <intervention>'", 16, GRAY_TXT)
    c.text(1230, 1290, "top 3 imports must name measurable changes", 16, GRAY_TXT)
    c.text(1230, 1316, "metaphor-only imports → REJECTED", 16, RED)


def knowledge_pipeline(c: Canvas):
    c.text(940, 46, "KNOWLEDGE PIPELINE — corpus to GROUND", 28)
    c.text(940, 88, "corpus(853) + ytsearch(12 domains) → scrape → raw transcripts → "
                    "distill(swarm) → knowledge/ cards → phase 05 GROUND", 16, GRAY_TXT)

    bw, bh = 380, 130

    def node_box(x, y, title, subs, *, fill, stroke=BUILT_STROKE, sw=2):
        r = c.rect(x, y, bw, bh, fill=fill, stroke=stroke, sw=sw)
        mx = x + bw / 2
        c.text(mx, y + 26, title, 20)
        c.text(mx, y + 56, subs[0], 16, GRAY_TXT)
        c.text(mx, y + 84, subs[1], 16, GRAY_TXT)
        if len(subs) > 2:
            c.text(mx, y + 112, subs[2], 16, GRAY_TXT)
        return r

    corpus = node_box(70, 150, "RECALL CORPUS",
                      ["853 tagged cards · 17-tag vocabulary", "data/card-index.json"],
                      fill=PHASE_FILL)
    yt = node_box(70, 430, "YTSEARCH SWEEPS",
                  ["yt-dlp ytsearch · 12 polymath domains",
                   "Meadows · Senge · Ackoff · Goldratt"], fill=PHASE_FILL)
    scrape = node_box(540, 150, "SCRAPE",
                      ["scripts/studio_scrape_youtube.py",
                       "enumerate → fetch auto-captions",
                       "dedup · scrape-manifest.jsonl"], fill=PANEL_FILL)
    raw = node_box(540, 430, "RAW TRANSCRIPTS",
                   ["knowledge/youtube/raw/<id>.txt",
                    "VTT → timestamped text (provenance)"], fill=PANEL_FILL)
    distill = node_box(1010, 150, "DISTILL (swarm)",
                       ["per-video distillation → cards",
                        "## Procedure / models + timestamps"], fill=PANEL_FILL)
    know = node_box(1010, 430, "KNOWLEDGE CARDS",
                    ["knowledge/{youtube,papers,books}",
                     "manifests mounted as harness --input"], fill=PHASE_FILL)

    ground = c.rect(1460, 260, 360, 170, fill=BUILT_FILL, stroke=BUILT_STROKE, sw=3)
    c.text(1640, 292, "05 GROUND", 22, BUILT_STROKE)
    c.text(1640, 326, "citations: [Card: title](url)", 16)
    c.text(1640, 354, "## Gaps — absent evidence is a finding", 16, GRAY_TXT)
    c.text(1640, 382, "feeds 07 SYNTHESIZE → 08 VERIFY", 16, GRAY_TXT)

    c.link(corpus, scrape)
    c.link(yt, scrape)
    c.link(scrape, raw)
    c.link(raw, distill)
    c.link(distill, know)
    c.link(know, ground)

    c.text(940, 640, "edges: corpus contributes every youtube URL · ytsearch sweeps 6 "
                     "queries/domain · scrape = auto-captions + dedup · distill keeps raw "
                     "for provenance", 16, GRAY_TXT)
    c.text(940, 680, "first pass: 20 cards scraped OK (12 from corpus + 8 canon) · hard cap 20 "
                     "reached · distillation is a separate step (studio_distill.py)", 16, GRAY_TXT)


DIAGRAMS = {
    "studio-map": studio_map,
    "phases-flow": phases_flow,
    "polymath-wheel": polymath_wheel,
    "knowledge-pipeline": knowledge_pipeline,
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="diagrams", help="output directory (default: diagrams)")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        c = Canvas(name)
        fn(c)
        ex, svg = out / f"{name}.excalidraw", out / f"{name}.svg"
        ex.write_text(json.dumps(c.excalidraw(), indent=1) + "\n")
        svg.write_text(c.svg() + "\n")
        print(f"{name}: {len(c.elements)} elements -> {ex.name}, {svg.name}")


if __name__ == "__main__":
    main()
