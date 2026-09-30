#!/usr/bin/env python3
"""Module 05 · closure addressability · the run (spec v1).

  python run.py --smoke     a few networks, to check the code; not a result
  python run.py             the full run the spec fixes

Writes runs/<smoke|full>/: cases.json (every case), gamma.json (null
calibration, fixed before any gap is compared), summary.json.
"""
import argparse
import itertools
import json
import os
import sys
import time
import zlib
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from controls.controls import c1, c2, c3  # noqa: E402
from model.dynamics import Compiled, simulate  # noqa: E402
from model.gf2 import parity  # noqa: E402
from model.network import boundary, detect, generate, internal, local, system  # noqa: E402

N, LAM = 60, 0.3
FULL = dict(densities=[0.5, 0.6, 0.7], nets=40, cands=3, n_desc=5, n_nd=5, pairs=10, R=100,
            etas=[0.0, 0.01], sweeps=20, abl_states=10, abl_R=100)
SMOKE = dict(densities=[0.5, 0.7], nets=2, cands=1, n_desc=2, n_nd=2, pairs=4, R=50,
             etas=[0.0, 0.01], sweeps=20, abl_states=3, abl_R=50)
ARMS = ["candidate", "C1", "C2", "C3"]


def stream(*parts):
    """An independent random stream for every purpose (spec: Runs, Seeds)."""
    ints = [p if isinstance(p, int) else zlib.crc32(str(p).encode()) for p in parts]
    return np.random.default_rng(np.random.SeedSequence(ints))


def f_holds(X, net, V):
    I = internal(net, V)
    if not I:
        return np.ones(len(X), dtype=bool)
    S = np.array([net.S[j] for j in I])
    b = np.array([net.b[j] for j in I])
    return np.all((X[:, S].sum(-1) & 1) == b, axis=1)


def readout(X, net, V, rels):
    return np.concatenate([[f_holds(X, net, V).mean()], X[:, rels].mean(0) if rels else []])


def D(p, q):
    return float(np.max(np.abs(p - q))) if len(p) else 0.0


def domain_cases(V, net, cfg, key):
    """The cases of one domain: positive control, descending, non-descending, natural."""
    order, idx = local(V)
    sy = system(net, V)
    k = len(order)
    subsets = [sum(1 << t for t in c) for r in (1, 2, 3) for c in itertools.combinations(range(k), r)]
    desc = [m for m in subsets if sy.in_rowspace(m)]
    nondesc = {r: [sum(1 << t for t in c) for c in itertools.combinations(range(k), r)
                   if not sy.in_rowspace(sum(1 << t for t in c))] for r in (1, 2, 3)}
    cases = []
    rng = stream(*key, "W")
    if nondesc[1]:
        cases.append(("positive", nondesc[1][int(rng.integers(len(nondesc[1])))]))
    pick = rng.choice(len(desc), min(cfg["n_desc"], len(desc)), replace=False) if desc else []
    cases += [("descending", desc[int(i)]) for i in pick]
    used = set()
    for _ in range(cfg["n_nd"]):
        for _try in range(20):
            r = int(rng.integers(1, 4))
            pool = [m for m in nondesc[r] if m not in used]
            if pool:
                m = pool[int(rng.integers(len(pool)))]
                used.add(m)
                cases.append(("non-descending", m))
                break
    B = boundary(net, V)
    nat_desc = all(sy.in_rowspace(sum(1 << idx[i] for i in net.S[j] if i in V)) for j in B)
    cases.append(("natural", nat_desc))
    return order, sy, cases, B


def run_case(net, V, order, sy, kind, spec, B, cfg, eta, key):
    Vset = set(order)
    if kind == "natural":
        cons, types, active = net.S, net.b, [True] * len(net.S)
        n_real = net.n
        y = sorted({i for j in B for i in net.S[j]} - Vset)
        W = None
    else:
        W = [order[t] for t in range(len(order)) if (spec >> t) & 1]
        yv = net.n
        tr = stream(*key, "coupling-type")
        cons = net.S + [tuple(W) + (yv,)]
        types = net.b + [int(tr.integers(2))]
        Bset = set(B)
        active = [j not in Bset for j in range(len(net.S))] + [True]
        n_real = net.n + 1
        y = [yv]
    other = [i for i in range(n_real) if i not in Vset and i not in y]
    comp = Compiled(n_real, cons, types, active)
    steps = cfg["sweeps"] * n_real
    wmask = spec if kind != "natural" else 0
    res = {"L1": [], "L2": []}
    for p in range(cfg["pairs"]):
        pr = stream(*key, "pair", p)
        for _ in range(1000):
            a, b = sy.sample(pr), sy.sample(pr)
            if a != b and (kind not in ("positive", "non-descending") or parity(a & wmask) != parity(b & wmask)):
                break
        outside = pr.integers(0, 2, n_real)
        outs = {}
        for batch, sigma in (("a", a), ("b", b), ("a1", a), ("a2", a)):
            init = outside.copy()
            for t, v in enumerate(order):
                init[v] = (sigma >> t) & 1
            X = simulate(comp, init, steps, eta, stream(*key, "batch", p, batch, int(eta * 1000)), cfg["R"])
            outs[batch] = (readout(X, net, Vset, y), readout(X, net, Vset, other)[1:])
        for lvl, s in (("L1", 0), ("L2", 1)):
            A, Bq, A1, A2 = (outs[x][s] for x in ("a", "b", "a1", "a2"))
            res[lvl].append((D(A, Bq), D(A, A1), D(A, A2)))
    out = {"components": 1 + len(y)}
    for lvl in ("L1", "L2"):
        arr = np.array(res[lvl])
        out[lvl] = {"G": float(np.mean(arr[:, 0] - arr[:, 1])), "G0": float(np.mean(arr[:, 2] - arr[:, 1]))}
    return out


def ablation(net, V, B, cfg, key):
    """Participation ablation, natural arm, eta = 0.01 (secondary readout)."""
    order, _ = local(V)
    sy = system(net, V)
    I = internal(net, V)
    rng = stream(*key, "ablation")
    pos = I[int(rng.integers(len(I)))]
    steps = cfg["sweeps"] * net.n

    def persist(off, si, batch):
        st = states[si]
        active = [j != off for j in range(len(net.S))]
        comp = Compiled(net.n, net.S, net.b, active)
        X = simulate(comp, st, steps, 0.01, stream(*key, "ablation-batch", "none" if off < 0 else off, batch, si), cfg["abl_R"])
        return float(f_holds(X, net, set(order)).mean())

    states = []
    for s in range(cfg["abl_states"]):
        sr = stream(*key, "ablation-state", s)
        st = sr.integers(0, 2, net.n)
        x = sy.sample(sr)
        for t, v in enumerate(order):
            st[v] = (x >> t) & 1
        states.append(st)
    base = [(persist(-1, si, 1), persist(-1, si, 2)) for si in range(len(states))]
    null = [abs(p1 - p2) for p1, p2 in base]
    tested = {}
    for off in [pos] + B:
        d = [persist(off, si, 3) - base[si][0] for si in range(len(states))]
        tested[str(off)] = float(np.mean(d))
    return {"null": null, "positive": str(pos), "changes": tested}


def one_network(args):
    cfg, di, dens, k = args
    seed = di * cfg["nets"] + k + 1
    net = generate(N, int(dens * N), stream("network", seed))
    cands = detect(net, LAM, stream("detector", seed))
    sel = stream("select", seed)
    chosen = [cands[int(i)] for i in sel.choice(len(cands), min(cfg["cands"], len(cands)), replace=False)] if cands else []
    rows, abl = [], []
    for ci, V in enumerate(chosen):
        V = set(V)
        doms = {"candidate": (V, {})}
        doms["C1"] = c1(net, len(V), LAM, stream("control", seed, ci, "C1"))
        doms["C2"] = c2(net, len(V), LAM, stream("control", seed, ci, "C2"))
        doms["C3"] = c3(net, len(V), len(internal(net, V)), LAM, stream("control", seed, ci, "C3"))
        for arm in ARMS:
            D_, meta = doms[arm]
            if D_ is None:
                rows.append({"density": dens, "network": seed, "candidate": ci, "arm": arm, "missing": True})
                continue
            key = (seed, arm, ci)
            order, sy, cases, B = domain_cases(D_, net, cfg, key)
            for cix, (kind, spec) in enumerate(cases):
                descends = spec if kind == "natural" else kind == "descending"
                for eta in cfg["etas"]:
                    r = run_case(net, D_, order, sy, kind, spec, B, cfg, eta, key + (cix,))
                    rows.append({"density": dens, "network": seed, "candidate": ci, "arm": arm, "case": cix,
                                 "kind": kind, "descends": bool(descends), "eta": eta, "size": len(D_),
                                 "W": len([t for t in range(len(order)) if kind != "natural" and (spec >> t) & 1]),
                                 **meta, **r})
            if arm == "candidate":
                abl.append({"density": dens, "network": seed, "candidate": ci, **ablation(net, D_, B, cfg, key)})
    return rows, abl, len(cands)


def group_key(r, lvl):
    comp = r["components"]
    cb = "2-4" if comp <= 4 else "5-8" if comp <= 8 else "9-16" if comp <= 16 else ">16"
    return f"{r['density']}|{r['eta']}|{r['arm']}|{r['kind']}|{lvl}" + (f"|{cb}" if r["kind"] == "natural" else "")


def analyse(rows, abl):
    cases = [r for r in rows if not r.get("missing")]
    # 1. gamma from the null, per group, fixed before any G is compared
    groups = {}
    for r in cases:
        for lvl in ("L1", "L2"):
            groups.setdefault(group_key(r, lvl), []).append(r[lvl]["G0"])
    gamma = {g: float(np.percentile(v, 95)) for g, v in groups.items()}
    # 2. positive controls
    pc = {}
    for r in cases:
        if r["kind"] == "positive":
            pc[(r["network"], r["candidate"], r["arm"], r["eta"])] = r["L1"]["G"] > gamma[group_key(r, "L1")]
    # 3. outcomes, in order of precedence
    for r in cases:
        if r["kind"] == "positive":
            r["outcome"] = "positive control: " + ("registers" if pc[(r["network"], r["candidate"], r["arm"], r["eta"])] else "does not register")
            continue
        if not pc.get((r["network"], r["candidate"], r["arm"], r["eta"]), False):
            r["outcome"] = "Unresolved"
        elif r["L1"]["G"] > gamma[group_key(r, "L1")]:
            r["outcome"] = "Registers"
        elif r["L2"]["G"] > gamma.get(group_key(r, "L2"), float("inf")):
            r["outcome"] = "Derived"
        else:
            r["outcome"] = "Absent"
    # 4. EE-H-0060 on closed candidates
    summ = {}
    for eta in sorted({r["eta"] for r in cases}):
        cand = [r for r in cases if r["arm"] == "candidate" and r["eta"] == eta and r["kind"] != "positive"]
        p1 = [r for r in cand if r["descends"]]
        p2 = [r for r in cand if not r["descends"]]
        resolved = [r for r in cand if r["outcome"] in ("Absent", "Registers")]
        correct = [r for r in resolved if (r["outcome"] == "Absent") == r["descends"]]
        res = lambda s: (sum(r["outcome"] in ("Absent", "Registers") for r in s) / len(s)) if s else None
        summ[str(eta)] = {
            "P1 cases": len(p1), "P2 cases": len(p2),
            "P1 resolution": res(p1), "P2 resolution": res(p2),
            "accuracy": (len(correct) / len(resolved)) if resolved else None,
            "outcomes": {o: sum(r["outcome"] == o for r in cand) for o in ("Absent", "Registers", "Derived", "Unresolved")},
            "positive controls registering": {arm: f"{sum(v for (n, c, a, e), v in pc.items() if a == arm and e == eta)}"
                                              f"/{sum(1 for (n, c, a, e) in pc if a == arm and e == eta)}" for arm in ARMS},
            "by kind": {k: {o: sum(r["outcome"] == o for r in cand if r["kind"] == k)
                            for o in ("Absent", "Registers", "Derived", "Unresolved")}
                        for k in ("descending", "non-descending", "natural")},
        }
    # 5. natural descent by arm (P3a, analytic)
    p3a = {}
    for arm in ARMS:
        nat = [r for r in cases if r["arm"] == arm and r["kind"] == "natural" and r["eta"] == 0.0]
        p3a[arm] = f"{sum(r['descends'] for r in nat)}/{len(nat)}"
    # 6. ablation (secondary)
    nulls = [x for a in abl for x in a["null"]]
    thr = float(np.percentile(nulls, 95)) if nulls else None
    abl_s = {"threshold": thr,
             "positive controls registering": f"{sum(abs(a['changes'][a['positive']]) > thr for a in abl)}/{len(abl)}",
             "boundary constraints participating": f"{sum(abs(v) > thr for a in abl for k, v in a['changes'].items() if k != a['positive'])}"
                                                   f"/{sum(len(a['changes']) - 1 for a in abl)}"}
    return gamma, summ, p3a, abl_s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    a = ap.parse_args()
    cfg, name = (SMOKE, "smoke") if a.smoke else (FULL, "full")
    out = os.path.join(HERE, "runs", name)
    os.makedirs(out, exist_ok=True)
    t0 = time.time()
    jobs = [(cfg, di, d, k) for di, d in enumerate(cfg["densities"]) for k in range(cfg["nets"])]
    with Pool(a.workers) as pool:
        results = pool.map(one_network, jobs)
    rows = [r for x in results for r in x[0]]
    abl = [r for x in results for r in x[1]]
    ncands = [x[2] for x in results]
    gamma, summ, p3a, abl_s = analyse(rows, abl)
    with open(os.path.join(out, "gamma.json"), "w") as f:
        json.dump(gamma, f, indent=1, sort_keys=True)
    with open(os.path.join(out, "cases.json"), "w") as f:
        json.dump({"rows": rows, "ablation": abl}, f, indent=1)
    summary = {"config": cfg, "networks": len(jobs), "candidates found per network": ncands,
               "seconds": round(time.time() - t0, 1), "EE-H-0060 (candidates)": summ,
               "natural boundaries that descend (P3a)": p3a, "participation ablation": abl_s}
    with open(os.path.join(out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
