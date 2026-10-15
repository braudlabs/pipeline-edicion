#!/usr/bin/env python3
"""Hojas de contacto con fotograma y tiempo rotulados.

  sheet.py <slug> --range A:B[:paso]        fotogramas A..B (B incluido)
  sheet.py <slug> --frames 10,11,40         fotogramas sueltos
  sheet.py <slug> --times 0:10:0.5          segundos inicio:fin:paso
  opciones: --cols N  --w ANCHO_MINIATURA  --full  --crop x,y,w,h (0..1)  -o salida.jpg

Por defecto usa los fotogramas de baja resolución de analysis/frames/<slug>/.
Con --full los extrae del original a resolución nativa (para tipografía y detalle).
"""
import argparse
import io
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import FRAMES, probe, src, t_of, f_of  # noqa: E402


def load_low(slug, n):
    p = FRAMES / slug / f"f{n:06d}.jpg"
    return Image.open(p).convert("RGB") if p.exists() else None


def load_full(slug, n, info):
    # El índice es de decodificación, igual que frames/ y Vision. Un seek por tiempo
    # puede devolver n-1: seleccionar n explícitamente evita falsear las etiquetas.
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(src(slug)), "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
         "-fps_mode", "passthrough",
         "-f", "image2pipe", "-vcodec", "png", "-"],
        capture_output=True, check=True,
    ).stdout
    return Image.open(io.BytesIO(raw)).convert("RGB")


def load_full_run(slug, a, count, info):
    """count fotogramas consecutivos desde a, en una sola decodificación."""
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["ffmpeg", "-v", "error", "-i", str(src(slug)),
                        "-vf", f"select=between(n\\,{a}\\,{a + count - 1})", "-frames:v", str(count),
                        "-fps_mode", "passthrough", "-start_number", "0", f"{td}/%05d.png"], check=True)
        return [Image.open(p).convert("RGB").copy() for p in sorted(Path(td).glob("*.png"))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--range")
    ap.add_argument("--frames")
    ap.add_argument("--times")
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--w", type=int, default=0, help="ancho de miniatura; 0 = tamaño de origen")
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--crop", help="x,y,w,h normalizados")
    ap.add_argument("--nolabel", action="store_true")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    info = probe(a.slug)
    if a.range:
        p = [int(x) for x in a.range.split(":")]
        idx = list(range(p[0], p[1] + 1, p[2] if len(p) > 2 else 1))
    elif a.frames:
        idx = [int(x) for x in a.frames.split(",")]
    elif a.times:
        t0, t1, dt = [float(x) for x in a.times.split(":")]
        idx, t = [], t0
        while t <= t1 + 1e-9:
            idx.append(f_of(t, info))
            t += dt
    else:
        ap.error("falta --range, --frames o --times")
    idx = [i for i in idx if 0 <= i < info["frames"]]

    thumbs = []
    run = None
    if a.full and len(idx) > 1 and idx[-1] - idx[0] <= 400:
        imgs = load_full_run(a.slug, idx[0], idx[-1] - idx[0] + 1, info)
        run = {idx[0] + k: im for k, im in enumerate(imgs)}
    for n in idx:
        if run is not None:
            im = run.get(n)
        else:
            im = load_full(a.slug, n, info) if a.full else load_low(a.slug, n)
        if im is None:
            continue
        if a.crop:
            x, y, w, h = [float(v) for v in a.crop.split(",")]
            W, H = im.size
            im = im.crop((int(x * W), int(y * H), int((x + w) * W), int((y + h) * H)))
        if a.w:
            im = im.resize((a.w, max(1, round(im.height * a.w / im.width))), Image.LANCZOS)
        thumbs.append((n, im))
    if not thumbs:
        sys.exit("sin fotogramas")

    tw, th = thumbs[0][1].size
    lab = 0 if a.nolabel else max(14, tw // 14)
    font = ImageFont.load_default(size=max(11, lab - 3)) if lab else None
    cols = min(a.cols, len(thumbs))
    rows = (len(thumbs) + cols - 1) // cols
    gap = 4
    sheet = Image.new("RGB", (cols * (tw + gap) + gap, rows * (th + lab + gap) + gap), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    for k, (n, im) in enumerate(thumbs):
        x = gap + (k % cols) * (tw + gap)
        y = gap + (k // cols) * (th + lab + gap)
        if lab:
            d.text((x + 2, y), f"f{n} · {t_of(n, info):.3f}s", fill=(255, 220, 90), font=font)
        sheet.paste(im, (x, y + lab))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(a.out, quality=88)
    print(f"{a.out}  {sheet.size[0]}x{sheet.size[1]}  {len(thumbs)} fotogramas")


if __name__ == "__main__":
    main()
