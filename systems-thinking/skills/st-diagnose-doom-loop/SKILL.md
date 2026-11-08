---
name: "st-diagnose-doom-loop"
description: "Step 22 of /systemsthinking (Diagnose): Name any doom loop (self-reinforcing failure) in the agent fleet or lane and its breaker."
---

# st-diagnose-doom-loop: step 22 of /systemsthinking (Diagnose)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Name any doom loop (self-reinforcing failure) in the agent fleet or lane and its breaker.
**Tool:** `studio operating gaps`
**Artifact:** `diagnosis.md#doom-loop`
**Jev / gate:** none

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `diagnosis.md#doom-loop` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-leverage-rank`. Router: `/systemsthinking`.
