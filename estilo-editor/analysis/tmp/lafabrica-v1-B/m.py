"""Utilidades de medida del revisor lafabrica-v1-B (sobre la caché de fotogramas nativos)."""
import numpy as np
from PIL import Image
from pathlib import Path
D = Path(__file__).parent / 'full'
_c = {}
def load(n):
    if n not in _c:
        if len(_c) > 80:
            _c.clear()
        _c[n] = np.asarray(Image.open(D / f'f{n:05d}.jpg').convert('RGB'), np.float32)
    return _c[n]
def gray(n):
    a = load(n)
    return a @ np.array([0.299, 0.587, 0.114], np.float32)
def bbox(mask):
    if mask.sum() == 0:
        return None
    ys, xs = np.nonzero(mask)
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
