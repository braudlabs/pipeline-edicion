from pathlib import Path
import json,shutil,hashlib,zipfile,subprocess,numpy as np
R=Path(__file__).resolve().parents[1];o=R/'output';a=R/'analysis'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4194304),b''):h.update(b)
    return h.hexdigest()
rows=[json.loads(x)['result']['structuredContent'] for x in (R/'ae/package-results.jsonl').read_text().splitlines()]
assert len(rows)==4 and all(x['ok'] for x in rows)
batch=rows[1]['result'];assert batch['failed']==0
assert batch['results'][-3]['count']==0 and batch['results'][-2]['count']==0
def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2)
old=decode(R.parent/'v7/assets/Mezcla-Final.wav');new=decode(R/'assets/Mezcla-Final.wav')
assert np.max(abs(old[:1932000]-new[:1932000]))<.000001
assert np.max(abs(old[1958000:]-new[1958000:]))<.000001
assert sha(R.parent/'v7/assets/Musica.wav')==sha(R/'assets/Musica.wav')
assert sha(R.parent/'v7/assets/Efectos.wav')==sha(R/'assets/Efectos.wav')
qa=json.loads((a/'stream-verification.json').read_text());qa['audioRepair']=json.loads((a/'audio-repair.json').read_text())
qa.update({'missingFonts':0,'missingMedia':0,'videoSha256':sha(o/'AD3-Pipeline-V8.mp4'),'unchangedPCMOutsideRepair':True,'musicAndSFXIdentical':True,'duration':2180/48,'fps':48,'frames':2180,'resolution':[1080,1920],'externalAudioAnalysis':'Automatic approval review blocked private-audio upload; no external listening analysis performed. Used exact local waveform/source comparison.','userApproval':False})
(a/'QA-FINAL.json').write_text(json.dumps(qa,indent=2));shutil.copy2(a/'QA-FINAL.json',o/'Proyecto/QA-FINAL.json')
previous=json.loads((R.parent/'v7/output/CURRENT-VERSION.json').read_text())
previous['userFeedback']='Se corta la terminación de producción y salta al cierre. Corregir el final de la palabra.'
dest=Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-16-ad3-pipeline-autonomo/edicion-final/V8')
meta={'version':8,'status':'rendered-and-locally-verified','userApproval':False,'duration':2180/48,'fps':48,'width':1080,'height':1920,'video':str(dest/'AD3-Pipeline-V8.mp4'),'aep':str(dest/'Proyecto/After-Effects/AD3-Pipeline-V8.aep'),'editables':str(dest/'AD3-Pipeline-V8-Editables.zip'),'review':'http://127.0.0.1:8785/Revisar-V8.html','videoSha256':qa['videoSha256'],'previousVersion':previous,'revisionScope':'Restore the final 0.30 seconds of the original producción voice take within the existing pause. V7 video stream is byte-identical; no picture or motion changes.','sourceTimeline':str(o/'Proyecto/Remotion/src/timeline.json'),'qa':str(a/'QA-FINAL.json')}
(o/'CURRENT-VERSION.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False))
with zipfile.ZipFile(o/'AD3-Pipeline-V8-Editables.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
    for p in (o/'Proyecto').rglob('*'):
        if p.is_file():z.write(p,str(Path('AD3-Pipeline-V8-Editables')/p.relative_to(o/'Proyecto')))
with zipfile.ZipFile(o/'AD3-Pipeline-V8-Editables.zip') as z:assert z.testzip() is None
print('V8 passed:',qa['videoSha256'])
