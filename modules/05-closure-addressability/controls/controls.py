"""Matched controls (spec: Control). Each has the candidate's size and
|S_F(V)| >= 2. C2 and C3 fail the closure test."""
from model.network import internal, is_closed, leakage, usable

DRAWS = 2000


def _connected(net, size, rng):
    V = {int(rng.integers(net.n))}
    while len(V) < size:
        nb = sorted({k for i in V for j in net.inc[i] for k in net.S[j]} - V)
        if not nb:
            return None
        V.add(int(nb[int(rng.integers(len(nb)))]))
    return V


def c1(net, size, lam, rng):
    for _ in range(DRAWS):
        V = {int(v) for v in rng.choice(net.n, size, replace=False)}
        if usable(net, V):
            return V, {}
    return None, {}


def c2(net, size, lam, rng):
    for _ in range(DRAWS):
        V = _connected(net, size, rng)
        if V and not is_closed(net, V, lam) and usable(net, V):
            return V, {}
    return None, {}


def c3(net, size, n_internal, lam, rng):
    near = None
    for _ in range(DRAWS):
        V = _connected(net, size, rng)
        if not V or is_closed(net, V, lam) or not usable(net, V):
            continue
        k = len(internal(net, V))
        if k == n_internal:
            return V, {"internal_match": "exact"}
        if near is None and abs(k - n_internal) == 1:
            near = V
    if near is not None:
        return near, {"internal_match": "within one"}
    return None, {}
