# Module NN · short-name · spec v1

Copy `modules/_template/` to `modules/NN-short-name/`. Answer every field before any run. To freeze, commit this file and tag the commit `NN-short-name/spec-v1`. After the tag, this version cannot change: a changed diagnostic is a new file version and a new tag (`spec-v2`), and earlier results stay in the record.

| Field | What it states |
| --- | --- |
| Bears on | `EE-H-nnnn`, `EE-C-nnnn`, and the book section that defines the diagnostic |
| Question | One sentence a reader outside the project would understand |
| Generative rule | The update rule, in full |
| Forbidden structure | What the rule may not contain at this stage of the book |
| Initial conditions | Including how they are sampled |
| Control | What the result is measured against, and why it is the fair comparison |
| Diagnostic | The quantity computed, and the threshold that counts as success |
| Readout resolution | What outcome differences the readout can register, and the noise floor below which a difference does not count |
| Positive control | A case whose effect is known to exist, which must register at that resolution |
| Failure criterion | What result would count against the hypothesis |
| Runs | Number of runs and seeds, and how variation is reported |
| Representation checks | The relabellings and re-encodings the verdict must survive |
| Freeze | The tag that fixes all of the above |

## Readout resolution

Every diagnostic declares the resolution of its readout (what outcome differences it can register) and includes a positive control: a case whose effect is known to exist, which must register at that resolution. A null result then has three possible outcomes, and the RESULT must say which applies:

- **Absent:** the positive control registers, and the tested case does not.
- **Derived:** the tested case registers only through another relation, or only at another level of readout.
- **Unresolved:** the positive control does not register, so the readout cannot decide.

Only "absent" counts as evidence that a relation does not participate, or that two microstates are the same. The noise sets the lower bound on what counts as a difference; the positive control shows the readout can see a difference at all. Together they keep a coarse readout from producing false "same" verdicts.

- **Book exports:** the commit in `book/SOURCE` when this spec was written
