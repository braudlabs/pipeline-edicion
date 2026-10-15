#!/usr/bin/env python3
"""Empareja cada palabra de la locución con el rótulo que la muestra.

  align.py <slug> [...]

Para cada palabra dicha: ¿aparece escrita?, ¿en qué fotograma por primera vez?, ¿con
cuánto desfase respecto a la voz?, ¿a qué tamaño y dónde?, ¿cuánto dura en pantalla?,
¿y dónde queda respecto a la cara?

Escribe datos/<slug>/align.json y resume por pantalla.
"""
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import DATOS, probe  # noqa: E402


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9€%$ ]", "", s)


NUM = {"cero": "0", "uno": "1", "un": "1", "una": "1", "dos": "2", "tres": "3", "cuatro": "4", "cinco": "5", "seis": "6",
       "siete": "7", "ocho": "8", "nueve": "9", "diez": "10", "veinte": "20", "treinta": "30", "cuarenta": "40",
       "cincuenta": "50", "cien": "100", "mil": "1000"}


def contains(nw, s):
    """¿El texto leído s (normalizado, con espacios) contiene la palabra nw?"""
    toks = s.split()
    if nw in toks:
        return True
    if len(nw) >= 4:
        for t in toks:
            if abs(len(t) - len(nw)) <= 2 and SequenceMatcher(None, nw, t).ratio() >= 0.78:
                return True
    joined = s.replace(" ", "")
    if len(nw) >= 3 and nw in joined:
        return True
    if len(nw) <= 2 and len(joined) <= 12 and (joined.startswith(nw) or joined.endswith(nw)):
        return True
    return False


def run(slug):
    info = probe(slug)
    fps, W, H = info["fps"], info["width"], info["height"]
    words = json.loads((DATOS / slug / "words.json").read_text())["words"]
    T = json.loads((DATOS / slug / "texts.json").read_text())["tracks"]
    faces = {x["f"]: x for x in json.loads((DATOS / slug / "faces.json").read_text())["faces"]}
    L = int(round(0.6 * fps))

    # por pista: fotograma -> texto normalizado
    per = []
    for t in T:
        per.append([(r[0], norm(r[7])) for r in t["per_frame"]])

    out = []
    for w in words:
        nw = norm(w["w"]).replace(" ", "")
        if not nw:
            continue
        alts = {nw}
        if nw in NUM:
            alts.add(NUM[nw])
        best = None
        for ti, t in enumerate(T):
            if t["f_out"] < w["f0"] - L or t["f_in"] > w["f1"] + L:
                continue
            first = None
            for f, s in per[ti]:
                if f < w["f0"] - L:
                    continue
                if f > w["f1"] + L:
                    break
                if any(contains(a, s) for a in alts):
                    first = f
                    break
            if first is None:
                continue
            d = abs(first - w["f0"])
            if best is None or d < best[0]:
                best = (d, first, ti)
        rec = {"w": w["w"], "t0": w["t0"], "t1": w["t1"], "f0": w["f0"], "f1": w["f1"], "gap_before": w.get("gap_before", 0)}
        if best:
            _, first, ti = best
            t = T[ti]
            rec.update(shown=True, track=t["id"], f_first=first, lag_f=first - w["f0"], lag_s=round((first - w["f0"]) / fps, 4),
                       f_out=t["f_out"], on_frames=t["f_out"] - first + 1, on_s=round((t["f_out"] - first + 1) / fps, 4),
                       h=t["h"], h_pct=t["h_pct"], tw=t["w"], tw_pct=t["w_pct"], cx_pct=t["cx_pct"], cy_pct=t["cy_pct"],
                       ang=t["ang"], track_text=t["text_longest"], track_words=t["n_words"])
            fc = faces.get(first) or faces.get(first + 1) or faces.get(first - 1)
            if fc:
                fx, fy, fw, fh = fc["b"]
                rec.update(face_h_pct=round(100 * fh / H, 1), face_cy_pct=round(100 * (fy + fh / 2) / H, 1),
                           face_cx_pct=round(100 * (fx + fw / 2) / W, 1),
                           # centro del rótulo respecto a la cara, en alturas de cara (0 = centro de la cara, +0,5 = barbilla)
                           rel_y=round((t["cy"] - (fy + fh / 2)) / fh, 2), rel_x=round((t["cx"] - (fx + fw / 2)) / fw, 2))
        else:
            rec.update(shown=False)
        out.append(rec)

    shown = [r for r in out if r["shown"]]
    lag = np.array([r["lag_f"] for r in shown])
    (DATOS / slug / "align.json").write_text(json.dumps({"slug": slug, "fps": fps, "words": out}, ensure_ascii=False))
    core = lag[np.abs(lag) <= L // 2] if len(lag) else lag
    print(f"{slug:15s} palabras {len(out):3d}  en pantalla {len(shown):3d} ({100 * len(shown) / max(1, len(out)):.0f}%)  "
          f"desfase fotogramas mediana {np.median(core):+.1f}  p10 {np.percentile(core, 10):+.0f}  p90 {np.percentile(core, 90):+.0f}  "
          f"= {1000 * np.median(core) / fps:+.0f} ms")
    miss = [r["w"] for r in out if not r["shown"]]
    print("      no encontradas:", " · ".join(miss[:40]))


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
