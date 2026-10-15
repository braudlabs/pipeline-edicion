from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw,ImageFont
from retime import T
R=Path(__file__).resolve().parents[1];P=R/'output/El-Sistema-V2.mp4';F=R/'analysis/encoded-frames';F.mkdir(exist_ok=True)
original=[1.6,5.8,10.8,15.5,19.5,21.6,24.5,29.1,33.4,35.7,38.9,42.8,47.7,50.3,52.8,55.5,59.0,60.7,62.7,64.8,67]
labels=['Apertura','Proceso','Interfaz','Inmersión','Confirmación','Guion','Referencias','Modelos','Mapa','Animación','Revisión','Resultado','Montaje','Subtítulos','Entrega','Versiones','Gancho','Formatos','Familia','Cierre','Logo']
im=Image.new('RGB',(1920,1824),'#111212');dr=ImageDraw.Draw(im);font=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',19);entries=[]
for i,(t,label) in enumerate(zip(original,labels)):
 t=T(t);f=F/f'P{i+1:02}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(P),'-frames:v','1',str(f)],check=True)
 a=Image.open(f);a.thumbnail((480,270));x=i%4*480;y=i//4*304;im.paste(a,(x,y));dr.text((x+12,y+277),f'P{i+1:02} · {t:05.2f}s · {label}',font=font,fill='#ededea');entries.append({'id':f'P{i+1:02}','time':t,'label':label})
im.save(R/'output/Contacto-V2.jpg',quality=92);(R/'output/Indice-Planos-V2.json').write_text(json.dumps(entries,indent=2,ensure_ascii=False))
# Transition strips from the encoded video, not only cached AE frames.
for name,t in [('inmersion',14.3),('mapa',35.34),('editor',45.3),('variantes',53.6)]:
 sh=Image.new('RGB',(1440,936),'#111');sd=ImageDraw.Draw(sh)
 for j in range(12):
  sec=T(t)-.4+j*.09;f=F/f'{name}-{j}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(sec),'-i',str(P),'-frames:v','1','-vf','scale=360:203',str(f)],check=True);sh.paste(Image.open(f),(j%4*360,j//4*312));sd.text((j%4*360+10,j//4*312+209),f'{sec:.3f}s',font=font,fill='white')
 sh.save(R/'analysis'/f'encoded-{name}.jpg')
print('Encoded contact and transition strips ready')
