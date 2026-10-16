"""Registro por correlación de fase de parches de fondo entre dos fotogramas (traslación subpíxel)."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from t import arr

def gray(n):
    return arr(n).mean(axis=2)

def phase_shift(a, b):
    """Desplazamiento (dx, dy) de b respecto de a (b(x) = a(x - d))."""
    a = a - a.mean(); b = b - b.mean()
    wy = np.hanning(a.shape[0])[:, None]; wx = np.hanning(a.shape[1])[None, :]
    A = np.fft.fft2(a * wy * wx); B = np.fft.fft2(b * wy * wx)
    R = np.conj(A) * B
    R /= np.maximum(np.abs(R), 1e-9)
    r = np.fft.ifft2(R).real
    i = np.unravel_index(np.argmax(r), r.shape)
    peak = r[i]
    def sub(v, k, n):
        # parábola
        c = v[k]; l = v[(k - 1) % n]; rr = v[(k + 1) % n]
        den = (l - 2 * c + rr)
        return 0 if den == 0 else 0.5 * (l - rr) / den
    dy = i[0] + sub(r[:, i[1]], i[0], r.shape[0]); dx = i[1] + sub(r[i[0], :], i[1], r.shape[1])
    if dy > r.shape[0] / 2: dy -= r.shape[0]
    if dx > r.shape[1] / 2: dx -= r.shape[1]
    return dx, dy, peak

if __name__ == "__main__":
    # reg.py fa fb x0,y0,x1,y1 [x0,y0,x1,y1 ...]
    fa, fb = int(sys.argv[1]), int(sys.argv[2])
    A, B = gray(fa), gray(fb)
    for r in sys.argv[3:]:
        x0, y0, x1, y1 = [int(v) for v in r.split(",")]
        dx, dy, pk = phase_shift(A[y0:y1, x0:x1], B[y0:y1, x0:x1])
        print(f"f{fa}->f{fb} parche [{x0},{y0}]-[{x1},{y1}]: dx={dx:+.2f} dy={dy:+.2f} pico={pk:.3f}")
