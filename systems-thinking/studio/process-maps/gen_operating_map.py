#!/usr/bin/env python3
"""Generate the full Systems Thinking Studio operating Excalidraw map from data."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PKG = ROOT.parent
DATA = PKG / "data" / "operating-cadence-20260830.json"
INK = "#1e1e1e"
STATUS = {
    "FIXED": "#d3f9d8",
    "PARTIAL": "#fff4e6",
    "MISSING": "#ffe3e3",
    "NOT_READY": "#e5dbff",
}
PHASE_FILL = "#d0ebff"


def seed(value: str) -> int:
    return int.from_bytes(hashlib.sha256(value.encode()).digest()[:4], "big") % (2**31)


def element(eid: str, typ: str, x: float, y: float, w: float, h: float, **kw) -> dict:
    result = {
        "id": eid,
        "type": typ,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": kw.get("stroke", INK),
        "backgroundColor": kw.get("fill", "transparent"),
        "fillStyle": "solid",
        "strokeWidth": kw.get("sw", 1.5),
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": {"type": 3} if typ != "text" else None,
        "seed": seed(eid),
        "version": 1,
        "versionNonce": seed(eid + "n"),
        "isDeleted": False,
        "boundElements": [],
        "updated": 1,
        "link": None,
        "locked": False,
    }
    if typ == "text":
        text = kw["text"]
        result.update(
            text=text,
            fontSize=kw.get("size", 16),
            fontFamily=1,
            textAlign="left",
            verticalAlign="middle",
            originalText=text,
            lineHeight=1.25,
            containerId=None,
        )
    if typ == "arrow":
        result.update(
            points=[[0, 0], [kw["dx"], kw["dy"]]],
            lastCommittedPoint=None,
            startArrowhead=None,
            endArrowhead="arrow",
            startBinding=None,
            endBinding=None,
        )
    return result


def write_map(elements: list[dict], width: int, height: int) -> None:
    excalidraw = {
        "type": "excalidraw",
        "version": 2,
        "source": "systems-thinking-studio",
        "elements": elements,
        "appState": {"viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    target = ROOT / "systems-thinking-operating-system.excalidraw"
    target.write_text(json.dumps(excalidraw))
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="system-ui,sans-serif">',
        '<rect width="100%" height="100%" fill="#ffffff"/>',
        '<defs><marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#1e1e1e"/></marker></defs>',
    ]
    for item in elements:
        if item["type"] == "rectangle":
            svg.append(f'<rect x="{item["x"]}" y="{item["y"]}" width="{item["width"]}" height="{item["height"]}" fill="{item["backgroundColor"]}" stroke="{item["strokeColor"]}" rx="8"/>')
        elif item["type"] == "text":
            base_y = item["y"] + item["fontSize"]
            for index, line in enumerate(item["text"].split("\n")):
                svg.append(f'<text x="{item["x"]}" y="{base_y + index * item["fontSize"] * 1.25}" font-size="{item["fontSize"]}" fill="{item["strokeColor"]}">{html.escape(line)}</text>')
        elif item["type"] == "arrow":
            x2 = item["x"] + item["points"][1][0]
            y2 = item["y"] + item["points"][1][1]
            svg.append(f'<line x1="{item["x"]}" y1="{item["y"]}" x2="{x2}" y2="{y2}" stroke="{item["strokeColor"]}" marker-end="url(#ah)"/>')
    svg.append("</svg>")
    target.with_suffix(".svg").write_text("\n".join(svg))


def add_box(elements: list[dict], eid: str, x: int, y: int, w: int, h: int, text: str, fill: str, size: int = 14) -> None:
    elements.append(element(eid, "rectangle", x, y, w, h, fill=fill))
    elements.append(element(eid + "t", "text", x + 10, y + 8, w - 20, h - 16, text=text, size=size))


def main() -> int:
    data = json.loads(DATA.read_text())
    width, height = 4520, 3300
    elements: list[dict] = [
        element("title", "text", 30, 20, 1700, 40, text="Systems Thinking Studio — full setup, cadence, ownership, and durable gap closure", size=28),
        element("subtitle", "text", 30, 62, 2400, 30, text=f"North star: {data['north_star']}  |  authority: {data['authority_state']}", size=15),
    ]
    # System loop.
    elements.append(element("loop-header", "text", 30, 115, 1000, 26, text="1. Closed system loop", size=20))
    for index, step in enumerate(data["system_loop"]):
        col, row = index % 3, index // 3
        x, y = 30 + col * 430, 155 + row * 118
        add_box(elements, f"loop-{index}", x, y, 390, 88, f"{index + 1:02d}  {step}", PHASE_FILL, 15)
        if index:
            prev_col, prev_row = (index - 1) % 3, (index - 1) // 3
            px, py = 30 + prev_col * 430 + 390, 155 + prev_row * 118 + 44
            if row == prev_row:
                elements.append(element(f"loop-arrow-{index}", "arrow", px, py, 10, 10, dx=x - px, dy=0))
            else:
                elements.append(element(f"loop-arrow-{index}", "arrow", px - 195, py + 44, 10, 10, dx=0, dy=y - (py + 44)))
    # Ownership column.
    elements.append(element("owners-header", "text", 1340, 115, 1000, 26, text="2. Agent and human ownership", size=20))
    for index, agent in enumerate(data["agents"]):
        x, y = 1340 + (index % 2) * 620, 155 + (index // 2) * 116
        text = f"{agent['id']} — {agent['role']}\nDO: {agent['does']}\nNOT: {agent['does_not']}"
        add_box(elements, f"agent-{index}", x, y, 590, 102, text, "#f1f3f5", 12)
    # Daily and weekly cadence.
    elements.append(element("daily-header", "text", 2610, 115, 900, 26, text="3. Daily outcomes", size=20))
    for index, item in enumerate(data["daily_outcomes"]):
        y = 155 + index * 92
        text = f"{item['time']} · {item['owner']}\n{item['outcome']}\nGate: {item['gate']}"
        add_box(elements, f"daily-{index}", 2610, y, 860, 78, text, "#e5dbff", 12)
    elements.append(element("weekly-header", "text", 3550, 115, 800, 26, text="4. Weekly operating rhythm", size=20))
    for index, item in enumerate(data["weekly_schedule"]):
        y = 155 + index * 92
        text = f"{item['day']} · {item['theme']}\n{item['outcome']}\nOwner: {item['owner']}"
        add_box(elements, f"weekly-{index}", 3550, y, 900, 78, text, "#fff4e6", 12)
    # Gap register: 3 columns × 10 rows.
    elements.append(element("gaps-header", "text", 30, 1110, 2500, 30, text="5. Thirty durable setups — status, owner, and proof gate", size=22))
    elements.append(element("legend", "text", 2900, 1120, 1500, 24, text="Legend: green=FIXED · amber=PARTIAL · red=MISSING · purple=NOT_READY", size=14))
    for index, gap in enumerate(data["gaps"]):
        col, row = index // 10, index % 10
        x, y = 30 + col * 1480, 1160 + row * 195
        text = f"{gap['id']} {gap['status']} · {gap['category']}\nGap: {gap['gap']}\nOwner: {gap['owner']}\nDurable: {gap['durable_setup']}\nProof: {gap['verification']}"
        add_box(elements, f"gap-{gap['id']}", x, y, 1420, 175, text, STATUS[gap['status']], 12)
    write_map(elements, width, height)
    print(f"wrote {ROOT / 'systems-thinking-operating-system.excalidraw'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
