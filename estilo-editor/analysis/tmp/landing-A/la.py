"""Utilidades locales de landing-A (solo lectura del vídeo; escribe en analysis/tmp/landing-A)."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import probe, t_of  # noqa
from sheet import load_full_run, load_full  # noqa
SLUG = "landing"
INFO = probe(SLUG)
OUT = Path(__file__).resolve().parent

def frames(a, b):
    """dict f -> np.uint8 HxWx3 (a..b incluidos)"""
    if a == b:
        return {a: np.asarray(load_full(SLUG, a, INFO))}
    imgs = load_full_run(SLUG, a, b - a + 1, INFO)
    return {a + k: np.asarray(im) for k, im in enumerate(imgs)}

def luma(A):
    A = A.astype(np.float32)
    return 0.2126 * A[..., 0] + 0.7152 * A[..., 1] + 0.0722 * A[..., 2]

def sheet(items, cols, out, scale=1.0, resample=Image.LANCZOS, labelsize=18, gap=4):
    """items: lista (etiqueta, np.array) -> hoja"""
    ims = []
    for lab, A in items:
        im = Image.fromarray(A.astype(np.uint8))
        if scale != 1.0:
            im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), resample)
        ims.append((lab, im))
    tw, th = ims[0][1].size
    font = ImageFont.load_default(size=labelsize)
    lab_h = labelsize + 6
    cols = min(cols, len(ims))
    rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * (tw + gap) + gap, rows * (th + lab_h + gap) + gap), (24, 24, 24))
    d = ImageDraw.Draw(S)
    for k, (lab, im) in enumerate(ims):
        x = gap + (k % cols) * (tw + gap)
        y = gap + (k // cols) * (th + lab_h + gap)
        d.text((x + 2, y + 1), lab, fill=(255, 220, 90), font=font)
        S.paste(im, (x, y + lab_h))
    S.save(out, quality=90)
    print(out, S.size)
