---
name: "st-kpi-define"
description: "Step 56 of /systemsthinking (KPIs): Define the KPI: before, target, window, unit, probe command, source."
---

# st-kpi-define: step 56 of /systemsthinking (KPIs)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Define the KPI: before, target, window, unit, probe command, source.
**Tool:** `goal new --kpi-*`
**Artifact:** `kpi.json`
**Jev / gate:** CODE: probe runs and prints a number

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `kpi.json` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `st-kpi-probe`. Router: `/systemsthinking`.
