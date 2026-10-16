import numpy as np
from la import *
np.set_printoptions(linewidth=250, suppress=True)
F = frames(8, 60)
R = luma(F[8])
# desplazamientos medidos (y0 del rótulo) para alinear
y0 = {9: 566, 10: 561, 11: 556, 12: 553, 14: 547, 18: 539, 26: 529, 40: 521, 60: 519}
for f in (9, 10, 11, 12, 14, 18, 26, 40, 60):
    D = luma(F[f]) - R
    sub = D[y0[f] - 3: y0[f] + 42, 180:316]
    # perfil vertical medio (por filas) normalizado y perfil horizontal en la zona media de la palabra
    rowp = sub.mean(1)
    # trazo horizontal de la G (barra) : columnas ~ 205..222 relativas? buscamos la fila con más tinta entre filas 15..25
    colp = sub[10:30].mean(0)
    print(f"f{f} max={sub.max():.0f}  suma total={sub.clip(0).sum():.0f}  (suma/max={sub.clip(0).sum()/sub.max():.0f})")
    print("  filas:", " ".join(f"{v:4.0f}" for v in rowp))
# anchura de la 'i' (astil vertical): perfil horizontal sobre el astil
for f in (9, 10, 11, 12, 14, 18, 26, 60):
    D = luma(F[f]) - R
    sub = D[y0[f] + 12: y0[f] + 34, 268:290]   # zona de la i
    p = sub.mean(0)
    print(f"f{f} perfil horiz i:", " ".join(f"{v:4.0f}" for v in p), " | norm:", " ".join(f"{v/p.max():.2f}" for v in p))
