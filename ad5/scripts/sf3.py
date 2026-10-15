"""AD5 v2 · estilo BRAUDLABS: dos niveles tipográficos, bloque de selección, cifras en anillo."""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OPT='/System/Library/Fonts/Supplemental/Optima.ttc'
def op(sz,b=True): return ImageFont.truetype(OPT,sz,index=1 if b else 0)
NAVY=(12,38,84); AZUL=(45,108,214); CIELO=(169,199,232); CREMA=(244,248,255)

def frame(p,t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',p,'-frames:v','1',
        '-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return Image.fromarray(np.frombuffer(raw,np.uint8)[:1080*1920*3].reshape(1920,1080,3)).convert('RGBA')

def sombra(base,fn,blur=18,alpha=0.55,off=(0,8)):
    sh=Image.new('RGBA',base.size,(0,0,0,0)); fn(ImageDraw.Draw(sh))
    sh=sh.filter(ImageFilter.GaussianBlur(blur))
    a=sh.split()[3].point(lambda v:int(v*alpha))
    t=Image.new('RGBA',base.size,NAVY+(0,)); t.putalpha(a); base.alpha_composite(t,off)

def sub(base,txt,y,sz=52):
    """Subtítulo corrido: TODAS las palabras. Crema, contorno navy, sombra. Sin caja."""
    ov=Image.new('RGBA',base.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    sombra(base, lambda dd: dd.text((540,y),txt,font=op(sz),fill=NAVY+(255,),anchor='mm',
                                    stroke_width=9,stroke_fill=NAVY+(255,)))
    d.text((540,y),txt,font=op(sz),fill=CREMA+(255,),anchor='mm',stroke_width=4,stroke_fill=NAVY+(255,))
    base.alpha_composite(ov)

def enfasis(base,txt,y,sz=132,rev=1.0):
    """Palabra clave con bloque de selección azul, como el magenta de T1."""
    ov=Image.new('RGBA',base.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    f=op(sz); bb=d.textbbox((540,y),txt,font=f,anchor='mm')
    x0,y0,x1,y1=bb[0]-30,bb[1]-16,bb[2]+30,bb[3]+20
    sombra(base, lambda dd: dd.rectangle([x0,y0,x1,y1],fill=NAVY+(255,)), blur=22, alpha=0.5, off=(0,10))
    xr=x0+(x1-x0)*rev                                  # el bloque barre al revelar
    d.rectangle([x0,y0,xr,y1], fill=AZUL+(240,))
    tm=Image.new('RGBA',base.size,(0,0,0,0)); ImageDraw.Draw(tm).text((540,y),txt,font=f,fill=CREMA+(255,),anchor='mm')
    ov.alpha_composite(tm)
    base.alpha_composite(ov)

def anillo(base,cx,cy,r,txt,sz=112,lleno=True):
    """Cifra en anillo, como el 50 de A2."""
    ov=Image.new('RGBA',base.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    sombra(base, lambda dd: dd.ellipse([cx-r,cy-r,cx+r,cy+r],fill=NAVY+(255,)), blur=20, alpha=0.45, off=(0,9))
    if lleno: d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=AZUL+(242,))
    d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=CIELO+(255,), width=4)
    d.text((cx,cy),txt,font=op(sz),fill=CREMA+(255,),anchor='mm')
    base.alpha_composite(ov)

def linea(base,pts,w=9):
    ov=Image.new('RGBA',base.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    sombra(base, lambda dd: dd.line(pts,fill=NAVY+(255,),width=w+5,joint='curve'), blur=10, alpha=0.5, off=(0,6))
    d.line(pts,fill=AZUL+(255,),width=w,joint='curve')
    base.alpha_composite(ov)

out=[]
# 1 · «A los 50» — la cifra en anillo
b=frame('assets/src-04.mp4',0.5); sub(b,'A los',1330,54); anillo(b,540,1520,118,'50')
out.append(('1 · A los [50]',b))
# 2 · la línea, con el subtítulo entero
b=frame('assets/src-04.mp4',3.3); linea(b,[(688,838),(734,813),(783,800),(830,801)])
sub(b,'el maquillaje ya no tapaba mis líneas',1490,50)
out.append(('2 · subtítulo íntegro',b))
# 3 · énfasis con bloque de selección
b=frame('assets/src-04.mp4',5.0); linea(b,[(688,838),(734,813),(783,800),(830,801)])
enfasis(b,'SE METÍA DENTRO',1500,92)
out.append(('3 · bloque de selección',b))
# 4 · correctores
b=frame('assets/src-02.mp4',1.5); enfasis(b,'CORRECTORES',1450,96)
out.append(('4 · correctores',b))
# 5 · hialurónico, dos niveles
b=frame('assets/src-03.mp4',3.0); sub(b,'con ácido',1330,50); enfasis(b,'HIALURÓNICO',1500,90)
out.append(('5 · dos niveles',b))
# 6 · jugosa
b=frame('assets/src-03.mp4',6.2); sub(b,'la piel se ve',1330,50); enfasis(b,'JUGOSA',1500,120)
out.append(('6 · jugosa',b))
# 7 · CTA
b=frame('assets/src-01.mp4',3.6); sub(b,'pruébalo',1300,54); anillo(b,540,1500,116,'1 mes',58)
out.append(('7 · CTA',b))

W,H=286,508
sh=Image.new('RGB',(len(out)*(W+8)+8,H+28),(14,16,20)); dd=ImageDraw.Draw(sh)
FU=ImageFont.truetype('/System/Library/Fonts/Avenir Next.ttc',18,index=5)
for i,(n,im) in enumerate(out):
    sh.paste(im.convert('RGB').resize((W,H)),(8+i*(W+8),24)); dd.text((10+i*(W+8),4),n,font=FU,fill=(150,205,255))
sh.save('analysis/v2.png'); print(sh.size)
