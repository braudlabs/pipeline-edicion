#!/usr/bin/env python3
"""Centroide/anchura subpíxel de la tinta blanca, excluyendo lo que ya era claro en un fotograma de referencia sin texto.
  cen2.py A B x0 y0 x1 y1 --ref F [--refscale 1.0] [--thr 200] [--refmax 170]
Bordes subpíxel: posiciones donde el perfil acumulado de tinta cruza 1 % y 99 % (x e y)."""
import argparse
import numpy as np
import fr
ap = argparse.ArgumentParser()
ap.add_argument("a", type=int); ap.add_argument("b", type=int)
ap.add_argument("x0", type=int); ap.add_argument("y0", type=int); ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
ap.add_argument("--ref", type=int)
ap.add_argument("--refscale", type=float, default=1.0)
ap.add_argument("--thr", type=float, default=200)
ap.add_argument("--refmax", type=float, default=170)
a = ap.parse_args()
lo = min(a.a, a.ref) if a.ref is not None else a.a
hi = max(a.b, a.ref) if a.ref is not None else a.b
F = fr.frames(lo, hi)
ok = None
if a.ref is not None:
    R = F[a.ref][a.y0:a.y1, a.x0:a.x1].min(2).astype(float) * a.refscale
    # dilata la zona clara de la referencia 3 px para tolerar el movimiento del fondo
    bright = R >= a.refmax
    for _ in range(3):
        b2 = bright.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                b2 |= np.roll(np.roll(bright, dy, 0), dx, 1)
        bright = b2
    ok = ~bright
def edge(p, q):
    c = np.cumsum(p); c = c / c[-1]
    i = np.searchsorted(c, q)
    c0 = c[i - 1] if i > 0 else 0.0
    return i - 1 + (q - c0) / (c[i] - c0 + 1e-12) + 0.5
print("f\ttinta\tcx\tcy\tsx\tsy\txL(1%)\txR(99%)\tancho\tyT(1%)\tyB(99%)\talto")
for f in range(a.a, a.b + 1):
    A = F[f][a.y0:a.y1, a.x0:a.x1].min(2).astype(float)
    w = np.clip((A - a.thr) / (251 - a.thr), 0, 1)
    if ok is not None:
        w = w * ok
    s = w.sum()
    if s < 300:
        print(f, "-"); continue
    ys, xs = np.mgrid[a.y0:a.y1, a.x0:a.x1]
    cx = (w * xs).sum() / s; cy = (w * ys).sum() / s
    sx = np.sqrt((w * (xs - cx) ** 2).sum() / s); sy = np.sqrt((w * (ys - cy) ** 2).sum() / s)
    px = w.sum(0); py = w.sum(1)
    xL, xR = a.x0 + edge(px, 0.01), a.x0 + edge(px, 0.99)
    yT, yB = a.y0 + edge(py, 0.01), a.y0 + edge(py, 0.99)
    print(f"{f}\t{s:.0f}\t{cx:.2f}\t{cy:.2f}\t{sx:.2f}\t{sy:.2f}\t{xL:.2f}\t{xR:.2f}\t{xR-xL:.2f}\t{yT:.2f}\t{yB:.2f}\t{yB-yT:.2f}")
