#!/usr/bin/env python3
"""¿Qué tipografía es? Compara un rótulo real con el mismo texto compuesto en fuentes candidatas.

  fontfit.py <slug> <fotograma> --roi x0,y0,x1,y1 --text "300€" [--mode bg|white] [-o lamina.jpg]

El rótulo debe estar sobre fondo plano (mode bg) o ser blanco sobre fondo oscuro (mode white).
Para cada fuente se ajusta el cuerpo a la altura de la tinta y el interletrado a su anchura,
y se mide el solape (IoU) con la tinta real. Devuelve cuerpo en px e interletrado en
milésimas de eme (la unidad de After Effects; en CSS: letter-spacing = tracking/1000 em).
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import probe  # noqa: E402
from sheet import load_full  # noqa: E402

SYS = "/System/Library/Fonts"
CANDIDATES = [
    ("SF Pro Display Bold", str(Path.home() / "Library/Fonts/SFPRODISPLAYBOLD.OTF"), 0, None),
    ("SF Pro (sistema) Semibold", f"{SYS}/SFNS.ttf", 0, b"Semibold"),
    ("SF Pro (sistema) Bold", f"{SYS}/SFNS.ttf", 0, b"Bold"),
    ("SF Pro (sistema) Heavy", f"{SYS}/SFNS.ttf", 0, b"Heavy"),
    ("Helvetica Neue Medium", f"{SYS}/HelveticaNeue.ttc", 10, None),
    ("Helvetica Neue Bold", f"{SYS}/HelveticaNeue.ttc", 1, None),
    ("Helvetica Neue Condensed Bold", f"{SYS}/HelveticaNeue.ttc", 4, None),
    ("Helvetica Bold", f"{SYS}/Helvetica.ttc", 1, None),
    ("Arial Bold", f"{SYS}/Supplemental/Arial Bold.ttf", 0, None),
    ("Arial Black", f"{SYS}/Supplemental/Arial Black.ttf", 0, None),
]
# pesos finos, para líneas secundarias: se activan con --thin
THIN = [
    ("SF Pro Display Regular", str(Path.home() / "Library/Fonts/SFPRODISPLAYREGULAR.OTF"), 0, None),
    ("SF Pro (sistema) Ultralight", f"{SYS}/SFNS.ttf", 0, b"Ultralight"),
    ("SF Pro (sistema) Thin", f"{SYS}/SFNS.ttf", 0, b"Thin"),
    ("SF Pro (sistema) Light", f"{SYS}/SFNS.ttf", 0, b"Light"),
    ("SF Pro (sistema) Regular", f"{SYS}/SFNS.ttf", 0, b"Regular"),
    ("Helvetica Neue UltraLight", f"{SYS}/HelveticaNeue.ttc", 5, None),
    ("Helvetica Neue Thin", f"{SYS}/HelveticaNeue.ttc", 12, None),
    ("Helvetica Neue Light", f"{SYS}/HelveticaNeue.ttc", 7, None),
    ("Helvetica Light", f"{SYS}/Helvetica.ttc", 4, None),
]


def get_font(path, index, var, size):
    f = ImageFont.truetype(path, size, index=index)
    if var:
        f.set_variation_by_name(var)
    return f


def render(text, font, tracking_px):
    """Texto con interletrado, respetando el kerning de la fuente. Devuelve máscara booleana ajustada a la tinta."""
    size = font.size
    w = int(sum(font.getlength(c) for c in text) + abs(tracking_px) * len(text) + 4 * size)
    im = Image.new("L", (max(8, w), int(size * 3)), 0)
    d = ImageDraw.Draw(im)
    x = size
    for i, c in enumerate(text):
        d.text((x, size), c, fill=255, font=font)
        adv = font.getlength(c)
        if i + 1 < len(text):
            pair = font.getlength(c + text[i + 1])
            adv = pair - font.getlength(text[i + 1])      # avance con kerning
        x += adv + tracking_px
    a = np.asarray(im) > 127
    ys, xs = np.nonzero(a)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def iou(a, b):
    h, w = max(a.shape[0], b.shape[0]), max(a.shape[1], b.shape[1])
    A = np.zeros((h, w), bool)
    B = np.zeros((h, w), bool)
    ya, xa = (h - a.shape[0]) // 2, (w - a.shape[1]) // 2
    yb, xb = (h - b.shape[0]) // 2, (w - b.shape[1]) // 2
    A[ya:ya + a.shape[0], xa:xa + a.shape[1]] = a
    B[yb:yb + b.shape[0], xb:xb + b.shape[1]] = b
    return (A & B).sum() / max(1, (A | B).sum()), A, B


def fit(text, target, path, index, var):
    th, tw = target.shape
    probe_font = get_font(path, index, var, 200)
    h200 = render(text, probe_font, 0).shape[0]
    best = (0, None)
    for k in (-0.04, -0.02, 0, 0.02, 0.04):
        size = max(8, int(round(200 * th / h200 * (1 + k))))
        font = get_font(path, index, var, size)
        # interletrado que iguala la anchura
        lo, hi = -0.25 * size, 0.15 * size
        for _ in range(18):
            mid = (lo + hi) / 2
            if render(text, font, mid).shape[1] < tw:
                lo = mid
            else:
                hi = mid
        tr = (lo + hi) / 2
        r = render(text, font, tr)
        score, A, B = iou(target, r)
        if score > best[0]:
            best = (score, {"size": size, "tracking_px": tr, "tracking_milesimas": round(1000 * tr / size), "A": A, "B": B,
                            "h": r.shape[0], "w": r.shape[1]})
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("frame", type=int)
    ap.add_argument("--roi", required=True, help="x0,y0,x1,y1 en px del original")
    ap.add_argument("--text", required=True)
    ap.add_argument("--mode", default="bg", choices=["bg", "white"])
    ap.add_argument("--thr", type=float, default=200, help="umbral de blanco en modo white")
    ap.add_argument("--thin", action="store_true", help="probar pesos finos en lugar de negritas")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    info = probe(a.slug)
    x0, y0, x1, y1 = [int(v) for v in a.roi.split(",")]
    im = np.asarray(load_full(a.slug, a.frame, info), np.float32)[y0:y1, x0:x1]
    if a.mode == "white":
        d = im.min(axis=2)
        mask = d >= a.thr
    else:
        border = np.concatenate([im[:4].reshape(-1, 3), im[-4:].reshape(-1, 3), im[:, :4].reshape(-1, 3), im[:, -4:].reshape(-1, 3)])
        ref = np.median(border, axis=0)
        d = np.sqrt(((im - ref) ** 2).sum(axis=2))
        mask = d >= 0.5 * np.percentile(d, 99.5)
    ys, xs = np.nonzero(mask)
    target = mask[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    print(f"# {a.slug} f{a.frame} «{a.text}»  tinta real: {target.shape[1]}x{target.shape[0]} px")
    res = []
    for name, path, index, var in (THIN if a.thin else CANDIDATES):
        try:
            score, r = fit(a.text, target, path, index, var)
        except Exception as e:  # fuente sin algún glifo, etc.
            print(f"{name:32s} error: {e}")
            continue
        res.append((score, name, r))
    res.sort(key=lambda t: -t[0])
    for score, name, r in res:
        print(f"{name:32s} IoU {score:.3f}  cuerpo {r['size']:4d}px  interletrado {r['tracking_milesimas']:+5d} milésimas ({r['tracking_px']:+.1f}px)")
    if a.out and res:
        tiles = []
        for score, name, r in res[:4]:
            A, B = r["A"], r["B"]
            rgb = np.zeros(A.shape + (3,), np.uint8)
            rgb[..., 0] = A * 255            # real en rojo
            rgb[..., 1] = B * 255            # candidata en verde (coincidencia = amarillo)
            t = Image.fromarray(rgb)
            lab = Image.new("RGB", (t.width, 22), (0, 0, 0))
            ImageDraw.Draw(lab).text((2, 3), f"{name}  IoU {score:.3f}  {r['size']}px  {r['tracking_milesimas']:+d}", fill=(255, 255, 255),
                                     font=ImageFont.truetype(f"{SYS}/Supplemental/Arial.ttf", 14))
            tile = Image.new("RGB", (t.width, t.height + 22))
            tile.paste(lab, (0, 0))
            tile.paste(t, (0, 22))
            tiles.append(tile)
        Wd = max(t.width for t in tiles)
        sheet = Image.new("RGB", (Wd, sum(t.height + 6 for t in tiles)), (30, 30, 30))
        y = 0
        for t in tiles:
            sheet.paste(t, (0, y))
            y += t.height + 6
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        sheet.save(a.out, quality=90)
        print("lámina:", a.out, "(rojo = real, verde = candidata, amarillo = coinciden)")


if __name__ == "__main__":
    main()
