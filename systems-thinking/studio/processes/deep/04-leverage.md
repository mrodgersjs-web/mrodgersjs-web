# Deep Process 04 — LEVERAGE → `leverage.md`

> Deepens `processes/phases.md` §04 and `workflows/find-leverage.md`. Harness
> gate: `run_phase 04 LEVERAGE leverage.md` greps `rank`, `Chosen`, `Rejected`
> (case-insensitive). Data: `data/leverage-points.json` — Meadows' 12 places
> to intervene, rank 12 (parameters) weakest → rank 1 (transcend paradigms)
> strongest, each with a `question` and `note` field.

## Purpose

LEVERAGE answers "where do we push?" with Meadows' 12-rank ladder instead of
habit. Two laws govern: (1) choose the HIGHEST rank the requester's authority
allows, not the highest that exists — an intervention above your authority is
a wish, below your authority is a waste of it; (2) the one-rank-higher option
must be written down and explicitly rejected with a reason, because the gap
between what we chose and what we refused IS the diagnostic about who owns
the system. The phase also guards the counterintuitive point accepted in
phase 03: a rank-12 push that violates it is the pathology restated as a plan.

## Entry criteria

- Phase 03 GREEN: `$RUN/diagnosis.md` exists with a verified archetype, an
  accepted counterintuitive point, and an intervention direction.
- Requester authority known or bounded (brief §Requester) — this is the cap.
- `studio.py` in the working directory.

## Inputs

| Input | Where | Use |
|---|---|---|
| `diagnosis.md` | `/inputs/diagnosis.md` | intervention direction + counterintuitive constraint |
| `frame.md` | `/inputs/frame.md` | the structures each rank would rewrite |
| `brief.md` | `/inputs/brief.md` | authority ceiling, forbidden moves, deadline |
| `studio leverage` | CLI | the 12 ranks with questions/notes (deterministic print) |
| `studio leverage <rank>` | CLI | one rank's detail |
| `data/leverage-points.json` | `/inputs/leverage-points.json` | canonical rank semantics + guiding questions |

## Procedure

1. [det] `python3 studio.py leverage` — print all 12 ranks with their
   `question` fields. The walk uses the questions, not just the names.
2. [agent] Build the rank-status table: one row per rank 12→1, three columns
   — rank, the concrete place in THIS system (named from the frame), and
   status: **Existing intervention** / **Unused** / **Named, not operating**.
   Most orgs discover they live at rank 12 and argue there because it is
   cheapest; make that visible.
3. [agent] `## Current rank`: name the rank where existing interventions sit,
   with the frame structure that proves it (e.g. cadence/volume/templates =
   dials on a machine whose goal is the problem).
4. [agent] Walk UP one rank at a time from current. For each step, translate
   the rank's `question` field into this system's language:
   - 11 buffers: which stock gets protected slack?
   - 10 structure: which routing/accumulation gets rewired?
   - 9 delays: which feedback gets faster, or which action rate slower?
   - 8: which error signal gets honest and timely?
   - 7: which reinforcing-loop gain gets governed, and who benefits from it
     staying high?
   - 6: who causes a consequence they never SEE — and would see it how?
   - 5: which rule changes every player's rational strategy at once?
   - 3: what single variable is the machine actually optimizing?
   - 2: what must everyone believe for this system to make sense?
5. [agent] Authority mapping: from brief §Requester, mark the highest rank
   the requester can change ALONE (owns the metric? the rule? the goal? the
   worldview?). Ranks above that line require coalition — note whose.
6. [agent] Consistency check against diagnosis: discard any candidate that
   violates the accepted counterintuitive point (usually: anything that
   pushes the growth loop harder / re-tunes parameters of the pathology).
7. [agent] `## Chosen intervention`: the highest rank within authority.
   State it as a system change with its rank number ("Rank 3 — Goals"),
   the owner, and what becomes observably different.
8. [agent] Support cast: 2-4 LOWER-numbered supporting ranks that make the
   chosen rank real (e.g. rank 6 information flow + rank 8 loop strength +
   rank 11 buffer operationalize a rank-3 goal change). Supporting ranks are
   servants, not co-equal plays — say which loop each one arms (B-loop error
   signal, R-loop gain cap).
9. [agent] `## Rejected higher option`: exactly one rank higher than chosen
   (number one smaller). Reject it explicitly with: why not NOW (authority,
   falsifiability horizon, coalition cost), and what would have to become
   true to revisit it. Also record rank-1/transcend as out of scope when
   applicable.
10. [agent] Test the choice against the archetype intervention from
    `archetypes.json` — they should rhyme; if the leverage choice contradicts
    the archetype's `intervention` field, one of the two phases is wrong.
    Reconcile now, not in synthesis.
11. [agent] Write the rank-choice falsifier: what observation within the
    brief's window proves this RANK was the wrong place to push (distinct
    from the diagnosis falsifier — this one kills the intervention locus).
12. [agent] Funding check: the chosen rank must fund (or at least not block)
    the discriminator instrument window from diagnosis — freezing the
    instrument to ship the intervention is self-defeating.
13. [det] Write `outputs/leverage.md`: `## Current rank` (table + rank
    number), `## Chosen intervention` (rank number + owner + change),
    `## Rejected higher option` (rank + why-not-now + revisit trigger).
14. [agent] Self-audit: chosen rank ≤ authority line; rejected rank is
    exactly one stronger; no supporting rank is doing the chosen rank's job
    by stealth; the counterintuitive point is honored.
15. [det] Pre-GREEN deep-check run: execute checks 2-6 below against
    `outputs/leverage.md` — especially rank-order logic (4): chosen rank
    valid, rejected exactly one stronger, full 12-row ladder present.
16. [agent] Monday test: write the first concrete action the owner takes
    next week under the chosen intervention (the meeting they book, the
    metric they re-point, the hours they protect). If no first action can
    be written, the choice is aspirational — drop to the highest rank that
    HAS a Monday action, and re-record the rejection accordingly.

## Deterministic checks

Mirror of the harness gate:

1. `grep -qi 'rank' leverage.md`, `grep -qi 'chosen' leverage.md`,
   `grep -qi 'rejected' leverage.md`.

Deeper gates:

2. Full ladder present — every rank 1..12 appears in the status table:
   ```bash
   for r in $(seq 1 12); do grep -qE "^\| $r \||\b$r —" leverage.md \
     || echo "FAIL missing rank $r"; done; echo DONE
   ```
3. Chosen rank is a real rank inside its section:
   `grep -A8 '^## Chosen' leverage.md | grep -E 'Rank [0-9]+'` returns a line.
4. Rank-order logic — rejected is exactly one rank stronger than chosen
   (smaller number):
   ```bash
   python3 - <<'PY'
   import re
   t=open('leverage.md').read()
   c=int(re.search(r'## Chosen.*?Rank (\d+)',t,re.S).group(1))
   r=int(re.search(r'## Rejected.*?Rank (\d+)',t,re.S).group(1))
   print('RANK LOGIC:','PASS' if 1<=c<=12 and r==c-1 else f'FAIL chosen={c} rejected={r}')
   PY
   ```
5. Owner present: the chosen section names an owner (grep -Ei
   'owner|requester|holds' within `## Chosen` context).
6. Why-not-now present: the rejected section contains a reason marker
   (`grep -A10 '^## Rejected' leverage.md | grep -Ei 'why not|authority|not now|cannot|unfalsifiable'`).

## Failure modes

1. **Rank tourism** — the table lists all 12 ranks but the choice was made
   before the walk (usually back at rank 12 where the argument is cheapest).
   Countermeasure: write the table BEFORE the choice; the choice must cite
   the row that justifies it.
2. **Authority inflation** — rank 3 chosen by someone who owns a dashboard,
   not the goal. Countermeasure: authority mapping (step 5) is a hard cap
   from brief §Requester; coalition ranks get named owners.
3. **Ladder skipping** — chosen rank jumps 12→3 with no supporting cast, so
   the goal change arrives with no information flow to enforce it.
   Countermeasure: support cast (step 8) mandatory; each supporting rank
   names the loop it arms.
4. **Rejection theater** — "Rank 2 rejected: too hard." No revisit trigger,
   no coalition math. Countermeasure: check 6; rejection must say why-not-NOW
   and what change reopens it.
5. **Counterintuitive violation** — chosen intervention pushes the growth
   loop the diagnosis just said to ease off. Countermeasure: step 6 + phase
   03's accepted point quoted into the artifact; reviewers grep for the
   contradiction (a rank-12 push on the diagnosed pathology).
6. **Rank mismatch with archetype** — leverage choice fights the archetype's
   own `intervention` field. Countermeasure: step 10 rhyme-test; reconcile
   or document why the system's specifics override the canonical move.
7. **Instrument cannibalization** — intervention consumes the exact window
   that would have identified the binding constraint. Countermeasure:
   step 12 funding check; freeze-first designs (cadence freeze) beat
   change-and-confound designs.
8. **Falsifier-free leverage** — the rank choice is unfalsifiable, so a
   failed intervention always blames execution. Countermeasure: rank-choice
   falsifier (step 11) distinct from the diagnosis falsifier.

## Worked example

From `~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/leverage.md`:

- Current rank named with proof (`leverage.md` §Current rank):
  > "**12 — Constants, parameters, numbers.** Cadence, posting volume (~3×),
  > templates. Dials on a machine whose goal is the problem. This is where
  > the team is arguing because it is easiest."
- The full 12-row walk exists in the artifact, e.g. (`leverage.md` table):
  > "| 6 | Information flows (who sees reply quality, time-to-reply,
  > qualified-lead yield) | Unused. Shippers see output, not consequence. |"
  > "| 11 | Buffers (reply-capacity slack vs posting hours) | Unused. Slack
  > is leftover time, not a protected stock. |"
- Chosen with authority logic + support cast (`leverage.md` §Chosen):
  > "**Rank 3 — Goals of the system.** Highest rank the requester can hold:
  > they are accountable for the engine *and* for replies/qualified inbound…
  > Make the goal real with the supporting loops… Rank 6: shippers see reply
  > quality, time-to-reply, and qualified-lead yield **per post** (not
  > impressions)."
- Rejected one-rank-higher with why-not-now (`leverage.md` §Rejected):
  > "**Rank 2 — Mindset / paradigm** … Why not now: the requester owns the
  > engine's goal and metrics, not the org's worldview. Paradigm work is
  > slow, unfalsifiable inside four weeks… preach the paradigm after the
  > numbers move, not instead of them."

## Depth extensions

- **Coalition map for rank+1**: if the rejected-higher rank is only blocked
   by coalition, name the 2-3 actors whose alignment unlocks it and what each
   wants (frame §4) — converts a rejection into a sequencing plan.
- **Rank half-life estimate**: for each candidate rank, estimate how long the
   change persists without daily defense (parameters decay in weeks; goal
   changes persist while the owner does; paradigm changes outlive them).
   Pick persistence the falsifier window requires.
- **Reverse walk**: start at rank 1 and walk DOWN, asking what the higher
   rank would make trivially unnecessary; if rank 6 information flow makes
   the rank 12 tuning harmless, that asymmetry is the argument for going high
   once instead of low forever.
- **Intervention interaction matrix**: chosen × supporting ranks, marked
   reinforce/neutral/undermine; an undermining pair (e.g. rank 7 gain cap
   fighting a rank 3 growth goal) must be resolved before phase 07.
- **Second-best rank**: record what you would do at one rank LOWER if
   authority shrinks tomorrow — makes the plan robust to org shocks and
   exposes whether the choice was rank-driven or vanity-driven.
- **Cost-per-rank honesty**: rough effort for the chosen vs rejected rank;
   a rank-2 move that costs less than a rank-3 move is a flag that the rank
   semantics are being gamed.

## Handoff

Phase 05 GROUND receives `/inputs/leverage.md`:
- the chosen rank + supporting ranks — grounding must find evidence
  specifically FOR the chosen rank's mechanism (information flows changing
  behavior, goal changes re-orienting loops), not generic systems content;
- the rejected-higher rationale — grounding may be asked to find counter-
  evidence (cases where the rank-2/paradigm move worked at this scale/time);
- the rank-choice falsifier and the instrument window the run must protect;
- the authority line (whose behavior the intervention presumes).
