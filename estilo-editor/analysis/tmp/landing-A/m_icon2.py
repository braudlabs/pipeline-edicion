import numpy as np
from la import *
F = frames(208, 345)
yy, xx = np.mgrid[0:1080, 0:1920]
def ring_stats(f, cx, cy, r=30.0):
    L = luma(F[f])
    x0, x1, y0, y1 = int(cx-36), int(cx+37), int(cy-36), int(cy+37)
    sub = L[y0:y1, x0:x1]; X = xx[y0:y1, x0:x1]; Y = yy[y0:y1, x0:x1]
    rad = np.hypot(X-cx, Y-cy)
    ang = (np.degrees(np.arctan2(X-cx, -(Y-cy))) + 360) % 360   # 0 = arriba, sentido horario
    bg = np.median(sub[rad > 34])
    ringm = (rad >= r-1.6) & (rad <= r+1.6)
    lit = np.zeros(72); val = np.zeros(72)
    for k in range(72):
        sel = ringm & (ang >= k*5) & (ang < k*5+5)
        v = sub[sel].max() - bg
        val[k] = v; lit[k] = v > 25
    inner = (rad < r-3)
    ink_in = np.clip(sub[inner] - bg - 15, 0, None).sum()
    # ángulo final del arco contiguo desde arriba
    k = 0
    while k < 72 and lit[k]: k += 1
    # brillo medio del arco encendido y perfil de brillo (cola)
    return k*5, int(lit.sum())*5, ink_in, val
for name, (cx, cy) in {"icono1": (191.5, 463.9), "icono2": (267.6, 464.8)}.items():
    print("##", name)
    fin = ring_stats(345, cx, cy)[2]
    for f in range(208, 346):
        a, tot, ink, val = ring_stats(f, cx, cy)
        if tot == 0 and ink < 20: continue
        tail = ""
        print(f"f{f}: arco contiguo desde 12h = {a:3d}°  total encendido {tot:3d}°  tinta interior {ink/fin*100:5.1f}%")
