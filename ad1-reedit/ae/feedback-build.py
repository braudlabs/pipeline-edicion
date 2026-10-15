from pathlib import Path
from PIL import Image
import json,math
R=Path(__file__).resolve().parent
S=json.load(open(R/'design.json'));IDS=json.load(open(R/'ids.json'));F=S['fps']
CAT={o['name']:{p['name'] for p in o['params']} for l in open(R/'inspect-results.jsonl') for o in json.loads(l)['result'].get('structuredContent',{}).get('operations',[])}
ops=[];req=[]
def op(n,**args):
 assert n in CAT,n
 assert set(args)<=CAT[n],(n,set(args)-CAT[n])
 ops.append({'operation':n,'args':args})
def flush():
 global ops
 if ops:req.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}});ops=[]
def rgb(c):return [int(c[i:i+2],16)/255 for i in [1,3,5]]
FONTS={'light':'HelveticaNeue-Light','regular':'SFProDisplay-Regular','bold':'SFProDisplay-Bold','italic':'Arial-ItalicMT','bolditalic':'Arial-BoldItalicMT'}
PP={k:['ADBE Transform Group',v] for k,v in {'pos':'ADBE Position','anchor':'ADBE Anchor Point','scale':'ADBE Scale','rot':'ADBE Rotate Z','ry':'ADBE Rotate Y','rx':'ADBE Rotate X','opacity':'ADBE Opacity'}.items()}
def keys(c,l,p,frames,values,ease='smooth',spatial=False):
 op('keyframe.set_batch',comp=c,layer=l,property=p,times=[f/F for f in frames],values=values)
 for i in range(len(frames)):
  if ease in ['linear','hold']:
   op('keyframe.set_interpolation',comp=c,layer=l,property=p,keyIndex=i+1,inType='linear',outType=ease)
  else:op('keyframe.set_easing',comp=c,layer=l,property=p,keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=80 if ease=='out' else 33,outInfluence=15 if ease=='out' else 33)
  if spatial:op('keyframe.set_spatial',comp=c,layer=l,property=p,keyIndex=i+1,inTangent=[0,0,0],outTangent=[0,0,0],continuous=False,autoBezier=False)

def compile_layer(c,n):
 name=n['name'];t=n['type'];w=n.get('w',0);h=n.get('h',0);anchor=n.get('anchor',[0,0]);baseScale=[100,100];is3=n.get('threeD',False);fx=0
 def effect(match,display,props):
  nonlocal fx
  fx+=1;op('effect.add',comp=c,layer=name,matchName=match,name=display)
  for pn,v in props.items():op('effect.set_property',comp=c,layer=name,effectIndex=fx,property=[pn],value=v)
  return fx
 def shadow(col,dist,angle,soft,alpha,display):
  return effect('ADBE Drop Shadow',display,{'ADBE Drop Shadow-0001':rgb(col)+[1],'ADBE Drop Shadow-0002':255*alpha,'ADBE Drop Shadow-0003':angle,'ADBE Drop Shadow-0004':dist,'ADBE Drop Shadow-0005':soft})
 if t=='text':
  op('layer.create_text',comp=c,name=name,text=n['text']);op('text.reset_style',comp=c,layer=name,scope='both')
  op('text.set_style',comp=c,layer=name,font=FONTS[n['font']],fontSize=n['size'],fillColor=rgb(n['color']),applyFill=True,applyStroke=False,justification=n.get('align','left'),tracking=n['track'],allCaps=False,fauxBold=False,fauxItalic=False,horizontalScale=1,verticalScale=1)
 elif t in ['image','comp','video','audio']:
  src=n['source'] if t=='comp' else n['asset'];op('layer.create_footage',comp=c,name=name,sourceItemId=IDS[src])
  if t=='image':
   iw,ih=Image.open(R.parent/'assets'/src).size;baseScale=[100*w/iw,100*h/ih]
  elif t=='comp':w=S['comps'][src]['width'];h=S['comps'][src]['height']
 elif t=='gradient':
  op('layer.create_solid',comp=c,name=name,color=rgb(n['color']),width=w,height=h)
  if n.get('radius'):
   center=n.get('center',[w/2,h/2]);effect('ADBE Ramp','Degradado radial',{'ADBE Ramp-0001':center,'ADBE Ramp-0002':rgb(n['color'])+[1],'ADBE Ramp-0003':[center[0]+n['radius'],center[1]],'ADBE Ramp-0004':rgb(n['endColor'])+[1],'ADBE Ramp-0005':2,'ADBE Ramp-0006':.4})
 else:
  op('layer.create_shape',comp=c,name=name);op('shape.add_group',comp=c,layer=name,name='Geometría editable')
  if t=='rect':
   op('shape.add_rect',comp=c,layer=name,groupIndex=1,size=[w,h],roundness=n.get('round',0));anchor=[-w/2,-h/2]
  elif t=='ellipse':op('shape.add_ellipse',comp=c,layer=name,groupIndex=1,size=[w,h])
  elif t in ['path','scanlines']:
   pts=n.get('points',[])
   if t=='scanlines':
    for i,y in enumerate(range(5,int(h),6)):pts.extend([[0,y],[w,y]] if i%2==0 else [[w,y],[0,y]])
   op('shape.add_path',comp=c,layer=name,groupIndex=1,vertices=pts,closed=n.get('closed',False))
  if n.get('color') and t not in ['scanlines']:op('shape.add_fill',comp=c,layer=name,groupIndex=1,color=rgb(n['color'])+[1])
  if n.get('stroke') or t=='scanlines':op('shape.add_stroke',comp=c,layer=name,groupIndex=1,color=rgb((n.get('stroke') or n.get('color','#000000')))+[1],width=n.get('strokeWidth',1))
 op('layer.set_props',comp=c,layer=name,props={'motionBlur':True,'threeDLayer':is3,'inPoint':n['from']/F,'outPoint':max(n['from']+1,n['to'])/F,'enabled':n['to']>n['from'],'label':9 if t=='text' else 13 if t in ['image','comp'] else 5})
 scale=[a*b for a,b in zip(n.get('scale',[1,1]),baseScale)]
 kwargs={'position':n['pos']+([0] if is3 and len(n['pos'])==2 else []),'anchorPoint':anchor+([0] if is3 else []),'scale':scale+([100] if is3 else []),'rotation':n.get('rot',0),'opacity':100*n.get('opacity',1)}
 op('transform.set',comp=c,layer=name,**kwargs)
 if 'startTime' in n:op('layer.set_props',comp=c,layer=name,props={'startTime':n['startTime'],'inPoint':n['from']/F,'outPoint':n['to']/F})
 if t=='video':op('layer.set_props',comp=c,layer=name,props={'audioEnabled':False})
 if n.get('textStroke'):op('text.set_style',comp=c,layer=name,applyStroke=True,strokeColor=rgb(n['textStroke'][0]),strokeWidth=n['textStroke'][1],strokeOverFill=False)
 for a in ['rx','ry']:
  if a in n:op('property.set',comp=c,layer=name,property=PP[a],value=-n[a])
 for a,k in n.get('anim',{}).items():
  if a in PP:
   vals=k['values']
   if a in ['pos','anchor'] and is3:vals=[v+([0] if len(v)==2 else []) for v in vals]
   if a=='scale':vals=[[v[i]*baseScale[i] for i in [0,1]]+([100] if is3 else []) for v in vals]
   if a in ['rx','ry']:vals=[-v for v in vals]
   if a=='opacity':vals=[v*100 for v in vals]
   keys(c,name,PP[a],k['frames'],vals,k['ease'],a in ['pos','anchor'])
 if n.get('round') and t=='comp':
  rr=n['round'];k=.5522848*rr;pts=[[rr,0],[w-rr,0],[w,rr],[w,h-rr],[w-rr,h],[rr,h],[0,h-rr],[0,rr]]
  it=[[-k,0],[0,0],[0,-k],[0,0],[k,0],[0,0],[0,k],[0,0]];ot=[[0,0],[k,0],[0,0],[0,k],[0,0],[-k,0],[0,0],[0,-k]]
  op('mask.add',comp=c,layer=name,name='Esquinas de publicación');op('mask.set_path',comp=c,layer=name,maskIndex=1,vertices=pts,inTangents=it,outTangents=ot,closed=True)
 if n.get('trim'):
  op('shape.add_trim_paths',comp=c,layer=name,groupIndex=1,end=0)
  keys(c,name,['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Filter - Trim','ADBE Vector Trim End'],n['trim'],[0,100],'out')
 # Blur changes are native effect keys; no pre-rendered graphics.
 if n.get('blur') or 'blur' in n.get('anim',{}):
  idx=effect('ADBE Gaussian Blur 2','Suavidad y foco',{'ADBE Gaussian Blur 2-0001':n.get('blur',0)*2,'ADBE Gaussian Blur 2-0003':0})
  if 'blur' in n.get('anim',{}):
   a=n['anim']['blur'];keys(c,name,['ADBE Effect Parade',idx,'ADBE Gaussian Blur 2-0001'],a['frames'],[x*2 for x in a['values']],a['ease'])
 if n.get('shadow'):
  x,y,b,cl,alpha=n['shadow'];shadow(cl,math.hypot(x,y),math.degrees(math.atan2(x,-y)),2*b,alpha,'Sombra suave')
 if n.get('chroma'):
  shadow('#ef402b',n['chroma'],180,.7,.65,'Franja roja');shadow('#184dff',n['chroma'],0,.6,.65,'Franja azul')
 if n.get('glow'):shadow(n.get('glowColor','#b3a7b2'),0,0,n['glow'],1,'Halo de luz')
 if 'wipe' in n.get('anim',{}):
  a=n['anim']['wipe']
  for direction in [90,270]:
   idx=effect('ADBE Linear Wipe','Persiana '+str(direction),{'ADBE Linear Wipe-0002':direction,'ADBE Linear Wipe-0003':0})
   keys(c,name,['ADBE Effect Parade',idx,'ADBE Linear Wipe-0001'],a['frames'],[v/2 for v in a['values']],a['ease'])

# New named iteration; build editable layers and actual cameras.
for c in S['comps'].values():
 if c['name'] not in json.load(open(R/'changed.json')):continue
 name=c['name'];op('comp.set_props',comp=name,props={'motionBlur':True,'shutterAngle':240,'shutterPhase':-120,'motionBlurSamplesPerFrame':16,'motionBlurAdaptiveSampleLimit':64})
 for n in c['layers']:
  compile_layer(name,n)
  if len(ops)>190:flush()
 if c.get('camera'):
  cam=c['camera'];nm='CAMARA - recorrido editorial'
  op('layer.create_camera',comp=name,name=nm);op('layer.set_props',comp=name,layer=nm,props={'autoOrient':'off'})
  op('property.set',comp=name,layer=nm,property=['ADBE Camera Options Group','ADBE Camera Zoom'],value=cam['zoom'])
  keys(name,nm,PP['pos'],cam['frames'],cam['values'],'out',True)
 flush();req.append({'name':'ae_save_project','arguments':{'path':str(R/'Cocina-Reedicion.aep')}})
op('timeline.set_active_comp',comp=S['master']);op('timeline.set_time',comp=S['master'],time=38);flush()
req.extend([{'name':'ae_save_project','arguments':{'path':str(R/'Cocina-Reedicion.aep')}},{'name':'ae_project_info','arguments':{}}])
(R/'construct.json').write_text(json.dumps(req,ensure_ascii=False));print(len(req),'requests',sum(len(x.get('arguments',{}).get('args',{}).get('ops',[])) for x in req),'native operations')
