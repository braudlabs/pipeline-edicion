from pathlib import Path
import json
R=Path(__file__).resolve().parent
engine=(R/'build-native.py').read_text().split('# New named iteration;')[0]
exec(compile(engine,str(R/'build-native.py'),'exec'))
old=json.loads((R/'design-v1.json').read_text())
S=json.loads((R/'design-v2.json').read_text())
info=json.loads((R.parent/'analysis/v2-baseline-project.json').read_text())
IDS={i['name']:i['id'] for i in info['items']}
for line in (R/'v2-inspect-results.jsonl').read_text().splitlines():
 for o in json.loads(line)['result'].get('structuredContent',{}).get('operations',[]):
  CAT[o['name']]={p['name'] for p in o['params']}
changed=json.loads((R.parent/'analysis/v2/change-map.json').read_text())['changedComps']
for name in changed:
 c=S['comps'][name]
 op('layer.delete',comp=name,layer='all')
 for n in c['layers']:
  compile_layer(name,n)
  if len(ops)>160:flush()
 cam=c['camera'];nm='CAMARA - recorrido editorial'
 op('layer.create_camera',comp=name,name=nm)
 op('layer.set_props',comp=name,layer=nm,props={'autoOrient':'off'})
 op('property.set',comp=name,layer=nm,property=['ADBE Camera Options Group','ADBE Camera Zoom'],value=cam['zoom'])
 keys(name,nm,PP['pos'],cam['frames'],cam['values'],'out',True)
 for f,options in cam.get('spatialOverrides',{}).items():
  idx=cam['frames'].index(int(f))+1
  op('keyframe.set_spatial',comp=name,layer=nm,property=PP['pos'],keyIndex=idx,continuous=False,autoBezier=False,**options)
  op('keyframe.set_easing',comp=name,layer=nm,property=PP['pos'],keyIndex=idx,inSpeed=0,outSpeed=0,inInfluence=64,outInfluence=40)
 flush()
 req.append({'name':'ae_save_project','arguments':{'path':str(R/'Cocina-Reedicion-V2.aep')}})

# Patch only changed caption layers in the existing main edit.
master=S['master'];previous={n['name']:n for n in old['comps'][master]['layers']};now={n['name']:n for n in S['comps'][master]['layers']}
for name,n in previous.items():
 if name not in now or n!=now[name]:op('layer.delete',comp=master,layer=name)
for name,n in now.items():
 if name not in previous or n!=previous[name]:compile_layer(master,n)
op('comp.set_props',comp=master,props={'resolutionFactor':[1,1]})
flush()
req.extend([{'name':'ae_save_project','arguments':{'path':str(R/'Cocina-Reedicion-V2.aep')}},{'name':'ae_project_info','arguments':{}},{'name':'ae_do','arguments':{'operation':'footage.list_missing','args':{}}},{'name':'ae_do','arguments':{'operation':'font.list_missing','args':{}}}])
(R/'v2-construct.json').write_text(json.dumps(req,ensure_ascii=False))
print(len(req),'requests',sum(len(x.get('arguments',{}).get('args',{}).get('ops',[])) for x in req),'native operations')
