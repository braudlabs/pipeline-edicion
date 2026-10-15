from pathlib import Path
from PIL import Image,ImageFont
import json,math
R=Path(__file__).resolve().parents[1]; A=R/'assets'; F=48
INK='#100e0b'; CREAM='#fff6e9'; AMBER='#ffb34f'; ORANGE='#ff753d'; DIM='#9c9486'; GREEN='#c4edb1'
S={'fps':F,'master':'COCINA - FINAL','comps':{},'events':{}}
def comp(name,dur,w=1080,h=1920,camera=None):
 c={'name':name,'width':w,'height':h,'duration':dur,'layers':[]}
 if camera:c['camera']=camera
 S['comps'][name]=c;return c
def node(c,t,name,pos=(0,0),a=0,b=None,**kw):
 n={'type':t,'name':name,'pos':list(pos),'from':a,'to':c['duration'] if b is None else b,**kw};c['layers'].append(n);return n
def anim(n,p,frames,values,ease='out'):
 n.setdefault('anim',{})[p]={'frames':frames,'values':values,'ease':ease};return n
def txt(c,name,s,x,y,size=70,col=CREAM,a=0,b=None,align='center',font='bold',**kw):
 return node(c,'text',name,(x,y),a,b,text=s,size=size,color=col,font=font,track=kw.pop('track',-28),align=align,**kw)
def rect(c,name,x,y,w,h,col=INK,a=0,b=None,**kw):return node(c,'rect',name,(x,y),a,b,w=w,h=h,color=col,**kw)
def ellipse(c,name,x,y,w,h=None,col=None,a=0,b=None,**kw):return node(c,'ellipse',name,(x,y),a,b,w=w,h=h or w,color=col,**kw)
def path(c,name,pts,col=AMBER,width=3,a=0,b=None,**kw):return node(c,'path',name,a=a,b=b,points=pts,stroke=col,strokeWidth=width,**kw)
def media(c,name,asset,x,y,w,a=0,b=None,**kw):
 iw,ih=Image.open(A/asset).size
 return node(c,'image',name,(x,y),a,b,asset=asset,w=w,h=w*ih/iw,anchor=[iw/2,ih/2],**kw)
def nested(c,name,src,x,y,scale=1,a=0,b=None,**kw):
 cc=S['comps'][src];return node(c,'comp',name,(x,y),a,b,source=src,anchor=[cc['width']/2,cc['height']/2],scale=[scale,scale],**kw)
def enter(n,a=0,d=16,axis='y',delta=80,blur=0):
 p=n['pos'];p0=p.copy();p0[0 if axis=='x' else 1]+=delta
 anim(n,'pos',[a,a+d],[p0,p]);anim(n,'opacity',[a,a+min(d,6)],[0,1])
 if blur:anim(n,'blur',[a,a+d],[blur,0])
 return n
def three(n,z=0):n['threeD']=True;n['pos']+=[z];return n
def bg(c):
 node(c,'gradient','Fondo negro ambar',(540,960),w=1080,h=1920,anchor=[540,960],color='#3c2718',endColor='#090a0c',center=[500,750],radius=1150)
 # Subtle architectural rules locate the stage without forming a card grid.
 for x in [100,980]:path(c,'Linea de escenario '+str(x),[[x,260],[x,1400]],'#6a4a2b',1,opacity=.26)
def label(c,s,y=330):txt(c,'Etiqueta editorial',s,540,y,24,DIM,track=180)
def focus_camera(frames,values):return {'frames':frames,'values':values,'zoom':1800}
def word_width(s,size):
 f=ImageFont.truetype(str(A/'Display-Bold.otf'),size);return f.getlength(s)-max(0,len(s)-1)*size*.028
def kinetic(c,s,x,y,size=140,col=CREAM,a=0,axis='y',spacing=2):
 widths=[word_width(ch,size) for ch in s];cursor=x-sum(widths)/2
 for i,(ch,w) in enumerate(zip(s,widths)):
  if ch!=' ':
   n=txt(c,f'{s} | letra {i}',ch,cursor+w/2,y,size,col,a+i*spacing)
   enter(n,a+i*spacing,13,axis,70 if axis=='y' else -70,5)
  cursor+=w

# Semantic objects are independent compositions, not captured reference frames.
c=comp('OBJ - Generar',240,720,210)
rect(c,'Base del control',0,0,720,210,'#201912',round=38,stroke='#7d5630',strokeWidth=2)
ellipse(c,'Indicador de generacion',95,105,48,col=AMBER)
txt(c,'Texto del control','GENERAR',400,131,67,CREAM,track=90)

for key,handle,followers,views in [('kurt','@notkurtgodel','83,3 mil','7,7 M'),('elliot','@notelliotkay','13,5 mil','4,9 M')]:
 c=comp('PRUEBA - '+key,480,980,1080)
 rect(c,'Panel oscuro de evidencia',0,0,980,1080,'#111315',round=42,stroke='#555047',strokeWidth=2)
 media(c,'Perfil original verificado',key+'-profile-proof.png',490,130,880)
 path(c,'Separador',[[70,235],[910,235]],'#504b43',2)
 txt(c,'Seguidores cifra editable',followers,480,410,160,CREAM)
 txt(c,'Seguidores unidad','SEGUIDORES',480,462,28,DIM,track=120)
 txt(c,'Visitas cifra editable',views,347,731,182,AMBER)
 txt(c,'Visitas unidad','VISUALIZACIONES',340,790,27,CREAM,track=60)
 txt(c,'Contexto de visitas','EN UN SOLO REEL',340,829,21,DIM,track=80)
 media(c,'Prueba original del reel',key+'-proof-0.png',758,764,270,shadow=[0,18,28,'#000000',.75])
 path(c,'Union cifra y prueba',[[235,886],[235,937],[758,937],[758,984]],AMBER,3)
 ellipse(c,'Nodo union',235,886,12,col=AMBER)
 txt(c,'Identificador de cuenta',handle,490,1030,31,DIM)

c=comp('OBJ - Biblioteca',320,940,880)
rect(c,'Marco de biblioteca',0,0,940,880,'#f5f0e8',round=28)
txt(c,'Cabecera biblioteca','Visual Hub',60,91,59,'#15120d',align='left')
txt(c,'Descripcion biblioteca','APRENDE · APLICA · ESCALA',60,132,20,'#666052',align='left',track=100)
for i,asset in enumerate(['curso-maestria.png','curso-escala.png','curso-masterclasses.png']):
 y=286+i*208
 media(c,'Curso real '+str(i+1),asset,237,y,334)
 txt(c,'Nombre curso '+str(i+1),['Maestría','Escala','Masterclasses'][i],455,y-4,43,'#17130e',align='left')
 txt(c,'Ordinal curso '+str(i+1),'0'+str(i+1),837,y+40,57,'#b79e7f')

# 21.1–25.17: macro token, pull-back, kinetic type and consumption mechanism.
c=comp('MG - Creditos',196,camera=focus_camera([0,18,42,154,196],[[540,870,-920],[540,910,-1850],[540,960,-1800],[540,960,-1800],[540,910,-1420]]));bg(c);label(c,'EL COSTE DE REPETIR')
for i in range(7):
 theta=i*2*math.pi/7;x=540+410*math.cos(theta);y=835+255*math.sin(theta)
 n=three(media(c,'Credito consumido '+str(i), 'credit-token.png',x,y,165,a=16+i*4),110+(i%3)*85)
 p=n['pos'].copy();anim(n,'pos',[16+i*4,41+i*4,83+i*10,98+i*10],[p,p,p,[540,1055,-10]])
 anim(n,'scale',[16+i*4,33+i*4,83+i*10,98+i*10],[[.7,.7],[1,1],[1,1],[.15,.15]])
 anim(n,'opacity',[16+i*4,28+i*4,91+i*10,99+i*10],[0,1,1,0])
 anim(n,'rot',[16+i*4,99+i*10],[i*24,i*24+65])
n=three(media(c,'Ficha protagonista','credit-token.png',540,785,590,a=0,b=63),-70)
anim(n,'pos',[0,20,45,62],[[540,960,-120],[540,795,-70],[540,765,-70],[540,1110,-30]])
anim(n,'scale',[0,22,45,62],[[1.1,1.1],[.79,.79],[.79,.79],[.14,.14]])
anim(n,'opacity',[48,63],[1,0])
kinetic(c,'CRÉDITOS',540,615,142,CREAM,7,'y',2)
n=nested(c,'Control de generacion','OBJ - Generar',540,1088,.87,24)
enter(n,24,18,'y',95,8)
for f in [67,101,139]:
 ellipse(c,'Pulso del control '+str(f),540,1088,94,col=None,a=f,b=f+22,stroke=AMBER,strokeWidth=5,anim={'scale':{'frames':[f,f+22],'values':[[1,1],[4,4]],'ease':'out'},'opacity':{'frames':[f,f+22],'values':[.85,0],'ease':'out'}})
for i in range(12):
 n=rect(c,'Medidor credito '+str(i),259+i*47,1240,34,9,AMBER,a=25,b=196,round=3)
 anim(n,'opacity',[25,54+i*9,55+i*9],[1,1,.08],'hold')
txt(c,'Repeticion de voz','generación tras generación',540,1360,39,DIM,102)
S['events']['credits']={'from':1012,'to':1208,'comp':c['name']}

# Time and money: foreground object and independent typography share a camera move.
c=comp('MG - Tiempo',112,camera=focus_camera([0,16,70,112],[[460,925,-1420],[540,960,-1800],[540,960,-1800],[570,960,-1610]]));bg(c)
n=three(media(c,'Reloj de arena fotografico','hourglass.png',352,865,420),-75);enter(n,0,17,'x',-430,15);anim(n,'rot',[0,19,75,112],[-17,-5,-5,8])
n=three(media(c,'Ficha como coste','credit-token.png',795,1090,420),120);enter(n,8,20,'x',470,12)
txt(c,'Unidad narrativa','SE CONVIERTE EN',540,430,27,DIM,track=130)
enter(txt(c,'Tiempo','TIEMPO',653,750,110,CREAM,7),7,14,'x',150,7)
enter(txt(c,'Dinero','DINERO',659,885,108,AMBER,21),21,14,'x',150,7)
n=txt(c,'Perdido','PERDIDO',540,1250,108,CREAM,78);enter(n,78,11,'y',65,6)
path(c,'Subrayado perdido',[[290,1290],[790,1290]],ORANGE,8,a=83,trim=[83,99])
S['events']['time']={'from':1540,'to':1652,'comp':c['name']}

# Accounts travel: front evidence, change depth, translate X, arrive and return overview.
c=comp('MG - Cuentas',349,camera=focus_camera([0,20,82,109,131,199,223,257,291,323,349],[[540,850,-1270],[540,940,-1820],[540,940,-1820],[870,960,-2530],[1640,940,-1820],[1640,940,-1820],[1640,1005,-1600],[1640,1005,-1600],[1090,960,-3280],[1090,960,-3280],[1090,960,-2860]]));bg(c)
for i,(k,x) in enumerate([('kurt',540),('elliot',1640)]):
 n=three(nested(c,'Perfil y resultados '+k,'PRUEBA - '+k,x,853,.84),0)
 n['ry']= -4 if i==0 else 4
 if i==0:enter(n,0,18,'y',150,10)
 # A warm backlight has its own depth, behind each proof object.
 n=three(ellipse(c,'Halo tras '+k,x,865,1060,1030,col='#624125',opacity=.25,blur=130),360)
 # Move halo below panels by layer order.
 c['layers'].remove(n);c['layers'].insert(3+i,n)
n=three(path(c,'Conexion entre cuentas',[[960,1160],[1090,1160],[1090,1160],[1230,1160]],AMBER,4,a=259,trim=[259,288]),100)
for x in [980,1230]:three(ellipse(c,'Punto de union '+str(x),x,1160,16,col=AMBER,a=259),100)
txt(c,'Titulo escena cuentas','CUENTAS REALES. ALCANCE REAL.',540,294,26,DIM,track=90)
enter(txt(c,'Consistencia cierre','CONSISTENCIA',540,1190,83,AMBER,290),290,16,'y',75,7)
txt(c,'Nota de pruebas','Cifras de las capturas aportadas',540,1380,21,DIM,0)
S['events']['accounts']={'from':1744,'to':2093,'comp':c['name']}

# Brand impression transitions into actual library, no old plate/receipt metaphor.
c=comp('MG - Marca',66)
rect(c,'Placa marca',130,1030,820,220,'#110d0b',round=38,opacity=.96)
kinetic(c,'Visual Hub',540,1176,114,CREAM,0,'x',1)
path(c,'Trazo marca',[[226,1222],[854,1222]],AMBER,5,a=9,trim=[9,35])
S['events']['brand']={'from':2125,'to':2191,'comp':c['name']}

c=comp('MG - Comunidad',145,camera=focus_camera([0,22,102,145],[[540,800,-1210],[540,950,-1900],[540,930,-1730],[540,930,-1540]]));bg(c);label(c,'VISUAL HUB · COMUNIDAD')
n=three(nested(c,'Biblioteca real de cursos','OBJ - Biblioteca',540,885,.90),60);anim(n,'ry',[0,24,105,145],[-22,-5,-5,9]);anim(n,'rx',[0,24,145],[9,0,-4]);enter(n,0,22,'y',190,10)
kinetic(c,'CREA MEJOR.',540,450,98,CREAM,4,'y',1)
txt(c,'Orientacion profesional','NEGOCIO  /  MARCA  /  CLIENTES',540,1330,29,DIM,25,track=80)
S['events']['community']={'from':2338,'to':2483,'comp':c['name']}

# Systems scene: enter through a template, pull back into connected production rig,
# camera dives into a repeat counter then locks on the consistent result.
c=comp('OBJ - Plantilla',480,600,720)
rect(c,'Superficie de plantilla',0,0,600,720,'#ece4d5',round=32)
txt(c,'Titulo plantilla','PLANTILLA',55,95,45,'#1a1712',align='left',track=50)
path(c,'Regla plantilla',[[55,135],[545,135]],'#b6a791',2)
for i,(label_,val) in enumerate([('01 · IDENTIDAD','MISMO AVATAR'),('02 · ESCENA','MISMO ESTILO'),('03 · SALIDA','MISMA CALIDAD')]):
 y=212+i*145;txt(c,'Campo '+str(i),label_,55,y,22,'#877b68',align='left',track=30)
 txt(c,'Valor '+str(i),val,55,y+52,33,'#1b1712',align='left')
rect(c,'Estado listo',55,640,490,40,'#cfbf9f',round=8)
txt(c,'Texto listo','LISTA PARA UTILIZAR',300,670,22,'#2d2518',track=70)

c=comp('OBJ - Resultado',480,600,720)
rect(c,'Base resultado',0,0,600,720,'#181b19',round=32,stroke='#597048',strokeWidth=2)
txt(c,'Titulo resultado','MISMA IDENTIDAD',300,82,30,DIM,track=70)
for i in range(3):
 x=122+i*178
 n=media(c,'Retrato original '+str(i+1),'chef-'+str(i+1)+'.jpg',x,290,195,a=60+i*7,rot=[-5,0,5][i],shadow=[0,12,12,'#000000',.7])
 enter(n,60+i*7,20,'y',95,7)
 txt(c,'Version '+str(i+1),'0'+str(i+1),x,501,26,AMBER,80+i*7)
txt(c,'Resultado label','CONSISTENCIA',300,571,51,GREEN)
txt(c,'Resultado texto','visual · generación tras generación',300,610,23,DIM)
ellipse(c,'Check circulo',300,636,56,col=GREEN)
path(c,'Check trazado',[[286,636],[297,646],[315,622]],'#172317',5)

c=comp('MG - Sistemas',374,camera=focus_camera([0,22,68,98,164,194,232,270,309,341,374],[[150,760,-1120],[150,820,-1780],[150,820,-1780],[600,850,-2650],[600,850,-2650],[1050,840,-1780],[1050,840,-1780],[1050,840,-1780],[1050,840,-1780],[1050,840,-1780],[1050,840,-1550]]));bg(c);label(c,'UN PROCESO QUE PUEDES REPETIR')
n=three(nested(c,'Plantilla editada','OBJ - Plantilla',150,775,.9),0);enter(n,0,20,'x',-170,9);anim(n,'ry',[0,24,98],[-16,-4,0])
n=three(nested(c,'Resultado consistente','OBJ - Resultado',1050,775,.9,a=65,b=265),0);enter(n,65,24,'x',150,9);anim(n,'ry',[65,92,194],[18,4,0])
three(path(c,'Proceso trazado',[[424,840],[525,840],[525,840],[775,840]],AMBER,5,a=63,trim=[63,104]),0)
for i,x in enumerate([470,550,630,710]):
 n=three(ellipse(c,'Pulso del proceso '+str(i),x,840,16,col=AMBER,a=84+i*7,b=130+i*7),-15);anim(n,'opacity',[84+i*7,91+i*7,129+i*7],[0,1,0])
kinetic(c,'SISTEMAS',540,459,114,CREAM,12,'y',1)
# Counter metaphor appears on the right only when '50 generaciones' is spoken.
counter_start=265
rect(c,'Oscurecimiento contador',80,575,920,580,'#100e0b',a=counter_start,b=355,round=45,opacity=1)
txt(c,'Contador contexto','SIN TENER QUE HACER',540,683,29,DIM,counter_start,b=355,track=85)
for i,(f,v) in enumerate([(265,'01'),(271,'05'),(277,'12'),(283,'24'),(289,'38'),(297,'50')]):
 b=[271,277,283,289,297,341][i]
 txt(c,'Intentos '+v,v,540,961,275,AMBER,f,b)
txt(c,'Contador unidad','GENERACIONES',540,1033,47,CREAM,265,341,track=80)
path(c,'Tachado cincuenta',[[318,873],[771,873]],ORANGE,11,a=314,b=341,trim=[314,327])
enter(txt(c,'Cierre sistemas','ALGO BUENO.',540,943,103,GREEN,341),341,14,'y',62,6)
S['events']['system']={'from':2574,'to':2948,'comp':c['name']}

# Live annotation sits below subject and grows from an actual live-session shot.
c=comp('MG - Directo',89)
n=rect(c,'Directo respaldo',150,1080,780,146,'#141610',round=32,opacity=.95);enter(n,0,15,'x',-95)
ellipse(c,'Directo luz',234,1150,27,col=GREEN,a=4)
n=txt(c,'Directo rotulo','SESIONES EN DIRECTO',577,1170,45,CREAM,4);enter(n,4,12,'x',-55)
S['events']['live']={'from':2994,'to':3083,'comp':c['name']}

c=comp('MG - Precio',121)
rect(c,'Respaldo oferta',130,1020,820,350,'#120e0b',round=45,opacity=.96)
txt(c,'Nombre oferta','Visual Hub',540,1102,49,CREAM,0)
n=txt(c,'Precio editable','39',487,1300,210,AMBER,43);enter(n,43,12,'y',90,7)
n=txt(c,'Moneda editable','$',678,1208,84,AMBER,43);enter(n,43,12,'y',90,7)
txt(c,'CTA','ENTRA EN LA COMUNIDAD',540,1340,24,DIM,58,track=65)
path(c,'Linea precio',[[245,1131],[835,1131]],'#765334',2,a=8,trim=[8,28])
S['events']['price']={'from':3279,'to':3400,'comp':c['name']}

# Main composition: exact editorial base, new scenes, adaptive caption overlays.
c=comp(S['master'],3400)
node(c,'video','Montaje nuevo de clips',(540,960),asset='Montaje-Cocina.mp4',anchor=[540,960])
node(c,'audio','Mezcla voz musica efectos',(540,960),asset='Mezcla-Final.wav')
for k,e in S['events'].items():
 n=nested(c,'ESCENA - '+k,e['comp'],540,960,a=e['from'],b=e['to'],startTime=e['from']/F)
 # Full-screen scenes cut on motion; no sluggish fade through the footage.
 if k in ['credits','community','system','accounts']:
  anim(n,'opacity',[e['from'],e['from']+3],[0,1])

caps=json.load(open(R/'analysis/captions.json'));layout=[]
emphasis={'IA':106,'misma persona':99,'cara':110,'voz':110,'consistente':96,'constantemente':88,'tiempo y dinero':92,'perdido':114,'plantillas y sistemas':85,'39 dólares':104,'prueba y error':95}
directions=['x-','y','x+','y','x-','x+']
full=[(e['from'],e['to']) for k,e in S['events'].items() if k in ['credits','accounts','community','system']]
for ci,cap in enumerate(caps):
 a,b=cap['from'],cap['to'];phrase=' '.join(w['text'] for w in cap['words'])
 # Integrated motion titles replace exactly matching spoken captions.
 if cap['clip']==8 or a>=3279:continue
 if cap['clip']==10 and a>=2125:continue
 if any(w in phrase for w in ['sesiones en','directo donde']) and a>=2994 and b<=3083:pass
 size=emphasis.get(phrase,78)
 total=word_width(phrase,size)
 if total>838:size=math.floor(size*838/total);total=word_width(phrase,size)
 onmg=any(aa<=a<bb for aa,bb in full)
 y=1328 if onmg else (1250 if cap['clip'] in [5,14] else 1230)
 axis= directions[ci%len(directions)];dx=-66 if axis=='x-' else 66 if axis=='x+' else 0;dy=40 if axis=='y' else 0
 pad=28;lh=size*1.30;left=(1080-total)/2
 widths=[word_width(w['text'],size) for w in cap['words']];space=ImageFont.truetype(str(A/'Display-Bold.otf'),size).getlength(' ')-size*.028
 if not onmg:
  fullwidth=sum(widths)+space*(len(widths)-1)+2*pad
  n=rect(c,f'SUB {ci:02d} | contraste',left-pad,y-size*.88,fullwidth,lh,'#100f0d',a,b,round=17,opacity=.83)
  anim(n,'pos',[a,a+7],[[left-pad+dx,y-size*.88+dy],[left-pad,y-size*.88]])
  anim(n,'opacity',[a,a+3],[.40,.83])
  fs=[a];vs=[[(widths[0]+2*pad)/fullwidth,1]]
  for wi,w in enumerate(cap['words'][1:],1):
   wa=max(a+1,w['from']);fs.extend([wa,wa+4]);vs.extend([vs[-1],[(sum(widths[:wi+1])+space*wi+2*pad)/fullwidth,1]])
  anim(n,'scale',fs,vs)
 x=(1080-sum(widths)-space*(len(widths)-1))/2
 for wi,(w,ww) in enumerate(zip(cap['words'],widths)):
  wa=max(a,w['from']);wb=b
  if wb<=wa:continue
  col=AMBER if w['text'].lower() in ['ia','problemas','persona','plástica','artificial','créditos','constantemente','consistentes','sistemas','error'] else CREAM
  n=txt(c,f'SUB {ci:02d}.{wi} | '+w['text'],w['text'],x+ww/2,y,size,col,wa,wb,shadow=[0,3,6,'#000000',.9],textStroke=['#100e0b',2])
  p=n['pos'];anim(n,'pos',[wa,min(wa+8,wb)],[[p[0]+dx,p[1]+dy],p]);anim(n,'opacity',[wa,min(wa+3,wb)],[.65,1])
  layout.append({'text':w['text'],'from':wa,'to':wb,'left':x,'right':x+ww,'top':y-size,'bottom':y+size*.29,'direction':axis,'fontSize':size})
  x+=ww+space

(R/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'analysis/caption-layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2))
(R/'analysis/motion-map.json').write_text(json.dumps({'fps':F,'events':S['events'],'reference':'96c1: macro > pullback > nested publication > depth push; typography: directional reveals and word hierarchy from LaFabrica references','nativeLayers':sum(len(c['layers']) for c in S['comps'].values()),'captionDirections':directions},ensure_ascii=False,indent=2))
print(len(S['comps']),'comps',sum(len(c['layers']) for c in S['comps'].values()),'semantic layers')
