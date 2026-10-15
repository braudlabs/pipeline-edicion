from pathlib import Path
import subprocess,json,hashlib,os,shutil
R=Path(__file__).resolve().parents[1]
base=Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-16-ad3-pipeline-autonomo/edicion-final')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4194304),b''):h.update(b)
    return h.hexdigest()
for version in [7,8]:
    src=R.parent/f'v{version}/output';dest=base/f'V{version}'
    count=0
    for p in src.rglob('*'):
        if not p.is_file():continue
        d=dest/p.relative_to(src);d.parent.mkdir(parents=True,exist_ok=True)
        if d.exists() and d.stat().st_size==p.stat().st_size and sha(d)==sha(p):continue
        temp=d.with_name(d.name+'.copy-in-progress')
        subprocess.run(['/bin/cp','-c',str(p),str(temp)],check=True)
        assert sha(temp)==sha(p)
        os.replace(temp,d);count+=1
    assert sha(dest/f'AD3-Pipeline-V{version}.mp4')==json.loads((src/'CURRENT-VERSION.json').read_text())['videoSha256']
    print('Delivered V'+str(version),count,'files',flush=True)
shutil.copy2(R/'output/CURRENT-VERSION.json',R.parent/'CURRENT-VERSION.json')
print('CURRENT-VERSION -> V8',flush=True)
