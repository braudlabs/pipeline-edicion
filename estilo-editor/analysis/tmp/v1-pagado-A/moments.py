#!/usr/bin/env python3
"""moments.py A B x0 y0 x1 y1 [lo hi]: momentos subpíxel de la tinta blanca (alfa suave) en una región px."""
import sys
import numpy as np
from tools import frames, drop_border
a, b = int(sys.argv[1]), int(sys.argv[2])
X0, Y0, X1, Y1 = [int(v) for v in sys.argv[3:7]]
lo = float(sys.argv[7]) if len(sys.argv) > 7 else 235
hi = float(sys.argv[8]) if len(sys.argv) > 8 else 253
print("f\tcx\tcy\tsx\tsy\tsx/sy\tmasa\tx0\tx1\ty0\ty1")
for k, im in enumerate(frames(a, b)):
    c = im[Y0:Y1, X0:X1].astype(np.float32).min(axis=2)
    al = np.clip((c - lo) / (hi - lo), 0, 1)
    hard = drop_border(al > 0)
    al = al * hard
    m = al.sum()
    if m < 20:
        print(f"{a+k}\t-"); continue
    ys, xs = np.mgrid[0:al.shape[0], 0:al.shape[1]]
    cx = (al * xs).sum() / m; cy = (al * ys).sum() / m
    sx = np.sqrt((al * (xs - cx) ** 2).sum() / m); sy = np.sqrt((al * (ys - cy) ** 2).sum() / m)
    # bordes subpíxel: perfil de columnas/filas, cruce al 50% del primer/último tramo
    col = al.sum(axis=0); row = al.sum(axis=1)
    def edge(p, rev=False):
        q = p[::-1] if rev else p
        thr = 0.5 * np.percentile(q[q > 0], 50)
        i = int(np.argmax(q >= thr))
        if i == 0: pos = 0.0
        else: pos = i - 1 + (thr - q[i - 1]) / max(1e-6, q[i] - q[i - 1])
        return (len(p) - 1 - pos) if rev else pos
    print(f"{a+k}\t{X0+cx:.2f}\t{Y0+cy:.2f}\t{sx:.3f}\t{sy:.3f}\t{sx/sy:.3f}\t{m:.0f}\t{X0+edge(col):.2f}\t{X0+edge(col,True):.2f}\t{Y0+edge(row):.2f}\t{Y0+edge(row,True):.2f}")
