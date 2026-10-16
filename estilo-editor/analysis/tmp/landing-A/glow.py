"""Perfil del resplandor del fondo en una banda superior (solo fondo): centro y anchura por fotograma -> detecta zoom/paneo."""
import numpy as np
from la import *
def prof(f, y0, y1, x0, x1):
    L = luma(frames(f, f)[f])[y0:y1, x0:x1].mean(0)
    L = L - L.min()
    xs = np.arange(x0, x1)
    c = (L * xs).sum() / L.sum()
    s = np.sqrt((L * (xs - c) ** 2).sum() / L.sum())
    return c, s, L.max() + 0, float(luma(frames(f, f)[f])[y0:y1, x0:x1].mean())
for name, fs, band in (("plano1", (1, 30, 60, 90, 120, 150, 180, 210, 214), (30, 110, 200, 1300)),
                       ("plano2", (215, 230, 250, 270, 290, 307), (4, 40, 100, 1500)),
                       ("plano3", (308, 340, 380, 420, 460, 500, 507), (4, 60, 800, 1920)),
                       ("plano4", (508, 520, 540, 560, 569), (4, 60, 200, 1700)),
                       ("plano5", (570, 600, 640, 680, 720, 749), (4, 60, 800, 1920))):
    print("##", name, "banda y%d-%d x%d-%d" % band)
    for f in fs:
        c, s, mx, mean = prof(f, *band)
        print(f"   f{f}: centro x={c:7.1f}  anchura σ={s:6.1f}  pico={mx:5.1f}  media={mean:5.1f}")
