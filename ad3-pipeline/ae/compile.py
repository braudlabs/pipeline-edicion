from pathlib import Path
import json,sys
R=Path(__file__).resolve().parent
base=(R.parents[1]/'ad1-reedit/ae/build-native.py').read_text().split('# New named iteration;')[0]
base=base.replace("S=json.load(open(R/'design.json'));IDS=json.load(open(R/'ids.json'));F=S['fps']", "S=json.load(open(R/sys.argv[1]));IDS=json.load(open(R/'ids.json'));F=S['fps']")
base=base.replace("def keys(c,l,p,frames,values,ease='smooth',spatial=False):", "def keys(c,l,p,frames,values,ease='smooth',spatial=False):\n assert all(a<b for a,b in zip(frames,frames[1:])),(c,l,p,frames)")
base=base.replace("op('transform.set',comp=c,layer=name,**kwargs)", "if is3:kwargs.pop('rotation',None)\n op('transform.set',comp=c,layer=name,**kwargs)\n if is3 and n.get('rot'):op('property.set',comp=c,layer=name,property=PP['rot'],value=n['rot'])")
exec(compile(base,str(R/'compile.py'),'exec'))
mode=sys.argv[2];names=list(S['comps'])
if len(sys.argv)>3:names=json.loads(sys.argv[3])
for name in names:
 c=S['comps'][name]
 op('comp.set_props',comp=name,props={'motionBlur':c.get('motionBlur',True),'shutterAngle':200,'shutterPhase':-100,'motionBlurSamplesPerFrame':16,'motionBlurAdaptiveSampleLimit':64})
 for n in c['layers']:
  compile_layer(name,n)
  if len(ops)>145:flush()
 if c.get('camera'):
  cam=c['camera'];nm='CAMARA - Recorrido';op('layer.create_camera',comp=name,name=nm);op('layer.set_props',comp=name,layer=nm,props={'autoOrient':'off'})
  op('property.set',comp=name,layer=nm,property=['ADBE Camera Options Group','ADBE Camera Zoom'],value=cam['zoom']);keys(name,nm,PP['pos'],cam['frames'],cam['values'],'out',True)
 flush()
req.append({'name':'ae_save_project','arguments':{'path':str(R/('AD3-Exploracion.aep' if mode=='style' else 'AD3-Pipeline-V1.aep'))}})
if mode=='style':
 for letter in 'ABC':
  name=next(k for k in S['comps'] if k.startswith('DIRECCION '+letter));req.append({'name':'ae_render_frame','arguments':{'compNameOrId':name,'time':1,'outPath':str(R.parent/'design'/f'Direccion-{letter}.png')}})
req.append({'name':'ae_project_info','arguments':{}})
(R/(mode+'-build.json')).write_text(json.dumps(req,ensure_ascii=False));print(len(req),'requests;',sum(len(x.get('arguments',{}).get('args',{}).get('ops',[])) for x in req),'operations')
