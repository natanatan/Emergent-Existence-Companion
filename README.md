# Emergent Existence: Computational Companion

Computational tests of the claims and hypotheses of *Emergent Existence*. The book's public repository, [Emergent-Existence](https://github.com/natanatan/Emergent-Existence), is the reference: this repository reads its registers through `exports/`, pinned to one book commit, and cites everything by permanent ID (`EE-C-nnnn` for claims, `EE-H-nnnn` for hypotheses).

## What gets tested

The book's Hypothesis Register marks 43 hypotheses as testable here. They are listed in [`BACKLOG.md`](BACKLOG.md), which is generated. To refresh it:

```
python tools/sync_book.py            # latest book exports
python tools/sync_book.py --ref <commit>
```

## Rules

These follow the book's own method.

1. **Diagnostics are declared before the run.** Each test starts as `tests/<ID>/PROTOCOL.md`, committed before any result: what is being tested, the book commit, the model, what counts as success, what counts as failure, and which parameters are fixed. The check in `checks/protocol.py` fails if a result was committed before its protocol.
2. **Failures are reported, not retuned away.** A failed prediction is a result. If the protocol changes after a run, the old protocol and its result stay, and the new one is a new run.
3. **A test never assumes what the claim is meant to derive.** Structure the book earns only at a later stage may appear in the diagnostics applied to a model's output, never in the model's premises. Each protocol lists the elements (two-letter codes from the book's element table) its model uses.
4. **Results say what they test and at which version.** Every result names the claim or hypothesis ID and the book commit in `book/SOURCE`.

## Layout

| Path | Contents |
| --- | --- |
| `book/` | Pinned snapshot of the book's exports, and `SOURCE` with the book commit |
| `BACKLOG.md` | Testable hypotheses and which have a test (generated) |
| `tests/<ID>/` | One directory per claim or hypothesis tested: `PROTOCOL.md`, code, `RESULT.md` |
| `tests/_template/` | Copy this to start a test |
| `checks/` | Repository checks, run in CI |
| `tools/` | Sync from the book |

## License

Code is MIT. Copyright (c) 2026 Natan Mallinger. The book's registers, which `book/` copies, are CC BY 4.0.
