# Module 05 · closure-addressability · spec v1

Reviewed against Closure, 6.4, 6.6, 6.7, 6.12 and 6.17, and frozen by the tag `05-closure-addressability/spec-v1`. Nothing in `model/`, `controls/` or `runs/` was written before that tag. The decisions taken at review, and the feasibility pilot that informed them, are recorded at the end.

## Bears on

| ID | What | Book |
| --- | --- | --- |
| `EE-H-0060` | A closed organization is relationally addressable exactly when external relations descend to its equivalence class (tested). Whether it can then serve as a new higher-order origin is **not** tested here | Closure, 6.12, 6.13, 6.17 |
| `EE-C-0088` | The descent criterion: if Σa ~F Σb then E(Σa) ~F′ E(Σb), so Ē([Σ]~F) = [E(Σ)]~F′ | 6.12 |
| `EE-C-0097` | The four diagnostics of closure, and the fifth: comparison with matched controls | 6.17 |
| `EE-C-0073` | The Minimal Closure Test: internal sufficiency, constraint participation, consistent realizability | 6.4 |
| `EE-C-0077` | Realizability: 𝒮F(ℛ) ≠ ∅ | 6.6 |
| `EE-C-0078` | Dynamic closure: preservation of sufficiency under 𝒰 (secondary readout only) | 6.7 |

## Question

When a group of mutually constraining relations holds itself together, does the rest of a network interact with it as a single unit exactly when that interaction depends only on what the group holds fixed, and not on how the group happens to be realized?

## Generative rule

**Relations.** N retained relations x₁ … x_N. Each has two resolvable values (retained distinctions, Boundary). They are written 0 and 1 in the implementation. Which value is called 0 carries no meaning (see representation check R2).

**Constraints.** M constraints. Constraint j has a member set S_j of three relations, drawn uniformly without replacement and independently of every other constraint. A constraint is its table of admissible patterns on S_j: four of the eight patterns are admissible, and the other four are not. The tables are drawn from the family of patterns with an even number of 1s, or, if the constraint's type b_j = 1, an odd number (b_j drawn uniformly). "Even" and "odd" describe the table from outside; the model holds only the table, and nothing in it counts (R4 checks this). A constraint's admissible set is unchanged by any permutation of its members, so no member plays a distinct role. A constraint among three relations is a mutual constraint among retained relations, which Relation (5.4) earns: the admissible values of each depend on the others. Nothing in the generator plants groups, modules or communities.

**Admissible succession 𝒰.** One succession step:

1. Choose one relation i uniformly at random.
2. Take C(i), the constraints with i as a member, and find the values v for which every constraint in C(i) is satisfied when x_i = v.
3. If exactly one value qualifies, set x_i to it. If both qualify or neither does, set x_i to a value chosen uniformly at random.

The rule reads only the current state. It never reads the step count, a position, a weight or any earlier state.

**Diagnostic perturbation family 𝔗C.** This family belongs to the test, not to the rule (Boundary, 4.6). After each step, with probability η, one relation chosen uniformly at random is flipped.

**Candidate domains.** A candidate is a set of relations V. Its internal constraints are I(V) = {j : S_j ⊆ V}. Its boundary constraints are B(V) = {j : S_j meets V but S_j ⊄ V}.

- **F** is the invariant "every internal constraint is satisfied".
- **𝒮F(V)** is the set of states of V that satisfy F.
- **~F** puts two states of V in the same class when both lie in 𝒮F(V). The class under test is O_F = 𝒮F(V).

## Forbidden structure

Closure has not earned the following, so the rule and the generator may not contain them. The list follows the Closure ledger's withholds, together with guardrail 4.

| Forbidden | Because | How this spec avoids it |
| --- | --- | --- |
| Positions, coordinates, a lattice, embedding, distances between relations | Metric distance, spatial enclosure and geometry are withheld | Members are drawn uniformly. No relation is near or far from another |
| Direction: input and output roles, directed edges | Orientation is earned at Orientation (7) | Constraints are symmetric in their members. The rule treats every member alike |
| A clock | Metric time is earned at Time (14) | The rule never reads the step count. The run length T is an external readout |
| Weights, magnitudes, majority, thresholds | Threshold aggregation is withheld; magnitude is earned at Scale (10) | The rule distinguishes three admissibility cases (one value, both values, neither). It never compares amounts |
| Memory, path dependence | Both are withheld at Closure | The rule is a function of the current state only |
| A target grouping | 6.17: "if closure appears only because the target boundary or topology is hard-coded, closure has not been generated" | Candidates are found by the detector below from an unplanted network |
| Reading agreement as causation | Physical causation is withheld | The verdict is stated as relational addressability (6.12) |

External readouts such as counts, fractions, rank over GF(2), distances between distributions and run lengths are allowed. They are diagnostics applied to the model's output, not premises of the rule (6.17; Methodology, 1.8).

## Initial conditions

- **Networks.** N = 60. The density M/N is 0.5, 0.6 or 0.7. There are 40 networks per density, with network seeds 1–120.
- **Candidate detector.** The detector is external and uses no target. From each constraint as a seed, it grows V greedily: at each step it adds the member set of the boundary constraint that most reduces leakage (below), with ties broken by a seeded random choice. It never makes an addition that would take |V| past 16, and it stops when no allowed addition reduces leakage. It keeps every V with 6 ≤ |V| ≤ 16 that passes the closure test:
  - **Sufficiency (6.4):** leakage L(V) ≤ λ. L(V) is the fraction of member–constraint incidences (i ∈ V, j ∋ i) whose constraint lies outside V. λ = 0.3. The leakage limit is a detector setting, not a definition of closure: whether the remaining outside incidences are constitutive is tested by the participation ablation.
  - **Participation (6.4):** every internal constraint is non-redundant, so removing it enlarges 𝒮F(V). Equivalently, the rows of I(V) are independent over GF(2).
  - **Realizability (6.6):** 𝒮F(V) ≠ ∅. Addressability also needs at least two microstates, so |𝒮F(V)| ≥ 2. That is a requirement of this test, not of closure.

  Duplicates are removed. Up to 3 candidates per network are selected at random (seeded).
- **Microstates.** States of V are drawn uniformly from 𝒮F(V), by sampling uniformly from the solutions of the internal parity system. How pairs are drawn is set out under Diagnostic.

## Control

The fifth diagnostic of 6.17 has three matched controls. Each is drawn from the same network with the same |V|, and each is required to have |𝒮F(V)| ≥ 2. A candidate with no available C3 is compared with C1 and C2 only, and the count of such candidates is reported.

| Control | Matched on | Differs by |
| --- | --- | --- |
| C1 random | Size | V drawn uniformly |
| C2 merely connected | Size, and connected through shared constraints | Fails the closure test |
| C3 equally dense | Size and number of internal constraints (within one, if no exact match is found in 2,000 draws; the match is recorded) | Fails the closure test |

These are the fair comparison because they separate closure from its look-alikes: size, connectedness and internal density. Chapter 6 argues that none of these is closure (6.4, 6.18). The controls bear on the fifth diagnostic of 6.17 (EE-C-0097). EE-H-0060 is a claim about closed organizations, so its verdict is computed on closed candidates only; the same predictions on the controls are reported alongside.

## Diagnostic

### Couplings

EE-H-0060 is about the external relations of a closed organization as a whole, so every arm states which external relations the organization has.

- **Coupling arms.** The candidate's own boundary constraints B(V) are removed from the rule for the whole run, so the only external relation is one added coupling. The coupling is a single constraint on W ∪ {y}, with W ⊆ V, 1 ≤ |W| ≤ 3, and y one fresh external relation. Its table is the even or odd parity family on |W| + 1 members, with its type drawn uniformly. The coupling reads W only through that table.
  - **Descending:** the parity of W is constant on 𝒮F(V). For a consistent parity system this holds exactly when W's indicator lies in the row space of I(V) over GF(2). Then E(Σa) and E(Σb) are the same for every Σa ~F Σb (6.12).
  - **Non-descending:** the parity of W varies on 𝒮F(V).
  - **Sampling W.** The eligible descending sets are the nonzero row-space vectors of weight 1 to 3. Five are drawn uniformly without replacement; if fewer than five exist, all are used and the count is reported, and a candidate with none contributes no descending case. Non-descending sets are drawn by choosing |W| uniformly from 1 to 3, then W uniformly among the non-descending sets of that size, without replacement, until five are drawn.
- **Natural arm.** No coupling is added, and B(V) stays in the rule. The external relations are B(V), and y is every relation outside V that B(V) reaches. B(V) descends when every boundary constraint's part inside V, S_j ∩ V, has an indicator in the row space of I(V). This is computed for every case. Natural cases enter the accuracy with the prediction their computed descent gives.

Whether a coupling or a boundary descends is computed by linear algebra, before any run.

### Runs, pairs and batches

- **Run length.** Every run lasts 20 sweeps, T = 20·(number of relations in the network, including y) succession steps. T is an external readout; the rule never reads it.
- **Pairs.** Σa ≠ Σb are drawn uniformly from 𝒮F(V). For a non-descending coupling, and for the positive control, pairs are drawn uniformly among those on which W's parity differs, so the tested difference is present in every pair. Every relation outside V, y included, is drawn uniformly once per pair and is shared by all batches of that pair.
- **Batches.** For each pair there are four batches of R = 100 runs: from Σa, from Σb, and two more from Σa, written Σa′ and Σa″.

### The addressability gap

For each component of a readout (F holding, and each relation in the readout), estimate from a batch the probability that it takes the value 1. D(x, z) is the largest difference over components between batches x and z. Comparing components one at a time keeps the readout resolvable when there are many components; a distance over joint states would need far more runs than there are.

- G = mean over pairs of D(a, b) − D(a, a′): the difference between the microstates, above run-to-run noise.
- G₀ = mean over pairs of D(a, a″) − D(a, a′): the same statistic when there is no difference in microstate. This is the null.

## Readout resolution

Each diagnostic declares what its readout can register and carries a positive control, a case whose effect is known to exist and which must register at that resolution. A null result is then one of three outcomes, and `RESULT.md` says which applies to every null:

- **Absent:** the positive control registers, and the tested case does not.
- **Derived:** the tested case registers only through another relation, or only at another level of readout.
- **Unresolved:** the positive control does not register, so the readout cannot decide.

Only "absent" counts as evidence that a relation does not participate, or that two microstates are the same.

### The addressability gap

- **Readout levels.**
  - **L1, the coupled readout:** F on V, and the relations y. This is the readout the verdict uses.
  - **L2, other relations:** every relation outside V that is not in y.

  The microstate of V itself is never a readout. Σa and Σb differ there by construction, and 6.12 says that lower-order multiplicity does not disappear; it becomes irrelevant to the coupling. In the coupling arms B(V) is removed, so nothing but the coupling joins V to the rest; L2 can differ only through y.
- **Resolution, the noise floor.** γ is the 95th percentile of G₀, calibrated separately for each combination of density, η, arm (candidate, C1, C2, C3), coupling kind (descending, non-descending, positive control, natural) and readout level. In the natural arm, where the number of components varies, cases are further grouped by component count (2–4, 5–8, 9–16, more than 16). All γ values are computed and recorded before any G is compared with them. A gap at or below γ cannot be told apart from run-to-run noise.
- **Positive control.** Each candidate and each control gets one coupling-arm case with W = {w}, a single member of V that is not constant on 𝒮F(V), with pairs that differ at w. It is non-descending by construction, and it is not among the five non-descending couplings. Its gap must exceed γ at L1. If it does not, every gap for that candidate or control is Unresolved.
- **Outcomes, in order of precedence.** A case takes the first that applies:
  1. **Unresolved:** the positive control did not register.
  2. **Registers:** G > γ at L1.
  3. **Derived:** G ≤ γ at L1, but G > γ at L2.
  4. **Absent:** otherwise.

  A case is **addressable** only if it is Absent.

### The participation ablation

This is a secondary readout, the second diagnostic of 6.17, run in the natural arm at η = 0.01.

- **Readout.** F-persistence is the fraction of runs in which F holds on V at T. To ablate a constraint, it is removed from the rule for every member, while F is still judged on the full I(V).
- **Resolution.** The absolute change in F-persistence must exceed the 95th percentile of the absolute change between two unablated batches. The sign of every change is reported.
- **Positive control.** One internal constraint of V, chosen at random, is ablated. It is constitutive of F by definition, so its ablation must register. If it does not, the ablation readout for that candidate is Unresolved.
- **Tested cases.** Each boundary constraint in B(V) is ablated in turn. These are the relations the closure test classes as non-constitutive. The outcomes follow the same order of precedence: Unresolved; Registers (it participates: a constitutive dependency outside V, reported against sufficiency, 6.4); Derived (it registers only on L2); Absent (it does not participate).

## Predictions and verdict

### EE-H-0060 (the verdict)

Computed on closed candidates, in the coupling arms and the natural arm together.

- **P1 (if):** cases whose external relations descend are Absent.
- **P2 (only if):** cases whose external relations do not descend Register.
- **Accuracy** is the fraction of cases, among those that are Absent or Register, in which descent predicts the outcome. It is pooled over densities, for each η separately, and also reported per density.
- **Resolution** is the fraction of cases that are Absent or Register, in the P1 set and in the P2 set, for each η. Unresolved and Derived cases are not resolved.

The verdict takes the first of these that applies:

1. **Inconclusive** if any representation check changes it (below).
2. **Inconclusive** if resolution is below 80% in the P1 set or the P2 set at either η. The readout could not decide often enough for a verdict.
3. **Fails** if accuracy is below 0.80 at either η, or below 0.80 at any single density. The RESULT reports which of P1 or P2 failed.
4. **Supports** if accuracy is at least 0.95 at both η, and at least 0.90 at every density.
5. **Inconclusive** otherwise, with the criterion that was missed and by how much.

### EE-C-0097, the fifth diagnostic (reported, not part of the verdict)

6.17 claims that the closure criterion identifies a nontrivial class whose higher-order addressability exceeds the look-alike controls. This is reported separately, because EE-H-0060 does not imply it.

- **P3a, analytic:** the fraction of natural boundaries that descend, closed candidates against each control. No runs are needed.
- **P3b, measured:** the fraction of natural-arm cases that are addressable, closed candidates against each control. Only resolved cases are counted, and the resolution rate of each arm is reported.

Each is the difference between the candidate fraction and the control fraction, with a network-level bootstrap 95% interval (10,000 resamples, pooled over densities, each η separately). It bears in favour if the interval lies entirely above 0, against if it lies entirely below 0, and is inconclusive otherwise.

### Secondary readouts

These are reported but do not decide anything: leakage; the participation ablation; the P1 and P2 accuracy on the controls; and closure robustness (the fraction of natural-arm runs under 𝔗C in which F holds at T). Realizability is not reported as a diagnostic on this substrate. Rows independent over GF(2) are always consistent, so 𝒮F(V) ≠ ∅ holds by construction once participation passes, and |𝒮F(V)| = 2^(|V| − rank).

## Runs

- 3 densities × 40 networks, with up to 3 candidates each, and for each candidate its three controls.
- Per candidate or control: 1 positive-control coupling, up to 5 descending couplings, 5 non-descending couplings and the natural arm; 10 pairs per case; 4 batches of R = 100 runs per pair; η ∈ {0, 0.01}.
- The ablation: in the natural arm at η = 0.01, per candidate, 1 positive control and every boundary constraint, each with 2 batches of 100 runs from each of 10 states drawn from 𝒮F(V).
- About 1.5 × 10⁸ runs in all. The implementation vectorizes over runs; the estimate is about a day on a four-core machine.
- **Seeds.** Every random draw has its own stream, derived from the tuple (density, network seed, arm, candidate index, purpose, case index, pair index, batch, η, run index). The purpose is one of: detector, control, W, pair, initial state, batch, ablation. The batch is one of a, b, a′, a″. No two batches share a stream, and every run can be reproduced on its own.
- Variation is reported as medians and interquartile ranges across networks, with bootstrap intervals at network level.
- Accuracy is also reported separately by density, by |W| and by |V|.

## Representation checks

The verdict must be the same under each of these. For R1–R3, per-case outcomes must also agree in at least 98% of cases, allowing for sampling noise. R4 changes only the encoding, so its trajectories must be identical under the same seeds.

| Check | Change | Why it should not matter |
| --- | --- | --- |
| R1 | Relabel the relations by a random permutation | Names carry no structure |
| R2 | Exchange the values 0 and 1 everywhere, adjusting each constraint's type | Which value is called 0 is a convention |
| R3 | Replace uniform choice of i by random-order sweeps, with each relation once per sweep | Both are admissible schedules with no privileged order |
| R4 | Encode constraints as explicit tables of admissible patterns instead of the parity rule | Same constraints, different encoding. Trajectories must be identical under the same seeds |

If a check changes the verdict, the result is reported as Inconclusive with the check named (Formalism, 9.28, diagnostic 1).

## Freeze

`05-closure-addressability/spec-v1`.

- **Book exports:** `natanatan/Emergent-Existence@fe713e6`

## Decisions at review

The author delegated the review of the open items to Claude on 30 September 2026, on the understanding that any change after v1 is a new specification version.

- **Feasibility pilot, before the freeze.** `feasibility/yield.py` and `feasibility/controls_yield.py` measure only detector yield, control availability and the cost of one update step. They compute no diagnostic. At the drafted λ = 0.2, the detector found candidates in 17 of 20 networks at density 0.5, 2 of 20 at 0.7 and none at 0.9, so the drafted spec would have been inconclusive by construction. At λ = 0.3 it found candidates in 20, 20 and 19 of 20 networks at densities 0.5, 0.6 and 0.7. C1 and C2 were available for every candidate, and C3 with an exact match for 50–75% of them, hence the within-one rule.
- **Thresholds.** λ = 0.3 and densities 0.5–0.7, from the pilot. γ is calibrated from the null, not fixed. The accuracy cut-offs (0.95 for success, 0.80 for failure) and the 80% resolution requirement stand as drafted: they are set by what would count as evidence, not by the pilot. Sample sizes were reduced to a feasible run, and the readout was changed from a distance over joint states to per-component differences, so that it can resolve differences at those sizes.
- **Forbidden structure.** Reviewed; no smuggled structure found. Two clarifications were added: a constraint is a table of admissible patterns, and "even" and "odd" only describe that table; a three-member constraint is a mutual constraint among relations, which Relation earns.
- **Substrate.** Parity tables are kept for v1, because they make descent exactly decidable before any run. A substrate without that property (general pattern tables, with descent decided by enumeration) belongs in a later module or version.
- **Module number.** The register entry for EE-H-0060 cites "App G, module 5", and Book I Beta has no Appendix G. This module takes the number 5; the reference should read "Computational Companion, module 05" in the next edition.
- **Derived cases** are neither addressable nor registering. They are left out of accuracy and count as unresolved.
- **Independent review.** Before the freeze, a separate reviewer checked the draft against Closure and the guardrails. It confirmed the descent test and the positive-control guarantee, and found no smuggled structure. It raised sixteen items, all addressed in this version. The main ones: the candidate's own boundary constraints also couple it to the network, so descent is now judged on all of its external relations (coupling arms remove B(V); the natural arm computes the descent of B(V)); the fifth-diagnostic comparison with controls bears on EE-C-0097, not on EE-H-0060, and is reported separately; γ is calibrated per readout and arm; non-descending pairs are drawn so the tested difference is present; the seed streams are fully specified; and the verdict has a strict order.
