from pathlib import Path
import json, math, numpy as np, subprocess
from PIL import Image,ImageFont
R=Path(__file__).resolve().parents[1];A=R/'assets';F=48
exec((R.parents[0]/'scripts/helpers.py').read_text().split('def photo_obj')[0].replace('R=Path(__file__).resolve().parents[1];A=R/\'assets\';F=48', ''))
W='#f0f7eb'; G='#659742'; M='#bacfa8'; INK='#273e1b'
T=json.load(open(R/'remotion/src/timeline.json')); N=T['duration'];S={'fps':48,'master':'AD3 - V4 FINAL','comps':{},'events':{}}
def tx(c,s,x,y,size=100,a=0,b=None,**kw):return txt(c,s,s,x,y,size,kw.pop('col',W),a,b,track=kw.pop('track',-50),**kw)
def green(c):return nested(c,'Fondo verde compartido','00 - Verde BRAUD',540,960,a=0,b=c['duration'])
def reveal(n,a=0,d=10,axis='y',delta=65):return enter(n,a,d,axis,delta,6)
def line(c,name,pts,a=0,b=None,width=2):return path(c,name,pts,M,width,a,b,trim=[a,a+16])
def ring(c,name,x,y,r,a=0,b=None):return ellipse(c,name,x,y,r*2,col=None,a=a,b=b,stroke=M,strokeWidth=2)
def pframe(c,name,asset,x,y,w,a=0,b=None):
 return media(c,name,asset,x,y,w,a,b)
bgc=comp('00 - Verde BRAUD',N)
node(bgc,'gradient','Luz radial',(540,960),w=1080,h=1920,anchor=[540,960],color='#43632b',endColor=INK,center=[595,960],radius=1205)

# Three distinct semantic constructions of the key assembly beat, shown as native styleframes.
for name in ['EXPLORACION - Convergencia','EXPLORACION - Suma']:
 c=comp(name,192);green(c)
 if 'Convergencia' in name:
  ring(c,'Circuito',540,890,350)
  for j,(s,ang) in enumerate(zip(['imagen','voz','texto'],[-90,30,150])):
   x=540+350*math.cos(math.radians(ang));y=890+350*math.sin(math.radians(ang));line(c,'Conexion '+s,[[540,890],[x,y]]);tx(c,s,x,y,60)
  tx(c,'1',540,1000,330);tx(c,'anuncio',540,1090,70)
 else:
  for j,s in enumerate(['imagen','voz','texto']):tx(c,s,540,700+j*145,130)
  line(c,'Resultado',[[200,1100],[880,1100]]);tx(c,'completo',540,1270,170)

# Choice: spatial editorial timeline. The same images travel, align, and become the film.
assembly=comp('01 - Se monta solo',188);green(assembly)
board=comp('01A - Pistas editables',188,1600,1700)
for i,y in enumerate([530,1000,1210]):line(board,'Pista '+str(i),[[90,y],[1510,y]],0,width=1.5)
for j,asset in enumerate(['toma-01.jpg','toma-02.jpg','toma-03.jpg']):
 n=pframe(board,'Clip real '+str(j+1),asset,430+j*355,570,260,0)
 anim(n,'pos',[0,22+j*6,70],[[430+j*355,570+(j-1)*360],[430+j*355,570],[430+j*355,570]],'flow')
 anim(n,'rot',[0,28+j*6],[(j-1)*13,0]);anim(n,'opacity',[j*3,j*3+8],[0,1])
 tx(board,['cortes','voz','subtítulos'][j],170,[345,900,1140][j],51,0,align='left',col=M)
# Genuine source waveform (three early clips, extracted from the newly edited audio).
samples=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(A/'Voz-Montada.wav'),'-t','12','-ac','1','-ar','8000','-f','f32le','-']),np.float32)
bins=np.array_split(samples,100);amps=[min(85,8+float(np.sqrt((x*x).mean()))*600) for x in bins]
for j,amp in enumerate(amps):
 n=rect(board,'Onda '+str(j),305+j*10.5,1000-amp/2,4,amp,M,a=35,b=188)
 anim(n,'opacity',[35+j//5,45+j//5],[0,1]);anim(n,'scale',[35,65],[[1,.05],[1,1]])
for j,s in enumerate(['Estos planos','no se han grabado']):
 n=tx(board,s,320+j*560,1280,60,57,align='left');reveal(n,57+j*5,14,'y',120)
n=line(board,'Cabezal',[[320,310],[320,1360]],91,width=3)
anim(n,'pos',[91,138,160],[[0,0],[850,0],[1090,0]],'linear')
n=nested(assembly,'Plano de pistas','01A - Pistas editables',540,960,.73,threeD=True)
anim(n,'pos',[0,22,65,136,160],[[590,1100,0],[565,1000,0],[540,960,0],[510,910,0],[290,650,0]],'flow')
anim(n,'scale',[0,65,136,160],[[1.05,1.05],[.7,.7],[.7,.7],[.86,.86]],'flow')
anim(n,'rx',[0,65,160],[14,0,-3],'flow');anim(n,'ry',[0,65,160],[-12,0,3],'flow')
tx(assembly,'se ensamblan',540,1450,92,94,135)
n=tx(assembly,'automáticamente',540,1500,112,135,188);reveal(n,135,12,'x',140)
# Actual next shot grows from a thumbnail into a clean full-frame hand-off.
n=pframe(assembly,'Salida al anuncio', 'toma-05.jpg', 660,875,145,157,188)
anim(n,'pos',[157,172,187],[[660,875],[610,920],[540,960]],'flow')
anim(n,'scale',[157,172,187],[[1,1],[3.2,3.2],[1080/145,1080/145]],'flow')

# Four constituent parts condense to one creativity. Same radial geometry as the pilot.
c=comp('02 - Una creatividad',66);green(c)
for j,(s,ang) in enumerate(zip(['personaje','escenas','voz','montaje'],[-90,0,90,180])):
 x=540+430*math.cos(math.radians(ang));y=910+430*math.sin(math.radians(ang))
 n=line(c,'Conexion '+s,[[540,910],[x,y]],0,width=2)
 anim(n,'opacity',[0,22],[1,0])
 n=tx(c,s,x,y,56,0,27);anim(n,'pos',[0,25],[[x,y],[540,910]],'out');anim(n,'opacity',[10,26],[1,0])
n=tx(c,'1',540,990,360,8);reveal(n,8,15,'y',120)
tx(c,'creatividad',540,1120,132,13);tx(c,'completa',540,1220,82,34)
for j in range(24):
 ang=j*math.pi/12
 n=line(c,'Radio '+str(j),[[540+280*math.cos(ang),880+280*math.sin(ang)],[540+405*math.cos(ang),880+405*math.sin(ang)]],8, width=1.6)

# The phrase physically locks together; it remains the sole caption on this beat.
c=comp('03 - Todo encaje',76);green(c)
for j,(s,x,y) in enumerate([('que',300,790),('todo',670,930),('encaje',530,1115)]):
 n=tx(c,s,x,y,[64,170,235][j],j*4)
 reveal(n,j*4,20,'x' if j!=1 else 'y',[-460,280,550][j])
ring(c,'Anillo de unión',540,945,380,0)
n=ellipse(c,'Punto de cierre',540,565,14,col=W,a=22)
anim(n,'pos',[22,36,47],[[160,945],[270,674],[540,565]],'flow')
n=line(c,'Cierre horizontal',[[180,1185],[895,1185]],34,width=2)
anim(n,'opacity',[53,75],[1,.3])

# One system branches into four outputs: authentic assets + readable typography.
hub=comp('04 - Sistemas Visual Hub',204);green(hub)
network=comp('04A - Sistema y salidas',204,2200,2400)
for j,(s,x,y,asset) in enumerate([
 ('imágenes',650,590,'toma-02.jpg'),('vídeos',1550,590,'toma-03.jpg'),
 ('avatares',650,1710,'toma-07.jpg'),('anuncios',1550,1710,'toma-05.jpg')]):
 line(network,'Rama '+s,[[1100,1200],[1100,y],[x,y]],0,width=2)
 ring(network,'Nodo '+s,x,y,205,0)
 n=pframe(network,'Original '+s,asset,x,y,220,0);n['circleClip']=True
 n=tx(network,s,x,y+295,105,0);anim(n,'opacity',[0,25+j*22,39+j*22],[.35,.35,1])
tx(network,'1',1100,1260,310,0);tx(network,'sistema',1100,1370,82,0)
n=nested(hub,'Viaje por el sistema','04A - Sistema y salidas',540,945,.44,threeD=True)
# The camera starts wide, visits the outputs in spoken order, then reveals the complete system.
anim(n,'pos',[0,24,52,86,115,145,180,203],[[540,940,0],[760,1270,0],[760,1270,0],[340,1270,0],[760,710,0],[340,710,0],[540,950,0],[540,950,0]],'flow')
anim(n,'scale',[0,24,52,86,115,145,180,203],[[.44,.44],[.75,.75],[.75,.75],[.75,.75],[.75,.75],[.75,.75],[.42,.42],[.43,.43]],'flow')
anim(n,'rx',[0,24,86,145,180],[8,0,-3,3,0],'flow');anim(n,'ry',[0,24,86,145,180],[-8,0,3,-3,0],'flow')
tx(hub,'para producir',540,450,64,0,30)
tx(hub,'con IA',540,1530,100,175,204)

# Production line becomes the offer; small copy shares the number's optical hierarchy.
c=comp('05 - Produccion y oferta',276);green(c)
for j in range(9):
 x=-100+j*170;ring(c,'Eslabon '+str(j),x,1000,45,0,105)
 if j<8:line(c,'Vinculo '+str(j),[[x+45,1000],[x+125,1000]],0,105,width=2)
tx(c,'una línea de',540,730,70,0,63)
n=tx(c,'producción',540,920,177,0,63);reveal(n,0,13,'x',200)
tx(c,'Entra en',540,670,58,63,117)
n=tx(c,'Visual Hub',540,875,178,63,130);reveal(n,63,12,'y',100)
anim(n,'pos',[108,142],[[540,875],[540,550]],'out');anim(n,'scale',[108,142],[[1,1],[.5,.5]],'out')
for j in range(30):
 ang=j*math.pi/15
 n=line(c,'Radio precio '+str(j),[[540+302*math.cos(ang),960+302*math.sin(ang)],[540+422*math.cos(ang),960+422*math.sin(ang)]],109,width=1.6)
 n=ellipse(c,'Punto precio '+str(j),540+422*math.cos(ang),960+422*math.sin(ang),12,col=M,a=116)
 anim(n,'opacity',[116,131],[0,1])
n=tx(c,'39',550,1070,370,112);reveal(n,112,16,'y',150)
tx(c,'$',306,963,92,119);tx(c,'al mes',550,1170,70,154)
tx(c,'dólares',550,1170,70,133,154)
n=tx(c,'Puedes cancelar',540,1390,74,172);reveal(n,172,10,'x',-70)
n=tx(c,'cuando quieras',540,1475,82,215);reveal(n,215,10,'y',60)

# Complete fresh master on the Remotion cut, with native typography overlays.
master=comp(S['master'],N)
node(master,'video','Montaje Remotion',(540,960),asset='Montaje-AD3.mp4',anchor=[540,960])
node(master,'audio','Mezcla - voz original',(540,960),asset='Mezcla-Final.wav',anchor=[0,0])
events=[('ensamblaje','01 - Se monta solo',642,830),('creatividad','02 - Una creatividad',988,1054),('encaje','03 - Todo encaje',1186,1262),('sistemas','04 - Sistemas Visual Hub',1508,1712),('oferta','05 - Produccion y oferta',1886,2162)]
for key,src,a,b in events:
 nested(master,key,src,540,960,a=a,b=b,startTime=a/F)
 S['events'][key]={'from':a,'to':b,'dropCaptions':True}

(R/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2));print('Designed',len(S['comps']),'comps',sum(len(c['layers']) for c in S['comps'].values()),'layers')
