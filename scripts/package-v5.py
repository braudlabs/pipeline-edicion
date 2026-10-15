from pathlib import Path
import json,zipfile,hashlib,shutil
R=Path(__file__).resolve().parents[1];O=R/'output'
D=Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-12-ad2-ia-cara/edicion-final')
native=D/'After-Effects-V5'
shutil.copy2(O/'AD2-subtitulos-V3.srt',O/'AD2-subtitulos-V5.srt')
with zipfile.ZipFile(O/'Visual-Hub-After-Effects-V5.zip','w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in native.rglob('*'):
  if p.is_file() and p.name!='.DS_Store':z.write(p,Path('After-Effects-V5')/p.relative_to(native))
files=[]
for folder in ['src','scripts','public/assets']:
 for p in (R/folder).rglob('*'):
  if not p.is_file() or p.name=='.DS_Store':continue
  rel=p.relative_to(R).as_posix()
  if '/v2/' in rel and p.suffix=='.wav':continue
  if '/v3/' in rel and p.suffix=='.wav' and p.name!='audio-mix-master.wav':continue
  files.append(p)
files += [R/n for n in ['README.md','package.json','package-lock.json','tsconfig.json','.gitignore']]
files += [O/n for n in ['NOTAS-V5.md','AD2-subtitulos-V5.srt','hoja-de-revision-V5.jpg']]
files += list((R/'analysis/v5').glob('*.json'))
files += [R/'analysis/v5/verify-final.py',R/'analysis/v5/descenders.jpg']
files += list((R/'analysis/whisper-python').glob('*.json'))
files += [R/'analysis/v3'/n for n in ['edit-audit.json','reference-caption-a.jpg','reference-caption-b.jpg','reference-caption-c.jpg','reference-camera.jpg']]
files += [R/'ae-v5'/n for n in ['Visual-Hub-Cuentas-V5.aep','build.py','build.json','init.json','init-result.jsonl','build-remaining-results.jsonl','final-inspect-results.jsonl','aerender.log','render-probe.json']]
files += list((R/'ae-v5/assets').glob('*'))
out=O/'Visual-Hub-AD2-Remotion-V5.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in files:z.write(p,Path('Visual-Hub-AD2-Remotion-V5')/p.relative_to(R))
for p in [out,O/'Visual-Hub-After-Effects-V5.zip']:
 with zipfile.ZipFile(p) as z:assert z.testzip() is None,p
manifest=[]
for name in ['AD2-La-IA-te-sale-cara-V5.mp4','Visual-Hub-After-Effects-V5.zip','Visual-Hub-AD2-Remotion-V5.zip','NOTAS-V5.md','AD2-subtitulos-V5.srt','hoja-de-revision-V5.jpg']:
 p=O/name;t=D/name;shutil.copy2(p,t);h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==hashlib.sha256(t.read_bytes()).hexdigest()
 manifest.append({'file':name,'bytes':p.stat().st_size,'sha256':h});print(name,round(p.stat().st_size/1048576,2),'MiB',flush=True)
(O/'entrega-V5.json').write_text(json.dumps(manifest,indent=2));shutil.copy2(O/'entrega-V5.json',D/'entrega-V5.json')
print('ZIP CRC and delivery SHA-256 checks passed.')
