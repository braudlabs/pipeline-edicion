import numpy as np
from nm import nelder_mead
dy = [48.33,43.05,38.55,34.71,31.54,28.73,26.42,24.30,22.37,20.65,19.03,17.66,16.36,15.03,13.89,12.83,11.84,10.92,10.11,9.36,8.60,7.83,7.19,6.62,5.95,5.50,4.91,4.51,4.01,3.65,3.22,2.87,2.57,2.23,1.95,1.73,1.50,1.20,1.01,0.87,0.73,0.58,0.45,0.29,0.18,0.10,0.06,0.03,0.01,0.0]
n = np.arange(1, len(dy) + 1, dtype=float)
dy = np.array(dy)
def bez(t, x1, y1, x2, y2):
    lo = np.zeros_like(t); hi = np.ones_like(t)
    for _ in range(50):
        s = (lo + hi)/2
        x = 3*(1-s)**2*s*x1 + 3*(1-s)*s**2*x2 + s**3
        lo = np.where(x < t, s, lo); hi = np.where(x >= t, s, hi)
    s = (lo + hi)/2
    return 3*(1-s)**2*s*y1 + 3*(1-s)*s**2*y2 + s**3
def model(p, n):
    D, N, n0, x1, y1, x2 = p
    x1 = np.clip(x1, 0, 1); x2 = np.clip(x2, 0, 1)
    t = np.clip((n - n0)/N, 0, 1)
    return D*(1 - bez(t, x1, y1, x2, 1.0))
best = None
for init in ([54, 50, 0, 0.2, 0.8, 0.3], [54, 50, 0, 0.1, 0.5, 0.5], [52, 49, 0.5, 0.05, 0.3, 0.2], [56, 50, 0, 0.3, 1.0, 0.6]):
    x, v = nelder_mead(lambda p: np.sum((model(p, n) - dy)**2), init)
    if best is None or v < best[1]: best = (x, v)
x, v = best
if __name__ == "__main__": print("bezier libre: D=%.2f N=%.2f n0=%.2f  cubic-bezier(%.3f, %.3f, %.3f, 1)  rms=%.3f" % (*x, np.sqrt(v/len(n))))
# con N=50, n0=0 fijos
x2_, v2_ = nelder_mead(lambda p: np.sum((model([p[0], 50, 0, p[1], p[2], p[3]], n) - dy)**2), [54, 0.2, 0.8, 0.3])
if __name__ == "__main__": print("bezier N=50 n0=0: D=%.2f cubic-bezier(%.3f, %.3f, %.3f, 1) rms=%.3f" % (*x2_, np.sqrt(v2_/len(n))))
if __name__ == "__main__":
    fs = {
        "expo 2^(-10 t)": (lambda p, n: p[0]*np.where((n-p[2]) < p[1], 2.0**(-10*(n-p[2])/p[1]), 0), [54, 50, 0]),
        "exp pura": (lambda p, n: p[0]*np.exp(-(n-p[2])/p[1]), [54, 11, 0]),
        "potencia (1-t)^m": (lambda p, n: p[0]*np.clip(1-(n-p[2])/p[1], 0, 1)**p[3], [54, 50, 0, 4]),
        "exp - recta (exp truncada)": (lambda p, n: p[0]*np.clip((np.exp(-(n-p[2])/p[1]) - np.exp(-p[3]/p[1]))/(1-np.exp(-p[3]/p[1])), 0, None)*((n-p[2])<p[3]), [54, 11, 0, 50]),
    }
    for name, (f, p0) in fs.items():
        xx, vv = nelder_mead(lambda p: np.sum((f(p, n) - dy)**2), p0)
        print(name, np.round(xx, 3), "rms=%.3f" % np.sqrt(vv/len(n)))
    print("n  medido  bezier")
    for k in range(0, 50, 2):
        print(int(n[k]), dy[k], round(float(model(x, n[k:k+1])[0]), 2))
