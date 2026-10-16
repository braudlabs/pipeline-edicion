#!/usr/bin/env python3
"""Tramos de tinta blanca por columnas (palabras/letras) en una banda, fotograma a fotograma.
  runs.py A B x0 y0 x1 y1 [thr=240] [gap=2] [axis=x|y]
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import frames
a, b, X0, Y0, X1, Y1 = [int(v) for v in sys.argv[1:7]]
thr = float(sys.argv[7]) if len(sys.argv) > 7 else 240
gap = int(sys.argv[8]) if len(sys.argv) > 8 else 2
axis = sys.argv[9] if len(sys.argv) > 9 else "x"
F = frames(a, b)
for k, im in enumerate(F):
    m = im[Y0:Y1, X0:X1].min(axis=2) >= thr
    prof = m.sum(axis=0 if axis == "x" else 1)
    on = prof >= 1
    runs = []
    i = 0
    n = len(on)
    while i < n:
        if on[i]:
            j = i
            last = i
            while j < n and (on[j] or j - last <= gap):
                if on[j]:
                    last = j
                j += 1
            runs.append((i, last))
            i = last + 1
        else:
            i += 1
    off = X0 if axis == "x" else Y0
    print(f"f{a+k}: " + "  ".join(f"{off+r0}-{off+r1}({r1-r0+1})" for r0, r1 in runs if r1 - r0 >= 2))
