"""The admissible succession rule U, vectorized over independent runs.

One step, per run: choose a relation i uniformly; find the values that
satisfy every active constraint containing i; if exactly one qualifies take
it, otherwise take a uniformly random value. The rule reads only the current
state: never the step count, a position, a weight or an earlier state.

Two encodings of the same constraints (representation check R4):
  "parity": a constraint admits a pattern when the pattern's parity equals b
  "table":  a constraint is a table of admissible patterns
Under the same random stream they must give identical trajectories.
"""
import numpy as np


class Compiled:
    """Constraints padded to arity 4 over n_real relations plus one dummy
    relation (index n_real, always 0). Constraint index M is a dummy that is
    inactive, used to pad incidence lists."""

    def __init__(self, n_real, constraints, types, active):
        M = len(constraints)
        self.n = n_real
        self.dummy = n_real
        self.members = np.full((M + 1, 4), n_real, dtype=np.int64)
        self.arity = np.zeros(M + 1, dtype=np.int64)
        for j, s in enumerate(constraints):
            self.members[j, :len(s)] = s
            self.arity[j] = len(s)
        self.b = np.zeros(M + 1, dtype=np.int64)
        self.b[:M] = types
        self.active = np.zeros(M + 1, dtype=bool)
        self.active[:M] = active
        inc = [[] for _ in range(n_real)]
        for j, s in enumerate(constraints):
            for i in s:
                inc[i].append(j)
        k = max(1, max(len(x) for x in inc))
        self.inc = np.full((n_real, k), M, dtype=np.int64)
        for i, js in enumerate(inc):
            self.inc[i, :len(js)] = js
        # admissible-pattern tables, for the "table" encoding
        self.table = np.zeros((M + 1, 16), dtype=bool)
        for j in range(M + 1):
            for p in range(16):
                bits = [(p >> t) & 1 for t in range(4)]
                pad_ok = all(bits[t] == 0 for t in range(self.arity[j], 4))
                self.table[j, p] = pad_ok and (sum(bits) & 1) == self.b[j]
        self.weights = np.array([1, 2, 4, 8], dtype=np.int64)


def simulate(c, init, steps, eta, rng, R, encoding="parity"):
    X = np.tile(np.append(init, 0).astype(np.int64), (R, 1))
    rows = np.arange(R)
    for _ in range(steps):
        i = rng.integers(c.n, size=R)
        coin = rng.integers(2, size=R)
        flip = rng.random(R) < eta
        fj = rng.integers(c.n, size=R)
        J = c.inc[i]                                   # (R, k)
        mem = c.members[J]                             # (R, k, 4)
        vals = X[rows[:, None, None], mem]             # (R, k, 4)
        isi = mem == i[:, None, None]
        act = c.active[J]
        ok = []
        for v in (0, 1):
            vv = np.where(isi, v, vals)
            if encoding == "parity":
                sat = (vv.sum(-1) & 1) == c.b[J]
            else:
                sat = c.table[J, (vv * c.weights).sum(-1)]
            ok.append(np.all(sat | ~act, axis=1))
        new = np.where(ok[0] & ~ok[1], 0, np.where(ok[1] & ~ok[0], 1, coin))
        X[rows, i] = new
        X[rows[flip], fj[flip]] ^= 1
    return X[:, :c.n]
