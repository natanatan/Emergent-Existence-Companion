"""Checks on the model itself. Run: python -m pytest tests  (or python tests/test_model.py)"""
import itertools
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.dynamics import Compiled, simulate  # noqa: E402
from model.gf2 import System, parity  # noqa: E402
from model.network import generate  # noqa: E402


def test_descent_matches_enumeration():
    """W's parity is constant on the solutions exactly when W is in the row space."""
    rng = np.random.default_rng(1)
    for _ in range(30):
        k = 7
        rows = [(int(rng.integers(1, 2 ** k)), int(rng.integers(2))) for _ in range(3)]
        sy = System(k, rows)
        if not sy.consistent:
            continue
        sols = [x for x in range(2 ** k) if all(parity(x & m) == r for m, r in rows)]
        for W in range(1, 2 ** k):
            constant = len({parity(x & W) for x in sols}) == 1
            assert constant == sy.in_rowspace(W)


def test_sampler_hits_only_solutions():
    rng = np.random.default_rng(2)
    rows = [(0b0111, 1), (0b1100, 0)]
    sy = System(4, rows)
    for _ in range(200):
        x = sy.sample(rng)
        assert all(parity(x & m) == r for m, r in rows)


def test_encodings_identical():
    """R4: parity and table encodings give identical trajectories under one stream."""
    net = generate(30, 20, np.random.default_rng(3))
    c = Compiled(net.n, net.S, net.b, [True] * len(net.S))
    init = np.random.default_rng(4).integers(0, 2, net.n)
    A = simulate(c, init, 500, 0.02, np.random.default_rng(5), 8, "parity")
    B = simulate(c, init, 500, 0.02, np.random.default_rng(5), 8, "table")
    assert (A == B).all()


def test_rule_treats_members_alike():
    """Permuting a constraint's members changes nothing."""
    net = generate(30, 20, np.random.default_rng(6))
    perm = [tuple(np.random.default_rng(j).permutation(s)) for j, s in enumerate(net.S)]
    init = np.random.default_rng(7).integers(0, 2, net.n)
    A = simulate(Compiled(net.n, net.S, net.b, [True] * 20), init, 400, 0.0, np.random.default_rng(8), 4)
    B = simulate(Compiled(net.n, perm, net.b, [True] * 20), init, 400, 0.0, np.random.default_rng(8), 4)
    assert (A == B).all()


def test_rule_never_reads_step_count():
    """The step loop exposes no counter to the rule (a structural check on the source)."""
    import inspect
    from model import dynamics
    src = inspect.getsource(dynamics.simulate)
    assert "enumerate(range(steps))" not in src and "for _ in range(steps)" in src


if __name__ == "__main__":
    for name, f in list(globals().items()):
        if name.startswith("test_"):
            f()
            print("ok", name)
