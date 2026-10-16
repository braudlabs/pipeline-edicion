"""Perfil de sombra: diferencia entre dos fotogramas con el mismo fotograma de origen y distinto rótulo,
en función de la distancia a la tinta del rótulo nuevo."""
import sys; sys.path.insert(0,'analysis/tmp/v7-ads90-rev-A')
from h import *
def dist_map(mask, maxd=60):
    # distancia aproximada (chebyshev->euclídea por dilataciones sucesivas con disco)
    H, W = mask.shape
    D = np.full((H, W), maxd+1, np.float32)
    D[mask] = 0
    cur = mask.copy()
    # distancia euclídea exacta por fuerza bruta en ventana reducida usando transformada 1D de dos pasadas
    INF = 1e9
    f = np.where(mask, 0.0, INF).astype(np.float64)
    # pasada por columnas luego filas (Felzenszwalb simplificado con límite maxd)
    def edt1d(f):
        n = len(f); d = np.empty(n); v = np.zeros(n, int); z = np.empty(n+1); k = 0
        v[0] = 0; z[0] = -INF; z[1] = INF
        for q in range(1, n):
            while True:
                s = ((f[q]+q*q)-(f[v[k]]+v[k]*v[k]))/(2*q-2*v[k])
                if s <= z[k]: k -= 1
                else: break
            k += 1; v[k] = q; z[k] = s; z[k+1] = INF
        k = 0
        for q in range(n):
            while z[k+1] < q: k += 1
            d[q] = (q-v[k])**2 + f[v[k]]
        return d
    g = np.empty_like(f)
    for x in range(W): g[:, x] = edt1d(f[:, x])
    for y in range(H): g[y] = edt1d(g[y])
    return np.sqrt(g)
if __name__ == '__main__':
    slug = sys.argv[1]; fa, fb = int(sys.argv[2]), int(sys.argv[3])   # fa: sin el rótulo nuevo, fb: con el rótulo nuevo
    roi = [int(v) for v in sys.argv[4].split(',')]
    F = frames(slug, min(fa, fb), max(fa, fb))
    x0, y0, x1, y1 = roi
    A = F[fa][y0:y1, x0:x1].astype(np.float32); B = F[fb][y0:y1, x0:x1].astype(np.float32)
    thr = int(sys.argv[5]) if len(sys.argv) > 5 else 250
    ma = A.min(2) >= thr; mb = B.min(2) >= thr
    print("tinta A", int(ma.sum()), "tinta B", int(mb.sum()))
    # tinta nueva: blanca en B. tinta vieja: blanca en A
    da = dist_map(ma); db = dist_map(mb)
    LA = A.mean(2); LB = B.mean(2)
    print('dist_px\tn\tratio B/A (mediana)\tdif B-A (media)\tA medio')
    for lo, hi in [(2,4),(4,6),(6,8),(8,10),(10,13),(13,16),(16,20),(20,25),(25,30),(30,40),(40,55)]:
        sel = (db >= lo) & (db < hi) & (da > 45) & (LA > 60)
        if sel.sum() < 200: print(f'{lo}-{hi}\t{int(sel.sum())}\t-'); continue
        print(f'{lo}-{hi}\t{int(sel.sum())}\t{np.median(LB[sel]/LA[sel]):.3f}\t{(LB[sel]-LA[sel]).mean():+.2f}\t{LA[sel].mean():.0f}')
