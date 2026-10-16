#!/usr/bin/env python3
"""Anchura 10-90 % de un borde horizontal o vertical (desenfoque) en una fila/columna dada.
  edgew.py A B  eje(h|v)  pos  ini fin     -> perfil de min(R,G,B) a lo largo de la línea
"""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
from common import probe
from sheet import load_full_run
slug = "lafabrica-v1"; info = probe(slug)
a, b, ax, pos, i0, i1 = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
dump = len(sys.argv) > 7
imgs = load_full_run(slug, a, b - a + 1, info)
for k, im in enumerate(imgs):
    A = np.asarray(im, np.float32)
    if ax == "h":
        line = A[pos - 3:pos + 4, i0:i1].mean(axis=0)
    else:
        line = A[i0:i1, pos - 3:pos + 4].mean(axis=1)
    v = line.min(axis=1)
    lo, hi = np.percentile(v, 3), np.percentile(v, 97)
    n = (v - lo) / max(1, hi - lo)
    # primer cruce de 10 % y de 90 %
    i10 = int(np.argmax(n >= 0.1)); i90 = int(np.argmax(n >= 0.9)); i50 = int(np.argmax(n >= 0.5))
    print(f"f{a+k}: fondo {lo:.0f} tinta {hi:.0f}  10%@{i0+i10} 50%@{i0+i50} 90%@{i0+i90}  ancho10-90={i90-i10}px" + ("  " + " ".join(f"{x:.0f}" for x in v) if dump else ""))
