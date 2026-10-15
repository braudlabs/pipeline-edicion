from native import *
import copy
FPS=60000/1001; D=2278/FPS; C='BIRDIEBALLS V08 - MASTER'
CREAM=[.988,.984,.941];ACC=[.863,.953,.584];DARK=[.065,.13,.1]
def q(t):return round(t*FPS)/FPS
def k(n,p,t,v,ins=80,outs=15):
 op('keyframe.set_batch',comp=C,layer=n,property=p,times=[q(z) for z in t],values=v)
 for i in range(len(t)):op('keyframe.set_easing',comp=C,layer=n,property=p,keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=ins,outInfluence=outs)
def fade(n,a,b,peak=100):k(n,O,[a,a+.045,b-.055,b-1/FPS],[0,peak,peak,0],65,20)
def draw(n,verts,w,col,a,b,dur=.23):
 path(C,n,verts,w,col,q(a),q(b));op('shape.add_trim_paths',comp=C,layer=n,groupIndex=1,start=0,end=0)
 k(n,['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Filter - Trim','ADBE Vector Trim End'],[a,a+dur],[0,100])
 fade(n,a,b)
def shine(n,a,b,x,y,size=80):
 # Four-point reflection with a single expansion and collapse; no idle spin.
 op('layer.create_shape',comp=C,name=n);op('shape.add_group',comp=C,layer=n,name='Reflejo')
 pts=[[0,-size],[size*.17,-size*.17],[size,0],[size*.17,size*.17],[0,size],[-size*.17,size*.17],[-size,0],[-size*.17,-size*.17]]
 op('shape.add_path',comp=C,layer=n,groupIndex=1,vertices=pts,closed=True);op('shape.add_fill',comp=C,layer=n,groupIndex=1,color=CREAM+[1]);xf(C,n,position=[x,y]);timing(C,n,q(a),q(b));props(C,n,motionBlur=True)
 k(n,S,[a,a+.1,b-1/FPS],[[0,0],[110,110],[0,0]],76,22);k(n,ROT,[a,b-1/FPS],[-18,35],50,30)
footage(C,'00 - Montaje original continuo',1,0,D,0);props(C,'00 - Montaje original continuo',motionBlur=False)
# Controlled reactions, with the camera settled during reading and segmentation.
t=[0,6.205,6.27,6.47,6.7,23.30,23.44,23.70,24.07,25.64,26.18,26.5,27.08,31.87,32.28,32.67,32.88,D-1/FPS]
v=[100,100,104,101.2,100,100,103.2,103.2,100,100,102.1,102.1,100,100,102.8,102.8,100,100]
k('00 - Montaje original continuo',S,t,[[x,x] for x in v])
cs=json.load(open(R.parents[1]/'v07/cues.json'))
# Keep semantic anchors; recomposition is reserved for deliberate title hierarchies.
mods={
 'cansado':dict(size=142), 'dejarte':dict(size=100,y=1110),
 'rinon':dict(size=330,y=1390,weight=400), 'bolas-hook':dict(x=252,y=1483,size=95),
 'cada':dict(size=114,y=1370), 'jugar':dict(size=178,y=1370,weight=700),
 'venga1':dict(size=83), 'venga2':dict(size=101), 'venga3':dict(size=123,weight=700),
 'no':dict(size=337,weight=700,color='#fcfbf0',condensed=False),
 'traigo':dict(y=335,size=82), 'solucion':dict(y=557,size=202), 'solucion-outline':dict(y=557,size=202),
 'literal':dict(size=129,weight=700), 'brand':dict(size=139,weight=700),
 'recuperamos':dict(y=900,size=134),
 'bolas-product':dict(x=540,y=772,size=96,anchor='middle',motion='direct'),
 'originales':dict(x=540,y=935,size=195,weight=700,anchor='middle',text='originales',motion='hero'),
 'marcas':dict(size=128,y=900), 'favoritas':dict(size=200,weight=400,y=900),
 'lagos':dict(size=146,y=1390), 'campos':dict(size=146,y=1390),
 'las-limpieza':dict(y=480,size=108), 'limpiamos':dict(y=480,size=141,weight=700),
 'y-las':dict(y=480,size=108), 'revisamos':dict(y=480,size=141,weight=700),
 'una1':dict(x=322,y=545,size=170), 'a-una':dict(x=540,y=545,size=96), 'una2':dict(x=753,y=545,size=170),
 'no-son':dict(y=1290,size=97), 'nuevas':dict(y=1480,size=244),
 'como-nuevas-dialogo':dict(size=147,weight=700),
 'mas-baratas':dict(size=127),
 'pide':dict(text='y pide las tuyas.',size=136,weight=700),
 'birdie-end':dict(y=900,size=151,weight=700),
 'juega-mas':dict(y=900,size=164,weight=400),
 'por-menos':dict(y=1075,size=208,weight=700)
}
for c in cs:
 c.update(mods.get(c['id'],{}));a=q(c['start']);b=q(c['end']);x=c['x'];y=c['y'];size=c['size'];n='TXT '+c['id'];c['nativeLayer']=n;c['start']=a;c['end']=b
 col=ACC if c.get('color')=='#dcf395' else CREAM
 text(C,n,c['text'],x,y,size,col,'SFProDisplay-Bold' if c.get('weight',400)==700 else 'SFProDisplay-Regular',int(c.get('tracking',-.045)*1000),a,b);xf(C,n,anchorPoint=[0,0])
 if c.get('anchor')=='start':op('text.set_style',comp=C,layer=n,justification='left')
 if c.get('outline'):
  op('text.set_style',comp=C,layer=n,applyFill=False,applyStroke=True,strokeColor=col,strokeWidth=1.8,strokeOverFill=False)
  op('effect.remove',comp=C,layer=n,effectIndex=1)
 else:
  op('text.set_style',comp=C,layer=n,applyStroke=True,strokeColor=DARK,strokeWidth=1.2 if c.get('contrast') else .5,strokeOverFill=False)
 if c.get('highlight'):
  idx=c['text'].find(c['highlight']);op('text.set_style_range',comp=C,layer=n,start=idx,end=idx+len(c['highlight']),fillColor=ACC)
 style=c.get('motion','soft');avail=b-a
 if style=='direct':pass
 elif style=='hero':
  travel=175 if c['id']=='rinon' else 100 if c['id'].startswith('solucion') else 65
  d=min(.29,avail*.53)
  k(n,P,[a,a+d*.68,a+d],[[x,y+travel],[x,y-4],[x,y]],83,17)
  k(n,O,[a,a+.042],[0,100],60,20)
 elif style=='snap':
  d=min(.16,avail*.45);k(n,S,[a,a+d*.46,a+d],[[87,87],[103,103],[100,100]],78,15);k(n,O,[a,a+.033],[0,100],55,20)
 elif style=='reveal':
  k(n,P,[a,a+.18],[[x-66,y],[x,y]],82,15);k(n,O,[a,a+.055],[0,100])
 elif style=='cascade':
  travel=34 if c['id'] not in ['una1','una2'] else 45
  k(n,P,[a,a+min(.20,avail*.45)],[[x,y+travel],[x,y]],80,15);k(n,O,[a,a+.04],[0,100])
 else:
  travel=c.get('travel',22);ax=c.get('axis','y');start=[x+travel,y] if ax=='x' else [x,y+travel]
  k(n,P,[a,a+min(.17,avail*.4)],[start,[x,y]],78,20);k(n,O,[a,a+.035],[0,100])
 # Replacements are half-open cuts; fade/lift only at phrase endings.
 if c.get('out') in ['fade','lift'] and avail>.2:
  out=min(c.get('outDuration',.065),.08);k(n,O,[b-out,b-1/FPS],[100,0],60,18)
  if c.get('out')=='lift':
   op('keyframe.set_batch',comp=C,layer=n,property=P,times=[q(b-out),q(b-1/FPS)],values=[[x,y],[x,y-15]])
# The same native pose drives fill and outline; matte is source-timed.
footage(C,'MATTE - sujeto - f550 a599',69,550/FPS,600/FPS,550/FPS)
props(C,'MATTE - sujeto - f550 a599',motionBlur=False)
op('layer.set_track_matte',comp=C,layer='TXT solucion',matteLayer='MATTE - sujeto - f550 a599',matteType='lumaInverted');props(C,'MATTE - sujeto - f550 a599',enabled=False)
# Causal graphic details. Each has one task and an explicit end.
draw('RIÑON - trazo de impacto',[[252,1427],[815,1427]],4,ACC,2.38,3.045,.20)
draw('ORIGINALES - certificacion',[[126,976],[954,976]],3.5,CREAM,13.28,13.69,.19)
shine('BOLA - reflejo tras limpieza',20.97,21.27,665,1018,45)
# A scan identifies the ball, then resolves into a drawn check; original real footage stays visible.
for i,(x,y,dx,dy) in enumerate([(72,740,1,1),(937,740,-1,1),(72,1560,1,-1),(937,1560,-1,-1)]):
 n='REVISION - esquina '+str(i);draw(n,[[x,y+dy*65],[x,y],[x+dx*65,y]],3.5,CREAM,21.36+i*.018,22.34,.18)
# Thin moving scanning reflection, no fake object or card.
path(C,'REVISION - barrido',[[90,0],[925,0]],3,ACC,q(21.38),q(21.98));xf(C,'REVISION - barrido',position=[0,780]);k('REVISION - barrido',P,[21.38,21.95],[[0,780],[0,1500]],62,32);fade('REVISION - barrido',21.38,21.98,55)
draw('REVISION - comprobada',[[865,650],[894,679],[949,612]],8,ACC,22.02,22.34,.19)
draw('NUEVAS - subrayado',[[220,1520],[861,1520]],3.5,ACC,25.24,25.58,.15)
shine('NUEVAS - brillo de bola',26.23,26.55,557,1377,42)
# The source already carries its own 70%; the support stays in one rail.
draw('CTA - trazo tuyas',[[549,1420],[917,1420]],4,ACC,32.23,32.70,.25)
draw('CIERRE - firma',[[155,1130],[925,1130]],4,CREAM,37.04,37.94,.34)
shine('CIERRE - reflejo pack',37.09,37.43,839,1408,53)
# Save the executable design manifest beside the AE operation log.
(R.parent/'study/cues-native.json').write_text(json.dumps(cs,ensure_ascii=False,indent=2))
frames=[('hook',2.8),('solution',9.66),('product',13.48),('inspection',22.23),('new',25.4),('end',37.32)]
save('build.json',[{'name':'ae_save_project','arguments':{'path':str(R/'Birdieballs-V08.aep')}}]+[{'name':'ae_render_frame','arguments':{'compNameOrId':C,'time':q(t),'outPath':str(R.parent/'stills'/(n+'-native.png'))}} for n,t in frames])
