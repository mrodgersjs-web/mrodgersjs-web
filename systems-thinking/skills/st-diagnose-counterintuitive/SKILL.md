---
name: "st-diagnose-counterintuitive"
description: "Step 21 of /systemsthinking (Diagnose): Write the counterintuitive finding: what the obvious push would make worse."
---

# st-diagnose-counterintuitive: step 21 of /systemsthinking (Diagnose)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Write the counterintuitive finding: what the obvious push would make worse.
**Tool:** `judgment`
**Artifact:** `diagnosis.md#counterintuitive`
**Jev / gate:** none

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `diagnosis.md#counterintuitive` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-diagnose-doom-loop`. Router: `/systemsthinking`.
