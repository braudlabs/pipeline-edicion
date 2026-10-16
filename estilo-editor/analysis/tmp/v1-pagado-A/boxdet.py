#!/usr/bin/env python3
"""boxdet.py A B: detecta el recuadro fino (líneas claras de 1-3 px) por crestas horizontales/verticales largas."""
import sys
import numpy as np
from tools import frames
a, b = int(sys.argv[1]), int(sys.argv[2])
def longest(v, gap=3):
    best = (0, 0, 0); i = 0; n = len(v)
    while i < n:
        if v[i]:
            j = i; g = 0; last = i
            while j + 1 < n and (v[j + 1] or g < gap):
                j += 1
                if v[j]: g = 0; last = j
                else: g += 1
            if last - i + 1 > best[0]: best = (last - i + 1, i, last)
            i = j + 1
        else: i += 1
    return best
print("f\tarriba(y,x0-x1)\tabajo(y,x0-x1)\tizq(x,y0-y1)\tdcha(x,y0-y1)\tancho\talto\tcentro")
for k, im in enumerate(frames(a, b)):
    L = im.astype(np.float32).mean(axis=2)
    rh = np.zeros_like(L, bool); rv = np.zeros_like(L, bool)
    rh[3:-3] = (L[3:-3] - np.maximum(L[:-6], L[6:])) > 12
    rv[:, 3:-3] = (L[:, 3:-3] - np.maximum(L[:, :-6], L[:, 6:])) > 12
    hs = [(longest(rh[y, 100:1000]), y) for y in range(250, 1100)]
    hs = sorted([(l[0], y, 100 + l[1], 100 + l[2]) for l, y in hs], reverse=True)
    rows = []
    for l, y, x0, x1 in hs:
        if l < 150: break
        if all(abs(y - r[1]) > 8 for r in rows): rows.append((l, y, x0, x1))
        if len(rows) == 2: break
    vs = [(longest(rv[250:1100, x]), x) for x in range(100, 1000)]
    vs = sorted([(l[0], x, 250 + l[1], 250 + l[2]) for l, x in vs], reverse=True)
    cols = []
    for l, x, y0, y1 in vs:
        if l < 150: break
        if all(abs(x - c[1]) > 8 for c in cols): cols.append((l, x, y0, y1))
        if len(cols) == 2: break
    rows.sort(key=lambda r: r[1]); cols.sort(key=lambda c: c[1])
    s = f"f{a+k}"
    if len(rows) == 2 and len(cols) == 2:
        s += f"\t{rows[0][1]},{rows[0][2]}-{rows[0][3]}\t{rows[1][1]},{rows[1][2]}-{rows[1][3]}\t{cols[0][1]},{cols[0][2]}-{cols[0][3]}\t{cols[1][1]},{cols[1][2]}-{cols[1][3]}"
        s += f"\t{cols[1][1]-cols[0][1]}\t{rows[1][1]-rows[0][1]}\t({(cols[0][1]+cols[1][1])/2:.0f},{(rows[0][1]+rows[1][1])/2:.0f})"
    else:
        s += f"\tfilas={rows}\tcols={cols}"
    print(s)
