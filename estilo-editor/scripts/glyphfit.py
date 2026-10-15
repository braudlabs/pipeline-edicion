#!/usr/bin/env python3
"""Identificación de tipografía glifo a glifo (independiente del interletrado).

  glyphfit.py <slug> <fotograma> --roi x0,y0,x1,y1 --text "300€" [--mode bg|white] [-o lamina.jpg]

Separa la tinta real en glifos (componentes conexas, de izquierda a derecha; las tildes y
puntos se unen a su letra) y compara cada uno con el mismo carácter en cada fuente
candidata, escalado a la misma altura. Informa del solape medio y de la relación de
anchuras (1,00 = misma proporción). El texto no debe llevar espacios.
"""
import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import probe  # noqa: E402
from fontfit import CANDIDATES, get_font  # noqa: E402
from sheet import load_full  # noqa: E402


def components(mask):
    h, w = mask.shape
    lab = np.zeros((h, w), np.int32)
    n = 0
    for y0, x0 in zip(*np.nonzero(mask)):
        if lab[y0, x0]:
            continue
        n += 1
        stack = [(y0, x0)]
        lab[y0, x0] = n
        while stack:
            y, x = stack.pop()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and mask[yy, xx] and not lab[yy, xx]:
                        lab[yy, xx] = n
                        stack.append((yy, xx))
    boxes = []
    for k in range(1, n + 1):
        ys, xs = np.nonzero(lab == k)
        if len(ys) >= 25:
            boxes.append([xs.min(), ys.min(), xs.max() + 1, ys.max() + 1])
    boxes.sort()
    # une a cada letra lo que queda encima o debajo de ella (puntos, tildes)
    merged = []
    for b in boxes:
        for m in merged:
            ov = min(b[2], m[2]) - max(b[0], m[0])
            if ov > 0.5 * min(b[2] - b[0], m[2] - m[0]):
                m[0], m[1], m[2], m[3] = min(m[0], b[0]), min(m[1], b[1]), max(m[2], b[2]), max(m[3], b[3])
                break
        else:
            merged.append(list(b))
    merged.sort()
    return merged


def glyph(ch, path, index, var, height):
    f = get_font(path, index, var, 300)
    im = Image.new("L", (900, 900), 0)
    ImageDraw.Draw(im).text((300, 300), ch, fill=255, font=f)
    a = np.asarray(im) > 127
    ys, xs = np.nonzero(a)
    a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    sc = height / a.shape[0]
    g = Image.fromarray((a * 255).astype(np.uint8)).resize((max(1, round(a.shape[1] * sc)), height), Image.LANCZOS)
    return np.asarray(g) > 127


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("frame", type=int)
    ap.add_argument("--roi", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--mode", default="bg", choices=["bg", "white"])
    ap.add_argument("--fitwidth", action="store_true", help="iguala también la anchura de cada glifo (solo forma; útil si hay perspectiva)")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    x0, y0, x1, y1 = [int(v) for v in a.roi.split(",")]
    im = np.asarray(load_full(a.slug, a.frame, probe(a.slug)), np.float32)[y0:y1, x0:x1]
    if a.mode == "white":
        mask = im.min(axis=2) >= 200
    else:
        border = np.concatenate([im[:4].reshape(-1, 3), im[-4:].reshape(-1, 3), im[:, :4].reshape(-1, 3), im[:, -4:].reshape(-1, 3)])
        d = np.sqrt(((im - np.median(border, axis=0)) ** 2).sum(axis=2))
        mask = d >= 0.5 * np.percentile(d, 99.5)
    boxes = components(mask)
    text = a.text.replace(" ", "")
    print(f"# {a.slug} f{a.frame} «{a.text}»: {len(boxes)} glifos separados para {len(text)} caracteres")
    if len(boxes) != len(text):
        print("  aviso: no coinciden (letras que se tocan); anchuras de los glifos:", [b[2] - b[0] for b in boxes])
        sys.exit(1)
    res = []
    for name, path, index, var in CANDIDATES:
        ious, wr, tiles = [], [], []
        for ch, b in zip(text, boxes):
            real = mask[b[1]:b[3], b[0]:b[2]]
            try:
                cand = glyph(ch, path, index, var, real.shape[0])
                natural_w = cand.shape[1]
                if a.fitwidth:
                    cand = np.asarray(Image.fromarray((cand * 255).astype(np.uint8)).resize((real.shape[1], real.shape[0]), Image.LANCZOS)) > 127
            except Exception:
                ious = None
                break
            w = max(real.shape[1], cand.shape[1])
            A = np.zeros((real.shape[0], w), bool)
            B = np.zeros((real.shape[0], w), bool)
            A[:, (w - real.shape[1]) // 2:(w - real.shape[1]) // 2 + real.shape[1]] = real
            B[:, (w - cand.shape[1]) // 2:(w - cand.shape[1]) // 2 + cand.shape[1]] = cand
            ious.append((A & B).sum() / (A | B).sum())
            wr.append(natural_w / real.shape[1])
            tiles.append((A, B))
        if ious:
            res.append((float(np.mean(ious)), name, ious, wr, tiles))
    res.sort(key=lambda t: -t[0])
    for score, name, ious, wr, _ in res:
        print(f"{name:32s} solape medio {score:.3f}  por glifo: " + " ".join(f"{v:.2f}" for v in ious) + "  | anchura cand/real: " + " ".join(f"{v:.2f}" for v in wr))
    if a.out and res:
        rows = []
        for score, name, ious, wr, tiles in res[:5]:
            hmax = max(t[0].shape[0] for t in tiles)
            wsum = sum(t[0].shape[1] + 10 for t in tiles)
            row = Image.new("RGB", (max(wsum, 520), hmax + 24), (20, 20, 20))
            ImageDraw.Draw(row).text((2, 3), f"{name}  solape {score:.3f}", fill=(255, 255, 255), font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14))
            x = 0
            for A, B in tiles:
                rgb = np.zeros(A.shape + (3,), np.uint8)
                rgb[..., 0] = A * 255
                rgb[..., 1] = B * 255
                row.paste(Image.fromarray(rgb), (x, 24))
                x += A.shape[1] + 10
            rows.append(row)
        Wd = max(r.width for r in rows)
        sheet = Image.new("RGB", (Wd, sum(r.height + 6 for r in rows)), (40, 40, 40))
        y = 0
        for r in rows:
            sheet.paste(r, (0, y))
            y += r.height + 6
        sc = min(1.0, 1500 / sheet.width)
        if sc < 1:
            sheet = sheet.resize((int(sheet.width * sc), int(sheet.height * sc)), Image.LANCZOS)
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        sheet.save(a.out, quality=90)
        print("lámina:", a.out)


if __name__ == "__main__":
    main()
