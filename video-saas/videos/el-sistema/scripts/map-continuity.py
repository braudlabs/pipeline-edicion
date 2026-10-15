from pathlib import Path
import json
from ae import AE
R=Path(__file__).resolve().parents[1];DEST=Path('/Users/alejandrorubiocamarero/Desktop/El director/video-saas/videos/el-sistema');S=json.loads((R/'src/design-v2.json').read_text())
with AE(log=R/'analysis/map-continuity.jsonl') as a:
 ops=[]
 for n in S['comps']['V2 · Moodboard']['layers']:
  if n['name'].startswith('Movimiento '):
   ops.extend([{'operation':'layer.set_props','args':{'comp':'V2 · Moodboard','layer':n['name'],'props':{'startTime':n['from']-n['sourceOffset']}}},{'operation':'layer.set_props','args':{'comp':'V2 · Moodboard','layer':n['name'],'props':{'inPoint':n['from'],'outPoint':n['to']}}}])
 print(a.call('ae_do',operation='batch.run',args={'ops':ops,'stopOnError':True}))
 a.call('ae_save_project',path=str(DEST/'ae/El-Sistema-V2.aep'))
