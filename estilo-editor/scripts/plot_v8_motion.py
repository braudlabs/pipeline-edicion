#!/usr/bin/env python3
"""Standalone measured-trajectory comparison. Raw rejected points remain in JSON."""
import json,math
from common import DATOS
p=DATOS/'revision-v2';fit=json.loads((p/'v8-motion-fit.json').read_text());curves=json.loads((p/'v8-native-curves.json').read_text());starts=fit['firstVisibleFrames'];bad={(r['label'],r['frame']) for r in fit['rejectedSamples']}
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="620" viewBox="0 0 1000 620"><rect width="1000" height="620" fill="#141819"/><style>text{font-family:Arial,sans-serif;fill:#b6c0c0;font-size:13px}.title{font-size:22px;fill:#eef3ed}</style><text x="50" y="42" class="title">V8 · La misma entrada; la salida requiere otra fase</text><text x="50" y="69">ΔY de tinta respecto a edad2 (px) · resolución nativa · umbral cromático30</text>']
for v in [-40,-20,0,20,40]:svg.append(f'<line x1="90" x2="900" y1="{300-v*4}" y2="{300-v*4}" stroke="#ffffff15"/><text x="46" y="{305-v*4}">{v}px</text>')
for i,c in enumerate(curves):
 rs=[r for r in c['rows'] if r['threshold30'] and 2<=r['frame']-starts[c['id']]<=32 and (c['id'],r['frame']) not in bad];base=next(r['threshold30']['y'] for r in rs if r['frame']-starts[c['id']]==2)
 pts=' '.join(f"{90+(r['frame']-starts[c['id']]-2)*26:.1f},{300-(r['threshold30']['y']-base)*4:.1f}" for r in rs)
 color=['#d8ff63','#81cbd8','#eeb487'][i];svg.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2"/><text x="{70+i*210}" y="112" style="fill:{color}">{c["id"]}</text>')
f=lambda t:math.exp(-fit['decayPerSourceFrame']*t)*(fit['cosCoefficientPx']*math.cos(fit['omegaRadiansPerSourceFrame']*t)+fit['sinCoefficientPx']*math.sin(fit['omegaRadiansPerSourceFrame']*t))
pts=' '.join(f'{90+(t-2)*26:.2f},{300-(f(t)-f(2))*4:.2f}' for t in range(2,33));svg.append(f'<polyline points="{pts}" fill="none" stroke="#eeeeee" stroke-width="1.5" stroke-dasharray="5,5"/><text x="700" y="112">Ajuste compartido (discontinuo)</text>')
for t in range(2,34,4):svg.append(f'<text x="{85+(t-2)*26}" y="540">{t}</text>')
svg+=['<text x="90" y="564">Edad en fotogramas del origen (59,94fps). ΔY positivo = más abajo en el vídeo.</text><text x="50" y="590">Sirve diverge al salir; no usar una curva única para toda la palabra.</text><text x="50" y="611">f3361 excluido: máscara cromática fragmentada al desvanecerse. Datos crudos conservados.</text></svg>'];(p/'v8-motion-comparison.svg').write_text(''.join(svg))
