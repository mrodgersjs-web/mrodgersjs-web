#!/usr/bin/env python3
import importlib.util
from pathlib import Path

MODULE = Path(__file__).with_name("distill.py")
spec = importlib.util.spec_from_file_location("distill", MODULE)
distill = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(distill)

sources = [
    {"sha256": "a", "source_class": "paper"},
    {"sha256": "b", "source_class": "youtube"},
    {"sha256": "c", "source_class": "paper"},
]
card = {
    "citation_sha256": ["a", "b", "c"],
    "feedback_loops": [{"name": "loop"}],
    "leverage_points": [{"rank": 1}],
    "rig_process_changes": [{"process": "Jake OBSERVE-MODEL loop"}],
    "falsification_tests": ["break the loop"],
}

ok = distill.gate_card(card, sources, ["Jake OBSERVE-MODEL loop"])
assert ok["ok"]
assert not distill.gate_card(card, sources[:1] * 3, ["Jake OBSERVE-MODEL loop"])["ok"]
wrong = dict(card, rig_process_changes=[{"process": "Climate modeling"}])
assert not distill.gate_card(wrong, sources, ["Jake OBSERVE-MODEL loop"])["ok"]
print("strict L2 card gate tests: PASS")
