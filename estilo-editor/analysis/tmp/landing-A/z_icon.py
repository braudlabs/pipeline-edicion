import sys
import numpy as np
from la import *
a, b, step = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
out = sys.argv[4]
x0, y0, x1, y1 = [int(v) for v in sys.argv[5].split(",")] if len(sys.argv) > 5 else (150, 425, 320, 520)
scale = float(sys.argv[6]) if len(sys.argv) > 6 else 2.2
cols = int(sys.argv[7]) if len(sys.argv) > 7 else 4
gain = float(sys.argv[8]) if len(sys.argv) > 8 else 1.0
F = frames(a, b)
items = [(f"f{f} {f/60:.3f}s", np.clip(F[f][y0:y1, x0:x1].astype(np.float32) * gain, 0, 255)) for f in range(a, b + 1, step)]
sheet(items, cols, OUT / out, scale=scale, resample=Image.LANCZOS)
