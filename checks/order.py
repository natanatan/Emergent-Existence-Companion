#!/usr/bin/env python3
"""Check each module's declared structure against the book's derivation order.

A spec states what its rule may use and must not contain as register IDs, in
a fenced block in SPEC.md:

    ```structure
    stage: Cl                      # the ladder stage the module tests
    uses: [Df, Ds, Bd, Rl, Cl]     # element codes or EE-C claim IDs the rule relies on
    forbids: [Or, Sc, Dt, Gm, Sp, Tm]
    ```

What counts as earned at a stage is read from book/ladder.json, never from
chapter numbers written in the spec, so the check follows the book if its
derivation order changes. For a claim ID, the claim's concepts and
composition must all be earned at the stage.

Errors (exit 1), for specs not yet frozen:
  - an unknown stage, element code or claim ID
  - something in `uses` that the stage has not earned
  - something in `forbids` that the stage has already earned
Flags (reported, exit 0), for frozen specs:
  - the same conditions, when the book changed after the freeze
  - drift: book/ladder.json at the spec tag and now disagree about anything
    the module uses or forbids. The results stand, scoped to the book commit
    they were run against (book/SOURCE at the tag), and the module is due
    for review under the new order.
Specs without a structure block are listed as undeclared.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r"```structure\n(.*?)```", re.S)
CLAIM = re.compile(r"^EE-C-\d{4}$")


def git(*args):
    r = subprocess.run(["git", "-C", HERE, *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def parse(text):
    m = BLOCK.search(text)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        k, v = (s.strip() for s in line.split(":", 1))
        out[k] = [x.strip() for x in v.strip("[]").split(",") if x.strip()] if k != "stage" else v
    return out


class Book:
    def __init__(self, ladder, claims):
        self.stage = {s["stage"]: s for s in ladder}
        self.claims = {c["id"]: c for c in claims}
        for c in claims:
            for a in c.get("aliases") or []:
                self.claims.setdefault(a, c)
        self.codes = {e for s in ladder for e in s["earns"]}

    def needs(self, item):
        """Element codes an item stands for, or None if unknown."""
        if CLAIM.match(item):
            c = self.claims.get(item)
            return None if c is None else set(c.get("concepts") or []) | set(c.get("composition") or [])
        return {item} if item in self.codes else None

    def earned(self, item, stage):
        """True, False, or None when the item or stage is unknown."""
        s, n = self.stage.get(stage), self.needs(item)
        if s is None or n is None:
            return None
        return n <= set(s["earned_so_far"])


def load(path):
    with open(os.path.join(HERE, path), encoding="utf-8") as f:
        return json.load(f)


def book_at(tag):
    ok1, lad = git("show", f"{tag}:book/ladder.json")
    ok2, cl = git("show", f"{tag}:book/claims.json")
    _, src = git("show", f"{tag}:book/SOURCE")
    if ok1 or ok2:
        return None, src.strip()
    return Book(json.loads(lad), json.loads(cl)), src.strip()


def problems(book, s):
    out = []
    stage = s.get("stage")
    if stage not in book.stage:
        return [f"unknown stage {stage!r}"]
    for item in s.get("uses", []):
        e = book.earned(item, stage)
        if e is None:
            out.append(f"uses {item}, which the book does not have")
        elif not e:
            out.append(f"uses {item}, which {book.stage[stage]['title']} has not earned")
    for item in s.get("forbids", []):
        e = book.earned(item, stage)
        if e is None:
            out.append(f"forbids {item}, which the book does not have")
        elif e:
            out.append(f"forbids {item}, which {book.stage[stage]['title']} has already earned")
    return out


def main():
    now = Book(load("book/ladder.json"), load("book/claims.json"))
    source = open(os.path.join(HERE, "book", "SOURCE")).read().strip()
    root = os.path.join(HERE, "modules")
    errors, flags, undeclared, ok = [], [], [], []
    for d in sorted(os.listdir(root)):
        spec = os.path.join(root, d, "SPEC.md")
        if d.startswith("_") or not os.path.exists(spec):
            continue
        s = parse(open(spec, encoding="utf-8").read())
        if s is None:
            undeclared.append(d)
            continue
        _, tags = git("tag", "--list", f"{d}/spec-v*")
        tags = sorted(tags.split(), key=lambda t: int(t.rsplit("v", 1)[1]))
        found = problems(now, s)
        if not tags:
            errors += [f"modules/{d}: {p}" for p in found]
            if not found:
                ok.append(d)
            continue
        tag = tags[-1]
        then, then_src = book_at(tag)
        flags += [f"modules/{d} ({tag}): {p} under the book at {source}" for p in found]
        if then is not None:
            stage = s.get("stage")
            changed = [i for i in s.get("uses", []) + s.get("forbids", [])
                       if then.earned(i, stage) != now.earned(i, stage)]
            if changed:
                flags.append(f"modules/{d} ({tag}): derivation order changed for {', '.join(changed)} since the "
                             f"freeze. Results stand, scoped to {then_src}; review the module under {source}")
        if not found:
            ok.append(d)
    for e in errors:
        print("error:", e)
    for f in flags:
        print("flag:", f)
    if undeclared:
        print("undeclared (no structure block):", ", ".join(undeclared))
    print(f"{len(ok)} declared and consistent with the book at {source}; "
          f"{len(errors)} errors, {len(flags)} flags, {len(undeclared)} undeclared")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
