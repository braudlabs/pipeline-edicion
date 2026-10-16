#!/usr/bin/env python3
"""shadow.py fTexto fSin x0 y0 x1 y1: perfil de oscurecimiento alrededor de la tinta blanca (sombra) frente a un fotograma sin rótulo."""
import sys
import numpy as np
from tools import frames
ft, fn = int(sys.argv[1]), int(sys.argv[2])
X0, Y0, X1, Y1 = [int(v) for v in sys.argv[3:7]]
A = frames(ft, ft)[0][Y0:Y1, X0:X1].astype(np.float32)
B = frames(fn, fn)[0][Y0:Y1, X0:X1].astype(np.float32)
m = A.min(axis=2) >= 235
la, lb = A.mean(axis=2), B.mean(axis=2)
def dil(m):
    g = m.copy(); g[1:] |= m[:-1]; g[:-1] |= m[1:]; g[:, 1:] |= m[:, :-1]; g[:, :-1] |= m[:, 1:]; return g
cur = m.copy(); prev = m.copy()
print("dist_px\tn\trazón_lum(con/sin)\tdif")
for d in range(1, 41):
    cur = dil(prev)
    ring = cur & ~prev
    if ring.sum() > 50:
        # desglosa arriba/abajo de la tinta
        ys, xs = np.nonzero(ring)
        r = la[ring].mean() / max(1, lb[ring].mean())
        print(f"{d}\t{int(ring.sum())}\t{r:.3f}\t{la[ring].mean()-lb[ring].mean():+.1f}")
    prev = cur
