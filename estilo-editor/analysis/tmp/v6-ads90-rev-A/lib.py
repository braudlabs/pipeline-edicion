"""Utilidades locales del revisor v6-ads90-rev-A: lectura rápida de fotogramas nativos."""
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import probe, src  # noqa: E402

SLUG = "v6-ads90-rev"
INFO = probe(SLUG)
W, H = INFO["width"], INFO["height"]


def frames(a, b):
    """Fotogramas a..b (incluidos) como array uint8 [n, H, W, 3]. Misma búsqueda que sheet.load_full_run."""
    count = b - a + 1
    t = max(0.0, (a - 0.5) * INFO["fps_den"] / INFO["fps_num"])
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t:.6f}", "-i", str(src(SLUG)), "-frames:v", str(count),
         "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True,
    ).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return arr


def gray(a):
    return a.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)
