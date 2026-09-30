#!/usr/bin/env python3
"""Check that every result was produced under a frozen specification.

For each modules/<NN-name>/ (folders starting with _ are skipped):
  - SPEC.md exists, and every EE-C / EE-H ID it cites is in book/
  - if RESULT.md exists:
      - it names its spec tag, which must be <NN-name>/spec-vN and exist
      - SPEC.md exists at that tag
      - the tagged commit is an ancestor of, and earlier than, the commit
        that first added RESULT.md (the spec was frozen before any result)
      - its verdict is Supports, Fails or Inconclusive

Tags are immutable records of each spec version, so earlier versions and
their results stay in the history when a spec is revised.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID_RE = re.compile(r"EE-[CH]-\d{4}")
NAME_RE = re.compile(r"^\d{2}-[a-z0-9-]+$")
VERDICTS = {"Supports", "Fails", "Inconclusive"}


def git(*args):
    r = subprocess.run(["git", "-C", HERE, *args], capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def main():
    ids = set()
    for name in ("claims.json", "hypotheses.json"):
        with open(os.path.join(HERE, "book", name), encoding="utf-8") as f:
            ids |= {x["id"] for x in json.load(f)}
    root = os.path.join(HERE, "modules")
    errors, count = [], 0
    for d in sorted(os.listdir(root)):
        full = os.path.join(root, d)
        if d.startswith("_") or not os.path.isdir(full):
            continue
        count += 1
        where = f"modules/{d}"
        if not NAME_RE.match(d):
            errors.append(f"{where}: folder name should be NN-short-name")
        spec = os.path.join(full, "SPEC.md")
        if not os.path.exists(spec):
            errors.append(f"{where}: no SPEC.md")
            continue
        for i in sorted(set(ID_RE.findall(open(spec, encoding="utf-8").read())) - ids):
            errors.append(f"{where}: SPEC.md cites {i}, which is not in book/")
        result = os.path.join(full, "RESULT.md")
        if not os.path.exists(result):
            continue
        text = open(result, encoding="utf-8").read()
        m = re.search(r"\*\*Spec tag:\*\*\s*`([^`]+)`", text)
        if not m or not m.group(1).startswith(f"{d}/spec-v"):
            errors.append(f"{where}: RESULT.md must name its spec tag, {d}/spec-vN")
            continue
        tag = m.group(1)
        rc, tag_commit = git("rev-list", "-n", "1", tag)
        if rc != 0:
            errors.append(f"{where}: spec tag {tag} does not exist")
            continue
        if git("cat-file", "-e", f"{tag}:modules/{d}/SPEC.md")[0] != 0:
            errors.append(f"{where}: {tag} has no SPEC.md for this module")
        _, added = git("log", "--diff-filter=A", "--format=%H", "--", f"modules/{d}/RESULT.md")
        first = added.split()[-1] if added else None
        if not first:
            errors.append(f"{where}: commit RESULT.md")
        elif first == tag_commit or git("merge-base", "--is-ancestor", tag_commit, first)[0] != 0:
            errors.append(f"{where}: RESULT.md was committed before, or together with, the spec freeze {tag}")
        v = re.search(r"\*\*Verdict:\*\*\s*(\w+)", text)
        if not v or v.group(1) not in VERDICTS:
            errors.append(f"{where}: verdict must be Supports, Fails or Inconclusive")
    for e in errors:
        print(e)
    print(f"{len(errors)} problem(s) in {count} module(s)" if errors else f"{count} module(s) in order")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
