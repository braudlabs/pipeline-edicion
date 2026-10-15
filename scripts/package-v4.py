import pathlib,zipfile,shutil,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1];OUT=R/'output';DEST=pathlib.Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-12-ad2-ia-cara/edicion-final');DEST.mkdir(exist_ok=True)
shutil.copy2(OUT/'AD2-subtitulos-V3.srt',OUT/'AD2-subtitulos-V4.srt')
files=[]
for directory in ['src','scripts','public/assets','versions/v2','versions/v3']:
 for p in (R/directory).rglob('*'):
  if not p.is_file() or p.name=='.DS_Store':continue
  rel=p.relative_to(R).as_posix()
  if '/v2/' in rel and p.suffix=='.wav':continue
  if '/v3/' in rel and p.suffix=='.wav' and p.name!='audio-mix-master.wav':continue
  files.append(p)
for n in ['package.json','package-lock.json','tsconfig.json','README.md','.gitignore']:files.append(R/n)
files+=sorted((R/'analysis/whisper-python').glob('*.json'))
files+=[R/'analysis/v3'/n for n in ['edit-audit.json','reference-caption-a.jpg','reference-caption-b.jpg','reference-caption-c.jpg','reference-camera.jpg']]
files+=[R/'analysis/v4'/n for n in ['faces.json','detect-faces.swift','face-placement.jpg','descenders.jpg','qc-summary.json','sync-check.json','final-probe.json','delivery-qc.log','verify-final.py']]
files+=[OUT/n for n in ['NOTAS-V4.md','AD2-subtitulos-V4.srt','hoja-de-revision-V4.jpg']]
zipout=OUT/'Visual-Hub-AD2-Remotion-V4.zip'
with zipfile.ZipFile(zipout,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,pathlib.Path('Visual-Hub-AD2-Remotion-V4')/p.relative_to(R))
with zipfile.ZipFile(zipout) as z:
 assert z.testzip() is None;names=set(z.namelist());base='Visual-Hub-AD2-Remotion-V4/'
 for required in ['src/index.tsx','src/video.tsx','src/motion-v4.tsx','src/captions-v4.tsx','src/caption-layout-v4.json','src/edit-time.ts','public/assets/v3/audio-mix-master.wav','public/assets/v3/kurt-proof-0.png','public/assets/v3/elliot-proof-0.png','package-lock.json','analysis/v4/faces.json']:
  assert base+required in names,required
manifest=[]
for name in ['AD2-La-IA-te-sale-cara-V4.mp4','Visual-Hub-AD2-Remotion-V4.zip','NOTAS-V4.md','AD2-subtitulos-V4.srt','hoja-de-revision-V4.jpg']:
 p=OUT/name;target=DEST/name;shutil.copy2(p,target);h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==hashlib.sha256(target.read_bytes()).hexdigest();manifest.append({'file':name,'bytes':p.stat().st_size,'sha256':h});print(name,round(p.stat().st_size/1048576,2),'MiB')
(OUT/'entrega-V4.json').write_text(json.dumps(manifest,indent=2));shutil.copy2(OUT/'entrega-V4.json',DEST/'entrega-V4.json')
print('ZIP CRC and delivery SHA-256 checks passed.')
