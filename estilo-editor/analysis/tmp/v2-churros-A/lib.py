"""Utilidades locales de v2-churros-A: fotogramas nativos cacheados y medidas."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
FULL = HERE / "full"
W, H = 1080, 1920
FPS = 24.0


def fr(n):
    return np.asarray(Image.open(FULL / f"f{n:05d}.jpg").convert("RGB"), np.float32)


def img(n):
    return Image.open(FULL / f"f{n:05d}.jpg").convert("RGB")


def white_box(A, roi=None, thr=225, sat=None):
    """Caja de la tinta blanca (min canal >= thr) en roi px (x0,y0,x1,y1)."""
    x0, y0, x1, y1 = roi or (0, 0, W, H)
    S = A[y0:y1, x0:x1]
    m = S.min(axis=2) >= thr
    if sat is not None:
        m &= (S.max(axis=2) - S.min(axis=2)) <= sat
    if m.sum() < 30:
        return None
    ys, xs = np.nonzero(m)
    bx0, bx1 = np.percentile(xs, [0.2, 99.8])
    by0, by1 = np.percentile(ys, [0.2, 99.8])
    return dict(x0=x0 + bx0, y0=y0 + by0, x1=x0 + bx1, y1=y0 + by1, cx=x0 + (bx0 + bx1) / 2,
                cy=y0 + (by0 + by1) / 2, w=bx1 - bx0, h=by1 - by0, area=int(m.sum()))


def sheet(frames, crop=None, w=0, cols=6, out="x.jpg", label=True, fn=None):
    """Hoja con fotogramas nativos; crop=(x,y,w,h) normalizado; fn: función img->img opcional."""
    thumbs = []
    for n in frames:
        im = img(n)
        if fn:
            im = fn(im, n)
        if crop:
            cx, cy, cw, ch = crop
            im = im.crop((int(cx * W), int(cy * H), int((cx + cw) * W), int((cy + ch) * H)))
        if w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        thumbs.append((n, im))
    tw, th = thumbs[0][1].size
    pad, lab = 4, 22 if label else 0
    rows = (len(thumbs) + cols - 1) // cols
    sh = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + lab + pad) + pad), (24, 24, 24))
    d = ImageDraw.Draw(sh)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except Exception:
        font = ImageFont.load_default()
    for i, (n, im) in enumerate(thumbs):
        x = pad + (i % cols) * (tw + pad)
        y = pad + (i // cols) * (th + lab + pad)
        if label:
            d.text((x + 2, y + 2), f"f{n} · {n / FPS:.3f}s", fill=(255, 220, 90), font=font)
        sh.paste(im, (x, y + lab))
    sh.save(out, quality=92)
    print(out, sh.size, len(thumbs), "fotogramas")
