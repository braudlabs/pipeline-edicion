#!/usr/bin/env python3
"""Perfil del halo alrededor de la tinta blanca: halo.py A B x0 y0 x1 y1 [--ref F --refscale s]
Imprime por fotograma el exceso de color (R-B y G-B) medio en anillos a 2..10 px de la tinta."""
import argparse
import numpy as np
import fr
ap = argparse.ArgumentParser()
ap.add_argument("a", type=int); ap.add_argument("b", type=int)
ap.add_argument("x0", type=int); ap.add_argument("y0", type=int); ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
ap.add_argument("--thr", type=float, default=240)
a = ap.parse_args()
F = fr.frames(a.a, a.b)
def dil(m):
    o = m.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o
print("f\ttinta_px\tmedia_tinta\t" + "\t".join(f"d{d}(R,G,B)" for d in (2, 3, 4, 5, 6, 8, 10, 14)))
for f in range(a.a, a.b + 1):
    T = F[f][a.y0:a.y1, a.x0:a.x1].astype(float)
    m = T.min(2) >= a.thr
    if m.sum() < 50:
        print(f, m.sum(), "-"); continue
    prev = m.copy(); out = []
    for d in range(1, 15):
        cur = dil(prev); ring = cur & ~prev
        if d in (2, 3, 4, 5, 6, 8, 10, 14):
            c = T[ring].mean(0)
            out.append(f"{c[0]:.0f},{c[1]:.0f},{c[2]:.0f}")
        prev = cur
    print(f"{f}\t{int(m.sum())}\t{T[m].mean():.0f}\t" + "\t".join(out))
