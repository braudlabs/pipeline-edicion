import sys; sys.path.insert(0,'analysis/tmp/v7-ads90-rev-A')
from aud import *
from xcorr import ncc
def band(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1/sr)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)
bands = {'sub<110': (20, 110), 'graves110-300': (110, 300), 'voz300-3k': (300, 3000), 'agudos>5k': (5000, 16000)}
B7 = {k: band(m7, *v) for k, v in bands.items()}
B6 = {k: band(m6, *v) for k, v in bands.items()}
def best(A, B, t, w, span):
    win = int(w*sr); i = int(round(t*sr)); seg = A[i:i+win]
    lo = max(0, i-int(span*sr)); hi = min(len(B)-win, i+int(span*sr))
    r = ncc(B[lo:hi+win], seg); k = int(np.argmax(r))
    return (lo+k-i)/sr*60, float(r[k])
t0, t1, dt, w = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
print('t7\tf7\t' + '\t'.join(f'{k}(lag_f,corr)' for k in bands))
for t in np.arange(t0, t1+1e-9, dt):
    out = []
    for k in bands:
        lag, r = best(B7[k], B6[k], t, w, 0.5)
        out.append(f'{lag:+6.2f} {r:.2f}')
    print(f'{t:.2f}\t{t*60:.0f}\t' + '\t'.join(out))
