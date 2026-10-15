"""Author native, editable AE layers through the documented Higgsfield operations."""
from pathlib import Path
import json,math
R=Path(__file__).resolve().parent
IDS=json.load(open(R/'ids.json'))
T=json.load(open(R.parent/'src/timeline.json'))
INK=[.065,.082,.071];CREAM=[.98,.946,.85];ORANGE=[1,.337,.145];YELLOW=[.99,.78,.32];MUTED=[.51,.57,.52];WHITE=[1,1,1]
POS=['ADBE Transform Group','ADBE Position'];SCALE=['ADBE Transform Group','ADBE Scale'];OPACITY=['ADBE Transform Group','ADBE Opacity'];ROT=['ADBE Transform Group','ADBE Rotate Z'];RY=['ADBE Transform Group','ADBE Rotate Y'];RX=['ADBE Transform Group','ADBE Rotate X']
ops=[];requests=[]
def op(n,**a):ops.append({'operation':n,'args':a})
def flush():
 global ops
 if ops:requests.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}});ops=[]
def save(name,extra=None):
 flush();requests.extend(extra or [])
 # Check parameter spelling against locally discovered native operation catalogue.
 catalog={}
 for p in [R.parent.parent/'ae-v5/catalog-results.jsonl',R.parent.parent/'ae-v5/mask-cat-results.jsonl',R/'init-results.jsonl']:
  for line in open(p):
   s=json.loads(line)['result'].get('structuredContent',{})
   for o in s.get('operations',[]):catalog[o['name']]={p['name'] for p in o['params']}
 for req in requests:
  for o in req.get('arguments',{}).get('args',{}).get('ops',[]):
   assert o['operation'] in catalog, o['operation']
   assert set(o['args'])<=catalog[o['operation']],o
 (R/(name+'.json')).write_text(json.dumps(requests,ensure_ascii=False));print(name,len(requests),'batches',sum(len(r.get('arguments',{}).get('args',{}).get('ops',[])) for r in requests),'ops')
def xf(c,n,**a):op('transform.set',comp=c,layer=n,**a)
def props(c,n,**a):op('layer.set_props',comp=c,layer=n,props=a)
def parent(c,n,p):op('layer.set_parent',comp=c,layer=n,parentLayer=p,jump=True)
def null(c,n,position=[0,0,0]):op('layer.create_null',comp=c,name=n);props(c,n,threeDLayer=True);xf(c,n,position=position,anchorPoint=[0,0,0])
def text(c,n,s,x,y,size=64,color=CREAM,tracking=-25,align='center'):
 op('layer.create_text',comp=c,name=n,text=s);op('text.reset_style',comp=c,layer=n,scope='both')
 op('text.set_style',comp=c,layer=n,font='SFProDisplay-Bold',fontSize=size,fillColor=color,applyFill=True,applyStroke=False,justification=align,tracking=tracking,allCaps=False,fauxBold=False,fauxItalic=False,horizontalScale=1,verticalScale=1)
 xf(c,n,position=[x,y],anchorPoint=[0,0]);props(c,n,motionBlur=True)
def shape(c,n,x,y):
 op('layer.create_shape',comp=c,name=n);op('shape.add_group',comp=c,layer=n,name='Vector editable');xf(c,n,position=[x,y]);props(c,n,motionBlur=True)
def fill(c,n,color):op('shape.add_fill',comp=c,layer=n,groupIndex=1,color=color+[1])
def stroke(c,n,color,width=3):op('shape.add_stroke',comp=c,layer=n,groupIndex=1,color=color+[1],width=width)
def rect(c,n,x,y,w,h,color,roundness=0):
 shape(c,n,x,y);op('shape.add_rect',comp=c,layer=n,groupIndex=1,size=[w,h],roundness=roundness);fill(c,n,color)
def circle(c,n,x,y,d,color=None,line=None,width=3):
 shape(c,n,x,y);op('shape.add_ellipse',comp=c,layer=n,groupIndex=1,size=[d,d])
 if color:fill(c,n,color)
 if line:stroke(c,n,line,width)
def path(c,n,points,color=CREAM,width=3,closed=False):
 shape(c,n,0,0);op('shape.add_path',comp=c,layer=n,groupIndex=1,vertices=points,closed=closed);stroke(c,n,color,width)
def image(c,n,source,x,y,scale=100):
 op('layer.create_footage',comp=c,name=n,sourceItemId=IDS[source]);xf(c,n,position=[x,y],scale=[scale,scale]);props(c,n,motionBlur=True)
def keys(c,n,p,frames,values,influence=65,spatial=False,speeds=None):
 op('keyframe.set_batch',comp=c,layer=n,property=p,times=[f/48 for f in frames],values=values)
 for i in range(len(frames)):
  sp=(speeds or [0]*len(frames))[i]
  op('keyframe.set_easing',comp=c,layer=n,property=p,keyIndex=i+1,inSpeed=sp,outSpeed=sp,inInfluence=influence,outInfluence=influence)
  if spatial:op('keyframe.set_spatial',comp=c,layer=n,property=p,keyIndex=i+1,inTangent=[0,0,0],outTangent=[0,0,0],continuous=False,autoBezier=False)
def trim(c,n,a,b):
 op('shape.add_trim_paths',comp=c,layer=n,groupIndex=1,end=0)
 keys(c,n,['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Filter - Trim','ADBE Vector Trim End'],[a,b],[0,100],70)
def rise(c,n,x,y,a=0,b=12,dy=50):
 keys(c,n,POS,[a,b],[[x,y+dy],[x,y]],75,True);keys(c,n,OPACITY,[a,a+5],[0,100])
def shadow(c,n,opacity=75,distance=4,softness=16):
 op('effect.add',comp=c,layer=n,matchName='ADBE Drop Shadow',name='Sombra suave')
 for prop,v in [('ADBE Drop Shadow-0002',opacity),('ADBE Drop Shadow-0004',distance),('ADBE Drop Shadow-0005',softness)]:op('effect.set_property',comp=c,layer=n,effectIndex=1,property=[prop],value=v)
def camera(c,n='CAMARA',position=[540,960,-1500]):
 op('layer.create_camera',comp=c,name=n);props(c,n,autoOrient='off')
 op('property.set',comp=c,layer=n,property=['ADBE Camera Options Group','ADBE Camera Zoom'],value=1500)
 xf(c,n,position=position)
def bg(c,color=INK):
 op('layer.create_solid',comp=c,name='Fondo',color=color)
def duration(e):return T['events'][e]['to']-T['events'][e]['from']
