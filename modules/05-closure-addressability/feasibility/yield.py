#!/usr/bin/env python3
"""Feasibility pilot for spec v1: detector yield and run cost only.

Run before the freeze to set sample sizes. It generates networks, runs the
closure detector and the control samplers, and times the update rule. It
computes no diagnostic: no gap, no ablation, no robustness, nothing that
bears on EE-H-0060.
"""
import itertools
import sys
import time

import numpy as np


def network(n, m, rng):
    S = np.array([rng.choice(n, 3, replace=False) for _ in range(m)])
    b = rng.integers(0, 2, m)
    return S, b


def incid(S, n):
    inc = [[] for _ in range(n)]
    for j, s in enumerate(S):
        for i in s:
            inc[i].append(j)
    return inc


def internal(S, V):
    return [j for j, s in enumerate(S) if set(s) <= V]


def leakage(S, inc, V):
    tot = sum(len(inc[i]) for i in V)
    out = sum(1 for i in V for j in inc[i] if not set(S[j]) <= V)
    return out / tot if tot else 1.0


def gf2_rank(rows, n):
    M = np.zeros((len(rows), n), dtype=np.uint8)
    for r, cols in enumerate(rows):
        M[r, list(cols)] = 1
    rank, col = 0, 0
    M = M.copy()
    for col in range(n):
        piv = next((r for r in range(rank, len(M)) if M[r, col]), None)
        if piv is None:
            continue
        M[[rank, piv]] = M[[piv, rank]]
        for r in range(len(M)):
            if r != rank and M[r, col]:
                M[r] ^= M[rank]
        rank += 1
    return rank


def closed(S, inc, V, lam):
    I = internal(S, V)
    if not I or leakage(S, inc, V) > lam:
        return False
    rank = gf2_rank([S[j] for j in I], max(V) + 1)
    # participation: rows independent; realizability with >= 2 states: |V| > rank
    return rank == len(I) and len(V) > rank   # parity systems with independent rows are always solvable


def detect(S, inc, lam, vmin=6, vmax=16):
    found = set()
    for j in range(len(S)):
        V = set(S[j])
        while True:
            best, bestL = None, leakage(S, inc, V)
            for k in {k for i in V for k in inc[i] if not set(S[k]) <= V}:
                W = V | set(S[k])
                if len(W) <= vmax:
                    L = leakage(S, inc, W)
                    if L < bestL:
                        best, bestL = W, L
            if best is None:
                break
            V = best
        if vmin <= len(V) <= vmax and closed(S, inc, V, lam):
            found.add(frozenset(V))
    return found


def run_cost(S, b, n, steps, rng):
    inc = incid(S, n)
    x = rng.integers(0, 2, n)
    t0 = time.perf_counter()
    for _ in range(steps):
        i = rng.integers(n)
        ok = []
        for v in (0, 1):
            x[i] = v
            if all((x[S[j]].sum() & 1) == b[j] for j in inc[i]):
                ok.append(v)
        x[i] = ok[0] if len(ok) == 1 else rng.integers(2)
    return (time.perf_counter() - t0) / steps


def main():
    n, nets = 60, int(sys.argv[1]) if len(sys.argv) > 1 else 20
    for dens in (0.5, 0.7, 0.9, 1.2, 1.5):
        for lam in (0.2, 0.3, 0.4):
            counts, sizes = [], []
            for seed in range(nets):
                rng = np.random.default_rng(seed)
                S, b = network(n, int(dens * n), rng)
                f = detect(S, incid(S, n), lam)
                counts.append(len(f))
                sizes += [len(v) for v in f]
            has = sum(c > 0 for c in counts)
            print(f"density {dens} lambda {lam}: networks with a candidate {has}/{nets}, "
                  f"median candidates {int(np.median(counts))}, sizes {sorted(set(sizes))[:8]}")
    rng = np.random.default_rng(0)
    S, b = network(n, 42, rng)
    print(f"python rule: {run_cost(S, b, n, 20000, rng)*1e6:.1f} microseconds per step")


if __name__ == "__main__":
    main()
