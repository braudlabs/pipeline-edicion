#!/usr/bin/env python3
"""Caja de tinta blanca nueva respecto de un fotograma de referencia.
  ink.py A B x0 y0 x1 y1 [--ref F] [--thr 215] [--gain 60]
  Tinta = min(R,G,B) >= thr  y (si hay ref) min(ref) < thr-gain... (no era ya blanca en la referencia).
"""
import argparse
import numpy as np
import fr

ap = argparse.ArgumentParser()
ap.add_argument("a", type=int); ap.add_argument("b", type=int)
ap.add_argument("x0", type=int); ap.add_argument("y0", type=int); ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
ap.add_argument("--ref", type=int)
ap.add_argument("--thr", type=float, default=215)
ap.add_argument("--gain", type=float, default=40)
ap.add_argument("--soft", action="store_true", help="además: caja con umbral bajo (thr-80) para ver fundidos/desenfoques")
a = ap.parse_args()
lo = min(a.a, a.ref) if a.ref is not None else a.a
hi = max(a.b, a.ref) if a.ref is not None else a.b
F = fr.frames(lo, hi)
ref = F[a.ref][a.y0:a.y1, a.x0:a.x1].min(2).astype(float) if a.ref is not None else None
print("f\tt\tx0\ty0\tx1\ty1\tcx\tcy\tancho\talto\tarea\tmedia_min\t| caja_suave(x0,y0,x1,y1,area)")
for f in range(a.a, a.b + 1):
    A = F[f][a.y0:a.y1, a.x0:a.x1].min(2).astype(float)
    def box(thr):
        m = A >= thr
        if ref is not None:
            m &= (A - ref) >= a.gain
        if m.sum() < 25:
            return None, int(m.sum()), m
        ys, xs = np.nonzero(m)
        bx0, bx1 = np.percentile(xs, [0.3, 99.7]); by0, by1 = np.percentile(ys, [0.3, 99.7])
        return (a.x0 + bx0, a.y0 + by0, a.x0 + bx1, a.y0 + by1), int(m.sum()), m
    bx, area, m = box(a.thr)
    s = ""
    if a.soft:
        bs, as_, ms = box(a.thr - 80)
        s = "\t| " + ("-" if bs is None else f"{bs[0]:.0f},{bs[1]:.0f},{bs[2]:.0f},{bs[3]:.0f} a={as_}")
    if bx is None:
        print(f"{f}\t{fr.t(f):.3f}\t-\t-\t-\t-\t-\t-\t-\t-\t{area}\t-{s}")
        continue
    print(f"{f}\t{fr.t(f):.3f}\t{bx[0]:.0f}\t{bx[1]:.0f}\t{bx[2]:.0f}\t{bx[3]:.0f}\t{(bx[0]+bx[2])/2:.1f}\t{(bx[1]+bx[3])/2:.1f}\t"
          f"{bx[2]-bx[0]:.0f}\t{bx[3]-bx[1]:.0f}\t{area}\t{A[m].mean():.0f}{s}")
