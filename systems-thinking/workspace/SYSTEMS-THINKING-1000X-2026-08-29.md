# Systems-Thinking 1000x Round — Evidence Pack (2026-08-29)

Target: the Jake systems-thinking capability built this morning. Mandate: 1000x better.
Method: three multiplicative 10s — static→executable, manual→always-on, symptom→loop —
with every gate plant-failure certified (a green that won't go red is theater).

## The three axes

| Axis | Before (v1) | After (v2) |
|---|---|---|
| **10× executable** | 5.5KB prose module Jake may skip | `rig-systems-verify.sh` — 9 numbered gates as commands with exit codes + `scan` mode emitting machine JSON; module v2 binds loop phases to commands |
| **10× always-on** | gates run once, manually, in a chat transcript | launchd `com.rig.systems-verify` every 900s writes standing state `~/.rig/live/systems-verify.json`; drift turns red unattended |
| **10× loop-level** | oscillation queued as prose | watchdog v2 kills the unmount limit cycle (confirm-before-unmount, bounded checks, lock, settle); backup resurrected by finding the REAL failure cause |

## What the round uncovered while certifying (three chained misdiagnoses corrected)

1. **The fleet was never down.** Every `docker ps` (this session's, the watchdog's, the JARVIS
   report's) queried Docker Desktop (empty context) while the entire OpenBot stack ran **Up 29h
   in the Colima VM**. The watchdog's "ssh owns ports" clash-detection was reading Colima's own
   port mux as foreign LAN ssh. Fleet: healthy. Diagnosis everywhere: wrong.
2. **The nightly backup died on a context mismatch, not "PG may be down."** Patched
   `rig-pg-backup-qnap.sh` to `docker --context colima exec` (`DOCKER_CMD` escape hatch);
   ran it: fresh 49K dump, OK logged, exit 0 — first successful backup in 43h, G7 green.
3. **The API crash was real drift, caught by the suite within minutes.** `eventsource@3.0.7`
   ESM-required-via-CJS crashes the server (Bun TypeError); the openbot watchdog respawned it
   loopback-bound with the morning's patch. Root fix (pin eventsource@2 / bump MCP SDK) queued.
4. **The mount storm's root is physical, the amplification was systemic.** QNAP LAN IP absent
   from this segment (ARP incomplete, 100% loss) → all SMB rides Tailscale → sessions genuinely
   die under load. v1's watchdog multiplied each death by force-unmounting healthy siblings
   (13,496 STALE events). v2: bounded 3s checks ×2, two-tick confirm-before-unmount, lockfile,
   settle-observe — the log now shows `SETTLE-CHECK ... NOT unmounting` where v1 destroyed.
   LAN path restoration queued (physical infra).

## Certification (A7)

- **Planted run** (`API_PORT=3999 JARVIS_PORT=9999 PGURL=bogus QNAP_LOG=forged-stale-log`):
  exit 1, gates `G1 R · G2 R · G5 R · G6 R · G8 R` while untouched `G3 G · G4 G · G7 G · G9 G` —
  reds are causal.
- **Restored run** (defaults): exit 1 with **8/9 GREEN** — G8 the sole red, carrying v1's
  trailing-hour STALE events; window clears ~15:57 local and the launchd suite flips it green
  unattended (that transition itself is the always-on proof).
- First launchd tick exposed a suite bug (launchd's minimal PATH broke `bun`/`psql` gates) —
  fixed with the watchdog's PATH-export pattern; environment, not estate.

## Artifacts

| What | Where |
|---|---|
| Gate suite + scan (v2 runtime) | `~/.rig/bin/rig-systems-verify.sh` (state: `~/.rig/live/systems-verify.json`) |
| Always-on wiring | `~/Library/LaunchAgents/com.rig.systems-verify.plist` (900s, RunAtLoad) |
| Watchdog v2 (+v1 backup) | `~/.rig/bin/qnap-mount-watchdog.sh` (`.v1-backup-20260829`) |
| Backup context fix | `platform/openbot/scripts/rig-pg-backup-qnap.sh` (canonical repo) |
| Drill retry (mount-resilient) | `platform/openbot/scripts/rig-pg-restore-drill.sh` (canonical repo) |
| Module v2 | `~/.jake/JAKE_SYSTEMS_THINKING.md` (5865 bytes; mirrors unchanged — path stable) |
| Workspace provenance copies | `Systems-Thinking/scripts/` (suite, watchdog v2, plist, drill, backup) |
| Machine proof | `proof/systems-thinking-1000x-20260829.json` |

## Queue (named units with contracts)

- **Q1′** LAN path to QNAP restored (physical: check switch/AP segment for 192.168.68.84) —
  until then Tailscale flapping is the floor; v2 damping holds the damage.
- **Q7** eventsource/MCP dependency fix (server crash path) — pin or upgrade, gate = 24h no respawn.
- **Q1..Q6 from the morning pack** remain: alerting, estate live-enforcement beyond G1, control
  center, channel→agent, voice, reboot drill.
