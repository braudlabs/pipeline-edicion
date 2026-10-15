#!/usr/bin/env python3
"""Color exacto en puntos de un fotograma a resolución nativa (media de 5x5 px).

  px.py <slug> <fotograma> x,y [x,y ...]        coordenadas en píxeles del original
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from common import probe  # noqa: E402
from sheet import load_full  # noqa: E402

slug, f = sys.argv[1], int(sys.argv[2])
im = np.asarray(load_full(slug, f, probe(slug)), np.float32)
for p in sys.argv[3:]:
    x, y = [int(float(v)) for v in p.split(",")]
    c = im[max(0, y - 2):y + 3, max(0, x - 2):x + 3].reshape(-1, 3).mean(axis=0)
    print(f"f{f} ({x},{y}): rgb({c[0]:.0f},{c[1]:.0f},{c[2]:.0f})  #{int(round(c[0])):02X}{int(round(c[1])):02X}{int(round(c[2])):02X}")
