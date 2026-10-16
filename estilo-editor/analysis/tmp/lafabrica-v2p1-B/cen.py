#!/usr/bin/env python3
"""Centroide subpíxel y extensión de la tinta blanca: cen.py A B x0 y0 x1 y1 [--thr 200]
Usa peso continuo (min(R,G,B)-thr recortado) para detectar derivas de fracción de píxel y cambios de escala."""
import argparse
import numpy as np
import fr
ap = argparse.ArgumentParser()
ap.add_argument("a", type=int); ap.add_argument("b", type=int)
ap.add_argument("x0", type=int); ap.add_argument("y0", type=int); ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
ap.add_argument("--thr", type=float, default=200)
a = ap.parse_args()
F = fr.frames(a.a, a.b)
print("f\tpeso\tcx\tcy\tsx(rms)\tsy(rms)\tx0\tx1\ty0\ty1")
for f in range(a.a, a.b + 1):
    A = F[f][a.y0:a.y1, a.x0:a.x1].min(2).astype(float)
    w = np.clip(A - a.thr, 0, None)
    s = w.sum()
    if s < 500:
        print(f, "-"); continue
    ys, xs = np.mgrid[a.y0:a.y1, a.x0:a.x1]
    cx = (w * xs).sum() / s; cy = (w * ys).sum() / s
    sx = np.sqrt((w * (xs - cx) ** 2).sum() / s); sy = np.sqrt((w * (ys - cy) ** 2).sum() / s)
    m = A >= 235
    yy, xx = np.nonzero(m)
    print(f"{f}\t{s/55:.0f}\t{cx:.2f}\t{cy:.2f}\t{sx:.2f}\t{sy:.2f}\t{xx.min()+a.x0}\t{xx.max()+a.x0}\t{yy.min()+a.y0}\t{yy.max()+a.y0}")
