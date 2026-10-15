from pathlib import Path
import json,math
from PIL import Image,ImageFont
R=Path(__file__).resolve().parents[1];F=30;D=69
BG='#0A0A0B';P='#141516';LINE='#303131';INK='#EDEDEA';SOFT='#98958D';Y='#F2B800';GREEN='#7ddb9a'
S={'fps':F,'duration':D,'master':'EL SISTEMA - PELICULA V1','comps':{}}
def comp(name,w=1920,h=1080):
 c={'name':name,'width':w,'height':h,'duration':D,'layers':[]};S['comps'][name]=c;return c
def node(c,t,name,x=0,y=0,a=0,b=D,**kw):
 name=name if not any(z['name']==name for z in c['layers']) else name+' '+str(len(c['layers']))
 n={'type':t,'name':name,'pos':[x,y],'from':a,'to':b,'anim':{},**kw};c['layers'].append(n);return n
def tx(c,text,x,y,size=48,a=0,b=D,col=INK,font='HelveticaNeue',align='left',track=-20,name=None):return node(c,'text',name or text,x,y,a,b,text=text,size=size,color=col,font=font,align=align,track=track)
def rect(c,name,x,y,w,h,col=P,a=0,b=D,stroke=None,round=18,opacity=1):return node(c,'rect',name,x,y,a,b,w=w,h=h,color=col,stroke=stroke,round=round,opacity=opacity)
def path(c,name,pts,col=LINE,width=2,a=0,b=D,closed=False,fill=None):return node(c,'path',name,0,0,a,b,points=pts,stroke=col,strokeWidth=width,closed=closed,color=fill)
def pic(c,name,asset,x,y,w,a=0,b=D):
 p=R/'assets'/asset
 if p.suffix in ['.png','.jpg']:ww,hh=Image.open(p).size
 else:ww,hh=1080,1920
 return node(c,'media',name,x,y,a,b,asset=asset,srcW=ww,srcH=hh,scale=[w/ww,w/ww],anchor=[ww/2,hh/2])
def nested(c,name,source,x=0,y=0,a=0,b=D,scale=1,anchor=None):return node(c,'comp',name,x,y,a,b,asset=source,scale=[scale,scale],anchor=anchor or [0,0])
def anim(n,p,t,v,ease='out'):n['anim'][p]={'times':t,'values':v,'ease':ease};return n
def reveal(n,t,dx=0,dy=38,d=.48):
 x,y=n['pos'];anim(n,'pos',[t,t+d],[[x+dx,y+dy],[x,y]]);anim(n,'opacity',[t,t+.25],[0,1]);return n
def bg(c):rect(c,'Fondo',0,0,c['width'],c['height'],BG,round=0)
def line(c,name,pts,a=0,b=D,col=LINE,width=2):return path(c,name,pts,col,width,a,b)
def logo(c,cx,cy,size=50,a=0,b=D):
 # Positions measured using the installed product font; native AE uses the same family.
 f=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',int(size),index=1)
 t1='EL';t2='SISTEMA';gap=size*.40;w1=f.getlength(t1)+size*.24;w2=f.getlength(t2)+size*.24*6;left=cx-(w1+w2+gap)/2
 tx(c,t1,left,cy,size,a,b,font='HelveticaNeue-Bold',track=240);tx(c,t2,left+w1+gap,cy,size,a,b,col=Y,font='HelveticaNeue-Bold',track=240)
def cursor(c,name,positions,times,a,b):
 n=path(c,name,[[0,0],[0,87],[21,67],[38,103],[53,96],[36,61],[66,59],[0,0]],'#060607',3,a,b,True,INK);n['pos']=positions[0];anim(n,'pos',times,positions,'flow');return n

# 01: real dashboard hierarchy, reconstructed as native editable layers from index.html.
home=comp('01A - Inicio real');bg(home)
rect(home,'Marco de la ventana',110,125,1700,860,'#101112',stroke=LINE,round=26)
line(home,'Cabecera',[[110,215],[1810,215]],col='#272829',width=1)
logo(home,318,181,25)
for j,t in enumerate(['Mis piezas','Créditos','Conexiones','Mejorar']):tx(home,t,1160+j*148,179,22,col=SOFT)
tx(home,'¡Buenas,',960-258,394,76,font='HelveticaNeue-UltraLight')
tx(home,'Alejandro!',960+14,394,76,font='HelveticaNeue-Bold')
tx(home,'¿Qué tienes en mente hacer hoy?',960,446,29,col=SOFT,align='center')
rect(home,'Campo real de la idea',420,512,1080,105,'#18191A',stroke='#3B3933',round=25)
tx(home,'Cuéntamelo con tus palabras…',455,578,29,0,11.66,col=SOFT)
rect(home,'Botón enviar',1403,532,76,66,Y,round=18)
line(home,'Flecha enviar',[[1428,565],[1454,565],[1444,555],[1454,565],[1444,575]],col='#141200',width=4)
labels=['Crear una pieza','Espiar a la competencia','Mis piezas','Campañas de Meta']
subs=[['Formatos guiados — o carta blanca','y lo montamos a tu manera.'],['Dime una marca y te traigo','su anuncio que mejor funciona.'],['El camino de cada creativo:','avatar, rondas, edición y final.'],['Conecta tu cuenta y gestionamos','campañas desde aquí.']]
for j,(label,ls) in enumerate(zip(labels,subs)):
 x=194+j*389;rect(home,'Acceso '+str(j),x,705,364,158,P,stroke=LINE,round=23)
 tx(home,label,x+28,750,23,font='HelveticaNeue-Bold',track=0)
 for k,s in enumerate(ls):tx(home,s,x+28,795+k*28,19,col=SOFT,track=0)
phrase='Quiero un anuncio de esta chaqueta: modelo y detalles del denim.'
f=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',26)
x=455
for i,ch in enumerate(phrase):
 if ch!=' ':tx(home,ch,x,578,26,11.66+i*.027,14.65,track=0,name=f'Teclado {i:02}')
 x+=f.getlength(ch)
cursor(home,'Cursor - escribir y enviar',[[1690,1190],[555,570],[555,570],[1555,676],[1440,560],[1440,560],[1470,1200]],[10.95,11.58,12.08,13.3,14.03,14.13,14.55],10.95,14.65)

intro=comp('01 - Superficie');bg(intro)
tx(intro,'Lo imaginas de una forma.',960,176,60,0,3.78,align='center',font='HelveticaNeue-Light')
for j in range(3):
 x=550+j*410;n=pic(intro,'Personaje variable '+str(j),f'chef-{j+1}.jpg',x,567,338,.10+j*.56,3.90)
 anim(n,'pos',[.10+j*.56,.65+j*.56,3.45,3.90],[[x+160,567],[x,567],[x,567],[x-260,567]],'flow')
 anim(n,'opacity',[.10+j*.56,.4+j*.56,3.45,3.90],[0,1,1,0])
 tx(intro,f'0{j+1}',x-160,931,22,.40+j*.56,3.8,col=SOFT,track=120)
reveal(tx(intro,'El problema',960,470,84,3.9,5.10,align='center',font='HelveticaNeue-Light'),3.90,dy=60)
reveal(tx(intro,'es el proceso.',960,603,172,5.02,7.84,align='center',font='HelveticaNeue-Bold',track=-50),5.02,dy=105,d=.65)
line(intro,'Subrayado proceso',[[426,650],[1486,650]],5.32,7.84,Y,3)
logo(intro,960,581,93,8.02,9.49)
n=nested(intro,'Interfaz real',home['name'],960,540,9.49,14.65,1,[960,540])
anim(n,'scale',[9.49,10.1,13.9,14.65],[[1.1,1.1],[1,1],[1,1],[6.0,6.0]],'flow')
anim(n,'pos',[9.49,10.1,13.9,14.65],[[1100,540],[960,540],[960,540],[960,440]],'flow')
exec((R/'scripts/interior.py').read_text())
# Master, filled by further native scenes as the edit proceeds.
master=comp(S['master']);bg(master)
nested(master,'01 - Superficie',intro['name'],0,0,0,14.65)
n=nested(master,'02 - Recorrido interior',inside['name'],0,0,14.30,42.08);anim(n,'opacity',[14.30,14.65,41.64,42.08],[0,1,1,0],'flow')
node(master,'audio','Mezcla sonora',0,0,0,D,asset='Mezcla-Final.wav')
(R/'src/design.json').write_text(json.dumps(S,indent=2,ensure_ascii=False))
print('Design:',sum(len(c['layers']) for c in S['comps'].values()),'native layers')
