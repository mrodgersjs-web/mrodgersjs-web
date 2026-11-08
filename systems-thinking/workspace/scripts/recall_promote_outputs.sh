#!/usr/bin/env bash
# Promote a frontier mission run's outputs into the repo's knowledge/recall
# tree, then run the deterministic merge gate as the authoritative check.
# Usage: scripts/recall_promote_outputs.sh <run-dir>
set -euo pipefail

RUN="${1:?usage: recall_promote_outputs.sh <run-dir>}"
OUT="$RUN/outputs"
[ -d "$OUT" ] || { echo "no outputs dir in $RUN" >&2; exit 1; }

W=$(pwd)
# bring back batch tag outputs, domain packs, indexes, raw search evidence
for p in tags/batch-01.out.jsonl tags/batch-02.out.jsonl tags/batch-03.out.jsonl \
         tags/batch-04.out.jsonl tags/batch-05.out.jsonl tags/batch-06.out.jsonl \
         card-index.json README.md; do
  [ -f "$OUT/$p" ] && cp "$OUT/$p" "knowledge/recall/$p" && echo "promoted $p"
done
for d in domains by-domain; do
  [ -d "$OUT/$d" ] && mkdir -p "knowledge/recall/$d" && cp "$OUT/$d"/* "knowledge/recall/$d"/ && echo "promoted $d/"
done
shopt -s nullglob
for f in "$OUT"/raw/*-search.json; do
  cp "$f" knowledge/recall/raw/ && echo "promoted raw/$(basename "$f")"
done

echo "== merge gate (repo-authoritative) =="
python3 scripts/recall_merge_tags.py
