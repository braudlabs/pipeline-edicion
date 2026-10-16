#!/usr/bin/env python3
"""Centroide subpíxel de cada tramo de tinta blanca (palabra) en una banda, fotograma a fotograma.
  track.py A B x0 y0 x1 y1 [thr=240] [gap=2] [lo=225]
Por tramo: x0-x1, centroide x (ponderado por min(RGB)-lo), centroide y, masa.
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import frames
a, b, X0, Y0, X1, Y1 = [int(v) for v in sys.argv[1:7]]
thr = float(sys.argv[7]) if len(sys.argv) > 7 else 240
gap = int(sys.argv[8]) if len(sys.argv) > 8 else 2
lo = float(sys.argv[9]) if len(sys.argv) > 9 else 225
F = frames(a, b)
for k, im in enumerate(F):
    mn = im[Y0:Y1, X0:X1].min(axis=2).astype(np.float32)
    m = mn >= thr
    w = np.clip(mn - lo, 0, None)
    on = m.sum(axis=0) >= 1
    runs = []
    i, n = 0, len(on)
    while i < n:
        if on[i]:
            j = last = i
            while j < n and (on[j] or j - last <= gap):
                if on[j]:
                    last = j
                j += 1
            runs.append((i, last))
            i = last + 1
        else:
            i += 1
    out = []
    for r0, r1 in runs:
        if r1 - r0 < 6:
            continue
        s0, s1 = max(0, r0 - 3), min(n, r1 + 4)
        ww = w[:, s0:s1]
        tot = ww.sum()
        if tot <= 0:
            continue
        cx = (ww.sum(axis=0) * np.arange(s0, s1)).sum() / tot + X0
        cy = (ww.sum(axis=1) * np.arange(ww.shape[0])).sum() / tot + Y0
        out.append(f"[{X0+r0}-{X0+r1} w{r1-r0+1} cx{cx:.2f} cy{cy:.2f} m{tot/1000:.0f}]")
    print(f"f{a+k}: " + " ".join(out))
