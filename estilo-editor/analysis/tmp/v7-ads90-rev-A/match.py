import sys
import numpy as np
from PIL import Image
from pathlib import Path
R = Path('analysis/frames')
def lo(slug, n):
    p = R / slug / f'f{n:06d}.jpg'
    return np.asarray(Image.open(p).convert('RGB'), np.float32) if p.exists() else None
a, b = int(sys.argv[1]), int(sys.argv[2])
span = int(sys.argv[3]) if len(sys.argv) > 3 else 12
cache = {}
def g(slug, n):
    k = (slug, n)
    if k not in cache: cache[k] = lo(slug, n)
    return cache[k]
print('f7\tmejor_f6\tdesfase\tmad\tmad_2o\t(mad con texto)')
for n in range(a, b + 1):
    A = g('v7-ads90-rev', n)
    H = A.shape[0]
    y0, y1 = int(H * 0.44), int(H * 0.58)
    res = []
    for k in range(-2, span + 1):
        B = g('v6-ads90-rev', n + k)
        if B is None: continue
        d = np.abs(A - B)
        dm = np.concatenate([d[:y0].ravel(), d[y1:].ravel()]).mean()
        res.append((dm, k, d.mean()))
    res.sort()
    print(f'{n}\t{n+res[0][1]}\t{res[0][1]:+d}\t{res[0][0]:.2f}\t{res[1][0]:.2f}(k={res[1][1]:+d})\t{res[0][2]:.2f}')
