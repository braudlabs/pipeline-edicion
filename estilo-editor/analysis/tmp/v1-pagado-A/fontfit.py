#!/usr/bin/env python3
"""fontfit.py fotograma x0 y0 x1 y1 texto [thr]: compara la máscara de un rótulo con fuentes candidatas (tamaño e interletrado libres)."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tools import frames
f = int(sys.argv[1]); X0, Y0, X1, Y1 = [int(v) for v in sys.argv[2:6]]; text = sys.argv[6]
thr = int(sys.argv[7]) if len(sys.argv) > 7 else 250
obs = frames(f, f)[0][Y0:Y1, X0:X1].min(axis=2) >= thr
ys, xs = np.nonzero(obs); obs = obs[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
H, W = obs.shape
print(f"observado: {W}x{H} px")
ED = "/Users/alejandrorubiocamarero/Documents/ChatGPT/editor"
C = [("HelveticaNeue Bold", "/System/Library/Fonts/HelveticaNeue.ttc", 1), ("HelveticaNeue Medium", "/System/Library/Fonts/HelveticaNeue.ttc", 10),
     ("Helvetica Bold", "/System/Library/Fonts/Helvetica.ttc", 1), ("Arial Bold", "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 0),
     ("SF Pro Display Bold", "/Users/alejandrorubiocamarero/Library/Fonts/SFPRODISPLAYBOLD.OTF", 0),
     ("Avenir Next Bold", "/System/Library/Fonts/Avenir Next.ttc", 0), ("Avenir Next Demi", "/System/Library/Fonts/Avenir Next.ttc", 2),
     ("Display-Bold (proyecto)", ED + "/public/assets/Display-Bold.otf", 0)]

def render(font, text, track):
    adv = [font.getlength(ch) for ch in text]
    Wd = int(sum(adv) + track * len(text) + 80); Hd = int(font.size * 1.6)
    im = Image.new("L", (Wd, Hd), 0); d = ImageDraw.Draw(im)
    x = 40.0
    for ch, a in zip(text, adv):
        d.text((x, font.size * 0.2), ch, font=font, fill=255); x += a + track
    m = np.asarray(im) >= 128
    ys, xs = np.nonzero(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

def iou(a, b):
    h = max(a.shape[0], b.shape[0]); w = max(a.shape[1], b.shape[1])
    A = np.zeros((h, w), bool); B = np.zeros((h, w), bool)
    A[:a.shape[0], :a.shape[1]] = a; B[:b.shape[0], :b.shape[1]] = b
    return (A & B).sum() / max(1, (A | B).sum())

for name, path, idx in C:
    try:
        ImageFont.truetype(path, 50, index=idx)
    except Exception as e:
        print(name, "no disponible", e); continue
    best = (0, 0, 0, None)
    f0 = ImageFont.truetype(path, 200, index=idx)
    r0 = render(f0, text, 0)
    size0 = 200 * H / r0.shape[0]          # iguala la altura total de tinta
    for size in np.arange(size0 * 0.94, size0 * 1.06, size0 * 0.01):
        font = ImageFont.truetype(path, int(round(size)), index=idx)
        for tr in np.arange(-0.12, 0.031, 0.005):
            r = render(font, text, tr * size)
            if abs(r.shape[1] - W) > 0.03 * W: continue
            v = iou(obs, r)
            if v > best[0]: best = (v, int(round(size)), tr, r.shape)
    print(f"{name:26s} IoU={best[0]:.3f} tamaño={best[1]} px interletrado={best[2]*100:+.1f}% em  render={best[3]}  nombre={ImageFont.truetype(path, 20, index=idx).getname()}")
