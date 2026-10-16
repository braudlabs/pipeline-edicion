#!/usr/bin/env python3
"""Sombra/halo de un rótulo: compara un fotograma con rótulo (B) con otro sin él (A) sobre el mismo fondo.
  shadow.py A B x0 y0 x1 y1 [thr=240]
Imprime la razón de luminancia B/A por distancia al glifo, y por dirección (arriba/abajo/izda/dcha).
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import frames, gray
A, B, X0, Y0, X1, Y1 = [int(v) for v in sys.argv[1:7]]
thr = float(sys.argv[7]) if len(sys.argv) > 7 else 240
lo, hi = min(A, B), max(A, B)
F = frames(lo, hi).astype(np.float32)
a = gray(F[A - lo])[Y0:Y1, X0:X1]
b = gray(F[B - lo])[Y0:Y1, X0:X1]
m = (F[B - lo].min(axis=2) >= thr)[Y0:Y1, X0:X1] & ~((F[A - lo].min(axis=2) >= thr)[Y0:Y1, X0:X1])
# control: zona lejos del glifo
def dil(z):
    e = z.copy(); e[1:, :] |= z[:-1, :]; e[:-1, :] |= z[1:, :]; e[:, 1:] |= z[:, :-1]; e[:, :-1] |= z[:, 1:]; return e
cur = m.copy()
print(f"tinta nueva: {int(m.sum())} px")
print("dist\tn\trazón\tdif")
rings = {}
for d in range(1, 81):
    nxt = dil(cur)
    ring = nxt & ~cur
    cur = nxt
    if ring.sum() > 0 and (d <= 12 or d % 4 == 0):
        r = b[ring] / np.maximum(a[ring], 1)
        print(f"{d}\t{int(ring.sum())}\t{np.median(r):.3f}\t{np.median(b[ring]-a[ring]):+.1f}")
far = ~cur
if far.sum() > 100:
    print(f"lejos(>80px)\t{int(far.sum())}\t{np.median(b[far]/np.maximum(a[far],1)):.3f}\t{np.median(b[far]-a[far]):+.1f}")
# direccional: desplazar la máscara 10 px en cada dirección y medir la razón en la franja nueva
ys, xs = np.nonzero(m)
if len(ys):
    def band(dx, dy, n=14, skip=4):
        out = np.zeros_like(m)
        for k in range(skip, n):
            sx, sy = dx * k, dy * k
            sh = np.zeros_like(m)
            h, w = m.shape
            x0, x1 = max(0, -sx), min(w, w - sx)
            y0, y1 = max(0, -sy), min(h, h - sy)
            sh[y0 + sy:y1 + sy, x0 + sx:x1 + sx] = m[y0:y1, x0:x1]
            out |= sh
        return out & ~dil(dil(dil(m)))
    for name, (dx, dy) in (("abajo", (0, 1)), ("arriba", (0, -1)), ("derecha", (1, 0)), ("izquierda", (-1, 0))):
        bd = band(dx, dy)
        # solo píxeles que no están también en la banda opuesta (bordes exteriores)
        if bd.sum() > 50:
            print(f"{name}\t{int(bd.sum())}\t{np.median(b[bd]/np.maximum(a[bd],1)):.3f}")
