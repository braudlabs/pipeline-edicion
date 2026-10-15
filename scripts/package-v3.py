import pathlib,zipfile,shutil,json,hashlib
R=pathlib.Path(__file__).resolve().parents[1];OUT=R/'output';DEST=pathlib.Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-12-ad2-ia-cara/edicion-final');DEST.mkdir(exist_ok=True)
files=[]
for d in ['src','scripts','public/assets','versions/v2']:
 for p in (R/d).rglob('*'):
  if not p.is_file() or p.name=='.DS_Store':continue
  rel=p.relative_to(R).as_posix()
  if '/v2/' in rel and p.suffix=='.wav':continue
  if '/v3/' in rel and p.suffix=='.wav' and p.name!='audio-mix-master.wav':continue
  files.append(p)
for n in ['package.json','package-lock.json','tsconfig.json','README.md','.gitignore']:files.append(R/n)
files+=sorted((R/'analysis/whisper-python').glob('*.json'))
files+=[R/'analysis/v3'/n for n in ['edit-audit.json','final-probe.json','sync-check.json','safe-zone-review.jpg','reference-caption-a.jpg','reference-caption-b.jpg','reference-caption-c.jpg','reference-camera.jpg','final-camera.jpg','delivery-qc.log']]
files+=[OUT/'NOTAS-V3.md',OUT/'AD2-subtitulos-V3.srt',OUT/'hoja-de-revision-V3.jpg']
zipout=OUT/'Visual-Hub-AD2-Remotion-V3.zip'
with zipfile.ZipFile(zipout,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,pathlib.Path('Visual-Hub-AD2-Remotion-V3')/p.relative_to(R))
with zipfile.ZipFile(zipout) as z:
 bad=z.testzip();assert bad is None,bad
 names=set(z.namelist());base='Visual-Hub-AD2-Remotion-V3/'
 for required in ['src/index.tsx','src/video.tsx','src/motion-v3.tsx','src/captions-v3.tsx','src/edl-v3.json','src/timing-v3.json','public/assets/v3/audio-mix-master.wav','public/assets/v3/kurt-proof-0.png','public/assets/v3/elliot-proof-0.png','package-lock.json']:
  assert base+required in names,required
manifest=[]
for name in ['AD2-La-IA-te-sale-cara-V3.mp4','Visual-Hub-AD2-Remotion-V3.zip','NOTAS-V3.md','AD2-subtitulos-V3.srt','hoja-de-revision-V3.jpg']:
 p=OUT/name;target=DEST/name;shutil.copy2(p,target);h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==hashlib.sha256(target.read_bytes()).hexdigest();manifest.append({'file':name,'bytes':p.stat().st_size,'sha256':h});print(name,round(p.stat().st_size/1048576,2),'MiB')
(OUT/'entrega-V3.json').write_text(json.dumps(manifest,indent=2));shutil.copy2(OUT/'entrega-V3.json',DEST/'entrega-V3.json')
print('Archive CRC passed; delivery copies verified by SHA-256.')
