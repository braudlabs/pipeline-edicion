#!/usr/bin/env python3
"""Comprueba que las capturas que usa el montaje están en modo producción.

Regla del feedback del Avance 03 («se ve muy IA»): las marcas de desarrollo del frontal
(«DEV», el selector «Explorar el inicio», «DESARROLLO / BRAUD») delatan prototipo.
Solo se revisan las capturas que nombra algún fuente de remotion/src.
Uso: python3 tools/check-snaps.py   (sale con código 1 si alguna falla)
"""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
snaps = root / 'snaps'
sources = '\n'.join(p.read_text() for p in (root / 'remotion' / 'src').rglob('*.tsx'))
MARKERS = {
    'etiqueta DEV': re.compile(r'class="edition-label">DEV<'),
    'selector «Explorar el inicio»': re.compile(r'Explorar el inicio'),
    'cabecera «DESARROLLO / …»': re.compile(r'DESARROLLO / '),
}

def used(name: str) -> bool:
    # comillas o ruta snaps/…; no cuentan las palabras de la locución: at(4, 'idea'), A(2, 'idea'), endOf(2, 'Studio')
    rx = rf"""(?<!\b[aA]\(\d, )(?<!\bat\(\d, )(?<!endOf\(\d, )['"]{re.escape(name)}(?:-[a-z]+)?['"]|snaps/{re.escape(name)}[.-]"""
    return bool(re.search(rx, sources))

bad = 0
for html in sorted(snaps.glob('*.html')):
    name = html.stem
    if not used(name):
        continue
    text = html.read_text(errors='ignore')
    hits = [label for label, rx in MARKERS.items() if rx.search(text)]
    print(('FALLA ' if hits else 'ok    ') + name + (': ' + ', '.join(hits) if hits else ''))
    bad += bool(hits)
sys.exit(1 if bad else 0)
