from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];F=48;ops=[];req=[]
CAT={o['name']:{p['name'] for p in o['params']} for path in [R/'ae/inspect-results.jsonl',R.parent/'v4/ae/inspect-results.jsonl'] for l in open(path) for o in json.loads(l)['result'].get('structuredContent',{}).get('operations',[])}
def op(n,**k):
 assert n in CAT and set(k)<=CAT[n],(n,k);ops.append({'operation':n,'args':k})
def flush():
 global ops
 req.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}});ops=[]
P={x:['ADBE Transform Group',y] for x,y in [('pos','ADBE Position'),('scale','ADBE Scale'),('rx','ADBE Rotate X'),('ry','ADBE Rotate Y'),('opacity','ADBE Opacity')]}
def keys(c,l,p,fr,vals):
 op('keyframe.set_batch',comp=c,layer=l,property=p,times=[f/F for f in fr],values=vals)
 for i in range(len(fr)):op('keyframe.set_easing',comp=c,layer=l,property=p,keyIndex=i+1,inSpeed=0,outSpeed=0,inInfluence=68,outInfluence=30)
 if p==P['pos']:
  for i in range(len(fr)):op('keyframe.set_spatial',comp=c,layer=l,property=p,keyIndex=i+1,continuous=False,autoBezier=False,inTangent=[0,0,0],outTangent=[0,0,0])
M='AD3 - V5 FINAL';C='01 - Se monta solo';B='01B - Caja continua'
op('comp.set_props',comp='AD3 - V4 FINAL',props={'name':M})
op('expression.set',comp=B,layer='Plano real - sincronizado con montaje',property=['ADBE Time Remapping'],expression='Math.max(830/48, time + 642/48);')
op('comp.set_props',comp=B,props={'motionBlur':True,'shutterAngle':210,'shutterPhase':-105,'motionBlurSamplesPerFrame':16,'motionBlurAdaptiveSampleLimit':64})
for name,a,b in [('SUB 18 - No son clips',833,857),('SUB 19 - sueltos',857,885)]:
 op('layer.copy_to_comp',comp=M,layer=name,targetComp=B)
 op('layer.set_props',comp=B,layer=name,props={'inPoint':(a-642)/48,'outPoint':min(216,b-642)/48})
 for p in [P['pos'],P['opacity'],['ADBE Effect Parade',1,'ADBE Gaussian Blur 2-0001']]:op('keyframe.shift',comp=B,layer=name,property=p,offset=-642/48)
op('layer.set_props',comp=M,layer='SUB 18 - No son clips',props={'enabled':False})
op('layer.set_props',comp=M,layer='SUB 19 - sueltos',props={'inPoint':858/48})
op('comp.set_props',comp=C,props={'duration':216/48,'workAreaDuration':216/48})
op('layer.set_props',comp=C,layer='Fondo verde compartido',props={'outPoint':216/48})
op('layer.set_props',comp=C,layer='Salida al anuncio',props={'enabled':False})
op('layer.set_props',comp=M,layer='ensamblaje',props={'outPoint':858/48})
# Preserve the board's existing animation until its last reading pose.
for p in ['pos','scale','rx','ry']:op('expression.set',comp=C,layer='Plano de pistas',property=P[p],expression='valueAtTime(Math.min(time, 136/48));')
op('layer.create_footage',comp=C,sourceItemId=587,name='Plano que espera - caja')
op('layer.set_props',comp=C,layer='Plano que espera - caja',props={'threeDLayer':True,'motionBlur':True,'inPoint':0,'outPoint':216/48})
op('transform.set',comp=C,layer='Plano que espera - caja',position=[540,2460,0],anchorPoint=[540,960,0],scale=[26,26,26])
for name,pos,anchor in [('Camara - descenso',[0,0,0],[0,0,0]),('Camara - entrada al plano',[540,1110,0],[540,1110,0])]:
 op('layer.create_null',comp=C,name=name);op('layer.set_props',comp=C,layer=name,props={'threeDLayer':True,'motionBlur':True,'outPoint':216/48});op('transform.set',comp=C,layer=name,position=pos,anchorPoint=anchor,scale=[100,100,100])
for name in ['Plano de pistas','Plano que espera - caja','automáticamente','se ensamblan']:op('layer.set_parent',comp=C,layer=name,parentLayer='Camara - descenso')
op('layer.set_parent',comp=C,layer='Camara - descenso',parentLayer='Camara - entrada al plano')
keys(C,'Camara - descenso',P['pos'],[148,178],[[0,0,0],[0,-1350,0]])
keys(C,'Camara - entrada al plano',P['pos'],[174,210],[[540,1110,0],[540,960,0]])
keys(C,'Camara - entrada al plano',P['scale'],[174,210],[[100,100,100],[10000/26]*3])
flush()
op('render.set_output',queueIndex=1,renderTemplate='Configuración óptima',outputTemplate='Calidad alta',outputPath=str(R/'analysis/native-part.mov'),timeSpanStart=0,timeSpanDuration=2162/48,render=True,skipFrames=0);flush()
req.append({'name':'ae_save_project','arguments':{'path':str(R/'ae/AD3-Pipeline-V5.aep')}})
for f in [774,804,820,840,852,857,858]:req.append({'name':'ae_render_frame','arguments':{'compNameOrId':M,'time':f/48,'outPath':str(R/f'analysis/native-{f}.png')}})
req.append({'name':'ae_project_info','arguments':{}})
(R/'ae/build-exit.json').write_text(json.dumps(req));print(len(req),'requests')
