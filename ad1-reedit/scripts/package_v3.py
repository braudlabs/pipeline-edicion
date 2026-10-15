from pathlib import Path
import json,shutil,zipfile,hashlib
R=Path(__file__).resolve().parents[1];D=Path((R/'analysis/delivery-path.txt').read_text());O=R/'output'
rows=[json.loads(l) for l in (R/'ae/v3-package-results.jsonl').read_text().splitlines()];assert len(rows)==6
for d in rows:
 s=d['result']['structuredContent'];assert s['ok'] and s.get('result',{}).get('ok',True) and not d['result'].get('isError')
info=rows[-1]['result']['structuredContent']['result'];aep=Path(info['file']);assert aep==D/'After-Effects/Cocina-Reedicion-V3.aep';assert aep.stat().st_size>1_000_000
assert rows[3]['result']['structuredContent']['result']['count']==0
assert rows[4]['result']['structuredContent']['result']['count']==0
media=[Path(i['file']) for i in info['items'] if i.get('file')]
for p in media:assert p.is_file() and p.is_relative_to(D/'After-Effects/assets'),p
comps=[i for i in info['items'] if i['type']=='CompItem']
v=json.loads((O/'Verificacion-V3.json').read_text());v.update({'nativeCompositions':len(comps),'nativeLayers':sum(i['layerCount'] for i in comps),'packagedMediaFiles':len(media),'missingMedia':0,'fontSubstitutions':0})
(O/'Verificacion-V3.json').write_text(json.dumps(v,ensure_ascii=False,indent=2))
for name in ['AD1-Cocina-V3.mp4','Creditos-V3.mp4','LEEME-V3.md','PROCEDENCIA-V3.json','Verificacion-V3.json','Portada-V3.jpg']:
 shutil.copy2(O/name,D/name)
files=[(aep,Path('After-Effects')/aep.name)]
files += [(p,p.relative_to(D)) for p in media]
files += [(p,p.relative_to(D)) for p in (D/'Remotion').rglob('*') if p.is_file() and not any(x.startswith('.') or x=='node_modules' for x in p.relative_to(D/'Remotion').parts)]
files += [(D/a,Path(b)) for a,b in [('LEEME-V3.md','LEEME.md'),('Verificacion-V3.json','Verificacion.json'),('Cocina-Reedicion.srt','Cocina-Reedicion.srt'),('CREDITOS.md','CREDITOS.md'),('PROCEDENCIA-V3.json','PROCEDENCIA.json')]]
archive=D/'Cocina-Proyectos-Editables-V3.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p,rel in files:z.write(p,str(Path('Cocina-V3')/rel))
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for p,rel in files:assert hashlib.sha256(z.read(str(Path('Cocina-V3')/rel))).digest()==hashlib.sha256(p.read_bytes()).digest()
link=O/archive.name
if not link.exists():link.symlink_to(archive)
current={'version':3,'design':str(R/'ae/design-v3.json'),'editableProject':str(aep),'finalVideo':str(D/'AD1-Cocina-V3.mp4'),'focusedPreview':str(D/'Creditos-V3.mp4'),'editableArchive':str(archive),'review':'http://127.0.0.1:8778/Revisar-V3.html','previousVersionPreserved':True}
(R/'CURRENT-VERSION.json').write_text(json.dumps(current,ensure_ascii=False,indent=2))
report={'archive':str(archive),'bytes':archive.stat().st_size,'files':len(files),'crcVerified':True,'allFileHashesVerified':True,'mediaFiles':len(media),'nativeComps':len(comps),'nativeLayers':sum(i['layerCount'] for i in comps)}
(R/'analysis/v3/package-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
