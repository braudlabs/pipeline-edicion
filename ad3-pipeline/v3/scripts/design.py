from pathlib import Path
import json,math,copy,subprocess,shutil
import numpy as np
V=Path(__file__).resolve().parents[1];A=V/'assets';F=48;D=2250
exec(compile((V.parent/'scripts/helpers.py').read_text().split('def photo_obj')[0],__file__,'exec'))
A=V/'assets';S={'fps':48,'master':'AD3 - FINAL V3','comps':{},'events':{}}
INK='#191a19';PAPER='#d5d2c7';WHITE='#eeece2';YELLOW='#e5ed52';BLACK='#111117'
for i,k in [(2,3),(3,2),(7,1)]:shutil.copy2(V/f'analysis/seleccion/{i}-{k}.jpg',A/f'Foto-{i}.jpg')
assets={i:next(p.name for p in A.glob(f'{i:02d}-*.jpg') if not p.name.endswith('frente.jpg')) for i in [1,2,3,5,7,8,9,10]};assets.update({i:f'Foto-{i}.jpg' for i in [2,3,7]})
def paper(c,dark=False):
 node(c,'gradient','Fondo editorial',(540,960),w=1080,h=1920,anchor=[540,960],color='#20202a' if dark else '#deddd2',endColor=BLACK if dark else '#bab8af',center=[460,710],radius=1400,noise=1.05)
def oval(c,n,x,y,w,h=None,color=WHITE,sw=3,a=0,b=None,trim=None):return ellipse(c,n,x,y,w,h,col=None,a=a,b=b,stroke=color,strokeWidth=sw,trim=trim)
def photo(i):return 'FOTO V3 - '+str(i)
def portrait(i):return 'RETRATO V3 - '+str(i)
for i in assets:
 c=comp(photo(i),D);media(c,'Fotografia sustituible',assets[i],540,960,1080)
 c=comp(portrait(i),D,800,800);media(c,'Retrato sustituible',assets[i],400,500 if i in [2,3] else 440,800,tint=[INK,WHITE,100])
# Actual voice envelope, designed as a fine editorial trace.
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(V.parent/'assets/Voz-Montada.wav'),'-t','14.5','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
pks=np.array([np.sqrt(np.mean(z*z)) for z in np.array_split(x,120)]);pks=np.maximum(1,pks/max(pks)*42)
for dark in [False,True]:
 c=comp('ONDA V3 - '+str(dark),D,860,130);col=WHITE if dark else INK
 pts=[[12+j*7,65-float(v)] for j,v in enumerate(pks)]+[[12+j*7,65+float(v)] for j,v in reversed(list(enumerate(pks)))];node(c,'path','Forma de la voz original',points=pts,closed=True,color=col)
# Three genuinely different visual studies, before motion construction.
c=comp('ESTUDIO A - Tipografia',1);paper(c)
txt(c,'Hasta los','Hasta los',98,430,66,INK,align='left',font='editorial')
txt(c,'Cortes','cortes',75,655,225,INK,align='left',font='serifitalic')
for i,src in enumerate([2,3,7]):nested(c,'Pieza '+str(i),photo(src),255+i*285,945,.245)
txt(c,'Ensamblan','se ensamblan',95,1350,104,INK,align='left',font='editorial')
rect(c,'Subrayado',91,1415,875,100,YELLOW);txt(c,'Automaticamente','automáticamente',104,1495,97,INK,align='left',font='serifitalic')
c=comp('ESTUDIO B - Publicacion',1);paper(c)
txt(c,'Titular 1','Se ensambla',98,565,118,INK,align='left',font='editorial');txt(c,'Titular 2','solo.',83,797,265,INK,align='left',font='serifitalic')
path(c,'Regla',[[94,860],[986,860]],INK,2)
nested(c,'Retrato',portrait(2),340,1150,.58,circleClip=True)
txt(c,'Cortes','Cortes',627,960,67,INK,align='left',font='editorial');nested(c,'Voz','ONDA V3 - False',778,1060,.34)
rect(c,'Marcador',613,1141,345,91,YELLOW);txt(c,'Subtitulos','Subtítulos',627,1211,63,INK,align='left',font='serifitalic')
path(c,'Rule 2',[[628,1270],[960,1270]],INK,1)
c=comp('ESTUDIO C - Conexion',1);paper(c,True)
txt(c,'Juntos','Todo encaja.',540,572,105,WHITE,font='editorial')
for j,(x,y) in enumerate([(410,850),(670,850),(540,1080)]):oval(c,'Ciclo '+str(j),x,y,500,color=WHITE,sw=3)
for t,x,y in [('cortes',380,850),('voz',703,850),('texto',540,1150)]:txt(c,t,t,x,y,52,WHITE,font='serifitalic')
ellipse(c,'Centro',540,925,18,col=YELLOW)
# Editorial sheet with three semantic tracks. Shared page moves are real camera travel.
c=comp('PLIEGO V3 - Ensamblado',190,1200,1600)
rect(c,'Papel',0,0,1200,1600,'#d5d2c7',noise=.7)
txt(c,'Intro','Hasta los',90,210,59,INK,align='left',font='editorial')
txt(c,'Cortes','cortes',76,425,210,INK,align='left',font='serifitalic')
path(c,'Regla de cortes',[[92,480],[1108,480]],INK,2)
for j,src in enumerate([2,3,7]):
 n=nested(c,'Toma '+str(j),photo(src),245+j*353,726,.26);enter(n,3+j*5,18,'x',80)
 # Deliberately narrow aspect crop is defined by a semantic precomp, not a material frame.
rect(c,'Etiqueta de voz',90,1002,106,43,YELLOW)
txt(c,'Voz','VOZ',100,1036,34,INK,align='left',font='editorial',track=80)
n=nested(c,'Voz original','ONDA V3 - False',685,1024,.94);anim(n,'wipe',[32,54],[100,0])
path(c,'Regla de texto',[[92,1100],[1108,1100]],INK,2)
rect(c,'Marcador de texto',87,1150,1012,155,YELLOW,a=46);n=c['layers'][-1];anim(n,'scale',[46,72],[[0,1],[1,1]])
txt(c,'Y los','y los',92,1214,47,INK,a=46,align='left',font='editorial')
n=txt(c,'Subtitulos','subtítulos',310,1280,146,INK,a=46,align='left',font='serifitalic');enter(n,46,15,'y',65,4)
path(c,'Regla inferior',[[92,1390],[1108,1390]],INK,2)
# Chosen direction B: from typographic/detail proof into one arranged creative.
c=comp('MG V3 - Ensamblado',190);paper(c)
n=three(nested(c,'Pliego editorial','PLIEGO V3 - Ensamblado',540,925,.74,0,144),0)
anim(n,'rot',[0,72,122,144],[-8,-8,0,0]);anim(n,'ry',[0,76,123],[-15,-15,0]);anim(n,'rx',[0,76,123],[5,5,0]);anim(n,'opacity',[0,124,144],[1,1,0])
c['camera']=camera([0,25,45,68,92,118,143,189],[[525,580,-1500],[525,580,-1500],[530,580,-1500],[535,1110,-1470],[535,1110,-1470],[540,925,-2350],[540,925,-2100],[540,960,-1800]])
# Large spoken phrase replaces small captions, with no duplicated copy.
n=txt(c,'Se ensamblan','se ensamblan',540,440,91,INK,a=95,b=136,font='editorial');enter(n,95,13,'y',35,3)
n=txt(c,'Automaticamente','automáticamente',540,1380,104,INK,a=134,b=180,font='serifitalic');enter(n,134,14,'x',-90,4)
n=nested(c,'Resultado continuo',photo(5),540,910,.13,132,190);anim(n,'scale',[132,155,171,189],[[.13,.13],[.31,.31],[.31,.31],[1,1]]);anim(n,'pos',[132,171,189],[[540,910],[540,910],[540,960]]);anim(n,'opacity',[132,140],[0,1])
S['events']['assembly']={'from':696,'to':886,'comp':c['name'],'dropCaptions':True}
# A printed portrait expands into environments, audio and final assembled piece.
c=comp('MG V3 - Creatividad',112);paper(c)
n=nested(c,'Personaje circular',portrait(2),540,830,.94,0,40,circleClip=True);anim(n,'scale',[0,20,36,40],[[.74,.74],[.94,.94],[.94,.94],[.80,.80]]);anim(n,'opacity',[0,6,35,40],[0,1,1,0])
n=txt(c,'Personaje','personaje',540,1338,156,INK,0,36,font='serifitalic');enter(n,0,14,'x',-80,3)
for j,src in enumerate([3,7,8]):
 n=nested(c,'Escena '+str(j),photo(src),255+j*285,900,.245,35,65);enter(n,35+j*3,12,'y',150,5)
n=txt(c,'Escenas','escenas',540,590,125,INK,36,60,font='editorial');enter(n,36,10,'y',-70,3)
n=nested(c,'Onda protagonista','ONDA V3 - False',540,890,1.04,60,78);anim(n,'wipe',[60,72],[100,0])
n=txt(c,'Voz','voz',540,1270,202,INK,60,78,font='serifitalic');enter(n,60,10,'x',90,4)
n=nested(c,'Montaje final',photo(5),540,890,.36,76,112);anim(n,'scale',[76,91,99,111],[[.24,.24],[.36,.36],[.36,.36],[1,1]]);anim(n,'pos',[76,99,111],[[540,890],[540,890],[540,960]])
n=txt(c,'Montaje','montaje',540,1420,129,INK,76,103,font='editorial');enter(n,76,10,'y',80,3)
# Match the actual moving shot on exit.
n=node(c,'video','Continuidad de la toma',(540,960),a=104,b=112,asset='Montaje-AD3.mp4',anchor=[540,960],w=1080,h=1920,startTime=-938/48);anim(n,'wipe',[104,111],[100,0])
S['events']['creative']={'from':938,'to':1050,'comp':c['name'],'dropCaptions':True}
# Reference-derived drawing circles: alignment is the action, never a decorative spinning bezel.
c=comp('MG V3 - Consistencia',176);paper(c,True)
for j,(xx,yy) in enumerate([(388,795),(692,795),(540,1040)]):
 n=oval(c,'Ciclo '+str(j),xx,yy,560,color=WHITE,sw=3.5,a=8+j*3,b=81,trim=[8+j*3,43+j*3]);n['glow']=5;n['glowColor']='#b6b6c6';anim(n,'pos',[8+j*3,46,68,80],[[xx,yy],[xx,yy],[540,915],[540,915]]);anim(n,'opacity',[8+j*3,15+j*3,74,81],[0,1,1,0])
txt(c,'Lo dificil','Lo difícil es',540,510,81,WHITE,0,26,font='editorial')
txt(c,'Que todo','que todo',540,470,80,WHITE,26,72,font='editorial')
n=txt(c,'Encaje','encaje',540,1350,170,WHITE,26,75,font='serifitalic');enter(n,26,17,'y',100,4)
# The three circles become the same person across three environments.
for j,src in enumerate([2,3,7]):
 n=nested(c,'Misma identidad '+str(src),portrait(src),540,905,.56,68+j*5,164,circleClip=True)
 anim(n,'pos',[68+j*5,101+j*3,148,163],[[540,905],[225+j*315,900],[225+j*315,900],[540,925]])
 anim(n,'scale',[68+j*5,104,148,163],[[.46,.46],[.43,.43],[.43,.43],[.49,.49]])
 anim(n,'opacity',[68+j*5,79+j*5,153,164],[0,1,1,0])
txt(c,'Misma','Misma',540,1250,77,WHITE,79,132,font='editorial')
n=txt(c,'Persona','persona',540,1430,180,WHITE,79,132,font='serifitalic');enter(n,79,14,'y',65,4)
rect(c,'Marca de coherencia',305,1210,470,122,YELLOW,132,164)
txt(c,'Mismo look','mismo look',540,1303,94,INK,132,164,font='editorial')
n=node(c,'video','Toma siguiente',(540,960),a=161,b=176,asset='Montaje-AD3.mp4',anchor=[540,960],w=1080,h=1920,startTime=-1248/48);anim(n,'wipe',[161,175],[100,0])
S['events']['consistency']={'from':1248,'to':1424,'comp':c['name'],'dropCaptions':True}
# Four outputs are a continuous drawing; focus moves along the network, then reveals its whole.
c=comp('MUNDO V3 - Sistema',144,2300,1500)
# One thin line with cubic tangents, not a stack of cards.
pts=[[0,800],[570,700],[1120,850],[1700,650],[2300,790]]
n=path(c,'Linea de salidas',pts,WHITE,3,trim=[0,100],inTangents=[[0,0],[-190,0],[-190,0],[-190,0],[-180,0]],outTangents=[[180,0],[190,0],[190,0],[190,0],[0,0]])
for j,(src,word,xx,yy) in enumerate([(2,'imágenes',360,680),(3,'vídeos',900,790),(7,'avatares',1450,700),(10,'anuncios',1990,760)]):
 a=j*15;n=nested(c,'Salida '+word,portrait(src),xx,yy,.40,a,144,circleClip=True);enter(n,a,16,'y',120,6)
 n=txt(c,'Nombre '+word,word,xx,yy+260,75,WHITE,a+5,144,font='editorial');enter(n,a+5,15,'y',36,3)
 oval(c,'Orbita '+word,xx,yy,350,color=YELLOW if j==0 else '#6a6a73',sw=2,a=a,b=144,trim=[a,a+22])
c=comp('MG V3 - Sistemas',144);paper(c,True)
n=nested(c,'Un sistema conectado','MUNDO V3 - Sistema',1300,860,1,0,144)
anim(n,'pos',[0,24,43,67,86,104,125,143],[[1330,860],[1330,860],[790,860],[240,860],[-300,860],[540,900],[540,900],[540,900]])
anim(n,'scale',[0,86,111,143],[[1,1],[1,1],[.44,.44],[.44,.44]])
n=txt(c,'Marca','Visual Hub',540,460,108,WHITE,0,124,font='serifitalic');enter(n,0,16,'y',-70,4)
n=txt(c,'Con IA','con IA',540,1420,99,WHITE,121,144,font='editorial');enter(n,121,11,'y',45)
S['events']['systems']={'from':1636,'to':1780,'comp':c['name'],'dropCaptions':True}
# A line of creative outputs. Constant travel and type scale provide the final cadence.
c=comp('MUNDO V3 - Produccion',82,3000,1300)
path(c,'Linea continua',[[0,670],[600,600],[1250,780],[1800,640],[2400,720],[3000,650]],WHITE,3,trim=[0,28],inTangents=[[0,0],[-200,0],[-200,0],[-200,0],[-200,0],[-200,0]],outTangents=[[200,0],[200,0],[200,0],[200,0],[200,0],[0,0]])
for j,src in enumerate([2,3,5,7,8,9]):
 n=nested(c,'Resultado '+str(j),photo(src),310+j*490,650,.27,0,82);n['rot']=[-5,3,-2,4,-3,2][j]
c=comp('MG V3 - Produccion',82);paper(c,True)
n=nested(c,'Continuidad del sistema','MUNDO V3 - Produccion',980,925,.86);anim(n,'pos',[0,81],[[980,925],[200,925]],'linear')
n=txt(c,'Una','una',540,468,79,WHITE,0,82,font='editorial');enter(n,0,10,'y',-45)
n=txt(c,'Linea','línea',540,683,213,WHITE,0,82,font='serifitalic');enter(n,0,14,'x',-100,4)
n=txt(c,'De produccion','de producción',540,1445,97,WHITE,13,82,font='editorial');enter(n,13,13,'x',80,4)
S['events']['production']={'from':1938,'to':2020,'comp':c['name'],'dropCaptions':True}
# Base edit, native live-footage captions and audio remain as delivered in V2.
old=json.load(open(V.parent/'v2/ae/design.json'));master=copy.deepcopy(old['comps']['AD3 - FINAL V2']);master['name']=S['master'];S['comps'][S['master']]=master
master['layers']=[n for n in master['layers'] if not n['name'].startswith('ESCENA') and not(n['name'].startswith('SUB') and any(n['from']>=e['from'] and n['from']<e['to'] for e in S['events'].values()))]
for n in master['layers']:
 if n['name'].startswith('SUB'):
  for e in S['events'].values():
   if n['from']<e['from']<n['to']:n['to']=e['from']
# Restore the tail of captions crossing a graphic boundary.
for n in old['comps']['AD3 - FINAL V2']['layers']:
 if n['name'].startswith('SUB'):
  for e in S['events'].values():
   if e['from']<=n['from']<e['to']<n['to']:
    q=copy.deepcopy(n);q['from']=e['to'];q['pos']=[q['pos'][0],1390];q.pop('anim',None);q['color']='#f4f1ea';master['layers'].append(q)
for k,e in S['events'].items():nested(master,'ESCENA V3 - '+k,e['comp'],540,960,1,e['from'],e['to'],startTime=e['from']/48)
master['layers']=sorted(master['layers'],key=lambda n:0 if n['name'] in ['Montaje Remotion','Voz musica efectos'] else 1 if n['name'].startswith('ESCENA') else 2)
(V/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print(len(S['comps']),'comps',sum(len(c['layers']) for c in S['comps'].values()),'layers')
