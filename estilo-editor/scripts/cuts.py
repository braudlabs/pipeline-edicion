#!/usr/bin/env python3
"""Cadencia de metraje, fotogramas repetidos y cortes, sobre TODOS los fotogramas.

  cuts.py <slug> [...]

1. Repetidos: compara cada fotograma (360 px de ancho) con el anterior por bloques de
   12x12. Si ningún bloque cambia más que el ruido de compresión, el fotograma es una
   repetición exacta del anterior (metraje a menos fps que la línea de tiempo y ningún
   gráfico moviéndose). No aporta información nueva.
2. Cadencia: separación entre fotogramas en los que cambia el metraje (no solo un rótulo).
   De ahí sale a cuántos fps está el metraje dentro de la línea de tiempo.
3. Cortes: pico aislado de diferencia frente a su entorno temporal, con el entorno
   medido en el percentil 75 para que la cadencia 2-3-2-3 no se confunda con cortes.

Escribe datos/<slug>/repeats.json, cuts.json y bursts.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from common import DATOS, FRAMES, probe, t_of  # noqa: E402

BLOCK = 12
REPEAT_MAXBLOCK = 3.0     # ruido de compresión medido entre repeticiones: 1-2,7 sobre 255


def maxblock_series(slug, n):
    out = np.zeros(n, np.float32)
    frac = np.zeros(n, np.float32)      # fracción de bloques que cambian
    prev = None
    for i in range(n):
        g = np.asarray(Image.open(FRAMES / slug / f"f{i:06d}.jpg").convert("L"), np.float32)
        h, w = g.shape
        g = g[: h - h % BLOCK, : w - w % BLOCK]
        if prev is not None:
            d = np.abs(g - prev)
            b = d.reshape(d.shape[0] // BLOCK, BLOCK, d.shape[1] // BLOCK, BLOCK).mean(axis=(1, 3))
            out[i] = b.max()
            frac[i] = (b > 2.0).mean()
        prev = g
    return out, frac


def run(slug):
    info = probe(slug)
    fps = info["fps"]
    fs = json.loads((DATOS / slug / "framestats.json").read_text())
    mad = np.array(fs["mad"])
    hd = np.array(fs["hd"])
    n = len(mad)

    cache = DATOS / slug / "repeats.json"
    if cache.exists():
        c = json.loads(cache.read_text())
        mb = np.array(c["maxblock"], np.float32)
        frac = np.array(c["changed_block_frac"], np.float32)
    else:
        mb, frac = maxblock_series(slug, n)
    repeat = mb < REPEAT_MAXBLOCK
    repeat[0] = False

    # --- cadencia del metraje -------------------------------------------------
    big = np.zeros(n, bool)
    for i in range(1, n):
        lo, hi = max(1, i - 3), min(n, i + 4)
        big[i] = frac[i] >= 0.02 and frac[i] >= 0.5 * frac[lo:hi].max()
    idx = np.nonzero(big)[0]
    gaps = np.diff(idx)
    gaps = gaps[gaps <= 4]
    mean_gap = float(gaps.mean()) if len(gaps) else 1.0
    gap_hist = {str(int(v)): int(c) for v, c in zip(*np.unique(gaps, return_counts=True))} if len(gaps) else {}
    footage_fps = fps / mean_gap

    # --- cortes ---------------------------------------------------------------
    W = max(4, int(round(0.3 * fps)))      # entorno de ±0,3 s
    K = max(1, int(round(fps / 20)))       # vecinos directos: 1 a 24 fps, 3 a 60
    cuts = []
    for i in range(1, n):
        if mad[i] < 4.0:
            continue
        neigh = np.concatenate([mad[max(1, i - W):i], mad[i + 1:min(n, i + W + 1)]])
        if not len(neigh):
            continue
        base = float(np.percentile(neigh, 75))
        near = np.concatenate([mad[max(1, i - K):i], mad[i + 1:min(n, i + K + 1)]])
        peak = float(near.max()) if len(near) else 0.0
        ratio = mad[i] / (base + 0.35)
        iso = mad[i] / (peak + 0.35)
        if ratio >= 3.0 and iso >= 1.6:
            conf = "alta" if (ratio >= 5 and iso >= 2.5 and (hd[i] >= 0.12 or mad[i] >= 14)) else "media"
            cuts.append({"f": int(i), "t": round(t_of(i, info), 4), "mad": round(float(mad[i]), 2),
                         "hd": round(float(hd[i]), 3), "ratio": round(float(ratio), 1),
                         "iso": round(float(iso), 1), "conf": conf})

    # --- ráfagas de movimiento fuerte sostenido (transiciones, barridos, zooms) ---
    sm = np.array([mad[max(0, i - K):i + K + 1].max() for i in range(n)])   # tapa los huecos de cadencia
    strong = sm >= 9.0
    bursts, start = [], None
    for i in range(n + 1):
        on = i < n and strong[i]
        if on and start is None:
            start = i
        elif not on and start is not None:
            if (i - start) >= max(4, int(0.12 * fps)):
                bursts.append({"f0": int(start), "f1": int(i - 1), "t0": round(t_of(start, info), 3),
                               "t1": round(t_of(i - 1, info), 3),
                               "dur_s": round((i - start) / fps, 3),
                               "mad_max": round(float(mad[start:i].max()), 1)})
            start = None

    out = DATOS / slug
    (out / "repeats.json").write_text(json.dumps({
        "slug": slug, "frames": n, "fps": fps,
        "repeat_frames": [int(i) for i in np.nonzero(repeat)[0]],
        "repeat_pct": round(100 * float(repeat.mean()), 1),
        "footage_change_gap_hist": gap_hist,
        "footage_change_mean_gap": round(mean_gap, 3),
        "footage_fps_estimate": round(footage_fps, 2),
        "maxblock": [round(float(v), 1) for v in mb],
        "changed_block_frac": [round(float(v), 3) for v in frac],
    }))
    (out / "cuts.json").write_text(json.dumps(cuts, indent=0))
    (out / "bursts.json").write_text(json.dumps(bursts, indent=0))
    alta = sum(c["conf"] == "alta" for c in cuts)
    print(f"{slug:15s} {fps:6.2f} fps  repetidos {100 * repeat.mean():4.1f}%  cadencia {gap_hist} -> metraje ~{footage_fps:.1f} fps"
          f"  cortes {len(cuts)} (alta {alta})  ráfagas {len(bursts)}")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
