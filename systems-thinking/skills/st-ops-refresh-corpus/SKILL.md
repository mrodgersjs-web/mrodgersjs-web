---
name: "st-ops-refresh-corpus"
description: "Step 64 of /systemsthinking (Operate): Refresh the Recall card index and pack, then studio doctor."
---

# st-ops-refresh-corpus: step 64 of /systemsthinking (Operate)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Refresh the Recall card index and pack, then studio doctor.
**Tool:** `scripts/recall_fetch_all.py + recall_merge_tags.py`
**Artifact:** `data/card-index.json`
**Jev / gate:** CODE: doctor green

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `data/card-index.json` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-ops-publish`. Router: `/systemsthinking`.
