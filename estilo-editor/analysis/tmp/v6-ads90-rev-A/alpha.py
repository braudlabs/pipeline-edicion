#!/usr/bin/env python3
"""Opacidad aparente de un rótulo blanco, fotograma a fotograma.

  alpha.py A B x0 y0 x1 y1 --ref R [--pre P] [--thr 246] [--erode 2] [--white 253]

Máscara = núcleo de la tinta en el fotograma de referencia R (min(RGB) >= thr, erosionada).
Dos estimadores:
  a_ring : contraste espacial en el mismo fotograma. T = media de min(RGB) en el núcleo; G = media de
           min(RGB) en un anillo alrededor de la tinta (fondo local). a = (T-G)/(white-G).
           Robusto a que el metraje cambie; exige fondo localmente parecido bajo la letra y a su lado.
  a_pre  : temporal. Fondo = fotograma P (rótulo ausente): mediana de (I_f-I_P)/(I_R-I_P) en el núcleo.
También imprime la caja de la tinta >= --box.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from lib import frames  # noqa: E402


def erode(m, n):
    for _ in range(n):
        e = m.copy()
        e[1:, :] &= m[:-1, :]
        e[:-1, :] &= m[1:, :]
        e[:, 1:] &= m[:, :-1]
        e[:, :-1] &= m[:, 1:]
        m = e
    return m


def dilate(m, n):
    for _ in range(n):
        e = m.copy()
        e[1:, :] |= m[:-1, :]
        e[:-1, :] |= m[1:, :]
        e[:, 1:] |= m[:, :-1]
        e[:, :-1] |= m[:, 1:]
        m = e
    return m


ap = argparse.ArgumentParser()
ap.add_argument("a", type=int)
ap.add_argument("b", type=int)
ap.add_argument("x0", type=int)
ap.add_argument("y0", type=int)
ap.add_argument("x1", type=int)
ap.add_argument("y1", type=int)
ap.add_argument("--ref", type=int, required=True)
ap.add_argument("--pre", type=int)
ap.add_argument("--thr", type=float, default=246)
ap.add_argument("--erode", type=int, default=2)
ap.add_argument("--box", type=float, default=240)
ap.add_argument("--white", type=float, default=253)
ap.add_argument("--r0", type=int, default=7)
ap.add_argument("--r1", type=int, default=13)
a = ap.parse_args()
pre = a.pre if a.pre is not None else a.a
lo = min(a.a, a.ref, pre)
hi = max(a.b, a.ref, pre)
F = frames(lo, hi)[:, a.y0:a.y1, a.x0:a.x1].astype(np.float32)
R = F[a.ref - lo]
P = F[pre - lo]
full = R.min(axis=2) >= 235
core = erode(R.min(axis=2) >= a.thr, a.erode)
ring = dilate(full, a.r1) & ~dilate(full, a.r0)
contrast = (R - P).sum(axis=2)
use = core & (contrast > 60)
print(f"# núcleo {int(core.sum())} px, anillo {int(ring.sum())} px, utilizables(pre) {int(use.sum())} px; ref f{a.ref}, fondo f{pre}")
print("f\ta_ring\ta_pre\tT\tG\tx0\tx1\ty0\ty1\tw\th\tarea")
for f in range(a.a, a.b + 1):
    I = F[f - lo]
    m = I.min(axis=2)
    T = float(m[core].mean()) if core.any() else 0
    G = float(m[ring].mean()) if ring.any() else 0
    a_ring = (T - G) / max(1.0, (a.white - G))
    if use.sum() > 10:
        al = (I - P).sum(axis=2)[use] / contrast[use]
        a_pre = f"{np.median(al):.3f}"
    else:
        a_pre = "-"
    mask = m >= a.box
    bx = "-\t-\t-\t-\t-\t-\t" + str(int(mask.sum()))
    if mask.sum() >= 20:
        cols = np.nonzero(mask.sum(axis=0) >= 2)[0]
        rows = np.nonzero(mask.sum(axis=1) >= 2)[0]
        if len(cols) and len(rows):
            bx = f"{a.x0 + cols[0]}\t{a.x0 + cols[-1]}\t{a.y0 + rows[0]}\t{a.y0 + rows[-1]}\t{cols[-1] - cols[0] + 1}\t{rows[-1] - rows[0] + 1}\t{int(mask.sum())}"
    print(f"{f}\t{a_ring:.3f}\t{a_pre}\t{T:.0f}\t{G:.0f}\t{bx}")
