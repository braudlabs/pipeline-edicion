import numpy as np
from la import *
F = frames(380, 430)
R = luma(F[430])
els = {  # nombre: (x0, x1, y0, y1) asentado
 "icono1": (158, 226, 432, 500), "icono2": (234, 302, 432, 500),
 "Ponte": (163, 267, 515, 556), "auriculares": (269, 451, 515, 556),
 "y": (160, 186, 584, 622), "disfruta": (188, 310, 572, 613), "la": (314, 341, 572, 613), "experiencia.": (344, 545, 572, 622),
}
res = {}
for name, (x0, x1, y0, y1) in els.items():
    yA, yB = y0 - 5, y1 + 5
    c0 = None; rows = []
    for f in range(382, 430):
        d = (luma(F[f]) - R)[yA:yB, x0:x1 + 1]
        m = d > 10
        if m.sum() < 6:
            rows.append((f, np.nan, 0.0)); continue
        w = np.where(m, d, 0)
        c = (w.sum(1) * np.arange(yA, yB)).sum() / w.sum()
        b = float(np.percentile(d[m], 99))
        if c0 is None: c0, b0 = c, b
        rows.append((f, c - c0, b / b0))
        # mover ventana con el elemento
        sh = int(round(c - c0))
        yA, yB = y0 - 5 + sh, y1 + 5 + sh
    res[name] = rows
names = list(els)
print("f    " + "  ".join(f"{n[:11]:>13s}" for n in names))
for i, f in enumerate(range(382, 430)):
    print(f"f{f} " + "  ".join((f"{res[n][i][1]:+6.1f}/{res[n][i][2]*100:3.0f}%" if not np.isnan(res[n][i][1]) else "      -     ").rjust(13) for n in names))
import json
json.dump({n: [(f, None if np.isnan(a) else round(a, 2), round(b, 3)) for f, a, b in res[n]] for n in names}, open(OUT / "exit_tracks.json", "w"))
