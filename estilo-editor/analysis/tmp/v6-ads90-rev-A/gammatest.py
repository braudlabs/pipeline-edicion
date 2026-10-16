#!/usr/bin/env python3
"""¿El fundido se mezcla en espacio gamma (código) o en luz lineal? Compara alpha sobre fondos oscuros y claros.
  gammatest.py A B x0 y0 x1 y1 --ref R --pre P --dxs "f:dx,f:dx,..." (o --dx0 n para un desplazamiento fijo)
"""
import argparse, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from lib import frames
from alpha2 import erode, shift  # noqa

