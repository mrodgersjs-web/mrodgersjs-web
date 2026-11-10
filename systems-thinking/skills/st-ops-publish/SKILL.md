---
name: "st-ops-publish"
description: "Step 65 of /systemsthinking (Operate): Commit + push the studio and outputs to mrodgersjs-web/mrodgersjs-web systems-thinking/. Secrets scan first."
---

# st-ops-publish: step 65 of /systemsthinking (Operate)

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** Commit + push the studio and outputs to mrodgersjs-web/mrodgersjs-web systems-thinking/. Secrets scan first.
**Tool:** `git`
**Artifact:** `commit`
**Jev / gate:** CODE: secret scan clean

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `commit` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `systemsthinking (done)`. Router: `/systemsthinking`.
