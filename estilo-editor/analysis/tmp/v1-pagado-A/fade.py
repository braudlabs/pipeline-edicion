#!/usr/bin/env python3
"""fade.py A B nombre:x0,y0,x1,y1 ...: opacidad estimada de la tinta blanca por región.
alfa ≈ (p98(min RGB) - fondo) / (253 - fondo), fondo = mediana de la región en el fotograma A-1... o percentil 30 local."""
import sys
import numpy as np
from tools import frames
a, b = int(sys.argv[1]), int(sys.argv[2])
regs = []
for s in sys.argv[3:]:
    n, r = s.split(":"); regs.append((n, [int(v) for v in r.split(",")]))
fr = frames(a, b)
print("f\t" + "\t".join(n for n, _ in regs))
for k, im in enumerate(fr):
    out = []
    for n, (x0, y0, x1, y1) in regs:
        c = im[y0:y1, x0:x1].astype(np.float32).min(axis=2)
        hi = np.percentile(c, 97); bg = np.percentile(c, 25)
        al = (hi - bg) / max(1, 253 - bg)
        out.append(f"p97={hi:.0f} bg={bg:.0f} a={al:.2f}")
    print(f"{a+k}\t" + "\t".join(out))
