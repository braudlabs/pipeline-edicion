from pathlib import Path
import json,math,numpy as np
R=Path(__file__).resolve().parents[1]/'ae'
exec((R/'compile.py').read_text().split('import sys')[0].replace('R=Path(__file__).resolve().parent', '# Keep AE directory'))
def change(c,l,pos=None,size=None):
 n=next(n for n in S['comps'][c]['layers'] if n['name']==l)
 if size:n['size']=size;op('text.set_style',comp=c,layer=l,fontSize=size)
 if pos:
  delta=np.array(pos)-np.array(n['pos']);n['pos']=pos;op('transform.set',comp=c,layer=l,position=pos)
  if 'pos' in n.get('anim',{}):
   k=n['anim']['pos'];k['values']=[(np.array(v)+delta).tolist() for v in k['values']];keys(c,l,PP['pos'],k['frames'],k['values'],k['ease'],True)
# Exact onset of the word "solo".
c=S['master'];a=next(n for n in S['comps'][c]['layers'] if n['text']=='se ha montado') if False else None
for n in S['comps'][c]['layers']:
 if n.get('text')=='se ha montado':n['to']=315;op('layer.set_props',comp=c,layer=n['name'],props={'outPoint':315/48})
 if n.get('text')=='solo':
  delta=315-n['from'];n['from']=315;op('layer.set_props',comp=c,layer=n['name'],props={'inPoint':315/48})
  for p,k in n['anim'].items():
   k['frames']=[f+delta for f in k['frames']]
   prop=PP.get(p) if p!='blur' else ['ADBE Effect Parade',1,'ADBE Gaussian Blur 2-0001']
   # This layer has Gaussian Blur first, followed by shadow. Shift the actual native keys.
   op('keyframe.shift',comp=c,layer=n['name'],property=prop,offset=delta/48)
c='02 - Una creatividad'
change(c,'creatividad',pos=[540,1100],size=106)
change(c,'completa',pos=[540,1220],size=80)
for j in range(3,10):
 op('layer.set_props',comp=c,layer='Radio '+str(j),props={'enabled':False})
 next(n for n in S['comps'][c]['layers'] if n['name']=='Radio '+str(j))['to']=0
c='03 - Todo encaje'
change(c,'que',pos=[540,750]);change(c,'todo',pos=[540,920]);change(c,'encaje',pos=[540,1115])
c='04A - Sistema y salidas'
for s in ['imágenes','vídeos','avatares','anuncios']:
 n=next(n for n in S['comps'][c]['layers'] if n['name']==s);change(c,s,pos=[n['pos'][0],n['pos'][1]+70],size=180)
 n=next(n for n in S['comps'][c]['layers'] if n['name']=='Original '+s)
 n['w']=360;n['h']=640;op('transform.set',comp=c,layer=n['name'],scale=[100/3,100/3])
 if s=='anuncios':
  cx,cy,r=540,640,540;k=.55228475*r
  op('mask.set_path',comp=c,layer=n['name'],maskIndex=1,vertices=[[cx,cy-r],[cx+r,cy],[cx,cy+r],[cx-r,cy]],inTangents=[[-k,0],[0,-k],[k,0],[0,k]],outTangents=[[k,0],[0,k],[-k,0],[0,-k]],closed=True)
  op('transform.set',comp=c,layer=n['name'],anchorPoint=[cx,cy]);n['anchor']=[cx,cy]
flush()
c='05 - Produccion y oferta'
op('layer.create_null',comp=c,name='Giro radial - oferta');op('transform.set',comp=c,layer='Giro radial - oferta',position=[540,960],anchorPoint=[0,0])
for j in range(30):
 for l in ['Radio precio '+str(j),'Punto precio '+str(j)]:op('layer.set_parent',comp=c,layer=l,parentLayer='Giro radial - oferta')
keys(c,'Giro radial - oferta',PP['rot'],[109,275],[0,52],'linear')
op('layer.create_shape',comp=c,name='Anillo precio');op('shape.add_group',comp=c,layer='Anillo precio',name='Anillo editable');op('shape.add_ellipse',comp=c,layer='Anillo precio',groupIndex=1,size=[604,604]);op('shape.add_stroke',comp=c,layer='Anillo precio',groupIndex=1,color=rgb('#bacfa8')+[1],width=2);op('transform.set',comp=c,layer='Anillo precio',position=[540,960]);op('layer.set_props',comp=c,layer='Anillo precio',props={'inPoint':109/48,'outPoint':276/48})
keys(c,'Anillo precio',PP['opacity'],[109,124],[0,75],'out')
flush()
req.append({'name':'ae_save_project','arguments':{'path':str(R/'AD3-Pipeline-V4.aep')}})
for c,t,n in [('AD3 - V4 FINAL',1018/48,'creatividad'),('AD3 - V4 FINAL',1655/48,'sistema'),('AD3 - V4 FINAL',2140/48,'oferta')]:req.append({'name':'ae_render_frame','arguments':{'compNameOrId':c,'time':t,'outPath':str(R.parent/f'analysis/refinado-{n}.png')}})
(R/'refine.json').write_text(json.dumps(req));(R/'design-refined.json').write_text(json.dumps(S,ensure_ascii=False,indent=2));print(len(req),'requests')
