#!/usr/bin/env python3
"""Admit one public HN evidence item for each missing source-class topic."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path.home() / ".rig/omniscout-campaigns/systems-thinking-5gb-20260829"
TARGETS = {
    "multi-agent-coordination": ("49316271", "Patterns and problems in emerging multi-agent systems"),
    "workflow-scheduler-authority": ("23350023", "Temporal – Workflow as Code"),
    "knowledge-organizational-learning": ("22454333", "Ask HN: Good ways to capture institutional knowledge?"),
    "complex-adaptive-systems": ("49409473", "How Complex Systems Fail (1998)"),
    "incident-learning-postmortems": ("20120059", "Google Cloud Networking Incident Postmortem"),
    "decision-calibration": ("22915837", "Forecasting s-curves is hard"),
}


def main() -> int:
    spec = importlib.util.spec_from_file_location("campaign", ROOT / "campaign.py")
    campaign = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(campaign)
    conn = campaign.db(ROOT)
    added = []
    for topic, (item_id, title) in TARGETS.items():
        ok = campaign.add_item(
            conn,
            key=f"hn-targeted:{item_id}",
            topic=topic,
            source_class="hn",
            url=f"https://hn.algolia.com/api/v1/items/{item_id}",
            title=title,
            metadata={"targeted_gap_repair": True, "hn_item_id": item_id},
        )
        if ok:
            added.append(topic)
    conn.commit()
    print({"added": added, "count": len(added), "targets": sorted(TARGETS)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
