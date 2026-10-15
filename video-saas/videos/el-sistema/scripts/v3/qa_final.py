from pathlib import Path
import subprocess,json
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2];P=R/'output/v3/El-Sistema-V3.mp4';O=R/'analysis/v3'
times=[.8,3.4,4.66,5.8,7.1,9.07,10.5,12.20,14.40,15.92,17.9,19.78,21.72,23.64,25.30,26.6,27.12,28.95,30.62,31.84,33.9,36.32,37.9,40.28,42.10,43.2,44.1,45.66]
f=ImageFont.truetype('/Users/alejandrorubiocamarero/Library/Fonts/SFPRODISPLAYREGULAR.OTF',21);contact=Image.new('RGB',(1920,2100),'#09090B');d=ImageDraw.Draw(contact)
for i,t in enumerate(times):
 out=O/f'encoded-{i+1:02}.jpg';subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(P),'-frames:v','1','-q:v','2',str(out)],check=True)
 a=Image.open(out);a.thumbnail((480,270));x=i%4*480;y=i//4*300;contact.paste(a,(x,y));d.text((x+12,y+274),f'{i+1:02} · {t:.2f} s',font=f,fill='#ff641a')
contact.save(R/'output/v3/Contacto-V3.jpg',quality=93)
for name,t,dur,fps in [('entrada-final',9.35,1.2,10),('mapa-final',27.85,.72,16),('texto-final',4.0,1.3,9),('formatos-final',41.28,1.3,9)]:
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(P),'-t',str(dur),'-vf',f'fps={fps},scale=480:270,tile=4x3','-frames:v','1',str(O/(name+'.jpg'))],check=True)
with (O/'encoded-loudness.log').open('w') as q:subprocess.run(['ffmpeg','-v','info','-i',str(P),'-af','loudnorm=I=-15:TP=-1.5:LRA=8:print_format=json','-f','null','-'],stderr=q,check=True)
with (O/'black-scan.log').open('w') as q:subprocess.run(['ffmpeg','-v','info','-i',str(P),'-vf','blackdetect=d=0.12:pix_th=0.06:pic_th=0.98','-an','-f','null','-'],stderr=q,check=True)
print('FINAL QA ready')
