#!/usr/bin/env python3
"""Fotogramas de estilo de AD6 «PapiCat Snacks».

Compone tipografia real sobre fotogramas reales del montaje renderizado.
Nada de maquetas: los fondos salen de output/ad6-montaje-base.mov y la
geometria de la banda verde sale de analysis/pista-banda-montaje.json.
"""
import os, subprocess, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOV = os.path.join(ROOT, "output", "ad6-montaje-base.mov")
OUT = os.path.join(ROOT, "output", "fotogramas-estilo")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920

FT_MARCA = "/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf"
FT_SUB = "/System/Library/Fonts/Avenir Next.ttc"          # idx 2 = Demi Bold
FT_SUB_I = 2

CREMA = (242, 228, 204)
CREMA_ALTA = (255, 243, 224)
COCOA = (59, 42, 28)
SAGE_CLARO = (176, 168, 132)

# Geometria de la banda medida sobre el montaje (1080x1920), plano E:
#   f291  bolsa x 336-749  banda y 940-1088 (h 148)   cara plana x ~360-700
#   f326  bolsa x 320-757  banda y 952-1108 (h 156)
#   f386  bolsa x 270-785  banda y 976-1160 (h 184)
# La banda arquea hacia abajo en el centro ~14 px y cae ~10 px de izquierda a derecha.
BANDA = {
    291: dict(x0=292, x1=760, y0=927, y1=1078, bow=14, tilt=-10),
    326: dict(x0=300, x1=772, y0=940, y1=1098, bow=15, tilt=-10),
    386: dict(x0=252, x1=800, y0=963, y1=1150, bow=17, tilt=-11),
}


def fotograma(n):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", MOV, "-vf", f"trim=start_frame={n}:end_frame={n+1}",
         "-fps_mode", "passthrough", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
        capture_output=True).stdout
    return Image.frombytes("RGB", (W, H), raw[:W * H * 3])


def capa_texto(texto, fuente, alto_caja, color, tracking=0.0, ancho_max=None):
    """Dibuja el texto en una capa RGBA ajustada, con altura de mayusculas ~alto_caja."""
    size = int(alto_caja / 0.716)
    f = ImageFont.truetype(fuente, size) if isinstance(fuente, str) else fuente(size)
    # medir con tracking
    anchos = [f.getlength(c) for c in texto]
    extra = tracking * size
    total = sum(anchos) + extra * (len(texto) - 1)
    if ancho_max and total > ancho_max:
        size = int(size * ancho_max / total)
        f = ImageFont.truetype(fuente, size) if isinstance(fuente, str) else fuente(size)
        anchos = [f.getlength(c) for c in texto]
        extra = tracking * size
        total = sum(anchos) + extra * (len(texto) - 1)
    asc, desc = f.getmetrics()
    lay = Image.new("RGBA", (int(total) + 4, asc + desc + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    x = 2.0
    for c in texto:
        d.text((x, 2), c, font=f, fill=color + (255,))
        x += f.getlength(c) + extra
    bb = lay.getbbox()
    return lay.crop(bb), size


def curvar(lay, bow, tilt, curvatura=0.30):
    """Deforma una capa plana sobre el cilindro de la bolsa.

    Comprime horizontalmente hacia los bordes (proyeccion de un cilindro),
    arquea hacia abajo en el centro (bow) y aplica una caida lateral (tilt).
    """
    a = np.array(lay).astype(np.float32)
    h, w = a.shape[:2]
    margen = int(bow + abs(tilt)) + 6
    out = np.zeros((h + 2 * margen, w, 4), np.float32)
    th = curvatura * math.pi / 2
    xs = np.arange(w)
    u = (xs / (w - 1)) * 2 - 1                     # -1 .. 1
    # muestreo inverso: para la columna de salida j, que columna de entrada la alimenta
    su = np.sin(u * th) / math.sin(th)             # posicion proyectada de cada columna
    dest = (su + 1) / 2 * (w - 1)
    src = np.interp(xs, dest, xs)                  # inversa
    dy = bow * (1 - ((xs / (w - 1)) * 2 - 1) ** 2) + tilt * (xs / (w - 1))
    for j in range(w):
        s0 = int(np.floor(src[j])); fr = src[j] - s0
        s1 = min(s0 + 1, w - 1)
        col = a[:, s0] * (1 - fr) + a[:, s1] * fr
        off = margen + dy[j]
        o0 = int(np.floor(off)); f2 = off - o0
        out[o0:o0 + h, j] += col * (1 - f2)
        out[o0 + 1:o0 + 1 + h, j] += col * f2
        # sombreado del cilindro: los bordes reciben menos luz
        k = 1 - 0.30 * (abs(u[j]) ** 2)
        out[:, j, :3] *= k
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), margen


def pegar(base, lay, cx, cy, sombra=None, halo=None):
    x = int(cx - lay.width / 2); y = int(cy - lay.height / 2)
    if halo:
        col, op, rad = halo
        g = Image.new("RGBA", (lay.width + rad * 4, lay.height + rad * 4), (0, 0, 0, 0))
        m = lay.split()[3]
        sol = Image.new("RGBA", lay.size, col + (int(255 * op),))
        g.paste(sol, (rad * 2, rad * 2), m)
        g = g.filter(ImageFilter.GaussianBlur(rad))
        base.alpha_composite(g, (x - rad * 2, y - rad * 2))
    if sombra:
        col, op, rad, dx, dy = sombra
        g = Image.new("RGBA", (lay.width + rad * 4, lay.height + rad * 4), (0, 0, 0, 0))
        sol = Image.new("RGBA", lay.size, col + (int(255 * op),))
        g.paste(sol, (rad * 2, rad * 2), lay.split()[3])
        g = g.filter(ImageFilter.GaussianBlur(rad))
        base.alpha_composite(g, (x - rad * 2 + dx, y - rad * 2 + dy))
    base.alpha_composite(lay, (x, y))


def marca_en_banda(base, f, alto_linea, lineas, ancho_frac=0.80, op=1.0):
    """Coloca el lockup sobre la banda, curvado al cilindro."""
    b = BANDA[f]
    bw = (b["x1"] - b["x0"]) * ancho_frac
    cx = (b["x0"] + b["x1"]) / 2
    cy = (b["y0"] + b["y1"]) / 2
    alturas, capas = [], []
    for txt, alt, trk in lineas:
        lay, _ = capa_texto(txt, FT_MARCA, alt, CREMA, tracking=trk, ancho_max=bw)
        capas.append(lay); alturas.append(lay.height)
    lead = int(alto_linea * 0.26)
    tot = sum(alturas) + lead * (len(capas) - 1)
    y = cy - tot / 2
    for lay, hh in zip(capas, alturas):
        cur, marg = curvar(lay, b["bow"], b["tilt"])
        if op < 1:
            al = cur.split()[3].point(lambda v: int(v * op)); cur.putalpha(al)
        pegar(base, cur, cx, y + hh / 2,
              sombra=((30, 22, 12), 0.55, 5, 0, 3))
        y += hh + lead


def subtitulo(base, texto, cy, alto=62, color=COCOA, halo=True, ancho=0.82, trk=0.01):
    lay, _ = capa_texto(texto, lambda s: ImageFont.truetype(FT_SUB, s, index=FT_SUB_I),
                        alto, color, tracking=trk, ancho_max=W * ancho)
    pegar(base, lay, W / 2, cy,
          halo=((CREMA_ALTA), 0.42, 14) if halo else None,
          sombra=((40, 28, 18), 0.22, 8, 0, 3))
    return lay


# ─────────────────────────── las tres ideas ───────────────────────────

def idea_A(f):
    """TEJIDO — el lockup esta crocheteado DENTRO de la banda, en lana crema.
    Dos lineas ajustadas a la banda. Abajo, la coletilla sobre la alfombra."""
    im = fotograma(f).convert("RGBA")
    marca_en_banda(im, f, 58, [("PapiCat", 62, 0.02), ("SNACKS", 34, 0.30)], 0.78)
    if f >= 340:
        subtitulo(im, "lo único capaz de hacer correr a tu gato", 1592, 46, trk=0.015)
    return im


def idea_B(f):
    """SELLO — el lockup llega entero desde abajo y aterriza en la banda con
    fisica de stop-motion. Una sola linea grande, la coletilla en la alfombra."""
    im = fotograma(f).convert("RGBA")
    marca_en_banda(im, f, 74, [("PapiCat", 76, 0.0)], 0.86)
    b = BANDA[f]
    lay, _ = capa_texto("SNACKS", FT_MARCA, 30, CREMA, tracking=0.42,
                        ancho_max=(b["x1"] - b["x0"]) * 0.55)
    cur, _ = curvar(lay, b["bow"] * 0.6, b["tilt"] * 0.6)
    al = cur.split()[3].point(lambda v: int(v * 0.92)); cur.putalpha(al)
    pegar(im, cur, (b["x0"] + b["x1"]) / 2, b["y1"] + 46, sombra=((40, 28, 18), 0.3, 6, 0, 3))
    if f >= 340:
        subtitulo(im, "lo único capaz de hacer correr a tu gato", 1592, 46, trk=0.015)
    return im


def idea_C(f):
    """DOS ESCALAS — el rotulo grande se apoya en la ALFOMBRA delante de la
    bolsa, como un objeto mas; la etiqueta pequena aparece luego en la banda."""
    im = fotograma(f).convert("RGBA")
    if f >= 320:
        marca_en_banda(im, f, 40, [("PapiCat", 40, 0.02)], 0.64, op=0.85)
    lay, _ = capa_texto("PapiCat", FT_MARCA, 112, COCOA, tracking=0.0, ancho_max=W * 0.72)
    pegar(im, lay, W / 2, 1432, halo=(CREMA_ALTA, 0.40, 18), sombra=((40, 26, 14), 0.30, 12, 0, 8))
    l2, _ = capa_texto("SNACKS", FT_MARCA, 44, COCOA, tracking=0.40, ancho_max=W * 0.58)
    pegar(im, l2, W / 2, 1540, halo=(CREMA_ALTA, 0.40, 14), sombra=((40, 26, 14), 0.28, 9, 0, 6))
    if f >= 340:
        subtitulo(im, "lo único capaz de hacer correr a tu gato", 1690, 42, trk=0.015)
    return im


def hoja(imgs, etiquetas, ruta, ancho_movil=372):
    """Contacto a tamano de movil con etiqueta debajo."""
    esc = ancho_movil / W
    hh = int(H * esc)
    pad, top = 18, 44
    sheet = Image.new("RGB", (len(imgs) * (ancho_movil + pad) + pad, hh + top + pad), (24, 22, 20))
    d = ImageDraw.Draw(sheet)
    ft = ImageFont.truetype(FT_SUB, 20, index=FT_SUB_I)
    for i, (im, lab) in enumerate(zip(imgs, etiquetas)):
        x = pad + i * (ancho_movil + pad)
        sheet.paste(im.convert("RGB").resize((ancho_movil, hh), Image.LANCZOS), (x, top))
        d.text((x, 14), lab, font=ft, fill=(236, 228, 214))
    sheet.save(ruta)
    return ruta


# ─────────── integracion en la lana: la textura de la banda atraviesa la letra ───────────

def tejer(base, lay, cx, cy, fuerza=0.55, fibra=True):
    """Funde una capa de texto con la lana de debajo.

    1. Toma la luminancia local del fondo, la normaliza y la usa para modular
       el relleno: los puntos del croche aparecen DENTRO de la letra.
    2. Desplaza un poco el borde con esa misma textura, para que el contorno
       siga los puntos en vez de ser un vector limpio.
    3. Anade un halo de fibra suelta (la pelusa de la lana).
    """
    x = int(cx - lay.width / 2); y = int(cy - lay.height / 2)
    fondo = np.array(base.convert("RGB").crop((x, y, x + lay.width, y + lay.height))).astype(np.float32)
    lum = fondo @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    suave = np.array(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
    det = np.clip((lum - suave) / 26.0, -1, 1)            # grano del punto, -1..1
    a = np.array(lay).astype(np.float32)
    alpha = a[..., 3] / 255.0
    # 2. borde mordido por la textura
    despl = np.clip(alpha + det * 0.22 * fuerza, 0, 1)
    # 1. relleno modulado
    rgb = a[..., :3] * (1.0 + det[..., None] * 0.42 * fuerza)
    rgb = rgb * (0.90 + 0.10 * np.clip(suave / 150.0, 0, 1.6))[..., None]
    nueva = Image.fromarray(np.clip(np.dstack([rgb, despl * 255]), 0, 255).astype(np.uint8))
    if fibra:
        m = nueva.split()[3].filter(ImageFilter.GaussianBlur(3.5))
        h = Image.new("RGBA", lay.size, (245, 234, 212, 0)); h.putalpha(m.point(lambda v: int(v * 0.34)))
        base.alpha_composite(h, (x, y))
    # sombra propia: la letra esta HUNDIDA en la lana, no encima
    s = Image.new("RGBA", (lay.width + 16, lay.height + 16), (0, 0, 0, 0))
    sol = Image.new("RGBA", lay.size, (26, 20, 10, 150)); s.paste(sol, (8, 8), nueva.split()[3])
    s = s.filter(ImageFilter.GaussianBlur(3))
    base.alpha_composite(s, (x - 8 + 1, y - 8 + 3))
    base.alpha_composite(nueva, (x, y))


def marca_tejida(base, f, lineas, ancho_frac=0.80, op=1.0):
    b = BANDA[f]
    bw = (b["x1"] - b["x0"]) * ancho_frac
    cx = (b["x0"] + b["x1"]) / 2; cy = (b["y0"] + b["y1"]) / 2
    capas = []
    for txt, alt, trk in lineas:
        lay, _ = capa_texto(txt, FT_MARCA, alt, CREMA, tracking=trk, ancho_max=bw)
        capas.append(lay)
    lead = int(lineas[0][1] * 0.30)
    tot = sum(l.height for l in capas) + lead * (len(capas) - 1)
    y = cy - tot / 2
    for lay in capas:
        cur, _ = curvar(lay, b["bow"], b["tilt"])
        if op < 1:
            cur.putalpha(cur.split()[3].point(lambda v: int(v * op)))
        tejer(base, cur, cx, y + lay.height / 2)
        y += lay.height + lead


def idea_A2(f, coletilla=False, dos_lineas=True):
    im = fotograma(f).convert("RGBA")
    ln = [("PapiCat", 60, 0.01), ("SNACKS", 30, 0.44)] if dos_lineas else [("PapiCat Snacks", 42, 0.02)]
    marca_tejida(im, f, ln, 0.80 if dos_lineas else 0.92)
    if coletilla:
        subtitulo(im, "lo único capaz de hacer correr a tu gato", 1600, 44, trk=0.02)
    return im


# ─────────────────────────── sistema de subtitulos ───────────────────────────
# Regla de color, decidida por medicion (analysis/mapa-texto2.json):
#   fondo claro (alfombra, luma 150-185)  -> COCOA  #3B2A1C
#   fondo oscuro (tarima, banda, luma <120) -> CREMA #F2E4CC
# Apoyo: halo difuso del color contrario al 35-42 %, nunca caja ni recuadro.

SUBS = [
    # (fotograma de muestra, texto, cy, alto, color, eje de entrada)
    (30,  "Hay dos cosas\nque despiertan a un gato", 1706, 52, "cocoa", "abajo"),
    (70,  "Una es el ruido de la bolsa",             1730, 52, "cocoa", "izquierda"),
    (100, "y la otra…",                              1754, 54, "crema", "abajo"),
    (150, "también es el ruido de la bolsa",          1754, 50, "crema", "derecha"),
    (200, "Snacks de pollo, sin cereales",            1742, 50, "cocoa", "izquierda"),
    (262, "del tamaño exacto\npara una boca pequeña", 1706, 48, "cocoa", "derecha"),
]


def bloque_sub(base, texto, cy, alto, modo, ancho=0.80):
    color = COCOA if modo == "cocoa" else CREMA
    halo = (CREMA_ALTA, 0.40, 15) if modo == "cocoa" else ((28, 20, 12), 0.45, 16)
    som = ((44, 30, 18), 0.22, 9, 0, 3) if modo == "cocoa" else ((20, 14, 8), 0.40, 7, 0, 3)
    lineas = texto.split("\n")
    capas = [capa_texto(l, lambda s: ImageFont.truetype(FT_SUB, s, index=FT_SUB_I),
                        alto, color, tracking=0.012, ancho_max=W * ancho)[0] for l in lineas]
    lead = int(alto * 0.62)
    tot = sum(c.height for c in capas) + lead * (len(capas) - 1)
    y = cy - tot / 2
    for c in capas:
        pegar(base, c, W / 2, y + c.height / 2, halo=halo, sombra=som)
        y += c.height + lead
    # control: el limite inferior real del bloque (descendentes incluidas)
    return y - lead


def muestra_sub(i):
    f, txt, cy, alto, modo, eje = SUBS[i]
    im = fotograma(f).convert("RGBA")
    fondo = bloque_sub(im, txt, cy, alto, modo)
    return im, f, eje, fondo


# ───────── sistema v2: mas peso, dos estaciones medidas, halo difuso (no caja) ─────────
FT_SUB_H = 8   # Avenir Next Heavy

# Contraste peor caso medido sobre el montaje (analysis/estaciones-subtitulo.json):
#   ninguna posicion del metraje llega a 4,5:1 con tinta plana. El halo difuso
#   es lo que sube la legibilidad sin recurrir a caja negra.
ESTACIONES = {
    "alfombra": dict(cy=1690, modo="cocoa"),   # 88,0 % — A, B, D1, D2, E
    "tarima":   dict(cy=1786, modo="crema"),   # 93,0 % — solo C (suelo de madera oscuro)
}

SUBS2 = [
    (30,  "A",  "Hay dos cosas\nque despiertan a un gato",  "alfombra", 50, "abajo"),
    (70,  "B",  "Una es el ruido de la bolsa",              "alfombra", 56, "izquierda"),
    (100, "C",  "y la otra…",                               "tarima",   60, "abajo"),
    (150, "C",  "también es el ruido de la bolsa",          "tarima",   52, "derecha"),
    (200, "D1", "Snacks de pollo, sin cereales",            "alfombra", 54, "izquierda"),
    (262, "D2", "del tamaño exacto\npara una boca pequeña", "alfombra", 48, "derecha"),
]


def bloque_sub2(base, texto, estacion, alto, ancho=0.82):
    e = ESTACIONES[estacion]; modo = e["modo"]; cy = e["cy"]
    color = COCOA if modo == "cocoa" else CREMA
    halo = ((255, 246, 230), 0.58, 19) if modo == "cocoa" else ((22, 15, 8), 0.60, 20)
    som = ((46, 32, 20), 0.30, 10, 0, 4) if modo == "cocoa" else ((16, 11, 6), 0.50, 8, 0, 4)
    lineas = texto.split("\n")
    capas = [capa_texto(l, lambda s: ImageFont.truetype(FT_SUB, s, index=FT_SUB_H),
                        alto, color, tracking=0.010, ancho_max=W * ancho)[0] for l in lineas]
    lead = int(alto * 0.58)
    tot = sum(c.height for c in capas) + lead * (len(capas) - 1)
    y = cy - tot / 2
    top = y
    for c in capas:
        pegar(base, c, W / 2, y + c.height / 2, halo=halo, sombra=som)
        y += c.height + lead
    return top, y - lead


def muestra_sub2(i):
    f, pl, txt, est, alto, eje = SUBS2[i]
    im = fotograma(f).convert("RGBA")
    top, bot = bloque_sub2(im, txt, est, alto)
    return im, f, pl, est, eje, top, bot


# ───────── sistema v3: estacion anclada por el BORDE INFERIOR del bloque ─────────
# El ancla es el limite inferior real (descendentes incluidas), no el centro:
# asi un bloque de dos lineas no invade la tarima oscura.
ANCLA = {"alfombra": 1718, "tarima": 1810}   # 89,5 % y 94,3 %


def bloque_sub3(base, texto, estacion, alto, ancho=0.82, dibujar=True):
    modo = ESTACIONES[estacion]["modo"]
    color = COCOA if modo == "cocoa" else CREMA
    halo = ((255, 246, 230), 0.66, 20) if modo == "cocoa" else ((20, 14, 7), 0.62, 21)
    som = ((46, 32, 20), 0.32, 11, 0, 4) if modo == "cocoa" else ((16, 11, 6), 0.52, 9, 0, 4)
    lineas = texto.split("\n")
    capas = [capa_texto(l, lambda s: ImageFont.truetype(FT_SUB, s, index=FT_SUB_H),
                        alto, color, tracking=0.010, ancho_max=W * ancho)[0] for l in lineas]
    lead = int(alto * 0.58)
    tot = sum(c.height for c in capas) + lead * (len(capas) - 1)
    y = ANCLA[estacion] - tot
    top = y
    for c in capas:
        if dibujar:
            pegar(base, c, W / 2, y + c.height / 2, halo=halo, sombra=som)
        y += c.height + lead
    return top, ANCLA[estacion]


# ─────────────── bloque protagonista: coreografia elegida (idea A · TEJIDO) ───────────────
# «Papicat» 12,480-13,060 s (tl f299-f313) · «Snacks» 13,060-13,600 (f313-f326)
# coletilla 13,980-16,080 (f336-f386)

def banda_en(f):
    ks = sorted(BANDA); 
    if f <= ks[0]: return BANDA[ks[0]]
    if f >= ks[-1]: return BANDA[ks[-1]]
    a = max(k for k in ks if k <= f); b = min(k for k in ks if k >= f)
    if a == b: return BANDA[a]
    t = (f - a) / (b - a)
    return {k: BANDA[a][k] + (BANDA[b][k] - BANDA[a][k]) * t for k in BANDA[a]}


def marca_tejida_f(base, f, lineas, ancho_frac=0.80, rev=(1.0, 1.0)):
    """rev = (fraccion revelada de la linea 1, de la linea 2). Revelado de izquierda a derecha."""
    b = banda_en(f)
    bw = (b["x1"] - b["x0"]) * ancho_frac
    cx = (b["x0"] + b["x1"]) / 2; cy = (b["y0"] + b["y1"]) / 2
    capas = [capa_texto(t, FT_MARCA, a, CREMA, tracking=k, ancho_max=bw)[0] for t, a, k in lineas]
    lead = int(lineas[0][1] * 0.30)
    tot = sum(c.height for c in capas) + lead * (len(capas) - 1)
    y = cy - tot / 2
    for c, r in zip(capas, rev):
        if r <= 0.001:
            y += c.height + lead; continue
        if r < 1.0:
            m = c.split()[3]; a2 = np.array(m)
            corte = int(c.width * r)
            a2[:, corte:] = 0
            if corte > 6:      # borde blando de 6 px, como un punto a medio tejer
                for i in range(6):
                    if corte - 6 + i >= 0:
                        a2[:, corte - 6 + i] = (a2[:, corte - 6 + i] * (1 - i / 6)).astype(np.uint8)
            c = c.copy(); c.putalpha(Image.fromarray(a2))
        cur, _ = curvar(c, b["bow"], b["tilt"])
        tejer(base, cur, cx, y + c.height / 2)
        y += c.height + lead


LINEAS_MARCA = [("PapiCat", 60, 0.01), ("SNACKS", 30, 0.44)]


def bloque_marca(f):
    im = fotograma(f).convert("RGBA")
    r1 = min(1.0, max(0.0, (f - 299) / 14))       # «Papicat» f299 -> f313
    r2 = min(1.0, max(0.0, (f - 313) / 13))       # «Snacks»  f313 -> f326
    if r1 > 0:
        marca_tejida_f(im, f, LINEAS_MARCA, 0.80, (r1, r2))
    if f >= 333:
        op = min(1.0, (f - 333) / 8)
        cap = capa_texto("lo único capaz de hacer correr a tu gato",
                         lambda s: ImageFont.truetype(FT_SUB, s, index=FT_SUB_H),
                         42, COCOA, tracking=0.02, ancho_max=W * 0.80)[0]
        if op < 1: cap.putalpha(cap.split()[3].point(lambda v: int(v * op)))
        dy = int((1 - op) * 60)
        pegar(im, cap, W / 2, ANCLA["alfombra"] - cap.height / 2 + dy,
              halo=((255, 246, 230), 0.66, 20), sombra=((46, 32, 20), 0.32, 11, 0, 4))
    return im
