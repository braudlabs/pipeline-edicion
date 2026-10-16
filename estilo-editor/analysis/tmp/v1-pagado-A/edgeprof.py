#!/usr/bin/env python3
"""edgeprof.py A B eje x0 y0 x1 y1 [dir]: posición subpíxel del borde (cruce al 50 % entre fondo y tinta) en un perfil.
eje=v: perfil vertical (media por filas) -> y del borde; eje=h: perfil horizontal -> x del borde.
dir=+ : el fondo está al principio del perfil y la tinta después; dir=- : al revés."""
import sys
import numpy as np
from tools import frames
a, b, eje = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
X0, Y0, X1, Y1 = [int(v) for v in sys.argv[4:8]]
d = sys.argv[8] if len(sys.argv) > 8 else "+"
for k, im in enumerate(frames(a, b)):
    c = im[Y0:Y1, X0:X1].astype(np.float32).min(axis=2)
    p = c.mean(axis=1) if eje == "v" else c.mean(axis=0)
    if d == "-": p = p[::-1]
    bg = np.median(p[:6]); ink = np.percentile(p, 97)
    if ink - bg < 12:
        print(f"f{a+k}\t-\t(bg {bg:.0f} tinta {ink:.0f})"); continue
    half = (bg + ink) / 2
    i = int(np.argmax(p >= half))
    pos = i - 1 + (half - p[i - 1]) / max(1e-6, p[i] - p[i - 1]) if i > 0 else 0.0
    if d == "-": pos = len(p) - 1 - pos
    off = Y0 if eje == "v" else X0
    print(f"f{a+k}\t{off+pos:.1f}\t(bg {bg:.0f} tinta {ink:.0f} alfa~{(ink-bg)/(253-bg):.2f})")
