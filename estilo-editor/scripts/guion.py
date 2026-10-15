#!/usr/bin/env python3
"""Guion anotado: la locución con los cortes y las palabras de énfasis marcados.

  guion.py <slug> [...]

Escribe datos/<slug>/guion-anotado.md. Es la forma más rápida de ver qué palabras destaca
el editor y dónde corta respecto a la frase.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import DATOS  # noqa: E402


def run(slug):
    A = json.loads((DATOS / slug / "align.json").read_text())
    fps = A["fps"]
    vf = DATOS / slug / "cuts-verificados.json"
    cuts = [c["f"] for c in json.loads((vf if vf.exists() else DATOS / slug / "cuts.json").read_text())]
    ws = A["words"]
    one = [w for w in ws if w["shown"] and w["track_words"] == 1 and abs(w["lag_f"]) <= fps / 4]
    base = float(np.median([w["h"] for w in one]))
    out, line, ci = [], [], 0
    for w in ws:
        while ci < len(cuts) and cuts[ci] <= w["f0"] + 1:
            line.append("‖")
            ci += 1
        tok = w["w"]
        if w["shown"] and abs(w.get("lag_f", 99)) <= fps / 2:
            r = w["h"] / base
            tok = f"⟦{tok}⟧" if r >= 2.4 else f"[{tok}]" if r >= 1.55 else tok
        else:
            tok = f"({tok})"
        if w.get("gap_before", 0) >= 0.3:
            line.append(f"…{w['gap_before']:.1f}s…")
        line.append(tok)
        if tok.rstrip(")]⟧")[-1:] in ".?!":
            out.append(f"{w['t1']:5.1f}s  " + " ".join(line))
            line = []
    if line:
        out.append("        " + " ".join(line))
    (DATOS / slug / "guion-anotado.md").write_text(
        f"# {slug} — guion anotado\n\n"
        "‖ = corte · [palabra] = énfasis (1,55–2,4× el subtítulo base) · ⟦palabra⟧ = palabra gigante (≥2,4×) · "
        "(palabra) = no localizada en pantalla por el lector de texto · …Ns… = pausa de voz. "
        "El tiempo de cada línea es el final de la frase.\n\n```\n" + "\n".join(out) + "\n```\n")
    print(f"{slug}: {len(out)} frases")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
