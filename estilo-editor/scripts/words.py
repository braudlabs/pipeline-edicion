#!/usr/bin/env python3
"""Pasa la transcripción de Whisper a una lista de palabras con tiempos y pausas.

  words.py <slug> [...]

Escribe datos/<slug>/words.json: palabras (inicio, fin, fotograma), pausas entre
palabras y ritmo de locución.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ANALYSIS, DATOS, f_of, probe  # noqa: E402


def run(slug):
    info = probe(slug)
    j = json.loads((ANALYSIS / "whisper" / f"{slug}.16k.json").read_text())
    words = []
    for seg in j["segments"]:
        for w in seg.get("words", []):
            words.append({"w": w["word"].strip(), "t0": round(w["start"], 3), "t1": round(w["end"], 3),
                          "f0": f_of(w["start"], info), "f1": f_of(w["end"], info),
                          "p": round(w.get("probability", 0), 2), "seg": seg["id"]})
    gaps = []
    for a, b in zip(words, words[1:]):
        g = round(b["t0"] - a["t1"], 3)
        b["gap_before"] = g
        gaps.append(g)
    if words:
        words[0]["gap_before"] = round(words[0]["t0"], 3)
    speech = sum(w["t1"] - w["t0"] for w in words)
    span = (words[-1]["t1"] - words[0]["t0"]) if words else 0
    out = DATOS / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "words.json").write_text(json.dumps({
        "slug": slug, "language": j.get("language"), "text": j["text"].strip(),
        "n_words": len(words), "first_word_t": words[0]["t0"] if words else None,
        "last_word_t": words[-1]["t1"] if words else None,
        "words_per_s_span": round(len(words) / span, 3) if span else None,
        "speech_ratio": round(speech / span, 3) if span else None,
        "pauses_over_150ms": [{"after": a["w"], "before": b["w"], "t": a["t1"], "gap": b["gap_before"]}
                               for a, b in zip(words, words[1:]) if b["gap_before"] >= 0.15],
        "words": words}, ensure_ascii=False, indent=0))
    big = sorted(gaps, reverse=True)[:5]
    print(f"{slug:15s} {len(words):3d} palabras  {len(words) / span if span else 0:.2f} pal/s  "
          f"pausas ≥150 ms: {sum(g >= 0.15 for g in gaps)}  mayores: {big}")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        run(s)
