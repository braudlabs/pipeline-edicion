"""trk3.py a b ref thr palabra:x0-x1:yA-yB ...  -> por fotograma y palabra: y0 y1 x0 x1 brillo(p99 L-Lref) suma(k)"""
import sys
import numpy as np
from la import *
a, b, ref = [int(v) for v in sys.argv[1:4]]
thr = float(sys.argv[4])
words = []
for s in sys.argv[5:]:
    n, r, ry = s.split(":"); x0, x1 = [int(v) for v in r.split("-")]; yA, yB = [int(v) for v in ry.split("-")]
    words.append((n, x0, x1, yA, yB))
R = luma(frames(ref, ref)[ref])
F = frames(a, b)
print("f\t" + "\t".join(f"{n}[y0 y1 x0 x1 bri sumK]" for n, *_ in words))
for f in range(a, b + 1):
    L = luma(F[f]); D = L - R
    out = [str(f)]
    for n, x0, x1, yA, yB in words:
        d = D[yA:yB, x0:x1 + 1]
        m = d > thr
        if m.sum() < 8:
            out.append("    -    "); continue
        ys, xs = np.nonzero(m)
        out.append(f"{ys.min()+yA:4d} {ys.max()+yA:4d} {xs.min()+x0:4d} {xs.max()+x0:4d} {np.percentile(d[m],99):4.0f} {d[m].sum()/1000:6.1f}")
    print("\t".join(out))
