import sys,json
from pathlib import Path
from ae import AE
from retime import T
R=Path(__file__).resolve().parents[1]
with AE() as a:
 for t in [1.6,10.8,12.8,14.9,17.2]:
  print(a.call('ae_do',operation='render.frame',args={'comp':'EL SISTEMA - PELICULA V2','time':T(t),'outPath':str(R/'analysis'/f'v2-frame-{t}.png')},timeoutMs=120000),flush=True)
