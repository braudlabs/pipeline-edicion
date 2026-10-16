import sys, collections
import numpy as np
from la import *
segs = [(0, 214, (700, 100, 1900, 700)), (215, 307, (700, 100, 1900, 700)), (308, 507, (700, 60, 1900, 1000)), (508, 569, (500, 60, 1500, 760)), (570, 730, (1100, 60, 1900, 1000))]
for a, b, (x0, y0, x1, y1) in segs:
    F = frames(a, b)
    prev = None; s = []
    for f in range(a, b + 1):
        L = luma(F[f])[y0:y1, x0:x1]
        if prev is not None: s.append((f, float(np.abs(L - prev).mean())))
        prev = L
    d = np.array([v for _, v in s])
    thr = 0.4
    line = "".join("N" if v > thr else "." for v in d)
    print(f"## plano f{a}-f{b}: región x{x0}-{x1} y{y0}-{y1}; N=nuevo (dif>{thr})")
    for i in range(0, len(line), 60):
        print(f"f{a+1+i:4d} {line[i:i+60]}")
    new = [f for f, v in s if v > thr]
    gaps = np.diff(new)
    print("  huecos:", dict(sorted(collections.Counter(gaps.tolist()).items())), f" fps≈{60*(len(new)-1)/(new[-1]-new[0]):.2f}", " dif nuevos: media %.2f min %.2f | repetidos: media %.3f max %.2f" % (d[d > thr].mean(), d[d > thr].min(), d[d <= thr].mean() if (d <= thr).any() else 0, d[d <= thr].max() if (d <= thr).any() else 0))
    # patrón de paso doble: cociente de la dif de cada nuevo respecto a la mediana local
    nv = [(f, v) for f, v in s if v > thr]
    big = [f for i, (f, v) in enumerate(nv) if 2 <= i < len(nv) - 2 and v > 1.3 * np.median([nv[j][1] for j in (i-2, i-1, i+1, i+2)])]
    print("  fotogramas nuevos con salto ≥1,3× sus vecinos:", big[:40])
