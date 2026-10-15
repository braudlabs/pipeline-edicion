"""Contrasta la reconstrucción con los volcados que devolvió el propio After Effects.

`v7/ae/patch-results.jsonl` guarda un `ae_comp_info` posterior al parche de V7,
es decir, el estado exacto de la imagen que se entregó en V8. Si la reproducción
de operaciones es correcta, cada capa debe coincidir en nombre y en entrada/salida.
"""
from pathlib import Path
import json
import sys

R = Path(__file__).resolve().parents[1]
AD3 = R.parent
F = 48

design = json.load(open(R / 'src/design.json'))
comps = design['comps']

dumps = {}
for line in open(AD3 / 'v7/ae/patch-results.jsonl'):
    res = json.loads(line).get('result', {}).get('structuredContent', {}).get('result')
    if isinstance(res, dict) and 'comps' in res:
        for c in res['comps']:
            if c.get('layers'):
                dumps[c['name']] = c

MAP = {'AD3 - V7 FINAL': design['master']}
bad = 0
total = 0

for ae_name, c in dumps.items():
    name = MAP.get(ae_name, ae_name)
    mine = comps.get(name)
    print(f'\n=== {ae_name} → {name} ===')
    if mine is None:
        print('  FALTA la comp')
        bad += 1
        continue
    if abs(mine['duration'] - c['duration'] * F) > 0.01:
        print(f'  duración {mine["duration"]} vs AE {c["duration"] * F:.0f}  ✗')
        bad += 1
    ours = {l['name']: l for l in mine['layers']}
    if len(ours) != len(c['layers']):
        print(f'  nº de capas {len(ours)} vs AE {len(c["layers"])}  ✗')
        bad += 1
    for l in c['layers']:
        total += 1
        m = ours.get(l['name'])
        if m is None:
            print(f'  {l["name"]:30} FALTA  ✗')
            bad += 1
            continue
        ae_in, ae_out = l['inPoint'] * F, l['outPoint'] * F
        if abs(m['in'] - ae_in) > 0.01 or abs(m['out'] - ae_out) > 0.01:
            print(f'  {l["name"]:30} {m["in"]:7.1f}→{m["out"]:7.1f}  '
                  f'AE {ae_in:7.1f}→{ae_out:7.1f}  ✗')
            bad += 1

print(f'\n{total} capas contrastadas, {bad} discrepancias')
sys.exit(1 if bad else 0)
