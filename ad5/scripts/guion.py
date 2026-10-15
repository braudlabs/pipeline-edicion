"""Guion de AD5. Fragmentos cortos y grandes, como en la creatina (84-96 px).
Reglas que se comprueban solas abajo: no falta ni sobra una palabra, nada
aparece dos veces a la vez, y nada se sale de cuadro."""
import unicodedata, re
from PIL import ImageFont

OPT='/System/Library/Fonts/Supplemental/Optima.ttc'
SUB, BIG = 88, None          # el tamaño de énfasis va por fragmento
ANCHO_UTIL = 940             # 70 px de aire a cada lado

# (clip, inicio_s, fin_s, nivel, texto, tamaño)   nivel: sub | big | ring
GUION = [
 ('04', 0.00, 1.74, 'sub',  'A los',                 88),
 ('04', 0.42, 1.74, 'ring', '50',                   104),
 ('04', 1.74, 2.34, 'sub',  'el maquillaje',          88),
 ('04', 2.38, 3.02, 'sub',  'ya no tapaba',           88),
 ('04', 3.06, 4.14, 'sub',  'mis líneas',             88),
 ('04', 4.20, 5.80, 'big',  'se metía dentro',       110),
 ('04', 5.88, 6.85, 'sub',  'y las marcaba más',      84),

 ('02', 0.00, 0.78, 'sub',  'dejé de gastar',         88),
 ('02', 0.82, 1.18, 'sub',  'dinero en',              88),
 ('02', 1.22, 1.90, 'big',  'correctores',           120),
 ('02', 1.94, 3.90, 'sub',  'el día que',             88),
 ('02', 3.94, 5.00, 'sub',  'entendí esto',           88),

 ('03', 0.00, 0.78, 'sub',  'ahora uso',              88),
 ('03', 0.82, 1.46, 'sub',  'este serum',             88),
 ('03', 1.50, 2.34, 'sub',  'con color',              88),
 ('03', 2.40, 2.98, 'sub',  'con ácido',              88),
 ('03', 3.04, 4.00, 'big',  'hialurónico',           118),
 ('03', 4.04, 4.78, 'big',  'no se cuartea',         112),
 ('03', 4.82, 6.14, 'sub',  'y la piel se ve',        84),
 ('03', 6.18, 6.85, 'big',  'jugosa',                140),

 ('01', 0.00, 0.62, 'sub',  'te dejo',                88),
 ('01', 0.66, 1.10, 'sub',  'el enlace',              88),
 ('01', 1.14, 2.80, 'sub',  'aquí abajo',             88),
 ('01', 2.90, 4.10, 'big',  'pruébalo un mes',       106),
 ('01', 4.15, 5.00, 'sub',  'y me cuentas',           88),
]

DICHO = {
 '04': 'a los 50 el maquillaje ya no tapaba mis líneas se metía dentro y las marcaba más',
 '02': 'dejé de gastar dinero en correctores el día que entendí esto',
 '03': 'ahora uso este serum con color con ácido hialurónico no se cuartea y la piel se ve jugosa',
 '01': 'te dejo el enlace aquí abajo pruébalo un mes y me cuentas',
}

def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9ñ ]', ' ', s).split()

def ancho(txt, sz):
    f = ImageFont.truetype(OPT, sz, index=1)
    return f.getbbox(txt.upper() if txt.isupper() else txt)[2]

def comprobar(verboso=True):
    fallo = False
    for clip, dicho in DICHO.items():
        frs = [(a,b,n,t,s) for c,a,b,n,t,s in GUION if c == clip]
        en_pantalla = [w for _,_,_,t,_ in frs for w in norm(t)]
        quiere = norm(dicho)
        faltan = [w for w in quiere if w not in en_pantalla]
        sobran = [w for w in en_pantalla if w not in quiere]
        solapes = []
        for i in range(len(frs)):
            for j in range(i+1, len(frs)):
                a1,b1,n1,t1,_ = frs[i]; a2,b2,n2,t2,_ = frs[j]
                if a2 < b1 and a1 < b2 and set(norm(t1)) & set(norm(t2)):
                    solapes.append((t1,t2))
        anchos = [(t,s,round(ancho(t,s))) for _,_,n,t,s in frs
                  if n != 'ring' and ancho(t,s) > ANCHO_UTIL]
        ok = not (faltan or sobran or solapes or anchos)
        fallo |= not ok
        if verboso:
            print(f"  {clip}  {'OK ' if ok else 'FALLA'}  {len(quiere)} dichas / {len(en_pantalla)} en pantalla")
            if faltan:  print(f"        FALTAN: {faltan}")
            if sobran:  print(f"        SOBRAN: {sobran}")
            if solapes: print(f"        DUPLICADO simultáneo: {solapes}")
            if anchos:  print(f"        SE SALE DE CUADRO: {anchos}")
    return not fallo

if __name__ == '__main__':
    print('cobertura y encaje del guion:')
    ok = comprobar()
    mx = max((ancho(t,s), t, s) for _,_,_,n,t,s in GUION if n != 'ring')
    print(f"\n  más ancho: {mx[1]!r} a {mx[2]} px = {round(mx[0])} px (tope {ANCHO_UTIL})")
    print('>>>', 'guion válido' if ok else 'HAY FALLOS')
