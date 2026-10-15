"""Tres ideas para el bloque protagonista, montadas sobre fotogramas reales."""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FUT = '/System/Library/Fonts/Supplemental/Futura.ttc'
def fut(sz, i=2): return ImageFont.truetype(FUT, sz, index=i)

NAVY=(14,42,92); AZUL=(46,111,217); CIELO=(169,199,232); CREMA=(242,247,255)

def frame(path, t):
    raw = subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',path,'-frames:v','1',
        '-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return Image.fromarray(np.frombuffer(raw,np.uint8)[:1080*1920*3].reshape(1920,1080,3))

def sombra(base, draw_fn, blur=18, alpha=110, off=(0,6)):
    """Sombra discreta: el usuario rechaza cajas, no sombras."""
    sh = Image.new('RGBA', base.size, (0,0,0,0))
    draw_fn(ImageDraw.Draw(sh))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    a = sh.split()[3].point(lambda v: int(v*alpha/255))
    tint = Image.new('RGBA', base.size, NAVY+(0,)); tint.putalpha(a)
    base.alpha_composite(tint, off)

def gota(d, cx, cy, r, fill, squash=1.0, alpha=255):
    """Gota Braud: círculo con punta. squash>1 = achatada."""
    rx, ry = r*squash, r/squash
    d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=fill+(alpha,))
    d.polygon([(cx-rx*0.62, cy-ry*0.72), (cx, cy-ry*2.05), (cx+rx*0.62, cy-ry*0.72)], fill=fill+(alpha,))

def texto(d, xy, s, font, fill, anchor='mm', contorno=4, contorno_fill=NAVY):
    d.text(xy, s, font=font, fill=fill+(255,), anchor=anchor,
           stroke_width=contorno, stroke_fill=contorno_fill+(255,))

# ---------------------------------------------------------------- IDEA A
def idea_a():
    """La gotita: se hunde en la línea (problema) y luego la rellena (solución)."""
    out=[]
    # A1 · el problema: la gota se hunde en la pata de gallo
    base = frame('assets/src-04.mp4', 5.0).convert('RGBA')
    ov = Image.new('RGBA', base.size, (0,0,0,0)); d=ImageDraw.Draw(ov)
    # la grieta que traza el dedo
    pts=[(690,835),(735,812),(782,800),(828,802)]
    sombra(base, lambda dd: dd.line(pts, fill=NAVY+(255,), width=13, joint='curve'))
    d.line(pts, fill=NAVY+(255,), width=9, joint='curve')
    for px,py in pts[1:]:
        d.ellipse([px-5,py-5,px+5,py+5], fill=NAVY+(255,))
    # la gota cayendo dentro, achatada por el impacto
    gota(d, 762, 742, 34, AZUL, squash=1.28)
    d.ellipse([748,726,760,740], fill=CREMA+(220,))          # brillo tontorrón
    # etiqueta
    texto(d, (762, 655), 'se cuela', fut(46), CREMA, contorno=5)
    base.alpha_composite(ov); out.append(('A1 · se cuela en la línea', base))

    # A2 · la solución: la gota rellena y la línea se alisa
    base = frame('assets/src-03.mp4', 6.2).convert('RGBA')
    ov = Image.new('RGBA', base.size, (0,0,0,0)); d=ImageDraw.Draw(ov)
    cx, cy = 700, 880
    for i,rr in enumerate((150,112,74)):
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr], outline=CIELO+(190-i*40,), width=3)
    gota(d, cx, cy-6, 52, AZUL)
    d.ellipse([cx-28,cy-34,cx-10,cy-12], fill=CREMA+(230,))
    texto(d, (cx, cy+206), 'RELLENA', fut(60), CREMA, contorno=6)
    base.alpha_composite(ov); out.append(('A2 · rellena', base))
    return out

# ---------------------------------------------------------------- IDEA B
def idea_b():
    """El ticket huido: el gasto en correctores se desenrolla y sale corriendo."""
    out=[]
    base = frame('assets/src-02.mp4', 1.5).convert('RGBA')
    ov = Image.new('RGBA', base.size, (0,0,0,0)); d=ImageDraw.Draw(ov)
    x0,y0,w = 96, 1090, 330
    sombra(base, lambda dd: dd.rectangle([x0,y0,x0+w,y0+560], fill=NAVY+(255,)), blur=22, alpha=120)
    d.rectangle([x0,y0,x0+w,y0+560], fill=CREMA+(242,))
    # borde dentado de ticket
    for i in range(0, w, 22):
        d.polygon([(x0+i,y0+560),(x0+i+11,y0+584),(x0+i+22,y0+560)], fill=CREMA+(242,))
    texto(d, (x0+w/2, y0+52), 'CORRECTORES', fut(30,3), NAVY, contorno=0)
    d.line([x0+24,y0+84,x0+w-24,y0+84], fill=CIELO+(255,), width=2)
    for i,(mes,eur) in enumerate([('enero','24€'),('febrero','24€'),('marzo','31€'),('abril','24€'),('mayo','38€')]):
        yy=y0+120+i*62
        texto(d,(x0+26,yy),mes,fut(30,0),NAVY,anchor='lm',contorno=0)
        texto(d,(x0+w-26,yy),eur,fut(32,2),NAVY,anchor='rm',contorno=0)
    d.line([x0+24,y0+446,x0+w-24,y0+446], fill=NAVY+(255,), width=3)
    texto(d,(x0+w-26,y0+498),'141€',fut(54,2),AZUL,anchor='rm',contorno=0)
    base.alpha_composite(ov); out.append(('B · el ticket', base))
    return out

# ---------------------------------------------------------------- IDEA C
def idea_c():
    """El parche que no tapa: intenta cubrir la línea, resbala y se rinde."""
    out=[]
    base = frame('assets/src-04.mp4', 5.0).convert('RGBA')
    ov = Image.new('RGBA', base.size, (0,0,0,0)); d=ImageDraw.Draw(ov)
    pts=[(690,835),(735,812),(782,800),(828,802)]
    d.line(pts, fill=NAVY+(255,), width=9, joint='curve')
    # el parche, ladeado y a medio caer
    par = Image.new('RGBA', (360,150), (0,0,0,0)); pd=ImageDraw.Draw(par)
    pd.rounded_rectangle([0,0,360,150], 30, fill=CIELO+(238,), outline=NAVY+(255,), width=5)
    pd.text((180,75),'TAPAR', font=fut(52), fill=NAVY+(255,), anchor='mm')
    par = par.rotate(-17, expand=True, resample=Image.BICUBIC)
    ov.alpha_composite(par, (556, 858))
    # gotas de sudor, lo tontorrón
    for sx,sy,sr in ((905,846,15),(940,884,11),(886,906,9)):
        gota(d, sx, sy, sr, AZUL, alpha=225)
    texto(d, (540, 700), 'no se puede', fut(50), CREMA, contorno=5)
    base.alpha_composite(ov); out.append(('C · el parche', base))
    return out

alts = idea_a() + idea_b() + idea_c()
W,H=300,533
sheet=Image.new('RGB',(len(alts)*(W+10)+10, H+40),(15,17,22)); dd=ImageDraw.Draw(sheet)
for i,(name,im) in enumerate(alts):
    sheet.paste(im.convert('RGB').resize((W,H)), (10+i*(W+10), 32))
    dd.text((12+i*(W+10), 9), name, font=fut(20,0), fill=(150,200,255))
sheet.save('analysis/alternativas.png')
print('ok', sheet.size)
