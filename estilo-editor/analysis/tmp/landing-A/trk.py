"""Seguimiento de palabras: caja y brillo por fotograma dentro de rangos de columnas."""
import sys
import numpy as np
from la import *

def runs_x(mask, x_off, mingap=6):
    cols = mask.sum(0) > 0
    runs = []; on = False; s = 0
    for x in range(len(cols)):
        if cols[x] and not on: on = True; s = x
        if not cols[x] and on:
            on = False; runs.append([s + x_off, x - 1 + x_off])
    if on: runs.append([s + x_off, len(cols) - 1 + x_off])
    # fusionar tramos separados por menos de mingap
    out = []
    for r in runs:
        if out and r[0] - out[-1][1] <= mingap: out[-1][1] = r[1]
        else: out.append(r)
    return out

def layout(f, roi, ref=None, thr=25, mingap=6):
    """roi=(x0,y0,x1,y1) px. Devuelve tramos de tinta en x y caja global."""
    F = frames(f, f)[f]
    L = luma(F)[roi[1]:roi[3], roi[0]:roi[2]]
    if ref is not None:
        R = luma(frames(ref, ref)[ref])[roi[1]:roi[3], roi[0]:roi[2]]
        D = L - R
    else:
        D = L - np.median(L)
    m = D > thr
    ys, xs = np.nonzero(m)
    print(f"f{f} tinta: x {xs.min()+roi[0]}..{xs.max()+roi[0]}  y {ys.min()+roi[1]}..{ys.max()+roi[1]}  max luma {L.max():.0f}")
    r = runs_x(m, roi[0], mingap)
    print("tramos x (fusionados con hueco<=%d):" % mingap, r)
    return r

if __name__ == "__main__":
    f = int(sys.argv[1]); roi = [int(v) for v in sys.argv[2].split(",")]
    ref = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] != "-" else None
    thr = float(sys.argv[4]) if len(sys.argv) > 4 else 25
    mg = int(sys.argv[5]) if len(sys.argv) > 5 else 6
    layout(f, roi, ref, thr, mg)
