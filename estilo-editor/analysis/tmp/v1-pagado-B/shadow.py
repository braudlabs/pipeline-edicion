"""¿Hay sombra/halo alrededor del texto? Compara un fotograma con texto y otro contiguo sin texto, por anillos de distancia a la máscara.
uso: shadow.py f_con f_sin x0,y0,x1,y1 [thr]"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr
fa, fb = int(sys.argv[1]), int(sys.argv[2])
X0, Y0, X1, Y1 = [int(v) for v in sys.argv[3].split(",")]
thr = float(sys.argv[4]) if len(sys.argv) > 4 else 215
A = arr(fa)[Y0:Y1, X0:X1]; B = arr(fb)[Y0:Y1, X0:X1]
m = A.min(axis=2) >= thr
# no contar blancos que ya estaban en el fondo
m &= ~(B.min(axis=2) >= thr)
# distancia por dilataciones sucesivas (chebyshev)
dist = np.full(m.shape, 99, int); cur = m.copy(); dist[cur] = 0
for d in range(1, 26):
    nxt = cur.copy()
    nxt[1:, :] |= cur[:-1, :]; nxt[:-1, :] |= cur[1:, :]; nxt[:, 1:] |= cur[:, :-1]; nxt[:, :-1] |= cur[:, 1:]
    nxt[1:, 1:] |= cur[:-1, :-1]; nxt[:-1, :-1] |= cur[1:, 1:]; nxt[1:, :-1] |= cur[:-1, 1:]; nxt[:-1, 1:] |= cur[1:, :-1]
    dist[nxt & ~cur] = d; cur = nxt
dl = (A.mean(axis=2) - B.mean(axis=2))
print(f"f{fa} (con) - f{fb} (sin): tinta {int(m.sum())} px")
for d in (1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25):
    s = dist == d
    if s.sum(): print(f"  anillo d={d:2d}: n={int(s.sum()):6d}  dif media {dl[s].mean():+6.2f}  mediana {np.median(dl[s]):+6.2f}")
s = dist == 99
print(f"  lejos (>25): dif media {dl[s].mean():+.2f} mediana {np.median(dl[s]):+.2f}")
