"""Alfa del rótulo por bloques de columnas (percentil alto del mapa de alfa por bloque) para ver si el fundido barre de izquierda a derecha.
uso: alpha_x.py A:B --bg N --roi x0,y0,x1,y1 [--color R,G,B] [--nb 10]"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr
ap = argparse.ArgumentParser()
ap.add_argument("range"); ap.add_argument("--bg", type=int, required=True)
ap.add_argument("--roi", required=True); ap.add_argument("--color", default="255,255,255"); ap.add_argument("--nb", type=int, default=10)
ap.add_argument("--minsens", type=float, default=110)
a = ap.parse_args()
f0, f1 = [int(v) for v in a.range.split(":")]
X0, Y0, X1, Y1 = [int(v) for v in a.roi.split(",")]
col = np.array([float(v) for v in a.color.split(",")], np.float32)
B = arr(a.bg)[Y0:Y1, X0:X1]
den = ((col - B) ** 2).sum(axis=2); ok = np.sqrt(den) > a.minsens
edges = np.linspace(0, X1 - X0, a.nb + 1).astype(int)
print("f\t" + "\t".join(f"x{X0+edges[i]}-{X0+edges[i+1]}" for i in range(a.nb)))
for n in range(f0, f1 + 1):
    I = arr(n)[Y0:Y1, X0:X1]
    al = ((I - B) * (col - B)).sum(axis=2) / np.maximum(den, 1)
    al[~ok] = np.nan
    row = []
    for i in range(a.nb):
        blk = al[:, edges[i]:edges[i + 1]]
        v = blk[~np.isnan(blk)]
        row.append(np.percentile(v, 92) if len(v) > 50 else float('nan'))
    print(f"{n}\t" + "\t".join(f"{v:.2f}" for v in row))
