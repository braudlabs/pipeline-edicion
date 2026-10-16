import numpy as np
from la import *
for name, a, b in (("plano3", 308, 507), ("plano5", 570, 749)):
    F = frames(a, b)
    print("##", name, "región x1700-1900 y20-420: media, pendiente horizontal (luma/100px), pendiente vertical; y columna x40-140 y100-900 media")
    for f in list(range(a, b + 1, 20)) + [b]:
        L = luma(F[f])
        R = L[20:420, 1700:1900]
        gx = np.polyfit(np.arange(200), R.mean(0), 1)[0] * 100
        gy = np.polyfit(np.arange(400), R.mean(1), 1)[0] * 100
        print(f"   f{f}: media {R.mean():6.2f}  gx {gx:+6.2f}  gy {gy:+6.2f} | izq {L[100:900, 40:140].mean():5.2f}")
