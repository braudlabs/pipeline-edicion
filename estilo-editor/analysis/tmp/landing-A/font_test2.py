import numpy as np
from PIL import Image, ImageDraw, ImageFont
from la import *
P = "/System/Library/Fonts/HelveticaNeue.ttc"
def render(text, size, index, tracking_em, kern=False, pad=20, sup=4):
    f = ImageFont.truetype(P, size * sup, index=index)
    W = int(sum(f.getlength(c) for c in text) + pad * 2 * sup + 50); H = int(size * sup * 1.6)
    im = Image.new("L", (W, H), 0); d = ImageDraw.Draw(im)
    x = pad * sup
    for i, c in enumerate(text):
        d.text((x, 10 * sup), c, font=f, fill=255)
        adv = f.getlength(c)
        if kern and i + 1 < len(text):
            adv = f.getlength(text[i:i + 2]) - f.getlength(text[i + 1])
        x += adv + tracking_em * size * sup
    im = im.resize((W // sup, H // sup), Image.LANCZOS)
    return np.asarray(im)
def bbox(A, thr=100):
    ys, xs = np.nonzero(A > thr)
    return xs.min(), xs.max(), ys.min(), ys.max()
targets = {"Gracias": 129, "por": 59, "reservar.": 140, "Te": 50, "dejamos": 151, "un": 44, "mensaje": 147, "de": 48, "los": 46, "fundadores.": 205, "Ponte": 101, "auriculares": 179, "disfruta": 120, "la": 24, "experiencia.": 198}
for idx, nm in ((5, "UltraLight"), (12, "Thin"), (7, "Light")):
    size = 52
    best = None
    for tr in np.arange(-0.16, -0.02, 0.005):
        err = 0
        for w, t in targets.items():
            x0, x1, _, _ = bbox(render(w, size, idx, tr))
            err += (x1 - x0 + 1 - t) ** 2
        if best is None or err < best[1]: best = (tr, err)
    tr = best[0]
    ws = {w: (lambda b: b[1] - b[0] + 1)(bbox(render(w, size, idx, tr))) for w in targets}
    # grosor de asta: perfil horizontal de la 'l'
    A = render("l", size, idx, 0)
    x0, x1, y0, y1 = bbox(A, 30)
    prof = A[(y0 + y1) // 2, x0 - 1:x1 + 2]
    print(f"{nm}: mejor tracking {tr*1000:.0f}‰ (sin kerning) rms={np.sqrt(best[1]/len(targets)):.1f}px  anchos: " + " ".join(f"{w}={ws[w]}/{targets[w]}" for w in targets))
    print("   perfil del asta 'l' a 52px:", list(prof), " suma/255 = %.2f px" % (prof.sum() / 255))
