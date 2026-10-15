from pathlib import Path
import json,re,unicodedata,math
R=Path(__file__).resolve().parent
words=json.load(open(R/'study/aligned-words.json'))['words']
def norm(s):return re.sub(r'[^a-z0-9]','', ''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c)))
def find(s,after=0):
 target=[norm(x) for x in s.split()]; ws=[norm(w['text']) for w in words]
 for i,w in enumerate(words):
  if w['oldStart']>=after and ws[i:i+len(target)]==target:return i,i+len(target)-1
 raise ValueError((s,after))
def span(s,after=0):
 i,j=find(s,after);return words[i]['start'],words[j]['end']
def start(s,after=0):return span(s,after)[0]
def end(s,after=0):return span(s,after)[1]
def q(t):return max(0,min(2121,round(t*24)))/24
cues=[]
def add(text,a,b,y=1210,size=103,x=540,color='white',motion='cut',group=None,**kw):
 c=dict(id=f'T{len(cues):03d}',text=text,start=q(a),end=q(b),x=x,y=y,size=size,color=color,motion=motion,group=group or f'phrase{len(cues)}',**kw)
 if c['end']<=c['start']:raise ValueError(c)
 cues.append(c);return c
used=set()
def rail(s,after=0,y=1220,size=102,motion='cut',color='white',hold=.10):
 i,j=find(s,after);used.update(range(i,j+1));a,b=span(s,after);nexta=words[j+1]['start'] if j+1<len(words) else 88.375
 return add(s,a,min(b+hold,nexta),y,size,color=color,motion=motion)
def group(s,after=0):
 i,j=find(s,after);used.update(range(i,j+1));return words[i]['start'],words[j]['end']
# Hook: coherent size ladder, compact construction, common exit.
a,b=group('Si eres una agencia de contenido');z=start('y tus')
add('Si eres una',a,z,y=950,size=83,motion='rise',group='hook')
add('agencia',start('agencia'),z,y=1090,size=200,color='lime',motion='rise',group='hook')
add('de contenido',start('de contenido'),z,y=1230,size=110,motion='slide',group='hook')
for s in ['y tus creativos','se ven como','el de al lado','el de la esquina','el de ahí','el de allá','lo único que te diferencia','es el']:
 rail(s,y=1190,size=95 if len(s)>22 else 106,motion='rise' if s=='y tus creativos' else 'cut')
a,b=group('precio y qué tan rápido puedes sacar los creativos',after=7)
add('precio',a,b+.08,y=1110,size=182,color='lime',motion='punch',group='tradeoff')
add('y qué tan',start('y qué tan'),start('rápido'),y=1252,size=82,group='tradeoff')
add('rápido',start('rápido'),b+.08,y=1275,size=182,color='lime',motion='slide',group='tradeoff')
add('puedes sacar',start('puedes sacar'),start('los creativos',after=9),y=1414,size=90,group='tradeoff')
add('los creativos.',start('los creativos',after=9),b+.08,y=1414,size=90,group='tradeoff')
rail('Pero tranquilo',after=10,y=1190,motion='rise')
a,b=group('Tenemos tu solución',after=11)
add('tenemos tu',a,b+.05,y=1150,size=88,motion='rise',group='solution')
add('solución.',start('solución',after=11),b+.05,y=1300,size=193,color='lime',motion='punch',group='solution')
for s in ['Ya se lo explico yo','Pelillos','Vamos a hacer que','tus creativos se vean','literalmente','como el que estás viendo']:
 rail(s,after=13,y=1330,size=91 if len(s)>22 else 103,motion='slide' if s=='literalmente' else 'cut')
a,b=group('Calidad Premium que trae clientes Premium',after=18)
add('calidad',a,start('que trae',after=19),y=1230,size=88,motion='rise',group='premium')
add('premium',start('Premium',after=18),b+.06,y=1370,size=172,color='lime',motion='rise',group='premium')
add('que trae clientes',start('que trae',after=19),b+.06,y=1230,size=88,group='premium')
a,b=group('no percebes',after=20);add('no percebes.',a,b+.08,y=1370,size=138,motion='punch',group='percebes')
rail('Instalaremos una maquinita',after=22,y=1350,size=90,motion='rise')
a,b=group('que te genera creativos casi listos para publicar',after=23)
add('que te',a,start('genera',after=23),y=1230,size=99,group='machine')
add('genera',start('genera',after=23),b+.08,y=1190,size=141,motion='slide',group='machine')
add('creativos',start('creativos',after=24),b+.08,y=1340,size=174,color='lime',motion='rise',group='machine')
add('casi listos',start('casi listos'),start('para publicar'),y=1475,size=85,group='machine')
add('para publicar.',start('para publicar'),b+.08,y=1475,size=85,group='machine')
for s in ['Eso sí','con un buen operador detrás','Por eso']:
 rail(s,after=26,y=1350,size=87 if len(s)>23 else 103)
a,b=group('formaremos personalmente a tu equipo',after=29)
add('formaremos',a,b+.08,y=1260,size=136,motion='slide',group='team')
add('personalmente',start('personalmente'),start('a tu equipo'),y=1400,size=94,group='team')
add('a tu equipo',start('a tu equipo'),b+.08,y=1400,size=130,color='lime',motion='rise',group='team')
rail('para que sepa utilizarlo',after=30,y=1350,size=95)
rail('Y antes de seguir',after=32,y=1350,size=96)
group('te explico lo que nadie te cuenta',after=33) # face fills the screen
for s in ['No te creas que','es abrir Higgsfield','generar un poco','y en']:
 rail(s,after=35,y=1390,size=97,motion='rise' if s=='No te creas que' else 'cut')
a,b=group('10 minutos');add('10',a,b+.04,y=1260,size=252,color='lime',motion='punch',group='ten')
add('minutos',start('minutos'),b+.04,y=1420,size=96,group='ten')
a,b=group('BOOM');add('¡BOOM!',a,b+.08,y=1350,size=198,motion='punch',group='boom')
a,b=group('Creativos como churros',after=40);add('creativos',a,b+.07,y=1300,size=132,motion='rise',group='churros');add('como churros.',start('como churros',after=40),b+.07,y=1440,size=130,color='lime',motion='slide',group='churros')
rail('para tu negocio',after=41,y=1390)
a,b=group('Ni de coña',after=42);add('Ni de coña.',a,b+.08,y=1390,size=157,motion='punch',group='nope')
for s in ['Si fuese así','coge a tu abuela','le activas el micro','y que le diga a']:
 rail(s,after=43,y=1350,size=98,motion='cut')
a,b=group('ChatGPT',after=46);add('ChatGPT',a,47.875,y=1290,size=149,motion='rise',group='chatgpt')
a,b=group('Hazme un anuncio',after=47)
add('Hazme',a,start('un anuncio',after=48),y=1270,size=110,motion='rise',group='grandma')
add('un anuncio',start('un anuncio',after=48),start('UGC',after=49),y=1170,size=89,motion='rise',group='grandma')
a,b=group('hiperrealista',after=48);add('hiperrealista',a,start('UGC',after=49),y=1295,size=129,color='lime',motion='slide',group='grandma')
a,b=group('UGC',after=49);add('UGC',a,start('bla',after=50),y=1280,size=167,color='lime',motion='punch',group='grandma')
ix,j= find('bla bla bla',after=50);used.update(range(ix,j+1));finish=start('pero',after=51)
for k in range(3):add('bla',words[ix+k]['start'],finish,x=345+195*k,y=1290,size=118,motion='punch',group='blah')
a,b=group('pero ya',after=51);add('¡pero',a,52.5,y=1195,size=86,group='ya');add('YA!',start('ya',after=51),52.5,y=1335,size=205,color='lime',motion='punch',group='ya')
rail('Evidentemente',after=56,y=1380,size=105,motion='cut')
rail('lo que prevalece',after=56,y=1380,size=103)
rail('es el',after=57,y=1380)
a,b=group('criterio visual',after=57);add('criterio',a,b+.15,y=1285,size=154,motion='rise',group='criterion');add('visual.',start('visual',after=58),b+.15,y=1440,size=169,color='lime',motion='slide',group='criterion')
for s in ['saber cómo formular','buenas historias']:
 rail(s,after=59,y=1380,size=100)
group('y dejar que el cabeza kiwi y el pelos locos este que llevan meses y meses haciéndolo',after=61)
for s in ['te ahorren','todo el trabajo sucio']:
 rail(s,after=65,y=1320,size=99,motion='rise' if s=='te ahorren' else 'cut')
a,b=group('La IA es un traductor',after=67);add('La IA es un',a,b+.04,y=1270,size=89,motion='rise',group='translator');add('traductor.',start('traductor',after=68),b+.04,y=1415,size=160,color='lime',motion='slide',group='translator')
rail('Si metes',after=69,y=1380)
a,b=group('ideas de mierda',after=69);add('ideas de',a,start('sacas',after=70),y=1240,size=91,group='cause');add('mierda.',start('mierda',after=70),end('sacas mierda',after=70)+.04,y=1390,size=178,motion='punch',group='cause');group('sacas mierda',after=70);add('sacas',start('sacas',after=70),end('sacas mierda',after=70)+.04,y=1240,size=91,group='cause')
rail('Si metes',after=71,y=1390)
a,b=group('conceptos con criterio',after=72);add('conceptos',a,b+.05,y=1270,size=124,motion='rise',group='good');add('con criterio',start('con criterio',after=72),b+.05,y=1410,size=141,color='lime',motion='slide',group='good')
rail('sacas',after=73,y=1390)
a,b=group('obras de arte',after=73);add('obras de',a,b+.10,y=1260,size=97,motion='rise',group='art');add('arte.',start('arte',after=74),b+.10,y=1460,size=251,color='lime',motion='rise',group='art')
for s in ['Y tus clientes','dejan de pensar','que eres una mierda','Ese es el criterio','que instalamos','en tu negocio']:
 rail(s,after=74,y=1410,size=96 if len(s)>20 else 103)
rail('Venga',after=80,y=940,motion='punch')
a,b=group('Agenda ya una llamada',after=80);add('agenda ya una',a,b+.04,y=910,size=88,motion='rise',group='call');add('llamada.',start('llamada',after=81),b+.04,y=1050,size=175,color='lime',motion='slide',group='call')
for s in ['y vemos qué encaje','puede tener esto','con tu negocio','Si sirve','te lo decimos','en la misma llamada','Y si no']:
 # The source transcript has "que" (unaccented); norm handles this.
 rail(s,after=81,y=1060,size=98,motion='cut')
a,b=group('también',after=87);add('también.',a,88.25,y=1060,size=161,color='lime',motion='rise',group='end')
# Enforce one text at a time at a common anchor, including retained components.
for i,c in enumerate(cues):
 for d in cues[i+1:]:
  if c['x']==d['x'] and abs(c['y']-d['y'])<.1 and c['start']<d['start']<c['end']:c['end']=d['start']

# Optical layout corrections verified in native AE.
fix={'T009': ('lo único que\nte diferencia', 100, 1140), 'T022': ('tus creativos se vean', 98, 1330), 'T024': ('como el que\nestás viendo', 100, 1280), 'T029': ('Instalaremos una\nmaquinita', 100, 1295), 'T036': ('con un buen\noperador detrás', 103, 1300), 'T041': ('para que sepa\nutilizarlo', 100, 1300)}
for c in cues:
 if c['id'] in fix:
  s,size,y=fix[c['id']];c['aeLayerName']=c['id']+' — '+c['text'];c.update(text=s,size=size,y=y)

# Ale prefers V01's criterion composition; apply only to this block.
for c in cues:
 if c['group']=='criterion':
  y,size=(655,211) if c['text']=='criterio' else (925,287)
  c.update(y=y,size=size,color='white',motion='rise',baselineAnchor=True,tracking=-55,masked=True,outlineWidth=1.65,outlineOpacity=90)
(R/'spec.json').write_text(json.dumps({'fps':24,'frames':2121,'design':'A Voice, compact native typography','cues':cues,'wordAlignment':'study/aligned-words.json','omittedForVisualAction':[33.6,35.7,52.5,56.375,61.38,65.7]},ensure_ascii=False,indent=2))
print(len(cues),'elements; uncovered words:',[(w['text'],w['start']) for i,w in enumerate(words) if i not in used])
