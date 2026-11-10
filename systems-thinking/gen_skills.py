#!/usr/bin/env python3
"""Generate the /systemsthinking metaskill + step skills from one table. Re-run to regenerate."""
import json, os, sys, pathlib
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "skills")
ST = "python3 ~/Developer/rig-intelligence/packages/systems-thinking-studio/scripts/studio.py"
# (slug, stage, what it does, tool/command, artifact, jev gate)
S = [
("intake-brief","Intake","Write the brief: problem, requester, stakes, constraints, deadline, what success looks like.","templates in studio/processes/deep/01-intake.md","brief.md","CODE: headings ## Problem and ## Success looks like exist"),
("intake-symptom","Intake","Capture the symptom in the requester's own words, with when it started and how often it returns.","studio map \"<symptom>\" (dry read)","brief.md#symptom","none"),
("intake-stakes","Intake","Name who loses what if nothing changes, in one number with its source.","read the source system","brief.md#stakes","none"),
("intake-authority","Intake","Record what the requester may change (authority ceiling). It caps the leverage rank later.","ask or read org doc","brief.md#authority","none"),
("intake-context-classify","Intake","Classify the decision context: clear, complicated, complex, chaotic, disorder. Disorder is RED.",f"{ST} context <ctx>","brief.md#context","JEV choice: context class (rig-s1gate), DEFERRED if down"),
("intake-done-test","Intake","Write the falsifiable success test that fails today and will pass when fixed.","goal new --done-test","done-test.sh","CODE: script exits non-zero today"),
("frame-boundary","Frame","Draw the system boundary: what is inside, outside, and ignored on purpose.",f"{ST} frame <name>","frame.md#boundary","none"),
("frame-domain","Frame","Start from a domain frame (gtm, linkedin, sales, founder, mike-os), never a blank page.",f"{ST} frame --domain <d>","frame.md","none"),
("frame-stocks","Frame","List the stocks (things that accumulate) with unit and current level.","frame template","frame.md#stocks","CODE: every stock has a unit"),
("frame-flows","Frame","List inflows and outflows for each stock with rate and source.","frame template","frame.md#flows","none"),
("frame-actors","Frame","Name the actors, their goals and the information each one sees.","frame template","frame.md#actors","none"),
("frame-loops","Frame","Find at least one reinforcing (R) and one balancing (B) loop. Label polarity on every link.","frame template","frame.md#loops","CODE: >=1 R and >=1 B"),
("frame-delays","Frame","Mark every delay and its length; delays are where oscillation and overshoot come from.","frame template","frame.md#delays","none"),
("frame-controller","Frame","Name the controller, observed state, sampling delay, allowed action and UNKNOWN route.","processes/source-gated-tranche.md","frame.md#controller","CODE: missing observation = BLOCKED"),
("diagnose-map","Diagnose","Run the symptom against the archetype table and get ranked suspects.",f"{ST} map \"<symptom>\"","diagnosis.md#suspect","none"),
("diagnose-archetype","Diagnose","Read the suspect archetype (Kim 2000) and its classic intervention.",f"{ST} archetype <id>","diagnosis.md","none"),
("diagnose-fixes-that-fail","Diagnose","Test for Fixes that Fail: the quick fix's side effect that returns the problem worse.",f"{ST} archetype fixes-that-fail","diagnosis.md","none"),
("diagnose-shifting-burden","Diagnose","Test for Shifting the Burden: symptomatic fix eroding the fundamental capability.",f"{ST} archetype shifting-the-burden","diagnosis.md","none"),
("diagnose-limits-growth","Diagnose","Test for Limits to Growth: find the limiting condition before pushing harder.",f"{ST} archetype limits-to-growth","diagnosis.md","none"),
("diagnose-evidence","Diagnose","Prove the suspect's predicted stock is actually moving, with a dated read.","source read","diagnosis.md#evidence","JEV bool: evidence supports suspect"),
("diagnose-counterintuitive","Diagnose","Write the counterintuitive finding: what the obvious push would make worse.","judgment","diagnosis.md#counterintuitive","none"),
("diagnose-doom-loop","Diagnose","Name any doom loop (self-reinforcing failure) in the agent fleet or lane and its breaker.","studio operating gaps","diagnosis.md#doom-loop","none"),
("leverage-rank","Leverage","Place current interventions on Meadows' 12 points (12 weakest, 1 strongest).",f"{ST} leverage all","leverage.md","none"),
("leverage-choose","Leverage","Choose the highest rank the requester's authority allows.",f"{ST} leverage --rank N","leverage.md#chosen","JEV choice: rank pick"),
("leverage-reject","Leverage","Record the one-rank-higher option and why it was rejected.","judgment","leverage.md#rejected","none"),
("leverage-wip-cap","Leverage","Set WIP cap, queue-age signal, drain condition and bottleneck owner before adding capacity.","source-gated tranche","leverage.md#wip","CODE: more agents rejected until constraint evidenced"),
("leverage-information","Leverage","Check rank-6 information flows: who would act differently if they saw the stock?",f"{ST} simulate <domain>","leverage.md#info","none"),
("leverage-rules-goals","Leverage","Check rules (5), self-organization (4) and goals (3) before parameters (12).","leverage-points.json","leverage.md","none"),
("ground-cards","Ground","Pull tagged Recall cards for the domain.",f"{ST} cards <tag>","grounding.md#citations","none"),
("ground-search","Ground","Search the live Recall KB for the mechanism.",f"{ST} search \"<q>\" exhaustive","grounding.md","none"),
("ground-library","Ground","Read the papers/books/youtube library under studio/knowledge.","studio/knowledge","grounding.md","none"),
("ground-cite","Ground","Cite as [Card: title](url). Never invent a citation.","card-index.json","grounding.md#citations","CODE: every cite resolves to a card id"),
("ground-gaps","Ground","Write ## Gaps: absent evidence is a finding, not a blank.","judgment","grounding.md#gaps","none"),
("ground-theory-spine","Ground","Verify theory provenance against the theory spine.","scripts/verify_theory_spine.py","verify.log","CODE: exit 0"),
("polymath-crosspoll","Polymath","Import a mechanism from another domain with the same structure.",f"{ST} crosspoll \"<structure>\" <domain>","polymath.md","none"),
("polymath-mechanisms","Polymath","Pull source-gated transfers from curated mechanisms.",f"{ST} mechanisms <q>","polymath.md","none"),
("polymath-score","Polymath","Score transfer fit; GREEN needs >= 0.60.","polymath-domains.json","polymath.md#score","JEV score: transfer fit"),
("polymath-deviate","Polymath","Run /deviate engines on the chosen leverage point for far-from-obvious options.","/deviate","polymath.md#deviations","none"),
("polymath-falsify","Polymath","Write the falsifier: the observation that would kill the imported mechanism.","judgment","polymath.md#falsifier","none"),
("synth-simulate","Synthesize","Run the Euler stock-flow model: baseline vs +volume vs information intervention.",f"{ST} simulate <domain>","simulation.md","none"),
("synth-deliverable","Synthesize","Assemble DELIVERABLE.md from every prior artifact; shrink nothing silently.","assemble","DELIVERABLE.md","none"),
("synth-causal-map","Synthesize","Draw the causal loop diagram (Excalidraw/SVG) with the leverage point marked.","scripts/gen_diagrams.py","causal-map.svg","JEV image check (dual judge)"),
("synth-plan","Synthesize","Write the falsifiable plan: one intervention, owner, date, KPI, kill criterion.","judgment","DELIVERABLE.md#plan","none"),
("synth-second-order","Synthesize","List second-order effects and who they hit, 1 week / 1 quarter / 1 year.","judgment","DELIVERABLE.md#effects","none"),
("synth-reversibility","Synthesize","Assess reversibility; irreversible steps go to Gate-D.","aops/REVERSIBILITY-ASSESSMENT.md","DELIVERABLE.md#reversibility","HUMAN: Gate-D for irreversible"),
("verify-run-det","Verify","Run the deterministic 8-phase path; GREEN only if classified, map hits, rank != 12, knowledge >= 2, polymath >= 0.60.",f"{ST} run \"<problem>\" --domain d --context c","run.json","CODE: exit 0"),
("verify-red-control","Verify","Run the planted RED (context disorder) and confirm it fails. A gate never failed is not trusted.",f"{ST} run \"x\" --context disorder","verify.log","CODE: must exit non-zero"),
("verify-seal","Verify","Seal the ProofPacket.","proofpacket/seal.py","proofpacket.json","CODE: seal verifies"),
("verify-jev-done","Verify","Gate the done claim with hosted Jev before calling it done.","rig-s1gate check done.claim","decision id","JEV: done.claim; DEFERRED if down, never PASS"),
("verify-jev-everywhere","Verify","Walk the jev-everywhere ladder for every judgment in the run: CODE, JEV, SYSTEM 2, HUMAN.","/jev-everywhere","jev-map.md","JEV: one decision id per typed judgment"),
("verify-jevharness-domain","Verify","Wrap the 8 phases as a /jevharness switch domain (typed questions per phase) and replay it.","/jevharness-new-domain, /jevharness-rig-gate","harness trace","JEV: harness run + replay match"),
("verify-cold-review","Verify","Zero-context (goldfish) review of DELIVERABLE.md; fix what it cannot follow.","subagent, no context","review.md","none"),
("loop-define","Loops","Turn the plan into a rig-loop: trigger, step, check, stop condition.","rig-loop","loop.yaml","none"),
("loop-cadence","Loops","Place it on the operating cadence; heavy work runs 21:00-06:00 MT, staggered.",f"{ST} operating daily|weekly","cadence.md","none"),
("loop-no-progress","Loops","Detect spin: same check tail twice = change strategy, not retry.","goal-loop","turns.jsonl","CODE: progress guard"),
("kpi-define","KPIs","Define the KPI: before, target, window, unit, probe command, source.","goal new --kpi-*","kpi.json","CODE: probe runs and prints a number"),
("kpi-probe","KPIs","Run the KPI probe; a missing source prints no_source, never zero.","ak-kpi / probe","kpi.log","CODE: no_source != 0"),
("kpi-scorecard","KPIs","Post the KPI to the systems-thinking scorecard on the Work Canvas.","Work Canvas API :4912","canvas stat card","none"),
("goal-register","Goals","Register the goal: mission + KPI + done-test, bound to the loop.","goal new ... --done-test","goals/<slug>","CODE: goal check exits 1 today"),
("goal-check","Goals","Run goal check; the exit code is the verdict, never the doer.","goal check <slug>","RESULT.json","CODE: exit code"),
("goal-close","Goals","Close with proof: decision id, ProofPacket, canvas updated, three-line report.","/goal-complete","proof","JEV: done.claim"),
("ops-daily","Operate","Daily: one causal map or leverage spec for a live RIG bottleneck (systems-thinking employee KPI).","studio run","work/<date>/","none"),
("ops-weekly-retro","Operate","Weekly: what loops moved, which KPIs moved, which held. Retire zero-output steps.","/goal-retro","retro.md","none"),
("ops-refresh-corpus","Operate","Refresh the Recall card index and pack, then studio doctor.","scripts/recall_fetch_all.py + recall_merge_tags.py","data/card-index.json","CODE: doctor green"),
("ops-publish","Operate","Commit + push the studio and outputs to mrodgersjs-web/mrodgersjs-web systems-thinking/. Secrets scan first.","git","commit","CODE: secret scan clean"),
]
def main():
    meta = OUT / "systemsthinking"; meta.mkdir(parents=True, exist_ok=True)
    stages = []
    for s in S:
        if s[1] not in stages: stages.append(s[1])
    rows = []
    for i, (slug, stage, what, tool, art, jev) in enumerate(S, 1):
        name = f"st-{slug}"; d = OUT / name; d.mkdir(parents=True, exist_ok=True)
        nxt = f"st-{S[i][0]}" if i < len(S) else "systemsthinking (done)"
        (d / "SKILL.md").write_text(f'''---
name: "{name}"
description: "Step {i} of /systemsthinking ({stage}): {what.replace('"', "'")}"
---

# {name}: step {i} of /systemsthinking ({stage})

> Deterministic first, LLM only where judgment is needed, verify always. Typed judgments go to hosted Jev
> (`rig-s1gate`) before any frontier model; Jev down = DEFERRED, never PASS. The studio advises; outward,
> paid or irreversible actions stop at Gate-D for Mike's approval of the exact text.

**Does:** {what}
**Tool:** `{tool}`
**Artifact:** `{art}`
**Jev / gate:** {jev}

## Steps
1. Read the prior artifact (the brief is the contract; never shrink it silently).
2. Run the tool. Write the artifact with real content; "unknown" is an answer, blank is not.
3. Apply the gate above. Red = stop and say what is missing.
4. Log one line to the run's EVIDENCE.md: step, artifact path, gate result, decision id if any.

## Done when
- `{art}` exists with real content and the gate above is green (or DEFERRED with reason).

Next: `{nxt}`. Router: `/systemsthinking`.
''')
        rows.append((i, stage, name, what, jev))
    table = "\n".join(f"| {i} | {st} | `{n}` | {w} | {j} |" for i, st, n, w, j in rows)
    (meta / "SKILL.md").write_text(f'''---
name: systemsthinking
description: "Systems thinking front door: map a problem as stocks, flows, loops, archetypes and Meadows leverage, ground it, import a polymath mechanism, ship a falsifiable plan, then run it as a /loop with KPIs and a /goal, Jev-gated (jev-everywhere + jevharness). Routes {len(S)} step skills across {len(stages)} stages."
---

# /systemsthinking: {len(S)} step skills, {len(stages)} stages

**Triggers:** /systemsthinking, /systems-thinking, "why does this keep happening", plateau, quick fix keeps failing,
causal map, leverage point, archetype, doom loop, stock and flow, GTM/sales/founder architecture.
**Engine:** Systems Thinking Studio (`studio` CLI, `{ST}`), 8-phase contract in
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
{table}

Work Canvas: "Systems Thinking OS · /systemsthinking" on :4912 (one card per step, loops/KPIs/goals filled).
''')
    json.dump([{"n": i, "stage": st, "name": n, "what": w, "jev": j} for i, st, n, w, j in rows],
              open(OUT / "steps.json", "w"), indent=1)
    print(len(S), "steps", stages)
main()
