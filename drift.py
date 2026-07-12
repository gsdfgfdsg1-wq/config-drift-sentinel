#!/usr/bin/env python3
"""Compare environment configuration without revealing secret values."""
import argparse
import hashlib
import json
from pathlib import Path


def fingerprint(value):
    return hashlib.sha256(str(value).encode()).hexdigest()[:12]


def compare(left, right, allowed=(), sensitive=()):
    findings = []
    for key in sorted(set(left) | set(right)):
        if key in allowed:
            continue
        if key not in left or key not in right:
            findings.append({"key": key, "kind": "missing", "left": key in left, "right": key in right})
        elif left[key] != right[key]:
            entry = {"key": key, "kind": "different"}
            if key in sensitive:
                entry.update({"left_fingerprint": fingerprint(left[key]), "right_fingerprint": fingerprint(right[key])})
            else:
                entry.update({"left": left[key], "right": right[key]})
            findings.append(entry)
    return {"drift": findings, "healthy": not findings, "score": max(0, 100 - 10 * len(findings))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left"); parser.add_argument("right")
    parser.add_argument("--allow", action="append", default=[]); parser.add_argument("--sensitive", action="append", default=[])
    args = parser.parse_args()
    report = compare(json.loads(Path(args.left).read_text()), json.loads(Path(args.right).read_text()), args.allow, args.sensitive)
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["healthy"] else 1)


if __name__ == "__main__":
    main()
