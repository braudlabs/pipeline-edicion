from pathlib import Path
from PIL import ImageFont
import json, math
R=Path(__file__).resolve().parent
comps={}
def comp(n,w=720,h=1280):
 c={'name':n,'width':w,'height':h,'frames':330,'layers':[]};comps[n]=c;return c

def node(c,n,t,x=0,y=0,**kw):
 d={'name':n,'type':t,'pos':[x,y],'anchor':[0,0],'from':0,'to':330,**kw};c['layers'].append(d);return d

def anim(n,p,frames,values,ease='smooth'):
 n.setdefault('anim',{})[p]={'frames':frames,'values':values,'ease':ease};return n

def text(c,n,s,x,y,size=42,font='bolditalic',color='#f0edef',track=-25,**kw):
 return node(c,n,'text',x,y,text=s,size=size,font=font,color=color,track=track,**kw)
def rect(c,n,x,y,w,h,color,**kw):return node(c,n,'rect',x,y,w=w,h=h,color=color,**kw)
def ellipse(c,n,x,y,w,h,color,**kw):return node(c,n,'ellipse',x,y,w=w,h=h,color=color,**kw)
def bg(c,a='#1a002e',b='#000000',radius=700,center=None):return node(c,'Fondo radial','gradient',0,0,w=c['width'],h=c['height'],color=a,endColor=b,radius=radius,center=center or [c['width']/2,c['height']/2])
def sub(c,n,src,x=0,y=0,**kw):return node(c,n,'comp',x,y,source=src,**kw)
def rise(n,at,until,dy=40,blur=5):
 x,y=n['pos'];n['from']=at;anim(n,'pos',[at,until],[[x,y+dy],[x,y]],'out');anim(n,'opacity',[at,at+3],[0,1],'linear');anim(n,'blur',[at,until],[blur,0],'out');return n

# All times below are absolute source-frame positions; every comp starts at zero.
a=comp('01 - Succes')
bg(a,'#1b0035','#050207',700,[360,650])
sphere=ellipse(a,'Esfera violeta',-105,985,1300,690,'#13002b',shadow=[0,15,20,'#000000',.8])
anim(sphere,'pos',[0,8,27],[[-80,530],[-170,975],[-160,1005]],'out');anim(sphere,'scale',[0,9,27],[[1,1.45],[1,1.04],[1,1]],'out')
r=rect(a,'Selección violeta',146,534,432,125,'#9419b4',glow=15,glowColor='#a509dd')
anim(r,'scale',[0,6,14],[[0,1],[.28,1],[1,1]],'smooth');r['from']=3
rr=rect(a,'Borde selección azul',146,522,432,13,'#3400d0');anim(rr,'scale',[0,6,14],[[0,1],[.28,1],[1,1]],'smooth');rr['from']=3
n=text(a,'succes — palabra editable','succes',148,642,142,'bold',track=-60,glow=17)
rise(n,2,12,85,12)
for word,x,y,st in [('is',267,706,12),('made',307,712,15),('by',432,738,16)]:
 n=text(a,'Subtítulo '+word,word,x,y,48,'italic',color='#c0b5c7',track=-45);rise(n,st,st+9,35,4)
# Cursor follows selection right edge, then settles.
cur=node(a,'Cursor','path',146,588,points=[[0,0],[0,49],[11,38],[23,57],[31,52],[20,34],[37,33]],closed=True,color='#070509',stroke='#d2c9d8',strokeWidth=2)
anim(cur,'pos',[0,5,14,23],[[135,588],[238,606],[580,654],[580,654]],'out')
# Foreground sphere occludes arriving lower caption, as in reference.
a['layers'].remove(sphere);a['layers'].append(sphere)

b=comp('02 - Action');bg(b,'#1c0033','#040107',690,[348,605])
for name,x,y,w,h,alpha,rot,bl in [('Superior',20,0,240,245,.18,-16,1),('Derecha',682,345,155,150,.6,10,.2),('Abajo',-35,710,190,170,.7,-25,4),('Inferior derecha',475,910,260,235,.32,0,.7)]:
 im=node(b,'Cerebro '+name,'image',x,y,asset='brain.png',w=w,h=h,opacity=alpha,rot=rot,blur=bl)
 anim(im,'pos',[30,56],[[x,y-8],[x+4,y]],'linear')
sp=ellipse(b,'Esfera primer plano',-340,1540,2040,1720,'#120027')
anim(sp,'pos',[30,56],[[-340,1530],[-340,1550]],'linear')
# Independent letters preserve the asynchronous reveal.
widths=[76,72,48,26,76,73];xs=[];v=191
for w in widths:xs.append(v);v+=w
for i,ch in enumerate('action'):
 n=text(b,'action - '+str(i+1),ch,xs[i],657,140,'bolditalic',color=('#ae00df' if i not in [3,4] else '#d377e3'),track=-40,glow=23,glowColor='#ae00e7')
 st=[34,36,31,35,33,32][i];rise(n,st,40,30,5)
# Window closes using native linear wipes, not text squashing.

w=comp('03 - Watch artwork',720,720)
im=node(w,'Reloj de bolsillo — recurso','image',101,204,asset='watch.png',w=211,h=285,opacity=.68,blur=.6,glow=6,glowColor='#7333ab')
anim(im,'pos',[60,72],[[65,229],[101,204]],'out');anim(im,'opacity',[60,67],[0,.68],'linear');anim(im,'rot',[60,74],[-12,0],'out')
for name,s,x,y,sz,st in [('not','not',292,326,42,65),('by','by',358,326,43,68),('waiting','waiting',414,326,43,71),('for the','for the',357,357,42,75)]:
 n=text(w,name,s,x,y,sz,font='italic',track=-35,glow=18,chroma=2);rise(n,st,st+7,25,4)
h=rect(w,'Selección perfect',323,365,267,64,'#b312cf',glow=19,glowColor='#b90fcd');h['from']=80;anim(h,'scale',[80,86],[[0,1],[1,1]],'out')
p=text(w,'perfect — palabra editable','perfect',324,421,80,track=-47,glow=17,chroma=2);rise(p,80,88,38,5)
d=text(w,'day','day',477,465,43,font='italic',track=-45,glow=18);rise(d,87,94,30,5)

watchscene=comp('03a - Watch scene');bg(watchscene,'#20071e','#000000',510,[360,640]);sub(watchscene,'Reloj y tipografía','03 - Watch artwork',0,280)
photo=comp('03b - Square publication',720,740)
bg(photo,'#270d26','#050306',700,[360,360])
sub(photo,'Arte ampliado','03 - Watch artwork',360,360,anchor=[360,360],scale=[1.21,1.21])
post=comp('04 - Instagram post',756,990)
# Transparent UI, gray stage behind, artwork centered in square.
sub(post,'Publicación - arte reutilizado','03b - Square publication',18,85,round=13)
text(post,'Usuario','burzaev_studio',24,56,35,'bold','#08080a',-40)
text(post,'Más','···',648,58,45,'bold','#08080a',0)
# Rounded outer image edge only, no screenshot flattening.
# UI outlines use compact paths and native vectors.
node(post,'Me gusta','path',31,824,points=[[20,30],[0,12],[0,3],[7,-3],[15,-3],[20,3],[25,-3],[33,-3],[40,3],[40,12]],closed=True,stroke='#16171b',strokeWidth=2.5)
text(post,'Likes','6',80,855,42,'regular','#111215',0)
node(post,'Comentarios','path',129,823,points=[[33,32],[23,28],[15,31],[5,28],[0,22],[-2,12],[1,4],[8,-2],[17,-4],[26,-1],[32,6],[33,17],[31,23]],closed=True,stroke='#16171b',strokeWidth=2.5)
text(post,'Comentarios total','0',173,855,40,'regular','#111215',0)
node(post,'Compartir','path',215,823,points=[[0,0],[40,0],[15,36],[12,15],[40,0],[12,15]],closed=False,stroke='#111215',strokeWidth=2.5)
text(post,'Compartidos total','0',263,855,40,'regular','#111215',0)
text(post,'Nombre del autor','Burzaev_studio',30,911,32,'bold','#08090c',-35)
# One readable text layer per typing state, each phrase is editable.
phrase='there will always be another reason'
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',32)
starts=[151,155,159,168,173,181]
for i,word in enumerate(phrase.split()):
 prefix=' '.join(phrase.split()[:i]);x=274+font.getlength(prefix+(' ' if prefix else ''))-len(prefix)*.25
 y=911
 if x+font.getlength(word)>716:x=30;y=950
 n=text(post,'Pie - '+word,word,x,y,32,'regular','#0b0b0d',-8);n['from']=starts[i]

ig=comp('05 - Instagram camera');bg(ig,'#c8c8c8','#7e7e7e',920,[352,650])
p=sub(ig,'Plano publicación 3D','04 - Instagram post',360,640,anchor=[378,445],threeD=True)
anim(p,'scale',[137,149,155,174,201,213],[[1.54,1.54],[.827,.827],[.827,.827],[1.01,1.01],[1.01,1.01],[1.05,1.05]],'smooth')
anim(p,'pos',[137,149,155,174,201,213],[[360,640],[360,633],[360,633],[362,392],[362,392],[375,376]],'smooth')
anim(p,'ry',[137,150,155,174,201,213],[0,0,0,18,18,0],'smooth')
anim(p,'rx',[137,150,155,174,201,213],[0,0,0,3,3,0],'smooth')

# Calendar world: genuine editable grid and dates; same tracked anchor in both engines.
cal=comp('06 - Calendar board',2200,2100)
# Reference date progression, read from decoded frames (one meaningful target/date).
dates=[(215,1),(219,2),(223,3),(227,4),(231,5),(235,6),(239,7),(242,9),(245,10),(248,11),(251,12),(253,13),(255,14),(257,15),(259,16),(261,17),(263,18),(265,19),(267,20),(269,21),(271,22),(273,24),(275,25),(277,26),(279,27),(281,28),(283,29),(285,30),(287,32)]
# Coordinates day 1 is second column; this reproduces neighbors 7/8/9 below it.
def xy(day):return [150+(day%7)*255,400+(day//7)*300]
for row in range(7):
 node(cal,'Línea horizontal '+str(row),'path',0,250+row*300,points=[[0,0],[2140,0]],closed=False,stroke='#292a2b',strokeWidth=1,opacity=.22)
for col in range(8):
 node(cal,'Línea vertical '+str(col),'path',22+col*255,240,points=[[0,0],[0,1750]],closed=False,stroke='#101113',strokeWidth=1,opacity=.24)
for i in range(1,33):
 x,y=xy(i);at=next((t for t,d in dates if d==i),0);end=next((t for t,d in dates if d>i),330)
 circ=ellipse(cal,'Día activo '+str(i),x,y,114,120,'#d9dddd' if i==1 else '#069d0e' if i==32 else '#f4070f',glow=24,glowColor='#a2bebd' if i==1 else '#118620' if i==32 else '#d61b16')
 circ['from']=at;circ['to']=end if any(d==i for t,d in dates) else 0
 n=text(cal,'Fecha '+str(i),str(i) if i<32 else 'now',x,y+29,88 if i<32 else 54,'light' if i<32 else 'regular','#d8d9d6',track=-15,align='center',glow=20,chroma=2)
 if i==1:
  nt=text(cal,'Uno negro activo','1',x,y+29,88,'regular','#050708',track=-15,align='center');nt['from']=215;nt['to']=219
cs=comp('07 - Calendar camera');rect(cs,'Negro',0,0,720,1280,'#000000')
world=sub(cs,'Tablero y fechas — plano 3D','06 - Calendar board',383,616,anchor=xy(1),threeD=True,ry=12,rx=-4,rot=4)
# Source date changes are discrete holds, confirmed in every decoded frame.
anim(world,'anchor',[t for t,d in dates]+[299,313],[xy(d) for t,d in dates]+[xy(32),xy(32)],'hold')
anim(world,'rot',[215,235,260,290,329],[2,4,5,5,5],'linear')
anim(world,'pos',[215,297,311,329],[[383,616],[383,616],[383,411],[383,411]],'smooth')
anim(world,'blur',[215,295,305,329],[.6,.6,7,7],'smooth')
# Cinematic focus envelope: dim outside the central rows, matching source.
rect(cs,'Sombra borde superior',-100,-500,920,660,'#000000',opacity=.92,blur=95)
rect(cs,'Sombra inferior',-100,875,920,1000,'#000000',opacity=.8,blur=100)
for word,x,at in [('You',20,214),("don’t",162,217),('start',330,220),('tomorrow',466,223)]:
 n=text(cs,'Titular '+word,word,x,376,67,'regular',track=-40,glow=20,chroma=2);rise(n,at,at+7,45,5);n['to']=239
 anim(n,'pos',[at,at+7,235,239],[[x,421],[x,376],[x,376],[x,145]],'out')
# Closing typography anchored to screen; overshoot and chromatic edges.
for s,sz,y,at,co in [('you',112,486,301,'#efeff0'),('start',160,592,310,'#efeff0'),('now',202,712,316,'#65257c')]:
 n=text(cs,'Cierre '+s,s,382,y,sz,'bold',co,-55,align='center',glow=12,chroma=4)
 rise(n,at,at+10,230,10);anim(n,'scale',[at,at+9,at+13],[[.86,.86],[1.035,1.035],[1,1]],'out')

master=comp('REPLICA - MASTER')
rect(master,'Negro base',0,0,720,1280,'#000000')
n=sub(master,'01 Succes','01 - Succes');n['to']=30
# Watch black frame underneath shutter transition.
n=sub(master,'03 Watch','03a - Watch scene',0,0);n['from']=56;n['to']=138
n=sub(master,'02 Action','02 - Action');n['from']=30;n['to']=67;anim(n,'wipe',[55,62,67],[0,92,100],'smooth')
n=sub(master,'04 Instagram','05 - Instagram camera');n['from']=138;n['to']=215
n=sub(master,'05 Calendar','07 - Calendar camera');n['from']=215
# Sparse scan lines across the full film, native single shape group in AE.
node(master,'Textura líneas CRT','scanlines',0,0,w=720,h=1280,color='#000000',opacity=.075)
for nn in post['layers']:
 if nn['name'] in ['Me gusta','Likes','Comentarios','Comentarios total','Compartir','Compartidos total']:nn['pos'][1]+=22
for cc in comps.values():
 for nn in cc['layers']:
  if nn['type']=='text':
   nn.setdefault('blur',.8)
   if 'blur' in nn.get('anim',{}):nn['anim']['blur']['values'][-1]=.8
finished=comp('REPLICA - FINAL')
sub(finished,'Acabado óptico - editable','REPLICA - MASTER',blur=.55)
# File metadata and semantic map.
spec={'fps':30,'width':720,'height':1280,'frames':330,'master':finished['name'],'comps':comps,'dateTargets':dates}
(R/'remotion/src/design.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2))
(R/'analysis/motion-map.json').write_text(json.dumps({'cuts':[30,138,214],'actionShutter':[55,67],'watchTextEntries':[65,68,71,75,80,87],'postCameraKeys':[137,149,155,174,201,213],'calendar':dates,'closingEntries':[301,310,316],'assetDifferences':['Generated replacement pocket watch','Generated replacement brain with lightning'],'font':'Arial / Arial Bold / Arial Italic / Arial Bold Italic, manually tracked to reference'},ensure_ascii=False,indent=2))
(R/'BRIEF.md').write_text('''# Réplica de referencia 96c1 — comparación de motores\n\nObjetivo: reconstruir los 330 fotogramas (11 s) de la referencia de Pinterest en Remotion y Adobe After Effects. Formato nativo: 720 × 1280, 30 fps. Audio común extraído de la referencia, exclusivamente para esta comparación local.\n\n## Diseño y movimiento\n- “succes” conserva la grafía visible original, selección violeta y cursor.\n- Esfera violeta, cerebros con rayo, entrada de letras de “action”, cierre en persiana.\n- Reloj mecánico, texto “not by waiting for the perfect day”, selección y halo.\n- La misma composición anidada en una publicación de Instagram, cámara con perspectiva y pie progresivo.\n- Calendario nativo con fechas editables, recorrido 1–31/now, cierre “you start now”.\n\n## Comparación justa\nAmbas versiones usan el mismo archivo de diseño, recursos, dimensiones, fotogramas clave y audio. Remotion renderiza React/SVG/CSS con muestreo temporal; AE utiliza composiciones, texto, formas, cámara 3D, efectos y claves nativos. Ningún vídeo renderizado por Remotion se importa al AEP. No se utiliza el vídeo original como fondo ni como gráfico.\n\n## Diferencias conocidas\nLos originales separados del reloj y el cerebro no están disponibles. Se han generado sustitutos compartidos por ambos proyectos. Arial aproxima la tipografía visible; el bloom, la perspectiva y el desenfoque pueden variar entre motores. No es una copia píxel a píxel.\n''')
print(len(comps),'compositions',sum(len(c['layers']) for c in comps.values()),'semantic layers')
