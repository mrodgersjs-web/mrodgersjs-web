---
name: "st-verify-red-control"
description: "Step 47 of /systemsthinking (Verify): Run the planted RED (context disorder) and confirm it fails. A gate never failed is not trusted."
---

# st-verify-red-control: step 47 of /systemsthinking (Verify)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Run the planted RED (context disorder) and confirm it fails. A gate never failed is not trusted.
**Tool:** `python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py run "x" --context disorder`
**Artifact:** `verify.log`
**Jev / gate:** CODE: must exit non-zero

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `verify.log` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-verify-seal`. Router: `/systemsthinking`.
