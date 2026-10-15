"""Diseño del anuncio de creatina en lenguaje BRAUDLABS.

Genera la spec declarativa del proyecto de After Effects. Es la única fuente:
el .aep se regenera siempre desde aquí, nunca se parchea a mano. Esa disciplina
es la lección de AD3 — ver MOTION-GRAPHICS-AE-REMOTION.md, §2.

Criterios aplicados de las preferencias de Ale:
  · Subtítulos elegantes, en el tercio inferior, lejos de la cara y del
    encabezado. Sin recuadro negro: el contraste lo dan contorno y sombra.
  · Entradas por un solo eje, alternando izquierda / derecha / abajo.
  · Nada de texto duplicado entre motion y subtítulo: donde el gráfico lleva
    la cifra, esa frase no se subtitula.
  · Las cifras se ligan a lo que pasa en el plano, no flotan sueltas.

Las cuatro cifras comparten una misma marca —anillo, número, etiqueta— y solo
cambia su escala. El código rompe la forma: es el remate.
"""
from pathlib import Path
from PIL import ImageFont
import json
import math

R = Path(__file__).resolve().parents[1]
F = 48
W, H = 1080, 1920
N = 952                                   # 19,833 s

# Paleta BRAUDLABS
CREAM = '#f0f7eb'
LINE = '#bacfa8'
LIGHT = '#92bd65'
INK = '#20271b'
SHADOW = '#182015'

FONT = '/Users/alejandrorubiocamarero/Library/Fonts/SFPRODISPLAYBOLD.OTF'
MASTER = 'CREATINA - FINAL'

OFFSET = {'01-A-hook': 0, '02-B-desarrollo': 338, '03-C-cierre': 712}

# Carril de subtítulos: y1500 sobre el jersey, la franja más oscura y uniforme
# de sus planos (medido: media 63-70, desviación 11-27).
RAIL = 1500
# En los macros el producto ocupa el centro y solo queda limpia la franja
# y1680-1920: no caben gráfico y subtítulo a la vez, así que esos beats los
# lleva el gráfico y no se subtitulan.
RAIL_MACRO = 1775
MARGEN = 940                              # ancho máximo de texto en pantalla

GRUPOS = [
    ('01-A-hook',        5, 10, 'y lo que más me preguntáis', 'right'),
    ('01-A-hook',       11, 13, 'es si hincha',               'left'),
    ('01-A-hook',       14, 19, 'A mí no me ha hinchado',     'bottom'),
    ('02-B-desarrollo',  0,  2, 'Lo que noté',                'left'),
    ('02-B-desarrollo',  3,  5, 'es que aguanto',             'right'),
    ('02-B-desarrollo',  6,  9, 'la última serie entera',     'bottom'),
    ('03-C-cierre',      0,  2, 'Así que nada',               'right'),
    ('03-C-cierre',      3,  5, 'si quieres ponerte',         'left'),
    ('03-C-cierre',      6,  7, 'bien fuerte',                'bottom'),
]
DESTACADO = {'A mí no me ha hinchado'}    # el remate del hook, algo mayor
CORTES = [510, 626, 652, 712]


def ancho(s, size, track):
    """Ancho real en pantalla, incluyendo el tracking de AE (milésimas de eme)."""
    return ImageFont.truetype(FONT, size).getlength(s) + len(s) * size * track / 1000


def ajusta(s, size, track, maximo=MARGEN):
    """Baja el cuerpo hasta que la línea entra en pantalla con margen."""
    while size > 44 and ancho(s, size, track) > maximo:
        size -= 2
    return size


def palabras(clip):
    d = json.load(open(R / f'analysis/{clip}.json'))
    return [w for seg in d['segments'] for w in seg.get('words', [])]


S = {'fps': F, 'master': MASTER, 'width': W, 'height': H, 'duration': N, 'comps': {}}


def comp(name, dur, w=W, h=H):
    c = {'name': name, 'width': w, 'height': h, 'duration': dur, 'layers': []}
    S['comps'][name] = c
    return c


def node(c, kind, name, pos, a, b, **kw):
    n = {'type': kind, 'name': name, 'pos': list(pos), 'from': a, 'to': b, **kw}
    c['layers'].append(n)
    return n


def anim(n, prop, frames, values, ease='out'):
    assert all(x < y for x, y in zip(frames, frames[1:])), (n['name'], prop, frames)
    n.setdefault('anim', {})[prop] = {'frames': frames, 'values': values, 'ease': ease}
    return n


def entra(n, a, axis='bottom', d=14, delta=70, blur=6, fade=6):
    """Entrada por un solo eje, con la curva seca de la serie (influencia 80/15)."""
    p = list(n['pos'])
    p0 = list(p)
    if axis == 'bottom':
        p0[1] += delta
    elif axis == 'left':
        p0[0] -= delta
    elif axis == 'right':
        p0[0] += delta
    anim(n, 'pos', [a, a + d], [p0, p])
    anim(n, 'opacity', [a, a + fade], [0, 1])
    if blur:
        anim(n, 'blur', [a, a + d], [blur, 0])
    return n


def sale(n, b, d=8):
    anim(n, 'opacity', [b - d, b], [1, 0], 'out')
    return n


def texto(c, name, s, x, y, size, col=CREAM, a=0, b=None, align='center',
          track=-45, **kw):
    return node(c, 'text', name, (x, y), a, c['duration'] if b is None else b,
                text=s, size=size, color=col, font='bold', track=track,
                align=align, **kw)


def anillo(c, name, x, y, d, a, b, col=LINE, width=2):
    return node(c, 'ellipse', name, (x, y), a, b, w=d, h=d, color=None,
                stroke=col, strokeWidth=width)


def regla(c, name, x0, x1, y, a, b, col=LINE, width=2, trim=None):
    n = node(c, 'path', name, (0, 0), a, b, points=[[x0, y], [x1, y]],
             stroke=col, strokeWidth=width)
    if trim:
        n['trim'] = trim
    return n


def marca(nombre, dur, cifra, etiqueta, y, d, cifra_size, etiq_size, gap=26):
    """La marca de cifra de la casa: anillo con el número y etiqueta al lado.

    Se centra el conjunto en el eje del cuadro, no solo el anillo, para que no
    quede colgando de un lado.
    """
    c = comp(nombre, dur)
    w_et = ancho(etiqueta, etiq_size, -20)
    total = d + gap + w_et
    x0 = W / 2 - total / 2
    cx = x0 + d / 2
    ex = x0 + d + gap

    anillo(c, 'Anillo', cx, y, d, 0, dur)
    n_cifra = texto(c, 'Cifra', cifra, cx, y + cifra_size * 0.36, cifra_size,
                    a=0, b=dur, track=-30)
    n_etiq = texto(c, 'Etiqueta', etiqueta, ex, y + etiq_size * 0.30, etiq_size,
                   col=CREAM, a=5, b=dur, align='left', track=-20)
    regla(c, 'Subrayado', ex, ex + w_et, y + etiq_size * 0.30 + 20, 8, dur,
          trim=[8, 24])

    entra(n_cifra, 0, 'bottom', delta=44)
    entra(n_etiq, 5, 'left', delta=48)
    anim(c['layers'][0], 'scale', [0, 15], [[0.7, 0.7], [1, 1]])
    anim(c['layers'][0], 'opacity', [0, 7], [0, 1])
    for l in c['layers']:
        sale(l, dur)
    return c


# ============================================================ máster
m = comp(MASTER, N)

node(m, 'video', 'Montaje Remotion', (W / 2, H / 2), 0, N,
     asset='Montaje-Creatina.mp4', anchor=[W / 2, H / 2])
node(m, 'audio', 'Voz y ambiente', (W / 2, H / 2), 0, N,
     asset='Voz-Creatina.wav', anchor=[W / 2, H / 2])

# --- las tres cifras, misma marca y distinta escala
marca('G1 - Seis meses', 108, '6', 'meses', RAIL + 30, 244, 146, 78)
marca('G2 - Cinco gramos', 104, '5', 'gramos', RAIL_MACRO - 15, 152, 96, 60)
marca('G3 - Tres euros', 56, '3€', 'la semana', RAIL_MACRO - 15, 152, 76, 60)

node(m, 'comp', 'Cifra - seis meses', (W / 2, H / 2), 20, 128,
     source='G1 - Seis meses', anchor=[W / 2, H / 2], startTime=20 / F)
node(m, 'comp', 'Cifra - cinco gramos', (W / 2, H / 2), 520, 624,
     source='G2 - Cinco gramos', anchor=[W / 2, H / 2], startTime=520 / F)
node(m, 'comp', 'Cifra - tres euros', (W / 2, H / 2), 654, 710,
     source='G3 - Tres euros', anchor=[W / 2, H / 2], startTime=654 / F)


# ------------------------------------------------- G4 · el código (remate)
# Lo único que el brief obliga a rotular. Rompe la forma de las marcas: en vez
# de anillo, la ráfaga radial del bloque de precio de AD3 sobre una palabra
# ancha, con la regla dibujándose debajo.
g4 = comp('G4 - Codigo', 107)
CX, CY = W / 2, 1488
CODIGO = 'ANDREA10'
size4 = ajusta(CODIGO, 138, -30, 880)
half = ancho(CODIGO, size4, -30) / 2

for i in range(26):
    ang = -math.pi / 2 + (i - 12.5) * math.radians(7.0)
    r0 = 176
    r1 = r0 + (26 if i % 2 == 0 else 17)
    x0, y0 = CX + math.cos(ang) * r0 * 1.9, CY + math.sin(ang) * r0 * 0.62
    x1, y1 = CX + math.cos(ang) * r1 * 1.9, CY + math.sin(ang) * r1 * 0.62
    a = 10 + (i % 6)
    n = node(g4, 'path', f'Radio {i}', (0, 0), a, 107,
             points=[[x0, y0], [x1, y1]], stroke=LINE, strokeWidth=2)
    n['trim'] = [a, a + 13]
    if i % 2 == 0:
        p = node(g4, 'ellipse', f'Punta {i}', (x1, y1), a + 8, 107,
                 w=7, h=7, color=LIGHT)
        anim(p, 'opacity', [a + 8, a + 14], [0, 1])

n_cod = texto(g4, 'Codigo', CODIGO, CX, CY + 40, size4, a=0, b=107, track=-30,
              shadow=[0, 3, 5, SHADOW, 0.55])
regla(g4, 'Regla', CX - half, CX + half, CY + 78, 6, 107, trim=[6, 26])
entra(n_cod, 0, 'bottom', delta=64, blur=7)

node(m, 'comp', 'Codigo ANDREA10', (W / 2, H / 2), 845, 952,
     source='G4 - Codigo', anchor=[W / 2, H / 2], startTime=845 / F)


# ------------------------------------------------------------- subtítulos
tramos = []
for clip, a_i, b_i, s, axis in GRUPOS:
    ws = palabras(clip)
    off = OFFSET[clip]
    tramos.append([off + round(ws[a_i]['start'] * F),
                   off + round(ws[b_i]['end'] * F), s, axis])

# Cada cola se recorta en la entrada del siguiente y en el corte de imagen:
# nunca hay dos subtítulos a la vez ni uno cruzando un plano.
for i, t in enumerate(tramos):
    b = t[1] + 12
    if i + 1 < len(tramos):
        b = min(b, tramos[i + 1][0] - 2)
    for c in CORTES:
        if t[0] < c <= b:
            b = min(b, c)
    t[1] = b

for i, (a, b, s, axis) in enumerate(tramos, 1):
    size = ajusta(s, 104 if s in DESTACADO else 92, -45)
    n = texto(m, f'SUB {i:02d} - {s[:22]}', s, W / 2, RAIL, size, a=a, b=b,
              shadow=[0, 3, 4, SHADOW, 0.65], textStroke=[INK, 1.1])
    entra(n, a, axis, d=10, delta=64, blur=5, fade=3)
    sale(n, b, 7)

out = R / 'src/design.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(S, ensure_ascii=False, indent=1))
print(f'{out.relative_to(R)}: {len(S["comps"])} comps, '
      f'{sum(len(c["layers"]) for c in S["comps"].values())} capas, {N} fotogramas')
print()
print('subtítulos (cuerpo ajustado al ancho de pantalla):')
for l in m['layers']:
    if l['type'] == 'text':
        w = ancho(l['text'], l['size'], l['track'])
        print(f'  f{l["from"]:4}–{l["to"]:4}  {l["size"]:3} pt  {w:5.0f} px  «{l["text"]}»')
print()
print(f'código: {size4} pt, {ancho(CODIGO, size4, -30):.0f} px')
