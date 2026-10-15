"""Spec de AD5 v2 · sistema de la creatina: tipografía limpia sin caja, cifras en
anillo de línea fina, énfasis por escala. Acentos en azul. Fuente Optima."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from guion import GUION, comprobar                       # noqa: E402

R = Path(__file__).resolve().parents[1]
F, W, H, TOTAL = 48, 1080, 1920, 1148
NAVY='#0C2654'; AZUL='#3A7CE0'; CREMA='#F6F9FF'
SEG = {'04':0, '02':332, '03':574, '01':906}             # fotograma de inicio por clip
CARRIL = {'04':1520, '02':1470, '03':1600, '01':1430}    # medido plano a plano
def f(clip, s): return round(SEG[clip] + s*F)

if not comprobar(verboso=False):
    sys.exit('el guion no pasa la comprobación: revísalo antes de construir')

layers=[]
def L(**k): k.setdefault('anim',{}); layers.append(k); return k
def anim(p,fr,v,e='out'): return {p:{'frames':fr,'values':v,'ease':e}}

L(name='Montaje', type='video', asset='Montaje.mov', **{'from':0,'to':TOTAL},
  pos=[W/2,H/2], scale=[1,1], srcW=W, srcH=H)
L(name='Voz', type='audio', asset='Voz.wav', **{'from':0,'to':TOTAL}, pos=[W/2,H/2])

# ---------------------------------------------------- la línea de la mejilla
# Se traza siguiendo su yema (x688→830, y838→801) en «se metía dentro».
L(name='linea-1', type='path', points=[[688,838],[734,813],[783,800],[830,801]],
  stroke=AZUL, strokeWidth=7, **{'from':f('04',4.24),'to':f('04',6.85)},
  pos=[0,0], anchor=[0,0], trim=[f('04',4.24), f('04',5.00)], shadow=[0,6,9,NAVY,0.5])
L(name='linea-2', type='path', points=[[700,884],[742,866],[788,858]],
  stroke=AZUL, strokeWidth=6, **{'from':f('04',5.88),'to':f('04',6.85)},
  pos=[0,0], anchor=[0,0], trim=[f('04',5.88), f('04',6.16)], shadow=[0,5,8,NAVY,0.45])
L(name='linea-3', type='path', points=[[704,790],[744,768],[790,757]],
  stroke=AZUL, strokeWidth=6, **{'from':f('04',6.02),'to':f('04',6.85)},
  pos=[0,0], anchor=[0,0], trim=[f('04',6.02), f('04',6.30)], shadow=[0,5,8,NAVY,0.45])
# remate: la misma línea vuelve en «y la piel se ve» y se borra sola
L(name='linea-remate', type='path', points=[[706,842],[748,818],[790,806],[826,806]],
  stroke=AZUL, strokeWidth=7, **{'from':f('03',5.10),'to':f('03',6.10)},
  pos=[0,0], anchor=[0,0], trim=[f('03',5.54), f('03',6.02)], trimInvertido=True,
  shadow=[0,5,8,NAVY,0.4],
  anim=anim('opacity',[f('03',5.10),f('03',5.30),f('03',5.90),f('03',6.10)],[0,0.95,0.95,0]))

# ------------------------------------------- flecha fina al enlace, en «abajo»
L(name='flecha', type='path', points=[[-46,-30],[0,22],[46,-30]], stroke=AZUL,
  strokeWidth=7, **{'from':f('01',1.20),'to':f('01',2.80)}, pos=[540,1660], anchor=[0,0],
  opacity=0, shadow=[0,5,9,NAVY,0.45],
  anim={**anim('pos',[f('01',1.20),f('01',1.52),f('01',1.84),f('01',2.16)],
               [[540,1600],[540,1672],[540,1614],[540,1668]]),
        **anim('opacity',[f('01',1.20),f('01',1.44),f('01',2.52),f('01',2.80)],[0,1,1,0])})

# ------------------------------------------------------------------ el guion
DESP={'izq':[-170,0],'der':[170,0],'abajo':[0,120]}
ejes=['abajo','izq','der']
for i,(clip,s0,s1,niv,txt,sz) in enumerate(GUION):
    a,b = f(clip,s0), f(clip,s1)
    y = CARRIL[clip]
    if niv == 'ring':
        # anillo de línea fina con la cifra dentro, como el «6 meses» de la creatina
        L(name=f'anillo-{i}', type='ellipse', w=184, h=184, stroke=AZUL, strokeWidth=4,
          **{'from':a,'to':b}, pos=[640,y], anchor=[0,0], opacity=0,
          shadow=[0,7,12,NAVY,0.45],
          anim={**anim('scale',[a,a+9],[[0.42,0.42],[1,1]]),
                **anim('opacity',[a,a+6,b-5,b],[0,1,1,0])})
        L(name=f'cifra-{i}', type='text', text=txt, font='bold', size=sz, color=CREMA,
          track=6, **{'from':a,'to':b}, pos=[640,y], anchor=[0,0], opacity=0,
          shadow=[0,7,14,NAVY,0.55],
          anim={**anim('scale',[a+2,a+11],[[0.5,0.5],[1,1]]),
                **anim('opacity',[a+2,a+8,b-5,b],[0,1,1,0])})
        continue
    dx,dy = DESP[ejes[i % 3]]
    # el fragmento que acompaña a una cifra se aparta a la izquierda del anillo
    x = 300 if (clip=='04' and s0 == 0.00) else W/2
    L(name=f'tx-{i:02d}', type='text', text=txt, font='bold', size=sz, color=CREMA,
      track=8, textStroke=[NAVY, 2], **{'from':a,'to':b}, pos=[x,y], anchor=[0,0],
      opacity=0, shadow=[0,9,20,NAVY,0.62],
      anim={**anim('pos',[a,a+7],[[x+dx,y+dy],[x,y]]),
            **anim('opacity',[a,a+5,b-4,b],[0,1,1,0])})

spec={'fps':F,'master':'AD5 - FINAL','total':TOTAL,
      'paleta':{'navy':NAVY,'azul':AZUL,'crema':CREMA},'fuente':'Optima',
      'comps':{'AD5 - FINAL':{'name':'AD5 - FINAL','width':W,'height':H,
                              'duration':TOTAL,'layers':layers}}}
json.dump(spec, open(R/'src/design.json','w'), ensure_ascii=False, indent=1)
print(f"spec v2: {len(layers)} capas · Optima · sin bloques ni personajes")
