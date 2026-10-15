#!/usr/bin/env python3
"""Estado verificable y snapshot versionable de notas, sin depender de la sesión."""
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from common import ROOT, ANALYSIS, DATOS, VIDEOS, probe


def main():
    prior_path = ROOT / "CURRENT-STUDY.json"
    prior = json.loads(prior_path.read_text()) if prior_path.exists() else {}
    segments = json.loads((DATOS / "segmentos.json").read_text())
    notes = ROOT / "notas"
    notes.mkdir(exist_ok=True)
    rows = []
    for segment in segments:
        sid, slug = segment["id"], segment["slug"]
        candidates = [p for p in (ANALYSIS / "notas" / f"{sid}.md", notes / f"{sid}.md") if p.exists()]
        source = max(candidates, key=lambda p: p.stat().st_mtime) if candidates else notes / f"{sid}.md"
        coverage_candidates = [p for p in (ANALYSIS / "notas" / f"{sid}.coverage.json", notes / f"{sid}.coverage.json") if p.exists()]
        coverage_path = max(coverage_candidates, key=lambda p: p.stat().st_mtime) if coverage_candidates else source.with_suffix(".coverage.json")
        coverage = json.loads(coverage_path.read_text()) if coverage_path.exists() else {}
        viewed = {Path(p).name for p in coverage.get("sheets_viewed", [])}
        live_index = ANALYSIS / "dense" / slug / "index.json"
        saved_index = DATOS / slug / "dense-index.json"
        if live_index.exists():
            shutil.copy2(live_index, saved_index)
        idx = json.loads(saved_index.read_text())
        expected = {x["sheet"] for x in idx if segment["f0"] <= x["f1"] and x["f0"] <= segment["f1"]}
        unexpected = sorted(viewed - expected)
        viewed &= expected
        sp = ANALYSIS / "supplemental" / slug / "index.json"
        saved_sp = DATOS / slug / "supplemental-index.json"
        if sp.exists():
            shutil.copy2(sp, saved_sp)
        si = json.loads(saved_sp.read_text()) if saved_sp.exists() else []
        expected_extra = {x["sheet"] for x in si if any(segment["f0"] <= f <= segment["f1"] for f in x["frames"])}
        supplemental_viewed = {Path(p).name for p in coverage.get("supplemental_sheets_viewed", [])} & expected_extra
        if source.exists() and source.parent != notes:
            shutil.copy2(source, notes / source.name)
        if coverage_path.exists() and coverage_path.parent != notes:
            shutil.copy2(coverage_path, notes / coverage_path.name)
        row = {**segment, "note": f"notas/{sid}.md" if source.exists() else None,
               "status_reported": coverage.get("status", "legacy_partial" if source.exists() else "pending"),
               "dense_viewed": len(viewed), "dense_expected": len(expected),
               "dense_missing": sorted(expected - viewed),
               "supplemental_viewed": len(supplemental_viewed), "supplemental_expected": len(expected_extra),
               "supplemental_missing": sorted(expected_extra - supplemental_viewed),
               "native_ranges": coverage.get("native_ranges", []),
               "native_frames": coverage.get("native_frames", []),
               "spectrograms_viewed": coverage.get("spectrograms_viewed", []),
               "coverage_anomalies": unexpected,
               "forensic_complete": coverage.get("forensic_complete", False)
                   and viewed == expected and supplemental_viewed == expected_extra}
        rows.append(row)
    materials = []
    for slug in VIDEOS:
        info = probe(slug)
        p = DATOS / slug / "exact-frames.json"
        audit = json.loads(p.read_text()) if p.exists() else None
        materials.append({"slug": slug, "frames": info["frames"], "fps_num": info["fps_num"],
                          "fps_den": info["fps_den"], "exact_audited": audit is not None,
                          "exact_duplicates": len(audit["native_identical_to_previous"]) if audit else None,
                          "legacy_omitted_nonidentical": len(audit["legacy_omitted_nonidentical"]) if audit else None})
    result = {"updated_at": datetime.now(timezone.utc).isoformat(),
              "scope": f"Estudio de {len(VIDEOS)} referencias para algoritmo de edición. Ver revisión V2; sin nuevos renders Birdieballs.",
              "complete": bool(rows) and all(r["forensic_complete"] for r in rows) and {r["slug"] for r in rows} == set(VIDEOS) and prior.get("revision_v2", {}).get("native_review_exhaustive", False),
              "revision_v2": prior.get("revision_v2", {}),
              "materials": materials, "segments": rows,
              "note": "Cobertura declarada de imágenes abiertas, no certificado automático de interpretación correcta. El muestreo de segundos no sustituye este registro."}
    (ROOT / "CURRENT-STUDY.json").write_text(json.dumps(result, ensure_ascii=False, indent=2))
    lines = ["# Estado del estudio", "", "Revisión vigente: [ALGORITMO-V2.md](ALGORITMO-V2.md), [interfaz](http://127.0.0.1:4317/study), [nota V8](notas/v8-revision-v2.md). Cobertura ampliada en CURRENT-STUDY.json.revision_v2; los segmentos de la tabla conservan el desglose anterior.", "", f"Actualizado: {result['updated_at']} (UTC).", "",
             "Fuente regenerable: `python3 scripts/estado.py`. Copia las notas en curso a `notas/`, fuera del directorio ignorado `analysis/`.", "",
             "El estudio solo se cierra cuando cada tramo declara revisión forense completa y tiene cobertura de todas sus hojas densas y suplementarias. Una revisión de hojas reducidas no certifica todos los detalles nativos.", "",
             "| Tramo | Densas abiertas / total | Suplementarias abiertas / total | Estado declarado | Forense completa |",
             "|---|---:|---:|---|---|"]
    for row in rows:
        label = f"[{row['id']}]({row['note']})" if row["note"] else row["id"]
        lines.append(f"| {label} | {row['dense_viewed']}/{row['dense_expected']} | {row['supplemental_viewed']}/{row['supplemental_expected']} | {row['status_reported']} | {'sí' if row['forensic_complete'] else 'no'} |")
    lines += ["", "## Auditoría de omisiones", "",
              "`repeat_frames` heredado usa diferencia por bloques en JPG reducidos, umbral 3/255; no son duplicados exactos. La auditoría nueva compara hashes de todos los fotogramas decodificados a resolución nativa.", "",
              "| Vídeo | Fotogramas | Idénticos al anterior | Omitidos legacy no idénticos |", "|---|---:|---:|---:|"]
    for m in materials:
        lines.append(f"| {m['slug']} | {m['frames']} | {m['exact_duplicates']} | {m['legacy_omitted_nonidentical']} |")
    lines += ["", "## Continuación independiente", "",
              "1. Leer `README.md`, `DECISIONES.md`, `METODO.md`, `ALGORITMO.md` y este estado.",
              "2. Retomar las hojas `dense_missing` / `supplemental_missing` de `CURRENT-STUDY.json` y los detalles pendientes de cada nota; escribir cobertura al terminar cada lote.",
              "3. Guardar evidencia nativa por índice explícito con `sheet.py`; no usar tiempo de seek para asignar fotogramas.",
              "4. Ejecutar `estado.py`, `consolidate.py`, `stats.py` y `estado.py` al terminar. Mantener distinción entre detector, observación y propuesta."]
    (ROOT / "ESTADO.md").write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} tramos: {sum(r['dense_viewed'] for r in rows)}/{sum(r['dense_expected'] for r in rows)} hojas densas; {sum(r['forensic_complete'] for r in rows)} completos forenses")


if __name__ == "__main__":
    main()
