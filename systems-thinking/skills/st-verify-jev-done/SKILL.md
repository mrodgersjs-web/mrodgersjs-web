---
name: "st-verify-jev-done"
description: "Step 49 of /systemsthinking (Verify): Gate the done claim with hosted Jev before calling it done."
---

# st-verify-jev-done: step 49 of /systemsthinking (Verify)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Gate the done claim with hosted Jev before calling it done.
**Tool:** `rig-s1gate check done.claim`
**Artifact:** `decision id`
**Jev / gate:** JEV: done.claim; DEFERRED if down, never PASS

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `decision id` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-verify-jev-everywhere`. Router: `/systemsthinking`.
