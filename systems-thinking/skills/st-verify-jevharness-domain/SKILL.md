---
name: "st-verify-jevharness-domain"
description: "Step 51 of /systemsthinking (Verify): Wrap the 8 phases as a /jevharness switch domain (typed questions per phase) and replay it."
---

# st-verify-jevharness-domain: step 51 of /systemsthinking (Verify)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Wrap the 8 phases as a /jevharness switch domain (typed questions per phase) and replay it.
**Tool:** `/jevharness-new-domain, /jevharness-rig-gate`
**Artifact:** `harness trace`
**Jev / gate:** JEV: harness run + replay match

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `harness trace` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-verify-cold-review`. Router: `/systemsthinking`.
