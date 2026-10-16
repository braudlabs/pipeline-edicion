import numpy as np
from la import *
F = frames(9, 60)
items = []
for f, yc in ((9, 585), (10, 580), (11, 575), (12, 572), (14, 566), (18, 558), (26, 548), (60, 538)):
    A = F[f][yc - 28: yc + 28, 176:324].astype(np.float32)
    # realce: normalizar al máximo para ver forma (ganancia)
    g = 255.0 / max(1, A.max())
    items.append((f"f{f} x{g:.1f}", np.clip(A * g, 0, 255)))
sheet(items, 4, OUT / "z_gracias.jpg", scale=2.6, resample=Image.NEAREST)
