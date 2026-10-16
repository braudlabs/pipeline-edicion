#!/usr/bin/env python3
"""chain.py fA fB R x,y [x,y...]: sigue parches fotograma a fotograma (NCC, plantilla 64, se actualiza) e imprime trayectorias y razón de distancias."""
import sys, itertools, math
import numpy as np
from tools import frames
fa, fb, R = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
P = [[float(v) for v in s.split(",")] for s in sys.argv[4:]]
fr = [im.astype(np.float32).mean(axis=2) for im in frames(fa, fb)]
T = 32
traj = [[tuple(p)] for p in P]
nccs = [[] for _ in P]
for k in range(1, len(fr)):
    A, B = fr[k - 1], fr[k]
    for i, tr in enumerate(traj):
        x, y = [int(round(v)) for v in tr[-1]]
        if y - T < 0 or x - T < 0 or y + T > A.shape[0] or x + T > A.shape[1]:
            tr.append(tr[-1]); nccs[i].append(0); continue
        t = A[y - T:y + T, x - T:x + T]; t0 = t - t.mean(); tn = np.sqrt((t0 ** 2).sum()) + 1e-6
        best = (-2, 0, 0); sc = {}
        for dy in range(-R, R + 1):
            for dx in range(-R, R + 1):
                yy, xx = y + dy, x + dx
                if yy - T < 0 or xx - T < 0 or yy + T > B.shape[0] or xx + T > B.shape[1]: continue
                w = B[yy - T:yy + T, xx - T:xx + T]; w0 = w - w.mean()
                c = float((t0 * w0).sum() / (tn * (np.sqrt((w0 ** 2).sum()) + 1e-6))); sc[(dx, dy)] = c
                if c > best[0]: best = (c, dx, dy)
        c, dx, dy = best
        def sub(ax):
            l = sc.get((dx - 1, dy) if ax == 0 else (dx, dy - 1)); r = sc.get((dx + 1, dy) if ax == 0 else (dx, dy + 1))
            if l is None or r is None: return 0
            den = l - 2 * c + r
            return 0.5 * (l - r) / den if den < -1e-9 else 0
        tr.append((tr[-1][0] + dx + sub(0), tr[-1][1] + dy + sub(1))); nccs[i].append(c)
for k in range(len(fr)):
    line = f"f{fa+k}\t" + "\t".join(f"({tr[k][0]:.1f},{tr[k][1]:.1f})" + (f" n{nccs[i][k-1]:.2f}" if k else "") for i, tr in enumerate(traj))
    ds = []
    for i, j in itertools.combinations(range(len(traj)), 2):
        d0 = math.dist(traj[i][0], traj[j][0])
        if d0 > 300: ds.append(math.dist(traj[i][k], traj[j][k]) / d0)
    print(line + "\t| razones: " + " ".join(f"{v:.4f}" for v in ds))
