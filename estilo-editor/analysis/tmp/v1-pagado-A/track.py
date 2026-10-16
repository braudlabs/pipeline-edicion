#!/usr/bin/env python3
"""track.py fA fB R x,y [x,y ...]: sigue parches (NCC, plantilla 72 px) de fA a fB y compara distancias entre pares."""
import sys, itertools, math
import numpy as np
from tools import frames
fa, fb, R = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
P = [tuple(int(v) for v in s.split(",")) for s in sys.argv[4:]]
A = frames(fa, fa)[0].astype(np.float32).mean(axis=2); B = frames(fb, fb)[0].astype(np.float32).mean(axis=2)
T = 36
out = []
for (x, y) in P:
    t = A[y - T:y + T, x - T:x + T]; t0 = t - t.mean(); tn = np.sqrt((t0 ** 2).sum())
    best = (-2, 0, 0); sc = {}
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            yy, xx = y + dy, x + dx
            if yy - T < 0 or xx - T < 0 or yy + T > B.shape[0] or xx + T > B.shape[1]: continue
            w = B[yy - T:yy + T, xx - T:xx + T]; w0 = w - w.mean()
            c = float((t0 * w0).sum() / (tn * np.sqrt((w0 ** 2).sum()) + 1e-6)); sc[(dx, dy)] = c
            if c > best[0]: best = (c, dx, dy)
    c, dx, dy = best
    # subpíxel
    def sub(k):
        l = sc.get((dx - 1, dy) if k == 0 else (dx, dy - 1)); r = sc.get((dx + 1, dy) if k == 0 else (dx, dy + 1))
        if l is None or r is None: return 0
        den = l - 2 * c + r
        return 0.5 * (l - r) / den if den < -1e-9 else 0
    out.append((x, y, x + dx + sub(0), y + dy + sub(1), c))
    print(f"({x},{y}) f{fa} -> ({out[-1][2]:.1f},{out[-1][3]:.1f}) f{fb}  ncc={c:.3f}  d=({dx + sub(0):+.1f},{dy + sub(1):+.1f})")
for i, j in itertools.combinations(range(len(out)), 2):
    a, b = out[i], out[j]
    d0 = math.dist(a[:2], b[:2]); d1 = math.dist(a[2:4], b[2:4])
    if d0 > 300: print(f"  par {a[:2]}-{b[:2]}: {d0:.1f} -> {d1:.1f}  razón {d1/d0:.4f}")
