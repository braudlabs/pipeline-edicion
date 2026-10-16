"""Curva de entrada/salida de un rótulo: caja de la diferencia frente a un fotograma de fondo y alfa estimada.
uso: entry.py A:B --bg N --final N --roi x,y,w,h [--thr 30] [--color R,G,B]
  bg    = fotograma sin el rótulo (fondo de referencia)
  final = fotograma con el rótulo ya opaco (para la máscara)
"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr

ap = argparse.ArgumentParser()
ap.add_argument("range")
ap.add_argument("--bg", type=int, required=True)
ap.add_argument("--final", type=int, required=True)
ap.add_argument("--roi", default="0,0,1,1")
ap.add_argument("--thr", type=float, default=30)
ap.add_argument("--color", default="255,255,255")
ap.add_argument("--maskthr", type=float, default=60, help="distancia máxima al color para la máscara final")
a = ap.parse_args()
f0, f1 = [int(v) for v in a.range.split(":")]
x, y, w, h = [float(v) for v in a.roi.split(",")]
W, H = 1080, 1920
X0, Y0, X1, Y1 = int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)
col = np.array([float(v) for v in a.color.split(",")], np.float32)
B = arr(a.bg)[Y0:Y1, X0:X1]
F = arr(a.final)[Y0:Y1, X0:X1]
M = np.sqrt(((F - col) ** 2).sum(axis=2)) <= a.maskthr
# sensibilidad: solo donde el fondo dista del color del rótulo
sens = np.sqrt(((B - col) ** 2).sum(axis=2))
Ms = M & (sens > 120)
ys, xs = np.nonzero(M)
print(f"# roi px [{X0},{Y0}]-[{X1},{Y1}]  máscara final f{a.final}: {int(M.sum())} px, caja x {X0+xs.min()}-{X0+xs.max()} y {Y0+ys.min()}-{Y0+ys.max()}  (ancho {xs.max()-xs.min()+1}, alto {ys.max()-ys.min()+1}); px sensibles {int(Ms.sum())}")
print("f\talfa\tcaja_dif(x0,y0,x1,y1)\tancho\talto\tcx\tcy")
for n in range(f0, f1 + 1):
    I = arr(n)[Y0:Y1, X0:X1]
    # alfa por proyección sobre (col - B)
    num = ((I - B) * (col - B)).sum(axis=2)
    den = ((col - B) ** 2).sum(axis=2)
    al = num[Ms] / np.maximum(den[Ms], 1)
    alpha = float(np.median(al)) if Ms.any() else float('nan')
    d = np.sqrt(((I - B) ** 2).sum(axis=2))
    # hacia el color del rótulo: la diferencia debe acercar al color
    closer = (np.sqrt(((I - col) ** 2).sum(axis=2)) + a.thr) < np.sqrt(((B - col) ** 2).sum(axis=2))
    m = closer
    if m.sum() < 40:
        print(f"{n}\t{alpha:.2f}\t-")
        continue
    yy, xx = np.nonzero(m)
    bx0, bx1 = np.percentile(xx, [0.5, 99.5]); by0, by1 = np.percentile(yy, [0.5, 99.5])
    print(f"{n}\t{alpha:.2f}\t{X0+bx0:.0f},{Y0+by0:.0f},{X0+bx1:.0f},{Y0+by1:.0f}\t{bx1-bx0:.0f}\t{by1-by0:.0f}\t{X0+(bx0+bx1)/2:.0f}\t{Y0+(by0+by1)/2:.0f}\t(n={int(m.sum())})")
