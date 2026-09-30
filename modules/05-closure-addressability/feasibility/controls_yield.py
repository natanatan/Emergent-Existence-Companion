#!/usr/bin/env python3
"""Feasibility pilot, part 2: can the three matched controls be drawn?

Structure only; no diagnostic is computed.
"""
import numpy as np
from yield_ import network, incid, internal, leakage, gf2_rank, detect

LAM = 0.3


def states_ok(S, V):
    I = internal(S, V)
    rank = gf2_rank([S[j] for j in I], max(V) + 1) if I else 0
    return len(V) > rank


def connected_sample(S, inc, size, rng, tries=400):
    n = len(inc)
    for _ in range(tries):
        V = {int(rng.integers(n))}
        while len(V) < size:
            nb = sorted({k for i in V for j in inc[i] for k in S[j]} - V)
            if not nb:
                break
            V.add(int(rng.choice(nb)))
        if len(V) == size:
            yield V


def main():
    n = 60
    for dens in (0.5, 0.6, 0.7):
        tot = c1 = c2 = c3 = nets_ok = 0
        for seed in range(20):
            rng = np.random.default_rng(seed)
            S, b = network(n, int(dens * n), rng)
            inc = incid(S, n)
            cands = sorted(detect(S, inc, LAM), key=sorted)[:3]
            nets_ok += bool(cands)
            for V in cands:
                tot += 1
                size, nI = len(V), len(internal(S, V))
                r = [set(rng.choice(n, size, replace=False).tolist()) for _ in range(200)]
                c1 += any(states_ok(S, W) for W in r)
                conn = list(connected_sample(S, inc, size, rng))
                fail = [W for W in conn if leakage(S, inc, W) > LAM and states_ok(S, W)]
                c2 += bool(fail)
                c3 += any(len(internal(S, W)) == nI for W in fail)
        print(f"density {dens}: networks with candidates {nets_ok}/20, candidates {tot}, "
              f"C1 found {c1}, C2 found {c2}, C3 (same internal count) found {c3}")


if __name__ == "__main__":
    main()
