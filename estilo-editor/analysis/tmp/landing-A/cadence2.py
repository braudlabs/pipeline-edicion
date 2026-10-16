import sys
import numpy as np
from la import *
a, b = int(sys.argv[1]), int(sys.argv[2])
x0, y0, x1, y1 = [int(v) for v in sys.argv[3].split(",")] if len(sys.argv) > 3 else (700, 100, 1900, 700)
F = frames(a, b)
prev = None; s = []
for f in range(a, b + 1):
    L = luma(F[f])[y0:y1, x0:x1]
    if prev is not None: s.append((f, float(np.abs(L - prev).mean())))
    prev = L
for i in range(0, len(s), 10):
    print(" ".join(f"f{f}:{d:5.2f}" for f, d in s[i:i+10]))
