# Emergent Existence · Computational Companion

Runnable models for the claims and hypotheses of *Emergent Existence*, Volume I, Book I.

The book builds physical structure step by step from a minimal starting point, and it keeps a public record of what each step earns and what it leaves open. Some of the open entries are not matters of argument. They are claims about what a model would do, and those can be run rather than debated: whether recursive relational rules settle into a stable low-dimensional regime, whether diffusion and wave behaviour diverge on a relational graph, whether an effective metric survives coarse-graining, whether temporal order survives the removal of every index.

This repository is where those runs live. It is written for readers in computer science and applied physics who want to run the models rather than read about them.

> A framework that claims to be constrained by more than its own consistency should say what would embarrass it, and say it precisely enough that someone else can check.

## How it connects to the book

```
Emergent-Existence (manuscript, registers, checks)
        │  exports/: claims EE-C-nnnn, hypotheses EE-H-nnnn, earned ladder
        ▼
Emergent-Existence-Companion (this repository)
        │  one module per question, each citing the IDs it bears on
        ▼
result → a dated status event on the Hypothesis Register entry, citing the run
```

- **Everything is cited by ID.** A module names the hypotheses (`EE-H-nnnn`) and claims (`EE-C-nnnn`) it tests. It reads them from the main repository's `exports/`, never from the prose, so edits to the book's wording cannot break a model.
- **Results flow back through the register.** When a run settles or bears on a question, the result goes to the main repository as a pull request that adds a status event to the relevant Hypothesis Register entry, citing the module, the run and the commit that produced it.
- **The starting backlog is the register.** 43 of the 135 entries in the Hypothesis Register are marked `companion_testable`. Several already name the diagnostic the book specifies for them, for example the addressability test of 6.17, the role-exchange and reversal tests of 7.15, the return diagnostics of 8.23 and the scale diagnostics of 10.25.

## Guardrails

These come from the book's Methodology and bind every module.

1. **A model demonstrates a mechanism, not a world.** A rule that produces three effective dimensions shows that such a rule can. It does not show that the world runs on it. Results are reported in that register.
2. **The diagnostic and its control are fixed before the run.** The specification is committed, and the commit is tagged, before any result exists. A module that changes its diagnostic after seeing results starts a new specification version; the earlier one and its results stay in the record.
3. **A failed diagnostic is reported, not retuned.** A failure is a finding. Adjusting parameters until the test passes turns a test into a demonstration of the modeller's patience.
4. **No smuggling.** A model may use only what the book has earned by the stage it tests. A model of Orientation may not encode a direction; a model of Distance may not start from coordinates; a model of Time may not rely on an iteration counter as a clock. Every module states what its rule is forbidden to contain, and the review checks for it.
5. **Results must survive a faithful change of representation.** Relabelling nodes, reordering updates or swapping an equivalent encoding should not change the verdict. If it does, the result belongs to the representation, not to the structure (Formalism, 9.28, diagnostic 1).
6. **Origin is represented openly.** A model may not fix what lies below the resolution it starts from. Initial conditions are sampled across the admissible alternatives (uniform, unresolved variation, and so on) rather than chosen as one, and a verdict that depends on that choice is reported as such (Origin, 1.5).

## Evidence standard

A Companion run is a source like any other, and the book holds its sources to one standard. The same rules apply when a module cites outside work.

- **Role.** Every source a claim relies on has a role: *premise* (the claim fails if the source is wrong), *support*, *lineage* or *foil*. Only premises carry the full checks below.
- **It says what it is cited for.** Checked against the source itself, with the page or line, the date and the checker recorded.
- **No scope inflation.** The claim may not exceed the source: "suggests" is not "shows", a simulation is not a measurement, a result in one regime is not a law.
- **Graded by method, not by standing.** The grade comes from the kind of result (measurement, replicated result, proof, single study, simulation, argument, opinion), adjusted by four questions: is the method visible, has anyone checked it independently, what is the source's record on questions of this kind, and who gains if it is believed. No source is weighted up or down for being official.
- **Independent lines, not citation counts.** Two papers from one group or one dataset are one line of evidence.
- **The strongest objection is recorded.** The best competing result or dissent is noted beside the source, so the claim is weighed against it rather than chosen around it.
- **Currency.** Retractions, failed replications and superseding results are checked on a schedule.
- **Status is capped by evidence.** A register entry cannot stand higher than its weakest premise source allows. A single unreplicated run keeps an entry Provisional however well it fits the argument.
- **Failure flags, it does not rewrite.** If a premise source is retracted or fails to replicate, every claim resting on it is flagged for the author's review. The text changes only by the author's decision.

## Anatomy of a module

Each question gets a folder:

```
modules/
  05-closure-addressability/
    SPEC.md        the preregistered specification (frozen before any run)
    model/         the generative rule and its implementation
    controls/      the matched controls
    runs/          seeds, configuration, raw outputs, environment lock
    RESULT.md      what happened, and the verdict
```

`SPEC.md` answers, in this order:

| Field | What it states |
| --- | --- |
| Bears on | The `EE-H` and `EE-C` IDs, and the book section that defines the diagnostic |
| Question | One sentence a reader outside the project would understand |
| Generative rule | The update rule, in full |
| Forbidden structure | What the rule may not contain at this stage of the book (guardrail 4) |
| Initial conditions | Including how they are sampled |
| Control | What the result is measured against, and why it is the fair comparison |
| Diagnostic | The quantity computed, and the threshold that counts as success |
| Readout resolution | What outcome differences the readout can register, and the noise floor below which a difference does not count |
| Positive control | A case whose effect is known to exist, which must register at that resolution |
| Failure criterion | What result would count against the hypothesis |
| Runs | Number of runs and seeds, and how variation is reported |
| Representation checks | The relabellings and re-encodings the verdict must survive |
| Freeze | The tagged commit that fixes all of the above |

`RESULT.md` reports the outcome as one of three verdicts, with the numbers behind it:

- **Supports:** the diagnostic passed against its control, and survived the representation checks.
- **Fails:** the failure criterion was met. The module is kept, and the failure is sent to the register like any other result.
- **Inconclusive:** neither, with the reason (too few runs, control too weak, sensitivity to representation).

Every diagnostic also declares its readout resolution and a positive control, a case whose effect is known to exist. A null result is then reported as **absent** (the positive control registers and the tested case does not), **derived** (the tested case registers only through another relation, or only at another level of readout) or **unresolved** (the positive control does not register). Only "absent" counts as evidence that a relation does not participate, or that two microstates are the same.

## Workflow

1. Pick an entry marked `companion_testable` in the main repository's Hypothesis Register.
2. Write `SPEC.md`, including the forbidden structure, and have it reviewed against the book section it cites.
3. Commit and tag the specification. From this point the diagnostic cannot change within this version.
4. Implement the model and the control. Pin the environment and record seeds.
5. Run, then write `RESULT.md` whatever the outcome.
6. Open a pull request on the main repository adding a dated status event to the Hypothesis Register entry, citing the module, the tag and the verdict. The status it may propose is limited by the evidence standard above: a single supporting run can move an entry to Provisional, not to Retained.

## Reproducing a result

Every run records the commit of this repository, the tag of its specification, the export version of the registers it read, the seeds and a locked environment. Rerunning a module from its tag must reproduce its `RESULT.md` within the variation it reports. A result that cannot be reproduced is reported as Inconclusive until it can.

## Contributing

Specifications are the most valuable contribution: a precise statement of what would count against a hypothesis is worth more than a model that confirms one. Proposals for new modules, reviews of existing specifications against the book, independent reimplementations and reported failures are all welcome. An independent reimplementation that reaches the same verdict is what turns one line of evidence into two.

## In this repository

| Path | Contents |
| --- | --- |
| [`BACKLOG.md`](BACKLOG.md) | The 43 `companion_testable` entries and the modules that bear on each (generated) |
| `book/` | A copy of the main repository's `exports/`, pinned to one commit, which `book/SOURCE` records. Refresh it with `python tools/sync_book.py` (or `--ref <commit>`) |
| `modules/_template/` | Copy it to `modules/NN-short-name/` to start a module. Spec tags are named `NN-short-name/spec-v1`, `spec-v2`, … |
| `checks/freeze.py` | Run in CI. Fails if a module cites an ID the book does not have, or if a `RESULT.md` was committed without a spec tag that came before it |

## Licence

Code is released under the MIT licence and documentation under CC BY 4.0, matching the main repository.

## Citing

Cite the module, its specification tag and the register ID it bears on, for example: *Emergent Existence Computational Companion, module 05, spec v1 (EE-H-0060).*
