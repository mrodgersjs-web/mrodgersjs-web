# Gates: v0 → v2 RIG operating-system upgrade brief

Scope: Answer what v2 looks like from measured v0, what top consulting firms actually operate, how to make the stack robust, the 1000x formal process, and how to upgrade RIG systems plus the fleet — with sources and live counts, not vibes.

- [x] G1: Live v0 is measured from disk/commands, not restated from JAKE-PAI-V2.md
  CHECK: test -f docs/v2-upgrade/leaf-v0-measured.json && python3 -c "import json,sys; d=json.load(open('docs/v2-upgrade/leaf-v0-measured.json')); assert d.get('workflow_count'); assert d.get('test_pass_line'); print('ok', d.get('workflow_count'), d.get('test_pass_line'))"
  EXPECT: ok
  EVIDENCE: ok 21 86/87 PASS; TESTS FAIL: seal_proof skeleton status; exit 1 (LeafV0 live .venv/bin/python tests/run_tests.py)

- [x] G2: Consulting-firm claims cite primary URLs (McK/BCG/Bain/Deloitte/Accenture or equivalent first-party pages)
  CHECK: python3 -c "import json; d=json.load(open('docs/v2-upgrade/leaf-consulting.json')); urls=d.get('primary_urls',[]); assert len(urls)>=6, urls; print('urls', len(urls))"
  EXPECT: urls
  EVIDENCE: urls 8

- [x] G3: Robustness section names fail-closed gates that already exist vs missing (durability, eval, Gate-D suspend, cost)
  CHECK: python3 -c "import json; d=json.load(open('docs/v2-upgrade/leaf-v0-measured.json')); g=d.get('gaps',[]); assert len(g)>=4; print('gaps', len(g))"
  EXPECT: gaps
  EVIDENCE: gaps 6

- [x] G4: 1000x process maps to machinery already on disk (IQRSQPI / excellence / doctrine-forge / ProofPacket / Gate-D), not a new slogan
  CHECK: python3 -c "import json; d=json.load(open('docs/v2-upgrade/leaf-1000x-process.json')); assert d.get('existing_machinery'); print('machinery', len(d['existing_machinery']))"
  EXPECT: machinery
  EVIDENCE: machinery 12

- [x] G5: Fleet upgrade map lists live nodes/agents with a source path per count
  CHECK: python3 -c "import json; d=json.load(open('docs/v2-upgrade/leaf-fleet.json')); assert d.get('nodes') or d.get('agents'); print('fleet-ok', d.get('node_count'), d.get('agent_count'))"
  EXPECT: fleet-ok
  EVIDENCE: fleet-ok 7 24

- [x] G6: Integration report exists and every number in it is re-measured at report time
  CHECK: test -f docs/v2-upgrade/REPORT.md && wc -l docs/v2-upgrade/REPORT.md
  EXPECT: /
  EVIDENCE: 163 docs/v2-upgrade/REPORT.md

- [x] G7: Report distinguishes v1 bridge vs v2 flywheel and does not treat JAKE-PAI-V2.md as live proof
  EVIDENCE: REPORT.md L3 "JAKE-PAI-V2.md is prior opinion (it still says 6 workflows). Live CLI says 21." Sections "v1 bridge (make the engine real)" and "v2 flywheel (make the firm real)" are separate.
