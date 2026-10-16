import numpy as np
from PIL import Image, ImageDraw, ImageFont
from la import *
P = "/System/Library/Fonts/HelveticaNeue.ttc"
def render(text, size, index, tracking_em, pad=20):
    f = ImageFont.truetype(P, size, index=index)
    # avance por glifo con tracking
    x = pad; W = int(sum(f.getlength(c) for c in text) + pad * 2 + 50); H = int(size * 1.6)
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    for i, c in enumerate(text):
        d.text((x, 10), c, font=f, fill=255)
        adv = f.getlength(c)
        # kerning simple
        if i + 1 < len(text):
            adv = f.getlength(text[i:i + 2]) - f.getlength(text[i + 1])
        x += adv + tracking_em * size
    A = np.asarray(im)
    ys, xs = np.nonzero(A > 100)
    return A[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
def ink_runs(A):
    cols = (A > 100).sum(0) > 0
    return int(cols.sum())
for idx, nm in ((5, "UltraLight"), (12, "Thin"), (7, "Light"), (0, "Regular")):
    for size in (50, 52, 54):
        f = ImageFont.truetype(P, size, index=idx)
        # altura de mayúscula G y T
        a = render("T", size, idx, 0); g = render("G", size, idx, 0); xh = render("x", size, idx, 0)
        w0 = render("Gracias", size, idx, 0).shape[1]
        # tracking para ancho 129
        tr = (129 - w0) / 6 / size
        wp = render("por", size, idx, tr).shape[1]; wr = render("reservar.", size, idx, tr).shape[1]
        wt = render("Te", size, idx, tr).shape[1]; wd = render("dejamos", size, idx, tr).shape[1]; wm = render("mensaje", size, idx, tr).shape[1]
        print(f"{nm:10s} {size}px: alto T={a.shape[0]} G={g.shape[0]} x={xh.shape[0]} | 'Gracias' sin tracking {w0}px -> tracking {tr*1000:.0f}‰ ; con él: por={wp} (obj 59) reservar.={wr} (obj 140) Te={wt} (obj 50) dejamos={wd} (obj 151) mensaje={wm} (obj 147)")
