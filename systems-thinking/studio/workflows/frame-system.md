# Workflow — Frame a System

Use when designing, changing, or handing off a system: an architecture, an
agent fleet, a GTM engine, a product loop, an org process.

1. Print the scaffold: `studio frame "<system name>"` (or copy `templates/system-frame.md`).
2. Boundary first. Write what is inside/outside and WHY the line is there.
   The boundary decision is itself a leverage point — flag it.
3. Stocks before flows. If you cannot name the accumulation, you have not
   found the system yet (work-in-progress, trust, pipeline, context debt,
   skill, cash, attention are all stocks).
4. Loops: at least one reinforcing (R) and one balancing (B). If only R
   loops exist, ask what limits them — that constraint is a hidden B loop.
5. Delays: for each loop, estimate the delay between action and observable
   effect. Oscillation/oversoot diagnoses live here.
6. Run `studio map "<symptoms in plain words>"`; record the top archetype
   suspect and the evidence for/against in section 7 of the frame.
7. Leverage: run `studio leverage`; mark where existing interventions sit
   (rank), and write the one-rank-higher option in section 8.
8. Measurement: define the stock health metric, a LEAD indicator that moves
   before the delay elapses, and a falsifier with a deadline.
9. Corpus: `studio cards systems-thinking --grep <topic>` and/or
   `studio search "<topic>" exhaustive`. Cite what applies.

Done when the success criteria in SKILL.md hold. The completed frame goes in
the repo/docs next to the system it describes.
