from pathlib import Path
import sys,json
R=Path(__file__).resolve().parents[2]
p=R/'scripts/v3/build.py'
ns={'__file__':str(p),'__name__':'patch'};exec(p.read_text().split("with AE(log=")[0],ns)
S=ns['S'];AE=ns['AE'];names=['V3 | 01 Idea a interfaz','V3 | 02 Dentro del sistema','V3 | Película protagonista','V3 | 03 Mapa a película','V3 | 05 Versiones']
with AE(log=R/'analysis/v3/refine-native.jsonl') as a:
 a.call('ae_save_project',path=str(R/'ae/v3/Antes-de-seams.aep'))
 info=a.call('ae_project_info')['result'];ids={x['name']:x['id'] for x in info['items']}
 for name in names:
  cc=S['comps'][name];print(name,flush=True)
  a.call('ae_do',operation='layer.delete',args={'comp':name,'layer':'all'})
  a.call('ae_do',operation='comp.set_props',args={'comp':name,'props':{'width':cc['width'],'height':cc['height']}})
  ns['ops']=[]
  for n in cc['layers']:ns['layer'](name,n,ids)
  ns['checked'](a,ns['ops'],name)
 a.call('ae_save_project',path=str(R/'ae/v3/El-Sistema-V3.aep'))
 print('PATCHED',flush=True)
