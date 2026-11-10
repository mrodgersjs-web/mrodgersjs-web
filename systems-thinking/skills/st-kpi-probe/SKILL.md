---
name: "st-kpi-probe"
description: "Step 57 of /systemsthinking (KPIs): Run the KPI probe; a missing source prints no_source, never zero."
---

# st-kpi-probe: step 57 of /systemsthinking (KPIs)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Run the KPI probe; a missing source prints no_source, never zero.
**Tool:** `ak-kpi / probe`
**Artifact:** `kpi.log`
**Jev / gate:** CODE: no_source != 0

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `kpi.log` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-kpi-scorecard`. Router: `/systemsthinking`.
