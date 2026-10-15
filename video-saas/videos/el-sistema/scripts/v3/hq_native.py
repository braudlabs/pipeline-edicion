from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));from ae import AE
S=json.loads((R/'src/v3/design.json').read_text())
with AE(log=R/'analysis/v3/hq-native.jsonl') as a:
 info=a.call('ae_project_info')['result'];ops=[]
 for z in info['items']:
  if z['name'].startswith('maquina-') and z['name'].endswith('.jpg'):
   file='v3/hq-'+z['name'].split('-')[-1]
   ops.extend([{'operation':'footage.replace','args':{'item':z['id'],'path':str(R/'assets'/file)}},{'operation':'item.set_props','args':{'item':z['id'],'name':file}}])
 for name,c in S['comps'].items():
  for n in c['layers']:
   if n['type']=='media' and n['asset'].startswith('v3/hq-'):
    ops.append({'operation':'transform.set','args':{'comp':name,'layer':n['name'],'anchorPoint':n['anchor'],'scale':[x*100 for x in n['scale']]}})
 for j in range(0,len(ops),90):
  d=a.call('ae_do',operation='batch.run',args={'ops':ops[j:j+90],'stopOnError':True});assert d['ok'] and not d['result'].get('failed'),d
 a.call('ae_save_project',path=str(R/'ae/v3/El-Sistema-V3.aep'))
 print('Higher resolution source frames linked',len(ops),flush=True)
