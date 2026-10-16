#!/usr/bin/env python3
"""Movimiento global (escala + traslación) del fondo entre un fotograma de referencia y los demás.
  mot.py REF A B [--step 1] [--excl x0,y0,x1,y1 ...] [--half 40] [--search 10] [--grid 12x20]
Empareja parches por SSD (con refinado subpíxel parabólico) y ajusta por mínimos cuadrados robustos
  dx = tx + (s-1)(x-540),  dy = ty + (s-1)(y-960).
"""
import argparse
import numpy as np
import fr

def gray(a):
    return a.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)

def shift(A, B, x, y, half, search):
    pa = A[y - half:y + half, x - half:x + half]
    if pa.std() < 6:
        return None
    pa = (pa - pa.mean()) / (pa.std() + 1e-6)
    best = None; E = np.full((2 * search + 1, 2 * search + 1), np.inf, np.float32)
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            pb = B[y + dy - half:y + dy + half, x + dx - half:x + dx + half]
            if pb.shape != pa.shape:
                continue
            pbm = (pb - pb.mean()) / (pb.std() + 1e-6)
            E[dy + search, dx + search] = ((pa - pbm) ** 2).mean()
    iy, ix = np.unravel_index(np.argmin(E), E.shape)
    if iy in (0, 2 * search) or ix in (0, 2 * search):
        return None
    def sub(m1, c, p1):
        d = m1 - 2 * c + p1
        return 0.0 if d == 0 else 0.5 * (m1 - p1) / d
    oy = sub(E[iy - 1, ix], E[iy, ix], E[iy + 1, ix]); ox = sub(E[iy, ix - 1], E[iy, ix], E[iy, ix + 1])
    return ix - search + ox, iy - search + oy, float(E[iy, ix]) / (float((pa ** 2).mean()) + 1e-6)

def fit(P):
    P = np.array(P)  # x, y, dx, dy
    keep = np.ones(len(P), bool)
    for _ in range(4):
        Q = P[keep]
        X = np.zeros((2 * len(Q), 3)); Y = np.zeros(2 * len(Q))
        X[0::2, 0] = 1; X[0::2, 2] = Q[:, 0] - 540; Y[0::2] = Q[:, 2]
        X[1::2, 1] = 1; X[1::2, 2] = Q[:, 1] - 960; Y[1::2] = Q[:, 3]
        sol, *_ = np.linalg.lstsq(X, Y, rcond=None)
        rx = P[:, 2] - (sol[0] + sol[2] * (P[:, 0] - 540)); ry = P[:, 3] - (sol[1] + sol[2] * (P[:, 1] - 960))
        r = np.hypot(rx, ry)
        thr = max(0.6, 2.5 * np.median(r[keep]))
        keep = r < thr
        if keep.sum() < 8:
            break
    return sol, int(keep.sum()), float(np.median(r[keep])) if keep.any() else float("nan")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("ref", type=int); ap.add_argument("a", type=int); ap.add_argument("b", type=int)
    ap.add_argument("--step", type=int, default=1)
    ap.add_argument("--excl", nargs="*", default=[])
    ap.add_argument("--half", type=int, default=40)
    ap.add_argument("--search", type=int, default=10)
    ap.add_argument("--nx", type=int, default=9); ap.add_argument("--ny", type=int, default=15)
    a = ap.parse_args()
    lo, hi = min(a.ref, a.a), max(a.ref, a.b)
    F = fr.frames(lo, hi)
    R = gray(F[a.ref])
    ex = [[int(v) for v in e.split(",")] for e in a.excl]
    m = a.half + a.search + 2
    pts = [(int(x), int(y)) for y in np.linspace(m, 1920 - m, a.ny) for x in np.linspace(m, 1080 - m, a.nx)]
    pts = [(x, y) for x, y in pts if not any(e[0] - a.half <= x <= e[2] + a.half and e[1] - a.half <= y <= e[3] + a.half for e in ex)]
    print("f\tescala\ttx\ty\tn_ok/n\tresid_px")
    for f in range(a.a, a.b + 1, a.step):
        B = gray(F[f]); P = []
        for x, y in pts:
            s = shift(R, B, x, y, a.half, a.search)
            if s and s[2] < 0.5:
                P.append((x, y, s[0], s[1]))
        if len(P) < 10:
            print(f, "pocos puntos", len(P)); continue
        sol, n, res = fit(P)
        print(f"{f}\t{1 + sol[2]:.5f}\t{sol[0]:+.2f}\t{sol[1]:+.2f}\t{n}/{len(P)}\t{res:.2f}")
