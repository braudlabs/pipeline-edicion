import json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'scripts'));from ae import AE
samples=[.8,3.4,4.66,5.80,7.1,8.95,10.5,12.20,14.40,15.92,17.9,19.78,21.72,23.64,25.30,26.6,27.12,28.95,30.62,31.84,33.9,36.32,37.9,40.28,41.9,43.2,44.1,45.66]
if '--short' in sys.argv:samples=[.8,5.8,8.95,10.5,12.2,15.92]
with AE(log=R/'analysis/v3/inspection.jsonl') as a:
 for op in ['font.list_missing','footage.list_missing']:
  q=a.call('ae_do',operation=op,args={});print(op,q,flush=True);(R/'analysis/v3'/(op+'.json')).write_text(json.dumps(q,indent=2))
 for t in samples:
  p=R/'analysis/v3'/f'frame-{t:.2f}.png'
  q=a.call('ae_do',operation='render.frame',args={'comp':'EL SISTEMA - V3 NARANJA','time':t,'outPath':str(p)},timeoutMs=120000)
  print(t,q.get('ok'),flush=True)
