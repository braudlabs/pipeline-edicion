#!/usr/bin/env python3
"""Convierte la lectura por fotograma (visionscan) en pistas de texto y de cara.

  tracks.py <slug> [...]

Pista de texto = un mismo rótulo seguido fotograma a fotograma: cuándo entra y sale,
dónde está, cuánto mide y cómo cambian posición y tamaño en cada fotograma (de ahí
salen las curvas de entrada y salida).

Escribe:
  datos/<slug>/texts.json   pistas con geometría por fotograma
  datos/<slug>/texts.tsv    cronología legible: una línea por pista
  datos/<slug>/faces.json   caja y pupilas de la cara principal por fotograma
"""
import json
import math
import re
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ANALYSIS, DATOS, probe, t_of  # noqa: E402


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9€%$]", "", s)


def geom(q):
    tlx, tly, trx, try_, brx, bry, blx, bly = q
    cx = (tlx + trx + brx + blx) / 4
    cy = (tly + try_ + bry + bly) / 4
    h = (math.hypot(blx - tlx, bly - tly) + math.hypot(brx - trx, bry - try_)) / 2
    w = (math.hypot(trx - tlx, try_ - tly) + math.hypot(brx - blx, bry - bly)) / 2
    ang = math.degrees(math.atan2(try_ - tly, trx - tlx))
    return cx, cy, w, h, ang


def similar(a, b):
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    if len(a) >= 2 and len(b) >= 2 and (a.startswith(b) or b.startswith(a) or a.endswith(b) or b.endswith(a)):
        return 0.85                      # texto que se va revelando o que entra por un borde
    return SequenceMatcher(None, a, b).ratio()


def run(slug):
    info = probe(slug)
    W, H, fps = info["width"], info["height"], info["fps"]
    gap_ok = max(2, round(fps / 10))     # fotogramas que la lectura puede fallar sin romper la pista
    recs = [json.loads(l) for l in open(ANALYSIS / "vision" / f"{slug}.jsonl")]
    recs.sort(key=lambda r: r["f"])

    tracks, active = [], []
    faces = []
    for r in recs:
        f = r["f"]
        # --- caras: la mayor de cada fotograma
        if r["faces"]:
            fc = max(r["faces"], key=lambda x: x["b"][2] * x["b"][3])
            d = {"f": f, "b": fc["b"]}
            for k in ("le", "re", "roll", "yaw"):
                if k in fc:
                    d[k] = fc[k]
            d["n"] = len(r["faces"])
            faces.append(d)
        # --- textos
        active = [t for t in active if f - t["last"] <= gap_ok]
        used = set()
        for obs in r["texts"]:
            if obs["c"] < 0.3 and len(norm(obs["s"])) < 3:
                continue
            key = norm(obs["s"])
            if not key:
                continue
            cx, cy, w, h, ang = geom(obs["q"])
            best, score = None, 0.0
            for t in active:
                if id(t) in used:
                    continue
                s = similar(key, t["key"])
                dist = math.hypot(cx - t["cx"], cy - t["cy"])
                if s >= 0.6 and dist < max(0.45 * H, 3 * max(h, t["h"])):
                    sc = s - dist / (4 * H)
                    if sc > score:
                        best, score = t, sc
            if best is None:
                best = {"id": len(tracks), "frames": [], "key": key}
                tracks.append(best)
                active.append(best)
            used.add(id(best))
            best["frames"].append({"f": f, "s": obs["s"], "c": obs["c"], "cx": round(cx, 1), "cy": round(cy, 1),
                                   "w": round(w, 1), "h": round(h, 1), "ang": round(ang, 2),
                                   "nw": len(obs.get("words", []))})
            # la clave sigue al texto más largo visto con buena confianza (revelados)
            if obs["c"] >= 0.5 and len(key) >= len(best["key"]):
                best["key"] = key
            best.update(last=f, cx=cx, cy=cy, h=h)

    out_tracks = []
    for t in tracks:
        fr = t["frames"]
        if len(fr) < 2 and fr[0]["c"] < 0.5:
            continue                    # lectura suelta de baja confianza: ruido
        good = [x for x in fr if x["c"] >= 0.5] or fr
        text = Counter(x["s"] for x in good).most_common(1)[0][0]
        longest = max(good, key=lambda x: (len(norm(x["s"])), x["c"]))["s"]
        mid = sorted(fr, key=lambda x: x["f"])[len(fr) // 4: max(len(fr) // 4 + 1, 3 * len(fr) // 4)]
        med = lambda k: sorted(x[k] for x in mid)[len(mid) // 2]  # noqa: E731
        f0, f1 = fr[0]["f"], fr[-1]["f"]
        out_tracks.append({
            "id": t["id"], "text": text, "text_longest": longest,
            "f_in": f0, "f_out": f1, "t_in": round(t_of(f0, info), 4), "t_out": round(t_of(f1 + 1, info), 4),
            "frames_on": f1 - f0 + 1, "dur_s": round((f1 - f0 + 1) / fps, 4),
            "cx": med("cx"), "cy": med("cy"), "w": med("w"), "h": med("h"), "ang": med("ang"),
            "cx_pct": round(100 * med("cx") / W, 1), "cy_pct": round(100 * med("cy") / H, 1),
            "h_pct": round(100 * med("h") / H, 2), "w_pct": round(100 * med("w") / W, 1),
            "n_words": max(1, Counter(x["nw"] for x in good).most_common(1)[0][0]),
            "per_frame": [[x["f"], x["cx"], x["cy"], x["w"], x["h"], x["ang"], x["c"], x["s"]] for x in fr],
        })
    out_tracks.sort(key=lambda t: (t["f_in"], t["cy"]))

    out = DATOS / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "texts.json").write_text(json.dumps({
        "slug": slug, "width": W, "height": H, "fps": fps,
        "per_frame_columns": ["f", "cx", "cy", "w", "h", "ang", "conf", "string"],
        "tracks": out_tracks}, ensure_ascii=False))
    with open(out / "texts.tsv", "w") as fh:
        fh.write("id\tf_in\tf_out\tt_in\tdur_s\tframes\tcx%\tcy%\th%\tw%\th_px\tang\tpalabras\ttexto\n")
        for t in out_tracks:
            fh.write(f"{t['id']}\t{t['f_in']}\t{t['f_out']}\t{t['t_in']:.3f}\t{t['dur_s']:.3f}\t{t['frames_on']}\t"
                     f"{t['cx_pct']}\t{t['cy_pct']}\t{t['h_pct']}\t{t['w_pct']}\t{t['h']:.0f}\t{t['ang']:.1f}\t"
                     f"{t['n_words']}\t{t['text_longest']}\n")
    (out / "faces.json").write_text(json.dumps({"slug": slug, "width": W, "height": H, "fps": fps, "faces": faces}))
    nface = len(faces)
    print(f"{slug:15s} {len(recs)} fotogramas leídos  pistas de texto: {len(out_tracks)}  "
          f"fotogramas con cara: {nface} ({100 * nface / max(1, len(recs)):.0f}%)")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
