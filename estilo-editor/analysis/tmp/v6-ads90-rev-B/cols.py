"""Perfil de columnas/filas de la tinta blanca (o de color) en una caja: localiza palabras y huecos.
  cols.py F x0,y0,x1,y1 [thr] [slug] [color R,G,B cthr]"""
import sys
import numpy as np
from lib import run, arr
f = int(sys.argv[1]); x0, y0, x1, y1 = [int(v) for v in sys.argv[2].split(',')]
thr = float(sys.argv[3]) if len(sys.argv) > 3 else 236
slug = sys.argv[4] if len(sys.argv) > 4 else 'v6-ads90-rev'
A = arr(run(f, f, slug)[0])[y0:y1, x0:x1]
if len(sys.argv) > 5:
    col = np.array([float(v) for v in sys.argv[5].split(',')]); cthr = float(sys.argv[6])
    M = np.sqrt(((A - col) ** 2).sum(axis=2)) <= cthr
else:
    M = A.min(axis=2) >= thr
cols = M.sum(axis=0); rows = M.sum(axis=1)
def runs(v, off):
    out = []; on = False
    for i, c in enumerate(v):
        if c > 0 and not on: s = i; on = True
        if c == 0 and on: out.append((off + s, off + i - 1)); on = False
    if on: out.append((off + s, off + len(v) - 1))
    return out
print('columnas con tinta:', runs(cols, x0))
print('filas con tinta   :', runs(rows, y0))
print('área', int(M.sum()))
