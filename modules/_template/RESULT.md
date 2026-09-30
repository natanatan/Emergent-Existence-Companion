# Module NN · short-name · result

- **Spec tag:** `NN-short-name/spec-v1`
- **Verdict:** Supports | Fails | Inconclusive
- **Repository commit:**
- **Book exports:** commit from `book/SOURCE`
- **Seeds and environment:** see `runs/`

## Numbers

The diagnostic against its control, with the variation across runs.

## Null outcomes

For every diagnostic that registered no difference, say which applies, with the positive control's reading beside it:

| Diagnostic | Positive control registered? | Outcome |
| --- | --- | --- |
| | yes / no | Absent / Derived / Unresolved |

Only "absent" counts as evidence that a relation does not participate, or that two microstates are the same.

## Representation checks

Which relabellings and re-encodings were run, and whether the verdict survived each.

## Verdict

Supports: the diagnostic passed against its control and survived the representation checks. Fails: the failure criterion was met. Inconclusive: neither, with the reason.

## Register event proposed

One pull request on the main repository that adds a source record for this run (`kind: simulation`, with the module, spec tag, commit and verdict), cites it from the Hypothesis Register entry, and adds a dated status event within the cap. A single supporting run can move an entry to Provisional, not to Retained. See the main repository's `docs/sources.md`.
