from pathlib import Path
import json,math
from PIL import Image,ImageFont
R=Path(__file__).resolve().parents[1];F=30;D=69
BG='#0A0A0B';P='#141516';LINE='#303131';INK='#EDEDEA';SOFT='#98958D';Y='#F2B800';GREEN='#7ddb9a'
S={'fps':F,'duration':D,'master':'EL SISTEMA - PELICULA V2','comps':{}}
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

# Native light, depth and material. No generated bitmap backgrounds.
def blur(n,amount):n.setdefault('effects',[]).append({'match':'ADBE Gaussian Blur 2','props':[[[1],amount],[[3],False]]});return n
def glow(n,r=55,intensity=.65):n.setdefault('effects',[]).append({'match':'ADBE Glo2','props':[[[2],55],[[3],r],[[4],intensity]]});return n
def ellipse(c,name,x,y,w,h,col=None,stroke=None,sw=2,a=0,b=D,opacity=1):return node(c,'ellipse',name,x,y,a,b,w=w,h=h,color=col,stroke=stroke,strokeWidth=sw,opacity=opacity)
def glass(c,name,x,y,w,h,a=0,b=D,fill='#15171A',r=28):
 n=rect(c,name+' sombra',x+8,y+18,w,h,'#000000',a,b,round=r,opacity=.50);blur(n,38)
 rect(c,name+' canto',x,y+3,w,h,'#42413A',a,b,round=r)
 rect(c,name,x,y,w,h,fill,a,b,stroke='#52514A',round=r)
 line(c,name+' luz superior',[[x+32,y+1],[x+w-32,y+1]],a,b,'#727067',1)
def background(c):
 bg(c)
 n=ellipse(c,'Luz ámbar',1440,1110,1300,650,'#6B4209',opacity=.66);blur(n,300);anim(n,'pos',[0,25,45,69],[[1500,1120],[1260,1000],[1700,980],[1430,1160]],'flow')
 # Upper field intentionally clear; lower light carries the depth.
 for j,(sw,blurv,opac) in enumerate([(56,78,.14),(12,24,.32),(2,0,.3)]):
  n=ellipse(c,'Curva de luz '+str(j),-470,1060,2120,1820,None,Y,sw,opacity=opac)
  if blurv:blur(n,blurv)
  anim(n,'pos',[0,20,40,69],[[-560,1150],[-360,1300],[-450,1240],[-560,1150]],'flow')
def pose(n,t,positions,scales=None,rx=None,ry=None):
 n['threeD']=True;anim(n,'pos',t,positions,'flow')
 if scales:anim(n,'scale',t,[[v,v] for v in scales],'flow')
 if rx:anim(n,'rx',t,rx,'flow')
 if ry:anim(n,'ry',t,ry,'flow')
 return n
def floating(c,name,source,times,positions,scales,rx,ry,a,b):
 cc=S['comps'][source];n=nested(c,name,source,positions[0][0],positions[0][1],a,b,scales[0],[cc['width']/2,cc['height']/2]);pose(n,times,positions,scales,rx,ry);return n
def caption(c,s,x,y,size,a,b,col=INK):
 n=tx(c,s,x,y,size,a,b,col=col,align='center',font='HelveticaNeue-Medium',track=-35);return reveal(n,a,dy=55,d=.45)
def photo_card(name,im,w=420,h=746,label=None):
 c=comp(name,w+20,h+20);glass(c,name,0,0,w+20,h+20,r=22);pic(c,'Fotografía',im,(w+20)/2,(h+20)/2,w)
 if label:
  rect(c,'Chip',25,h-55,180,54,'#171717',round=15);tx(c,label,46,h-17,23)
 return c
# Product home, split into native components that can separate in depth.
prompt=comp('V2 · Campo de idea',1280,168)
glass(prompt,'Campo',2,2,1276,160,r=28,fill='#23241F')
tx(prompt,'Cuéntamelo con tus palabras…',42,97,35,0,11.66,col=SOFT)
phrase='Quiero un anuncio de una máquina que fabrica creativos.'
f=ImageFont.truetype('/System/Library/Fonts/HelveticaNeue.ttc',38);x=42
for i,ch in enumerate(phrase):
 if ch!=' ':tx(prompt,ch,x,98,38,11.66+i*.037,D,track=0,name=f'Escritura {i}')
 x+=f.getlength(ch)
rect(prompt,'Enviar',1156,31,97,97,Y,round=23)
line(prompt,'Flecha',[[1188,79],[1224,79],[1209,64],[1224,79],[1209,94]],col='#161305',width=5)
window=comp('V2 · Ventana real',1720,940);glass(window,'Ventana',10,10,1700,920,r=32,fill='#111315')
logo(window,239,83,28)
for j,s in enumerate(['Mis piezas','Créditos','Conexiones','Mejorar']):tx(window,s,1040+j*155,81,22,col=SOFT)
line(window,'División superior',[[10,116],[1710,116]],col='#33332D',width=1)
tx(window,'¡Buenas,',541,308,77,font='HelveticaNeue-Thin');tx(window,'Alejandro!',844,308,77,font='HelveticaNeue-Bold')
tx(window,'¿Qué tienes en mente hacer hoy?',860,375,29,col=SOFT,align='center')
# Blank center is occupied by the same input object used throughout the journey.
for j,(s,sub) in enumerate([('Crear una pieza','De la idea al anuncio.'),('Espiar a la competencia','Encuentra la referencia.'),('Mis piezas','Todo el proceso, ordenado.'),('Campañas de Meta','Conecta tu cuenta.')]):
 x=98+j*388;glass(window,'Acceso '+str(j),x,704,358,155,r=22,fill='#1B1D1C')
 tx(window,s,x+26,758,24,font='HelveticaNeue-Bold');tx(window,sub,x+26,808,22,col=SOFT)
# The entire camera shot has separated UI planes; input remains in front.
hero=comp('V2 · Cámara superficie');background(hero)
floating(hero,'Ventana en perspectiva',window['name'],[9.36,10.05,11.35,12.18,13.66,14.35],[[1120,610,360],[960,535,100],[960,535,100],[890,440,-480],[890,440,-480],[900,400,-1850]],[.89,.89,.89,.95,.95,1.05],[13,5,5,2,2,0],[-23,-8,-8,-4,-4,0],9.36,14.48)
floating(hero,'La misma idea en primer plano',prompt['name'],[9.36,10.05,11.35,12.18,13.66,14.48],[[1100,540,130],[960,541,15],[960,541,15],[928,548,-580],[928,548,-580],[960,540,-2220]],[.89,.89,.89,.96,.96,1.05],[13,5,5,2,2,0],[-23,-8,-8,-4,-4,0],9.36,14.48)
# Cursor appears only for the cause: writing then submitting.
cursor(hero,'Cursor enviar',[[1710,1220],[1604,538],[1604,538],[1810,1170]],[12.85,13.46,13.65,14.1],12.85,14.25)
# A quieter opening with a sculpted field; framed visuals move as objects, not slides.
intro=comp('V2 · Apertura');background(intro)
caption(intro,'Lo imaginas.',465,500,105,.0,2.82)
for j in [2,1,0]:
 card=photo_card('V2 · Variable '+str(j),f'chef-{j+1}.jpg',290,515)
 x=1040+j*265
 floating(intro,'Prueba '+str(j),card['name'],[.12+j*.12,.78+j*.12,2.58,3.15],[[x+400,615,200+j*100],[x,565,j*90],[x,565,j*90],[x-750,565,-350]],[.95,1,1,.6],[10,4,4,0],[-23,-10+j*7,-10+j*7,35],.12+j*.12,3.15)
caption(intro,'No sale igual.',960,549,119,2.92,4.82)
for j,s in enumerate(['Es el','proceso.']):
 n=caption(intro,s,960,430+j*180,85 if j==0 else 191,5.01+j*.05,7.85,col=SOFT if j==0 else INK)
# A precise route line turns the isolated word into a connected process.
pts=[[470,703],[1445,703]];n=line(intro,'Trazo conductor',pts,5.40,7.84,Y,3);anim(n,'scale',[5.40,6.0],[[.01,1],[1,1]],'flow')
logo(intro,960,568,98,8.02,9.40)
n=nested(intro,'Superficie',hero['name'],0,0,9.36,14.48)
# Native compositional modules of the inner system, used as 3D planes.
confirmation=comp('V2 · Confirmación',1200,670);glass(confirmation,'Respuesta',8,8,1184,654,r=32,fill='#151719')
tx(confirmation,'EL SISTEMA',56,72,23,col=Y,font='HelveticaNeue-Bold',track=140)
tx(confirmation,'Esta es la idea.',56,158,65,font='HelveticaNeue-Medium')
for j,s in enumerate(['Una máquina. Dieciséis planos.', 'Deivid y su máquina, en cada escena.']):tx(confirmation,s,56,259+j*59,43,col=INK)
for j in range(5):pic(confirmation,'Miniatura '+str(j),f'denim-{j+1:02}.jpg',101+j*123,420,85)
line(confirmation,'Separador coste',[[55,527],[1140,527]],col='#3D3D34',width=1)
tx(confirmation,'Coste previsto antes de generar',56,590,31,18.10,D,col=SOFT)
rect(confirmation,'Confirmar',853,549,287,77,Y,19.02,D,round=20)
tx(confirmation,'Confirmar',996,600,30,19.02,D,col='#171305',align='center',font='HelveticaNeue-Bold')
# Detailed script panel; five scenes fan from a common origin.
script=comp('V2 · Guion',790,890);glass(script,'Guion',6,6,778,878,r=30)
tx(script,'GUION',50,77,24,col=Y,track=130);tx(script,'Dieciséis escenas.',50,158,60,font='HelveticaNeue-Medium')
for j,s in enumerate(['La máquina le interrumpe','Diez anuncios más','La reacción de Deivid','Producción en cadena','Enterrado en creativos']):
 y=242+j*113;rect(script,'Renglón '+str(j),44,y,698,91,'#222521',stroke='#45483D',round=16)
 tx(script,f'0{j+1}',71,y+56,29,col=Y);tx(script,s,150,y+57,31);tx(script,['6 s','6 s','4 s','5 s','9 s'][j],703,y+57,24,col=SOFT,align='right')
identity=comp('V2 · Ancla',900,890);glass(identity,'Referencias',6,6,888,878,r=30)
tx(identity,'REFERENCIAS',46,76,24,col=Y,track=120);tx(identity,'Personaje y producto.',46,152,54,font='HelveticaNeue-Medium')
pic(identity,'Ancla modelo','denim-01.jpg',270,496,290);pic(identity,'Ancla tejido','denim-02.jpg',636,496,290)
for j,s in enumerate(['Personaje','Producto']):
 x=80+j*365;rect(identity,'Ancla bloqueada '+str(j),x,778,350,66,'#2D3022',round=16);tx(identity,s,x+30,822,28);line(identity,'Ancla check '+str(j),[[x+269,810],[x+281,822],[x+307,791]],col=GREEN,width=4)
models=comp('V2 · Modelos',840,810);glass(models,'Modelos',6,6,828,798,r=30)
tx(models,'GENERACIÓN',46,75,24,col=Y,track=120);tx(models,'Cada plano,',46,157,57,font='HelveticaNeue-Medium');tx(models,'su modelo.',46,222,57,font='HelveticaNeue-Medium')
for j,s in enumerate(['Imagen · identidad','Vídeo · movimiento']):
 y=278+j*106;rect(models,'Motor '+str(j),42,y,754,85,'#29291F',stroke='#716640',round=20);tx(models,s,77,y+56,35)
rect(models,'Prompt',42,527,754,221,'#101214',stroke='#34352E',round=20)
for j in range(7):
 for k in range(3):rect(models,f'Instrucción {j} {k}',72+k*230,561+j*23,100+((j+k)%4)*30,6,'#857A50' if (j+k)%3==0 else '#4A4D48',round=3)
# Compact workflow modules and full photographic moodboard share the same plane style.
mapc=comp('V2 · Moodboard',1640,850);glass(mapc,'Mapa',6,6,1628,838,r=30)
tx(mapc,'MOODBOARD',48,77,23,col=Y,track=130);tx(mapc,'16 planos. Una misma idea.',48,151,57,font='HelveticaNeue-Medium')
for j in range(16):
 x=134+(j%8)*195;y=327+(j//8)*286
 pic(mapc,'Frame '+str(j),f'maquina-{j+1:02}.jpg',x,y,143,0,35.34)
 n=pic(mapc,'Movimiento '+str(j),f'maquina-{j+1:02}.mp4',x,y,143,35.34,D);n['freezeTail']=True;n['sourceOffset']=1.5
 tx(mapc,f'{j+1:02}',x-70,y+142,18,col=SOFT,track=90)
rect(mapc,'Aprobar',580,766,480,76,Y,0,35.34,round=20);tx(mapc,'Aprobar y animar',820,816,31,0,35.34,col='#171305',align='center',font='HelveticaNeue-Bold')
rect(mapc,'Animando',580,766,480,76,'#273026',35.34,D,round=20);tx(mapc,'En movimiento',820,816,31,35.34,D,col=GREEN,align='center')
quality=comp('V2 · Calidad',1010,910);glass(quality,'Control',6,6,998,898,r=30)
tx(quality,'REVISIÓN',48,76,24,col=Y,track=130);tx(quality,'Solo lo que está a la altura.',48,151,49,font='HelveticaNeue-Medium')
pic(quality,'Revisada','denim-01.jpg',255,464,278);pic(quality,'Selección','denim-03.jpg',747,464,278)
line(quality,'Revisión ruta',[[416,460],[582,460]],col='#837545',width=3)
rect(quality,'Revisar',99,772,330,79,'#32291F',round=18);tx(quality,'Coherencia',264,823,28,col='#D9B883',align='center')
rect(quality,'Válida',584,772,330,79,'#253021',round=18);tx(quality,'Aprobado',749,823,30,col=GREEN,align='center')
# Inner shot: fly through the input, then open a layered production surface.
inner=comp('V2 · Inmersión');background(inner)
# Connective paths live behind the planes and carry the amber detail from the input.
for j in range(3):
 n=line(inner,'Ruta producción '+str(j),[[-500,250+j*240],[2420,250+j*240]],14.3,41.8,'#6C5C2A',1)
 anim(n,'opacity',[14.3,15.3,16.3],[0,.6,.28])
# The initial reveal is composed of modules assembling from depth (ref 2), then camera follows details (ref 3).
module_data=[(confirmation,960,540,0),(script,340,460,240),(identity,1630,445,280),(models,1535,835,160),(mapc,900,870,330),(quality,300,790,160)]
for j,(cc,x,y,z) in enumerate(module_data):
 # First broad state is 14.8–15.7; only the requested stage comes forward afterward.
 times=[14.28,15.08,15.55,16.22]
 positions=[[x, y+400, z+1000],[x,y,z],[x,y,z],[x,y,z+1800]]
 scales=[.34,.42,.42,.35]
 rxs=[25,10,10,10];rys=[-30,-12,-12,-12]
 if j==0:
  positions[-1]=[960,540,-140];scales[-1]=1.05;rxs[-1]=1;rys[-1]=-4
  times.extend([20.4,20.98]);positions.extend([[960,540,-140],[-730,490,850]]);scales.extend([1.05,.48]);rxs.extend([1,7]);rys.extend([-4,35])
 elif j==1:
  times.extend([20.4,21.03,22.22,22.9]);positions.extend([[420,650,1400],[960,550,-100],[960,550,-100],[-600,430,1000]]);scales.extend([.4,.97,.97,.48]);rxs.extend([8,1,1,12]);rys.extend([-15,-6,-6,27])
 elif j==2:
  times.extend([22.23,22.9,26.91,27.6]);positions.extend([[1560,480,1400],[960,548,-90],[960,548,-90],[-710,540,1000]]);scales.extend([.4,1.0,1.0,.48]);rxs.extend([8,1,1,12]);rys.extend([-15,-7,-7,35])
 elif j==3:
  times.extend([26.94,27.62,31.82,32.4]);positions.extend([[1540,740,1400],[960,535,-160],[960,535,-160],[-850,400,1000]]);scales.extend([.4,1.07,1.07,.48]);rxs.extend([8,2,2,12]);rys.extend([-15,-6,-6,35])
 elif j==4:
  times.extend([31.82,32.42,36.1,36.72]);positions.extend([[1530,720,1400],[960,533,-60],[960,533,-60],[-950,540,1300]]);scales.extend([.4,.93,.93,.48]);rxs.extend([8,2,2,12]);rys.extend([-15,-3,-3,35])
 else:
  times.extend([36.1,36.74,40.65,41.65]);positions.extend([[1630,520,1400],[960,540,-110],[960,540,-110],[300,900,160]]);scales.extend([.4,.98,.98,.42]);rxs.extend([8,1,1,10]);rys.extend([-15,-5,-5,-12])
 # Return every object to the shared wide state before the surface comes back.
 if j!=5:times.extend([40.7,41.65]);positions.extend([positions[-1],[x,y,z]]);scales.extend([scales[-1],.42]);rxs.extend([rxs[-1],10]);rys.extend([rys[-1],-12])
 floating(inner,'Estación '+cc['name'],cc['name'],times,positions,scales,rxs,rys,14.28,42.15)
cursor(inner,'Cursor de aprobación',[[1800,1160],[1130,900],[1130,900],[1550,1150]],[33.7,34.14,34.32,34.95],33.7,35.13)
exec((R/'scripts/finish-v2.py').read_text())
master=comp(S['master']);background(master)
nested(master,'Apertura y superficie',intro['name'],0,0,0,14.48)
n=nested(master,'Inmersión y proceso',inner['name'],0,0,14.23,42.15);anim(n,'opacity',[14.23,14.48,41.75,42.15],[0,1,1,0],'flow')
n=nested(master,'Resultado y montaje',result['name'],0,0,41.72,53.7);anim(n,'opacity',[41.72,42.12],[0,1],'flow')
n=nested(master,'Versiones',variants['name'],0,0,53.5,63.36);anim(n,'opacity',[53.5,53.7],[0,1],'flow')
n=nested(master,'Cierre',closing['name'],0,0,63.22,D);anim(n,'opacity',[63.22,63.36],[0,1],'flow')
node(master,'audio','Mezcla V2',0,0,0,D,asset='Mezcla-V2.wav')
# User selected La Máquina on 3 Oct; this supersedes the initial dossier exclusion.
assetmap={f'denim-{i+1:02}':f'maquina-{j:02}' for i,j in enumerate([1,4,10,11,12])}
for c in S['comps'].values():
 for n in c['layers']:
  if n['type']=='media':
   for old,new in assetmap.items():
    if n['asset'].startswith(old):n['asset']=n['asset'].replace(old,new)
   if n['asset'].startswith('chef-'):
    j=int(n['asset'].split('-')[1].split('.')[0])-1;n['asset']=f'maquina-{[1,10,12][j]:02}.mp4';n['scale']=[v*n['srcW']/1080 for v in n['scale']];n['anchor']=[540,960];n['srcW']=1080;n['srcH']=1920;n['freezeTail']=True
# All keyframes follow the same pause edit; no independent timing patches in AE.
from retime import T,D as NEWD
S['duration']=NEWD
for c in S['comps'].values():
 c['duration']=NEWD
 for n in c['layers']:
  n['from']=T(n['from']);n['to']=min(NEWD,T(n['to']))
  for an in n['anim'].values():an['times']=[T(t) for t in an['times']]
(R/'src/design-v2.json').write_text(json.dumps(S,indent=2,ensure_ascii=False))
print('V2',len(S['comps']),'comps',sum(len(c['layers']) for c in S['comps'].values()),'layers',NEWD,'seconds')
