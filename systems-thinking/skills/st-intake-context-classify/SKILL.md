---
name: "st-intake-context-classify"
description: "Step 5 of /systemsthinking (Intake): Classify the decision context: clear, complicated, complex, chaotic, disorder. Disorder is RED."
---

# st-intake-context-classify: step 5 of /systemsthinking (Intake)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Classify the decision context: clear, complicated, complex, chaotic, disorder. Disorder is RED.
**Tool:** `python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py context <ctx>`
**Artifact:** `brief.md#context`
**Jev / gate:** JEV choice: context class (rig-s1gate), DEFERRED if down

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `brief.md#context` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-intake-done-test`. Router: `/systemsthinking`.
