---
name: "st-goal-check"
description: "Step 60 of /systemsthinking (Goals): Run goal check; the exit code is the verdict, never the doer."
---

# st-goal-check: step 60 of /systemsthinking (Goals)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Run goal check; the exit code is the verdict, never the doer.
**Tool:** `goal check <slug>`
**Artifact:** `RESULT.json`
**Jev / gate:** CODE: exit code

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `RESULT.json` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-goal-close`. Router: `/systemsthinking`.
