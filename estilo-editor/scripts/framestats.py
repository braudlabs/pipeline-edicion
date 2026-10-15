#!/usr/bin/env python3
"""Métricas por fotograma y detección de cortes.

  framestats.py <slug> [...]

Decodifica el original a baja resolución y calcula, para cada fotograma respecto al
anterior: diferencia media absoluta (mad), distancia de histograma (hd), luma media y
desviación, saturación media y color medio. De ahí salen:

  datos/<slug>/framestats.json   series por fotograma (compactas)
  datos/<slug>/cuts.json         cortes candidatos con su puntuación
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import DATOS, probe, src, t_of  # noqa: E402


def decode(slug, info):
    vertical = info["height"] > info["width"]
    w, h = (90, 160) if vertical else (160, 90)
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(src(slug)), "-vf", f"scale={w}:{h}:flags=area",
         "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(h, w, 3).astype(np.float32)
    p.wait()


def run(slug):
    info = probe(slug)
    mad, hd, luma, lstd, sat, rgb = [], [], [], [], [], []
    prev_g = prev_h = None
    for fr in decode(slug, info):
        g = fr @ np.array([0.299, 0.587, 0.114], np.float32)
        hist = np.histogram(g, bins=64, range=(0, 255))[0].astype(np.float32)
        hist /= hist.sum()
        if prev_g is None:
            mad.append(0.0)
            hd.append(0.0)
        else:
            mad.append(float(np.abs(g - prev_g).mean()))
            hd.append(float(np.abs(hist - prev_h).sum() / 2))
        mx, mn = fr.max(axis=2), fr.min(axis=2)
        sat.append(float(((mx - mn) / np.maximum(mx, 1)).mean()))
        luma.append(float(g.mean()))
        lstd.append(float(g.std()))
        rgb.append([float(v) for v in fr.reshape(-1, 3).mean(axis=0)])
        prev_g, prev_h = g, hist
    mad = np.array(mad)
    hd = np.array(hd)
    n = len(mad)

    # Corte duro = pico aislado: mucho mayor que su entorno inmediato.
    cuts = []
    W = 6
    for i in range(1, n):
        lo, hi = max(1, i - W), min(n, i + W + 1)
        neigh = np.concatenate([mad[lo:i], mad[i + 1:hi]])
        base = float(np.median(neigh)) if len(neigh) else 0.0
        peak = float(max(mad[i - 1] if i > 1 else 0, mad[i + 1] if i + 1 < n else 0))
        ratio = mad[i] / (base + 0.35)
        iso = mad[i] / (peak + 0.35)          # frente a los dos vecinos directos
        if mad[i] >= 4.0 and ratio >= 3.0 and iso >= 1.6:
            conf = "alta" if (ratio >= 6 and iso >= 2.5 and (hd[i] >= 0.12 or mad[i] >= 14)) else "media"
            cuts.append({"f": i, "t": round(t_of(i, info), 4), "mad": round(float(mad[i]), 2),
                         "hd": round(float(hd[i]), 3), "ratio": round(float(ratio), 1),
                         "iso": round(float(iso), 1), "conf": conf})

    dup = [int(i) for i in range(1, n) if mad[i] < 0.06]
    out = DATOS / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "framestats.json").write_text(json.dumps({
        "slug": slug, "fps": info["fps"], "frames": n,
        "mad": [round(float(v), 2) for v in mad],
        "hd": [round(float(v), 3) for v in hd],
        "luma": [round(v, 1) for v in luma],
        "luma_std": [round(v, 1) for v in lstd],
        "sat": [round(v, 3) for v in sat],
        "rgb": [[round(c, 1) for c in v] for v in rgb],
        "dup_frames": dup,
    }))
    (out / "cuts.json").write_text(json.dumps(cuts, indent=0))
    alta = sum(c["conf"] == "alta" for c in cuts)
    print(f"{slug:16s} {n:5d} f  cortes candidatos: {len(cuts):3d} (alta {alta}, media {len(cuts) - alta})"
          f"  repetidos: {len(dup)} ({100 * len(dup) / n:.0f}%)  mad mediana {np.median(mad):.2f}")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
