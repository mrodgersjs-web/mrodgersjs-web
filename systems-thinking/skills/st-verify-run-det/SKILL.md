---
name: "st-verify-run-det"
description: "Step 46 of /systemsthinking (Verify): Run the deterministic 8-phase path; GREEN only if classified, map hits, rank != 12, knowledge >= 2, polymath >= 0.60."
---

# st-verify-run-det: step 46 of /systemsthinking (Verify)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Run the deterministic 8-phase path; GREEN only if classified, map hits, rank != 12, knowledge >= 2, polymath >= 0.60.
**Tool:** `python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py run "<problem>" --domain d --context c`
**Artifact:** `run.json`
**Jev / gate:** CODE: exit 0

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `run.json` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-verify-red-control`. Router: `/systemsthinking`.
