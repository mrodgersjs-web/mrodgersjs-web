---
name: "st-synth-causal-map"
description: "Step 42 of /systemsthinking (Synthesize): Draw the causal loop diagram (Excalidraw/SVG) with the leverage point marked."
---

# st-synth-causal-map: step 42 of /systemsthinking (Synthesize)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Draw the causal loop diagram (Excalidraw/SVG) with the leverage point marked.
**Tool:** `scripts/gen_diagrams.py`
**Artifact:** `causal-map.svg`
**Jev / gate:** JEV image check (dual judge)

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `causal-map.svg` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-synth-plan`. Router: `/systemsthinking`.
