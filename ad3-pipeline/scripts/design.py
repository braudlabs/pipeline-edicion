exec(compile(open(__file__.replace('design.py','helpers.py')).read(),__file__,'exec'))
import subprocess
T=json.load(open(R/'remotion/src/timeline.json'));D=T['duration'];assets=sorted(p.name for p in A.glob('*.jpg'))
# Tall photographic sources preserve the original frame; short sources crop deliberately.
for i in range(10):
 photo_obj('IMAGEN - '+str(i+1),assets[i],540,960,0)
 photo_obj('TIRA - '+str(i+1),assets[i],270,310,-20 if i==0 else 45)
for i in range(3):
 cc=comp('FOTOGRAMAS - '+str(i+1),2600,270,78)
 for k in range(3):media(cc,'Miniatura '+str(k),assets[i],45+k*90,36,88)
# A waveform of the actual first three voices, not a decorative oscillator.
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(A/'Voz-Montada.wav'),'-t',str(696/48),'-ac','1','-ar','8000','-f','f32le','-']),np.float32)
peaks=np.array([np.sqrt(np.mean(z*z)) for z in np.array_split(x,150)]);peaks=np.maximum(2,peaks/max(peaks)*26)
c=comp('OBJ - Voz real',D,860,86);rect(c,'Pista de voz',0,0,860,86,'#e7e9f4',round=12)
pts=[[i*5.65+8,43-float(v)] for i,v in enumerate(peaks)]+[[i*5.65+8,43+float(v)] for i,v in reversed(list(enumerate(peaks)))];node(c,'path','Onda del audio aportado',points=pts,closed=True,color=BLUE)
# Native transcript lane; its words are source content, not a fake product UI.
c=comp('OBJ - Pista de texto',D,860,86)
for i,(s,xx,w) in enumerate([('Este anuncio',0,265),('con IA',280,265),('montado solo',560,300)]):
 rect(c,'Segmento '+str(i),xx,0,w,86,INK,round=12);txt(c,'Texto '+str(i),s,xx+w/2,55,29,CREAM)
# Main self-assembly: preserve footage identity through change of scale, snap, scan, return.
c=comp('MG - Ensamblado',190);bg(c)
c['camera']=camera([0,20,65,94,138,160,189],[[540,960,-1800],[540,940,-1850],[540,940,-1850],[540,1100,-1700],[540,1100,-1700],[540,960,-2160],[540,960,-1800]])
for j,y in enumerate([865,1015,1165]):
 n=three(rect(c,'Guia de alineacion '+str(j),104,y,872,102,'#dedcd3',round=14),120);enter(n,20+j*8,15,'x',-100,3)
 for k in range(3):
  n=three(path(c,f'Registro {j}-{k}',[[110+k*280,y-15],[110+k*280,y-3]],'#98998f',2,a=20+j*8),119);enter(n,20+j*8,15,'x',-100)
labels=[('Clips',835),('Voz',985),('Subtítulos',1135)]
for j,(s,y) in enumerate(labels):
 n=three(txt(c,'Etiqueta '+s,s,110,y,29,INK,20+j*14,align='left'),110);enter(n,20+j*14,15,'y',30)
# First portrait begins full screen, other source images emerge from that frame.
for i in range(3):
 start=0 if i==2 else 20+i*7
 n=three(nested(c,'Fuente visual '+str(i+1),'IMAGEN - '+str(i+1),250+i*290,560,.5,start,102,round=14,shadow=[0,14,19,'#282921',.21]),0)
 if i==2:
  anim(n,'pos',[0,23,57,86,139,160],[[540,960,0],[830,560,0],[830,560,0],[830,913,0],[830,913,0],[540,760,0]])
  anim(n,'scale',[0,23,57,86,139,160],[[2,2],[.5,.5],[.5,.5],[.15,.15],[.15,.15],[.15,.15]])
 else:
  anim(n,'pos',[start,start+18,57+i*5,83+i*5,139,160],[[540,560,280],[250+i*290,560,0],[250+i*290,560,0],[250+i*290,913,0],[250+i*290,913,0],[540,760,100+i*80]])
  anim(n,'scale',[start,start+18,57+i*5,83+i*5,139,160],[[.3,.3],[.5,.5],[.5,.5],[.15,.15],[.15,.15],[.15,.15]])
  anim(n,'opacity',[start,start+8,146,160],[0,1,1,0])
 anim(n,'opacity',[start,start+8,86,101],[0 if i!=2 else 1,1,1,0])
 n['rot']=0
 fornum=i
 nn=three(nested(c,'Imagen en pista '+str(i),'FOTOGRAMAS - '+str(i+1),250+i*290,913,1,78+i*3,190,round=9),-4)
 anim(nn,'opacity',[78+i*3,90+i*3],[0,1])
# Picture compression is a crop/track metaphor; finished preview replaces it at the collapse.
n=three(nested(c,'Voz a su pista','OBJ - Voz real',540,1058,1,37,167),-20);anim(n,'pos',[37,66,134,161],[[540,660,-20],[540,1058,-20],[540,1058,-20],[540,1160,-20]]);anim(n,'scale',[37,66,134,161],[[.58,1],[1,1],[1,1],[.48,.58]]);anim(n,'opacity',[37,43,152,167],[0,1,1,0])
n=three(nested(c,'Texto a su pista','OBJ - Pista de texto',540,1208,1,59,169),-35);anim(n,'pos',[59,88,134,165],[[540,715,-35],[540,1208,-35],[540,1208,-35],[540,1215,-35]]);anim(n,'scale',[59,88,134,165],[[.7,1],[1,1],[1,1],[.5,.5]]);anim(n,'opacity',[59,65,151,169],[0,1,1,0])
# A single line moves through all three aligned tracks.
n=three(path(c,'Cabezal sincronizado',[[0,813],[0,1270]],RED,5,a=90,b=149),-80);anim(n,'pos',[90,96,141],[[120,0,-80],[120,0,-80],[950,0,-80]],'linear')
n=three(path(c,'Asa del cabezal',[[-11,0],[11,0],[0,15]],RED,4,a=90,b=149,closed=True),-81);anim(n,'pos',[90,96,141],[[120,795,-81],[120,795,-81],[950,795,-81]],'linear')
# Actual next-shot photograph resolves the three tracks into a single vertical composition.
n=nested(c,'Resultado del montaje','IMAGEN - 5',540,780,.76,146,190,round=10,shadow=[0,10,25,'#171917',.24]);anim(n,'opacity',[146,155],[0,1]);anim(n,'pos',[146,168,189],[[540,780],[540,780],[540,960]]);anim(n,'scale',[146,168,189],[[.76,.76],[.76,.76],[2,2]])
# Keep the phrase readable before the transition back to live footage.
S['events']['assembly']={'from':696,'to':886,'comp':c['name'],'captionY':1415}

# One creative: a filmstrip turns into a single finished vertical image.
c=comp('MG - Una creatividad',112);bg(c)
for i in range(4):
 src=[2,3,8,5][i];x=540+(i-1.5)*360
 n=three(nested(c,'Componente visual '+str(i),'IMAGEN - '+str(src),x,810,.59,0,112,round=14,shadow=[0,12,22,'#212321',.2]),(i%2)*120)
 anim(n,'pos',[0,14+i*3,66,91],[[x+600,810,250],[x,810,(i%2)*120],[x,810,(i%2)*120],[540,810,i*90]])
 anim(n,'ry',[0,20,66,91],[-17,0,0,0]);anim(n,'scale',[0,20,66,91],[[.55,.55],[.59,.59],[.59,.59],[.84,.84]])
 if i<3:anim(n,'opacity',[79,92],[1,0])
c['camera']=camera([0,20,55,92,111],[[0,900,-1500],[120,900,-1500],[800,900,-1650],[540,900,-1830],[540,900,-1700]])
for i,(s,at) in enumerate([('personaje',0),('escenas',36),('voz',60),('montaje',76)]):
 n=txt(c,'Componente hablado '+s,s,540,1320,91,RED,at,[36,60,76,112][i]);enter(n,at,10,'x',[-80,80,-60,60][i],5)
S['events']['creative']={'from':938,'to':1050,'comp':c['name'],'dropCaptions':True}

# Consistency: misregistered strips lock into one image, then reveal three locations.
c=comp('MG - Encaje y consistencia',176);bg(c)
# Independently cropped strips of one supplied photograph; no traced reference assets.
for i in range(3):
 src='COLUMNA - '+str(i);cc=comp(src,176,180,700)
 media(cc,'Parte de la misma toma',assets[6],270-i*180,360,540)
for i in range(3):
 n=nested(c,'Encaje '+str(i),'COLUMNA - '+str(i),360+i*180,820,1,0,72,shadow=[0,8,10,'#22231e',.18]);anim(n,'pos',[0,13+i*5,48,69],[[360+i*205,820+[-180,150,-90][i]],[360+i*180,820],[360+i*180,820],[360+i*180,820]]);anim(n,'rot',[0,20],[[ -8,6,-4][i],0])
 n['anim']['opacity']={'frames':[55,72],'values':[1,0],'ease':'out'}
for i,src in enumerate([2,7,9]):
 n=three(nested(c,'Misma persona en '+str(src),'IMAGEN - '+str(src),540,820,.74,57,176,round=12,shadow=[0,10,18,'#262721',.2]),150 if i!=1 else 0)
 endpos=[220+i*320,820,150 if i!=1 else 0];anim(n,'pos',[57,88,145,175],[[540,820,150 if i!=1 else 0],endpos,endpos,[540,850,0]])
 anim(n,'scale',[57,88,145,175],[[.74,.74],[.53,.53],[.53,.53],[2,2]])
 if i!=1:anim(n,'opacity',[57,67,145,172],[0,1,1,0])
 else:anim(n,'opacity',[57,70],[0,1])
c=S['comps']['MG - Encaje y consistencia'];c['camera']=camera([0,45,88,145,175],[[540,925,-1800],[540,925,-1800],[540,925,-2020],[540,925,-2020],[540,960,-1800]])
S['events']['consistency']={'from':1248,'to':1424,'comp':c['name'],'captionY':1390}

# Four outputs from one source: a central frame unfolds into a sequential film path.
c=comp('MG - Sistemas',144);bg(c)
# Thin red track is revealed continuously behind the media, read left to right by the camera.
p=three(path(c,'Ruta de produccion',[[160,910],[2250,910]],RED,4,a=0,trim=[0,103]),180)
for i,(lab,src) in enumerate([('imágenes',2),('vídeos',3),('avatares',7),('anuncios',10)]):
 x=320+i*560
 n=three(nested(c,'Salida '+lab,'IMAGEN - '+str(src),x,750,.7,i*12,144,round=14,shadow=[0,12,22,'#252722',.22]),0);enter(n,i*12,20,'y',110,6)
 n=three(txt(c,'Tipo '+lab,lab,x,1180,72,INK,i*12),-10);enter(n,i*12,16,'y',50,3)
 n=three(ellipse(c,'Registro '+lab,x,1240,12,col=RED,a=i*12),0)
c['camera']=camera([0,18,44,72,100,122,143],[[320,920,-1780],[320,920,-1780],[880,920,-1780],[1440,920,-1780],[2000,920,-1780],[1160,920,-3300],[1160,920,-3300]])
# Borderless identity wordmark; no made-up product chrome.
txt(c,'Marca','Visual Hub',540,325,64,INK,0);enter(txt(c,'Remate IA','con IA',540,1450,58,INK,122),122,12,'y',35);S['events']['systems']={'from':1636,'to':1780,'comp':c['name'],'captionY':1450,'dropCaptions':True}

# Production: incoming thumbnails feed an output frame along a ruled rail.
c=comp('MG - Produccion',82);bg(c)
for i in range(7):
 n=three(nested(c,'Unidad '+str(i),'IMAGEN - '+str([2,3,5,7,8,9,10][i]),120+i*230,880,.32,0,82,round=10,shadow=[0,8,10,'#292a24',.22]),i*40)
 anim(n,'pos',[0,50,81],[[120+i*230,880,i*40],[-450+i*230,880,i*40],[-900+i*230,880,i*40]],'linear')
path(c,'Carril superior',[[0,540],[1080,540]],'#b7b7ae',2);path(c,'Carril inferior',[[0,1210],[1080,1210]],'#b7b7ae',2)
for i in range(23):path(c,'Registro '+str(i),[[i*50,1210],[i*50,1220+(i%4==0)*12]],'#9e9f96',2)
kin=txt(c,'Linea','una línea',540,415,86,INK);enter(kin,0,12,'x',-60)
kin=txt(c,'Produccion','de producción',540,1370,96,RED,14);enter(kin,14,14,'x',80)
S['events']['production']={'from':1938,'to':2020,'comp':c['name'],'dropCaptions':True}

# Build master; footage and audio remain independently replaceable.
c=comp('AD3 - FINAL',D)
node(c,'video','Montaje Remotion',(540,960),asset='Montaje-AD3.mp4',anchor=[540,960],w=1080,h=1920)
node(c,'audio','Voz musica efectos',(0,0),asset='Mezcla-Final.wav')
for key,e in S['events'].items():
 n=nested(c,'ESCENA - '+key,e['comp'],540,960,1,e['from'],e['to'],startTime=e['from']/F)
# A small waveform during the voice reveal, away from the mouth.
n=nested(c,'Voz visible','OBJ - Voz real',540,1450,.64,642,686,startTime=642/F)
anim(n,'opacity',[642,648,681,686],[0,1,1,0]);anim(n,'scale',[642,655],[[.2,.64],[.64,.64]])
# Offer: native restrained type, avoiding duplicate subtitle tracks.
n=txt(c,'Marca final','Visual Hub',540,1235,64,CREAM,2040,D,shadow=[0,2,4,'#100f0e',.6]);enter(n,2040,15,'x',-65)
n=txt(c,'Precio mensual','$39',457,1400,138,CREAM,2085,D,shadow=[0,2,4,'#100f0e',.6]);enter(n,2085,16,'y',75,4)
n=txt(c,'Periodicidad','/mes',640,1398,58,CREAM,2090,D,shadow=[0,2,4,'#100f0e',.6]);enter(n,2090,13,'x',65,3)
n=txt(c,'Cancelacion','Cancela cuando quieras',540,1485,43,CREAM,2160,D,shadow=[0,2,4,'#100f0e',.6]);enter(n,2160,16,'y',45,3)
(R/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2));print('Design:',len(S['comps']),'comps;',sum(len(c['layers']) for c in S['comps'].values()),'layers')
