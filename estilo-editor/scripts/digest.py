#!/usr/bin/env python3
"""Cronología fusionada de un tramo: cortes, ráfagas, rótulos, locución, golpes de audio y caras.

  digest.py <slug> <f0> <f1> [--anim]

Con --anim añade, para cada rótulo, su geometría fotograma a fotograma durante la
entrada y la salida (posición, tamaño y ángulo), que es de donde se leen las curvas.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DATOS, probe, t_of  # noqa: E402


def main():
    slug, f0, f1 = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    anim = "--anim" in sys.argv
    info = probe(slug)
    fps = info["fps"]
    d = DATOS / slug
    ld = lambda n: json.loads((d / n).read_text())  # noqa: E731
    cuts, bursts, texts, words, audio, faces, rep = (ld("cuts.json"), ld("bursts.json"), ld("texts.json"),
                                                     ld("words.json"), ld("audio.json"), ld("faces.json"), ld("repeats.json"))
    ev = []
    for c in cuts:
        if f0 <= c["f"] <= f1:
            ev.append((c["f"], 0, f"CORTE ({c['conf']})  mad={c['mad']} hd={c['hd']} ratio={c['ratio']}"))
    for b in bursts:
        if b["f1"] >= f0 and b["f0"] <= f1:
            ev.append((b["f0"], 1, f"RÁFAGA de movimiento f{b['f0']}-f{b['f1']} ({b['dur_s']} s) mad_max={b['mad_max']}"))
    for t in texts["tracks"]:
        if t["f_out"] >= f0 and t["f_in"] <= f1:
            ev.append((t["f_in"], 3, f"TEXTO «{t['text_longest']}»  f{t['f_in']}-f{t['f_out']} ({t['frames_on']} f, {t['dur_s']:.3f} s)  "
                                     f"centro {t['cx_pct']}%,{t['cy_pct']}%  alto {t['h']:.0f}px ({t['h_pct']}%)  ancho {t['w']:.0f}px  "
                                     f"ángulo {t['ang']:.1f}°  id={t['id']}"))
            if anim and t["frames_on"] >= 3:
                pf = t["per_frame"]
                head = pf[:10]
                tail = pf[-5:] if len(pf) > 14 else []
                for row in head:
                    ev.append((row[0], 4, f"    · id={t['id']} f{row[0]}: cx={row[1]:.0f} cy={row[2]:.0f} w={row[3]:.0f} h={row[4]:.0f} "
                                          f"ang={row[5]:.1f} conf={row[6]} «{row[7]}»"))
                for row in tail:
                    ev.append((row[0], 4, f"    · id={t['id']} f{row[0]}: cx={row[1]:.0f} cy={row[2]:.0f} w={row[3]:.0f} h={row[4]:.0f} "
                                          f"ang={row[5]:.1f} conf={row[6]} «{row[7]}» (final)"))
    for w in words["words"]:
        if f0 <= w["f0"] <= f1:
            gap = w.get("gap_before", 0)
            ev.append((w["f0"], 2, f"VOZ «{w['w']}»  {w['t0']:.2f}-{w['t1']:.2f} s (f{w['f0']}-f{w['f1']})"
                                   + (f"  [pausa previa {gap:.2f} s]" if gap >= 0.15 else "")))
    for o in audio["onsets"]:
        fo = int(round(o["t"] * fps))
        if f0 <= fo <= f1 and o["z"] >= 6:
            kind = "grave" if o["low"] >= 0.45 else "agudo" if o["high"] >= 0.55 else "medio/ancho"
            ev.append((fo, 5, f"GOLPE de audio t={o['t']:.3f} s  z={o['z']}  {kind}  subida {o['rise_db']} dB  nivel {o['level_db']} dB"))
    ev.sort(key=lambda e: (e[0], e[1]))

    print(f"# {slug}  f{f0}-f{f1}  ({t_of(f0, info):.3f}-{t_of(f1, info):.3f} s)  {fps:.3f} fps  {info['width']}x{info['height']}")
    print(f"# metraje estimado a ~{rep['footage_fps_estimate']} fps dentro de la línea de {fps:.2f}; "
          f"repetidos exactos en el tramo: {sum(f0 <= r <= f1 for r in rep['repeat_frames'])}")
    for f, _, txt in ev:
        print(f"f{f:<5d} {t_of(f, info):7.3f}s  {txt}")

    # caras: resumen por plano (entre cortes)
    bounds = [f0] + [c["f"] for c in cuts if f0 < c["f"] <= f1] + [f1 + 1]
    fa = {x["f"]: x for x in faces["faces"]}
    H, W = info["height"], info["width"]
    print("\n# CARA por plano (caja de Vision; alto en % del alto del fotograma, centro en %):")
    for a, b in zip(bounds, bounds[1:]):
        fr = [fa[i] for i in range(a, b) if i in fa]
        if len(fr) < 3:
            print(f"f{a}-f{b - 1}: sin cara ({len(fr)} detecciones)")
            continue
        g = lambda x: (100 * x["b"][3] / H, 100 * (x["b"][0] + x["b"][2] / 2) / W, 100 * (x["b"][1] + x["b"][3] / 2) / H)  # noqa: E731
        s, e = g(fr[0]), g(fr[-1])
        print(f"f{a}-f{b - 1} ({b - a} f): alto {s[0]:.1f}%→{e[0]:.1f}%  centro x {s[1]:.1f}%→{e[1]:.1f}%  y {s[2]:.1f}%→{e[2]:.1f}%  "
              f"({len(fr)} detecciones)")


if __name__ == "__main__":
    main()
