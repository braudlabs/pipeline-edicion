from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1];A=R/'assets';O=R/'analysis/styleframes';O.mkdir(exist_ok=True)
BG='#0A0A0B';INK='#EDEDEA';S='#98958D';Y='#F2B800'
def font(n,b=False):return ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',n,index=1 if b else 0)
def base(title):
 im=Image.new('RGB',(1920,1080),BG);d=ImageDraw.Draw(im);d.text((85,70),'EL',font=font(23,True),fill=INK);d.text((128,70),'SISTEMA',font=font(23,True),fill=Y);d.text((85,950),title,font=font(20),fill=S);return im,d
def panel(im,d,x,y,w,h,label,img=None):
 d.rounded_rectangle((x,y,x+w,y+h),18,fill='#131415',outline='#363635',width=1);d.text((x+24,y+22),label,font=font(24,True),fill=INK)
 if img:
  a=Image.open(A/img);a.thumbnail((w-30,h-75));im.paste(a,(int(x+(w-a.width)/2),y+65))
def line(d,pts,col='#635525',width=2):d.line(pts,fill=col,width=width)
im,d=base('A · Recorrido continuo por estaciones · Dirección elegida')
for i,(x,y,w,h,label,img) in enumerate([(95,225,435,250,'01  La idea',None),(605,180,580,300,'02  El guion',None),(1260,180,310,410,'03  El ancla','denim-01.jpg'),(1650,240,185,310,'04  Modelo',None),(645,610,815,260,'05  El mapa',None),(95,650,430,220,'06  Revisión',None)]):
 panel(im,d,x,y,w,h,label,img)
 if i==0:
  for j,tx in enumerate(['Un anuncio de esta chaqueta.','Modelo, sarga y detalles.','Confirmar antes de generar.']):d.text((120,295+j*45),tx,font=font(24),fill=INK if j<2 else Y)
 if i==1:
  for j in range(5):d.rounded_rectangle((635,242+j*38,1150,266+j*38),5,fill='#272624');d.text((645,242+j*38),f'{j+1:02}',font=font(18),fill=Y)
 if i==3:
  for j,tx in enumerate(['Soul','Seedance','Kling']):d.text((1675,325+j*62),tx,font=font(21),fill=Y if j==1 else S)
 if i==4:
  for j in range(5):
   a=Image.open(A/f'denim-{j+1:02d}.jpg');a.thumbnail((115,172));im.paste(a,(675+j*151,673))
 if i==5:d.text((120,735),'Dicción  →  corregir',font=font(25),fill=S);d.text((120,790),'Toma aprobada  ↗',font=font(25),fill=Y)
line(d,[(530,350),(605,350)]);line(d,[(1185,350),(1260,350)]);line(d,[(1570,450),(1650,450)]);line(d,[(1740,550),(1740,740),(1460,740)]);line(d,[(645,740),(525,740)])
im.save(O/'A-recorrido.png')
im,d=base('B · Profundidad por capas · Alternativa de estudio')
for j in range(4,-1,-1):panel(im,d,330+j*150,220-j*22,1000,520,f'{j+1:02}  '+['Tu idea','Guion','Referencias','Generación','Resultado'][j], 'denim-01.jpg' if j==0 else None)
im.save(O/'B-capas.png')
im,d=base('C · Carril de producción · Alternativa de estudio')
for j in range(5):panel(im,d,80+j*363,245,320,550,['Guion','Ancla','Modelo','Revisión','Final'][j],f'denim-{j+1:02d}.jpg');line(d,[(400+j*363,530),(443+j*363,530)],Y)
im.save(O/'C-carril.png')
