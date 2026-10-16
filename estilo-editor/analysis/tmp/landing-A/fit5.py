"""Ajuste por palabra con inicio, duración N y recorrido D libres (bezier fijo). Ventanas limpias."""
import sys
import numpy as np
from la import *
from nm import nelder_mead
from fit2 import bez
import fit4
BEZ = (0.048, 0.158, 0.073, 1.0)
def fitword(name, ref, a, b, x0, x1, yA, yB, cfinal=None, fin=None, yAf=None, yBf=None, thr=10, show=False):
    R = luma(frames(ref, ref)[ref]); F = fit4.fr(a, b)
    rows = []
    for f in range(a, b + 1):
        cy, br, sm = fit4.centroid(luma(F[f]) - R, x0, x1, yA, yB, thr)
        if not np.isnan(cy): rows.append((f, cy, br))
    fs = np.array([r[0] for r in rows], float); cy = np.array([r[1] for r in rows]); br = np.array([r[2] for r in rows])
    if cfinal is None and fin is not None:
        Ff = fit4.fr(fin, fin + 3)
        cfinal = np.mean([fit4.centroid(luma(Ff[f]) - R, x0, x1, yAf or yA, yBf or yB, thr)[0] for f in Ff])
    def model(p):
        t0, N, D = p[0], p[1], p[2]
        c = p[3] if cfinal is None else cfinal
        t = np.clip((fs - t0) / N, 0, 1)
        return c + D * (1 - bez(t, *BEZ))
    p0 = [fs[0] - 0.5, 55, 50.25] + ([cy[-1]] if cfinal is None else [])
    best = None
    for N_init in (45, 55, 70, 90):
        p0[1] = N_init
        x, v = nelder_mead(lambda p: np.sum((model(p) - cy) ** 2), p0, step=[0.5, 8, 2] + ([1] if cfinal is None else []))
        if best is None or v < best[1]: best = (x, v)
    x, v = best
    # con D fijo 50.25
    def model2(p):
        c = p[2] if cfinal is None else cfinal
        t = np.clip((fs - p[0]) / p[1], 0, 1)
        return c + 50.25 * (1 - bez(t, *BEZ))
    q0 = [fs[0] - 0.5, x[1]] + ([cy[-1]] if cfinal is None else [])
    x2, v2 = nelder_mead(lambda p: np.sum((model2(p) - cy) ** 2), q0, step=[0.5, 5] + ([1] if cfinal is None else []))
    cfin = x[3] if cfinal is None else cfinal
    print(f"{name:13s} visible desde f{int(fs[0])} | libre: inicio f{x[0]:.2f} N={x[1]:.1f} D={x[2]:.1f} final_y={cfin:.1f} rms={np.sqrt(v/len(fs)):.2f} | D=50,25: inicio f{x2[0]:.2f} N={x2[1]:.1f} rms={np.sqrt(v2/len(fs)):.2f}  (fin f{x2[0]+x2[1]:.1f})")
    if show:
        print("   " + "  ".join(f"f{int(f)}:{c-cfin:+.2f}/{b:.0f}" for f, c, b in rows))
    return x2
if __name__ == "__main__":
    w = sys.argv[1]
    if w == "p2":
        fitword("Gracias", 8, 9, 85, 180, 314, 440, 660)
        fitword("por", 8, 26, 89, 316, 378, 440, 660)
        fitword("reservar.", 8, 43, 89, 380, 524, 440, 660)
        fitword("T", 8, 86, 123, 145, 176, 440, 660, fin=196, yAf=440, yBf=548)
        fitword("dejamos", 8, 96, 132, 202, 355, 440, 660, fin=196, yAf=440, yBf=548)
        fitword("un", 8, 105, 132, 357, 405, 440, 660, fin=196, yAf=440, yBf=548)
        fitword("mensaje", 8, 114, 142, 408, 560, 440, 660, fin=196, yAf=440, yBf=548)
        fitword("de", 8, 124, 200, 146, 200, 548, 700, fin=200)
        fitword("los", 8, 133, 200, 202, 251, 548, 700, fin=200)
        fitword("fundadores.", 8, 143, 204, 252, 460, 548, 700)
