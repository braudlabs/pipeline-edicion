import numpy as np, itertools
rows = [l.rstrip("\n").split("\t") for l in open("subs2_0_118.tsv")][1:]
data = {}
for r in rows:
    if len(r) < 8 or r[2] in ("¿Y",): continue
    data[int(r[0])] = float(r[7])
B = np.mean([v for f, v in data.items() if 76 <= f <= 88])
print("base final", round(B, 2))
fs = np.array(sorted(f for f in data if f <= 88)); s = np.array([1 + (data[f] - B) / (B - 960) for f in fs])
print(" ".join(f"f{f}:{v:.4f}" for f, v in zip(fs, s)))

def bez(t, x1, y1, x2, y2):
    # resuelve x(u)=t por bisección vectorizada
    lo = np.zeros_like(t); hi = np.ones_like(t)
    for _ in range(40):
        u = (lo + hi) / 2
        x = 3 * (1 - u) ** 2 * u * x1 + 3 * (1 - u) * u ** 2 * x2 + u ** 3
        lo = np.where(x < t, u, lo); hi = np.where(x >= t, u, hi)
    u = (lo + hi) / 2
    return 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u ** 2 * y2 + u ** 3

best = None
A = s[0] - 1
for D in (66, 68, 70, 72, 74, 76, 78, 80, 84, 90, 96):
    t = np.clip(fs / D, 0, 1)
    for x1 in np.arange(0.0, 0.5, 0.05):
        for y1 in np.arange(0.0, 1.01, 0.1):
            for x2 in np.arange(0.0, 0.8, 0.05):
                p = bez(t, x1, y1, x2, 1.0)
                err = np.sqrt(np.mean((1 + A * (1 - p) - s) ** 2))
                if best is None or err < best[0]:
                    best = (err, D, x1, y1, x2)
print("mejor bezier (y2=1): rms=%.5f D=%d x1=%.2f y1=%.2f x2=%.2f" % best)
# curvas estándar
t = lambda D: np.clip(fs / D, 0, 1)
cands = {
 "outCubic": lambda x: 1 - (1 - x) ** 3, "outQuart": lambda x: 1 - (1 - x) ** 4, "outQuint": lambda x: 1 - (1 - x) ** 5,
 "outExpo": lambda x: np.where(x >= 1, 1, 1 - 2 ** (-10 * x)), "outCirc": lambda x: np.sqrt(1 - (x - 1) ** 2),
 "outQuad": lambda x: 1 - (1 - x) ** 2, "outSine": lambda x: np.sin(x * np.pi / 2)}
for name, fn in cands.items():
    bb = min(((np.sqrt(np.mean((1 + A * (1 - fn(t(D))) - s) ** 2)), D) for D in range(40, 200, 2)))
    print(f"{name}: rms={bb[0]:.5f} D={bb[1]}")
# exponencial con tau
bb = min(((np.sqrt(np.mean((1 + A * np.exp(-fs / tau) - s) ** 2)), tau) for tau in np.arange(10, 40, 0.5)))
print("exp tau: rms=%.5f tau=%.1f" % bb)
# muelle críticamente amortiguado: (1+w t) e^{-w t}
bb = min(((np.sqrt(np.mean((1 + A * (1 + w * fs) * np.exp(-w * fs) - s) ** 2)), w) for w in np.arange(0.02, 0.4, 0.002)))
print("muelle crit: rms=%.5f w=%.3f" % bb)
err, D, x1, y1, x2 = best
p = bez(np.clip(fs / D, 0, 1), x1, y1, x2, 1.0)
print(" ".join(f"f{f}:{1 + A*(1-v):.4f}" for f, v in zip(fs, p)))
