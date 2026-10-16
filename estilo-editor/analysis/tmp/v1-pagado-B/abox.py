"""Caja del rótulo a partir del mapa de alfa (proyección sobre color-fondo), robusta durante el fundido.
uso: abox.py A:B --bg N --roi x,y,w,h [--color R,G,B] [--frac 0.5]
"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr
ap = argparse.ArgumentParser()
ap.add_argument("range"); ap.add_argument("--bg", type=int, required=True)
ap.add_argument("--roi", default="0,0,1,1"); ap.add_argument("--color", default="255,255,255")
ap.add_argument("--frac", type=float, default=0.5)
ap.add_argument("--minsens", type=float, default=110)
a = ap.parse_args()
f0, f1 = [int(v) for v in a.range.split(":")]
x, y, w, h = [float(v) for v in a.roi.split(",")]
W, H = 1080, 1920
X0, Y0, X1, Y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
col = np.array([float(v) for v in a.color.split(",")], np.float32)
B = arr(a.bg)[Y0:Y1, X0:X1]
den = ((col - B) ** 2).sum(axis=2)
ok = np.sqrt(den) > a.minsens
print(f"# roi px [{X0},{Y0}]-[{X1},{Y1}] bg f{a.bg}")
print("f\talfa90\tx0\ty0\tx1\ty1\tancho\talto\tcx\tcy\tn")
for n in range(f0, f1 + 1):
    I = arr(n)[Y0:Y1, X0:X1]
    al = ((I - B) * (col - B)).sum(axis=2) / np.maximum(den, 1)
    al[~ok] = 0
    top = float(np.percentile(al[ok], 97)) if ok.any() else 0
    if top < 0.12:
        print(f"{n}\t{top:.2f}\t-"); continue
    m = al > a.frac * top
    # limpia motas: exige vecindad
    mm = m[1:-1,1:-1] & m[:-2,1:-1] & m[2:,1:-1] & m[1:-1,:-2] & m[1:-1,2:]
    yy, xx = np.nonzero(mm)
    if len(xx) < 50:
        print(f"{n}\t{top:.2f}\t-"); continue
    bx0, bx1 = np.percentile(xx, [0.3, 99.7]); by0, by1 = np.percentile(yy, [0.3, 99.7])
    print(f"{n}\t{top:.2f}\t{X0+1+bx0:.0f}\t{Y0+1+by0:.0f}\t{X0+1+bx1:.0f}\t{Y0+1+by1:.0f}\t{bx1-bx0:.0f}\t{by1-by0:.0f}\t{X0+1+(bx0+bx1)/2:.1f}\t{Y0+1+(by0+by1)/2:.1f}\t{len(xx)}")
