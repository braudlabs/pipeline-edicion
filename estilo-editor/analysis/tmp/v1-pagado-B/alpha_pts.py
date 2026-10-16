"""Alfa de un rótulo en puntos concretos: proyección de (I-B) sobre (col-B), media 7x7.
uso: alpha_pts.py A:B --bg N --color R,G,B x,y [x,y ...]"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr
ap = argparse.ArgumentParser()
ap.add_argument("range"); ap.add_argument("--bg", type=int, required=True)
ap.add_argument("--color", default="255,255,255"); ap.add_argument("pts", nargs="+")
a = ap.parse_args()
f0, f1 = [int(v) for v in a.range.split(":")]
col = np.array([float(v) for v in a.color.split(",")], np.float32)
B = arr(a.bg)
pts = [tuple(int(v) for v in p.split(",")) for p in a.pts]
print("f\t" + "\t".join(f"({x},{y})" for x, y in pts) + "\tmediana")
for n in range(f0, f1 + 1):
    I = arr(n); row = []
    for x, y in pts:
        i = I[y - 3:y + 4, x - 3:x + 4].reshape(-1, 3).mean(axis=0); b = B[y - 3:y + 4, x - 3:x + 4].reshape(-1, 3).mean(axis=0)
        al = float(((i - b) * (col - b)).sum() / max(((col - b) ** 2).sum(), 1))
        row.append(al)
    print(f"{n}\t" + "\t".join(f"{v:.2f}" for v in row) + f"\t{np.median(row):.2f}")
