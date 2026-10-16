#!/usr/bin/env python3
"""Utilidades propias del revisor v1-pagado-A (solo numpy + PIL)."""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import probe, src  # noqa: E402

SLUG = "v1-pagado"
INFO = probe(SLUG)
W, H = INFO["width"], INFO["height"]
FPS = INFO["fps_num"] / INFO["fps_den"]


def frames(a, b):
    """Fotogramas a..b (incluidos) como lista de arrays uint8 HxWx3."""
    n = b - a + 1
    t = max(0.0, (a - 0.5) / FPS)
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", str(src(SLUG)), "-frames:v", str(n),
         "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return [arr[i] for i in range(arr.shape[0])]


def drop_border(mask):
    """Quita los componentes del mask que tocan el borde de la región (relleno iterativo)."""
    reach = np.zeros_like(mask)
    reach[0, :] = mask[0, :]
    reach[-1, :] = mask[-1, :]
    reach[:, 0] = mask[:, 0]
    reach[:, -1] = mask[:, -1]
    while True:
        g = reach.copy()
        g[1:, :] |= reach[:-1, :]
        g[:-1, :] |= reach[1:, :]
        g[:, 1:] |= reach[:, :-1]
        g[:, :-1] |= reach[:, 1:]
        g &= mask
        if (g == reach).all():
            break
        reach = g
    return mask & ~reach


def bbox(mask, pct=0.0):
    if mask.sum() < 20:
        return None
    ys, xs = np.nonzero(mask)
    if pct:
        x0, x1 = np.percentile(xs, [pct, 100 - pct])
        y0, y1 = np.percentile(ys, [pct, 100 - pct])
    else:
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    return float(x0), float(y0), float(x1), float(y1)


def roi_px(roi):
    x, y, w, h = roi
    return int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)


def white_mask(im, thr=235):
    return im.min(axis=2) >= thr


def save(arr, path):
    Image.fromarray(arr).save(path, quality=92)
