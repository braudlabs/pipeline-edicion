"""Surgical second review: consumption gesture, coherent camera, no duplicate copy."""
from pathlib import Path
import json,copy
R=Path(__file__).resolve().parents[1]
helpers=(R/'scripts/design.py').read_text().split('# Semantic objects')[0]
exec(compile(helpers,str(R/'scripts/design.py'),'exec'))
S=json.loads((R/'ae/design-v1.json').read_text())
before=copy.deepcopy(S)

# The existing six photographic credits consolidate into one stack and are spent.
# No repeated type, labels, arbitrary counters or newly invented evidence.
c=S['comps']['MG - Creditos']
c['layers']=[n for n in c['layers'] if not n['name'].startswith('Generaciones plano')]
c['camera']=focus_camera([0,20,67,102,196],[[540,940,-1050],[540,960,-1900],[540,960,-1900],[540,960,-1800],[540,960,-1800]])
for n in c['layers']:
 if n['name'].startswith('créditos |'):n['to']=101
 if not n['name'].startswith('Ficha en profundidad '):continue
 i=int(n['name'].split()[-1]);p=n['pos'].copy();a=n['from'];consume=110+i*12;end=consume+23
 stack=[540+(i-2.5)*28,820-(i-2.5)*27,100+i*55]
 n['to']=end+1
 anim(n,'pos',[a,28+i*3,65,102,consume,end],[[p[0],p[1]+240,p[2]],p,p,stack,stack,[540,1110,330]])
 factor=520/n['w']
 anim(n,'scale',[a,65,102,consume,end],[[1,1],[1,1],[factor,factor],[factor,factor],[.035,.035]])
 anim(n,'rot',[a,65,102,consume,end],[-18+i*12,i*7,(i-2.5)*7,(i-2.5)*7,32])
 anim(n,'opacity',[a,25+i*3,102,end-5,end],[0,.85,1,1,0])
 # All trajectories now have one purposeful turn: field -> stack -> consumption.
 anim(n,'blur',[a,28+i*3,consume,end],[6,0,0,5])

# A dark, shallow aperture gives the vanishing credits a destination.
tmp={'duration':196,'layers':[]}
n=ellipse(tmp,'Sombra de la ranura',540,1130,720,88,col='#000000',a=82,b=196,blur=24,opacity=.6)
anim(n,'opacity',[82,102],[0,.6])
n=ellipse(tmp,'Borde metalico de consumo',540,1100,660,92,col='#523821',a=82,b=196,stroke='#bc7f38',strokeWidth=2)
anim(n,'scale',[82,101],[[.3,.3],[1,1]]);anim(n,'opacity',[82,101],[0,.85])
n=ellipse(tmp,'Interior de la ranura',540,1097,630,67,col='#08090b',a=82,b=196)
anim(n,'scale',[82,101],[[.3,.3],[1,1]]);anim(n,'opacity',[82,101],[0,1])
c['layers'][1:1]=tmp['layers']

# Time and money: the products share a retreat in depth, followed by a clear hold.
c=S['comps']['MG - Tiempo']
c['camera']=focus_camera([0,23,112],[[540,960,-1460],[540,960,-1850],[540,960,-1850]])
for n in c['layers']:
 if n['name']=='Reloj protagonista':
  n['to']=89
  anim(n,'pos',[0,22,65,89],[[-200,870,-90],[270,870,-90],[270,870,-90],[270,870,1950]])
  anim(n,'rot',[0,22,65,89],[-16,-7,-7,-7]);anim(n,'opacity',[0,7,72,89],[0,1,1,0])
 if n['name']=='Dinero entra del fondo':
  n['to']=89
  anim(n,'pos',[27,49,65,89],[[822,1120,850],[822,1120,130],[822,1120,130],[822,1120,2050]])
  anim(n,'rot',[27,49,65,89],[-12,7,7,7]);anim(n,'opacity',[27,39,72,89],[0,1,1,0])
 if n['name'] in ['Tiempo','Dinero']:
  anim(n,'opacity',[n['from'],n['from']+7,72,87],[0,1,1,0])

# Post motion: camera does the travel; page faces stay coherent and still.
c=S['comps']['MG - Cuentas']
cam=c['camera'];remove=cam['frames'].index(117)
cam['frames'].pop(remove);cam['values'].pop(remove)
cam['values']=[[p[0],960,p[2]] for p in cam['values']]
cam['values'][-1]=cam['values'][-2][:]
cam['spatialOverrides']={
 '102':{'outTangent':[450,0,-1250]},
 '139':{'inTangent':[-450,0,-1250]}
}
for n in c['layers']:
 if not n['name'].startswith('Publicacion emerge '):continue
 a=0 if n['name'].endswith('kurt') else 121
 x=540 if a==0 else 2180
 n['anim'].pop('ry',None);n['ry']=0
 anim(n,'pos',[a+38,a+64],[[x,880,190],[x,845,190]])
 anim(n,'scale',[a+38,a+64],[[.60,.60],[.78,.78]])

# Original community screenshot: one frontal dolly, one readable pause, one exit.
c=S['comps']['MG - Comunidad']
c['camera']=focus_camera([0,31,111,145],[[540,960,-1430],[540,960,-1960],[540,960,-1960],[540,960,-1670]])
for n in c['layers']:
 if n['name']=='Pagina de comunidad real':
  n['pos']=[540,860,50];n['anim']={};n.pop('rx',None);n.pop('ry',None)
  # Only the camera changes apparent size. The page is never independently rotated.
  anim(n,'opacity',[0,5],[0,1])

# The spoken graphic replaces the subtitle, so wording is never echoed below it.
main=S['comps'][S['master']]
remove_groups={'SUB 32.','SUB 73.','SUB 76.'}
removed=[n['name'] for n in main['layers'] if any(n['name'].startswith(p) for p in remove_groups)]
main['layers']=[n for n in main['layers'] if n['name'] not in removed]

# Caption crosses a footage/graphic cut: put its graphic half below the white page.
for n in main['layers'][:]:
 if n['name'].startswith('SUB 62.'):
  part=copy.deepcopy(n);n['to']=2338
  part.update(name=n['name']+' MG',pos=[n['pos'][0],1368],**{'from':2338})
  part['anim']={};part['opacity']=1;main['layers'].append(part)
# Reinstate the final spoken 'generaciones' as an ordinary caption, no typographic stack.
model=copy.deepcopy(next(n for n in main['layers'] if n['name']=='SUB 33.1 | generaciones'))
model.update(name='SUB 34.0 | generaciones',pos=[540,1368],**{'from':1183,'to':1208})
model['anim']={}
anim(model,'pos',[1183,1190],[[575,1368],[540,1368]])
anim(model,'opacity',[1183,1186],[.5,1]);main['layers'].append(model)

# The large '50' belongs to the board; the line underneath names what is counted.
for n in main['layers']:
 if n['name']=='SUB 75.0 | 50':
  removed.append(n['name'])
 if n['name'] in ['SUB 75.1 | generaciones','SUB 75.2 | para']:
  # Keep the remaining two words together, centered as one phrase.
  widths=[word_width('generaciones',73),word_width('para',73)]
  gap=ImageFont.truetype(str(A/'Display-Bold.otf'),73).getlength(' ')-73*.028
  left=(1080-sum(widths)-gap)/2
  idx=0 if 'generaciones' in n['name'] else 1
  x=left+widths[0]/2 if idx==0 else left+widths[0]+gap+widths[1]/2
  delta=x-n['pos'][0];n['pos'][0]=x
  for p in n['anim']['pos']['values']:p[0]+=delta
main['layers']=[n for n in main['layers'] if n['name'] not in removed]

# Preserve the cards, identity collage, native board, footage, audio and other scenes.
changed=['MG - Creditos','MG - Tiempo','MG - Cuentas','MG - Comunidad']
assert S['comps']['MG - Sistemas']==before['comps']['MG - Sistemas']
assert S['comps']['OBJ - Intentos']==before['comps']['OBJ - Intentos']
(R/'ae/design-v2.json').write_text(json.dumps(S,ensure_ascii=False,indent=2))
(R/'analysis/v2/change-map.json').write_text(json.dumps({'changedComps':changed,'removedCaptionLayers':removed,'restoredCaption':'SUB 34.0 | generaciones','preservedMotionComps':['MG - Sistemas','OBJ - Intentos'],'designDecision':'Replace repeated typography with the existing credits consolidating and being consumed; fixed page faces, camera-only page travel; remove lower caption when the graphic carries that phrase.'},ensure_ascii=False,indent=2))
print('V2 design ready:',len(removed),'duplicated caption layers removed')
