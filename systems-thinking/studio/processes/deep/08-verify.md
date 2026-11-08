# Deep Process 08 — VERIFY → `verify.log` + `proofpacket.json`

> Deepens `processes/phases.md` §07 (the deterministic tail, slot 08 in the
> 8-phase chain). Harness: a bash block — no agent call — checking artifact
> presence/size, `grep -qE '\[[0-9]+\]|rank' leverage.md`,
> `grep -qi 'falsifier' DELIVERABLE.md`, appending PASS/FAIL lines to
> `$RUN/verify.log`, ending `RUN GREEN` or `RUN RED`. The deep contract adds
> the polymath gates, citation resolution, and the ProofPacket seal:
> sha256-hashing every artifact into `$RUN/proofpacket.json` via
> `proofpacket/seal.py`, then proving it with `proofpacket/verify.py`.

## Purpose

VERIFY is the studio's honesty layer, and it is deliberately stupid: no
LLM, no judgment, just mechanical checks and hashes. Three jobs. (1) Every
phase's artifact exists and is non-empty — including DEGRADED phases, so a
proxy-down run ships honest failure, never silent absence. (2) The structural
promises grep-true: ranks present, falsifier dated, polymath contract
sections in place, citations resolvable. (3) The whole run is sealed into a
tamper-evident ProofPacket: each artifact gets a SHA-256, the packet gets a
canonical integrity hash, optionally an HMAC signature — so "this is what
the studio concluded, from these exact bytes" becomes a checkable claim
weeks later. A green without a seal is an unverifiable opinion.

## Entry criteria

- Phases 01-07 have each returned GREEN, RED-after-3, or logged DEGRADED —
  the harness reached the verify block (`$RUN/harness.log` ends with a
  phase-07 outcome).
- All artifacts the run claims exist in `$RUN` (`brief.md frame.md
  diagnosis.md leverage.md grounding.md polymath.md DELIVERABLE.md`; verify
  log itself is created here).
- `proofpacket/seal.py` + `proofpacket/verify.py` available under the
  package (`$STUDIO/proofpacket/`), python3 present. `PROOFPACKET_KEY`
  optional (signature-only feature).

## Inputs

| Input | Where | Use |
|---|---|---|
| `$RUN/*.md` artifacts | run dir | the bytes being verified and sealed |
| `$RUN/harness.log` | run dir | phase outcomes (GREEN/RED/DEGRADED trail) |
| `data/card-index.json` | package | citation resolution for `[Card: …]` claims |
| `proofpacket/seal.py` | `$STUDIO/proofpacket/seal.py` | sha256 + canonical packet hash (+ optional HMAC) → `proofpacket.json` |
| `proofpacket/verify.py` | `$STUDIO/proofpacket/verify.py` | re-hash artifacts, check packet integrity/signature |
| `PROOFPACKET_KEY` | env (optional) | HMAC-SHA256 signing key for WHO-sealed proof |

## Procedure

1. [det] Presence: for each artifact in `brief.md frame.md diagnosis.md
   leverage.md grounding.md polymath.md DELIVERABLE.md` — `[ -s "$RUN/$f" ]`
   → `PASS $f ($(wc -l < $f) lines)` else `FAIL $f missing/empty`, ok=0.
2. [det] Structure: `grep -qE '\[[0-9]+\]|rank' "$RUN/leverage.md"` and
   `grep -qi 'falsifier' "$RUN/DELIVERABLE.md"` → `PASS structure` else
   `FAIL structure`, ok=0.
3. [det] Phase-section sweep (deep addition): each artifact greps its
   contract headings — brief `## Problem`+`## Success looks like`; frame
   `Stocks`+`Reinforcing`+`Balancing`+`Delay`; diagnosis `## Suspect`+
   `## Evidence`+`## Counterintuitive`; leverage `rank`+`Chosen`+
   `Rejected`; grounding `Citations`+`## Gaps`; polymath `## Target
   structure`+`## Candidate imports`+`## Top imports`+`## Rejected`;
   DELIVERABLE its four sections. Any miss → `FAIL sections <artifact>`,
   ok=0.
4. [det] Falsifier dated: `grep -E '[0-9]+ ?weeks?|20[0-9]{2}'` inside the
   deliverable's falsifier context → else `FAIL falsifier undated`, ok=0.
5. [det] Citation resolution (deep addition): every `[Card: title](url)` in
   grounding.md resolves against `data/card-index.json` (title substring,
   case-insensitive) or the artifact explicitly recorded the corpus as
   absent. Ghost citations → `FAIL citations`, ok=0.
6. [det] Verdict: append everything to `$RUN/verify.log`; `RUN GREEN` only
   if ok=1, else `RUN RED`. RED never blocks the seal (step 7 seals the
   honest state) but is the last line a reader sees.
7. [det] Seal — hash every artifact into the run's ProofPacket:
   ```bash
   cd "$RUN"
   python3 "$STUDIO/proofpacket/seal.py" \
     --out proofpacket.json \
     --name "$SLUG" --verifier "systems-studio" \
     --evidence "8-phase run; phase gates + deep checks in verify.log; artifacts hashed at verify time" \
     --base "$RUN" \
     brief.md frame.md diagnosis.md leverage.md grounding.md \
     polymath.md DELIVERABLE.md verify.log harness.log problem.txt
   ```
   (seal.py warns on missing files and records them `exists:false` — a
   DEGRADED run seals its gaps visibly rather than skipping them.)
8. [det] Optional signature: with `PROOFPACKET_KEY` set, add `--sign`; the
   packet then carries an HMAC-SHA256 over the packet hash proving WHO
   sealed it. Without the key, integrity still holds (what), provenance
   doesn't (who).
9. [det] Prove the seal round-trips:
   ```bash
   python3 "$STUDIO/proofpacket/verify.py" "$RUN/proofpacket.json"
   # → [1] INTEGRITY PASS  [2] ARTIFACTS PASS (n/n hashes match)  === VERIFIED ===
   # add --check-signature (with key) for [3] SIGNATURE PASS
   ```
   Append the verifier output to verify.log. Exit ≠ 0 → `FAIL proofpacket`,
   ok=0 (a packet that cannot verify itself is worse than none).
10. [det] Tamper spot-check (deep addition, cheap): flip one byte in a
    scratch copy of an artifact listed in the packet, re-run verify.py
    against the original packet with `--base` pointed at the scratch dir →
    expect ARTIFACTS FAIL; delete the scratch. This proves the seal bites.
11. [det] Chain check: confirm each phase's attempt logs exist
   (`phase-01..07-attempt*.log`) and record attempt counts in verify.log —
   a phase that passed on attempt 3 is a fragility signal even when GREEN.
   Unread `feedback-*.txt` files (retry hints for a phase that never
   re-ran) are flagged, not discarded.
12. [det] Red-run sealing: if the run is RED, still execute steps 7-9 —
   seal the failed state with `--evidence "RED run sealed for forensics"`.
   Honest failure with a hash beats a silent gap; exit nonzero either way.
13. [det] Index update: append `"<run-dir>": {"packet": "<sha256>",
   "verdict": "GREEN|RED", "sealed_at": "<ts>"}` to
   `~/.rig/systems-studio/runs/index.json` when that file exists (create
   nothing new outside the run dir otherwise).
14. [det] Final line: rewrite the verdict considering the seal —
   `RUN GREEN — sealed sha256:<packet_sha256>` or `RUN RED`. Emit
   `$RUN/verify.log` to stdout and print the run dir.
15. [det] Consumption proof: close verify.log with the two commands any
   later consumer runs to re-verify the run unaided —
   `python3 $STUDIO/proofpacket/verify.py <run>/proofpacket.json` and
   `grep -E 'RUN (GREEN|RED)' <run>/verify.log`. A run that cannot be
   re-verified in five seconds will not be re-verified at all.

## Deterministic checks

This phase IS checks. The full gate list it executes:

1. Artifact presence/size for all seven phase artifacts (harness mirror).
2. `grep -qE '\[[0-9]+\]|rank' leverage.md`; `grep -qi 'falsifier'
   DELIVERABLE.md` (harness mirror).
3. Per-artifact section contracts (step 3 sweep; the harness's phase greps,
   re-run as a set).
4. Falsifier carries a date/week horizon.
5. `[Card:]` citations resolve to `card-index.json` or corpus recorded absent.
6. `python3 verify.py proofpacket.json` exits 0, prints `=== VERIFIED ===`,
   artifact count matches the sealed list, every sha256 recomputes equal.
7. Packet integrity: recomputed canonical-hash equals stored `packet_sha256`
   (verify.py check [1] — catches packet edits, not just artifact edits).
8. With `--check-signature`: HMAC valid for the key.
9. `grep -c '^FAIL' verify.log` == 0 AND last line matches
   `RUN GREEN` for a green run; any FAIL or a RED verdict is shipped as-is.

## Failure modes

1. **Green theater** — checks that can't fail (grep patterns matching any
   prose, e.g. bare `rank`). Countermeasure: anchor checks to section
   headings and dated patterns (steps 3-4); every check should have a
   concrete failure mode you have seen or planted.
2. **Seal-and-edit** — artifact edited after sealing; packet now lies.
   Countermeasure: verify.py at consumption time (step 9 is cheap; anyone
   consuming the run re-runs it); freeze rule from phase 07.
3. **Silent skip on DEGRADED** — missing polymath.md (proxy-down run)
   quietly dropped from the seal list. Countermeasure: seal the declared
   list; seal.py records `exists:false` — absence is visible in the packet,
   and verify.log says which phase was DEGRADED.
4. **Sealing the wrong directory** — `--base` mismatch stores absolute or
   wrong-relative paths; verify.py then resolves nothing.
   Countermeasure: always `--base "$RUN"`, run from `$RUN`; verify.py's
   default base is the packet's own dir.
5. **Unsigned provenance overclaim** — unsigned packet presented as
   "authenticated". Countermeasure: unsigned = integrity-only; the words
   "who sealed it" require `--sign` + key custody.
6. **Log oracle drift** — verify.log edited post-hoc to flip a FAIL.
   Countermeasure: verify.log is itself sealed (it's in the artifact list);
   post-seal edits break the packet hash.
7. **Check sprawl** — 40 greps, half stale, maintainers disable the phase.
   Countermeasure: checks mirror the phase prompts' required sections 1:1;
   new checks come in only with a planted-failure demonstration.
8. **RED swallowed** — run ends RED but exit code 0 and nobody notices.
   Countermeasure: the harness propagates ok to its exit status; CI treats
   any `RUN RED` as failure while still archiving the sealed run dir.

## Worked example

From `~/.rig/systems-studio/runs/20260828-112908-our-linkedin-content-engine-tripled-outp/verify.log`
(7-phase era — no polymath.md, no seal yet; the deep 08 adds both):

> "PASS brief.md (      30 lines)
> PASS frame.md (      82 lines)
> PASS diagnosis.md (      33 lines)
> PASS leverage.md (      44 lines)
> PASS grounding.md (      90 lines)
> PASS DELIVERABLE.md (      65 lines)
> PASS structure (leverage rank + falsifier)
> RUN GREEN — deliverable: /Users/rig128gb/.rig/systems-studio/runs/
> 20260828-112908-our-linkedin-content-engine-tripled-outp/DELIVERABLE.md"

Note what the era's log could NOT say: that diagnosis.md's sections were
checked (phase 03 shipped no gate), that grounding's citations resolved,
or that any of it was sealed. The deep 08 run of the same problem would add
`PASS polymath.md (… lines)`, `PASS sections`, `PASS citations`,
`[verify] === VERIFIED ===`, and close with
`RUN GREEN — sealed sha256:<packet hash>`; seal.py would have printed:

> "[seal] wrote proofpacket.json
> [seal]   artifacts : 10
> [seal]   sealed_at : 2026-08-28T…Z
> [seal]   packet    : sha256:<64-hex>"

## Depth extensions

- **Planted-failure regression**: once per harness change, break a copy of
   a green run (delete polymath.md; edit DELIVERABLE.md post-seal) and prove
   verify goes RED / verify.py FAILs — keep the transcript as the checks'
   own proof they can fail.
- **Cross-run chain**: seal a monthly `index.json` listing each run's
   packet hash; a run that vanishes or mutates then breaks the chain, not
   just its own packet.
- **Signature custody**: rotate `PROOFPACKET_KEY`, keep the verifying key
   in a separate location from the sealing env; a sealed+signed run then
   distinguishes studio-sealed from human-sealed artifacts.
- **Check coverage report**: emit which claims in DELIVERABLE.md are
  machine-checked vs merely present (rank tags, falsifier date, citations)
  — the unchecked remainder is the trust surface; make it explicit.
- **Deterministic re-verify mode**: `--timestamp` on seal.py makes packets
  byte-reproducible; seal twice in CI and diff — any drift is tooling
  nondeterminism, not content.
- **Consumption contract**: publish the two-command proof for downstream
  consumers (verify.py + one grep of the verdict line) in the run's
  README slot; a deliverable that can't be re-verified in 5 seconds won't
  be.

## Handoff

The run is complete; VERIFY hands to the consumer, not another phase:
- `$RUN/DELIVERABLE.md` — the decision document (frozen);
- `$RUN/verify.log` — the deterministic trail, every PASS/FAIL with line
  counts, ending in the verdict;
- `$RUN/proofpacket.json` — per-artifact sha256 + sizes, canonical packet
  hash, optional HMAC signature; re-provable forever with
  `python3 proofpacket/verify.py <run>/proofpacket.json`;
- `$RUN/harness.log` + phase attempt logs — the retry/feedback history for
  forensics;
- the open instrument list (Unknowns carried through grounding → deliverable)
  — the seed of the NEXT run, whose brief should open with those readouts.
