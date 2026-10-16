import sys; sys.path.insert(0,'analysis/tmp/v7-ads90-rev-A')
from h import *
a, b = int(sys.argv[1]), int(sys.argv[2])
k0, k1 = int(sys.argv[3]), int(sys.argv[4])
F = frames('v7-ads90-rev', a, b)
G = frames('v6-ads90-rev', a + k0, b + k1)
def g(A):
    L = A[::2, ::2].astype(np.float32).mean(2)
    gx = L[1:-1,2:]-L[1:-1,:-2]; gy = L[2:,1:-1]-L[:-2,1:-1]
    m = np.sqrt(gx*gx+gy*gy)
    m[400:560]=0
    return m - m.mean()
gF = {n: g(F[n]) for n in F}; gG = {n: g(G[n]) for n in G}
def corr(a,b): return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()))
print('f7\t' + '\t'.join(f'k={k:+d}' for k in range(k0, k1+1)) + '\tmejor')
for n in range(a, b+1):
    row = [corr(gF[n], gG[n+k]) for k in range(k0, k1+1)]
    mx = max(row)
    best = [k for k, r in zip(range(k0, k1+1), row) if r > mx - 0.004]
    print(f'{n}\t' + '\t'.join(f'{r:.3f}' for r in row) + f'\t{best}')
