"""Centroide subpíxel de la tinta blanca (o de un color) en una región, fotograma a fotograma.
uso: cen.py A:B --roi x0,y0,x1,y1(px) [--lo 185 --hi 245] [--color R,G,B --tol 70]
Devuelve cx, cy (centro de masas), masa, y los cuantiles 2/98 % en x e y (bordes robustos).
"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr
ap = argparse.ArgumentParser()
ap.add_argument("range"); ap.add_argument("--roi", required=True)
ap.add_argument("--lo", type=float, default=185); ap.add_argument("--hi", type=float, default=245)
ap.add_argument("--color"); ap.add_argument("--tol", type=float, default=70)
a = ap.parse_args()
f0, f1 = [int(v) for v in a.range.split(":")]
X0, Y0, X1, Y1 = [int(v) for v in a.roi.split(",")]
print("f\tcx\tcy\tmasa\tx02\tx98\ty02\ty98\tancho\talto")
for n in range(f0, f1 + 1):
    I = arr(n)[Y0:Y1, X0:X1]
    if a.color:
        col = np.array([float(v) for v in a.color.split(",")], np.float32)
        d = np.sqrt(((I - col) ** 2).sum(axis=2))
        w = np.clip(1 - d / a.tol, 0, 1)
    else:
        w = np.clip((I.min(axis=2) - a.lo) / (a.hi - a.lo), 0, 1)
    m = w.sum()
    if m < 20:
        print(f"{n}\t-\t-\t{m:.0f}"); continue
    xs = np.arange(X0, X1)[None, :]; ys = np.arange(Y0, Y1)[:, None]
    cx = (w * xs).sum() / m; cy = (w * ys).sum() / m
    px = w.sum(axis=0).cumsum() / m; py = w.sum(axis=1).cumsum() / m
    def q(p, c, o):
        i = np.searchsorted(c, p)
        i = min(max(i, 1), len(c) - 1)
        # interpolación lineal
        fr = (p - c[i - 1]) / max(c[i] - c[i - 1], 1e-9)
        return o + i - 1 + fr + 0.5
    x02, x98 = q(0.02, px, X0), q(0.98, px, X0); y02, y98 = q(0.02, py, Y0), q(0.98, py, Y0)
    print(f"{n}\t{cx:.2f}\t{cy:.2f}\t{m:.0f}\t{x02:.1f}\t{x98:.1f}\t{y02:.1f}\t{y98:.1f}\t{x98-x02:.1f}\t{y98-y02:.1f}")
