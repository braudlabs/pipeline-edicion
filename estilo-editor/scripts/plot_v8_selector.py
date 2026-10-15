#!/usr/bin/env python3
"""Standalone plot of measured selection handles, with semantic phase annotations."""
import json
from common import DATOS
root = DATOS / 'revision-v2'
rows = json.loads((root / 'v8-selector-curves.json').read_text())['rows']
x = lambda f: 70 + (f - 196) / 130 * 870
y = lambda width: 410 - width / 850 * 290
points = ' '.join(f'{x(r["frame"]):.2f},{y(r["threshold70"]["separationX"]):.2f}'
                  for r in rows if 196 <= r['frame'] <= 326 and r['threshold70']['separationX'] is not None)
grid = ''.join(f'<line x1="70" y1="{y(w)}" x2="940" y2="{y(w)}" stroke="#354943"/>'
               f'<text x="58" y="{y(w)+5}" text-anchor="end">{w}</text>' for w in [0, 200, 400, 600, 800])
ticks = ''.join(f'<text x="{x(f)}" y="438" text-anchor="middle">f{f}</text>' for f in [196, 210, 230, 255, 270, 300, 326])
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 535" role="img" aria-labelledby="title desc">
<title id="title">V8: la selección se cierra y reabre; no es escala de texto</title>
<desc id="desc">Separación horizontal entre medianas de los tiradores azules, de frame196 a326. 810píxeles en230, 2en255–257, 810en300. Centro horizontal aproximadamente539píxeles. Palabras y máscara requieren pistas independientes.</desc>
<rect width="1000" height="535" fill="#11221e"/>
<g fill="#dfece6" font-family="system-ui,sans-serif" font-size="15">
<text x="35" y="35" font-size="23">Clientes → igualdad → empleados</text>
<text x="35" y="62" fill="#adbbb5">Medida nativa: distancia entre tiradores (px), no ancho de glifos</text>
<rect x="{x(231)}" y="100" width="{x(258)-x(231)}" height="310" fill="#4c3750" opacity=".45"/>
<rect x="{x(258)}" y="100" width="{x(300)-x(258)}" height="310" fill="#224d5f" opacity=".45"/>
{grid}{ticks}<polyline points="{points}" fill="none" stroke="#97e5ff" stroke-width="3"/>
<text x="{x(244)}" y="95" text-anchor="middle">Cierre + =</text>
<text x="{x(281)}" y="95" text-anchor="middle">Reapertura + empleados</text>
<text x="35" y="480">Centro: 538,5–540,5 px. Sensibilidad entre dos umbrales: máximo 1 px.</text>
<text x="35" y="508" fill="#adbbb5">Nuevos, palabra central, selección y oclusión del pelo tienen tiempos/capas independientes.</text>
</g></svg>'''
(root / 'v8-selector-comparison.svg').write_text(svg)
print(root / 'v8-selector-comparison.svg')
