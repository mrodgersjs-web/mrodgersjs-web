---
name: "st-intake-done-test"
description: "Step 6 of /systemsthinking (Intake): Write the falsifiable success test that fails today and will pass when fixed."
---

# st-intake-done-test: step 6 of /systemsthinking (Intake)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Write the falsifiable success test that fails today and will pass when fixed.
**Tool:** `goal new --done-test`
**Artifact:** `done-test.sh`
**Jev / gate:** CODE: script exits non-zero today

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `done-test.sh` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-frame-boundary`. Router: `/systemsthinking`.
