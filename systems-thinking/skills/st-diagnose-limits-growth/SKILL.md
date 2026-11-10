---
name: "st-diagnose-limits-growth"
description: "Step 19 of /systemsthinking (Diagnose): Test for Limits to Growth: find the limiting condition before pushing harder."
---

# st-diagnose-limits-growth: step 19 of /systemsthinking (Diagnose)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Test for Limits to Growth: find the limiting condition before pushing harder.
**Tool:** `python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py archetype limits-to-growth`
**Artifact:** `diagnosis.md`
**Jev / gate:** none

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `diagnosis.md` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-diagnose-evidence`. Router: `/systemsthinking`.
