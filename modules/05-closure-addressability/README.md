# Module 05 · closure addressability

Tests EE-H-0060 against the frozen specification in [`SPEC.md`](SPEC.md) (v1, merge commit `091e8f4`).

## Run it

```
pip install numpy
cd modules/05-closure-addressability
python tests/test_model.py      # checks on the model itself
python run.py --smoke           # a few networks, about a minute: checks the code, not a result
python run.py                   # the full run the spec fixes, about 15 hours on 4 cores
```

Each run writes `runs/<smoke|full>/`:
- `summary.json`: the outcome counts, accuracy, positive controls, P3a and the ablation.
- `gamma.json`: the null calibration.
- `cases.json`: every case.

## Status

The smoke test of v1 ([`runs/smoke/SMOKE.md`](runs/smoke/SMOKE.md)) found design problems in v1: the natural arm has no positive control, and it can score dissolution as addressability. **The full v1 run is on hold pending spec v2.**
