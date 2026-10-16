#!/usr/bin/env python3
"""Desplazamiento horizontal subpíxel de un rótulo respecto a un fotograma de referencia por correlación
normalizada de la forma del texto (máscara de tinta de la referencia) con la imagen de 'blancura' de cada fotograma.
  xcorr.py A B x0 y0 x1 y1 --ref R [--dx a,b] [--dy a,b] [--pre P]
Con --pre se resta el fondo (fotograma sin rótulo) antes de correlacionar (mejor para fundidos).
"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import frames
ap = argparse.ArgumentParser()
ap.add_argument("a", type=int); ap.add_argument("b", type=int)
ap.add_argument("x0", type=int); ap.add_argument("y0", type=int); ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
ap.add_argument("--ref", type=int, required=True)
ap.add_argument("--pre", type=int)
ap.add_argument("--dx", default="-40,10")
ap.add_argument("--dy", default="0,0")
a = ap.parse_args()
pad = 60
lo = min(a.a, a.ref, a.pre if a.pre is not None else a.a); hi = max(a.b, a.ref)
F = frames(lo, hi)[:, a.y0:a.y1, max(0, a.x0 - pad):a.x1 + pad].astype(np.float32)
off = a.x0 - max(0, a.x0 - pad)
R = F[a.ref - lo].min(axis=2)
tmpl = (R[:, off:off + (a.x1 - a.x0)] >= 240).astype(np.float32)
tm = tmpl - tmpl.mean()
dxa, dxb = [int(v) for v in a.dx.split(",")]
dya, dyb = [int(v) for v in a.dy.split(",")]
P = F[a.pre - lo].min(axis=2) if a.pre is not None else None
print("f\tdx\tdy\tncc")
for f in range(a.a, a.b + 1):
    I = F[f - lo].min(axis=2)
    if P is not None:
        I = I - P
    sc = {}
    for dy in range(dya, dyb + 1):
        for dx in range(dxa, dxb + 1):
            x = off + dx
            if x < 0 or x + tm.shape[1] > I.shape[1]:
                continue
            y0 = max(0, dy); y1 = min(I.shape[0], I.shape[0] + dy)
            w = I[y0:y1, x:x + tm.shape[1]]
            t = tm[y0 - dy:y1 - dy]
            ww = w - w.mean()
            den = np.sqrt((ww ** 2).sum() * (t ** 2).sum()) + 1e-6
            sc[(dx, dy)] = float((ww * t).sum() / den)
    (dx, dy), best = max(sc.items(), key=lambda kv: kv[1])
    sub = 0.0
    if (dx - 1, dy) in sc and (dx + 1, dy) in sc:
        l, c, r = sc[(dx - 1, dy)], best, sc[(dx + 1, dy)]
        d = l - 2 * c + r
        sub = 0.0 if abs(d) < 1e-9 else 0.5 * (l - r) / d
    suby = 0.0
    if (dx, dy - 1) in sc and (dx, dy + 1) in sc:
        l, c, r = sc[(dx, dy - 1)], best, sc[(dx, dy + 1)]
        d = l - 2 * c + r
        suby = 0.0 if abs(d) < 1e-9 else 0.5 * (l - r) / d
    print(f"{f}\t{dx + sub:+.2f}\t{dy + suby:+.2f}\t{best:.3f}")
