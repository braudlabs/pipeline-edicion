"""trk2.py a b ref yA yB thr palabra:x0-x1 ...  -> por fotograma y palabra: y0 y1 alto x0 x1 brillo(p99 de L-Lref) area"""
import sys
import numpy as np
from la import *
a, b, ref, yA, yB = [int(v) for v in sys.argv[1:6]]
thr = float(sys.argv[6])
words = []
for s in sys.argv[7:]:
    n, r = s.split(":"); x0, x1 = [int(v) for v in r.split("-")]
    words.append((n, x0, x1))
R = luma(frames(ref, ref)[ref])
F = frames(a, b)
print("f\t" + "\t".join(f"{n}[y0 y1 h x0 x1 brillo area]" for n, _, _ in words))
for f in range(a, b + 1):
    L = luma(F[f]); D = L - R
    out = [str(f)]
    for n, x0, x1 in words:
        d = D[yA:yB, x0:x1 + 1]
        m = d > thr
        if m.sum() < 8:
            out.append("   -   "); continue
        ys, xs = np.nonzero(m)
        out.append(f"{ys.min()+yA:4d} {ys.max()+yA:4d} {ys.max()-ys.min()+1:3d} {xs.min()+x0:4d} {xs.max()+x0:4d} {np.percentile(d[m],99):5.0f} {int(m.sum()):5d}")
    print("\t".join(out))
