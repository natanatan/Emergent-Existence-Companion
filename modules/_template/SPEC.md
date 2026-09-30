# Module NN · short-name · spec v1

Copy `modules/_template/` to `modules/NN-short-name/`. Answer every field before any run. To freeze, commit this file and tag the commit `NN-short-name/spec-v1`. After the tag, this version cannot change: a changed diagnostic is a new file version and a new tag (`spec-v2`), and earlier results stay in the record.

| Field | What it states |
| --- | --- |
| Bears on | `EE-H-nnnn`, `EE-C-nnnn`, and the book section that defines the diagnostic |
| Question | One sentence a reader outside the project would understand |
| Generative rule | The update rule, in full |
| Structure | The stage tested, and what the rule uses and forbids, as register IDs (below) |
| Forbidden structure | What the rule may not contain at this stage, in words, and how the spec avoids each item |
| Initial conditions | Including how they are sampled; for anything below the starting resolution, whether the alternatives are sampled or one is declared (guardrail 6) |
| Control | What the result is measured against, and why it is the fair comparison |
| Diagnostic | The quantity computed, and the threshold that counts as success |
| Readout resolution | What outcome differences the readout can register, and the noise floor below which a difference does not count |
| Positive control | A case whose effect is known to exist, which must register at that resolution |
| Failure criterion | What result would count against the hypothesis |
| Runs | Number of runs and seeds, and how variation is reported |
| Representation checks | The relabellings and re-encodings the verdict must survive |
| Freeze | The tag that fixes all of the above |

## Structure

Declare the stage and the structure by ID, so `checks/order.py` can follow the book if its derivation order changes:

```structure
stage: Cl                      # the ladder stage this module tests
uses: [Df, Ds, Bd, Rl, Cl]     # element codes or EE-C claim IDs the rule relies on
forbids: [Or, Sc, Dt, Gm, Sp, Tm]
```

Codes are the element codes in `book/elements.json`; stages are the codes in `book/ladder.json`. What each stage has earned is read from the ladder, never from chapter numbers in this spec.

## Readout resolution

Every diagnostic declares the resolution of its readout (what outcome differences it can register) and includes a positive control: a case whose effect is known to exist, which must register at that resolution. A null result then has three possible outcomes, and the RESULT must say which applies:

- **Absent:** the positive control registers, and the tested case does not.
- **Derived:** the tested case registers only through another relation, or only at another level of readout.
- **Unresolved:** the positive control does not register, so the readout cannot decide.

Only "absent" counts as evidence that a relation does not participate, or that two microstates are the same. The noise sets the lower bound on what counts as a difference; the positive control shows the readout can see a difference at all. Together they keep a coarse readout from producing false "same" verdicts.

- **Book exports:** the commit in `book/SOURCE` when this spec was written
