---
name: "st-verify-cold-review"
description: "Step 52 of /systemsthinking (Verify): Zero-context (goldfish) review of DELIVERABLE.md; fix what it cannot follow."
---

# st-verify-cold-review: step 52 of /systemsthinking (Verify)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Zero-context (goldfish) review of DELIVERABLE.md; fix what it cannot follow.
**Tool:** `subagent, no context`
**Artifact:** `review.md`
**Jev / gate:** none

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `review.md` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-loop-define`. Router: `/systemsthinking`.
