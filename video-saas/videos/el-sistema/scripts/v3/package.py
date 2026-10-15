from pathlib import Path
import json,shutil,sys,hashlib
R=Path(__file__).resolve().parents[2];DEST=Path('/Users/alejandrorubiocamarero/Desktop/El director/video-saas/videos/el-sistema');sys.path.insert(0,str(R/'scripts'));from ae import AE
S=json.loads((R/'src/v3/design.json').read_text());used={n['asset'] for c in S['comps'].values() for n in c['layers'] if n['type'] in ['media','audio']}
for file in used:
 src=R/'assets'/file;dst=DEST/'assets'/file;dst.parent.mkdir(parents=True,exist_ok=True)
 if not dst.exists() or src.stat().st_size!=dst.stat().st_size:shutil.copy2(src,dst)
for file in ['Voice.wav','Music.wav','SFX.wav','Mix.wav']:
 shutil.copy2(R/'assets/v3'/file,DEST/'assets/v3'/file)
for folder in ['src/v3','scripts/v3']:
 shutil.copytree(R/folder,DEST/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
shutil.copy2(R/'scripts/ae.py',DEST/'scripts/ae.py')
for file in ['ENTREGA-V3.md','BRIEF.md','CURRENT-VERSION.json','Revisar-V3.html']:
 shutil.copy2(R/file,DEST/file)
(DEST/'output/v3').mkdir(parents=True,exist_ok=True);(DEST/'ae/v3').mkdir(parents=True,exist_ok=True);(DEST/'analysis/v3').mkdir(parents=True,exist_ok=True)
for file in ['El-Sistema-V3.mp4','El-Sistema-V3.srt','El-Sistema-V3.vtt','Contacto-V3.jpg']:
 shutil.copy2(R/'output/v3'/file,DEST/'output/v3'/file)
for file in ['final-probe.json','decode-check.log','encoded-loudness.log','black-scan.log','font.list_missing.json','footage.list_missing.json','mask-control-check.json','encoded-05.jpg','final-native-project.json']:
 shutil.copy2(R/'analysis/v3'/file,DEST/'analysis/v3'/file)
with AE(log=R/'analysis/v3/package-native.jsonl') as a:
 info=a.call('ae_project_info')['result'];ops=[]
 for x in info['items']:
  if x['name'] in used:ops.append({'operation':'footage.replace','args':{'item':x['id'],'path':str(DEST/'assets'/x['name'])}})
 for j in range(0,len(ops),90):
  q=a.call('ae_do',operation='batch.run',args={'ops':ops[j:j+90],'stopOnError':True});assert q['ok'] and not q['result'].get('failed'),q
 q=a.call('ae_do',operation='render.set_output',args={'queueIndex':1,'outputPath':str(DEST/'output/v3/El-Sistema-V3-Master.mov')});assert q['ok'],q
 q=a.call('ae_save_project',path=str(DEST/'ae/v3/El-Sistema-V3.aep'));assert q['ok'],q
 q=a.call('ae_do',operation='footage.list_missing',args={});(DEST/'analysis/v3/media-links-delivery.json').write_text(json.dumps(q,indent=2));assert q['result']['count']==0
shutil.copy2(DEST/'ae/v3/El-Sistema-V3.aep',R/'ae/v3/El-Sistema-V3.aep')
x=R/'output/v3/El-Sistema-V3.mp4';y=DEST/'output/v3/El-Sistema-V3.mp4';assert hashlib.sha256(x.read_bytes()).digest()==hashlib.sha256(y.read_bytes()).digest()
print(json.dumps({'delivery':str(DEST),'media':len(used),'video_bytes':y.stat().st_size,'native':str(DEST/'ae/v3/El-Sistema-V3.aep'),'copy_verified':True},ensure_ascii=False))
