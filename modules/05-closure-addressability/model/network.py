"""Networks, candidate domains and the closure detector (spec: Generative
rule, Initial conditions). The generator plants nothing."""
import numpy as np

from .gf2 import System


class Network:
    def __init__(self, n, S, b):
        self.n = n
        self.S = [tuple(int(v) for v in s) for s in S]
        self.b = [int(x) for x in b]
        self.inc = [[] for _ in range(n)]
        for j, s in enumerate(self.S):
            for i in s:
                self.inc[i].append(j)


def generate(n, m, rng):
    S = [rng.choice(n, 3, replace=False) for _ in range(m)]
    b = rng.integers(0, 2, m)
    return Network(n, S, b)


def internal(net, V):
    return [j for j, s in enumerate(net.S) if set(s) <= V]


def boundary(net, V):
    return sorted({j for i in V for j in net.inc[i] if not set(net.S[j]) <= V})


def leakage(net, V):
    tot = sum(len(net.inc[i]) for i in V)
    out = sum(1 for i in V for j in net.inc[i] if not set(net.S[j]) <= V)
    return out / tot if tot else 1.0


def local(V):
    order = sorted(V)
    return order, {v: k for k, v in enumerate(order)}


def system(net, V):
    """The internal parity system of V, over V's members in sorted order."""
    order, idx = local(V)
    rows = []
    for j in internal(net, V):
        m = 0
        for i in net.S[j]:
            m |= 1 << idx[i]
        rows.append((m, net.b[j]))
    return System(len(order), rows)


def usable(net, V):
    """|S_F(V)| >= 2: consistent, and more members than independent rows."""
    sy = system(net, V)
    return sy.consistent and len(V) > sy.rank


def is_closed(net, V, lam):
    I = internal(net, V)
    if not I or leakage(net, V) > lam:
        return False
    sy = system(net, V)
    return sy.independent and sy.consistent and len(V) > sy.rank


def detect(net, lam, rng, vmin=6, vmax=16):
    found = set()
    for j in range(len(net.S)):
        V = set(net.S[j])
        while True:
            cur = leakage(net, V)
            opts = []
            for k in {k for i in V for k in net.inc[i] if not set(net.S[k]) <= V}:
                W = V | set(net.S[k])
                if len(W) <= vmax:
                    opts.append((leakage(net, W), k, W))
            better = [o for o in opts if o[0] < cur]
            if not better:
                break
            best = min(o[0] for o in better)
            ties = sorted((o for o in better if o[0] == best), key=lambda o: o[1])
            V = ties[int(rng.integers(len(ties)))][2]
        if vmin <= len(V) <= vmax and is_closed(net, V, lam):
            found.add(frozenset(V))
    return sorted(found, key=sorted)
