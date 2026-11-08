---
name: "st-diagnose-fixes-that-fail"
description: "Step 17 of /systemsthinking (Diagnose): Test for Fixes that Fail: the quick fix's side effect that returns the problem worse."
---

# st-diagnose-fixes-that-fail: step 17 of /systemsthinking (Diagnose)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Test for Fixes that Fail: the quick fix's side effect that returns the problem worse.
**Tool:** `python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py archetype fixes-that-fail`
**Artifact:** `diagnosis.md`
**Jev / gate:** none

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `diagnosis.md` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-diagnose-shifting-burden`. Router: `/systemsthinking`.
