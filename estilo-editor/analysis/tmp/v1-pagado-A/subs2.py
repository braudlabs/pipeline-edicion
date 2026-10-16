#!/usr/bin/env python3
"""subs2.py A B [lo hi]: bordes subpíxel (alfa suave) de cada pista OCR: x0,x1 (ancho), línea base, tope de la x, masa."""
import json, sys
import numpy as np
from tools import frames, drop_border, ROOT, W, H
a, b = int(sys.argv[1]), int(sys.argv[2])
lo = float(sys.argv[3]) if len(sys.argv) > 3 else 235
hi = float(sys.argv[4]) if len(sys.argv) > 4 else 253
T = json.load(open(ROOT / "datos/v1-pagado/texts.json"))["tracks"]
fr = frames(a, b)

def cross(p, frac, rev=False):
    q = p[::-1] if rev else p
    thr = frac * q.max()
    i = int(np.argmax(q >= thr))
    pos = 0.0 if i == 0 else i - 1 + (thr - q[i - 1]) / max(1e-6, q[i] - q[i - 1])
    return (len(p) - 1 - pos) if rev else pos

print("f\tid\ttexto\tx0\tx1\tancho\tcx\tbase\txtop\txh\tytop\tybot\tmasa")
for tr in T:
    if tr["f_out"] < a or tr["f_in"] > b:
        continue
    pf = tr["per_frame"]
    X0 = max(0, int(min(p[1] - p[3] / 2 for p in pf) - 50)); X1 = min(W, int(max(p[1] + p[3] / 2 for p in pf) + 50))
    Y0 = max(0, int(min(p[2] - p[4] / 2 for p in pf) - 45)); Y1 = min(H, int(max(p[2] + p[4] / 2 for p in pf) + 45))
    for f in range(max(a, tr["f_in"]), min(b, tr["f_out"]) + 1):
        c = fr[f - a][Y0:Y1, X0:X1].astype(np.float32).min(axis=2)
        al = np.clip((c - lo) / (hi - lo), 0, 1)
        al = al * drop_border(al > 0)
        m = al.sum()
        if m < 30:
            print(f"{f}\t{tr['id']}\t{tr['text']}\t-"); continue
        col = al.sum(axis=0); row = al.sum(axis=1)
        nz = np.nonzero(col > 0.5)[0]; x0 = nz.min(); x1 = nz.max()
        # bordes subpíxel horizontales: suma de alfa parcial en la primera/última columna
        base = cross(row, 0.35, rev=True); xtop = cross(row, 0.55)
        nzr = np.nonzero(row > 0.5)[0]
        # ancho subpíxel por momento: cruces al 15 % del máximo de columna
        xl = cross(col, 0.15); xr = cross(col, 0.15, rev=True)
        print(f"{f}\t{tr['id']}\t{tr['text']}\t{X0+xl:.2f}\t{X0+xr:.2f}\t{xr-xl:.2f}\t{X0+(xl+xr)/2:.2f}\t{Y0+base:.2f}\t{Y0+xtop:.2f}\t{base-xtop:.2f}\t{Y0+nzr.min()}\t{Y0+nzr.max()}\t{m:.0f}")
