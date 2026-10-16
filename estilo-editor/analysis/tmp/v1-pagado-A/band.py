#!/usr/bin/env python3
"""band.py A B [y0 y1 x0 x1 thr]: firma por fotograma de la tinta blanca en la franja de subtítulos."""
import sys
import numpy as np
from tools import frames, drop_border
a, b = int(sys.argv[1]), int(sys.argv[2])
Y0 = int(sys.argv[3]) if len(sys.argv) > 3 else 1090
Y1 = int(sys.argv[4]) if len(sys.argv) > 4 else 1260
X0 = int(sys.argv[5]) if len(sys.argv) > 5 else 120
X1 = int(sys.argv[6]) if len(sys.argv) > 6 else 960
thr = int(sys.argv[7]) if len(sys.argv) > 7 else 250
f = a
prev = None
while f <= b:
    e = min(b, f + 59)
    for k, im in enumerate(frames(f, e)):
        m = drop_border(im[Y0:Y1, X0:X1].min(axis=2) >= thr)
        n = int(m.sum())
        if n < 40:
            sig = "—"
        else:
            ys, xs = np.nonzero(m)
            sig = f"x {X0+xs.min()}-{X0+xs.max()} (w{xs.max()-xs.min()+1}) y {Y0+ys.min()}-{Y0+ys.max()} area {n}"
        print(f"f{f+k}\t{sig}")
    f = e + 1
