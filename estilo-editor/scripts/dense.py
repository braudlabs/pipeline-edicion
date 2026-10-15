#!/usr/bin/env python3
"""Hojas densas: TODOS los fotogramas del vídeo, en orden, sin muestreo.

  dense.py <slug> [...]

Solo se omiten las repeticiones exactas del fotograma anterior (metraje a menos fps que
la línea de tiempo, sin ningún gráfico moviéndose): no contienen información nueva. El
fotograma conservado lleva «+k» en su rótulo para indicar cuántas repeticiones le siguen.

Marcas sobre la miniatura: barra roja = corte de confianza alta en ese fotograma;
barra naranja = corte de confianza media.

Salida: analysis/dense/<slug>/d<NNN>_f<primero>-f<último>.jpg e index.json.
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import ANALYSIS, DATOS, FRAMES, probe, t_of  # noqa: E402


def run(slug):
    info = probe(slug)
    vertical = info["height"] > info["width"]
    cols, rows, tw = (10, 4, 152) if vertical else (5, 6, 308)
    per = cols * rows
    rep = set(json.loads((DATOS / slug / "repeats.json").read_text())["repeat_frames"])
    cuts = {c["f"]: c["conf"] for c in json.loads((DATOS / slug / "cuts.json").read_text())}
    n = info["frames"]

    keep = [i for i in range(n) if i not in rep]
    follow = {}
    for a, b in zip(keep, keep[1:] + [n]):
        follow[a] = b - a - 1

    outdir = ANALYSIS / "dense" / slug
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("d*.jpg"):
        old.unlink()
    font = ImageFont.load_default(size=11)
    lab, gap = 14, 4
    index = []
    for s in range(0, len(keep), per):
        chunk = keep[s:s + per]
        first = Image.open(FRAMES / slug / f"f{chunk[0]:06d}.jpg")
        th = round(first.height * tw / first.width)
        r = (len(chunk) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (tw + gap) + gap, r * (th + lab + gap) + gap), (24, 24, 24))
        d = ImageDraw.Draw(sheet)
        for k, f in enumerate(chunk):
            im = Image.open(FRAMES / slug / f"f{f:06d}.jpg").convert("RGB").resize((tw, th), Image.LANCZOS)
            x = gap + (k % cols) * (tw + gap)
            y = gap + (k // cols) * (th + lab + gap)
            # un corte se marca en el fotograma conservado que lo contiene (él o sus repeticiones)
            mark = None
            for g in range(f, f + follow[f] + 1):
                if g in cuts:
                    mark = cuts[g]
            txt = f"f{f} {t_of(f, info):.2f}s" + (f" +{follow[f]}" if follow[f] else "")
            d.text((x + 1, y), txt, fill=(255, 90, 90) if mark == "alta" else (255, 170, 60) if mark else (255, 220, 90), font=font)
            sheet.paste(im, (x, y + lab))
            if mark:
                d.rectangle([x, y + lab, x + tw - 1, y + lab + 3], fill=(255, 40, 40) if mark == "alta" else (255, 160, 30))
        name = f"d{s // per:03d}_f{chunk[0]:05d}-f{chunk[-1] + follow[chunk[-1]]:05d}.jpg"
        sheet.save(outdir / name, quality=86)
        index.append({"sheet": name, "f0": chunk[0], "f1": chunk[-1] + follow[chunk[-1]],
                      "t0": round(t_of(chunk[0], info), 3), "t1": round(t_of(chunk[-1] + follow[chunk[-1]], info), 3),
                      "shown": len(chunk)})
    (outdir / "index.json").write_text(json.dumps(index, indent=0))
    print(f"{slug:15s} {n} fotogramas -> {len(keep)} distintos en {len(index)} hojas de {per} ({sheet.width}px de ancho)")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
