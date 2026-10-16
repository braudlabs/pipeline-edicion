#!/usr/bin/env python3
"""pts.py A B x,y [x,y...]: color (media 5x5) en puntos px para cada fotograma."""
import sys
import numpy as np
from tools import frames
a, b = int(sys.argv[1]), int(sys.argv[2])
P = [tuple(int(float(v)) for v in s.split(",")) for s in sys.argv[3:]]
print("f\t" + "\t".join(f"({x},{y})" for x, y in P))
for k, im in enumerate(frames(a, b)):
    out = []
    for x, y in P:
        c = im[max(0, y - 2):y + 3, max(0, x - 2):x + 3].reshape(-1, 3).astype(float).mean(axis=0)
        out.append(f"{c[0]:.0f},{c[1]:.0f},{c[2]:.0f}")
    print(f"{a+k}\t" + "\t".join(out))
