#!/usr/bin/env python3
"""Audita índices y duplicados por hash del fotograma nativo decodificado.

No sustituye métricas anteriores: añade exact-frames.json y hojas suplementarias
para TODOS los índices omitidos por el umbral legacy que no son idénticos.
"""
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from common import ANALYSIS, DATOS, FRAMES, VIDEOS, probe, src, t_of


def audit(slug):
    info = probe(slug)
    outdir = DATOS / slug
    output = outdir / "native-framemd5.txt"
    if not output.exists():
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-threads", "2", "-i", str(src(slug)),
             "-map", "0:v:0", "-an", "-fps_mode", "passthrough", "-f", "framemd5", "-"],
            capture_output=True, text=True, check=True)
        output.write_text(result.stdout)
    records = [line.split(",") for line in output.read_text().splitlines()
               if line.strip() and not line.startswith("#")]
    hashes = [row[-1].strip() for row in records]
    if len(hashes) != info["frames"]:
        raise ValueError(f"{slug}: decodificados {len(hashes)} != probe {info['frames']}")
    exact = {i for i in range(1, len(hashes)) if hashes[i] == hashes[i - 1]}
    legacy = set(json.loads((outdir / "repeats.json").read_text())["repeat_frames"])
    omitted_nonidentical = sorted(legacy - exact)
    supplemental = ANALYSIS / "supplemental" / slug
    supplemental.mkdir(parents=True, exist_ok=True)
    vertical = info["height"] > info["width"]
    cols, rows, tw = (10, 4, 152) if vertical else (5, 6, 308)
    per, gap, lab = cols * rows, 4, 14
    font = ImageFont.load_default(size=11)
    index = []
    for offset in range(0, len(omitted_nonidentical), per):
        chunk = omitted_nonidentical[offset:offset + per]
        first = Image.open(FRAMES / slug / f"f{chunk[0]:06d}.jpg")
        th = round(first.height * tw / first.width)
        sheet = Image.new("RGB", (cols * (tw + gap) + gap,
                           ((len(chunk) + cols - 1) // cols) * (th + lab + gap) + gap), (24, 24, 24))
        draw = ImageDraw.Draw(sheet)
        for k, f in enumerate(chunk):
            im = Image.open(FRAMES / slug / f"f{f:06d}.jpg").convert("RGB").resize((tw, th), Image.Resampling.LANCZOS)
            x, y = gap + (k % cols) * (tw + gap), gap + (k // cols) * (th + lab + gap)
            draw.text((x + 1, y), f"f{f} {t_of(f, info):.3f}s", font=font, fill=(100, 240, 255))
            sheet.paste(im, (x, y + lab))
        name = f"s{offset // per:03d}_f{chunk[0]:05d}-f{chunk[-1]:05d}.jpg"
        sheet.save(supplemental / name, quality=90)
        index.append({"sheet": name, "frames": chunk, "f0": chunk[0], "f1": chunk[-1]})
    (supplemental / "index.json").write_text(json.dumps(index, indent=1))
    report = {
        "slug": slug, "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "ffmpeg framemd5, raw decoded native pixel format, compare adjacent frame hashes",
        "native_hashes": str(output.relative_to(DATOS.parent)),
        "hash_file_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "frames": len(hashes), "native_identical_to_previous": sorted(exact),
        "legacy_similar_to_previous_count": len(legacy),
        "legacy_omitted_nonidentical": omitted_nonidentical,
        "legacy_kept_identical": sorted(exact - legacy),
        "supplemental_sheets": len(index),
        "note": "Un hash distinto puede ser ruido de compresión; nunca prueba por sí solo un evento editorial. Las hojas suplementarias usan JPG reducidos, los efectos finos requieren extracción nativa.",
    }
    (outdir / "exact-frames.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    return f"{slug}: {len(hashes)} f, {len(exact)} idénticos, {len(omitted_nonidentical)} omitidos no idénticos, {len(index)} hojas suplementarias"


if __name__ == "__main__":
    slugs = sys.argv[1:] or list(VIDEOS)
    with ThreadPoolExecutor(max_workers=2) as pool:
        for line in pool.map(audit, slugs):
            print(line, flush=True)
