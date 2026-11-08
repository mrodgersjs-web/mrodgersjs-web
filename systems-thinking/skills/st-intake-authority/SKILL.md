---
name: "st-intake-authority"
description: "Step 4 of /systemsthinking (Intake): Record what the requester may change (authority ceiling). It caps the leverage rank later."
---

# st-intake-authority: step 4 of /systemsthinking (Intake)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Record what the requester may change (authority ceiling). It caps the leverage rank later.
**Tool:** `ask or read org doc`
**Artifact:** `brief.md#authority`
**Jev / gate:** none

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `brief.md#authority` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-intake-context-classify`. Router: `/systemsthinking`.
