#!/usr/bin/env python3
"""Altura de la última (o primera) letra redonda del rótulo blanco, fotograma a fotograma: mide la escala global del texto."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from common import probe
from sheet import load_full_run
slug = "lafabrica-v1"
info = probe(slug)
a, b = int(sys.argv[1]), int(sys.argv[2])
side = sys.argv[3]            # R = última letra, L = primera
y_lo, y_hi = int(sys.argv[4]), int(sys.argv[5])
thr = float(sys.argv[6]) if len(sys.argv) > 6 else 205
w_in, w_out = (int(sys.argv[7]), int(sys.argv[8])) if len(sys.argv) > 8 else (20, 110)
x_lo, x_hi = (int(sys.argv[9]), int(sys.argv[10])) if len(sys.argv) > 10 else (0, 1080)
imgs = load_full_run(slug, a, b - a + 1, info)
print("f\tx0\tx1\tcx\tancho\ttop\tbase\talto_letra")
for k, im in enumerate(imgs):
    A = np.asarray(im, np.float32)[y_lo:y_hi, x_lo:x_hi]
    m = A.min(axis=2) >= thr
    ys, xs = np.nonzero(m)
    if len(xs) < 50:
        print(a + k, "-"); continue
    x0, x1 = np.percentile(xs, [0.15, 99.85])
    if side == "R":
        c0, c1 = int(x1 - w_out), int(x1 - w_in)
    else:
        c0, c1 = int(x0 + w_in), int(x0 + w_out)
    sub = m[:, c0:c1]
    rows = np.nonzero(sub.sum(axis=1) >= 3)[0]
    if len(rows) == 0:
        print(a + k, "-"); continue
    # tramo contiguo más largo
    splits = np.split(rows, np.nonzero(np.diff(rows) > 2)[0] + 1)
    seg = max(splits, key=len)
    top, base = y_lo + seg[0], y_lo + seg[-1]
    print(f"{a+k}\t{x_lo+x0:.0f}\t{x_lo+x1:.0f}\t{x_lo+(x0+x1)/2:.1f}\t{x1-x0:.0f}\t{top}\t{base}\t{base-top+1}")
