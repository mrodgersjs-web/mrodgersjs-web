# Jake Systems-Thinking Run — Evidence Pack (2026-08-29)

Mission: apply the verify-and-build discipline (sealed queue, per-unit gates, evidence packs)
to the JARVIS gap report closeout, and install the systems-thinking loop as a durable Jake
capability. Every done-claim below traces to a command + exit code run this session.

## Unit results

| Unit | Change | Gate (command → result) | Verdict |
|---|---|---|---|
| U1 R1 wildcard bind | `server/src/index.ts` serve() gained `hostname: process.env.SERVER_HOST ?? "127.0.0.1"`; `.env` PORT 3001→3005 (aligned to estate contract) + `SERVER_HOST=127.0.0.1`; restart via canonical `.logs/server-launcher.sh` (old omp-spawned PID 57706 killed) | `lsof -nP -iTCP:3005 -sTCP:LISTEN` → `bun 86056 TCP 127.0.0.1:3005 (LISTEN)` (wildcard gone); `curl /api/copilotkit/info` → 200; `curl :3011/` → `<title>OpenBot</title>`; `bun test tests/rig-foundation-estate-truth.test.ts` → 15 pass / 0 fail | **PASS** |
| U2 R7 jarvis | No change (already loaded by others between report and run — OBSERVE phase caught it) | `launchctl print gui/501/com.rig.jarvis` → state=running pid=62754, KeepAlive+RunAtLoad=true; `curl :8000/` → 401 (auth-gated = alive) | **RESOLVED-BY-OTHERS, VERIFIED** |
| U3 R2 backup theater | New canonical script `platform/openbot/scripts/rig-pg-restore-drill.sh` (restores newest QNAP dump into scratch db `openbot_restore_drill` on live PG, gates on table-count match + agents/users rows, drops scratch) | First run → exit 4 (29 vs 30: gate counted `drizzle.__drizzle_migrations`) — **gate bug caught by running it**; fixed count to `CREATE TABLE public\.`; rerun → **exit 0**, `tables=29 (dump=29) agents=11 users=1`, scratch dropped | **PASS** |
| U4 systems-thinking | New `~/.jake/JAKE_SYSTEMS_THINKING.md` (loop + 7 imported process rules + Jake E/T/C/S/L/V binding + done tests); wired into read-first substrates of jake-pai SKILL.md in all 4 harnesses | `grep -c JAKE_SYSTEMS_THINKING` → 1 in .claude/.codex/.hermes/.agents mirrors (after fixing a 4× duplicate insertion) | **PASS** |

## Findings the process itself produced (beyond the morning report)

1. **R1's real shape was not "one-line fix"**: the `:3005` holder was a dev server spawned by an
   omp session 9.5h earlier (not launchd), the running OpenBot.app depended on it, and
   `OPENBOT_TOOL_URL` routes agent containers to `host.docker.internal:3005`. Fix went in at
   the root (code default + canonical launcher), with `SERVER_HOST` as the explicit escape
   hatch for the dormant container path.
2. **Backup has TWO silent failure modes**, not one: (a) containers down → `docker exec` fails →
   WARN + exit 1 (known); (b) **missed run during sleep leaves no trace at all** — last night's
   03:00 job produced no log line while launchd still reports last-exit 0 (stale). Missed-run ≠
   healthy. Queued: alerting + missed-run catch-up.
3. **Estate contract exists but isn't enforced live**: `rig-foundation-estate-truth.test.ts`
   pins `host: 127.0.0.1` for api/ui — yet the live listener was wildcard for 9.5h. The test
   parses .env; nothing compares it to `lsof`. Queued: live-enforcement check in the watchdog.
4. **Verifier discipline pays same-day**: U3's first gate failure was the gate's own bug. Run
   the gate before trusting the gate.

## Sealed next queue (contracts, not scope creep)

| # | Unit | Contract / gate |
|---|---|---|
| Q1 | Backup alerting + missed-run catch-up | backup script alerts on failure AND on skipped calendar fire; gate = simulate both, alert observed |
| Q2 | Estate live-enforcement | watchdog (or test) compares lsof binds to the pinned 127.0.0.1 contract; gate = wildcard bind makes it fail red |
| Q3 | R3 control center (operate, not just observe) | UI: per-agent model assignment + health badges + host metrics; process-map first, per the morning report |
| Q4 | R4 channel→agent routing | Telegram chat → named agent (not just model override); four-agent operable-crew pattern |
| Q5 | R5 voice wiring | ELEVENLABS key wired; STT/TTS recipes turned on; Kokoro evaluated |
| Q6 | Reboot recovery drill | reboot (or simulate) → watchdog restores fleet → gate = 5 agent containers + API + UI healthy post-boot |

## Artifacts and hashes

- `platform/openbot/server/src/index.ts` — serve() hostname default (canonical repo, was untracked; now the tracked-shape fix on disk)
- `platform/openbot/.env` — PORT=3005, SERVER_HOST=127.0.0.1
- `platform/openbot/scripts/rig-pg-restore-drill.sh` — repeatable gate, exit 0 proven
- `~/.rig/live/openbot-pg-restore-drill.log` — drill receipts (PASS line 2026-08-29T19:12:49Z)
- `~/.jake/JAKE_SYSTEMS_THINKING.md` — module (5466 bytes)
- jake-pai SKILL.md ×4 mirrors — module in read-first list, exactly one reference each

Machine proof: `proof/jake-systems-thinking-run-20260829.json`

## Addendum (19:16Z): the final gate sweep caught a live oscillation

The fresh re-run of all gates (never trust stale output) failed G6: the QNAP `RIGVault` share
had unmounted mid-mission — its mountpoint silently became a local directory. Root cause in
`~/.rig/logs/qnap-watchdog.log`: **13,496 STALE events total, 2,212 today** — the mount
watchdog's fix loop is the oscillation's driver: every remount of one share from
`100.64.83.55` instantly stales the other (two SMB sessions fighting), so the watchdog
ping-pongs them forever. Classic fixes-that-fail: the fix feeds the failure. Also proven: the
backup script would have "succeeded" into the dead local mountpoint at 03:00, which is the
exact silent-failure class R2 named. Manual watchdog run remounted RIGVault; drill re-run →
exit 0. Q1's contract now includes: single-session SMB mount strategy (or backup target moved
to a stable share), mount-state alerting, and the drill wired to run before any restore is
trusted.

Prior art: `JARVIS-GAP-REPORT-2026-08-29.md` (morning state), `PLAYBOOK-ARCHIFY-GAP-REPORT-2026-08-29.md` (the discipline's source audit).
