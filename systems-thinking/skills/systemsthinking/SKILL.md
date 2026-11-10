---
name: systemsthinking
description: "Systems thinking front door: map a problem as stocks, flows, loops, archetypes and Meadows leverage, ground it, import a polymath mechanism, ship a falsifiable plan, then run it as a /loop with KPIs and a /goal, Jev-gated (jev-everywhere + jevharness). Routes 65 step skills across 12 stages."
---

# /systemsthinking: 65 step skills, 12 stages

**Triggers:** /systemsthinking, /systems-thinking, "why does this keep happening", plateau, quick fix keeps failing,
causal map, leverage point, archetype, doom loop, stock and flow, GTM/sales/founder architecture.
**Engine:** Systems Thinking Studio (`studio` CLI, `python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py`), 8-phase contract in
`processes/phases.md`. **Source of truth in git:** `github.com/mrodgersjs-web/mrodgersjs-web` → `systems-thinking/`.
**Owner:** iris-strategy. **Jev:** `/jev-everywhere` (ladder CODE → JEV → SYSTEM 2 → HUMAN) and `/jevharness`
(the 8 phases as a switch domain with typed questions, replayable).

## Commands
| Command | Does | Steps |
|---|---|---|
| `/systemsthinking <problem>` | full run, intake to verify | 1-52 |
| `/systemsthinking quick <symptom>` | map + leverage only | 15, 23, 24 |
| `/systemsthinking loop <plan>` | turn a plan into loop + KPI + goal | 53-61 |
| `/systemsthinking daily` | the systems-thinking employee's daily deliverable | 62 |

## Rules
- One step owns one artifact. Deterministic steps run a program. Never invent a citation. Never skip Verify.
- Disorder context is RED until decomposed. More agents/schedules are rejected until the constraint is evidenced.
- A KPI with no source prints `no_source`, never 0. Only `goal check`'s exit code completes a goal.
- Jev before done; DEFERRED if down. Jacob/Alex, James and job-application floors are never lifted.

## Ladder
| # | Stage | Skill | Does | Jev / gate |
|---|---|---|---|---|
| 1 | Intake | `st-intake-brief` | Write the brief: problem, requester, stakes, constraints, deadline, what success looks like. | CODE: headings ## Problem and ## Success looks like exist |
| 2 | Intake | `st-intake-symptom` | Capture the symptom in the requester's own words, with when it started and how often it returns. | none |
| 3 | Intake | `st-intake-stakes` | Name who loses what if nothing changes, in one number with its source. | none |
| 4 | Intake | `st-intake-authority` | Record what the requester may change (authority ceiling). It caps the leverage rank later. | none |
| 5 | Intake | `st-intake-context-classify` | Classify the decision context: clear, complicated, complex, chaotic, disorder. Disorder is RED. | JEV choice: context class (rig-s1gate), DEFERRED if down |
| 6 | Intake | `st-intake-done-test` | Write the falsifiable success test that fails today and will pass when fixed. | CODE: script exits non-zero today |
| 7 | Frame | `st-frame-boundary` | Draw the system boundary: what is inside, outside, and ignored on purpose. | none |
| 8 | Frame | `st-frame-domain` | Start from a domain frame (gtm, linkedin, sales, founder, mike-os), never a blank page. | none |
| 9 | Frame | `st-frame-stocks` | List the stocks (things that accumulate) with unit and current level. | CODE: every stock has a unit |
| 10 | Frame | `st-frame-flows` | List inflows and outflows for each stock with rate and source. | none |
| 11 | Frame | `st-frame-actors` | Name the actors, their goals and the information each one sees. | none |
| 12 | Frame | `st-frame-loops` | Find at least one reinforcing (R) and one balancing (B) loop. Label polarity on every link. | CODE: >=1 R and >=1 B |
| 13 | Frame | `st-frame-delays` | Mark every delay and its length; delays are where oscillation and overshoot come from. | none |
| 14 | Frame | `st-frame-controller` | Name the controller, observed state, sampling delay, allowed action and UNKNOWN route. | CODE: missing observation = BLOCKED |
| 15 | Diagnose | `st-diagnose-map` | Run the symptom against the archetype table and get ranked suspects. | none |
| 16 | Diagnose | `st-diagnose-archetype` | Read the suspect archetype (Kim 2000) and its classic intervention. | none |
| 17 | Diagnose | `st-diagnose-fixes-that-fail` | Test for Fixes that Fail: the quick fix's side effect that returns the problem worse. | none |
| 18 | Diagnose | `st-diagnose-shifting-burden` | Test for Shifting the Burden: symptomatic fix eroding the fundamental capability. | none |
| 19 | Diagnose | `st-diagnose-limits-growth` | Test for Limits to Growth: find the limiting condition before pushing harder. | none |
| 20 | Diagnose | `st-diagnose-evidence` | Prove the suspect's predicted stock is actually moving, with a dated read. | JEV bool: evidence supports suspect |
| 21 | Diagnose | `st-diagnose-counterintuitive` | Write the counterintuitive finding: what the obvious push would make worse. | none |
| 22 | Diagnose | `st-diagnose-doom-loop` | Name any doom loop (self-reinforcing failure) in the agent fleet or lane and its breaker. | none |
| 23 | Leverage | `st-leverage-rank` | Place current interventions on Meadows' 12 points (12 weakest, 1 strongest). | none |
| 24 | Leverage | `st-leverage-choose` | Choose the highest rank the requester's authority allows. | JEV choice: rank pick |
| 25 | Leverage | `st-leverage-reject` | Record the one-rank-higher option and why it was rejected. | none |
| 26 | Leverage | `st-leverage-wip-cap` | Set WIP cap, queue-age signal, drain condition and bottleneck owner before adding capacity. | CODE: more agents rejected until constraint evidenced |
| 27 | Leverage | `st-leverage-information` | Check rank-6 information flows: who would act differently if they saw the stock? | none |
| 28 | Leverage | `st-leverage-rules-goals` | Check rules (5), self-organization (4) and goals (3) before parameters (12). | none |
| 29 | Ground | `st-ground-cards` | Pull tagged Recall cards for the domain. | none |
| 30 | Ground | `st-ground-search` | Search the live Recall KB for the mechanism. | none |
| 31 | Ground | `st-ground-library` | Read the papers/books/youtube library under studio/knowledge. | none |
| 32 | Ground | `st-ground-cite` | Cite as [Card: title](url). Never invent a citation. | CODE: every cite resolves to a card id |
| 33 | Ground | `st-ground-gaps` | Write ## Gaps: absent evidence is a finding, not a blank. | none |
| 34 | Ground | `st-ground-theory-spine` | Verify theory provenance against the theory spine. | CODE: exit 0 |
| 35 | Polymath | `st-polymath-crosspoll` | Import a mechanism from another domain with the same structure. | none |
| 36 | Polymath | `st-polymath-mechanisms` | Pull source-gated transfers from curated mechanisms. | none |
| 37 | Polymath | `st-polymath-score` | Score transfer fit; GREEN needs >= 0.60. | JEV score: transfer fit |
| 38 | Polymath | `st-polymath-deviate` | Run /deviate engines on the chosen leverage point for far-from-obvious options. | none |
| 39 | Polymath | `st-polymath-falsify` | Write the falsifier: the observation that would kill the imported mechanism. | none |
| 40 | Synthesize | `st-synth-simulate` | Run the Euler stock-flow model: baseline vs +volume vs information intervention. | none |
| 41 | Synthesize | `st-synth-deliverable` | Assemble DELIVERABLE.md from every prior artifact; shrink nothing silently. | none |
| 42 | Synthesize | `st-synth-causal-map` | Draw the causal loop diagram (Excalidraw/SVG) with the leverage point marked. | JEV image check (dual judge) |
| 43 | Synthesize | `st-synth-plan` | Write the falsifiable plan: one intervention, owner, date, KPI, kill criterion. | none |
| 44 | Synthesize | `st-synth-second-order` | List second-order effects and who they hit, 1 week / 1 quarter / 1 year. | none |
| 45 | Synthesize | `st-synth-reversibility` | Assess reversibility; irreversible steps go to Gate-D. | HUMAN: Gate-D for irreversible |
| 46 | Verify | `st-verify-run-det` | Run the deterministic 8-phase path; GREEN only if classified, map hits, rank != 12, knowledge >= 2, polymath >= 0.60. | CODE: exit 0 |
| 47 | Verify | `st-verify-red-control` | Run the planted RED (context disorder) and confirm it fails. A gate never failed is not trusted. | CODE: must exit non-zero |
| 48 | Verify | `st-verify-seal` | Seal the ProofPacket. | CODE: seal verifies |
| 49 | Verify | `st-verify-jev-done` | Gate the done claim with hosted Jev before calling it done. | JEV: done.claim; DEFERRED if down, never PASS |
| 50 | Verify | `st-verify-jev-everywhere` | Walk the jev-everywhere ladder for every judgment in the run: CODE, JEV, SYSTEM 2, HUMAN. | JEV: one decision id per typed judgment |
| 51 | Verify | `st-verify-jevharness-domain` | Wrap the 8 phases as a /jevharness switch domain (typed questions per phase) and replay it. | JEV: harness run + replay match |
| 52 | Verify | `st-verify-cold-review` | Zero-context (goldfish) review of DELIVERABLE.md; fix what it cannot follow. | none |
| 53 | Loops | `st-loop-define` | Turn the plan into a rig-loop: trigger, step, check, stop condition. | none |
| 54 | Loops | `st-loop-cadence` | Place it on the operating cadence; heavy work runs 21:00-06:00 MT, staggered. | none |
| 55 | Loops | `st-loop-no-progress` | Detect spin: same check tail twice = change strategy, not retry. | CODE: progress guard |
| 56 | KPIs | `st-kpi-define` | Define the KPI: before, target, window, unit, probe command, source. | CODE: probe runs and prints a number |
| 57 | KPIs | `st-kpi-probe` | Run the KPI probe; a missing source prints no_source, never zero. | CODE: no_source != 0 |
| 58 | KPIs | `st-kpi-scorecard` | Post the KPI to the systems-thinking scorecard on the Work Canvas. | none |
| 59 | Goals | `st-goal-register` | Register the goal: mission + KPI + done-test, bound to the loop. | CODE: goal check exits 1 today |
| 60 | Goals | `st-goal-check` | Run goal check; the exit code is the verdict, never the doer. | CODE: exit code |
| 61 | Goals | `st-goal-close` | Close with proof: decision id, ProofPacket, canvas updated, three-line report. | JEV: done.claim |
| 62 | Operate | `st-ops-daily` | Daily: one causal map or leverage spec for a live RIG bottleneck (systems-thinking employee KPI). | none |
| 63 | Operate | `st-ops-weekly-retro` | Weekly: what loops moved, which KPIs moved, which held. Retire zero-output steps. | none |
| 64 | Operate | `st-ops-refresh-corpus` | Refresh the Recall card index and pack, then studio doctor. | CODE: doctor green |
| 65 | Operate | `st-ops-publish` | Commit + push the studio and outputs to mrodgersjs-web/mrodgersjs-web systems-thinking/. Secrets scan first. | CODE: secret scan clean |

Work Canvas: "Systems Thinking OS · /systemsthinking" on :4912 (one card per step, loops/KPIs/goals filled).
