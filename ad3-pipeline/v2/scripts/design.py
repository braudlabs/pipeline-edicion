from pathlib import Path
import json,math,copy,subprocess
import numpy as np
from PIL import Image
V=Path(__file__).resolve().parents[1];R=V;A=V/'assets';F=48
# Retain deterministic authoring primitives; all built layers are native AE layers.
exec(compile((V.parents[0]/'scripts/helpers.py').read_text().split('def photo_obj')[0],__file__,'exec'))
R=V;A=V/'assets';F=48;INK='#102e35';CREAM='#f1efe8';RED='#fc785f';BLUE='#80c4cb';D=2250
S={'fps':48,'master':'AD3 - FINAL V2','comps':{},'events':{}}
assets={i:next(p.name for p in A.glob(f'{i:02d}-*.jpg') if not p.name.endswith('frente.jpg')) for i in range(1,11)}
assets[7]='07-frente.jpg'
def stage(c):
 n=media(c,'Escenario generado sustituible','Estudio-Petroleo.png',540,960,1180);anim(n,'pos',[0,c['duration']-1],[[510,940],[555,970]],'linear')
 # A subtle physical ground shadow anchors the floating assembly.
 n=ellipse(c,'Sombra de conjunto',540,1450,740,70,col='#061c21');n['opacity']=.32;n['blur']=28

def raw(i):return 'FOTO V2 - '+str(i)
def port(i):return 'MARCO V2 - '+str(i)
for i in [1,2,3,5,7,8,9,10]:
 c=comp(raw(i),D);media(c,'Fotografia sustituible',assets[i],540,960,1080)
 inner=comp('VENTANA V2 - '+str(i),D,700,1400);media(inner,'Contenido sustituible',assets[i],350,700,790)
 c=comp(port(i),D,941,1672);nested(c,'Contenido en ventana','VENTANA V2 - '+str(i),470,826,1,round=28);media(c,'Material del marco','Marco.png',470.5,836,941)
# Actual voice envelope inside a tactile frame. 150 points, not invented audio data.
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(V.parent/'assets/Voz-Montada.wav'),'-t','14.5','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
pks=np.array([np.sqrt(np.mean(z*z)) for z in np.array_split(x,150)]);pks=np.maximum(2,pks/max(pks)*52)
for kind in ['Imagen','Voz','Texto']:
 c=comp('CAPA V2 - '+kind,D,1000,300);rect(c,'Fondo de inserto',72,66,838,166,'#092c35',round=12)
 if kind=='Imagen':
  for i,src in enumerate([1,2,3]):
   cc=comp('MINI V2 - '+str(src),D,276,160);media(cc,'Toma '+str(src),assets[src],138,172,278)
  c=S['comps']['CAPA V2 - '+kind]
  for i,src in enumerate([1,2,3]):nested(c,'Toma real '+str(src),'MINI V2 - '+str(src),214+i*278,149,1)
 if kind=='Voz':
  pts=[[82+i*5.5,150-float(v)] for i,v in enumerate(pks)]+[[82+i*5.5,150+float(v)] for i,v in reversed(list(enumerate(pks)))];node(c,'path','Onda de la voz original',points=pts,closed=True,color=RED)
  path(c,'Eje del audio',[[80,150],[910,150]],'#ffbaa7',1)
 if kind=='Texto':
  for j,(s,xx) in enumerate([('Este anuncio',226),('con IA',502),('montado solo',770)]):txt(c,'Texto editable '+str(j),s,xx,167,38,CREAM)
  for xx in [354,628]:path(c,'Division '+str(xx),[[xx,118],[xx,183]],'#4f6f73',2)
 media(c,'Chasis generado','Chasis.png',500,150,1000)
# Frame of a single finished creative: photographic face, actual waves and native type share a world.
c=comp('MG V2 - Ensamblado',190);stage(c)
c['camera']=camera([0,22,75,116,154,189],[[540,920,-1820],[510,850,-1850],[550,880,-1910],[570,880,-1790],[540,840,-1870],[540,960,-1800]])
# The outgoing shot remains the visual anchor before its two companion shots arrive.
n=nested(c,'Del plano a la pista',raw(3),540,960,1,0,31);anim(n,'pos',[0,21,30],[[540,960],[540,566],[540,566]]);anim(n,'scale',[0,21,30],[[1,1],[.19,.19],[.19,.19]]);anim(n,'opacity',[0,21,30],[1,1,0])
for j,kind in enumerate(['Imagen','Voz','Texto']):
 at=[12,31,52][j];y=[555,863,1171][j];z=[-10,-130,-250][j]
 n=three(nested(c,'Pieza '+kind,'CAPA V2 - '+kind,540,y,.91,at,168,shadow=[0,14,20,'#000000',.5]),z)
 # Three differentiated arrivals become one aligned spatial assembly.
 anim(n,'pos',[at,at+23,112,143,164],[[540+[-400,470,0][j],y+[0,0,360][j],z+350],[540,y,z],[540,y,z],[540,820+j*24,80+j*40],[540,820,300]])
 anim(n,'rx',[at,at+23,112,150],[[32,-35,25][j],-8,-8,0]);anim(n,'ry',[at,at+23,112,150],[[-28,30,-22][j],-11,-11,0]);anim(n,'scale',[at,at+23,112,155],[[.75,.75],[.91,.91],[.91,.91],[.46,.46]])
 anim(n,'opacity',[at,at+8,145,165],[0,1,1,0])
 for s,yy in [({'Imagen':'Clips','Voz':'Voz','Texto':'Subtítulos'}[kind],y-155)]:
  t=three(txt(c,'Etiqueta '+kind,s,139,yy,35,CREAM,at+8,134,align='left'),z);enter(t,at+8,14,'x',-30);anim(t,'opacity',[at+8,at+18,121,134],[0,1,1,0])
# A narrow scanning light travels across all three layers as they synchronize.
n=three(path(c,'Sincronia',[[0,388],[0,1280]],RED,6,a=87,b=135),-320);anim(n,'pos',[87,94,132],[[140,0,-320],[140,0,-320],[925,0,-320]],'linear');anim(n,'opacity',[87,94,127,135],[0,.9,.9,0])
n=three(nested(c,'Creatividad ensamblada',port(5),540,820,.50,142,185,shadow=[0,20,28,'#000000',.5]),-220);anim(n,'opacity',[142,150,175,185],[0,1,1,0]);anim(n,'scale',[142,160,184],[[.12,.12],[.5,.5],[1.38,1.38]]);anim(n,'ry',[142,163,184],[-24,0,0])
n=nested(c,'Resolucion a la toma',raw(5),540,960,.6,171,190);anim(n,'opacity',[171,184],[0,1]);anim(n,'scale',[171,189],[[.6,.6],[1,1]])
S['events']['assembly']={'from':696,'to':886,'comp':c['name'],'captionY':1450}

# An exploded portrait: four components converge into the same finished image.
c=comp('MG V2 - Creatividad',112);stage(c)
c['camera']=camera([0,26,74,111],[[395,825,-1770],[500,845,-1790],[670,850,-1870],[540,960,-1800]])
for i,src in enumerate([2,3,8,5]):
 at=[0,22,48,70][i];n=three(nested(c,'Componente '+str(i),port(src),540,815,.59,at,112,shadow=[0,20,24,'#000000',.42]),-i*95)
 anim(n,'pos',[at,at+18,94,111],[[540+[-270,350,-330,300][i],780+i*30,180-i*30],[540+(i-1.5)*62,800+i*18,-i*95],[540,800,-i*18],[540,800,-i*18]])
 anim(n,'ry',[at,at+18,94],[-34,-18,0]);anim(n,'rx',[at,at+18,94],[12,4,0]);anim(n,'opacity',[at,at+6,98,111],[0,1,1,0])
# Real voice and glyphs float on independent planes before the last closure.
n=three(nested(c,'Voz como capa','CAPA V2 - Voz',540,1170,.64,48,90),-520);enter(n,48,16,'x',150,4);anim(n,'opacity',[48,54,79,90],[0,1,1,0])
for i,(w,a,b) in enumerate([('personaje',0,36),('escenas',36,60),('voz',60,76),('montaje',76,112)]):
 n=txt(c,'Palabra '+w,w,540,1450,94,CREAM,a,b);enter(n,a,10,'x',[-90,90,-70,70][i],4)
# Live frame arrives in exactly the same master time as the edit underneath.
n=node(c,'video','Resultado en movimiento',(540,960),a=98,b=112,asset='Montaje-AD3.mp4',anchor=[540,960],w=1080,h=1920,startTime=-938/48,scale=[.7,.7]);anim(n,'opacity',[98,111],[0,1]);anim(n,'scale',[98,111],[[.7,.7],[1,1]])
S['events']['creative']={'from':938,'to':1050,'comp':c['name'],'dropCaptions':True}

# Consistency: separated image blades align within an optical gate; the same subject survives the move.
c=comp('MG V2 - Consistencia',176);stage(c)
for i in range(3):
 cc=comp('LAMINA V2 - '+str(i),176,240,800);media(cc,'Seccion del rostro',assets[7],360-i*240,550,720)
c=S['comps']['MG V2 - Consistencia']
for i in range(3):
 n=nested(c,'Lamina que encaja '+str(i),'LAMINA V2 - '+str(i),300+i*240,855,1,0,68);anim(n,'pos',[0,22+i*5,53,68],[[300+i*240,855+[170,-180,210][i]],[300+i*240,855],[300+i*240,855],[540,850]]);anim(n,'rot',[0,28],[[8,-7,6][i],0]);anim(n,'opacity',[0,8,55,68],[0,1,1,0])
n=media(c,'Iris de coherencia','Iris.png',540,850,1040,0,91);anim(n,'rot',[0,33,56,90],[-50,0,0,28]);anim(n,'scale',[0,28,57,90],[[1.2,1.2],[1,1],[1,1],[1.34,1.34]]);anim(n,'opacity',[0,7,70,90],[0,1,1,0])
for i,src in enumerate([2,7,9]):
 n=three(nested(c,'Identidad '+str(src),port(src),540,850,.50,58+i*5,159,shadow=[0,16,24,'#000000',.4]),90 if i!=1 else -120)
 anim(n,'pos',[58+i*5,94+i*3,137,158],[[540,850,120],[160+i*380,825,90 if i!=1 else -120],[160+i*380,825,90 if i!=1 else -120],[540,900,0]])
 anim(n,'ry',[58+i*5,97,137,158],[0,[20,0,-20][i],[20,0,-20][i],0]);anim(n,'scale',[58+i*5,97,137,158],[[.50,.50],[.43,.43],[.43,.43],[.72,.72]]);anim(n,'opacity',[58+i*5,70+i*5,145,159],[0,1,1,0])
c['camera']=camera([0,52,104,137,175],[[540,900,-1800],[540,900,-1800],[540,870,-2000],[540,870,-2000],[540,960,-1800]])
n=node(c,'video','Volver a la toma viva',(540,960),a=147,b=176,asset='Montaje-AD3.mp4',anchor=[540,960],w=1080,h=1920,startTime=-1248/48,scale=[.56,.56]);anim(n,'opacity',[147,163],[0,1]);anim(n,'scale',[147,175],[[.56,.56],[1,1]])
S['events']['consistency']={'from':1248,'to':1424,'comp':c['name'],'captionY':1450}

# The hub branches into four editorial outputs; camera goes from object detail to full system.
c=comp('MG V2 - Sistemas',144);stage(c)
# Native branch paths, animated before the output arrives. No fabricated UI.
for i,(x,y) in enumerate([(200,570),(880,570),(200,1190),(880,1190)]):
 pts=[[540,850],[540,850+(y-850)*.45],[x,850+(y-850)*.45],[x,y]]
 p=three(path(c,'Salida conectada '+str(i),pts,'#85cbd0',5,a=12+i*12,trim=[12+i*12,34+i*12]),200)
for i,(lab,src,x,y) in enumerate([('imágenes',2,200,525),('vídeos',3,880,525),('avatares',7,200,1180),('anuncios',10,880,1180)]):
 n=three(nested(c,'Salida '+lab,port(src),x,y,.29,20+i*12,144,shadow=[0,10,17,'#000000',.6]),0)
 anim(n,'pos',[20+i*12,40+i*12,125,143],[[540,850,220],[x,y,0],[x,y,0],[x,y,0]]);anim(n,'ry',[20+i*12,40+i*12],[i%2*60-30,0]);anim(n,'opacity',[20+i*12,30+i*12],[0,1])
 n=three(txt(c,'Tipo '+lab,lab,x,y+265,53,CREAM,24+i*12),-20);enter(n,24+i*12,15,'y',35)
n=three(media(c,'Centro de produccion','Iris.png',540,850,450),-130);anim(n,'rot',[0,110],[-70,20],'linear')
n=three(txt(c,'Marca del sistema','Visual\nHub',540,823,63,CREAM,0),-150)
c['camera']=camera([0,22,70,100,123,143],[[540,850,-950],[540,850,-1250],[560,820,-1820],[540,860,-2050],[540,890,-2200],[540,890,-2200]])
n=txt(c,'Con IA','con IA',540,1480,70,CREAM,121);enter(n,121,12,'y',35)
S['events']['systems']={'from':1636,'to':1780,'comp':c['name'],'dropCaptions':True}

# Production line: deep repeated frames move toward the viewer, cross a physical output gate.
c=comp('MG V2 - Produccion',82);stage(c)
for i,src in enumerate([2,3,5,7,8,9,10]):
 n=three(nested(c,'Produccion '+str(i),port(src),540+(i-3)*330,840,.44,0,82,shadow=[0,14,20,'#000000',.5]),250+i*220)
 anim(n,'pos',[0,81],[[540+(i-3)*330,840,250+i*220],[540+(i-5)*330,840,-150+i*220]],'linear');n['ry']=-27
c['camera']=camera([0,26,63,81],[[365,880,-1640],[470,880,-1780],[590,880,-1640],[650,880,-1530]])
for i in range(12):
 n=three(path(c,'Guia de carril '+str(i),[[i*220-900,300],[i*220-900,1350]],'#44777d',1),900)
for w,y,sz,a,dx in [('una línea',390,92,0,-80),('de producción',1420,100,13,80)]:
 n=txt(c,w,w,540,y,sz,CREAM,a);enter(n,a,12,'x',dx,3)
S['events']['production']={'from':1938,'to':2020,'comp':c['name'],'dropCaptions':True}

# Retain the established cut, audio and live-shot captions, replacing only the motion scenes.
old=json.load(open(V.parent/'ae/design.json'));master=copy.deepcopy(old['comps']['AD3 - FINAL']);master['name']=S['master'];S['comps'][S['master']]=master
master['layers']=[n for n in master['layers'] if not n['name'].startswith('ESCENA') and n['name']!='Voz visible']
for n in master['layers']:
 if n['name'].startswith('SUB') and any(n['from']<e['to'] and n['to']>e['from'] for e in S['events'].values()):
  n['color']=CREAM;n['textStroke']=['#09262d',.6];n['shadow']=[0,2,3,'#03181d',.55]
  if n['from']>=696 and n['from']<886 or n['from']>=1248 and n['from']<1424:
   dy=1450-n['pos'][1];n['pos'][1]+=dy
   if 'pos' in n.get('anim',{}):
    for pp in n['anim']['pos']['values']:pp[1]+=dy
for key,e in S['events'].items():nested(master,'ESCENA V2 - '+key,e['comp'],540,960,1,e['from'],e['to'],startTime=e['from']/48)
# Layer order is authored back-to-front. Main captions remain on top of the graphic scenes.
master['layers']=sorted(master['layers'],key=lambda n:0 if n['name'] in ['Montaje Remotion','Voz musica efectos'] else 1 if n['name'].startswith('ESCENA') else 2)
(V/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2));print(len(S['comps']),'comps',sum(len(c['layers']) for c in S['comps'].values()),'layers')
