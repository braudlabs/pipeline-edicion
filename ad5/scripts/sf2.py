"""Idea A refinada: la gotita atraviesa los cuatro clips. Estados clave."""
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FUT='/System/Library/Fonts/Supplemental/Futura.ttc'
def fut(sz,i=2): return ImageFont.truetype(FUT,sz,index=i)
NAVY=(14,42,92); AZUL=(46,111,217); CIELO=(169,199,232); CREMA=(242,247,255)

def frame(p,t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',p,'-frames:v','1',
        '-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return Image.fromarray(np.frombuffer(raw,np.uint8)[:1080*1920*3].reshape(1920,1080,3)).convert('RGBA')

def sombra(base, fn, blur=16, alpha=120, off=(0,7)):
    sh=Image.new('RGBA',base.size,(0,0,0,0)); fn(ImageDraw.Draw(sh))
    sh=sh.filter(ImageFilter.GaussianBlur(blur))
    a=sh.split()[3].point(lambda v:int(v*alpha/255))
    t=Image.new('RGBA',base.size,NAVY+(0,)); t.putalpha(a); base.alpha_composite(t,off)

def gota(d,cx,cy,r,fill=AZUL,squash=1.0,alpha=255,brillo=True):
    rx,ry=r*squash,r/squash
    d.ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=fill+(alpha,))
    d.polygon([(cx-rx*0.60,cy-ry*0.74),(cx,cy-ry*2.0),(cx+rx*0.60,cy-ry*0.74)],fill=fill+(alpha,))
    if brillo:
        d.ellipse([cx-rx*0.52,cy-ry*0.60,cx-rx*0.10,cy-ry*0.14],fill=CREMA+(int(alpha*0.85),))

def sub(base,txt,y=1500,sz=62):
    """Subtítulo: crema, contorno navy fino, sombra suave. Sin caja."""
    ov=Image.new('RGBA',base.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
    sombra(base, lambda dd: dd.text((540,y),txt,font=fut(sz),fill=NAVY+(255,),anchor='mm',
                                    stroke_width=9,stroke_fill=NAVY+(255,)), blur=20, alpha=95, off=(0,8))
    d.text((540,y),txt,font=fut(sz),fill=CREMA+(255,),anchor='mm',stroke_width=5,stroke_fill=NAVY+(255,))
    base.alpha_composite(ov)

out=[]

# 1 · PROBLEMA (clip 04) — la línea se dibuja siguiendo su dedo. Sin gota todavía.
b=frame('assets/src-04.mp4',5.0); ov=Image.new('RGBA',b.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
pts=[(688,838),(734,813),(783,800),(830,801)]
sombra(b, lambda dd: dd.line(pts,fill=NAVY+(255,),width=14,joint='curve'), blur=12, alpha=130)
d.line(pts,fill=NAVY+(255,),width=9,joint='curve')
d.ellipse([825,795,837,807],fill=NAVY+(255,))
b.alpha_composite(ov); sub(b,'se metía dentro',1480)
out.append(('1 · la línea, trazada con su dedo',b))

# 2 · GIRO (clip 02) — la gota irrumpe, pasada de frenada, y empuja al corrector.
b=frame('assets/src-02.mp4',1.5); ov=Image.new('RGBA',b.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
# estela de la entrada
for i,(sx,sy,sr,al) in enumerate(((150,560,22,60),(212,548,30,95),(280,540,38,140))):
    gota(d,sx,sy,sr,AZUL,squash=1.35,alpha=al,brillo=False)
gota(d,362,536,62,AZUL,squash=1.18)
# ojos tontorrones
d.ellipse([336,516,356,540],fill=CREMA+(255,)); d.ellipse([372,516,392,540],fill=CREMA+(255,))
d.ellipse([343,527,353,539],fill=NAVY+(255,)); d.ellipse([379,527,389,539],fill=NAVY+(255,))
b.alpha_composite(ov); sub(b,'dejé de gastar',1760)
out.append(('2 · la gota irrumpe',b))

# 3 · SOLUCIÓN (clip 03) — anillos Braud y la línea del principio se alisa.
b=frame('assets/src-03.mp4',6.2); ov=Image.new('RGBA',b.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
cx,cy=250,760
for i,rr in enumerate((188,146,104)):
    d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],outline=CIELO+(210-i*45,),width=3)
gota(d,cx,cy,64,AZUL)
sombra(b, lambda dd: dd.text((cx,cy+250),'HIALURÓNICO',font=fut(38,3),fill=NAVY+(255,),anchor='mm',
                             stroke_width=7,stroke_fill=NAVY+(255,)), blur=16, alpha=110)
d.text((cx,cy+250),'HIALURÓNICO',font=fut(38,3),fill=CREMA+(255,),anchor='mm',stroke_width=4,stroke_fill=NAVY+(255,))
b.alpha_composite(ov); sub(b,'la piel se ve jugosa',1480,58)
out.append(('3 · rellena y se alisa',b))

# 4 · CTA (clip 01) — la gota se tira por donde ella señala.
b=frame('assets/src-01.mp4',4.3); ov=Image.new('RGBA',b.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
for i,(sy,sr,al) in enumerate(((1180,26,70),(1268,34,110),(1362,44,165))):
    gota(d,404,sy,sr,AZUL,squash=0.80,alpha=al,brillo=False)
gota(d,404,1470,58,AZUL,squash=0.88)
b.alpha_composite(ov); sub(b,'pruébalo un mes',1740,58)
out.append(('4 · se tira al enlace',b))

W,H=300,533
sh=Image.new('RGB',(len(out)*(W+10)+10,H+40),(15,17,22)); dd=ImageDraw.Draw(sh)
for i,(n,im) in enumerate(out):
    sh.paste(im.convert('RGB').resize((W,H)),(10+i*(W+10),32))
    dd.text((12+i*(W+10),9),n,font=fut(19,0),fill=(150,200,255))
sh.save('analysis/idea-a.png'); print('ok',sh.size)
