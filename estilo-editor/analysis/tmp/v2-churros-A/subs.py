"""Seguimiento de la tinta blanca de los subtítulos, fotograma a fotograma, en una región.
uso: subs.py f0 f1 x0 y0 x1 y1 [thr] [sat]   (px)  -> tramos con caja constante"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import fr

def box(A, roi, thr=232, sat=14, minrow=2):
    x0, y0, x1, y1 = roi
    S = A[y0:y1, x0:x1]; g = S.min(axis=2); m = (g >= thr) & ((S.max(axis=2) - g) <= sat)
    rows = m.sum(axis=1); cols = m.sum(axis=0)
    ys = np.nonzero(rows >= minrow)[0]; xs = np.nonzero(cols >= minrow)[0]
    if len(ys) == 0 or m.sum() < 60: return None
    big = np.nonzero(rows >= 0.5 * rows.max())[0]
    return (x0 + xs[0], y0 + ys[0], x0 + xs[-1], y0 + ys[-1], int(m.sum()), y0 + big[0], y0 + big[-1])

def track(f0, f1, roi, thr=232, sat=14):
    out = []
    for n in range(f0, f1 + 1):
        out.append((n, box(fr(n), roi, thr, sat)))
    return out

def runs(tr, tol=2, atol=0.06):
    res = []; cur = None
    for n, b in tr:
        if cur and ((b is None and cur[2] is None) or (b is not None and cur[2] is not None and all(abs(b[i] - cur[2][i]) <= tol for i in range(4)) and abs(b[4] - cur[2][4]) <= atol * cur[2][4])):
            cur[1] = n
        else:
            cur = [n, n, b]; res.append(cur)
    return res

if __name__ == "__main__":
    a = [int(v) for v in sys.argv[1:7]]
    thr = int(sys.argv[7]) if len(sys.argv) > 7 else 232
    sat = int(sys.argv[8]) if len(sys.argv) > 8 else 14
    tr = track(a[0], a[1], tuple(a[2:6]), thr, sat)
    for s, e, b in runs(tr):
        if b is None:
            print(f"f{s}-f{e} ({e-s+1} f): sin tinta")
        else:
            print(f"f{s}-f{e} ({e-s+1} f): x {b[0]}-{b[2]} (ancho {b[2]-b[0]+1}, cx {(b[0]+b[2])/2:.0f}) y {b[1]}-{b[3]} (alto {b[3]-b[1]+1}) área {b[4]}  banda-x {b[5]}-{b[6]}")
