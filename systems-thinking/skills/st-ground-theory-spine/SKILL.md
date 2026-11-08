---
name: "st-ground-theory-spine"
description: "Step 34 of /systemsthinking (Ground): Verify theory provenance against the theory spine."
---

# st-ground-theory-spine: step 34 of /systemsthinking (Ground)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Verify theory provenance against the theory spine.
**Tool:** `scripts/verify_theory_spine.py`
**Artifact:** `verify.log`
**Jev / gate:** CODE: exit 0

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `verify.log` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-polymath-crosspoll`. Router: `/systemsthinking`.
