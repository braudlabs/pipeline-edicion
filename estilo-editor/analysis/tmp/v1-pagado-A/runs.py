#!/usr/bin/env python3
"""runs.py A B x0 y0 x1 y1 thr [mingap]: tramos de columnas con tinta (letras/palabras) y sus bordes subpíxel."""
import sys
import numpy as np
from tools import frames
a, b = int(sys.argv[1]), int(sys.argv[2])
X0, Y0, X1, Y1 = [int(v) for v in sys.argv[3:7]]
thr = float(sys.argv[7]); mingap = int(sys.argv[8]) if len(sys.argv) > 8 else 1
for k, im in enumerate(frames(a, b)):
    c = im[Y0:Y1, X0:X1].astype(np.float32).min(axis=2)
    al = np.clip((c - (thr - 20)) / 40, 0, 1)          # rampa suave ±20 alrededor del umbral
    col = al.sum(axis=0)
    on = col > 1.0
    runs = []; i = 0; n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j + 1 < n and (on[j + 1] or (j + 1 + mingap < n and on[j + 1:j + 1 + mingap].any())): j += 1
            # borde subpíxel: interpolación al nivel 1.0
            l = i - (col[i] - 1.0) / max(1e-6, col[i] - (col[i - 1] if i > 0 else 0)) if i > 0 else i
            r = j + (col[j] - 1.0) / max(1e-6, col[j] - (col[j + 1] if j + 1 < n else 0)) if j + 1 < n else j
            runs.append((X0 + l, X0 + r)); i = j + 1
        else: i += 1
    rows = al.sum(axis=1); rr = np.nonzero(rows > 1.0)[0]
    ytxt = f"y {Y0+rr.min()}-{Y0+rr.max()}" if len(rr) else "y -"
    print(f"f{a+k}\t{ytxt}\t" + "  ".join(f"[{l:.1f}-{r:.1f}]" for l, r in runs))
