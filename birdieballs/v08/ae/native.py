"""Native AE operations. Quantized half-open ranges; no temporal text blending."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
ops=[]
WHITE=[.992,.984,.956]; LIME=[.82,.96,.43]; INK=[.035,.06,.07]
P=['ADBE Transform Group','ADBE Position'];S=['ADBE Transform Group','ADBE Scale'];O=['ADBE Transform Group','ADBE Opacity'];ROT=['ADBE Transform Group','ADBE Rotate Z']
def op(n,**a):ops.append({'operation':n,'args':a})
def props(c,n,**a):op('layer.set_props',comp=c,layer=n,props=a)
def xf(c,n,**a):op('transform.set',comp=c,layer=n,**a)
def timing(c,n,a,b,start=0):props(c,n,startTime=start,inPoint=a,outPoint=b)
def key(c,n,p,t,v,ease=72):
 op('keyframe.set_batch',comp=c,layer=n,property=p,times=t,values=v)
 if ease:
  for i in range(len(t)):op('keyframe.set_easing',comp=c,layer=n,property=p,keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=ease,outInfluence=65)
def text(c,n,s,x,y,size=100,color=WHITE,font='SFProDisplay-Bold',tracking=-28,a=0,b=88.375):
 op('layer.create_text',comp=c,name=n,text=s);op('text.reset_style',comp=c,layer=n)
 op('text.set_style',comp=c,layer=n,font=font,fontSize=size,fillColor=color,applyFill=True,applyStroke=False,justification='center',tracking=tracking,autoLeading=False,leading=size*.92,allCaps=False,fauxBold=False,fauxItalic=False,horizontalScale=1,verticalScale=1)
 xf(c,n,position=[x,y],anchorPoint=[0,-size*.34]);timing(c,n,a,b);props(c,n,motionBlur=True)
 op('effect.add',comp=c,layer=n,matchName='ADBE Drop Shadow',name='Legibilidad')
 for k,v in [(2,46),(3,135),(4,3),(5,8)]:op('property.set',comp=c,layer=n,property=['ADBE Effect Parade','Legibilidad',k],value=v)
def rect(c,n,x,y,w,h,color=INK,roundness=0,a=0,b=88.375):
 op('layer.create_shape',comp=c,name=n);op('shape.add_group',comp=c,layer=n,name='Forma')
 op('shape.add_rect',comp=c,layer=n,groupIndex=1,size=[w,h],roundness=roundness)
 op('shape.add_fill',comp=c,layer=n,groupIndex=1,color=color+[1]);xf(c,n,position=[x,y]);timing(c,n,a,b);props(c,n,motionBlur=True)
def ellipse(c,n,x,y,w,h,color=LIME,a=0,b=88.375):
 op('layer.create_shape',comp=c,name=n);op('shape.add_group',comp=c,layer=n,name='Forma');op('shape.add_ellipse',comp=c,layer=n,groupIndex=1,size=[w,h]);op('shape.add_fill',comp=c,layer=n,groupIndex=1,color=color+[1]);xf(c,n,position=[x,y]);timing(c,n,a,b);props(c,n,motionBlur=True)
def path(c,n,verts,width=5,color=WHITE,a=0,b=88.375):
 op('layer.create_shape',comp=c,name=n);op('shape.add_group',comp=c,layer=n,name='Trazo');op('shape.add_path',comp=c,layer=n,groupIndex=1,vertices=verts,closed=False);op('shape.add_stroke',comp=c,layer=n,groupIndex=1,color=color+[1],width=width);xf(c,n,position=[0,0]);timing(c,n,a,b);props(c,n,motionBlur=True)
def footage(c,n,id,a,b,start):
 op('layer.create_footage',comp=c,name=n,sourceItemId=id);timing(c,n,a,b,start);props(c,n,audioEnabled=False,motionBlur=True)
def enter(c,n,a,x,y,style='rise'):
 if style=='cut':return
 if style=='slide':key(c,n,P,[a,a+5/24],[[x-45,y],[x,y]],78)
 elif style=='punch':key(c,n,S,[a,a+3/24,a+7/24],[[91,91],[101.5,101.5],[100,100]],72)
 else:key(c,n,P,[a,a+5/24,a+8/24],[[x,y+32],[x,y-2],[x,y]],74)
 key(c,n,O,[a,a+2/24],[0,100],0)
def save(name,extra=[]):
 req=[]
 for i in range(0,len(ops),160):req.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops[i:i+160],'stopOnError':True}}})
 req+=extra;(R/name).write_text(json.dumps(req,ensure_ascii=False));print(name,len(ops),'ops',len(req),'requests')
