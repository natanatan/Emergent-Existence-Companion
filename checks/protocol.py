#!/usr/bin/env python3
"""Check that every test declared its diagnostics before its result.

For each tests/<ID>/ (except _template):
  - <ID> is a claim or hypothesis in the pinned book snapshot
  - PROTOCOL.md exists
  - if RESULT.md exists, PROTOCOL.md was first committed before RESULT.md
  - PROTOCOL.md has not changed since RESULT.md was first committed
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def first_commit_time(path):
    out = subprocess.run(["git", "-C", HERE, "log", "--diff-filter=A", "--format=%ct", "--", path],
                         capture_output=True, text=True).stdout.split()
    return int(out[-1]) if out else None


def last_commit_time(path):
    out = subprocess.run(["git", "-C", HERE, "log", "-1", "--format=%ct", "--", path],
                         capture_output=True, text=True).stdout.split()
    return int(out[0]) if out else None


def main():
    ids = set()
    for name in ("claims.json", "hypotheses.json"):
        with open(os.path.join(HERE, "book", name), encoding="utf-8") as f:
            ids |= {x["id"] for x in json.load(f)}
    errors = []
    tests = os.path.join(HERE, "tests")
    for d in sorted(os.listdir(tests)):
        full = os.path.join(tests, d)
        if d.startswith("_") or not os.path.isdir(full):
            continue
        if d not in ids:
            errors.append(f"tests/{d}: not a claim or hypothesis ID in book/")
        proto, result = os.path.join(full, "PROTOCOL.md"), os.path.join(full, "RESULT.md")
        if not os.path.exists(proto):
            errors.append(f"tests/{d}: no PROTOCOL.md")
            continue
        if os.path.exists(result):
            p, r = first_commit_time(proto), first_commit_time(result)
            if p is None or r is None:
                errors.append(f"tests/{d}: commit PROTOCOL.md, then run, then commit RESULT.md")
            elif p >= r:
                errors.append(f"tests/{d}: RESULT.md was committed no later than PROTOCOL.md")
            elif (last_commit_time(proto) or 0) > r:
                errors.append(f"tests/{d}: PROTOCOL.md changed after the result; write a new protocol for a new run")
    for e in errors:
        print(e)
    print(f"{len(errors)} problem(s)" if errors else "protocols are in order")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
