"""Utilidades del revisor v6-ads90-rev-B (solo lectura del original; escribe en analysis/tmp/v6-ads90-rev-B)."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import probe, t_of  # noqa: E402
from sheet import load_full_run  # noqa: E402

TMP = Path(__file__).resolve().parent
SLUG = "v6-ads90-rev"
_info = {}


def info(slug=SLUG):
    if slug not in _info:
        _info[slug] = probe(slug)
    return _info[slug]


def run(a, b, slug=SLUG):
    """Fotogramas a..b (incluido) como lista de PIL RGB."""
    return load_full_run(slug, a, b - a + 1, info(slug))


def arr(im):
    return np.asarray(im, np.float32)


def luma(A):
    return 0.2126 * A[..., 0] + 0.7152 * A[..., 1] + 0.0722 * A[..., 2]


def label_sheet(items, cols, out, gap=4, scale=1.0, font_px=None):
    """items: lista de (texto, PIL). Monta una hoja rotulada."""
    ims = []
    for txt, im in items:
        if scale != 1.0:
            im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        ims.append((txt, im))
    tw = max(im.width for _, im in ims)
    th = max(im.height for _, im in ims)
    lab = font_px or max(14, tw // 14)
    font = ImageFont.load_default(size=max(11, lab - 3))
    cols = min(cols, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + gap) + gap, rows * (th + lab + gap) + gap), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for k, (txt, im) in enumerate(ims):
        x = gap + (k % cols) * (tw + gap)
        y = gap + (k // cols) * (th + lab + gap)
        d.text((x + 2, y), txt, fill=(255, 220, 90), font=font)
        sheet.paste(im, (x, y + lab))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=90)
    print(f"{out}  {sheet.size[0]}x{sheet.size[1]}  {len(ims)} celdas")
    return sheet


def crop_px(im, box):
    return im.crop(box)
