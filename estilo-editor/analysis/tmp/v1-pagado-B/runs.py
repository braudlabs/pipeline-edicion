"""Tramos de columnas (o filas) con tinta en una banda: bordes de letras al píxel.
uso: runs.py f1,f2,... --roi x0,y0,x1,y1 [--thr 235] [--color R,G,B --tol 60] [--axis x|y] [--min 2]
"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr
ap = argparse.ArgumentParser()
ap.add_argument("frames"); ap.add_argument("--roi", required=True)
ap.add_argument("--thr", type=float, default=235); ap.add_argument("--color"); ap.add_argument("--tol", type=float, default=60)
ap.add_argument("--axis", default="x"); ap.add_argument("--min", type=int, default=2)
a = ap.parse_args()
if ":" in a.frames:
    p = [int(v) for v in a.frames.split(":")]; frames = range(p[0], p[1] + 1, p[2] if len(p) > 2 else 1)
else:
    frames = [int(v) for v in a.frames.split(",")]
X0, Y0, X1, Y1 = [int(v) for v in a.roi.split(",")]
for n in frames:
    I = arr(n)[Y0:Y1, X0:X1]
    if a.color:
        col = np.array([float(v) for v in a.color.split(",")], np.float32)
        m = np.sqrt(((I - col) ** 2).sum(axis=2)) <= a.tol
    else:
        m = I.min(axis=2) >= a.thr
    prof = m.sum(axis=0 if a.axis == "x" else 1)
    o = X0 if a.axis == "x" else Y0
    runs = []; s = None
    for i, c in enumerate(prof):
        if c >= a.min and s is None: s = i
        if c < a.min and s is not None:
            runs.append((o + s, o + i - 1)); s = None
    if s is not None: runs.append((o + s, o + len(prof) - 1))
    print(n, " ".join(f"{p}-{q}" for p, q in runs))
