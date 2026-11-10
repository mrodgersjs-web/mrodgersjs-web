#!/usr/bin/env python3
"""
verify.py — verify a ProofPacket against the artifacts on disk.

Three independent checks, each reported separately so you can see exactly
what held and what broke:

  1. INTEGRITY  — recompute the packet's combined hash from its own content
                  and compare to the stored packet_sha256. Catches any edit
                  to the packet body (a swapped artifact hash, a changed
                  timestamp, an added file).
  2. ARTIFACTS  — re-hash every artifact file on disk and compare to the
                  hash recorded in the packet. Catches tampering with the
                  actual files after they were sealed.
  3. SIGNATURE  — (only if --key / $PROOFPACKET_KEY is supplied) recompute the
                  HMAC-SHA256 over the packet hash and constant-time compare
                  to the stored signature. Proves who sealed it.

Exit code 0 = all requested checks passed. Non-zero = at least one failed.
Standard library only. Runs on python3, no pip install.

Usage:
    python3 verify.py proofpacket.json
    python3 verify.py proofpacket.json --base example
    PROOFPACKET_KEY=secret python3 verify.py proofpacket.json --check-signature
    python3 verify.py proofpacket.json --key secret --check-signature
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path

ENV_KEY = "PROOFPACKET_KEY"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_payload(packet: dict) -> bytes:
    data = {k: v for k, v in packet.items()
            if k not in ("packet_sha256", "signature", "signature_algo")}
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_packet_hash(packet: dict) -> str:
    return hashlib.sha256(canonical_payload(packet)).hexdigest()


def check_integrity(packet: dict) -> tuple[bool, str]:
    stored = packet.get("packet_sha256", "")
    if not stored:
        return False, "no packet_sha256 stored in packet"
    recomputed = compute_packet_hash(packet)
    if recomputed == stored:
        return True, f"packet hash matches (sha256:{stored[:16]}...)"
    return False, (f"packet hash MISMATCH\n         stored:     {stored}\n"
                   f"         recomputed: {recomputed}")


def check_artifacts(packet: dict, base: Path) -> tuple[bool, list[str]]:
    lines: list[str] = []
    ok = True
    artifacts = packet.get("artifacts", [])
    if not artifacts:
        return True, ["  (no artifacts in packet)"]
    for art in artifacts:
        rel = art.get("path", "?")
        path = base / rel
        if not path.exists():
            ok = False
            lines.append(f"  MISSING  {rel}")
            continue
        actual = sha256_file(path)
        expected = art.get("sha256", "")
        if actual == expected:
            lines.append(f"  OK       {rel}")
        else:
            ok = False
            lines.append(f"  CHANGED  {rel}")
            lines.append(f"             expected sha256:{expected}")
            lines.append(f"             actual   sha256:{actual}")
    return ok, lines


def check_signature(packet: dict, key: bytes) -> tuple[bool, str]:
    sig = packet.get("signature", "")
    pkt_hash = packet.get("packet_sha256", "")
    if not sig:
        return False, "packet is not signed (no signature field)"
    if not pkt_hash:
        return False, "no packet_sha256 to verify the signature against"
    expected = hmac.new(key, pkt_hash.encode("utf-8"), hashlib.sha256).hexdigest()
    if hmac.compare_digest(expected, sig):
        return True, "signature valid (HMAC-SHA256)"
    return False, "signature INVALID for the supplied key"


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Verify a ProofPacket.")
    p.add_argument("packet", help="Path to the proofpacket.json file.")
    p.add_argument("--base", default=None,
                   help="Base dir to resolve artifact paths "
                        "(default: the packet's own directory).")
    p.add_argument("--check-signature", action="store_true",
                   help="Also verify the HMAC signature.")
    p.add_argument("--key", default=None,
                   help=f"Signing key (else ${ENV_KEY}).")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    packet_path = Path(args.packet)
    if not packet_path.exists():
        print(f"[verify] ERROR: packet not found: {packet_path}", file=sys.stderr)
        return 2

    packet = json.loads(packet_path.read_text())
    base = Path(args.base) if args.base else packet_path.resolve().parent

    print(f"[verify] packet : {packet_path}")
    print(f"[verify] name   : {packet.get('name', '?')}")
    print(f"[verify] sealed : {packet.get('sealed_at', '?')} "
          f"by {packet.get('verifier', '?')}")
    print(f"[verify] base   : {base}")
    print()

    all_ok = True

    ok, msg = check_integrity(packet)
    all_ok &= ok
    print(f"[1] INTEGRITY  {'PASS' if ok else 'FAIL'}")
    print(f"    {msg}")
    print()

    ok, lines = check_artifacts(packet, base)
    all_ok &= ok
    print(f"[2] ARTIFACTS  {'PASS' if ok else 'FAIL'}")
    for line in lines:
        print(line)
    print()

    if args.check_signature:
        key = (args.key or os.environ.get(ENV_KEY, "")).encode("utf-8")
        if not key:
            print(f"[3] SIGNATURE  FAIL")
            print(f"    --check-signature requested but no key "
                  f"(--key or ${ENV_KEY}) supplied")
            all_ok = False
        else:
            ok, msg = check_signature(packet, key)
            all_ok &= ok
            print(f"[3] SIGNATURE  {'PASS' if ok else 'FAIL'}")
            print(f"    {msg}")
        print()

    verdict = "VERIFIED" if all_ok else "FAILED"
    print(f"[verify] === {verdict} ===")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
