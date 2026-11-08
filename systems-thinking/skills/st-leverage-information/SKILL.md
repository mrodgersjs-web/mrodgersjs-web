---
name: "st-leverage-information"
description: "Step 27 of /systemsthinking (Leverage): Check rank-6 information flows: who would act differently if they saw the stock?"
---

# st-leverage-information: step 27 of /systemsthinking (Leverage)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Check rank-6 information flows: who would act differently if they saw the stock?
**Tool:** `python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py simulate <domain>`
**Artifact:** `leverage.md#info`
**Jev / gate:** none

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `leverage.md#info` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-leverage-rules-goals`. Router: `/systemsthinking`.
