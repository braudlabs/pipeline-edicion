"""Utilidades locales del revisor lafabrica-v2p1-B: carga de fotogramas nativos por tubería rawvideo."""
import subprocess
import sys
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import probe, src  # noqa
SLUG = "lafabrica-v2p1"
INFO = probe(SLUG)
W, H = INFO["width"], INFO["height"]

def frames(a, b):
    """dict f -> ndarray uint8 HxWx3 para a..b inclusive (misma búsqueda que sheet.load_full_run)."""
    n = b - a + 1
    tt = max(0.0, (a - 0.5) * INFO["fps_den"] / INFO["fps_num"])
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{tt:.6f}", "-i", str(src(SLUG)), "-frames:v", str(n),
                          "-fps_mode", "passthrough", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    arr = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return {a + k: arr[k] for k in range(arr.shape[0])}

def t(f):
    return f / 24.0
