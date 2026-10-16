import json
import numpy as np
from nm import nelder_mead
from fit2 import bez
T = json.load(open("exit_tracks.json"))
def fit(name, f_lo, f_hi):
    rows = [(f, a) for f, a, b in T[name] if a is not None and f_lo <= f <= f_hi]
    fs = np.array([r[0] for r in rows], float); dy = np.array([r[1] for r in rows])
    def model(p):
        t0, N, D, x1, y1, x2, y2 = p
        t = np.clip((fs - t0) / N, 0, 1)
        return -D * bez(t, np.clip(x1, 0, 1), y1, np.clip(x2, 0, 1), y2)
    best = None
    for init in ([387, 33, 45, 0.7, 0.0, 0.8, 1.0], [387, 34, 45, 0.9, 0.05, 0.7, 1.0], [386, 36, 45, 0.6, 0.0, 0.6, 0.6], [387, 33, 45, 0.5, 0.0, 0.9, 0.3]):
        x, v = nelder_mead(lambda p: np.sum((model(p) - dy) ** 2), init, step=[1, 3, 2, 0.1, 0.05, 0.1, 0.1], iters=8000)
        if best is None or v < best[1]: best = (x, v)
    x, v = best
    print(f"{name}: inicio f{x[0]:.2f} N={x[1]:.1f} (fin f{x[0]+x[1]:.1f}) D={x[2]:.1f}px cubic-bezier({np.clip(x[3],0,1):.3f}, {x[4]:.3f}, {np.clip(x[5],0,1):.3f}, {x[6]:.3f}) rms={np.sqrt(v/len(fs)):.3f}")
    return x
x = fit("experiencia.", 382, 419)
fit("disfruta", 382, 419)
fit("Ponte", 382, 414)
fit("icono1", 382, 421)
fit("icono2", 382, 426)
# tabla progreso
rows = [(f, a, b) for f, a, b in T["experiencia."] if a is not None]
print("f: progreso posición (dy/-45) | brillo medido | (1-prog)^(1/2.2)")
for f, a, b in rows:
    if f >= 386:
        p = min(1, max(0, -a / 45.0))
        print(f"f{f}: {p*100:5.1f}%  {b*100:5.1f}%  {(1-p)**(1/2.2)*100:5.1f}%")
