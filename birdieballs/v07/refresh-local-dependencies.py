from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib,json
base=Path('node_modules'); files=[p for p in base.rglob('*') if p.is_file() and p.suffix in {'.js','.mjs','.cjs','.json'} and '.remotion' not in p.parts]
print('Local files:',len(files),flush=True)
def refresh(p):
 n=p.stat().st_size
 if not n:return
 with p.open('rb',buffering=0) as f:d=f.read(n)
 if len(d)!=n:raise RuntimeError(f'Incomplete read {p}: {len(d)}/{n}')
 temp=p.with_name(p.name+'.available-v07');temp.write_bytes(d);temp.replace(p)
 return len(d)
total=0;errors=[]
with ThreadPoolExecutor(max_workers=12) as pool:
 tasks={pool.submit(refresh,p):p for p in files}
 for i,f in enumerate(as_completed(tasks),1):
  try:total+=f.result() or 0
  except Exception as e:errors.append(str(e))
  if i%1000==0:print(i,'files',flush=True)
Path('birdieballs/v07/dependency-refresh.json').write_text(json.dumps({'files':len(files),'bytes':total,'errors':errors,'operation':'Same-byte atomic rewrite to restore readable local dependency files; no version change'},indent=2))
print('Done',len(files),total,errors,flush=True)
