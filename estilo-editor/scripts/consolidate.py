#!/usr/bin/env python3
"""Junta las notas de revisión por tramo en una ficha por vídeo y en una tabla única de sucesos.

  consolidate.py

Lee analysis/notas/<slug>-<letra>.md, escribe fichas/<slug>.md (cabecera con las medidas del
vídeo + las notas de sus tramos en orden) y datos/eventos.json (todos los sucesos anotados).
"""
import json
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ANALYSIS, DATOS, ROOT, VIDEOS, probe  # noqa: E402

NOTAS = ROOT / "notas"             # copia persistente; analysis/ es ignorado por Git
LIVE_NOTAS = ANALYSIS / "notas"
FICHAS = ROOT / "fichas"


def events_of(text):
    blocks = re.findall(r"```json\s*(\[.*?\])\s*```", text, flags=re.S)
    if not blocks:
        return None, text
    raw = blocks[-1]
    try:
        ev = json.loads(raw)
    except json.JSONDecodeError:
        return None, text
    # la ficha no repite el bloque JSON: va a datos/eventos.json
    match = list(re.finditer(r"```json\s*(\[.*?\])\s*```", text, flags=re.S))[-1]
    body = (text[:match.start()] + text[match.end():]).rstrip() + "\n"
    return ev, body


def main():
    FICHAS.mkdir(exist_ok=True)
    all_events = []
    missing_json = []
    for slug in VIDEOS:
        candidates = {}
        for directory in (NOTAS, LIVE_NOTAS):
            for p in directory.glob(f"{slug}-[A-Z].md"):
                if p.name not in candidates or p.stat().st_mtime > candidates[p.name].stat().st_mtime:
                    candidates[p.name] = p
        parts = sorted(candidates.values(), key=lambda p: p.name)
        if not parts:
            continue
        info = probe(slug)
        head = [f"# {VIDEOS[slug]}", "",
                f"`{slug}` · {info['width']}×{info['height']} · {info['fps']:.3f} fps · {info['frames']} fotogramas · {info['duration']:.2f} s", "",
                "Ficha de trabajo consolidada. La presencia de una nota no certifica revisión completa: consultar `ESTADO.md` y la cobertura del tramo. El guion siguiente es inferencia automática OCR/voz.", ""]
        gu = DATOS / slug / "guion-anotado.md"
        if gu.exists():
            head += ["## Guion con cortes y énfasis", "", *gu.read_text().splitlines()[2:], ""]
        body = []
        for p in parts:
            txt = p.read_text()
            ev, clean = events_of(txt)
            if ev is None:
                missing_json.append(p.name)
            else:
                for e in ev:
                    if not isinstance(e, dict) or not isinstance(e.get("f0"), int) or not isinstance(e.get("f1"), int):
                        raise ValueError(f"{p}: suceso sin f0/f1 enteros")
                    if not 0 <= e["f0"] <= e["f1"] < info["frames"]:
                        raise ValueError(f"{p}: rango inválido {e['f0']}..{e['f1']}")
                    e["slug"] = slug
                    e["tramo"] = p.stem
                    e["source_note"] = f"notas/{p.name}"
                    e["source_sha256"] = hashlib.sha256(txt.encode()).hexdigest()
                    e.setdefault("evidence_level", "reported_observation; consult note for native verification")
                all_events += ev
            # baja un nivel los títulos para que cuelguen de la ficha
            clean = re.sub(r"^(#+) ", lambda m: "#" + m.group(1) + " ", clean, flags=re.M)
            body += [f"---", "", clean]
        (FICHAS / f"{slug}.md").write_text("\n".join(head + body))
        print(f"{slug:15s} {len(parts)} tramos -> fichas/{slug}.md ({sum(len(b) for b in body)} caracteres)")
    (DATOS / "eventos.json").write_text(json.dumps(all_events, ensure_ascii=False, indent=0))
    c = Counter((e.get("tipo", "?"), e.get("nombre", "?")) for e in all_events)
    print(f"\n{len(all_events)} sucesos en datos/eventos.json")
    for (tipo, nombre), n in sorted(c.items(), key=lambda kv: (kv[0][0], -kv[1])):
        print(f"  {tipo:22s} {nombre:40s} {n}")
    if missing_json:
        print("\nsin bloque JSON válido:", ", ".join(missing_json))


if __name__ == "__main__":
    main()
