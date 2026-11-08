#!/usr/bin/env python3
"""Assemble PASS L2 cards into a citation-bound Jake v3 mechanism appendix."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def one_line(value: object) -> str:
    return " ".join(str(value or "").split())


def assemble(root: Path, min_cards: int) -> dict:
    summary_path = root / "l2" / "SYNTHESIS.json"
    summary = json.loads(summary_path.read_text())
    source_pass = int(summary.get("pass") or 0)
    source_quarantined = int(summary.get("quarantined") or 0)
    source_not_ready = int(summary.get("not_ready") or 0)
    if source_pass < min_cards or source_quarantined != 0 or source_not_ready != 0:
        raise RuntimeError(
            "L2 synthesis is not promotable: "
            f"pass={source_pass}, quarantined={source_quarantined}, "
            f"not_ready={source_not_ready}"
        )
    cards: list[dict] = []
    for path in sorted((root / "l2").glob("*.json")):
        value = json.loads(path.read_text())
        if value.get("schema") != "rig.omniscout.systems-mechanism-card.v1":
            continue
        if value.get("gate", {}).get("ok"):
            cards.append(value)
    if len(cards) < min_cards:
        raise RuntimeError(f"need {min_cards} PASS cards, found {len(cards)}")
    lines = [
        "## Sourced mechanism library (OmniScout 36GB, v3)",
        "",
        "> Generated from citation-gated L2 cards. Authority remains STAGED_NOT_PROMOTED;",
        "> use mechanisms as tested hypotheses until their falsification gates pass in RIG.",
        "",
    ]
    index: list[dict] = []
    for card in cards:
        syn = card["synthesis"]
        card_hash = card["card_sha256"]
        lines.extend([
            f"### {one_line(syn.get('mechanism_name'))}",
            "",
            f"- **Topic:** `{card['topic']}`",
            f"- **Boundary:** {one_line(syn.get('system_boundary'))}",
        ])
        for loop in (syn.get("feedback_loops") or [])[:2]:
            lines.append(
                f"- **{one_line(loop.get('polarity'))} loop — {one_line(loop.get('name'))}:** "
                f"{one_line(loop.get('mechanism'))} Delay: {one_line(loop.get('delay'))}"
            )
        for leverage in (syn.get("leverage_points") or [])[:2]:
            lines.append(
                f"- **Leverage #{leverage.get('rank')}:** {one_line(leverage.get('intervention'))} — "
                f"{one_line(leverage.get('why'))}"
            )
        for failure in (syn.get("failure_modes") or [])[:2]:
            lines.append(
                f"- **Failure signal:** {one_line(failure.get('mode'))} → "
                f"{one_line(failure.get('early_signal'))}; gate: {one_line(failure.get('gate'))}"
            )
        for change in (syn.get("rig_process_changes") or [])[:2]:
            lines.append(
                f"- **RIG change — {one_line(change.get('process'))}:** {one_line(change.get('change'))}; "
                f"done test: `{one_line(change.get('done_test'))}`"
            )
        tests = syn.get("falsification_tests") or []
        if tests:
            lines.append(f"- **Refute it:** {one_line(tests[0])}")
        lines.append(f"- **Card proof:** `{card_hash}`")
        lines.append("- **Sources:**")
        for source in card["sources"][:8]:
            lines.append(
                f"  - [{one_line(source.get('title'))}]({source['source_url']}) — "
                f"`{source['sha256']}` ({source['source_class']})"
            )
        lines.append("")
        index.append({"topic": card["topic"], "card_sha256": card_hash,
                      "citation_count": len(card["sources"])})
    text = "\n".join(lines).rstrip() + "\n"
    appendix = root / "l2" / "JAKE_SYSTEMS_MECHANISMS_V3.md"
    appendix.write_text(text)
    result = {
        "schema": "rig.jake.systems-mechanism-appendix.v1",
        "ok": True,
        "cards": len(cards),
        "appendix": str(appendix),
        "sha256": stable_hash(text),
        "source_l2_pass_cards": source_pass,
        "source_l2_quarantined_cards": source_quarantined,
        "source_l2_not_ready_cards": source_not_ready,
        "source_l2_summary_sha256": summary.get("summary_sha256"),
        "authority_state": "STAGED_NOT_PROMOTED",
        "index": index,
    }
    (root / "l2" / "JAKE_SYSTEMS_MECHANISMS_V3.proof.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.home() / ".rig/omniscout-campaigns/systems-thinking-5gb-20260829")
    parser.add_argument("--min-cards", type=int, default=12)
    args = parser.parse_args()
    assemble(args.root, args.min_cards)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
