#!/usr/bin/env python3
"""subs.py A B [thr]: métrica de tinta blanca de cada pista OCR en f A..B (bbox, línea base, altura de x)."""
import json, sys
import numpy as np
from tools import frames, drop_border, ROOT, W, H
a, b = int(sys.argv[1]), int(sys.argv[2])
thr = int(sys.argv[3]) if len(sys.argv) > 3 else 250
T = json.load(open(ROOT / "datos/v1-pagado/texts.json"))["tracks"]
fr = frames(a, b)
print("f\tid\ttexto\tx0\ty0\tx1\ty1\tcx\tw\th\tbase\txtop\txh\tarea")
for tr in T:
    if tr["f_out"] < a or tr["f_in"] > b:
        continue
    pf = tr["per_frame"]
    xs0 = min(p[1] - p[3] / 2 for p in pf) - 50
    xs1 = max(p[1] + p[3] / 2 for p in pf) + 50
    ys0 = min(p[2] - p[4] / 2 for p in pf) - 45
    ys1 = max(p[2] + p[4] / 2 for p in pf) + 45
    X0, X1, Y0, Y1 = max(0, int(xs0)), min(W, int(xs1)), max(0, int(ys0)), min(H, int(ys1))
    for f in range(max(a, tr["f_in"]), min(b, tr["f_out"]) + 1):
        im = fr[f - a][Y0:Y1, X0:X1]
        m = drop_border(im.min(axis=2) >= thr)
        if m.sum() < 30:
            print(f"{f}\t{tr['id']}\t{tr['text']}\t-")
            continue
        ys, xs = np.nonzero(m)
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        rows = m.sum(axis=1).astype(float)
        mx = rows.max()
        good = np.nonzero(rows >= 0.35 * mx)[0]
        base = good.max()
        xtop = np.nonzero(rows >= 0.55 * mx)[0].min()
        print(f"{f}\t{tr['id']}\t{tr['text']}\t{X0+x0}\t{Y0+y0}\t{X0+x1}\t{Y0+y1}\t{X0+(x0+x1)/2:.1f}\t{x1-x0+1}\t{y1-y0+1}\t{Y0+base}\t{Y0+xtop}\t{base-xtop+1}\t{int(m.sum())}")
