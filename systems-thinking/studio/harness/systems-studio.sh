#!/usr/bin/env bash
# systems-studio — phase-gated chain harness for the Systems Thinking Studio.
# Usage: systems-studio "<problem statement>"
# Runs 8 phases; each = frontier react agent call + deterministic check.
# Artifacts land in ~/.rig/systems-studio/runs/<ts-slug>/ ; DELIVERABLE.md is the product.
set -uo pipefail

STUDIO="/Users/rig128gb/Developer/rig-intelligence/packages/systems-thinking-studio"
PROBLEM="${1:?usage: systems-studio \"<problem statement>\"}"
RUNS="$HOME/.rig/systems-studio/runs"
SLUG=$(printf '%s' "$PROBLEM" | tr -cs 'a-zA-Z0-9' '-' | cut -c1-40 | tr 'A-Z' 'a-z' | sed 's/^-//;s/-$//')
RUN="$RUNS/$(date +%Y%m%d-%H%M%S)-${SLUG:-run}"
mkdir -p "$RUN"
printf '%s\n' "$PROBLEM" > "$RUN/problem.txt"
STUDIO_INPUTS=(
  --input "$STUDIO/data/archetypes.json"
  --input "$STUDIO/data/leverage-points.json"
  --input "$STUDIO/data/decision-contexts.json"
  --input "$STUDIO/templates/system-frame.md"
  --input "$STUDIO/scripts/studio.py"
  --input "$STUDIO/data/polymath-domains.json"
)
# knowledge library manifests (populated by the scrape pipeline)
for m in "$STUDIO"/knowledge/youtube/manifest.md "$STUDIO"/knowledge/papers/manifest.md; do
  [ -f "$m" ] && STUDIO_INPUTS+=(--input "$m")
done

# newest file named $1 under frontier outputs; falls back to salvaging the
# final answer block from the phase log when the agent answered in prose
latest_output() {
  find "$RUN/.apodex" -type f -name "$1" -path "*outputs*" 2>/dev/null | sort | tail -1
}

salvage_answer() {  # $1=phase log, $2=artifact name -> prints answer text or nothing
  python3 - "$1" "$2" <<'PYEOF'
import re, sys
log = open(sys.argv[1], errors="replace").read()
m = re.split(r"\[ReAct\] done", log)[0]
marks = [mm.end() for mm in re.finditer(r"^\[✓[^\n]*\]\s*$|^\[✗[^\n]*\]\s*$", m, re.M)]
block = m[marks[-1]:] if marks else ""
block = block.strip("\n-— ")
if len(block) > 400 and any(k in block.lower() for k in sys.argv[2].split("-")):
    print(block)
PYEOF
}

run_phase() {
  local num="$1" name="$2" artifact="$3" prompt="$4"; shift 4
  local checks=("$@") attempt=1 out fb
  while :; do
    echo "[phase $num $name] attempt $attempt" | tee -a "$RUN/harness.log"
    # accumulate prior artifacts as inputs
    local prior=()
    for f in brief.md frame.md diagnosis.md leverage.md grounding.md polymath.md; do
      [ -f "$RUN/$f" ] && prior+=(--input "$RUN/$f")
    done
    frontier --mode react --no-tui -y --max-turns 16 --cwd "$RUN" \
      "${STUDIO_INPUTS[@]}" ${prior[@]+"${prior[@]}"} \
      -p "Systems Thinking Studio phase $num ($name) for this problem: $(cat "$RUN/problem.txt")

$prompt

Write your artifact to outputs/$artifact (create it) with a file-write tool BEFORE writing your final message. Use absolute paths when reading /inputs. The studio CLI is at /inputs/studio.py — copy it out first (cp /inputs/studio.py .) then run with python3. Keep it tight: the artifact only." \
      > "$RUN/phase-$num-attempt$attempt.log" 2>&1
    out=$(latest_output "$artifact")
    if [ -z "$out" ]; then
      if salvage_answer "$RUN/phase-$num-attempt$attempt.log" "$artifact" > "$RUN/$artifact" 2>/dev/null && [ -s "$RUN/$artifact" ]; then
        out="$RUN/$artifact"; echo "[phase $num] salvaged answer from log" | tee -a "$RUN/harness.log"
      fi
    fi
    if [ -n "$out" ] && { [ -f "$RUN/$artifact" ] || cp "$out" "$RUN/$artifact" 2>/dev/null; }; then
      local ok=1 missing=""
      for c in "${checks[@]}"; do
        grep -qi "$c" "$RUN/$artifact" || { ok=0; missing+=" [$c]"; }
      done
      if [ "$ok" = 1 ]; then echo "[phase $num] GREEN" | tee -a "$RUN/harness.log"; return 0; fi
      fb="previous attempt failed checks:$missing — fix exactly these sections"
    else
      fb="no artifact named $artifact was produced — write it to outputs/$artifact"
      echo "[phase $num] DEGRADED (no artifact)" | tee -a "$RUN/harness.log"
    fi
    if [ "$attempt" -ge 3 ]; then
      echo "[phase $num] RED after 3 attempts" | tee -a "$RUN/harness.log"
      echo "phase $num RED: $fb" >> "$RUN/verify.log"
      exit 1
    fi
    printf '%s\n' "$fb" > "$RUN/feedback-$num-$attempt.txt"
    attempt=$((attempt+1))
  done
}

run_phase 01 INTAKE brief.md \
  "Write the intake brief. Sections required: '## Problem' (restate precisely), '## Success looks like' (observable outcomes), plus stakes, constraints, deadline, requester." \
  "## Problem" "## Success looks like"

run_phase 02 FRAME frame.md \
  "Copy /inputs/system-frame.md as your frame and FILL every numbered section for this problem (boundary, stocks table, flows, actors, loops R+B, delays, measurement). Read /inputs/decision-contexts.json and add: '## Decision Context' (clear|complicated|complex|chaotic|disorder), '## Response mode', and '## Classification confidence'. Select the matching response mode; if DISORDER, decompose before recommending leverage. Use /inputs/archetypes.json and /inputs/leverage-points.json as reference. 'Unknown' is a valid entry; blanks are not." \
  "Stocks" "Reinforcing" "Balancing" "Delay" "Decision Context" "Response mode"

run_phase 03 DIAGNOSE diagnosis.md \
  "Run: cp /inputs/studio.py . && python3 studio.py map \"<the problem's symptom words>\". Then verify the top archetype's predicted stock is actually moving in this situation. Required sections: '## Suspect' (archetype + confidence + matched symptoms), '## Evidence', '## Counterintuitive point' (quote it and say whether we accept it)." \
  "Suspect" "Evidence" "Counterintuitive"

run_phase 04 LEVERAGE leverage.md \
  "Read frame.md first. If its decision context is DISORDER, write a RED finding and do not select leverage. Otherwise run: python3 studio.py leverage. Required sections: '## Current rank' (where existing interventions sit, 12-1), '## Chosen intervention' (highest rank the requester's authority allows, with the rank number), '## Rejected higher option' (one rank higher, why not now)." \
  "rank" "Chosen" "Rejected"

run_phase 05 GROUND grounding.md \
  "Ground in evidence: python3 studio.py cards systems-thinking; python3 studio.py search \"<topic>\" exhaustive; read /inputs/frame.md and /inputs/diagnosis.md; ALSO read the knowledge manifests mounted at /inputs/manifest.md (YouTube + papers distilled source cards — use the relevant ones). Cite everything as [Card: title](url) or source url. Required: '## Citations' and '## Gaps' (what the corpus does NOT cover — absent evidence is a finding)." \
  "Citations" "## Gaps"

run_phase 06 POLYMATH polymath.md \
  "Polymathic cross-domain import. Read /inputs/polymath-domains.json. Run: python3 studio.py crosspoll \"<the target structure from frame.md: loop, delay, stock, constraint>\". Then execute the 7-step protocol it prints: state target structure, pick 3+ non-native domains, list structurally-matching mechanisms, write concrete IMPORTS ('in <target>, <mechanism> implies <measurable intervention>'), score transfer validity (structural-similarity x mechanism-clarity x testability, keep >= 0.60), keep top 3, REJECT metaphor-only imports with reasons. Required sections: '## Target structure', '## Candidate imports', '## Top imports', '## Rejected (metaphor-only)'." \
  "## Target structure" "## Top imports" "## Rejected"

run_phase 07 SYNTHESIZE DELIVERABLE.md \
  "Synthesize brief+frame+diagnosis+leverage+grounding+polymath into the deliverable. Required: '## What is happening' (the system story), '## What to do' (ranked interventions each tagged with its leverage rank + owner), '## Falsifier' (observation + deadline that kills this analysis), '## Rejected' (what was considered and why not — include the rejected polymath imports). No new claims beyond grounding." \
  "## What is happening" "## What to do" "## Falsifier" "## Rejected"

# Phase 08 VERIFY — deterministic only + ProofPacket seal
{
  echo "== systems-studio verify $(date)"
  ok=1
  for f in brief.md frame.md diagnosis.md leverage.md grounding.md polymath.md DELIVERABLE.md; do
    if [ -s "$RUN/$f" ]; then echo "PASS $f ($(wc -l < "$RUN/$f") lines)"; else echo "FAIL $f missing/empty"; ok=0; fi
  done
  if grep -A3 -i '^## Decision Context' "$RUN/frame.md" | grep -qi 'disorder'; then
    echo "FAIL context remains DISORDER — decompose before leverage"; ok=0
  elif grep -qi '^## Decision Context' "$RUN/frame.md" && grep -qi '^## Response mode' "$RUN/frame.md"; then
    echo "PASS context classification and response mode"
  else
    echo "FAIL context classification"; ok=0
  fi
  if grep -qE '\[[0-9]+\]|rank' "$RUN/leverage.md" && grep -qi 'falsifier' "$RUN/DELIVERABLE.md" && grep -q 'Rejected (metaphor-only)' "$RUN/polymath.md"; then
    echo "PASS structure (leverage rank + falsifier + polymath gate)"
  else echo "FAIL structure"; ok=0; fi
  if [ "$ok" = 1 ]; then
    echo "RUN GREEN — deliverable: $RUN/DELIVERABLE.md"
    if [ -f "$STUDIO/proofpacket/seal.py" ]; then
      ( cd "$RUN" && python3 "$STUDIO/proofpacket/seal.py" --out proofpacket.json \
          --name "systems-studio-run" --verifier "harness" \
          --evidence "8-phase chain: all deterministic checks green" \
          problem.txt brief.md frame.md diagnosis.md leverage.md grounding.md polymath.md DELIVERABLE.md \
        && echo "SEALED proofpacket.json ($(python3 -c "import json;d=json.load(open('proofpacket.json'));print(d.get('packet_hash','?')[:16])" 2>/dev/null))" )
    fi
  else
    echo "RUN RED"
  fi
} >> "$RUN/verify.log" 2>&1
cat "$RUN/verify.log"
echo "run dir: $RUN"
