"""Rutas y utilidades compartidas del estudio de estilo del editor."""
import json
import subprocess
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"          # ignorado por git: intermedios pesados
REFS = ANALYSIS / "refs"              # enlaces duros a los originales
FRAMES = ANALYSIS / "frames"          # todos los fotogramas a baja resolución
DATOS = ROOT / "datos"                # resultados ligeros, versionables
LAMINAS = ROOT / "laminas"            # hojas de evidencia seleccionadas

DOWNLOADS = Path.home() / "Downloads"

# slug -> nombre original aportado por el usuario
VIDEOS = {
    "v8": "BRAUDLABS - V8.mp4",
    "landing": "BRAUDLABS - LANDING.mp4",
    "v1-pagado": "BRAUDLABS - V1 -  NI ME HAN PAGADO.mp4",
    "v2-churros": "BRAUDLABS - V2 - CHURROS COCINA.mp4",
    "v3-ia-cara": "BRAUDLABS - V3 - LA IA TE SALE CARA.mp4",
    "v5-maquina": "BRAUDLABS - V5 - LA MAQUINA - REV.mp4",
    "v6-ads90": "BRAUDLABS - V6 - ADS 90S.mp4",
    "v6-ads90-rev": "BRAUDLABS - V6 - ADS 90s - REV.mp4",
    "v7-ads90-rev": "BRAUDLABS - V7 - ADS 90s - REV.mp4",
    "lafabrica-v1": "LaFabrica-V1.mp4",
    "lafabrica-v2p1": "LaFabrica_V2_P1.mp4",
}


def src(slug: str) -> Path:
    p = REFS / f"{slug}.mp4"
    return p if p.exists() else DOWNLOADS / VIDEOS[slug]


def probe(slug: str) -> dict:
    """Metadatos del vídeo; se cachean en datos/<slug>/probe.json."""
    out = DATOS / slug / "probe.json"
    if out.exists():
        return json.loads(out.read_text())
    raw = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(src(slug))],
        capture_output=True, text=True, check=True,
    ).stdout
    j = json.loads(raw)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    fps = Fraction(v["r_frame_rate"])
    info = {
        "slug": slug,
        "original": VIDEOS[slug],
        "width": v["width"],
        "height": v["height"],
        "fps": float(fps),
        "fps_num": fps.numerator,
        "fps_den": fps.denominator,
        "frames": int(v["nb_frames"]),
        "duration": float(j["format"]["duration"]),
        "video_codec": v["codec_name"],
        "video_bitrate": int(v.get("bit_rate", 0)),
        "pix_fmt": v.get("pix_fmt"),
        "audio_codec": a and a["codec_name"],
        "audio_rate": a and int(a["sample_rate"]),
        "audio_channels": a and a["channels"],
        "audio_bitrate": a and int(a.get("bit_rate", 0)),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(info, indent=1, ensure_ascii=False))
    return info


def t_of(frame: int, info: dict) -> float:
    return frame * info["fps_den"] / info["fps_num"]


def f_of(t: float, info: dict) -> int:
    return int(round(t * info["fps_num"] / info["fps_den"]))
