#!/usr/bin/env python3
"""Estadísticas cruzadas de todos los vídeos: la base medida del algoritmo.

  stats.py

Lee datos/<slug>/* y escribe:
  datos/estadisticas.json   todas las cifras
  datos/estadisticas.md     las mismas cifras en tablas legibles

Se puede volver a ejecutar en cualquier momento (por ejemplo, tras añadir un vídeo o
corregir una lista de cortes). No decodifica vídeo: tarda segundos.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import ImageFont

sys.path.insert(0, str(Path(__file__).parent))
from common import DATOS, VIDEOS  # noqa: E402

# v6 comparte casi todo el montaje: no ponderar el original como referencia independiente.
# v7 reutiliza gran parte de la cola; no equivale a identidad de fotogramas decodificados.
SLUGS = [s for s in VIDEOS if s != "v6-ads90" and (DATOS / s / "align.json").exists()]

SF_BOLD = Path.home() / "Library/Fonts/SFPRODISPLAYBOLD.OTF"
TRACKING = -60          # milésimas de eme, medido con fontfit.py
EMPH = 1.55             # una palabra es de énfasis si su caja mide ≥ 1,55× la del subtítulo base
GIANT = 2.4             # y gigante si ≥ 2,4×

_font = ImageFont.truetype(str(SF_BOLD), 1000) if SF_BOLD.exists() else None


def unit_width(word):
    """Anchura de la palabra a cuerpo 1 px en SF Pro Display Bold con el interletrado medido."""
    if _font is None or not word:
        return None
    return (_font.getlength(word) + TRACKING * (len(word) - 1)) / 1000


def pct(a, qs):
    a = np.asarray(a, float)
    return [round(float(v), 3) for v in np.percentile(a, qs)] if len(a) else [None] * len(qs)


def load(slug, name):
    return json.loads((DATOS / slug / name).read_text())


def video_stats(slug):
    info = load(slug, "probe.json")
    fps, W, H = info["fps"], info["width"], info["height"]
    words = load(slug, "words.json")
    al = load(slug, "align.json")["words"]
    tracks = load(slug, "texts.json")["tracks"]
    byid = {t["id"]: t for t in tracks}
    cuts = load(slug, "cuts.json")
    cuts_src = "detector"
    vf = DATOS / slug / "cuts-verificados.json"      # lista corregida a mano tras la revisión visual, si existe
    if vf.exists():
        cuts, cuts_src = json.loads(vf.read_text()), "verificados"
    audio = load(slug, "audio.json")
    rep = load(slug, "repeats.json")
    fs = load(slug, "framestats.json")

    shown = [w for w in al if w["shown"]]
    tight = [w for w in shown if abs(w["lag_f"]) <= fps / 4]
    one = [w for w in tight if w["track_words"] == 1]
    base_h = float(np.median([w["h"] for w in one]))
    base_w = [w for w in one if w["h"] < 1.35 * base_h]

    # --- cuerpo tipográfico estimado por anchura
    sizes = []
    for w in base_w:
        word = w["w"].strip(".,;:¿?¡!\"")
        u = unit_width(word)
        if u and len(word) >= 3 and abs(byid[w["track"]]["ang"]) <= 3:
            sizes.append(byid[w["track"]]["w"] / u)
    base_size = float(np.median(sizes)) if sizes else None

    # --- énfasis
    emph, seen = [], set()
    for w in shown:
        if w["h"] >= EMPH * base_h and abs(w["lag_f"]) <= fps / 2 and w["track"] not in seen:
            seen.add(w["track"])
            t = byid[w["track"]]
            word = w["w"].strip(".,;:¿?¡!\"")
            u = unit_width(word) if t["n_words"] == 1 else None
            comp = None
            for o in tracks:
                if o["id"] == t["id"] or o["frames_on"] < 3:
                    continue
                ov = min(t["f_out"], o["f_out"]) - max(t["f_in"], o["f_in"]) + 1
                if (ov >= 0.5 * t["frames_on"] and 0.5 * base_h <= o["h"] < 0.62 * t["h"]
                        and abs(o["cy"] - t["cy"]) < 2.2 * t["h"] and abs(o["cx"] - t["cx"]) < 0.4 * W):
                    if comp is None or abs(o["cy"] - t["cy"]) < abs(comp["cy"] - t["cy"]):
                        comp = o
            emph.append({
                "palabra": word, "t": w["t0"], "f_in": t["f_in"], "f_out": t["f_out"],
                "en_pantalla_s": round(t["frames_on"] / fps, 3),
                "alto_px": t["h"], "veces_base": round(t["h"] / base_h, 2),
                "ancho_pct": t["w_pct"], "cx_pct": t["cx_pct"], "cy_pct": t["cy_pct"],
                "cuerpo_px": round(t["w"] / u) if u and len(word) >= 3 else None,
                "gigante": t["h"] >= GIANT * base_h,
                "linea": None if comp is None else {
                    "texto": comp["text_longest"], "alto_px": comp["h"],
                    "posicion": "encima" if comp["cy"] < t["cy"] else "debajo",
                    "separacion_centros_px": round(abs(comp["cy"] - t["cy"])),
                    "entra_antes_s": round((t["f_in"] - comp["f_in"]) / fps, 3),
                    "sale_con_ella": abs(comp["f_out"] - t["f_out"]) <= max(1, fps / 12)},
            })
    span = words["words"][-1]["t1"] - words["words"][0]["t0"]
    wide = [e["ancho_pct"] for e in emph if e["ancho_pct"] >= 50]
    with_line = [e for e in emph if e["linea"]]

    # --- cortes
    last_f = int(words["words"][-1]["t1"] * fps) + int(fps)
    cf = [c["f"] for c in cuts if c["f"] < last_f]
    shots = np.diff([0] + cf + [min(info["frames"], last_f)]) / fps
    on = np.array([w["f0"] for w in words["words"]])
    delta, after_punct = [], 0
    for f in cf:
        delta.append(int(f - on[int(np.argmin(np.abs(on - f)))]))
        prev = [w for w in words["words"] if w["f1"] <= f + 1]
        if prev and prev[-1]["w"][-1:] in ".,?!;:":
            after_punct += 1
    tol = max(1, round(fps / 24))

    # --- final
    luma = fs["luma"]
    black = 0
    while black < len(luma) and luma[-1 - black] < 3:
        black += 1
    rel = [w["rel_y"] for w in base_w if "rel_y" in w]

    first_text = min((t for t in tracks if t["frames_on"] >= 3 and t["h_pct"] >= 2.5), key=lambda t: t["f_in"])
    return {
        "slug": slug, "original": info["original"], "ancho": W, "alto": H, "fps": round(fps, 3),
        "fotogramas": info["frames"], "duracion_s": round(info["duration"], 3),
        "metraje_fps_estimado": rep["footage_fps_estimate"], "repetidos_pct": rep["repeat_pct"],
        "audio": {**audio["loudness"], "primer_sonido_s": audio["first_sound_t"], "ultimo_sonido_s": audio["last_sound_t"]},
        "voz": {"palabras": words["n_words"], "palabras_por_s": words["words_per_s_span"],
                "pausas_ge_300ms": sum(1 for w in words["words"] if w.get("gap_before", 0) >= 0.3),
                "primera_palabra_s": words["first_word_t"], "ultima_palabra_s": words["last_word_t"]},
        "subtitulo_base": {
            "palabras_alineadas_n": len(al), "palabras_localizadas_n": len(shown),
            "muestra_desfase_cercano_n": len(tight),
            "desfase_todos_f_p10_p50_p90": pct([w["lag_f"] for w in shown], [10, 50, 90]),
            "desfases_excluidos_del_resumen_base_n": len(shown) - len(tight),
            "palabras_localizadas_pct": round(100 * len(shown) / len(al), 1),
            "desfase_fotogramas_p10_p50_p90": pct([w["lag_f"] for w in tight], [10, 50, 90]),
            "desfase_ms_p50": round(1000 * float(np.median([w["lag_f"] for w in tight])) / fps),
            "caja_alto_px_p50": round(base_h, 1),
            "cuerpo_px_estimado_por_anchura": round(base_size) if base_size else None,
            "cuerpo_pct_ancho": round(100 * base_size / W, 2) if base_size else None,
            "en_pantalla_s_p10_p50_p90": pct([w["on_frames"] / fps for w in base_w], [10, 50, 90]),
            "palabra_dicha_s_p50": round(float(np.median([w["t1"] - w["t0"] for w in base_w])), 3),
            "centro_x_pct_p10_p50_p90": pct([w["cx_pct"] for w in base_w], [10, 50, 90]),
            "centro_y_pct_p10_p50_p90": pct([w["cy_pct"] for w in base_w], [10, 50, 90]),
            "respecto_cara_y_p10_p50_p90": pct(rel, [10, 50, 90]), "respecto_cara_n": len(rel),
        },
        "enfasis": {
            "n": len(emph), "cada_s": round(span / len(emph), 2) if emph else None,
            "gigantes": sum(e["gigante"] for e in emph),
            "ancho_pct_p25_p50_p75_de_las_anchas": pct(wide, [25, 50, 75]),
            "en_pantalla_s_p10_p50_p90": pct([e["en_pantalla_s"] for e in emph], [10, 50, 90]),
            "con_linea_pequena": len(with_line),
            "linea_encima": sum(e["linea"]["posicion"] == "encima" for e in with_line),
            "linea_sale_a_la_vez": sum(e["linea"]["sale_con_ella"] for e in with_line),
            "linea_separacion_centros_px_p50": pct([e["linea"]["separacion_centros_px"] for e in with_line], [50])[0],
            "linea_entra_antes_s_p50": pct([e["linea"]["entra_antes_s"] for e in with_line], [50])[0],
            "palabras": emph,
        },
        "cortes": {
            "tolerancia_f_real": tol, "tolerancia_s_real": round(tol / fps, 5),
            "fuente": cuts_src, "n": len(cf), "plano_medio_s": round(float(shots.mean()), 3),
            "plano_s_p10_p50_p90_max": pct(shots, [10, 50, 90, 100]),
            "primer_corte_s": round(cf[0] / fps, 3) if cf else None,
            "corte_menos_inicio_palabra_f_p10_p50_p90": pct(delta, [10, 50, 90]),
            "pct_a_1f_de_un_inicio": round(100 * float(np.mean(np.abs(delta) <= tol)), 1) if delta else None,
            "pct_tras_puntuacion": round(100 * after_punct / len(cf), 1) if cf else None,
        },
        "arranque": {"primer_rotulo_f": first_text["f_in"], "primer_rotulo_s": first_text["t_in"],
                     "primer_rotulo": first_text["text_longest"],
                     "primer_enfasis_s": emph[0]["t"] if emph else None,
                     "primer_enfasis": emph[0]["palabra"] if emph else None},
        "final": {"cola_tras_ultima_palabra_s": round(info["duration"] - words["last_word_t"], 3),
                  "negro_final_fotogramas": black, "negro_final_s": round(black / fps, 3)},
    }


def md(S):
    L = ["# Estadísticas automáticas y sus límites", "",
         "Generado por `scripts/stats.py` a partir de `datos/<slug>/`. No editar a mano: volver a ejecutar el script.",
         "`v6-ads90` se excluye para no ponderar dos veces el montaje compartido: 2424/2650 fotogramas decodificados coinciden por hash con rev; 226 difieren. V7 reutiliza visualmente gran parte de la cola con desplazamiento de 5f en anclas verificadas, sin identidad general por hash.", ""]
    L += ["Estas cifras describen candidatos OCR/detector; no son reglas creativas ni verificación visual. "
          "La fracción localizada no permite distinguir omisión editorial, oclusión y fallo OCR. "
          "El resumen de desfase base condiciona a |lag| ≤0,25 s; ver todos los desfases y n excluidos en JSON. "
          "La cadencia es una estimación de cambios en la imagen final, no los fps originales del rodaje. "
          "Los énfasis se detectan por altura relativa y pueden mezclar textos de interfaz, grafismos y OCR parcial.", ""]

    def table(title, head, rows):
        L.extend([f"## {title}", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)])
        L.extend("| " + " | ".join(str(c) for c in r) + " |" for r in rows)
        L.append("")

    f3 = lambda v: "–".join("—" if x is None else f"{x:g}" for x in v)  # noqa: E731
    table("Material", ["vídeo", "px", "fps", "s", "metraje fps", "LUFS", "LRA", "pico dBTP", "palabras/s"],
          [[s["slug"], f"{s['ancho']}×{s['alto']}", s["fps"], s["duracion_s"], s["metraje_fps_estimado"],
            s["audio"]["integrated_lufs"], s["audio"]["lra"], s["audio"]["true_peak_dbfs"], s["voz"]["palabras_por_s"]] for s in S])
    table("Subtítulo base", ["vídeo", "localizadas %", "desfase f (p10–p50–p90)", "cuerpo px", "% del ancho",
                              "en pantalla s (p10–p50–p90)", "centro y % (p10–p50–p90)", "respecto a la cara (p10–p50–p90)"],
          [[s["slug"], s["subtitulo_base"]["palabras_localizadas_pct"], f3(s["subtitulo_base"]["desfase_fotogramas_p10_p50_p90"]),
            s["subtitulo_base"]["cuerpo_px_estimado_por_anchura"], s["subtitulo_base"]["cuerpo_pct_ancho"],
            f3(s["subtitulo_base"]["en_pantalla_s_p10_p50_p90"]), f3(s["subtitulo_base"]["centro_y_pct_p10_p50_p90"]),
            f3(s["subtitulo_base"]["respecto_cara_y_p10_p50_p90"])] for s in S])
    L += ["«Cuerpo px» sale de la anchura medida dividida por la anchura de la palabra en SF Pro Display Bold a −60; "
          "el ajuste directo contra la tinta (`fontfit.py`) da en torno a un 7 % menos (98 px en v1).",
          "«Respecto a la cara»: centro del subtítulo medido en alturas de cara desde el centro de la cara "
          "(+0,5 = barbilla; negativo = por encima).", ""]
    table("Palabras de énfasis", ["vídeo", "n", "1 cada s", "gigantes", "ancho % (p25–p50–p75)", "en pantalla s (p10–p50–p90)",
                                   "con línea pequeña", "línea encima", "salen a la vez", "separación centros px", "línea entra antes s"],
          [[s["slug"], s["enfasis"]["n"], s["enfasis"]["cada_s"], s["enfasis"]["gigantes"],
            f3(s["enfasis"]["ancho_pct_p25_p50_p75_de_las_anchas"]), f3(s["enfasis"]["en_pantalla_s_p10_p50_p90"]),
            s["enfasis"]["con_linea_pequena"], s["enfasis"]["linea_encima"], s["enfasis"]["linea_sale_a_la_vez"],
            s["enfasis"]["linea_separacion_centros_px_p50"], s["enfasis"]["linea_entra_antes_s_p50"]] for s in S])
    table("Cortes", ["vídeo", "fuente", "n", "plano medio s", "plano s (p10–p50–p90–máx)", "primer corte s",
                      "corte − inicio de palabra, f (p10–p50–p90)", "tolerancia f", "% dentro de tolerancia", "% tras puntuación"],
          [[s["slug"], s["cortes"]["fuente"], s["cortes"]["n"], s["cortes"]["plano_medio_s"], f3(s["cortes"]["plano_s_p10_p50_p90_max"]),
            s["cortes"]["primer_corte_s"], f3(s["cortes"]["corte_menos_inicio_palabra_f_p10_p50_p90"]),
            s["cortes"]["tolerancia_f_real"], s["cortes"]["pct_a_1f_de_un_inicio"], s["cortes"]["pct_tras_puntuacion"]] for s in S])
    table("Arranque y final", ["vídeo", "1.ª palabra s", "1.er rótulo (f / s)", "1.er énfasis", "última palabra s",
                                "cola tras la voz s", "negro final (f / s)"],
          [[s["slug"], s["voz"]["primera_palabra_s"], f"{s['arranque']['primer_rotulo_f']} / {s['arranque']['primer_rotulo_s']}",
            f"{s['arranque']['primer_enfasis']} @ {s['arranque']['primer_enfasis_s']}", s["voz"]["ultima_palabra_s"],
            s["final"]["cola_tras_ultima_palabra_s"], f"{s['final']['negro_final_fotogramas']} / {s['final']['negro_final_s']}"] for s in S])
    L += ["## Palabras de énfasis, una a una", ""]
    for s in S:
        L += [f"### {s['slug']}", "", "| s | palabra | × base | cuerpo px | ancho % | centro y % | en pantalla s | línea pequeña |", "|---|---|---|---|---|---|---|---|"]
        for e in s["enfasis"]["palabras"]:
            ln = e["linea"]
            L.append(f"| {e['t']} | {e['palabra']} | {e['veces_base']} | {e['cuerpo_px'] or '—'} | {e['ancho_pct']} | {e['cy_pct']} | {e['en_pantalla_s']} | "
                     + (f"«{ln['texto']}» {ln['posicion']}, a {ln['separacion_centros_px']} px, entra {ln['entra_antes_s']:+} s antes" if ln else "—") + " |")
        L.append("")
    return "\n".join(L)


def main():
    S = [video_stats(s) for s in SLUGS]
    (DATOS / "estadisticas.json").write_text(json.dumps(S, ensure_ascii=False, indent=1))
    (DATOS / "estadisticas.md").write_text(md(S))
    print(f"{len(S)} vídeos -> datos/estadisticas.json y datos/estadisticas.md")
    if _font is None:
        print("aviso: no se encontró SF Pro Display Bold; los cuerpos tipográficos quedan sin estimar")


if __name__ == "__main__":
    main()
