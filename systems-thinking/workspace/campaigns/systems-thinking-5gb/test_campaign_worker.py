#!/usr/bin/env python3
import fcntl
import importlib.util
import tempfile
import threading
import time
from pathlib import Path

MODULE = Path(__file__).with_name("campaign.py")
spec = importlib.util.spec_from_file_location("campaign", MODULE)
campaign = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(campaign)


def lattice() -> dict:
    return {
        "campaign_id": "test",
        "policy": {
            "source_class_floors_bytes": {"paper": 1, "hn": 0, "youtube": 0},
            "paper_download_concurrency": 3,
            "youtube_concurrency": 1,
            "max_single_artifact_bytes": 100,
            "free_disk_floor_bytes": 1,
        },
    }


def test_parallel_paper_batch() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        conn = campaign.db(root)
        topics = [
            "feedback-stock-flow",
            "cybernetics-control-observability",
            "systems-archetypes-leverage",
        ]
        for index, topic in enumerate(topics):
            assert campaign.add_item(
                conn,
                key=f"paper:{index}",
                topic=topic,
                source_class="paper",
                url=f"https://example.com/{index}.pdf",
                title={
                    "feedback-stock-flow": "Feedback dynamics in operational systems",
                    "cybernetics-control-observability": "Control and observability in systems",
                    "systems-archetypes-leverage": "Systems archetypes and leverage",
                }[topic],
                metadata={},
            )
        conn.commit()
        active = 0
        peak = 0
        lock = threading.Lock()

        def fake_capture(root_: Path, row, _max_bytes: int):
            nonlocal active, peak
            with lock:
                active += 1
                peak = max(peak, active)
            time.sleep(0.05)
            path = root_ / f"{row['id']}.pdf"
            path.write_bytes(b"x" * 100)
            with lock:
                active -= 1
            return path, 100, f"digest-{row['id']}"

        original = campaign.capture_paper
        campaign.capture_paper = fake_capture
        try:
            status = campaign.run_campaign(root, conn, lattice(), target=400, max_items=3)
        finally:
            campaign.capture_paper = original
        assert status["artifact_bytes"] == 300
        assert status["states"]["done"] == 3
        assert peak == 3



def test_topic_anchor_gate_goes_red_without_process_anchor() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        conn = campaign.db(root)
        assert campaign.add_item(
            conn,
            key="anchor-paper",
            topic="feedback-stock-flow",
            source_class="paper",
            url="https://example.com/feedback.pdf",
            title="Feedback dynamics in operational systems",
            metadata={},
        )
        artifact = root / "anchor.pdf"
        artifact.write_bytes(b"x")
        conn.execute(
            """UPDATE items SET state='done',bytes=1,sha256='a',
               artifact_path=? WHERE unique_key='anchor-paper'""",
            (str(artifact),),
        )
        conn.commit()
        strict = lattice()
        strict["policy"]["min_source_classes"] = 1
        strict["policy"]["min_topics_with_artifacts"] = 1
        strict["topic_domain_anchor_floors"] = {
            "feedback-stock-flow": ["feedback"]
        }
        ok, _receipt = campaign.gate(root, conn, strict, target=1)
        assert ok
        conn.execute(
            "UPDATE items SET title='Generic dynamics paper' WHERE unique_key='anchor-paper'"
        )
        conn.commit()
        ok, receipt = campaign.gate(root, conn, strict, target=1)
        assert not ok
        assert not receipt["checks"]["topic_domain_anchors"]["feedback-stock-flow"]

def test_domain_rejection_and_writer_lock() -> None:
    assert not campaign.title_relevant(
        "Viewing Forests As Complex Adaptive Systems", "complex-adaptive-systems"
    )
    assert campaign.title_relevant(
        "Complex Adaptive Systems for Operations", "complex-adaptive-systems"
    )
    assert campaign.is_terminal_capture_error(RuntimeError("HTTP 403: blocked"))
    assert not campaign.is_terminal_capture_error(RuntimeError("HTTP 429: rate limited"))
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        conn = campaign.db(root)
        handle = (root / "writer.lock").open("w")
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            try:
                campaign.run_campaign(root, conn, lattice(), target=1, max_items=0)
            except RuntimeError as exc:
                assert "another campaign writer" in str(exc)
            else:
                raise AssertionError("second writer was admitted")
        finally:
            handle.close()


if __name__ == "__main__":
    test_parallel_paper_batch()
    test_domain_rejection_and_writer_lock()
    print("campaign worker tests: PASS")
