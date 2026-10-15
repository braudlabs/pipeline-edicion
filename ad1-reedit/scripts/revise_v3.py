"""New credit concept: photographic generation workstation and depletion gesture."""
from pathlib import Path
import json,copy,math
R=Path(__file__).resolve().parents[1]
exec(compile((R/'scripts/design.py').read_text().split('# Semantic objects')[0],str(R/'scripts/design.py'),'exec'))
S=json.loads((R/'ae/design-v2.json').read_text());old=copy.deepcopy(S)
WHITE='#f2efe9';BLACK='#171817';ACCENT='#e98a36'

# Four independently replaceable photographic attempts, from supplied footage.
sources=['chef-1.jpg','attempt-2.jpg','attempt-3.jpg','attempt-4.jpg']
for i,asset in enumerate(sources,1):
 c=comp('OBJ - Intento fotografico '+str(i),196,768,672)
 rect(c,'Superficie fotografica',0,0,768,672,'#141414')
 media(c,'Fotografia sustituible '+str(i),asset,384,[485,650,500,485][i-1],768)

# Content moves inside a fixed viewport. The interface itself never slides or flexes.
c=comp('OBJ - Visor de intentos',196,768,672)
rect(c,'Fondo del visor',0,0,768,672,'#151411')
beats=[0,67,101,139]
for i,a in enumerate(beats):
 end=beats[i+1]+14 if i<3 else 196
 n=nested(c,'Resultado visible '+str(i+1),'OBJ - Intento fotografico '+str(i+1),384,336,1,a,end)
 fs=[a,a+13] if a else [0,23];values=[[1162,336],[384,336]] if a else [[384,336],[384,336]]
 if i<3:fs += [beats[i+1],beats[i+1]+14];values += [[384,336],[-440,336]]
 anim(n,'pos',fs,values)
 if a:anim(n,'blur',[a,a+13],[15,0])

c=comp('OBJ - Estudio de generaciones',196,840,930)
rect(c,'Cuerpo de interfaz',0,0,840,930,'#202220',round=26,stroke='#444740',strokeWidth=2)
n=nested(c,'Ventana de fotografia','OBJ - Visor de intentos',420,372,1,round=16)
# Thin corner marks identify the viewport, rather than adding a headline.
for i,(x,y,sx,sy) in enumerate([(53,52,1,1),(787,52,-1,1),(53,692,1,-1),(787,692,-1,-1)]):
 path(c,'Marco de enfoque '+str(i),[[x,y+sy*24],[x,y],[x+sx*24,y]],'#f5eee5',2,opacity=.68)
# A compact resources display: qualitative depletion, no invented price or quantity.
rect(c,'Fondo del saldo',58,793,500,17,'#53554d',round=8)
n=rect(c,'Saldo de creditos',58,793,500,17,ACCENT,round=8)
anim(n,'scale',[0,67,79,101,113,139,154,172,186],[[1,1],[1,1],[.65,1],[.65,1],[.30,1],[.30,1],[.06,1],[.06,1],[.002,1]])
path(c,'Indicador energia',[[64,748],[89,718],[82,741],[103,741],[77,771],[84,748],[64,748]],WHITE,2,closed=True)
for i in range(3):
 rect(c,'Trazo de ajuste '+str(i),143,729+i*18,138-i*21,5,'#7a7d72',round=2)
# Regeneration control, built from a native circular arrow and a pressure state.
n=rect(c,'Boton repetir',641,739,139,139,ACCENT,round=28)
anim(n,'scale',[0,64,67,73,98,101,107,136,139,145],[[1,1],[1,1],[.93,.93],[1,1],[1,1],[.93,.93],[1,1],[1,1],[.93,.93],[1,1]])
pts=[[710+30*math.cos(math.radians(a)),808+30*math.sin(math.radians(a))] for a in range(-40,261,10)]
path(c,'Arco repetir',pts,BLACK,7)
path(c,'Flecha repetir',[[713,769],[731,788],[705,790]],BLACK,7)
path(c,'Linea de estado',[[58,865],[558,865]],'#777b70',2,opacity=.55)

# Cursor presses line up with the existing sound design at 67, 101 and 139 frames.
n=node(c,'path','Cursor de generacion',(925,997),40,196,points=[[0,0],[0,70],[19,54],[36,85],[48,79],[31,48],[57,48]],closed=True,color=WHITE,stroke=BLACK,strokeWidth=3,shadow=[0,2,3,'#000000',.6])
anim(n,'pos',[40,60,67,73,101,107,139,145,163,188],[[925,997],[735,823],[730,829],[735,823],[730,829],[735,823],[730,829],[735,823],[820,906],[1030,1120]])
anim(n,'scale',[40,64,67,73,98,101,107,136,139,145],[[1,1],[1,1],[.90,.90],[1,1],[1,1],[.90,.90],[1,1],[1,1],[.90,.90],[1,1]])
for f in [67,101,139]:
 n=ellipse(c,'Respuesta al clic '+str(f),736,824,24,col=None,a=f,b=f+15,stroke=WHITE,strokeWidth=2)
 anim(n,'scale',[f,f+15],[[1,1],[4,4]]);anim(n,'opacity',[f,f+15],[.8,0])

c=comp('MG - Creditos',196)
node(c,'gradient','Lienzo claro',(540,960),w=1080,h=1920,anchor=[540,960],color='#faf8f3',endColor='#dfdfd5',center=[540,650],radius=1500)
# History sits in actual depth and becomes visible as the camera opens the stage.
for i,(x,a,z,angle) in enumerate([(245,67,460,-9),(840,101,470,8),(175,139,770,-13)]):
 n=three(nested(c,'Historial fotografico '+str(i+1),'OBJ - Intento fotografico '+str(i+1),x,778,.63,a,196,round=18,shadow=[0,20,24,'#292a21',.23]),z)
 final=[[230,510,80],[850,510,80],[230,1080,80]][i]
 anim(n,'pos',[a,a+18,160,186],[[540,808,z],[x,778,z],[x,778,z],final])
 anim(n,'ry',[a,a+18,160,186],[0,angle,angle,0]);anim(n,'rot',[a,a+18,160,186],[0,angle*.4,angle*.4,0])
 anim(n,'scale',[a,160,186],[[.63,.63],[.63,.63],[.72,.72]])
 anim(n,'opacity',[a,a+10],[0,1])
n=three(nested(c,'Estudio completo','OBJ - Estudio de generaciones',540,822,1,0,196,shadow=[0,24,24,'#323327',.26]),0)
anim(n,'pos',[0,160,186],[[540,822,0],[540,822,0],[850,1080,0]])
anim(n,'scale',[0,160,186],[[1,1],[1,1],[.72,.72]])
# One pull-back reveals the workbench; a second reveals the accumulated attempts.
c['camera']=focus_camera([0,29,160,186,196],[[540,1050,-1510],[540,960,-1900],[540,960,-1900],[540,960,-2250],[540,960,-2250]])

# A direct cut keeps dark captions on the light graphic from its first frame.
for n in S['comps'][S['master']]['layers']:
 if n.get('name')=='ESCENA - credits':n['anim']['opacity']['values']=[1,1]

# Captions remain elegant dark ink on the light stage, including the full phrase.
m=S['comps'][S['master']]
v1=json.loads((R/'ae/design-v1.json').read_text())
for n in v1['comps'][S['master']]['layers']:
 if n['name'].startswith('SUB 32.'):
  m['layers'].append(copy.deepcopy(n))
for n in m['layers'][:]:
 if n['name'].startswith(('SUB 31.','SUB 32.','SUB 33.','SUB 34.')):
  n['color']=BLACK;n['textStroke']=[WHITE,.5];n['shadow']=[0,1,2,WHITE,.3]
 # The last six frames of the previous phrase cross the graphic cut.
 if n['name'].startswith('SUB 30.'):
  n['to']=1012
  part=copy.deepcopy(n);part['name']+=' MG';part['from']=1012;part['to']=1018;part['pos'][1]=1368;part['anim']={};part['color']=BLACK;part['textStroke']=[WHITE,.5];part['shadow']=[0,1,2,WHITE,.3]
  m['layers'].append(part)

changed=[k for k in old['comps'] if old['comps'][k]!=S['comps'][k]]
assert set(changed)=={'MG - Creditos',S['master']},changed
(R/'ae/design-v3.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'analysis/v3/concept.json').write_text(json.dumps({'concept':'Photo-generation workstation on a light canvas, new attempt per click, depleted resources and accumulating photographic history.','newAssets':sources[1:],'sourceFiles':['04a-otra-cocinera.mp4','04b-otra-cocinera.mp4','04c-otra-cocinera.mp4'],'sourceTimeSeconds':2,'newComps':[k for k in S['comps'] if k not in old['comps']],'changedComps':changed,'clickFrames':[67,101,139],'qualitativeGauge':True,'titles':False,'restoredVerbatimCaption':'absurda de créditos'},ensure_ascii=False,indent=2))
print('New concept:',len(c['layers']),'stage layers;',len(S['comps']),'total comps')
