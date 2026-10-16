"""Diferencia por fotograma entre v6-ads90 (original) y v6-ads90-rev (revisión)."""
import sys
import numpy as np
from lib import run, arr, info, t_of

a, b = int(sys.argv[1]), int(sys.argv[2])
thr = float(sys.argv[3]) if len(sys.argv) > 3 else 30
CH = 120
print("f\tt\tmad\tmax\tn>thr\tx0\ty0\tx1\ty1\tcx\tcy\tw\th")
for s in range(a, b + 1, CH):
    e = min(b, s + CH - 1)
    R = run(s, e, "v6-ads90-rev")
    O = run(s, e, "v6-ads90")
    for k, (r, o) in enumerate(zip(R, O)):
        d = np.abs(arr(r) - arr(o)).max(axis=2)
        m = d > thr
        n = int(m.sum())
        f = s + k
        if n < 20:
            print(f"{f}\t{t_of(f, info()):.3f}\t{d.mean():.3f}\t{d.max():.0f}\t{n}")
            continue
        ys, xs = np.nonzero(m)
        x0, x1 = np.percentile(xs, [0.3, 99.7])
        y0, y1 = np.percentile(ys, [0.3, 99.7])
        print(f"{f}\t{t_of(f, info()):.3f}\t{d.mean():.3f}\t{d.max():.0f}\t{n}\t{x0:.0f}\t{y0:.0f}\t{x1:.0f}\t{y1:.0f}\t{(x0+x1)/2:.1f}\t{(y0+y1)/2:.1f}\t{x1-x0:.0f}\t{y1-y0:.0f}")
