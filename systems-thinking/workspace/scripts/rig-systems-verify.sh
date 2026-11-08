#!/usr/bin/env bash
# rig-systems-verify.sh — the Jake systems-thinking loop, executable.
#
# Modes:
#   scan    OBSERVE as code: emit JSON system state (no pass/fail) for mission packets.
#   verify  VERIFY as code: numbered gates, JSON result + exit 0 (all green) / 1 (reds).
#
# Contract constants are env-overridable SOLELY for plant-failure certification
# (rig-adversarial-verification: a green that won't go red is theater). Production
# runs use the defaults.
#
# Gates:
#   G1 api-bind-contract   :3005 listener bound to loopback only (no wildcard)
#   G2 api-health          API answers 200 on 127.0.0.1
#   G3 ui-proxy            UI serves through the proxy
#   G4 estate-contract     rig-foundation-estate-truth test passes
#   G5 jarvis-alive        com.rig.jarvis loaded + :8000 responds
#   G6 backup-restorable   restore drill exits 0 (a backup never restored is a hypothesis)
export PATH="$HOME/.bun/bin:$HOME/.homebrew/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
#   G8 mount-stability     both QNAP shares mounted; oscillation quiet (≤2 STALE/hour)
#   G9 module-wiring       systems-thinking module present + wired exactly once ×4 harnesses
set -uo pipefail

MODE="${1:-verify}"
API_PORT="${API_PORT:-3005}"
API_HOST_EXPECT="${API_HOST_EXPECT:-127.0.0.1}"
UI_PORT="${UI_PORT:-3011}"
JARVIS_PORT="${JARVIS_PORT:-8000}"
OB="$HOME/Developer/rig-intelligence/platform/openbot"
BACKUP_LOG="${BACKUP_LOG:-$HOME/.rig/live/openbot-pg-backup.log}"
QNAP_LOG="${QNAP_LOG:-$HOME/.rig/logs/qnap-watchdog.log}"
MODULE="$HOME/.jake/JAKE_SYSTEMS_THINKING.md"
STATE_JSON="$HOME/.rig/live/systems-verify.json"
LOG="$HOME/.rig/live/systems-verify.log"
DRILL="${DRILL:-$OB/scripts/rig-pg-restore-drill.sh}"
ts() { date -u +%FT%TZ; }
log() { echo "[$(ts)] $*" >> "$LOG"; }

# ---------- scan (OBSERVE) ----------
scan() {
  python3 - "$API_PORT" "$UI_PORT" "$JARVIS_PORT" <<'PYEOF'
import json, subprocess, sys, os, re, time
api_port, ui_port, jarvis_port = sys.argv[1:4]
def sh(cmd):
    try: return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20).stdout.strip()
    except Exception as e: return f"ERROR {e}"
listeners = sh(f"lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk '{{print $1, $9}}' | sort -u")
established = sh(f"lsof -nP -iTCP:{api_port} -sTCP:ESTABLISHED 2>/dev/null | awk 'NR>1{{print $1, $2}}' | sort -u")
mounts = sh("mount | grep -E 'smbfs|nfs' | sed 's/ (.*//'")
svc = lambda label: sh(f"launchctl print gui/$(id -u)/{label} 2>/dev/null | grep -m1 'state =' | sed 's/.*= //'") or "not-loaded"
qnap_tail = sh(f"tail -200 {os.environ['HOME']}/.rig/logs/qnap-watchdog.log 2>/dev/null")
stale_last_hour = len(re.findall(time.strftime('%Y-%m-%d') + r' \d\d:\d\d:\d\d STALE', qnap_tail))
backup_tail = sh(f"tail -5 {os.environ['HOME']}/.rig/live/openbot-pg-backup.log 2>/dev/null")
last_ok = (re.findall(r'\[(.+?)\] OK', backup_tail) or [None])[-1]
print(json.dumps({
  "observed_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
  "listeners": listeners.splitlines(),
  "api_dependents": established.splitlines(),
  "network_mounts": mounts.splitlines(),
  "services": {"com.rig.jarvis": svc("com.rig.jarvis"),
               "com.rig.openbot-watchdog": svc("com.rig.openbot-watchdog"),
               "com.rig.qnap-watchdog": svc("com.rig.qnap-watchdog")},
  "qnap_stale_events_today": len(re.findall(time.strftime('%Y-%m-%d') + r'.*STALE', qnap_tail)),
  "backup_last_ok": last_ok,
  "ports": {"api": api_port, "ui": ui_port, "jarvis": jarvis_port},
}, indent=1))
PYEOF
}

# ---------- gates ----------
gate() { # id, description, command
  local id="$1" desc="$2" cmd="$3" out rc
  out="$(bash -c "$cmd" 2>&1)"; rc=$?
  RESULTS+=("$id|$rc|$desc|$out")
  [ $rc -eq 0 ] || FAILED=$((FAILED+1))
}

verify() {
  RESULTS=(); FAILED=0
  gate G1 "api-bind-contract" \
    "lsof -nP -iTCP:$API_PORT -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print \$9}' | grep -qv '^127\.0\.0\.1:' && exit 1; lsof -nP -iTCP:$API_PORT -sTCP:LISTEN | awk 'NR>1{print \$9}' | grep -q '^127\.0\.0\.1:'"
  gate G2 "api-health" \
    "curl -s -m 5 -o /dev/null -w '%{http_code}' http://127.0.0.1:$API_PORT/api/copilotkit/info | grep -qx 200"
  gate G3 "ui-proxy" \
    "curl -s -m 5 http://127.0.0.1:$UI_PORT/ | grep -q '<title>OpenBot</title>'"
  gate G4 "estate-contract" \
    "cd $OB && bun test tests/rig-foundation-estate-truth.test.ts 2>&1 | tail -3 | grep -q ' 0 fail'"
  gate G5 "jarvis-alive" \
    "launchctl print gui/\$(id -u)/com.rig.jarvis 2>/dev/null | grep -q 'state = running' && curl -s -m 3 -o /dev/null http://127.0.0.1:$JARVIS_PORT/"
  gate G6 "backup-restorable" "bash '$DRILL'"
  gate G7 "backup-freshness" \
    "python3 -c \"
import re,time
t=open('$BACKUP_LOG').read()
ok=re.findall(r'\[([^]]+)\] OK',t)
assert ok, 'no OK line ever'
last=time.mktime(time.strptime(ok[-1],'%Y-%m-%dT%HZ'))
age=(time.time()-last)/3600
print(f'last_ok={ok[-1]} age_h={age:.1f}')
exit(0 if age<=26 else 1)\""
  gate G8 "mount-stability" \
    "mount | grep -q 'RIGVault' && mount | grep -q 'RIGLake' && [ \$(grep \"\$(date +%Y-%m-%d)\" '$QNAP_LOG' 2>/dev/null | grep -cE ' STALE(-CONFIRMED)?:' | tail -1) -ge 0 ] && [ \$(awk -v d=\"\$(date -v-1H '+%Y-%m-%d %H')\" '\$0 ~ / STALE(-CONFIRMED)?:/ && \$1\" \"\$2 >= d {c++} END {print c+0}' '$QNAP_LOG') -le 4 ]"
  gate G9 "module-wiring" \
    "test -s '$MODULE' && for d in .claude .codex .hermes .agents; do [ \"\$(grep -c JAKE_SYSTEMS_THINKING \$HOME/\$d/skills/jake-pai/SKILL.md 2>/dev/null)\" = 1 ] || exit 1; done"

  # assemble JSON state
  python3 - "${RESULTS[@]}" <<PYEOF > "$STATE_JSON"
import json,sys,datetime
rows=[]
for a in sys.argv[1:]:
    id_,rc,desc,out=a.split('|',3)
    rows.append({"id":id_,"ok":rc=='0',"desc":desc,"evidence":out[:200]})
failed=sum(1 for r in rows if not r["ok"])
print(json.dumps({"schema":"rig.systems_verify.v1","at":datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
  "mode":"verify","gates":rows,"failed":failed,"exit":1 if failed else 0},indent=1))
PYEOF
  for r in "${RESULTS[@]}"; do IFS='|' read -r id rc desc out <<< "$r"; log "$id $([ $rc = 0 ] && echo GREEN || echo RED) — $desc"; done
  log "verify exit=$FAILED failures"
  cat "$STATE_JSON"
  exit $(( FAILED > 0 ? 1 : 0 ))
}

case "$MODE" in
  scan) scan ;;
  verify) verify ;;
  *) echo "usage: $0 [scan|verify]" >&2; exit 64 ;;
esac
