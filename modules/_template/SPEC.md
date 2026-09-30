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
| Failure criterion | What result would count against the hypothesis |
| Runs | Number of runs and seeds, and how variation is reported |
| Representation checks | The relabellings and re-encodings the verdict must survive |
| Freeze | The tag that fixes all of the above |

- **Book exports:** the commit in `book/SOURCE` when this spec was written
