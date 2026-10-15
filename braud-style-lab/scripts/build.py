from pathlib import Path
import json,math,numpy as np
R=Path(__file__).resolve().parents[1];F=24;D=67/F
CAT={o['name']:{p['name'] for p in o['params']} for path in ['inspect-results.jsonl','qa-type-resume-results.jsonl'] for l in open(R/'ae'/path) for o in json.loads(l)['result'].get('structuredContent',{}).get('operations',[])}
ops=[];req=[]
def op(n,**k):
 assert n in CAT,n;assert set(k)<=CAT[n],(n,set(k)-CAT[n]);ops.append({'operation':n,'args':k})
def flush():
 global ops
 if ops:req.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}});ops=[]
def rgb(h):return [int(h[i:i+2],16)/255 for i in (0,2,4)]
W=rgb('f0f7eb');G=rgb('bacfa8')
P={k:['ADBE Transform Group',v] for k,v in {'pos':'ADBE Position','scale':'ADBE Scale','anchor':'ADBE Anchor Point','rot':'ADBE Rotate Z','rx':'ADBE Rotate X','ry':'ADBE Rotate Y','opacity':'ADBE Opacity'}.items()}
def keys(c,l,p,fr,values,kind='flow',spatial=False):
 op('keyframe.set_batch',comp=c,layer=l,property=p,times=[(x-383)/F for x in fr],values=values)
 for i in range(len(fr)):
  if kind in ['linear','hold']:
   op('keyframe.set_interpolation',comp=c,layer=l,property=p,keyIndex=i+1,inType='linear',outType=kind)
  else:
   if kind=='ease' or i in (0,len(fr)-1):spd=0
   else:
    dv=(np.array(values[i+1])-np.array(values[i-1]))*F/(fr[i+1]-fr[i-1]);spd=float(np.linalg.norm(dv)) if spatial else (float(dv) if dv.ndim==0 else dv.tolist())
   # Temporal easing for array properties is shared speed; independent scale axes stay nearly equal.
   if isinstance(spd,list):spd=float(np.mean(spd))
   op('keyframe.set_easing',comp=c,layer=l,property=p,keyIndex=i+1,inSpeed=spd,outSpeed=spd,inInfluence=33.333,outInfluence=33.333)
  if spatial:op('keyframe.set_spatial',comp=c,layer=l,property=p,keyIndex=i+1,continuous=True,autoBezier=True)
def text(c,l,txt,size,track,pos,scale=[100,100],align='center'):
 op('layer.create_text',comp=c,name=l,text=txt);op('text.reset_style',comp=c,layer=l,scope='both');op('text.set_style',comp=c,layer=l,font='SFProDisplay-Bold',fontSize=size,tracking=track,justification=align,fillColor=W,applyFill=True,applyStroke=False,allCaps=False,fauxBold=False,fauxItalic=False)
 op('transform.set',comp=c,layer=l,position=pos,scale=scale);op('layer.set_props',comp=c,layer=l,props={'motionBlur':True,'label':9})
def shape(c,l):op('layer.create_shape',comp=c,name=l);op('shape.add_group',comp=c,layer=l,name='Geometría');op('transform.set',comp=c,layer=l,position=[600,600]);op('layer.set_props',comp=c,layer=l,props={'motionBlur':True})
def fx(c,l,index,match,name,props):
 op('effect.add',comp=c,layer=l,matchName=match,name=name)
 for p,v in props.items():op('effect.set_property',comp=c,layer=l,effectIndex=index,property=[p],value=v)
C='01 - Treinta variantes';T='02 - Costo mínimo';M='BRAUDLABS - Motion aislado';BG='00 - Verde texturizado'
for c,w,h in [(BG,1080,1920),(C,1200,1200),(T,1200,900),(M,1080,1920)]:
 op('comp.create',name=c,width=w,height=h,fps=F,duration=D)
 op('comp.set_props',comp=c,props={'motionBlur':True,'shutterAngle':210,'shutterPhase':-105,'motionBlurSamplesPerFrame':24,'motionBlurAdaptiveSampleLimit':96,'resolutionFactor':[1,1]})
flush()
# Native background: broad lighting plus procedural texture and monochrome grain.
op('layer.create_solid',comp=BG,name='Verde - luz radial',color=rgb('426127'),width=1080,height=1920)
fx(BG,'Verde - luz radial',1,'ADBE Ramp','Luz suave',{'ADBE Ramp-0001':[595,1110],'ADBE Ramp-0002':rgb('4b6c32')+[1],'ADBE Ramp-0003':[1800,1110],'ADBE Ramp-0004':rgb('243a15')+[1],'ADBE Ramp-0005':2,'ADBE Ramp-0006':1})
op('layer.create_solid',comp=BG,name='Textura - fractal editable',color=[.5,.5,.5],width=1080,height=1920)
fx(BG,'Textura - fractal editable',1,'ADBE Fractal Noise','Fibra y manchas',{'ADBE Fractal Noise-0004':100,'ADBE Fractal Noise-0005':0,'ADBE Fractal Noise-0010':640,'ADBE Fractal Noise-0015':8,'ADBE Fractal Noise-0017':44,'ADBE Fractal Noise-0018':45})
op('layer.set_blend_mode',comp=BG,layer='Textura - fractal editable',mode='softLight')
op('transform.set',comp=BG,layer='Textura - fractal editable',opacity=45)
# Neutral grain overlay gives luminance variation without changing the palette.
op('layer.create_solid',comp=BG,name='Grano - 6 por ciento',color=[.5,.5,.5],width=1080,height=1920)
fx(BG,'Grano - 6 por ciento',1,'ADBE Noise2','Grano fino',{'ADBE Noise2-0001':25,'ADBE Noise2-0002':0,'ADBE Noise2-0003':1})
op('layer.set_blend_mode',comp=BG,layer='Grano - 6 por ciento',mode='overlay');op('transform.set',comp=BG,layer='Grano - 6 por ciento',opacity=45)
flush()
# Repeater creates one spoke and one dot, thirty native copies. The ring has its own contraction.
shape(C,'Anillo')
op('shape.add_ellipse',comp=C,layer='Anillo',groupIndex=1,size=[488,488]);op('shape.add_stroke',comp=C,layer='Anillo',groupIndex=1,color=W+[1],width=2)
keys(C,'Anillo',['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Shape - Ellipse','ADBE Vector Ellipse Size'],[385,388,398],[[680,680],[680,680],[488,488]],'ease')
keys(C,'Anillo',P['opacity'],[384,388,399],[0,75,100],'ease')
shape(C,'Radios - 30 repeticiones')
op('shape.add_path',comp=C,layer='Radios - 30 repeticiones',groupIndex=1,vertices=[[-244,0],[-400,0]],closed=False)
op('shape.add_stroke',comp=C,layer='Radios - 30 repeticiones',groupIndex=1,color=G+[1],width=2)
op('shape.add_trim_paths',comp=C,layer='Radios - 30 repeticiones',groupIndex=1,start=0,end=100)
op('shape.add_repeater',comp=C,layer='Radios - 30 repeticiones',groupIndex=1,copies=30,position=[0,0],rotation=12)
keys(C,'Radios - 30 repeticiones',['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Filter - Trim','ADBE Vector Trim End'],[385,388,400],[0,9,100],'ease')
keys(C,'Radios - 30 repeticiones',P['opacity'],[385,389,397],[0,80,100],'ease')
keys(C,'Radios - 30 repeticiones',P['rot'],[383,449],[-26.4,52.8],'linear')
shape(C,'Puntos - 30 repeticiones')
op('shape.add_ellipse',comp=C,layer='Puntos - 30 repeticiones',groupIndex=1,size=[17,17])
op('property.set',comp=C,layer='Puntos - 30 repeticiones',property=['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Shape - Ellipse','ADBE Vector Ellipse Position'],value=[-400,0])
op('shape.add_fill',comp=C,layer='Puntos - 30 repeticiones',groupIndex=1,color=G+[1]);op('shape.add_repeater',comp=C,layer='Puntos - 30 repeticiones',groupIndex=1,copies=30,position=[0,0],rotation=12)
keys(C,'Puntos - 30 repeticiones',['ADBE Root Vectors Group',1,'ADBE Vectors Group','ADBE Vector Shape - Ellipse','ADBE Vector Ellipse Size'],[388,395],[[0,0],[17,17]],'ease')
keys(C,'Puntos - 30 repeticiones',P['opacity'],[387,390,397],[0,70,100],'ease');keys(C,'Puntos - 30 repeticiones',P['rot'],[383,449],[-26.4,52.8],'linear')
text(C,'Contador - número editable','30',364,-50,[600,730])
fx(C,'Contador - número editable',1,'ADBE Slider Control','Valor',{'ADBE Slider Control-0001':30})
keys(C,'Contador - número editable',['ADBE Effect Parade',1,'ADBE Slider Control-0001'],[383,389,390,391,392,393,394,395,396,398],[0,1,6,15,21,24,26,28,29,30],'hold')
op('expression.set',comp=C,layer='Contador - número editable',property=['ADBE Text Properties','ADBE Text Document'],expression='Math.round(effect("Valor")(1)).toString();')
keys(C,'Contador - número editable',P['opacity'],[388,389,392],[0,70,100],'ease');keys(C,'Contador - número editable',P['pos'],[389,392,397],[[620,750],[603,732],[600,730]],'flow',True)
text(C,'Variantes - subtítulo','variantes',51,-50,[598,773])
keys(C,'Variantes - subtítulo',P['opacity'],[393,395],[0,100],'ease');keys(C,'Variantes - subtítulo',P['pos'],[393,396],[[598,800],[598,773]],'ease',True)
flush()
# Typographic hierarchy; source text remains independently editable.
text(T,'Mínimo - protagonista','mínimo',264.3,-60,[600,600],[100.38,100]);keys(T,'Mínimo - protagonista',P['opacity'],[417,418,420],[0,55,100],'flow');keys(T,'Mínimo - protagonista',P['pos'],[417,420],[[600,636],[600,600]],'ease',True)
text(T,'A un costo - entrada por palabras','a un costo',58,-60,[489.5,393],align='left')
op('expression.set',comp=T,layer='A un costo - entrada por palabras',property=['ADBE Text Properties','ADBE Text Document'],expression='var f=timeToFrames(time)+383; f<410 ? "" : f<413 ? "a" : f<415 ? "a un" : value;')
keys(T,'A un costo - entrada por palabras',P['pos'],[410,412],[[489.5,412],[489.5,393]],'ease',True)
text(T,'De producción - remate','de producción',58,-50,[437,657],align='left')
op('expression.set',comp=T,layer='De producción - remate',property=['ADBE Text Properties','ADBE Text Document'],expression='var f=timeToFrames(time)+383; f<425 ? "" : f<427 ? "de" : value;')
keys(T,'De producción - remate',P['pos'],[425,428],[[437,677],[437,657]],'ease',True)
flush()
# Save the semantic sources first; compositing follows after their actual project ids are returned.
req.append({'name':'ae_save_project','arguments':{'path':str(R/'ae/BRAUDLABS-Motion-Piloto.aep')}})
req.append({'name':'ae_project_info','arguments':{}})
(R/'ae/build-sources.json').write_text(json.dumps(req));print(len(req),'requests',sum(len(q.get('arguments',{}).get('args',{}).get('ops',[])) for q in req),'operations')
