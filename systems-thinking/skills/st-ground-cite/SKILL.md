---
name: "st-ground-cite"
description: "Step 32 of /systemsthinking (Ground): Cite as [Card: title](url). Never invent a citation."
---

# st-ground-cite: step 32 of /systemsthinking (Ground)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Cite as [Card: title](url). Never invent a citation.
**Tool:** `card-index.json`
**Artifact:** `grounding.md#citations`
**Jev / gate:** CODE: every cite resolves to a card id

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `grounding.md#citations` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-ground-gaps`. Router: `/systemsthinking`.
