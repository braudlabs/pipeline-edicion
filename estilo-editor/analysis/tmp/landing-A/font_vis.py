import numpy as np
from PIL import Image
from la import *
from font_test2 import render, bbox
F = frames(200, 200)[200]
vid = F[485:600, 140:570].astype(np.float32)
def line(text, idx, tr):
    A = render(text, 52, idx, tr)
    x0, x1, y0, y1 = bbox(A, 60)
    return A[y0 - 4:y1 + 5, x0 - 4:x1 + 5]
rows = [("vídeo f200 (Te dejamos un mensaje / de los fundadores.)", vid)]
for idx, nm, tr in ((5, "UltraLight -70", -0.070), (12, "Thin -95", -0.095), (7, "Light -115", -0.115)):
    a = line("Te dejamos un mensaje", idx, tr); b = line("de los fundadores.", idx, tr)
    H = a.shape[0] + b.shape[0] + 12; W = max(a.shape[1], b.shape[1], 430)
    C = np.zeros((H, W), np.float32); C[:a.shape[0], :a.shape[1]] = a; C[a.shape[0] + 12:a.shape[0] + 12 + b.shape[0], :b.shape[1]] = b
    rows.append((f"Helvetica Neue {nm}‰ 52px (PIL, sin kerning)", np.repeat(C[..., None], 3, 2)))
# igualar tamaños
W = max(r[1].shape[1] for r in rows); H = max(r[1].shape[0] for r in rows)
items = []
for lab, A in rows:
    C = np.zeros((H, W, 3), np.float32); C[:A.shape[0], :A.shape[1]] = A
    items.append((lab, C))
sheet(items, 2, OUT / "font_vis.jpg", scale=1.75, resample=Image.LANCZOS)
