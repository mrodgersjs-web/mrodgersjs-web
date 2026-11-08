#!/usr/bin/env python3
"""
seal.py — hash a set of artifact files into a ProofPacket JSON.

A ProofPacket is the canonical, tamper-evident record that a set of files
existed in an exact state at an exact moment. Each artifact gets a SHA-256.
The packet itself gets a combined integrity hash computed over a canonical
(sorted-key, separator-fixed) JSON payload, so two people who seal the same
files the same way get the same packet hash. Optionally, the packet hash is
signed with HMAC-SHA256 using a key from the environment, so a third party
can prove WHO sealed it, not just that it is internally consistent.

Standard library only. Runs on python3, no pip install.

Usage:
    python3 seal.py --out proofpacket.json FILE [FILE ...]
    python3 seal.py --out proofpacket.json --timestamp 2026-06-16T00:00:00Z \
        --name "phase-3" --verifier "mike" example/build.txt example/notes.md
    PROOFPACKET_KEY=secret python3 seal.py --out proofpacket.json --sign FILE

Options:
    --out PATH          Where to write the packet JSON (default: proofpacket.json)
    --timestamp TS      ISO-8601 UTC timestamp to stamp into the packet.
                        Pass this explicitly for reproducible (byte-identical)
                        packets; omit to use the current UTC time.
    --name NAME         Human label for what is being sealed.
    --verifier WHO      Who sealed it (agent or human). Default: "anonymous".
    --evidence TEXT     Free-text note on why this is done / what it proves.
    --sign              Sign the packet hash with HMAC-SHA256 using the key in
                        the PROOFPACKET_KEY environment variable.
    --base DIR          Base directory; artifact paths are stored relative to it.
"""
from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = "1.0.0"
SIGNATURE_ALGO = "hmac-sha256"
ENV_KEY = "PROOFPACKET_KEY"


def sha256_file(path: Path) -> tuple[str, int]:
    """Return (hex digest, size in bytes) for a file, streamed in chunks."""
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def artifact_record(path: Path, base: Path) -> dict:
    """Build one artifact entry. Missing files are recorded, not silently dropped."""
    try:
        rel = str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        rel = str(path)
    if not path.exists():
        return {"path": rel, "sha256": "", "size_bytes": 0, "exists": False}
    digest, size = sha256_file(path)
    return {"path": rel, "sha256": digest, "size_bytes": size, "exists": True}


def canonical_payload(packet: dict) -> bytes:
    """
    Canonical bytes used for the integrity hash. The hash and signature fields
    are excluded so the hash describes the *content* of the packet, not itself.
    sort_keys + tight separators make the encoding deterministic.
    """
    data = {k: v for k, v in packet.items()
            if k not in ("packet_sha256", "signature", "signature_algo")}
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def compute_packet_hash(packet: dict) -> str:
    return hashlib.sha256(canonical_payload(packet)).hexdigest()


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Seal artifacts into a ProofPacket.")
    p.add_argument("artifacts", nargs="+", help="Files to seal.")
    p.add_argument("--out", default="proofpacket.json", help="Output packet path.")
    p.add_argument("--timestamp", default=None,
                   help="ISO-8601 UTC timestamp (pass for reproducible packets).")
    p.add_argument("--name", default="unnamed", help="Label for what is sealed.")
    p.add_argument("--verifier", default="anonymous", help="Who sealed it.")
    p.add_argument("--evidence", default=None, help="Why this is done.")
    p.add_argument("--sign", action="store_true",
                   help=f"Sign with HMAC-SHA256 using ${ENV_KEY}.")
    p.add_argument("--base", default=".", help="Base dir for relative paths.")
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    base = Path(args.base)

    sealed_at = args.timestamp or datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )

    artifacts = [artifact_record(Path(a), base) for a in args.artifacts]
    missing = [a["path"] for a in artifacts if not a["exists"]]
    if missing:
        print(f"[seal] WARNING: {len(missing)} artifact(s) missing on disk: "
              f"{', '.join(missing)}", file=sys.stderr)

    packet: dict = {
        "schema_version": SCHEMA_VERSION,
        "name": args.name,
        "sealed_at": sealed_at,
        "status": "verified",
        "verifier": args.verifier,
        "evidence": args.evidence,
        "artifacts": artifacts,
        "packet_sha256": "",
        "signature": "",
        "signature_algo": SIGNATURE_ALGO,
    }

    packet["packet_sha256"] = compute_packet_hash(packet)

    if args.sign:
        key = os.environ.get(ENV_KEY, "").encode("utf-8")
        if not key:
            print(f"[seal] ERROR: --sign requested but ${ENV_KEY} is empty.",
                  file=sys.stderr)
            return 2
        packet["signature"] = hmac.new(
            key, packet["packet_sha256"].encode("utf-8"), hashlib.sha256
        ).hexdigest()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2) + "\n")

    signed = " (signed)" if packet["signature"] else ""
    print(f"[seal] wrote {out}{signed}")
    print(f"[seal]   artifacts : {len(artifacts)}")
    print(f"[seal]   sealed_at : {sealed_at}")
    print(f"[seal]   packet    : sha256:{packet['packet_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
