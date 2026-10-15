from pathlib import Path
import json
from PIL import ImageFont
R=Path(__file__).resolve().parents[1];F=48
S=json.load(open(R/'ae/design.json'));T=json.load(open(R/'remotion/src/timeline.json'));c=S['comps'][S['master']]
# Cadence based on the recorded phrases. Larger impact words alternate with compact connectors.
chunks={
1:[(0, .70,'Tengo que'),(.70,1.6,'revelarte algo'),(2.4,2.72,'No'),(3.24,3.92,'Este anuncio'),(3.92,4.34,'no solo'),(4.34,4.94,'se ha hecho'),(4.94,5.4,'con IA'),(5.9,6.54,'sino que además'),(6.54,7.0,'se ha montado'),(7,7.82,'solo')],
2:[(.05,.80,'Esta'),(.80,1.22,'persona'),(1.22,1.95,'no es real'),(2.54,3.28,'Este escenario'),(3.28,3.74,'tampoco')],
3:[(.05,1.08,'Estos planos'),(1.08,1.94,'no se han grabado'),(2.78,3.26,'Y esta voz'),(3.26,3.76,'tampoco')],
4:[(.05,1.08,'Hasta los cortes'),(1.08,2.02,'y los subtítulos'),(2.02,2.84,'se ensamblan'),(2.84,3.93,'automáticamente')],
5:[(.18,.68,'No son clips'),(.68,1.28,'sueltos'),(1.34,1.90,'personaje'),(2.08,2.48,'escenas'),(2.58,2.92,'voz'),(2.92,3.45,'y montaje'),(3.6,4.7,'Una creatividad completa')],
6:[(.05,.94,'Generar'),(.94,1.30,'con IA'),(1.30,2.24,'es fácil'),(2.78,3.28,'Lo difícil'),(3.28,3.80,'es que'),(3.80,4.76,'todo encaje')],
7:[(.05,.96,'Misma persona'),(1.20,1.78,'mismo look'),(2.18,2.72,'Sin volver'),(2.72,3.06,'a empezar'),(3.06,3.82,'con cada plano')],
8:[(.05,.40,'En'),(.40,.98,'Visual Hub'),(.98,1.72,'compartimos'),(1.72,2.06,'los sistemas'),(2.06,2.88,'para producir'),(2.88,3.46,'imágenes'),(3.66,4.03,'vídeos'),(4.20,4.66,'avatares'),(4.66,5.32,'y anuncios'),(5.32,5.85,'con IA')],
9:[(.05,.80,'Si tienes una'),(.80,1.32,'agencia'),(1.46,1.89,'una marca'),(1.89,2.68,'o produces para'),(2.68,3.24,'clientes'),(3.30,3.94,'necesitas una'),(3.94,4.74,'línea de producción')],
10:[(.05,.40,'Entra en'),(.40,1.14,'Visual Hub'),(1.60,2.48,'39 dólares'),(2.48,2.96,'al mes'),(2.96,4.08,'Puedes cancelar'),(4.08,4.95,'cuando quieras')]
}
def mapped(i,a,b):
 out=[]
 for seg in T['video']:
  if seg['clip']!=i:continue
  aa=max(a*F,seg['sourceFrame']);bb=min(b*F,seg['sourceEnd'])
  if bb>aa:out.append((round(seg['from']+aa-seg['sourceFrame']),round(seg['from']+bb-seg['sourceFrame'])))
 return out
fontpath=R.parents[1]/'ad1-reedit/assets/Display-Bold.otf'
records=[];idx=0
for i,groups in chunks.items():
 for a,b,s in groups:
  for start,end in mapped(i,a,b):
   records.append({'text':s,'from':start,'to':end,'clip':i})
   if i==1 and a<2:continue # The whispered close-up fills the safe image area with her face.
   ranges=[(start,end)]
   for e in S['events'].values():
    ranges=[v for aa,bb in ranges for v in ([(aa,bb)] if bb<=e['from'] or aa>=e['to'] else ([(aa,e['from'])] if aa<e['from'] else [])+([(e['to'],bb)] if bb>e['to'] else []))]
   for aa,bb in ranges:
    if bb-aa<5:continue
    idx+=1
    hero=s in ['solo','no es real','tampoco','sueltos','es fácil','mismo look','agencia','clientes']
    size=155 if hero else 108
    while ImageFont.truetype(str(fontpath),size).getlength(s)-(len(s)-1)*size*.045>895:size-=1
    y={1:1435,2:1380,3:1450,5:1420,6:1410,7:1400,8:1330,9:1390}.get(i,1400)
    col='#273e1b' if i==5 else '#f0f7eb'
    if s in ['no es real','es fácil','agencia']:col='#92bd65'
    n={'type':'text','name':f'SUB {idx:02d} - {s}','text':s,'pos':[540,y],'from':aa,'to':bb,'size':size,'color':col,'font':'bold','track':-45,'align':'center','shadow':[0,3,4,'#182015',.65] if i!=5 else [0,1,1,'#e9dfcb',.3],'textStroke':['#20271b',1.1] if i!=5 else ['#ded1b5',.7]}
    c['layers'].append(n)
    axis='y' if idx%3==0 else 'x';delta=75 if axis=='y' else -110 if idx%3==1 else 110
    p0=n['pos'].copy();p0[0 if axis=='x' else 1]+=delta
    d=min(8,bb-aa-1)
    n['anim']={'pos':{'frames':[aa,aa+d],'values':[p0,n['pos']],'ease':'out'},'opacity':{'frames':[aa,aa+2],'values':[0,1],'ease':'linear'},'blur':{'frames':[aa,aa+d],'values':[5,0],'ease':'out'}}
def ts(f):
 ms=round(f/F*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
(R/'output/AD3-Pipeline-V4.srt').write_text('\n\n'.join(f"{j+1}\n{ts(r['from'])} --> {ts(r['to'])}\n{r['text']}" for j,r in enumerate(records))+'\n')
(R/'analysis/captions.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));(R/'ae/design.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
print('Native captions',idx,'all phrases',len(records))
