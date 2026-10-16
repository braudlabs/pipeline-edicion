#!/usr/bin/env python3
"""fade2.py A B fRef fBg nombre:x0,y0,x1,y1 ...: opacidad sobre los píxeles que son tinta en fRef (erosionados),
con el fondo tomado de fBg (fotograma sin el rótulo). alfa=(I-B)/(253-B), media sobre píxeles."""
import sys
import numpy as np
from tools import frames
a, b, fref, fbg = [int(v) for v in sys.argv[1:5]]
regs = []
for s in sys.argv[5:]:
    n, r = s.split(":"); regs.append((n, [int(v) for v in r.split(",")]))
fr = frames(a, b)
ref = frames(fref, fref)[0]; bgf = frames(fbg, fbg)[0]
def ero(m):
    g = m.copy(); g[1:] &= m[:-1]; g[:-1] &= m[1:]; g[:, 1:] &= m[:, :-1]; g[:, :-1] &= m[:, 1:]; return g
masks = []
for n, (x0, y0, x1, y1) in regs:
    m = ero(ero(ref[y0:y1, x0:x1].min(axis=2) >= 250))
    B = bgf[y0:y1, x0:x1].astype(np.float32).min(axis=2)
    m &= B < 200          # descarta donde el fondo ya era casi blanco
    masks.append((m, B))
print("f\t" + "\t".join(f"{n}(n={int(m.sum())})" for (n, _), (m, _) in zip(regs, masks)))
for k, im in enumerate(fr):
    out = []
    for (n, (x0, y0, x1, y1)), (m, B) in zip(regs, masks):
        c = im[y0:y1, x0:x1].astype(np.float32).min(axis=2)
        al = ((c[m] - B[m]) / np.maximum(1, 253 - B[m]))
        out.append(f"{np.median(al):.2f}")
    print(f"{a+k}\t" + "\t".join(out))
