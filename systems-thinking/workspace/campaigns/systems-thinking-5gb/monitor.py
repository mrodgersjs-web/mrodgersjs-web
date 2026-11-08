#!/usr/bin/env python3
import json
import subprocess
import sys
import time

TARGET = 5_000_000_000
REMOTE = """python3 ~/.rig/omniscout-campaigns/systems-thinking-5gb-20260829/campaign.py status --root ~/.rig/omniscout-campaigns/systems-thinking-5gb-20260829 --lattice ~/.rig/omniscout-campaigns/systems-thinking-5gb-20260829/lattice.json"""
last = -1
last_change = time.monotonic()
while True:
    result = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", "rig36gb", REMOTE], capture_output=True, text=True, timeout=30)
    if result.returncode:
        print(f"STATUS_ERROR exit={result.returncode} {result.stderr[-200:]}", flush=True)
    else:
        value = json.loads(result.stdout)
        size = int(value["artifact_bytes"])
        print(f"{value['updated_at']} bytes={size} progress={value['progress']:.6f} done={value['states'].get('done',0)} failed={value['states'].get('failed',0)} queued={value['states'].get('queued',0)}", flush=True)
        if size >= TARGET:
            raise SystemExit(0)
        if size > last:
            last = size
            last_change = time.monotonic()
        elif time.monotonic() - last_change > 1800:
            print("STALL: no byte progress for 30 minutes", flush=True)
            raise SystemExit(2)
    time.sleep(120)
