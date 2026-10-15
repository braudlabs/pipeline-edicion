#!/usr/bin/env python3
"""Montaje base de AD6 «PapiCat Snacks».

Lee la EDL de src/edl.json, recorta cada clip a los fotogramas medidos,
normaliza la geometria 1076x1928 -> 1080x1920 (9:16 exacto) y aplica los
movimientos de camara anadidos con remuestreo subpixel (PIL AFFINE).
No escribe fotogramas intermedios en disco: todo va por tuberias.
"""
import json, subprocess, sys, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-22-croche-gato/entrega"
EDL = json.load(open(os.path.join(ROOT, "src", "edl.json")))

SW, SH = 1076, 1928          # fuente
CW, CH = 1076, 1914          # recorte 9:16 exacto dentro de la fuente
CY = (SH - CH) // 2          # 7 px arriba y abajo
OW, OH = 1080, 1920          # salida
FPS = 24


def ease(kind, t):
    if kind == "lineal":
        return t
    if kind == "in":
        return t * t
    if kind == "out":
        return 1.0 - (1.0 - t) ** 2
    if kind == "inout":
        return 2 * t * t if t < 0.5 else 1.0 - ((-2 * t + 2) ** 2) / 2
    raise ValueError(kind)


def read_frames(clip, f0, n):
    """Devuelve un generador de fotogramas PIL del clip fuente."""
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", f"{SRC}/{clip}.mp4",
         "-vf", f"trim=start_frame={f0}:end_frame={f0+n}", "-fps_mode", "passthrough",
         "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE, bufsize=10 ** 8)
    size = SW * SH * 3
    got = 0
    while got < n:
        buf = p.stdout.read(size)
        if len(buf) < size:
            break
        yield Image.frombytes("RGB", (SW, SH), buf)
        got += 1
    p.stdout.close()
    p.wait()
    if got != n:
        sys.exit(f"ERROR: {clip} devolvio {got} fotogramas, esperaba {n}")


def main():
    total = sum(s["n"] for s in EDL["planos"])
    assert total == EDL["total_fotogramas"], (total, EDL["total_fotogramas"])
    out = os.path.join(ROOT, "output", "ad6-montaje-base-MUDO.mov")
    enc = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OW}x{OH}", "-r", str(FPS), "-i", "-",
         "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le",
         "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
         out], stdin=subprocess.PIPE, bufsize=10 ** 8)

    written = 0
    for s in EDL["planos"]:
        cam = s["camara"]
        z0, z1 = cam["zoom"]
        (cx0, cy0), (cx1, cy1) = cam["centro"]
        n = s["n"]
        for i, im in enumerate(read_frames(s["clip"], s["f0"], n)):
            t = i / (n - 1) if n > 1 else 0.0
            e = ease(cam["ease"], t)
            z = z0 + (z1 - z0) * e
            cx = cx0 + (cx1 - cx0) * e
            cy = cy0 + (cy1 - cy0) * e
            w, h = CW / z, CH / z
            x0 = cx * CW - w / 2
            y0 = cy * CH - h / 2
            x0 = min(max(x0, 0.0), CW - w)
            y0 = min(max(y0, 0.0), CH - h)
            coef = (w / OW, 0.0, x0, 0.0, h / OH, y0 + CY)
            o = im.transform((OW, OH), Image.AFFINE, coef, resample=Image.BICUBIC)
            enc.stdin.write(o.tobytes())
            written += 1
        print(f"  {s['id']:3s} {s['clip']:12s} src f{s['f0']:3d}..{s['f0']+n-1:3d}  "
              f"{n:3d} f  zoom {z0:.3f}->{z1:.3f}  -> tl f{s['tl0']}..{s['tl0']+n-1}", flush=True)
    enc.stdin.close()
    enc.wait()
    print(f"escritos {written} fotogramas -> {out}")


if __name__ == "__main__":
    main()
