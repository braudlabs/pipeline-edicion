#!/usr/bin/env python3
"""Tramos de filas y columnas con tinta blanca en una región: rows.py A B x0 y0 x1 y1 [--thr 235] [--ref F] [--minrow 3]"""
import argparse
import numpy as np
import fr
ap = argparse.ArgumentParser()
ap.add_argument("a", type=int); ap.add_argument("b", type=int)
ap.add_argument("x0", type=int); ap.add_argument("y0", type=int); ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
ap.add_argument("--thr", type=float, default=235)
ap.add_argument("--ref", type=int)
ap.add_argument("--refmax", type=float, default=200)
ap.add_argument("--minrow", type=int, default=3)
ap.add_argument("--mincol", type=int, default=2)
a = ap.parse_args()
lo = min(a.a, a.ref) if a.ref is not None else a.a
hi = max(a.b, a.ref) if a.ref is not None else a.b
F = fr.frames(lo, hi)
def runs(v):
    out = []; on = False
    for i, x in enumerate(v):
        if x and not on: s = i; on = True
        if not x and on: out.append((s, i - 1)); on = False
    if on: out.append((s, len(v) - 1))
    return out
ref = F[a.ref][a.y0:a.y1, a.x0:a.x1].min(2) if a.ref is not None else None
for f in range(a.a, a.b + 1):
    A = F[f][a.y0:a.y1, a.x0:a.x1].min(2)
    m = A >= a.thr
    if ref is not None:
        m &= ref < a.refmax
    rr = runs(m.sum(1) >= a.minrow); cr = runs(m.sum(0) >= a.mincol)
    if not rr:
        print(f, "-", int(m.sum())); continue
    print(f, "area", int(m.sum()), "| x", cr[0][0] + a.x0, cr[-1][1] + a.x0, "ancho", cr[-1][1] - cr[0][0] + 1,
          "| y", rr[0][0] + a.y0, rr[-1][1] + a.y0, "alto", rr[-1][1] - rr[0][0] + 1,
          "| filas", [(p + a.y0, q + a.y0) for p, q in rr], "| ncols", len(cr))
