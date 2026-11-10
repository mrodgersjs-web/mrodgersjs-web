# JARVIS Mission Control Card — Gap Report (2026-08-29)

Method: card's Phase-0 discovery executed for real on this host + 5 parallel read-only audits (Hermes crew, OpenBot UI, services/access, voice/connectors, verification depth). No mutations.

## 1. What the card does as-supplied

**It cannot clone or install anything.** `GITHUB_REPO_URL` is empty, no project archive, no `Javis dashboard template.html`. By its own Phase-1 termination rule it ends `BLOCKED_MISSING_SOURCE_ASSET` — by design ("stop rather than manufacture a counterfeit"). The only part that executes is Phase 0 discovery, which this report already ran for real.

Two additional mismatches:
- The card assumes Ubuntu/VPS/systemd/non-root deployment user. This host is macOS/launchd. Phases 8–9 would need adaptation, not obedience.
- The estate already contains a **real, cloneable JARVIS**: `~/OpenJarvis` (Stanford open-source, Apache-2.0), with `com.rig.jarvis.plist` (KeepAlive, RunAtLoad, `jarvis serve`) — **but the plist is not loaded into launchctl**. Dead service definition; last run shut down cleanly on 127.0.0.1:8000. The missing-source problem is solved by OpenJarvis on disk, not by the card.

## 2. Capability gap matrix

| # | Card capability | Verdict | Evidence |
|---|---|---|---|
| 1 | 4-agent crew (JARVIS/Dev/Research/Asst) | COVERED-DIFFERENTLY | 22 depts w/ named owners (`~/.rig/departments/_REGISTRY.py`), ~120 agent JSONs (`~/.hermes/agents/`), Jake PAI conductor (`~/.hermes/jake/`) |
| 2 | Telegram: one gateway, channel→agent | PARTIAL | One bot, per-chat **model** overrides (`config.yaml` `channel_overrides`); **no channel→agent routing**; `profiles/jarvis/telegram/bot.py` is file-based, no api.telegram.org wiring |
| 3 | Per-agent model assignment + validated change | PARTIAL | Global default + per-channel + MoA per class (`config.yaml`); agent JSONs carry `node_target`, no model key; no UI flow, no validate/rollback |
| 4 | Agent status + live health | PARTIAL | Roster + profiles (`agents/routes.ts`, `agent-card.tsx`); no health/heartbeat badge |
| 5 | Communications view | COVERED-DIFFERENTLY | Per-channel transcripts + authed WS events (`channels/routes.ts:653`, `chat-transcript.tsx`); no single cross-channel wall |
| 6 | Control center (switch models in UI) | MISSING | Agent form has name/role/endpoint/auth only (`agent-profile.tsx`); model lives in per-bot YAML/env |
| 7 | Real host metrics (CPU/mem/disk/uptime) | MISSING | No endpoint, no UI, anywhere in server routes |
| 8 | Auth on all routes | COVERED | Everything behind `requireUser` (`app.ts:239-243`); admin verbs requireAdmin |
| 9 | Voice in/out | MISSING-FRAGMENTED | Orb = mic amplitude only (`ai-core.tsx`); `ELEVENLABS_API_KEY` unwired (`.env:108`); full STT/TTS recipes exist as unwired codex skills; Kokoro absent |
| 10 | Email/calendar read-only connectors | COVERED-DIFFERENTLY | Orchard read+write w/ confirm-gate prose; Composio CLI+key installed, unused; **no enforced read-only scopes anywhere** |
| 11 | Persistent services | COVERED | launchd RunAtLoad+KeepAlive: openbot-ui, openbot-watchdog (300s), hermes gateway, `com.mission.*` family |
| 12 | Reboot recovery **tested** | MISSING | Watchdog implies recovery; no drill ever exercised |
| 13 | Backups + restore | PARTIAL-FAILING | Nightly pg_dump 7d rotation; **1 dump on disk**; failure exits 1 with no alert; **no restore test exists** |
| 14 | Loopback-only binding | PARTIAL — **LIVE HOLE** | `lsof`: `bun *:3005` **wildcard-bound** (API); everything else 127.0.0.1; dev-fallback auth on an all-interfaces listener |
| 15 | Private remote access | PARTIAL | Tailscale installed; only Phronema served on tailnet (:10000); OpenBot unreachable from other devices |
| 16 | Security tests (secrets/auth/injection) | COVERED | 43-file bun suite: secret-leak, auth-rejection, loopback-compose, Gate-D, idempotency; `rig-verify-local.sh` independent |
| 17 | Design-regression baseline | MISSING | No screenshot-baseline mechanism anywhere |
| 18 | Independent verifier | MIXED | `rig-verify-local.sh` independent; systems-studio **seals its own phases** (self-verified) |

## 3. Are we going deep enough?

**Deeper than the card** on governance and proof: sealed foundation builds, ProofPackets (SHA-256+HMAC), attention cap (A_ops), lattice routing, per-step process maps with harnesses, 43-test contract suite. The card's security bar (secrets, auth, invalid-model rejection) is met or exceeded.

**Shallow exactly where the card is strong — operability and recovery.** Ranked by risk:

1. **`:3005` wildcard bind** (R1) — contradicts our own loopback doctrine; one-line fix.
2. **Backup theater** (R2) — a backup never restored is a hypothesis. 1 dump, silent failure, no restore drill.
3. **Read-only cockpit = half a mission control** (R3) — we can see the lattice; we cannot operate it (no model assignment, no health, no host metrics). The card's "control center" is the missing layer.
4. **Channel→model, not channel→agent** (R4) — Telegram routing can't address a specific agent; the four-agent operable-crew pattern is architecturally absent.
5. **Voice fragmented across three disconnected layers** (R5) — keys, recipes, UI all exist, none wired.
6. **Verification depth gaps** (R6) — no design baseline before data-wiring, no reboot drill, studio self-seals.
7. **Dead `com.rig.jarvis` plist** (R7) — load it or delete it; a defined-but-unloaded service is drift.

**Process rules worth importing from the card:** separate verifier for every build (we self-seal the studio); design baseline screenshot before wiring data; restore-verified backups; enforced (not prose) read-only connector scopes; numbered functional test matrix per install.

**Meta-finding (build-cards pipeline):** this card shipped without a source URL and nearly induced a counterfeit build. Cards must REQUIRE `GITHUB_REPO_URL` or an explicit `RECONSTRUCTION-ONLY` marker at intake.

## 4. Recommended next slice (no scope taken here)

Fix R1 (bind `:3005` to 127.0.0.1) + load-or-delete `com.rig.jarvis` + one restore drill — three small, high-leverage moves that close the only red-line findings. Control-center UI work (R3) and channel→agent routing (R4) are the real builds; do them as process maps, not ad hoc.
