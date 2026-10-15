from pathlib import Path
import json,os
R=Path(__file__).resolve().parents[1];F=48;D=18;N=2180;ops=[];req=[]
CAT={o['name']:{p['name'] for p in o['params']} for l in open(R.parent/'v4/ae/inspect-results.jsonl') for o in json.loads(l)['result'].get('structuredContent',{}).get('operations',[])}
def op(n,**k):assert n in CAT and set(k)<=CAT[n],(n,k);ops.append({'operation':n,'args':k})
def flush():
 global ops
 req.append({'name':'ae_do','arguments':{'operation':'batch.run','args':{'ops':ops,'stopOnError':True}}});ops=[]
def rgb(h):return [int(h[i:i+2],16)/255 for i in [1,3,5]]
rows=[json.loads(l)['result']['structuredContent']['result'] for l in open(R/'ae/inspect-results.jsonl')]
M='AD3 - V7 FINAL';C='01 - Se monta solo';O='05 - Produccion y oferta'
req.append({'name':'ae_save_project','arguments':{'path':str(R/'ae/AD3-Pipeline-V7.aep')}})
op('comp.set_props',comp='AD3 - V6 FINAL',props={'name':M,'duration':N/F,'workAreaDuration':N/F})
for x in json.loads((R.parent/'v6/analysis/color-changes.json').read_text()):
 if 'old' in x:op('text.set_style',comp=x['comp'].replace('V5','V7'),layer=x['layer'],fillColor=[v/255 for v in x['old']])
for p,h in [('ADBE Ramp-0002','#43632b'),('ADBE Ramp-0004','#273e1b')]:op('property.set',comp='00 - Verde BRAUD',layer='Luz radial',property=['ADBE Effect Parade','ADBE Ramp',p],value=rgb(h)+[1])
op('layer.set_props',comp=M,layer='SUB 08 - solo',props={'outPoint':340/F})
# Retimed base media and duration.
for i,n in [(139,'Montaje-AD3.mp4'),(140,'Mezcla-Final.wav')]:op('footage.replace',item=i,path=str(R/'assets'/n))
for name in ['Montaje Remotion','Mezcla - voz original','oferta']:op('layer.set_props',comp=M,layer=name,props={'outPoint':N/F})
op('comp.set_props',comp='00 - Verde BRAUD',props={'duration':N/F,'workAreaDuration':N/F})
for name in ['Grano fino','Textura - fibra editable','Luz radial']:op('layer.set_props',comp='00 - Verde BRAUD',layer=name,props={'outPoint':N/F})
# A broad film panel arrives from below. Less zoom, shorter empty journey.
P={k:['ADBE Transform Group',v] for k,v in [('pos','ADBE Position'),('scale','ADBE Scale')]}
def keys(layer,p,fr,vals):
 for i in [2,1]:op('keyframe.remove',comp=C,layer=layer,property=P[p],keyIndex=i)
 op('keyframe.set_batch',comp=C,layer=layer,property=P[p],times=[f/F for f in fr],values=vals)
 for i in [1,2]:
  op('keyframe.set_easing',comp=C,layer=layer,property=P[p],keyIndex=i,inSpeed=0,outSpeed=0,inInfluence=65,outInfluence=30)
  if p=='pos':op('keyframe.set_spatial',comp=C,layer=layer,property=P[p],keyIndex=i,inTangent=[0,0,0],outTangent=[0,0,0],continuous=False,autoBezier=False)
op('transform.set',comp=C,layer='Plano que espera - caja',position=[540,2590,0],scale=[68,68,68])
keys('Camara - descenso','pos',[154,180],[[0,0,0],[0,-1480,0]])
keys('Camara - entrada al plano','pos',[168,198],[[540,1110,0],[540,960,0]])
keys('Camara - entrada al plano','scale',[168,198],[[100,100,100],[10000/68]*3])
# Move CTA words, diagram and price together by 18 frames, preserving key curves.
op('comp.set_props',comp=O,props={'duration':294/F,'workAreaDuration':294/F})
def keypaths(node,path):
 for p in node.get('properties',[]):
  if p.get('keyframes'):yield path+[p['matchName']]
 for g in node.get('groups',[]):yield from keypaths(g,path+[g['matchName']])
for l in rows[5]['layers']:
 if l['name']=='Fondo verde compartido':op('layer.set_props',comp=O,layer=l['name'],props={'outPoint':294/F});continue
 if l['name'] in ['producción','una línea de'] or l['name'].startswith(('Eslabon','Vinculo')):continue
 for key,val in l.items():
  if isinstance(val,dict) and 'matchName' in val:
   for path in keypaths(val,[val['matchName']]):op('keyframe.shift',comp=O,layer=l['name'],property=path,offset=D/F)
 op('layer.set_props',comp=O,layer=l['name'],props={'inPoint':l['inPoint']+D/F,'outPoint':l['outPoint']+D/F})
flush()
# Import distinct photographs without replacing original footage used elsewhere.
for name in ['imagenes','videos','avatares','anuncios']:op('project.import_file',path=str(R/f'assets/generated/{name}-soul.png'),name=f'Soul - {name}')
flush()
for name,label in [('imagenes','imágenes'),('videos','vídeos'),('avatares','avatares'),('anuncios','anuncios')]:
 l='Original '+label;comp='04A - Sistema y salidas'
 op('layer.replace_source',comp=comp,layer=l,item='Soul - '+name,fixExpressions=False)
 op('transform.set',comp=comp,layer=l,anchorPoint=[1024,1024,0],scale=[20,20,100])
 rr=900;cc=1024;kk=rr*.5522847498
 op('mask.set_path',comp=comp,layer=l,maskIndex=1,vertices=[[cc,cc-rr],[cc+rr,cc],[cc,cc+rr],[cc-rr,cc]],inTangents=[[-kk,0],[0,-kk],[kk,0],[0,kk]],outTangents=[[kk,0],[0,kk],[-kk,0],[0,-kk]],closed=True)
flush()
op('render.set_output',queueIndex=1,renderTemplate='Configuración óptima',outputTemplate='Calidad alta',outputPath=str(R/'analysis/native-part.mov'),timeSpanStart=0,timeSpanDuration=N/F,render=True,skipFrames=0);flush()
req.append({'name':'ae_save_project','arguments':{'path':str(R/'ae/AD3-Pipeline-V7.aep')}})
for f in [341,352,800,813,825,840,1545,1660,1944,1962,1980,2036,2179]:req.append({'name':'ae_render_frame','arguments':{'compNameOrId':M,'time':f/F,'outPath':str(R/f'analysis/native-{f}.png')}})
req.append({'name':'ae_comp_info','arguments':{'nameOrId':[M,O,C,'04A - Sistema y salidas']}});req.append({'name':'ae_project_info','arguments':{}})
(R/'ae/patch.json').write_text(json.dumps(req));print(len(req),'AE requests')
# Reuse only frames wholly unaffected relative to the green V5.
for i in range(16):
 if i not in [2,5,10,11,13,14,15]:
  for ext in ['mp4','json']:os.link(R.parent/f'v5/analysis/parts/{i:02d}.{ext}',R/f'analysis/parts/{i:02d}.{ext}')
(R/'scripts/render-parts.py').write_text((R.parent/'v6/scripts/render-parts.py').read_text().replace('V6','V7').replace('N=2162','N=2180'))
