"""Cadencia del metraje: diferencia entre fotogramas consecutivos en una región sin rótulos (mitad derecha superior)."""
import sys
import numpy as np
from la import *
a, b = int(sys.argv[1]), int(sys.argv[2])
x0, y0, x1, y1 = [int(v) for v in sys.argv[3].split(",")] if len(sys.argv) > 3 else (700, 100, 1900, 700)
F = frames(a, b)
prev = None; s = []
for f in range(a, b + 1):
    L = luma(F[f])[y0:y1, x0:x1]
    if prev is not None:
        s.append((f, float(np.abs(L - prev).mean())))
    prev = L
line = "".join("N" if d > 0.12 else "." for f, d in s)
print(f"f{a+1}..f{b}  (N = fotograma nuevo de metraje, . = repetido) umbral 0.12")
for i in range(0, len(line), 60):
    print(f"f{a+1+i:4d} {line[i:i+60]}")
new = [f for f, d in s if d > 0.12]
gaps = np.diff(new)
import collections
print("huecos entre fotogramas nuevos:", dict(collections.Counter(gaps.tolist())))
if len(new) > 1:
    print(f"fps de metraje estimado: {60*(len(new)-1)/(new[-1]-new[0]):.2f}")
print("dif media en nuevos: %.2f ; en repetidos: %.3f" % (np.mean([d for f, d in s if d > 0.12]), np.mean([d for f, d in s if d <= 0.12] or [0])))
