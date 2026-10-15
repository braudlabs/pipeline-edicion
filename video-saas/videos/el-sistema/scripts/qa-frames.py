from pathlib import Path
from ae import AE
from retime import T
import json,sys
R=Path(__file__).resolve().parents[1];out=R/'analysis/qa-v2';out.mkdir(exist_ok=True)
TIMES=[float(x) for x in sys.argv[1:]] or [1.6,5.8,10.8,15.5,17.2,21.6,24.5,29.1,33.4,35.7,38.9,42.8,47.7,50.3,52.8,55.5,59.0,60.7,62.7,64.8,67]
with AE() as a:
 for t in TIMES:
  a.call('ae_do',operation='render.frame',args={'comp':'EL SISTEMA - PELICULA V2','time':T(t),'outPath':str(out/f'{t:.2f}.png')},timeoutMs=120000);print(t,T(t),flush=True)
