from pathlib import Path
import json
R=Path(__file__).resolve().parent
exec(compile((R/'build-native.py').read_text().split('# New named iteration;')[0],str(R/'build-native.py'),'exec'))
old=json.loads((R/'design-v2.json').read_text());S=json.loads((R/'design-v3.json').read_text())
results=[json.loads(l) for p in ['v3-init-results.jsonl','v3-init-resume-results.jsonl'] for l in (R/p).read_text().splitlines()]
assert len(results)==10,len(results)
for z in results:
 st=z['result']['structuredContent'];assert st['ok'] and st.get('result',{}).get('ok',True) and not z['result'].get('isError'),z
info=results[-1]['result']['structuredContent']['result'];IDS={i['name']:i['id'] for i in info['items']}
for filename in ['v3-inspect-results.jsonl','v3-project-catalog-results.jsonl']:
 for line in (R/filename).read_text().splitlines():
  for o in json.loads(line)['result'].get('structuredContent',{}).get('operations',[]):CAT[o['name']]={p['name'] for p in o['params']}
names=[k for k in S['comps'] if k not in old['comps']]+['MG - Creditos']
for name in names:
 c=S['comps'][name]
 if name=='MG - Creditos':op('layer.delete',comp=name,layer='all')
 op('comp.set_props',comp=name,props={'motionBlur':True,'shutterAngle':200,'shutterPhase':-100,'motionBlurSamplesPerFrame':16,'motionBlurAdaptiveSampleLimit':64})
 for n in c['layers']:
  compile_layer(name,n)
  if len(ops)>165:flush()
 if c.get('camera'):
  cam=c['camera'];nm='CAMARA - recorrido editorial';op('layer.create_camera',comp=name,name=nm)
  op('layer.set_props',comp=name,layer=nm,props={'autoOrient':'off'})
  op('property.set',comp=name,layer=nm,property=['ADBE Camera Options Group','ADBE Camera Zoom'],value=cam['zoom'])
  keys(name,nm,PP['pos'],cam['frames'],cam['values'],'out',True)
 flush()
master=S['master'];previous={n['name']:n for n in old['comps'][master]['layers']};current={n['name']:n for n in S['comps'][master]['layers']}
for name,n in previous.items():
 if name not in current or n!=current[name]:op('layer.delete',comp=master,layer=name)
for name,n in current.items():
 if name not in previous or n!=previous[name]:compile_layer(master,n)
op('render.clear_queue');op('render.add_to_queue',comp=master,outputPath=str(R.parent/'analysis/v3/Native-Credits.mov'));flush()
req.extend([{'name':'ae_save_project','arguments':{'path':str(R/'Cocina-Reedicion-V3.aep')}},{'name':'ae_project_info','arguments':{}},{'name':'ae_do','arguments':{'operation':'font.list_missing','args':{}}},{'name':'ae_do','arguments':{'operation':'footage.list_missing','args':{}}}])
(R/'v3-construct.json').write_text(json.dumps(req,ensure_ascii=False));print(len(req),'requests;',sum(len(x.get('arguments',{}).get('args',{}).get('ops',[])) for x in req),'native operations')
