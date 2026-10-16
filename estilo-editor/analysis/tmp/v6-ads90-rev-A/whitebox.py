#!/usr/bin/env python3
"""Caja de la tinta casi blanca (min(R,G,B) >= thr) por fotograma, con perfil de columnas/filas.
  whitebox.py A B x0 y0 x1 y1 [thr] [minrun]
Imprime: f, x0,x1,y0,y1 de la tinta, ancho, alto, área, y la media de min(RGB) en el percentil 99 (≈ opacidad).
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import frames

a, b, X0, Y0, X1, Y1 = [int(v) for v in sys.argv[1:7]]
thr = float(sys.argv[7]) if len(sys.argv) > 7 else 240
F = frames(a, b)
print("f\tx0\tx1\ty0\ty1\tw\th\tcx\tcy\tarea\tp99\tmax")
for k, im in enumerate(F):
    A = im[Y0:Y1, X0:X1].astype(np.float32)
    m = A.min(axis=2)
    mask = m >= thr
    n = int(mask.sum())
    p99 = float(np.percentile(m, 99))
    if n < 20:
        print(f"{a+k}\t-\t-\t-\t-\t-\t-\t-\t-\t{n}\t{p99:.0f}\t{m.max():.0f}")
        continue
    cols = np.nonzero(mask.sum(axis=0) >= 2)[0]
    rows = np.nonzero(mask.sum(axis=1) >= 2)[0]
    x0, x1, y0, y1 = X0 + cols[0], X0 + cols[-1], Y0 + rows[0], Y0 + rows[-1]
    print(f"{a+k}\t{x0}\t{x1}\t{y0}\t{y1}\t{x1-x0+1}\t{y1-y0+1}\t{(x0+x1)/2:.1f}\t{(y0+y1)/2:.1f}\t{n}\t{p99:.0f}\t{m.max():.0f}")
