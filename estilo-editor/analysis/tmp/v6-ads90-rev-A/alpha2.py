#!/usr/bin/env python3
"""Opacidad y desplazamiento de un rótulo blanco que se mueve mientras entra o sale.

  alpha2.py A B x0 y0 x1 y1 --ref R --pre P [--dx a,b] [--dy a,b] [--white 253] [--erode 3]
            [--scales 1.0] [--prelist P1,P2,...]

La máscara es el núcleo de la tinta en el fotograma de referencia R (opaco). En cada fotograma f se busca
el desplazamiento entero (dx, dy) —y opcionalmente la escala respecto al centro de la caja— que maximiza
el contraste núcleo-anillo, y con él:
  alpha = mediana sobre el núcleo desplazado de (I_f - P)/(white - P)   (P = fotograma sin rótulo)
Con --prelist se toma como fondo, para cada f, el fotograma de la lista más cercano en el tiempo.
Salida: f, dx, dy, escala, alpha (mediana), p25, p75, T (min(RGB) medio en el núcleo), G (anillo).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

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


def shift(m, dx, dy):
    out = np.zeros_like(m)
    h, w = m.shape
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = m[ys0:ys1, xs0:xs1]
    return out


def scale_mask(m, s):
    if abs(s - 1) < 1e-6:
        return m
    h, w = m.shape
    ys, xs = np.nonzero(m)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    im = Image.fromarray((m * 255).astype(np.uint8))
    # afín inversa: salida(x,y) <- entrada(cx + (x-cx)/s, cy + (y-cy)/s)
    im2 = im.transform((w, h), Image.AFFINE, (1 / s, 0, cx - cx / s, 0, 1 / s, cy - cy / s), Image.BILINEAR)
    return np.asarray(im2) > 127


ap = argparse.ArgumentParser()
ap.add_argument("a", type=int)
ap.add_argument("b", type=int)
ap.add_argument("x0", type=int)
ap.add_argument("y0", type=int)
ap.add_argument("x1", type=int)
ap.add_argument("y1", type=int)
ap.add_argument("--ref", type=int, required=True)
ap.add_argument("--pre", type=int)
ap.add_argument("--prelist")
ap.add_argument("--dx", default="0,0")
ap.add_argument("--dy", default="0,0")
ap.add_argument("--white", type=float, default=253)
ap.add_argument("--thr", type=float, default=244)
ap.add_argument("--erode", type=int, default=3)
ap.add_argument("--scales", default="1.0")
a = ap.parse_args()
pres = [int(v) for v in a.prelist.split(",")] if a.prelist else [a.pre if a.pre is not None else a.a]
lo = min([a.a, a.ref] + pres)
hi = max([a.b, a.ref] + pres)
F = frames(lo, hi)[:, a.y0:a.y1, a.x0:a.x1].astype(np.float32)
R = F[a.ref - lo]
full = R.min(axis=2) >= 235
core0 = erode(R.min(axis=2) >= a.thr, a.erode)
ring0 = dilate(full, 12) & ~dilate(full, 5)
dxa, dxb = [int(v) for v in a.dx.split(",")]
dya, dyb = [int(v) for v in a.dy.split(",")]
scales = [float(v) for v in a.scales.split(",")]
print(f"# núcleo {int(core0.sum())} px; ref f{a.ref}; fondo f{pres}")
print("f\tdx\tdy\tesc\talpha\tp25\tp75\tT\tG")
for f in range(a.a, a.b + 1):
    I = F[f - lo]
    m = I.min(axis=2)
    pf = min(pres, key=lambda p: abs(p - f))
    P = F[pf - lo]
    best = None
    for s in scales:
        cs = scale_mask(core0, s)
        rs = scale_mask(ring0, s)
        for dy in range(dya, dyb + 1):
            for dx in range(dxa, dxb + 1):
                c = shift(cs, dx, dy)
                r = shift(rs, dx, dy)
                if c.sum() < 20 or r.sum() < 20:
                    continue
                sc = m[c].mean() - m[r].mean()
                if best is None or sc > best[0]:
                    best = (sc, dx, dy, s, c, r)
    sc, dx, dy, s, c, r = best
    den = (a.white * 3 - P.sum(axis=2))
    ok = c & (den > 90)
    if ok.sum() > 10:
        al = (I.sum(axis=2) - P.sum(axis=2))[ok] / den[ok]
        print(f"{f}\t{dx}\t{dy}\t{s:.3f}\t{np.median(al):.3f}\t{np.percentile(al, 25):.3f}\t{np.percentile(al, 75):.3f}\t{m[c].mean():.0f}\t{m[r].mean():.0f}")
    else:
        print(f"{f}\t{dx}\t{dy}\t{s:.3f}\t-\t-\t-\t{m[c].mean():.0f}\t{m[r].mean():.0f}")
