---
name: "st-goal-register"
description: "Step 59 of /systemsthinking (Goals): Register the goal: mission + KPI + done-test, bound to the loop."
---

# st-goal-register: step 59 of /systemsthinking (Goals)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Register the goal: mission + KPI + done-test, bound to the loop.
**Tool:** `goal new ... --done-test`
**Artifact:** `goals/<slug>`
**Jev / gate:** CODE: goal check exits 1 today

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `goals/<slug>` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-goal-check`. Router: `/systemsthinking`.
