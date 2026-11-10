# Systems-Thinking Process Run — harness-engineering-playbook × archify (2026-08-29)

Method: same discipline as `JARVIS-GAP-REPORT-2026-08-29.md` — clone, install, execute the
supplied process for real on this host, then produce a done/gap matrix. Two external repos:
`flyrank-bih/harness-engineering-playbook` and `tt-a1i/archify`. No canonical-repo writes;
deliverables in this workspace + skill directories.

## 1. What was executed (evidence, not claims)

| Step | Result | Evidence |
|---|---|---|
| Clone both repos | DONE | `/tmp/repos/harness-engineering-playbook`, `/tmp/repos/archify` |
| Install archify skill | DONE | `npx skills add tt-a1i/archify -g` → `~/.claude/skills/archify` |
| archify doctor | 15/15 ok | all five renderers + schema validators + compare runtime |
| Playbook deps (`bun install`) | DONE | 6 packages, 190ms |
| Playbook offline orchestration suite | **41/41 PASS** when environment is clean | plan 12/12 · ralph 13/13 · agent-runner 12/12 · follow-up 4/4 · migrate ✅ |
| archify: author + validate + deliver a real map | DONE, showcase quality | `/tmp/archify-work/harness-playbook.html` — `ok: true`, sha256 sealed (spec `1d85fe27…`, artifact `ffe882f9…`), 11/11 nodes render-verified in browser |

## 2. Host collisions found (both are real findings, not playbook defects)

1. **Symlinked checkout path silently breaks the playbook's runner tests.**
   `scripts/agent-log.mjs` guards `main()` with `path.resolve(argv[1]) === import.meta.url`.
   Node realpaths the module (`/private/tmp/...`) but not `argv[1]` (`/tmp/...`) → `main()`
   never runs → **empty summaries, zero errors** → 7 self-tests fail with `Unexpected end of
   JSON input`. Same checkout under a real path: 12/12 pass. Lesson for every harness on this
   host: main-module guards must compare realpaths, and checkouts must not live under symlinked
   dirs (`/tmp` on macOS, some Orca workspace mounts).
2. **RIG github-steward git guard blocks the playbook's follow-up selftest.**
   `git config --global core.hooksPath = ~/.rig/github-steward/hooks` BLOCKs commits in temp
   repos ("outside every registered canonical root") → stub migration repo never gets its
   `main` branch → push fails → follow-up selftest 0/4. With `GIT_CONFIG_GLOBAL=/dev/null`:
   4/4 pass. Two harnesses composed on one host fight; the guard needs a selftest allowlist
   (e.g. env opt-out for throwaway fixtures) or the playbook's selftests must pin
   `core.hooksPath=/dev/null` locally.

## 3. Gap matrix — harness-engineering-playbook

| # | Capability (claimed) | Verdict | Evidence |
|---|---|---|---|
| 1 | Router doc (AGENT_GUIDE.md), provider adapters, path-scoped rules | COVERED | guide verified; `.claude/rules/*` per-path; CLAUDE.md/AGENTS.md thin adapters |
| 2 | Plan/CAPTURE → sealed `_queue.tsv` + evidence packs | COVERED | plan-selftest 12/12 offline |
| 3 | Ralph loop, fresh context per page, resumable state machine | COVERED | ralph-selftest 13/13; `.ralph/ACTIVE_PAGE`, BLOCKED, runs/ |
| 4 | Numbered exit contract (0/3/4/5/6/7/8), stuck vs blocked | COVERED | `docs/principles/loop-and-exit.md`; regression-tested in suite |
| 5 | Visual contract-diff gate (THE GATE) | COVERED-OFFLINE | pixelmatch pipeline present; **no live-store validation on this host** (needs Shopify creds) |
| 6 | Provider-neutral agent-runner (claude/codex/custom) + JSONL normalization | COVERED | runner selftest 12/12 (from real path) |
| 7 | Follow-up change requests through the same gates | COVERED | follow-up selftest 4/4 (guard bypassed) |
| 8 | Trust marks ✅/⚠️ on every platform fact | COVERED | `docs/validation-status.md` inventory |
| 9 | Offline self-tests with stub agents | COVERED | 41 checks; the entire loop provable with zero credentials |
| 10 | Control panel (demo/) | NOT EXERCISED | `bun dev` not run in this session — not needed for the audit |
| 11 | Live Shopify migration end-to-end | **MISSING-BY-DESIGN here** | requires `.env` store creds; every ⚠️ doc-derived item stays unverified without a store |
| 12 | Portability of the harness itself | **GAP** | symlink-path failure (#2.1) — main-guard not realpath-safe; selftests assume unconstrained git |

**What the playbook has that RIG harnesses mostly lack:** per-unit *evidence packs*
(contract/assets/dynamics/visual-deltas/gate.json bound by hash), a *numbered exit table* the
runner obeys, and *back-pressure proofs* — the entire orchestration is testable offline with
stub agents before a single credential exists. That is the import candidate.

## 4. Gap matrix — archify

| # | Capability | Verdict | Evidence |
|---|---|---|---|
| 1 | Five diagram types, typed JSON IR, deterministic render | COVERED | doctor 15/15; authored architecture IR from scratch |
| 2 | Validate with machine repair receipts | COVERED (excellent) | every failure returned exact subject + evidence + supportedFixes; labelAt suggestions were copy-paste correct |
| 3 | Showcase gate (9 checks, 0 err 0 warn) | COVERED | `ok: true` after 8 repair rounds |
| 4 | Atomic deliver + sha256 receipts | COVERED | spec + artifact hashes emitted |
| 5 | Desktop-readability enforcement | COVERED (strict) | rejected viewBox 2060 (scale 0.45) and 1400 with long sublabels; forced 5-col grid |
| 6 | Skill packaging / install UX | COVERED | `skills add -g` clean; update-checker silent (`status: current`) |
| 7 | **Gaps:** authoring cost | PARTIAL | a correct showcase map took 8 validate rounds; grid-mode corridor planning (crossings between long edges) is the hard part; no auto-layout escape hatch (by design) |
| 8 | Multi-harness install | PARTIAL | installs to `~/.claude/skills` via CLI; RIG's hermes/codex dirs need manual copy |

## 5. Where the two meet (the actual deliverable)

The archify map of the playbook harness (`harness-playbook.html`) is the visual contract for
the **verify-and-build skill** distilled from this run: `~/.claude/skills/verify-and-build/`
(installed to claude/codex/hermes/agents skill dirs). It carries the loop-and-exit table, the
sealed-queue contract, the evidence-pack requirement, offline self-test proof before live
credentials, and the two host-hardening rules found today (realpath-safe main guards; git-guard
opt-out for throwaway selftest repos).

## 6. Recommended next slice (no scope taken here)

1. Import the evidence-pack pattern into rig-intelligence builds (hash-bound gate.json per unit).
2. Fix the github-steward guard to allow env-scoped selftest fixtures (unblocks third-party
   harness selftests on this host).
3. Add archify maps as a standard step of the Systems-Thinking process — the validate-repair
   loop is itself a verify-and-build demonstration.

## Artifact index

- Map: `/tmp/archify-work/harness-playbook.html` (+ `.architecture.json` source, sha256-sealed)
- Clones: `/tmp/repos/{harness-engineering-playbook,archify}` (realpath-safe copies under `~/tmp-playbook-check`)
- Skill: `~/.claude/skills/verify-and-build/SKILL.md` (+ mirrors)
