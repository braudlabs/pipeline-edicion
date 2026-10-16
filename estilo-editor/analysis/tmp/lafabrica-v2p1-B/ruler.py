#!/usr/bin/env python3
"""Recorte nativo con regla en píxeles del original: ruler.py F x0 y0 x1 y1 [--zoom 1.0] [--step 50] -o out.jpg
Varios fotogramas: F puede ser lista separada por comas (se apilan en columnas --cols)."""
import argparse
from PIL import Image, ImageDraw, ImageFont
import fr
ap = argparse.ArgumentParser()
ap.add_argument("f"); ap.add_argument("x0", type=int); ap.add_argument("y0", type=int); ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
ap.add_argument("--zoom", type=float, default=1.0)
ap.add_argument("--step", type=int, default=50)
ap.add_argument("--cols", type=int, default=2)
ap.add_argument("--nogrid", action="store_true")
ap.add_argument("-o", required=True)
a = ap.parse_args()
fs = [int(v) for v in a.f.split(",")]
F = fr.frames(min(fs), max(fs))
font = ImageFont.load_default(size=13)
tiles = []
for f in fs:
    im = Image.fromarray(F[f][a.y0:a.y1, a.x0:a.x1])
    if a.zoom != 1.0:
        im = im.resize((round(im.width * a.zoom), round(im.height * a.zoom)), Image.LANCZOS if a.zoom < 1 else Image.BICUBIC)
    M = 44
    can = Image.new("RGB", (im.width + M, im.height + 18 + 16), (24, 24, 24))
    can.paste(im, (M, 18))
    d = ImageDraw.Draw(can)
    d.text((2, 1), f"f{f} {fr.t(f):.3f}s", fill=(255, 220, 90), font=font)
    x = (a.x0 // a.step + 1) * a.step
    while x < a.x1:
        px = M + (x - a.x0) * a.zoom
        if not a.nogrid:
            d.line([(px, 18), (px, 18 + im.height)], fill=(0, 255, 255), width=1)
        d.text((px - 12, 18 + im.height + 1), str(x), fill=(0, 255, 255), font=font)
        x += a.step
    y = (a.y0 // a.step + 1) * a.step
    while y < a.y1:
        py = 18 + (y - a.y0) * a.zoom
        if not a.nogrid:
            d.line([(M, py), (M + im.width, py)], fill=(0, 255, 255), width=1)
        d.text((2, py - 7), str(y), fill=(0, 255, 255), font=font)
        y += a.step
    tiles.append(can)
cols = min(a.cols, len(tiles)); rows = (len(tiles) + cols - 1) // cols
tw, th = tiles[0].size
sheet = Image.new("RGB", (cols * (tw + 4) + 4, rows * (th + 4) + 4), (24, 24, 24))
for k, tl in enumerate(tiles):
    sheet.paste(tl, (4 + (k % cols) * (tw + 4), 4 + (k // cols) * (th + 4)))
sheet.save(a.o, quality=90)
print(a.o, sheet.size)
