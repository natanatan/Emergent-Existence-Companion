# Module 05 · closure-addressability · spec v1

**Draft for review. Not frozen.** Review against Closure, 6.4, 6.6, 6.7, 6.12 and 6.17. When the review is done, commit and tag `05-closure-addressability/spec-v1`. Nothing in `model/`, `controls/` or `runs/` is written before that tag. Thresholds marked *proposed* are the reviewer's to confirm or change before the freeze, never after.

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

**Constraints.** M constraints. Constraint j has a member set S_j of three relations, drawn uniformly without replacement and independently of every other constraint. It admits exactly the patterns on S_j that contain an even number of 1s, or, if its type b_j = 1, an odd number (b_j drawn uniformly). A constraint's admissible set is unchanged by any permutation of its members, so no member plays a distinct role. Nothing in the generator plants groups, modules or communities.

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

- **Networks.** N = 60. The density M/N is 0.5, 0.7 or 0.9. There are 100 networks per density, with network seeds 1–300.
- **Candidate detector.** The detector is external and uses no target. From each constraint as a seed, it grows V greedily: at each step it adds the member set of the boundary constraint that most reduces leakage (below), stopping at |V| = 16 or when no addition reduces leakage. It keeps every V with 6 ≤ |V| ≤ 16 that passes the closure test:
  - **Sufficiency (6.4):** leakage L(V) ≤ λ. L(V) is the fraction of member–constraint incidences (i ∈ V, j ∋ i) whose constraint lies outside V. *Proposed λ = 0.2.*
  - **Participation (6.4):** every internal constraint is non-redundant, so removing it enlarges 𝒮F(V). Equivalently, the rows of I(V) are independent over GF(2).
  - **Realizability (6.6):** 𝒮F(V) ≠ ∅. Addressability also needs at least two microstates, so |𝒮F(V)| ≥ 2. That is a requirement of this test, not of closure.

  Duplicates are removed. Up to 5 candidates per network are selected at random (seeded).
- **Microstates.** Pairs Σa ≠ Σb are drawn uniformly from 𝒮F(V), by sampling uniformly from the solutions of the internal parity system. The state of every relation outside V is drawn uniformly once per pair and is shared by a and b.

## Control

The fifth diagnostic of 6.17 has three matched controls. Each is drawn from the same network with the same |V|, and each is required to have |𝒮F(V)| ≥ 2:

| Control | Matched on | Differs by |
| --- | --- | --- |
| C1 random | Size | V drawn uniformly |
| C2 merely connected | Size, and connected through shared constraints | Fails the closure test |
| C3 equally dense | Size and number of internal constraints | Fails the closure test |

These are the fair comparison because they separate closure from its look-alikes: size, connectedness and internal density. Chapter 6 argues that none of these is closure (6.4, 6.18).

## Diagnostic

**External couplings E.** Each coupling adds constraints that link a subset W ⊆ V (1 ≤ |W| ≤ 3) to one or two fresh external relations Y. There are three kinds:

- **Descending:** W is chosen so that its parity is constant on 𝒮F(V), meaning its indicator lies in the row space of I(V) over GF(2). Then E(Σa) and E(Σb) see the same thing for every Σa ~F Σb. This is the descent condition of 6.12.
- **Non-descending:** W is chosen so that its parity varies on 𝒮F(V).
- **Natural:** the candidate's own boundary constraints B(V), with the relations they reach outside V as Y. No coupling is added.

Whether a coupling descends is computed by linear algebra, before any run.

**Run length.** Every run lasts T = 50·|V ∪ Y| succession steps. T is an external readout; the rule never reads it.

**Addressability gap.** From R = 200 runs per microstate, estimate the distributions P_a and P_b of a readout (defined under Readout resolution). Then:

- D_ab = total-variation distance between P_a and P_b.
- The noise floor D_aa is the same distance between two independent batches of R runs from Σa.
- For a candidate and coupling, the gap is G = mean over 20 pairs of (D_ab − D_aa).
- The gap **registers** when G > γ, where γ is calibrated from the null (below).

## Readout resolution

Each diagnostic declares what its readout can register and carries a positive control, a case whose effect is known to exist and which must register at that resolution. A null result is then one of three outcomes, and `RESULT.md` says which applies to every null:

- **Absent:** the positive control registers, and the tested case does not.
- **Derived:** the tested case registers only through another relation, or only at another level of readout.
- **Unresolved:** the positive control does not register, so the readout cannot decide.

Only "absent" counts as evidence that a relation does not participate, or that two microstates are the same.

### The addressability gap

- **Readout levels.**
  - **L1, the coupled readout:** o = (whether F holds on V, the state of Y). This is the readout the verdict uses.
  - **L2, other relations:** the state of every relation outside V ∪ Y.

  The microstate of V itself is never a readout. Σa and Σb differ there by construction, and 6.12 says that lower-order multiplicity does not disappear; it becomes irrelevant to the coupling.
- **Resolution, the noise floor.** γ is calibrated from the null before any verdict is computed. For each candidate and coupling, the null gap G₀ is the same statistic as G, computed with three independent batches of R runs all started from the same Σa. γ is the 95th percentile of G₀ over all cases at that density. A gap at or below γ cannot be told apart from run-to-run noise.
- **Positive control.** Each candidate, and each control, gets one known non-descending coupling: W = {w}, a single member of V that is not constant on 𝒮F(V). Its 20 pairs are drawn so that Σa and Σb differ at w. Its gap must exceed γ at L1. If it does not, every gap for that candidate is **Unresolved**. The positive-control coupling is not counted among the 10 non-descending couplings.
- **Outcomes.** For each case:
  - **Registers:** G > γ at L1.
  - **Absent:** G ≤ γ at L1, and the positive control registered.
  - **Derived:** G ≤ γ at L1, but the gap computed on L2 exceeds γ.
  - **Unresolved:** the candidate's positive control did not register.

  A case is **addressable** only if it is Absent.

### The participation ablation

This is a secondary readout, the second diagnostic of 6.17.

- **Readout.** F-persistence is the fraction of runs, at η = 0.01, in which F holds on V at T. To ablate a constraint, it is removed from the rule's C(i) for every member, while F is still judged on the full I(V).
- **Resolution.** The change in F-persistence must exceed the 95th percentile of the change between two unablated batches.
- **Positive control.** One internal constraint of V is ablated. It is constitutive of F by definition, so its ablation must register a drop in F-persistence. If it does not, the ablation readout for that candidate is **Unresolved**.
- **Tested cases.** Each boundary constraint in B(V) is ablated in turn. These are the relations the closure test classes as non-constitutive.
  - **Absent:** the boundary constraint does not participate.
  - **Registers:** it participates. That is a constitutive dependency outside V, and it is reported against sufficiency (6.4).
  - **Derived:** it registers only through another relation, that is, only on L2.

## Predictions and verdict

Accuracy and P3 are computed on resolved cases only. The rates of Unresolved and Derived cases are reported for every arm and density.

- **P1 (if):** descending couplings are Absent.
- **P2 (only if):** non-descending couplings Register.
- **Accuracy** is the fraction of cases, among those that are Absent or Register, in which descent predicts the outcome. There are 10 descending and 10 non-descending couplings per candidate.
- **P3 (nontrivial class):** under natural couplings, closed candidates are addressable (Absent) more often than each control. This is measured as the difference in the fraction addressable, with a network-level bootstrap 95% interval (10,000 resamples).

**Success:** all of the following hold at η = 0 and η = 0.01. *Proposed thresholds.*

- Accuracy is at least 0.95.
- For each control, the P3 interval lies entirely above 0.
- Unresolved and Derived cases together are no more than 20% of the cases in the P1 set, in the P2 set, and in each P3 arm.

**Secondary readouts.** These are reported but do not decide the verdict: leakage; the participation ablation above; and closure robustness (the fraction of runs under 𝔗C in which F holds at T). These are the remaining three diagnostics of 6.17.

## Failure criterion

Either of these counts against the hypothesis, provided the readout was resolved in at least 80% of cases:

- Accuracy < 0.80 at either η. Descent then does not track addressability, in one direction or both. The RESULT reports which of P1 or P2 failed.
- For any control, the P3 interval lies entirely below 0.05. The closure criterion then picks out nothing that the look-alike controls do not.

The verdict is **Inconclusive** in either of these cases, and the RESULT says which applied and by how much:

- More than 20% of cases in any set are Unresolved or Derived. The readout could not decide often enough for a verdict.
- The result lies between the success and failure criteria.

## Runs

- 3 densities × 100 networks, with up to 5 candidates each, and for each candidate its three controls.
- Per candidate or control: 1 positive-control coupling, 10 descending, 10 non-descending and 1 natural coupling; 20 microstate pairs per coupling; R = 200 runs per microstate; η ∈ {0, 0.01}.
- Seeds are derived deterministically from (network seed, candidate index, coupling index, pair index, run index), so every run can be reproduced on its own.
- Null gaps G₀ and the resulting γ per density are computed and recorded before any gap G is compared with them.
- Variation is reported as medians and interquartile ranges across networks, with bootstrap intervals at network level.
- Accuracy is also reported separately by density, by |W| and by |V|, so a pooled pass cannot hide a failing regime.

## Representation checks

The verdict must be the same under each of these. Per-case addressability must also agree in at least 98% of cases, allowing for sampling noise.

| Check | Change | Why it should not matter |
| --- | --- | --- |
| R1 | Relabel the relations by a random permutation | Names carry no structure |
| R2 | Exchange the values 0 and 1 everywhere, adjusting each constraint's type | Which value is called 0 is a convention |
| R3 | Replace uniform choice of i by random-order sweeps, with each relation once per sweep | Both are admissible schedules with no privileged order |
| R4 | Encode constraints as explicit tables of admissible patterns instead of the parity rule | Same constraints, different encoding. Trajectories must be identical under the same seeds |

If a check changes the verdict, the result is reported as Inconclusive with the check named (Formalism, 9.28, diagnostic 1).

## Freeze

`05-closure-addressability/spec-v1`. Not yet tagged.

- **Book exports:** `natanatan/Emergent-Existence@fe713e6`
