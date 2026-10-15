"""Current user direction: unobtrusive captions; objects transform into evidence.
Run after design.py. All animation remains native AE keys and layers.
"""
exec((__import__('pathlib').Path(__file__).parent/'design.py').read_text())

def clean_bg(c):
 node(c,'gradient','Luz de escenario',(540,960),w=1080,h=1920,anchor=[540,960],color='#392215',endColor='#08090c',center=[560,820],radius=1150)
def cursor(c,n,x,y,a,b,z=0):
 p=node(c,'path',n,(x,y),a,b,points=[[0,0],[0,92],[23,71],[43,112],[58,104],[38,65],[72,65]],closed=True,color=CREAM,stroke='#191610',strokeWidth=4,shadow=[0,4,5,'#000000',.55]);return three(p,z)
def camera(c,frames,poses):c['camera']=focus_camera(frames,poses)

# Credits: one material object opens into a field, then the words form a depth tunnel.
c=comp('MG - Creditos',196);clean_bg(c)
camera(c,[0,20,67,101,138,174,196],[[540,940,-1050],[540,960,-1900],[540,960,-1900],[540,975,-1700],[540,975,-1650],[540,975,-1550],[540,975,-1500]])
for i,(x,y,z,w) in enumerate([(180,640,120,360),(880,650,240,410),(900,1190,160,380),(220,1210,210,270),(120,930,380,330),(805,955,480,300)]):
 n=three(media(c,'Ficha en profundidad '+str(i),'credit-token.png',x,y,w,8+i*3,b=114),z)
 p=n['pos'].copy();enter(n,8+i*3,17,'y',240,6)
 anim(n,'pos',[8+i*3,28+i*3,65,103+i],[[x,y+240,z],p,p,[540+(x-540)*2,y-250,z-500]])
 anim(n,'rot',[8+i*3,72,108+i],[-18+i*12,i*7,i*7+52])
 anim(n,'opacity',[8+i*3,25+i*3,88+i*2,110+i],[0,.85,.85,0])
n=three(media(c,'Macro de credito','credit-token.png',540,912,980,0,b=89),-180)
anim(n,'pos',[0,19,61,89],[[540,1040,-180],[740,895,-180],[740,895,-180],[1520,895,-400]])
anim(n,'scale',[0,19,61,89],[[1.0,1.0],[.70,.70],[.70,.70],[.36,.36]])
anim(n,'rot',[0,20,61,89],[-24,7,7,37])
kinetic(c,'créditos',423,993,165,CREAM,23,'x',2)
for n in c['layers']:
 if 'créditos |' in n['name']:n['to']=94;three(n,-230)
for i in range(4):
 yy=670+i*170
 n=three(txt(c,'Generaciones plano '+str(i),'generaciones',540,yy,137,CREAM if i==1 else '#c9975c',90+i*10,b=196,opacity=1-abs(i-1)*.24),150+i*300)
 enter(n,90+i*10,14,'y',100,8)
 anim(n,'pos',[90+i*10,111+i*10,196],[[540,yy+100,150+i*300],[540,yy,150+i*300],[540,yy,150+i*300-250]])
 n['glow']=7

# Time: text and objects pass each other in depth; 'perdido' is the spoken payoff.
c=comp('MG - Tiempo',112);clean_bg(c)
camera(c,[0,18,43,64,90,112],[[540,960,-1080],[540,960,-1720],[540,960,-1720],[540,960,-2120],[540,960,-1600],[540,960,-1540]])
n=three(media(c,'Reloj protagonista','hourglass.png',280,870,600,0,b=86),-90)
anim(n,'pos',[0,20,51,86],[[-420,870,-90],[270,870,-90],[270,870,-90],[270,1800,-90]])
anim(n,'rot',[0,22,53,86],[-26,-7,-7,19])
n=three(txt(c,'Tiempo','tiempo',693,785,155,CREAM,10,b=87),30);enter(n,10,16,'x',270,12)
n=three(media(c,'Dinero entra del fondo','credit-token.png',822,1140,660,27,b=87),130)
anim(n,'pos',[27,47,69,87],[[822,1140,700],[822,1140,130],[822,1140,130],[1822,1140,-120]])
anim(n,'rot',[27,50,87],[-22,14,46]);anim(n,'opacity',[27,39],[0,1])
n=three(txt(c,'Dinero','dinero',437,1042,163,CREAM,29,b=87,shadow=[0,4,10,'#000000',.95]),-190);enter(n,29,15,'x',-360,12)
kinetic(c,'perdido',540,1008,170,CREAM,80,'y',1)
for n in c['layers']:
 if 'perdido |' in n['name']:three(n,-50)

# Reusable post scaffolding, with real media. No editorial headings or disclaimer text.
for key,handle in [('kurt','notkurtgodel'),('elliot','notelliotkay')]:
 c=comp('PUBLICACION - '+key,480,900,1210)
 rect(c,'Borde de publicacion',0,0,900,1210,'#e9e7e2',round=19)
 rect(c,'Superficie negra',5,5,890,1200,'#101316',round=15)
 media(c,'Avatar original',key+'-avatar.png',95,86,103)
 txt(c,'Usuario editable',handle,174,80,38,CREAM,align='left')
 txt(c,'Seguidores etiqueta','seguidores',174,130,25,DIM,align='left')
 for i in range(3):ellipse(c,'Menu '+str(i),817+i*13,80,6,col=CREAM)
 # The original reel screenshot itself retains the verifiable view count.
 media(c,'Reel original y visitas',key+'-proof-0.png',450,656,626)
 path(c,'Separador inferior',[[54,1168],[846,1168]],'#44484c',2)

c=comp('MG - Cuentas',349);clean_bg(c)
camera(c,[0,20,46,68,102,117,139,171,195,239,266,294,327,349],[[540,930,-1290],[540,960,-1800],[540,960,-1800],[540,960,-2070],[540,960,-2070],[1300,920,-2920],[2180,960,-1800],[2180,960,-1800],[2180,960,-2070],[2180,960,-2070],[2180,960,-2320],[1360,960,-4300],[1360,960,-4300],[1360,960,-3900]])
for key,x,a,followers,views in [('kurt',540,0,'83,3 mil','7,7 M'),('elliot',2180,121,'13,5 mil','4,9 M')]:
 # Post grows out of the initial number; its independent angle settles in depth.
 n=three(nested(c,'Publicacion emerge '+key,'PUBLICACION - '+key,x,845,.78,a+38),190)
 anim(n,'opacity',[a+38,a+54],[0,1]);anim(n,'scale',[a+38,a+59,a+100],[[.27,.27],[.78,.78],[.78,.78]])
 anim(n,'ry',[a+38,a+67,277,310],[-24 if key=='kurt' else 24,-3 if key=='kurt' else 3,-3 if key=='kurt' else 3,-12 if key=='kurt' else 12])
 anim(n,'pos',[a+38,a+64,277],[[x,1010,440],[x,845,190],[x,845,190]])
 # One native number changes scale and position into the profile header.
 n=three(txt(c,'Seguidores protagonistas '+key,followers,x,931,196,CREAM,a),-170)
 anim(n,'pos',[a,a+14,a+43,a+65],[[x,1070,-170],[x,931,-170],[x,931,-170],[x+120,512,0]])
 anim(n,'scale',[a,a+15,a+43,a+65],[[.75,.75],[1,1],[1,1],[.265,.265]])
 anim(n,'blur',[a,a+13],[12,0]);anim(n,'opacity',[a,a+5],[0,1])
 n=three(txt(c,'Seguidores unidad '+key,'seguidores',x,1012,51,CREAM,a+9,b=a+55),-169);enter(n,a+9,13,'y',60,7);anim(n,'opacity',[a+44,a+55],[1,0])
 # Selection frame references the cursor-led reveal in the supplied motion reference.
 n=three(rect(c,'Seleccion cifra '+key,x-414,745,828,232,None,a+8,a+50,stroke=AMBER,strokeWidth=3,round=3),-190)
 anim(n,'scale',[a+8,a+21,a+42,a+50],[[.02,1],[1,1],[1,1],[1,.01]])
 for j,(xx,yy) in enumerate([(x-414,745),(x+414,745),(x-414,977),(x+414,977)]):
  n=three(rect(c,'Ancla seleccion '+key+str(j),xx-6,yy-6,12,12,AMBER,a+15,a+47),-191)
 n=cursor(c,'Cursor '+key,x+550,1120,a+2,a+58,-230)
 anim(n,'pos',[a+2,a+19,a+39,a+58],[[x+550,1120,-230],[x+416,990,-230],[x+416,990,-230],[x+910,1210,-230]])
 # View count travels out of the original reel and becomes the next focal point.
 n=three(txt(c,'Visitas protagonistas '+key,views,x,1060,225,AMBER,a+57),-300)
 anim(n,'pos',[a+57,a+77,a+99,a+112],[[x,1130,170],[x,1015,-300],[x,1015,-300],[x-184,1229,190]])
 anim(n,'scale',[a+57,a+77,a+99,a+112],[[.24,.24],[1,1],[1,1],[.155,.155]])
 anim(n,'opacity',[a+57,a+65,a+105,a+113],[0,1,1,0]);n['shadow']=[0,4,20,'#000000',1]
 n=three(txt(c,'Unidad visitas '+key,'visitas en un reel',x,1112,41,CREAM,a+61,b=a+114),-300)
 enter(n,a+61,16,'y',60,7);anim(n,'opacity',[a+105,a+114],[1,0])
 # A fast line draws from the statistic into the original evidence.
 n=three(path(c,'Vinculo a evidencia '+key,[[x-270,1110],[x-270,1200],[x,1200]],AMBER,4,a+67,a+111,trim=[a+67,a+89]),-100)
kinetic(c,'consistencia',540,1205,110,CREAM,296,'y',1)

# The library is genuine; strip away all extra headline/categorisation layers.
c=S['comps']['MG - Comunidad'];c['layers']=[n for n in c['layers'] if n['name'] not in ['Etiqueta editorial','Orientacion profesional'] and not n['name'].startswith('CREA MEJOR.')]
S['comps']['MG - Sistemas']['layers']=[n for n in S['comps']['MG - Sistemas']['layers'] if n['name']!='Etiqueta editorial' and not n['name'].startswith('SISTEMAS |')]

# Real library surface, framed by AE; no invented promotional headings.
c=comp('OBJ - Biblioteca',320,940,880)
rect(c,'Fondo real de pagina',0,0,940,880,'#f5f4f0',round=16)
media(c,'Biblioteca original de Visual Hub','skool-cursos.png',470,440,1480)
c=comp('MG - Comunidad',145);clean_bg(c)
camera(c,[0,23,84,112,145],[[285,770,-1100],[540,920,-1880],[540,920,-1880],[640,1040,-1700],[645,1100,-1340]])
n=three(nested(c,'Pagina de comunidad real','OBJ - Biblioteca',540,885,.98),50)
anim(n,'ry',[0,25,104,145],[-16,-3,-3,9]);anim(n,'rx',[0,25,145],[6,0,-4]);enter(n,0,20,'y',110,8)

# A native 50-cell board, with discrete holds as in the supplied calendar reference.
steps=[(265,1),(271,5),(277,12),(283,24),(289,38),(297,50)]
c=comp('OBJ - Intentos',374,2100,2400)
for value in range(1,51):
 xx=210+((value-1)%5)*420;yy=120+((value-1)//5)*240
 ellipse(c,'Celda '+str(value),xx,yy,158,col=None,stroke='#71523a',strokeWidth=2,opacity=.65)
 txt(c,'Numero '+str(value),str(value),xx,yy+28,87,'#8b7866')
 for si,(f,v) in enumerate(steps):
  if v!=value:continue
  end=steps[si+1][0] if si+1<len(steps) else 341
  ellipse(c,'Intento seleccionado '+str(value),xx,yy,168,col=ORANGE,a=f,b=end)
  txt(c,'Intento blanco '+str(value),str(value),xx,yy+31,95,CREAM,f,end)

c=comp('MG - Sistemas',374);clean_bg(c)
camera(c,[0,23,66,94,141,174,204,243,264,374],[[540,960,-1130],[540,960,-1850],[540,960,-1850],[540,1990,-2360],[540,1990,-2180],[940,1990,-1470],[940,1990,-1470],[540,1990,-2300],[540,1990,-2300],[540,1990,-2300]])
for i,(asset,x,y,z,w) in enumerate([('curso-escala.png',150,960,220,510),('curso-masterclasses.png',930,965,280,510),('curso-maestria.png',540,900,-80,610)]):
 n=three(media(c,'Recurso real '+str(i),asset,x,y,w,0,b=104,shadow=[0,18,22,'#000000',.8]),z)
 enter(n,i*4,20,'y',160,8);anim(n,'ry',[0,23,65,102],[[-21,22,-12][i],[-7,9,0][i],[-7,9,0][i],[-18,18,0][i]])
kinetic(c,'plantillas',540,630,125,CREAM,1,'x',1)
for n in c['layers']:
 if n['name'].startswith('plantillas |'):n['to']=83
for i in range(3):
 x=140+i*400
 n=three(media(c,'Resultado generado '+str(i+1),'chef-'+str(i+1)+'.jpg',x,1990,360,78+i*6,b=265,shadow=[0,16,18,'#000000',.8]),[100,-30,100][i])
 enter(n,78+i*6,24,'y',300,12);anim(n,'ry',[78+i*6,108+i*6,174,243],[[-18,0,18][i],[-7,0,7][i],[-7,0,7][i],[-4,0,4][i]])
for i,x in enumerate([330,730]):
 n=three(path(c,'Conexion de identidad '+str(i),[[x,1990],[x+40,1990]],AMBER,5,99,265,trim=[99,124]),-55)
kinetic(c,'consistentes',540,635,113,CREAM,146,'y',1)
for n in c['layers']:
 if n['name'].startswith('consistentes |'):n['to']=213
kinetic(c,'realistas',540,635,113,CREAM,216,'x',1)
for n in c['layers']:
 if n['name'].startswith('realistas |'):n['to']=265
n=nested(c,'Tablero de intentos','OBJ - Intentos',540,935,1,265,341)
n['motionBlur']=False
anim(n,'anchor',[f for f,v in steps],[[210+((v-1)%5)*420,120+((v-1)//5)*240] for f,v in steps],'hold')
anim(n,'scale',[265,283,297,313,340],[[1.25,1.25],[1.25,1.25],[1.25,1.25],[2.7,2.7],[2.7,2.7]])
path(c,'Tachado ultimo intento',[[310,926],[770,926]],CREAM,12,314,341,trim=[314,329])
kinetic(c,'algo bueno',540,1030,139,CREAM,341,'y',1)

# Typographic brand/price without a box over the footage.
c=comp('MG - Marca',66);kinetic(c,'Visual Hub',540,1085,122,CREAM,0,'x',1)
for n in c['layers']:n['shadow']=[0,3,9,'#000000',.85]
c=comp('MG - Precio',121)
txt(c,'Marca sobre chaqueta','Visual Hub',540,1118,52,'#211b16',0)
n=txt(c,'Precio editable','39',500,1332,218,'#241b12',43);enter(n,43,13,'y',85,4)
n=txt(c,'Moneda editable','$',674,1234,91,'#241b12',43);enter(n,43,13,'y',85,4)
for n in c['layers']:n['shadow']=[0,1,3,'#fff6e9',.45]

# Rewrite captions as small centered phrases with short, varied, single-axis entries.
c=S['comps'][S['master']];c['layers']=[n for n in c['layers'] if not n['name'].startswith('SUB ') and n['name']!='ESCENA - live']
caps=json.load(open(R/'analysis/captions.json'));layout=[]
ys={1:970,2:910,3:930,4:1130,5:1210,6:1110,7:1110,9:1190,10:1090,11:1110,12:960,13:1170,14:1190}
for ci,cap in enumerate(caps):
 a,b=cap['from'],cap['to'];phrase=' '.join(w['text'] for w in cap['words'])
 if cap['clip']==8 or a>=3279:continue
 if cap['clip']==10 and a>=2125:continue
 onmg=any(e['from']<=a<e['to'] for k,e in S['events'].items() if k in ['credits','accounts','community','system'])
 size={'IA':96,'misma persona':87,'cara':98,'voz':98,'consistente':89,'constantemente':82,'prueba y error':87}.get(phrase,73)
 if word_width(phrase,size)>842:size=math.floor(size*842/word_width(phrase,size))
 y=1368 if onmg else ys.get(cap['clip'],1160)
 # On the chef's bright coat, use dark ink rather than a dark backdrop.
 ink=cap['clip'] in [5,14] and not onmg
 col='#171a1a' if ink else CREAM
 axis=directions[ci%len(directions)];dx=-48 if axis=='x-' else 48 if axis=='x+' else 0;dy=35 if axis=='y' else 0
 widths=[word_width(w['text'],size) for w in cap['words']];space=ImageFont.truetype(str(A/'Display-Bold.otf'),size).getlength(' ')-size*.028
 x=(1080-sum(widths)-space*(len(widths)-1))/2
 for wi,(w,ww) in enumerate(zip(cap['words'],widths)):
  wa=a+wi*2
  if wa>=b:wa=a
  n=txt(c,f'SUB {ci:02d}.{wi} | '+w['text'],w['text'],x+ww/2,y,size,col,wa,b,
        shadow=[0,2,4,'#ffffff',.5] if ink else [0,3,7,'#000000',.94],textStroke=['#f7f2e8',.5] if ink else ['#141414',1.5])
  p=n['pos'];anim(n,'pos',[wa,min(wa+7,b)],[[p[0]+dx,p[1]+dy],p]);anim(n,'opacity',[wa,min(wa+3,b)],[.5,1])
  layout.append({'text':w['text'],'from':wa,'to':b,'left':x,'right':x+ww,'top':y-size,'bottom':y+size*.29,'direction':axis,'fontSize':size,'darkInk':ink});x+=ww+space

# Remove obsolete objects from the final construction manifest; no old motions used.
for k in ['OBJ - Generar','PRUEBA - kurt','PRUEBA - elliot','MG - Directo','OBJ - Plantilla','OBJ - Resultado']:S['comps'].pop(k,None)
S['events'].pop('live',None)
(R/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'analysis/caption-layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2))
(R/'analysis/motion-map.json').write_text(json.dumps({'fps':48,'events':S['events'],'feedback':'Sin fondos en subtitulos. Sin titulos explicativos ni notas. Transformacion de cifra a perfil y reel; planos de profundidad y camara.','layers':sum(len(c['layers']) for c in S['comps'].values())},ensure_ascii=False,indent=2))
print('Feedback applied:',len(S['comps']),'comps')
