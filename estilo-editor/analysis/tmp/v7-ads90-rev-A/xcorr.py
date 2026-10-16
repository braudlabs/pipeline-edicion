import sys; sys.path.insert(0,'analysis/tmp/v7-ads90-rev-A')
from aud import *
def ncc(ref, seg):
    n = len(ref) + len(seg) - 1
    N = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(ref, N) * np.conj(np.fft.rfft(seg, N)), N)[:len(ref) - len(seg) + 1]
    cs = np.concatenate([[0], np.cumsum(ref.astype(np.float64) ** 2)])
    e = np.sqrt((cs[len(seg):] - cs[:-len(seg)]) * (seg.astype(np.float64) ** 2).sum()) + 1e-12
    return c / e
def best(t, w=0.25, span=0.6, A=None, B=None):
    A = m7 if A is None else A; B = m6 if B is None else B
    win = int(w * sr); i = int(round(t * sr)); seg = A[i:i + win]
    lo = max(0, i - int(span * sr)); hi = min(len(B) - win, i + int(span * sr))
    r = ncc(B[lo:hi + win], seg)
    k = int(np.argmax(r))
    return (lo + k - i) / sr, float(r[k])
if __name__ == '__main__':
    t0, t1, dt = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    w = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
    print('t7(s)\tf7\tlag(s)\tlag(f)\tlag(muestras)\tcorr')
    for t in np.arange(t0, t1 + 1e-9, dt):
        lag, r = best(t, w)
        print(f'{t:.3f}\t{t*60:.1f}\t{lag:+.4f}\t{lag*60:+.2f}\t{lag*sr:+.0f}\t{r:.3f}')
