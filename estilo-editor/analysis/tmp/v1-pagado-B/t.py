"""Utilidades propias del revisor v1-pagado-B: carga de fotogramas nativos en caché y hojas."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

D = Path(__file__).parent
FR = D / "fr"

def load(n):
    return Image.open(FR / f"f{n:06d}.jpg").convert("RGB")

def arr(n):
    return np.asarray(load(n), np.float32)

def sheet(frames, out, crop=None, w=0, cols=8, label=True, scale=None):
    thumbs = []
    for n in frames:
        im = load(n)
        if crop:
            x, y, cw, ch = crop
            W, H = im.size
            im = im.crop((int(x * W), int(y * H), int((x + cw) * W), int((y + ch) * H)))
        if w:
            im = im.resize((w, max(1, round(im.height * w / im.width))), Image.LANCZOS)
        elif scale:
            im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.LANCZOS)
        thumbs.append((n, im))
    tw, th = thumbs[0][1].size
    lab = max(14, tw // 14) if label else 0
    lab = min(lab, 26)
    font = ImageFont.load_default(size=max(11, lab - 3)) if lab else None
    cols = min(cols, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    gap = 4
    sh = Image.new("RGB", (cols * (tw + gap) + gap, rows * (th + lab + gap) + gap), (24, 24, 24))
    d = ImageDraw.Draw(sh)
    for k, (n, im) in enumerate(thumbs):
        x = gap + (k % cols) * (tw + gap)
        y = gap + (k // cols) * (th + lab + gap)
        if lab:
            d.text((x + 2, y), f"f{n} {n/24:.3f}s", fill=(255, 220, 90), font=font)
        sh.paste(im, (x, y + lab))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sh.save(out, quality=90)
    print(out, sh.size, len(thumbs))

if __name__ == "__main__":
    # t.py sheet A:B out [crop x,y,w,h] [w=N] [cols=N] [step=N] [frames=a,b,c]
    args = sys.argv[1:]
    rng = args[0]
    out = args[1]
    kw = dict(a.split("=", 1) for a in args[2:])
    if "," in rng or ":" not in rng:
        frames = [int(v) for v in rng.split(",")]
    else:
        p = [int(v) for v in rng.split(":")]
        frames = list(range(p[0], p[1] + 1, p[2] if len(p) > 2 else 1))
    crop = tuple(float(v) for v in kw["crop"].split(",")) if "crop" in kw else None
    sheet(frames, out, crop=crop, w=int(kw.get("w", 0)), cols=int(kw.get("cols", 8)),
          scale=float(kw["scale"]) if "scale" in kw else None)
