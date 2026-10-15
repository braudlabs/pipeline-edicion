from pathlib import Path
import json,math
from PIL import Image,ImageFont
R=Path(__file__).resolve().parents[2];E=json.loads((R/'src/v3/edit-map.json').read_text());D=E['duration'];F=30
BG='#09090B';P='#18181C';LINE='#3A3A40';INK='#F5F5F7';MUTED='#8C8C94';ORANGE='#FF641A'
S={'fps':F,'duration':D,'master':'EL SISTEMA - V3 NARANJA','comps':{}}
def comp(name,w=1920,h=1080):
 c=dict(name=name,width=w,height=h,duration=D,layers=[]);S['comps'][name]=c;return c
def node(c,t,name,x=0,y=0,a=0,b=D,**k):
 if any(n['name']==name for n in c['layers']):name+=' '+str(len(c['layers']))
 n=dict(type=t,name=name,pos=[x,y],anim={},**{'from':a,'to':b},**k);c['layers'].append(n);return n
def tx(c,s,x,y,size=100,a=0,b=D,col=INK,bold=True,align='left',track=-25):return node(c,'text',s,x,y,a,b,text=s,size=size,color=col,font='SFProDisplay-'+('Bold' if bold else 'Regular'),align=align,track=track)
def rect(c,name,x,y,w,h,col=P,a=0,b=D,r=26,stroke=None,opacity=1):return node(c,'rect',name,x,y,a,b,w=w,h=h,color=col,stroke=stroke,round=r,opacity=opacity)
def ell(c,name,x,y,w,h,col=None,a=0,b=D,stroke=None,sw=2,opacity=1):return node(c,'ellipse',name,x,y,a,b,w=w,h=h,color=col,stroke=stroke,strokeWidth=sw,opacity=opacity)
def path(c,name,points,col=LINE,sw=2,a=0,b=D,closed=False,fill=None):return node(c,'path',name,0,0,a,b,points=points,color=fill,stroke=col,strokeWidth=sw,closed=closed)
def anim(n,p,t,v,ease='flow'):n['anim'][p]={'times':t,'values':v,'ease':ease};return n
def blur(n,v):n.setdefault('effects',[]).append({'match':'ADBE Gaussian Blur 2','props':[[[1],v],[[3],False]]});return n
def bg(c,col=BG):rect(c,'Fondo',0,0,c['width'],c['height'],col,r=0)
def atmosphere(c):
 bg(c)
 # restrained, broad orange backlight, no permanent ornamental line.
 n=ell(c,'Luz de estudio',1440,1140,1280,390,'#7F2509',opacity=.28);blur(n,240)
def pic(c,name,asset,x,y,w,a=0,b=D,offset=1.5):
 if asset.startswith('maquina-') and asset.endswith('.jpg'):asset='v3/hq-'+asset.split('-')[-1]
 ww,hh=(1080,1920) if asset.endswith('.mp4') else Image.open(R/'assets'/asset).size
 return node(c,'media',name,x,y,a,b,asset=asset,scale=[w/ww,w/ww],anchor=[ww/2,hh/2],sourceOffset=offset,freezeTail=asset.endswith('.mp4'))
def nest(c,name,cc,x=960,y=540,a=0,b=D,s=1):
 return node(c,'comp',name,x,y,a,b,asset=cc['name'],scale=[s,s],anchor=[cc['width']/2,cc['height']/2])
def enter(n,t,dx=0,dy=60,d=.38):
 x,y=n['pos'][:2];anim(n,'pos',[t,t+d],[[x+dx,y+dy],[x,y]],'out');anim(n,'opacity',[t,t+.13],[0,1],'linear');return n
def title(c,s,x,y,size,a,b,col=INK):return enter(tx(c,s,x,y,size,a,b,col,align='center'),a,dy=65,d=.34)
def pose(n,t,pos,scale=None,rx=None,ry=None,rot=None):
 n['threeD']=True;anim(n,'pos',t,[p if len(p)==3 else p+[0] for p in pos]);
 if scale:anim(n,'scale',t,[[s,s] for s in scale])
 if rx:anim(n,'rx',t,rx)
 if ry:anim(n,'ry',t,ry)
 if rot:anim(n,'rot',t,rot)
 return n
def panel(c,name,x,y,w,h,col=P,r=32):
 rect(c,name+' canto',x-1,y-1,w+2,h+2,'#3C3C43',r=r+1)
 rect(c,name,x,y,w,h,col,r=r)
def card(name,i,w=480,h=800,a=0,b=D,moving=False):
 c=comp(name,w,h);n=pic(c,'Imagen',f'maquina-{i:02}.'+('mp4' if moving else 'jpg'),w/2,h/2,max(w,h*1080/1920),a,b);n['maskCrop']=[w,h,32] # applied on the precomp instance instead; underlying source remains untouched
 n.pop('maskCrop');return c
def tile(c,name,cc,x,y,a=0,b=D,s=1):
 n=nest(c,name,cc,x,y,a,b,s);n['roundedMask']=[cc['width'],cc['height'],28];return n
def wordmark(c,x,y,size,a=0,b=D):
 n=tx(c,'el sistema',x,y,size,a,b,INK,align='center',track=-45)
 # Precisely measured mark: type alone, with an orange terminal.
 f=ImageFont.truetype('/Users/alejandrorubiocamarero/Library/Fonts/SFPRODISPLAYBOLD.OTF',round(size));w=f.getlength('el sistema')-9*size*.045
 ell(c,'Punto de marca',x+w/2+size*.19,y-size*.10,size*.14,size*.14,ORANGE,a,b)
 return n
def cursor(c,t,positions,times,b):
 n=path(c,'Cursor',[[0,0],[0,61],[16,48],[30,76],[42,70],[30,43],[51,42]],'#09090B',2,t,b,True,INK);n['pos']=positions[0];anim(n,'pos',times,positions);return n
def draw(n,t,d=.4):n['trim']={'times':[t,t+d],'values':[0,100],'ease':'out'};return n
# Reusable real shots, native crop comps. Nothing from reference videos is inserted.
shots={i:card('V3 | Plano '+str(i),i,480,800) for i in range(1,17)}
# Opening: pictures arrive in depth, typography changes scale on the voice.
intro=comp('V3 | 01 Idea a interfaz');atmosphere(intro)
for j,i in reversed(list(enumerate([1,10,12]))):
 n=tile(intro,'Visión '+str(i),shots[i],1310+j*255,555,0,2.75,.96)
 pose(n,[0,.50+j*.06,2.22,2.75],[[1470+j*340,700,700+j*180],[1240+j*255,548,j*120],[1210+j*255,525,j*110],[2200+j*290,470,-80]],[.94,.98,1.02,.93],[13,2,2,5],[-28,-8+j*7,-8+j*7,22],[0,0,0,0])
n=tx(intro,'Lo imaginas.',126,548,126,0,2.7);enter(n,0,dy=90,d=.40)
n=tx(intro,'No sale igual.',130,657,60,.75,2.7,MUTED,bold=False);enter(n,.75,dx=-80,dy=0,d=.30)
# Single-axis type handoff, bold hierarchy.
title(intro,'No es la',960,447,96,2.65,4.05,MUTED)
n=title(intro,'herramienta.',960,647,196,2.77,4.05);anim(n,'pos',[2.77,3.13,3.91,4.25],[[960,742],[960,647],[960,647],[960,170]])
title(intro,'Es el',960,395,78,4.05,5.18,MUTED)
n=title(intro,'proceso.',960,640,234,4.18,5.18,ORANGE);anim(n,'scale',[4.18,4.6,5.0,5.28],[[.82,.82],[1,1],[1,1],[1.38,1.38]])
n=wordmark(intro,960,590,176,5.18,6.30);enter(n,5.18,dy=90,d=.4)
# Minimal product surface: the field is the hero; text readable at this camera distance.
field=comp('V3 | Entrada',1440,196);panel(field,'Campo',2,2,1436,192,'#202023',r=42)
text=tx(field,'Una máquina que fabrica creativos',62,120,56,7.65,D,bold=False,track=-15);text['typeOn']=[7.65,9.00]
ell(field,'Enviar',1340,98,64,64,ORANGE)
path(field,'Flecha enviar',[[1340,119],[1340,78],[1325,93],[1340,78],[1355,93]],INK,4)
tx(field,'Cuéntame tu idea…',62,120,56,0,7.65,MUTED,bold=False,track=-15)
title(intro,'Así de simple.',960,359,125,6.3,9.47)
fld=nest(intro,'Entrada continua',field,960,570,6.3,9.95,1)
pose(fld,[6.3,6.95,7.8,8.35,9.2,9.95],[[1080,860,420],[960,590,0],[960,590,0],[887,568,-230],[887,568,-230],[580,560,-1740]],[.9,1,1,1,1,1],[14,0,0,0,0,0],[-19,0,0,0,0,0])
cursor(intro,8.7,[[1600,1130],[1580,597],[1580,597],[1710,1130]],[8.7,9.10,9.23,9.6],9.75)
# 2: the input opens into the system. Native modules explode and assemble, then attention follows the same objects.
inside=comp('V3 | 02 Dentro del sistema');atmosphere(inside)
conf=comp('V3 | Confirmación',1390,780);panel(conf,'Propuesta',2,2,1386,776)
tx(conf,'Tu idea, entendida.',70,136,88)
tx(conf,'La máquina de fabricar creativos',74,225,38,col=MUTED,bold=False)
for j,i in enumerate([1,4,10,11]):
 n=tile(conf,'Ejemplo '+str(i),shots[i],160+j*235,427,s=.36)
 anim(n,'opacity',[10.90,11.55+j*.32,11.80+j*.32],[.22,.22,1]);anim(n,'scale',[11.55+j*.32,11.84+j*.32,12.04+j*.32],[[.36,.36],[.41,.41],[.36,.36]])
rect(conf,'Aceptar',998,524,314,116,ORANGE,r=28);tx(conf,'Confirmar',1155,597,40,col=BG,align='center')
n=tx(conf,'Antes de gastar.',73,709,45,13.3,D,col=INK);enter(n,13.3,dx=-70,dy=0,d=.32)
# Depth overview, not a flat slide of little cards. Shot rail and script fan are next locations.
scriptc=comp('V3 | Guion',1050,900);panel(scriptc,'Guion',1,1,1048,898)
tx(scriptc,'16 escenas.',62,126,80)
for j,s in enumerate(['La máquina interrumpe','Diez anuncios más','La reacción de Deivid','Producción en cadena','Enterrado en creativos']):
 y=199+j*124;rect(scriptc,'Renglón '+str(j),54,y,942,103,'#252529',r=20);tx(scriptc,f'{j+1:02}',88,y+67,38,col=ORANGE);tx(scriptc,s,184,y+68,39,bold=False)
identity=comp('V3 | Identidad',1130,850);panel(identity,'Anclas',1,1,1128,848)
tx(identity,'Misma identidad.',60,124,82)
for j,i in enumerate([1,4]):
 tile(identity,'Referencia '+str(i),shots[i],309+j*512,472,s=.63)
 txt=['Personaje','Producto'][j];tx(identity,txt,309+j*512,796,36,col=MUTED,align='center')
# Small semantic thumbnails form a depth explosion, not arbitrary decorations.
for j,(cc,x,y,zz) in enumerate([(scriptc,0,530,470),(identity,1840,510,520),(conf,960,580,0)]):
 n=nest(inside,'Módulo '+str(j),cc,x,y,9.48,15.60,.60)
 if j==2:
  pose(n,[9.48,10.30,10.78,11.46,13.95,14.62,15.6],[[1010,540,-1650],[960,555,140],[960,555,140],[930,550,-40],[930,550,-40],[920,490,-200],[-890,490,160]],[.94,.70,.70,1.11,1.11,1.17,.9],[8,9,9,1,1,0,8],[-16,-13,-13,-3,-3,0,23])
 else:
  pose(n,[9.48,10.3,10.8,11.46,14.94,15.6],[[960,540,700],[x,y,zz],[x,y,zz],[x+(-700 if j==0 else 700),y,900],[x,y,900],[x-1500,y,1000]],[.4,.60,.60,.60,.60,.55],[30,6,6,9,9,9],[-35,-10,-10,-15,-15,24])
# Orange confirms and carries into the scene strip.
cursor(inside,13.60,[[1710,1080],[1480,785],[1480,785],[1850,1050]],[13.60,14.05,14.19,14.56],14.65)
r=ell(inside,'Pulso confirmar',1485,785,140,140,None,14.13,14.65,ORANGE,3);anim(r,'scale',[14.13,14.65],[[.1,.1],[1.65,1.65]]);anim(r,'opacity',[14.13,14.65],[1,0])
# The script lines unfold into the actual shot series. A rapid, causal assembly.
rail=comp('V3 | Despliegue escenas',2700,1080)
for j,i in enumerate([1,2,3,4,5]):
 n=tile(rail,'Escena '+str(j+1),shots[i],420+j*495,552,15.10,17.05,.83)
 pose(n,[15.10+j*.035,15.74+j*.035,16.37,17.05],[[320,550,80+j*90],[380+j*495,540,0],[380+j*495,540,0],[380+j*495-1900,540,80]],[.66,.91,.91,.92],[0,0,0,0],[-60,-5,-5,20],[-10,0,0,0])
 tx(rail,f'{j+1:02}',380+j*495,996,32,15.4+j*.035,17.05,ORANGE,align='center')
n=nest(inside,'Guion a imágenes',rail,1340,540,15.10,17.05);anim(n,'pos',[15.10,16.20,17.05],[[1340,540],[1050,540],[500,540]],'linear')
# Close-up anchors expand into a series of consistent frames.
anchors=comp('V3 | Personaje y producto');atmosphere(anchors)
for j,i in enumerate([1,4]):
 n=tile(anchors,'Ancla '+str(i),shots[i],640+j*640,580,16.45,19.30,.8)
 pose(n,[16.45+j*.10,17.00+j*.10,18.50,19.30],[[640+j*640+500,620,750],[640+j*640,560,0],[640+j*640,560,0],[640+j*640,540,720]],[.73,.80,.80,.65],[10,0,0,15],[-20,0,0,-22])
 title(anchors,['Personaje.','Producto.'][j],640+j*640,1010,57,16.8+j*.60,19.10,ORANGE)
 # lock brackets: an actual graphic action, two independent corners.
 for k,pts in enumerate([[[432+j*640,256],[432+j*640,202],[486+j*640,202]],[[848+j*640,812],[848+j*640,866],[794+j*640,866]]]):
  draw(path(anchors,'Ancla esquina '+str(j)+str(k),pts,ORANGE,5,17.05+j*.6,19.10),17.05+j*.6,.35)
# Pull back reveals the same person across shots. Asymmetrical crop gives the film presence.
for j,i in enumerate([1,6,10,11,12]):
 n=tile(anchors,'Consistencia '+str(i),shots[i],230+j*365,590,19.0,20.83,.65)
 pose(n,[19.0+j*.05,19.60+j*.025,20.45,20.83],[[960,620,900+j*130],[230+j*365,612,0],[230+j*365,612,0],[230+j*365-1900,520,0]],[.45,.66,.66,.7],[20,0,0,0],[-15,0,0,15])
title(anchors,'En todos los planos.',960,226,100,19.16,20.74)
nest(inside,'Identidad continua',anchors,960,540,16.45,20.83)
# Models: image -> selected model -> detailed instructions, distinct transformations.
model=comp('V3 | Modelo y detalle');atmosphere(model)
for j,s in enumerate(['Cada plano.','Su modelo.']):title(model,s,525,448+j*166,143,20.56+j*.12,22.82,ORANGE if j else INK)
for j,s in enumerate(['Imagen','Vídeo','Movimiento']):
 xx=1070+j*340;cc=comp('V3 | Motor '+s,430,250);panel(cc,s,1,1,428,248);tx(cc,s,215,151,59,align='center')
 n=nest(model,'Elección '+s,cc,xx,700,20.62,23.05,.70)
 pose(n,[20.62+j*.07,21.24,21.65,22.23,23.05],[[xx,930,450],[xx,720,0],[xx,720,0],[1370+(j-1)*385,710,70],[2300+(j-1)*385,700,100]],[.6,.70,.70,.74,.7],[10,0,0,0,0],[-20,0,0,0,20])
n=tile(model,'Plano concreto',shots[4],1350,330,20.57,22.83,.60);enter(n,20.57,dy=120)
# Prompt macro: rows write and a travelling focus illuminates the active line.
prompt=comp('V3 | Detalle prompt',1220,760);panel(prompt,'Instrucciones',1,1,1218,758)
for j in range(9):
 tx(prompt,f'{j+1:02}',45,90+j*73,24,col=MUTED,bold=False)
 for k in range(3):
  n=rect(prompt,'Instrucción '+str(j)+str(k),118+k*355,64+j*73,180+((j+k)%4)*39,17,ORANGE if (j+k)%4==0 else '#676770',22.65+j*.045+k*.018,D,r=8)
  anim(n,'scale',[22.65+j*.045+k*.018,22.99+j*.045+k*.018],[[.01,1],[1,1]],'out')
n=nest(model,'Macro instrucciones',prompt,800,540,22.55,24.86,1)
pose(n,[22.55,23.05,24.28,24.86],[[880,700,550],[650,530,-60],[570,510,-100],[500,-700,-100]],[.82,1.02,1.10,1.12],[14,3,3,3],[-26,-8,-8,-8])
title(model,'Al detalle.',1540,592,92,22.90,24.68,ORANGE)
nest(inside,'Modelo adecuado',model,960,540,20.53,24.86)
# A large, tall moodboard allows an intentional macro -> overview camera move.
board=comp('V3 | Mapa 16 planos',3820,1740)
for j in range(16):
 x=248+(j%8)*466;y=420+(j//8)*820
 tile(board,'Fotograma '+str(j+1),shots[j+1],x,y,0,26.81,.90)
 live=card('V3 | Vivo '+str(j+1),j+1,480,800,26.81,D,True)
 tile(board,'Plano vivo '+str(j+1),live,x,y,26.81,D,.90)
 tx(board,f'{j+1:02}',x-197,y+384,26,col=ORANGE)
mapscene=comp('V3 | 03 Mapa a película');atmosphere(mapscene)
n=nest(mapscene,'Cámara mapa',board,960,1200,24.58,28.22,.95)
pose(n,[24.58,25.12,25.68,26.18,26.84,27.34,28.22],[[1900,980,0],[1880,940,0],[1140,560,0],[960,480,0],[960,480,0],[960,480,0],[3453,1215,0]],[.98,.98,.55,.445,.445,.445,1.5],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0])
title(mapscene,'El mapa completo.',960,185,88,24.75,25.20)
rect(mapscene,'Aprobar mapa',1420,870,360,105,ORANGE,26.03,26.84,r=28);tx(mapscene,'Animar',1600,940,43,26.03,26.84,BG,align='center')
cursor(mapscene,26.10,[[1800,1100],[1680,940],[1680,940],[1950,1160]],[26.1,26.5,26.61,26.82],26.87)
# A hero shot takes over from the grid, then opens into the editor.
livehero=card('V3 | Película protagonista',1,660,1100,27.98,D,True)
n=tile(mapscene,'Del mapa al resultado',livehero,960,540,28.20,30.15,.98)
pose(n,[28.20,28.43,29.60,30.15],[[960,540,0],[960,540,0],[960,540,0],[1370,485,100]],[.98,.98,.98,.72],[0,0,0,0],[0,0,0,-5])
for j in range(2):
 x=[588,1332][j];pts=[[x,335],[x,244],[x+(92 if j==0 else -92),244]] if j==0 else [[x,745],[x,836],[x-92,836]]
 draw(path(mapscene,'Control esquina '+str(j),pts,ORANGE,6,28.24,29.75),28.24,.28)
rect(mapscene,'Estado revisado',728,856,464,98,ORANGE,28.84,29.77,r=49);tx(mapscene,'Revisado',960,921,49,28.84,29.77,BG,align='center')
livehero['layers'][0]['sourceOffset']=2.67
# 4 Editor: native timeline closes gaps; same picture remains the anchor.
edit=comp('V3 | 04 Montaje');atmosphere(edit)
editor=comp('V3 | Editor nativo',1800,980);panel(editor,'Ventana',1,1,1798,978,'#131315',r=34)
wordmark(editor,225,86,42);tx(editor,'La máquina',1715,83,30,col=MUTED,align='right',bold=False)
path(editor,'Separación',[[35,126],[1765,126]],'#303035',2)
tx(editor,'El ritmo,',130,314,123,0,31.32);tx(editor,'resuelto.',130,454,123,0,31.32,col=ORANGE)
# Timeline: five object precomps hold thumbnail and waveform together.
for j,i in enumerate([1,4,10,11,12]):
 cc=comp('V3 | Fragmento '+str(i),205,300)
 rect(cc,'Clip',0,0,205,202,'#2A2A30',r=18);pic(cc,'Fotograma',f'maquina-{i:02}.jpg',102,102,114)
 for k in range(29):
  h=8+(k*17+j*11)%50;rect(cc,'Onda '+str(k),8+k*6.5,248-h/2,3,h,ORANGE,r=1)
 n=nest(editor,'Corte '+str(j),cc,229+j*233,734,30.00,36.73,1)
 anim(n,'pos',[30,30.62,31.08,31.46,35.96,36.73],[[229+j*245,810],[229+j*245,734],[229+j*245,734],[229+j*207,734],[229+j*207,734],[229+j*207,734]])
 # little scissors/gap markers disappear after the cut, causally.
 if j<4:
  rect(editor,'Silencio '+str(j),335+j*245,601,30,266,'#672C14',30.3,31.15,r=4,opacity=.65)
head=rect(editor,'Cabezal',146,584,3,305,INK,30.15,36.73,r=0);anim(head,'pos',[30.15,36.5],[[146,584],[1170,584]],'linear')
# The main picture always plays, with editorial captions as part of the demonstration.
output=comp('V3 | Salida subtitulada',660,1000)
for j,(a,b,i) in enumerate([(29.90,31.5,1),(31.5,32.85,10),(32.85,34.15,11),(34.15,35.7,12),(35.7,36.75,1)]):
 pic(output,'Toma '+str(j),f'maquina-{i:02}.mp4',330,500,660,a,b,offset=1.5)
for j,(a,b,s,size) in enumerate([(32.30,32.95,'palabra',103),(32.95,33.28,'por',107),(33.28,34.05,'palabra.',103),(34.05,34.90,'Tu estilo.',92),(34.90,35.75,'Tu marca.',94)]):
 n=tx(output,s,330,835,size,a,b,INK,align='center',track=-30);enter(n,a,dx=60 if j%2 else 0,dy=0 if j%2 else 55,d=.18)
 n.setdefault('effects',[]).append({'match':'ADBE Drop Shadow','props':[[[2],80],[[3],135],[[4],2],[[5],8]]})
film=tile(editor,'Película',output,1443,515,29.9,36.75,.70)
n=nest(edit,'Superficie editor',editor,960,540,29.90,36.85,1)
pose(n,[29.90,30.42,31.28,31.72,32.44,33.03,34.99,35.70,36.25,36.85],[[950,640,470],[960,540,20],[960,540,20],[1030,340,-390],[1030,340,-390],[590,540,-360],[590,540,-360],[960,540,0],[960,540,0],[-900,540,140]],[.9,.99,.99,1.02,1.02,1.01,1.01,.96,.96,.90],[12,1,1,4,4,0,0,0,0,0],[-20,-3,-3,-7,-7,5,5,0,0,20])
title(edit,'Sin pausas.',960,270,102,31.34,32.50)
# Publish state uses type as the focal change, over the reconstructed UI.
rect(edit,'Listo fondo',0,0,1920,1080,BG,35.95,36.8,r=0)
title(edit,'Listo.',960,635,246,35.95,36.80,ORANGE)
# 5 A single visual multiplies, then the crop transforms across formats.
variants=comp('V3 | 05 Versiones');atmosphere(variants)
title(variants,'Una idea.',960,252,144,36.75,38.0)
title(variants,'Más versiones.',960,252,144,38.0,40.0,ORANGE)
for j,i in enumerate([10,1,12]):
 n=tile(variants,'Rama '+str(i),shots[i],480+j*480,657,36.73,40.1,.76)
 pose(n,[36.73+j*.06,37.34+j*.08,38.1,39.70,40.1],[[960,650,350+j*200],[480+j*480,646,0],[480+j*480,646,0],[480+j*480,646,0],[480+j*480-1950,646,0]],[.5,.76,.76,.76,.76],[10,0,0,0,0],[-25,-8+j*8,-8+j*8,-8+j*8,30])
for j,(txt,t) in enumerate([('Gancho',39.9),('Ángulo',40.60)]):
 title(variants,txt,540,581,174,t,t+(.72 if j else .8))
 n=tile(variants,'Alternativa '+txt,shots[[10,6][j]],1370,540,t,t+(.72 if j else .8),.94);enter(n,t,dx=150,dy=0,d=.3)
# Same footage, crop reshaped by mask path keys, paired with exact format labels.
formats=comp('V3 | Formatos',1400,960)
pic(formats,'Imagen común','maquina-01.jpg',700,795,1400)
fmt=nest(variants,'Encuadre adaptable',formats,1280,540,41.32,42.58,.73)
fmt['morphMask']={'times':[41.32,41.62,41.93,42.24],'sizes':[[520,924],[880,880],[1360,765],[1360,765]],'center':[700,480],'round':30}
for a,b,s in [(41.32,41.65,'9:16'),(41.65,41.97,'1:1'),(41.97,42.58,'16:9')]:tx(variants,s,320,575,134,a,b,ORANGE,align='center')
# Ending: bold identity, orange process/idea contrast, a short resolved brand pose.
close=comp('V3 | 06 Firma');bg(close)
title(close,'Tú, la idea.',960,610,170,42.48,43.52)
title(close,'Yo, el proceso.',960,610,161,43.52,44.96,ORANGE)
wm=wordmark(close,960,604,174,44.96,D);enter(wm,44.96,dy=75,d=.36)
# The orange punctuation in the logo is the final stop, rather than an extra tag line.
master=comp(S['master']);bg(master)
for name,cc,a,b in [('Idea e interfaz',intro,0,9.68),('Interior',inside,9.48,24.85),('Mapa y resultado',mapscene,24.58,30.15),('Montaje',edit,29.90,36.85),('Versiones',variants,36.73,42.58),('Firma',close,42.48,D)]:
 n=nest(master,name,cc,960,540,a,b)
 # Very short luminance-safe handoff; choreography supplies the transition.
 if a>0:anim(n,'opacity',[a,a+.12],[0,1],'linear')
node(master,'audio','Diseño sonoro V3',0,0,0,D,asset='v3/Mix.wav')
# Enforce half-open, frame-aligned boundaries and keys.
for c in S['comps'].values():
 for n in c['layers']:
  n['from']=round(max(0,n['from'])*F)/F;n['to']=min(D,round(n['to']*F)/F)
  assert n['to']>n['from'],n
  for k in n['anim'].values():
   assert len(k['times'])==len(k['values']),n['name']
   assert all(a<b for a,b in zip(k['times'],k['times'][1:])),n['name']
(R/'src/v3/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('V3',len(S['comps']),'comps',sum(len(c['layers']) for c in S['comps'].values()),'layers',D,'seconds')
