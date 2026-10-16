"""Utilidades locales del revisor v3-ia-cara-B: fotogramas nativos desde la caché PNG."""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
FR = Path('/private/tmp/claude-501/-Users-alejandrorubiocamarero-Documents-ChatGPT-editor/1f516058-b06c-4444-a7f3-77af77afb931/scratchpad/v3B/fr')
FPS = 24.0
def im(n):
    return Image.open(FR / f"{n:05d}.png").convert("RGB")
def arr(n):
    return np.asarray(im(n), np.float32)
def font(sz=22):
    for p in ["/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/SFNS.ttf"]:
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()
def sheet(frames, out, crop=None, w=None, cols=6, scale=None, label=True, resample=Image.LANCZOS):
    """crop = (x0,y0,x1,y1) en px del original. w = ancho de cada celda (px)."""
    tiles = []
    for n in frames:
        I = im(n)
        if crop:
            I = I.crop(crop)
        if w:
            I = I.resize((w, round(I.height * w / I.width)), resample)
        elif scale:
            I = I.resize((round(I.width*scale), round(I.height*scale)), resample)
        tiles.append((n, I))
    tw, th = tiles[0][1].size
    lab = 26 if label else 0
    rows = (len(tiles) + cols - 1) // cols
    S = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + lab + 4) + 4), (20, 20, 20))
    d = ImageDraw.Draw(S)
    f = font(20)
    for i, (n, I) in enumerate(tiles):
        x = 4 + (i % cols) * (tw + 4)
        y = 4 + (i // cols) * (th + lab + 4)
        if label:
            d.text((x + 2, y + 1), f"f{n} · {n/FPS:.3f}s", fill=(255, 220, 90), font=f)
        S.paste(I, (x, y + lab))
    S.save(out, quality=90)
    print(out, S.size, len(tiles), "fotogramas")

def bbox(mask, x0=0, y0=0, pct=0.3, minpx=25):
    if mask.sum() < minpx:
        return None
    ys, xs = np.nonzero(mask)
    bx0, bx1 = np.percentile(xs, [pct, 100 - pct])
    by0, by1 = np.percentile(ys, [pct, 100 - pct])
    return (x0 + bx0, y0 + by0, x0 + bx1, y0 + by1)

def dark_box(n, roi, thr=90, pct=0.3):
    """Caja de la tinta oscura (máx. canal < thr) dentro de roi=(x0,y0,x1,y1) px."""
    x0, y0, x1, y1 = roi
    A = arr(n)[y0:y1, x0:x1]
    m = A.max(2) < thr
    b = bbox(m, x0, y0, pct)
    dens = float((255 - A.max(2))[m].mean()) / 255 if m.any() else 0
    return b, int(m.sum()), dens

def white_box(n, roi, thr=225, pct=0.3):
    x0, y0, x1, y1 = roi
    A = arr(n)[y0:y1, x0:x1]
    m = A.min(2) >= thr
    b = bbox(m, x0, y0, pct)
    return b, int(m.sum())

def fmt(b):
    if b is None:
        return "-"
    return "x %4.0f-%4.0f  y %4.0f-%4.0f  c=(%6.1f,%6.1f) w=%4.0f h=%4.0f" % (b[0], b[2], b[1], b[3], (b[0]+b[2])/2, (b[1]+b[3])/2, b[2]-b[0], b[3]-b[1])

def stab_sheet(frames, centers, size, out, cols=3, w=None, label=True):
    """Hoja estabilizada: recorta una ventana size=(W,H) centrada en centers[n] (px del original), con relleno."""
    tiles = []
    W, H = size
    for n in frames:
        cx, cy = centers[n]
        I = im(n)
        C = Image.new("RGB", (W, H), (60, 0, 60))
        x0 = int(round(cx - W / 2)); y0 = int(round(cy - H / 2))
        C.paste(I.crop((max(0, x0), max(0, y0), min(1080, x0 + W), min(1920, y0 + H))), (max(0, -x0), max(0, -y0)))
        if w:
            C = C.resize((w, round(H * w / W)), Image.LANCZOS)
        tiles.append((n, C))
    tw, th = tiles[0][1].size
    lab = 26 if label else 0
    rows = (len(tiles) + cols - 1) // cols
    S = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + lab + 4) + 4), (20, 20, 20))
    d = ImageDraw.Draw(S)
    f = font(20)
    for i, (n, I) in enumerate(tiles):
        x = 4 + (i % cols) * (tw + 4)
        y = 4 + (i // cols) * (th + lab + 4)
        if label:
            d.text((x + 2, y + 1), f"f{n} · {n/FPS:.3f}s", fill=(255, 220, 90), font=f)
        S.paste(I, (x, y + lab))
    S.save(out, quality=90)
    print(out, S.size, len(tiles), "fotogramas")
