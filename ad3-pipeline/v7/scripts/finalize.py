from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess
r=Path(__file__).resolve().parents[1];o=r/'output';a=r/'analysis'
rows=[json.loads(s)['result']['structuredContent'] for s in (r/'ae/package-results.jsonl').open()];assert len(rows)==3 and all(x['ok'] for x in rows)
res=rows[0]['result'];assert res['failed']==0 and res['results'][-3]['count']==0 and res['results'][-2]['count']==0
info=rows[-1]['result'];comps=[x for x in info['items'] if x['type']=='CompItem']
probe=json.loads((a/'final-probe.json').read_text());v=next(x for x in probe['streams'] if x['codec_type']=='video');audio=next(x for x in probe['streams'] if x['codec_type']=='audio')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4194304),b''):h.update(b)
 return h.hexdigest()
with (a/'final-decode.log').open('w') as log:subprocess.run(['ffmpeg','-v','error','-i',str(o/'AD3-Pipeline-V7.mp4'),'-f','null','-'],stderr=log,stdout=subprocess.DEVNULL,check=True)
assert not (a/'final-decode.log').read_text()
# Verify unchanged green-version segments are identical, and the retimed raw voice is aligned.
parts=[0,1,3,4,6,7,8,9,12];assert all(sha(a/f'parts/{i:02d}.mp4')==sha(r.parent/f'v5/analysis/parts/{i:02d}.mp4') for i in parts)
import numpy as np
def voice(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ac','2','-ar','48000','-']),np.float32).reshape(-1,2)
x=voice(r.parent/'v4/assets/Voz-Montada.wav');y=voice(r/'assets/Voz-Montada.wav');assert len(y)==len(x)+18000
voiceDiff=max(float(abs(x[:1940000]-y[:1940000]).max()),float(abs(x[1940000:]-y[1958000:]).max()));assert voiceDiff<.000001
assert np.count_nonzero(y[1940000:1958000])==0
scope=json.loads((a/'scope-check.json').read_text());assert not scope['masterCaptionOverlaps'] and scope['productionToCTASeparationFrames']==9
# Measure the changed final mix rather than inheriting previous audio figures.
s=subprocess.run(['ffmpeg','-hide_banner','-i',str(o/'AD3-Pipeline-V7.mp4'),'-af','loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
levels=json.loads(s[s.rfind('{'):s.rfind('}')+1])
qa={'resolution':[v['width'],v['height']],'fps':48,'frames':int(v['nb_frames']),'duration':float(v['duration']),'audioDuration':float(audio['duration']),'fullDecodeErrors':0,'nativeComps':len(comps),'nativeLayers':sum(c['layerCount'] for c in comps),'missingFonts':0,'missingMedia':0,'videoSha256':sha(o/'AD3-Pipeline-V7.mp4'),'mixLUFS':float(levels['input_i']),'mixTruePeakDBTP':float(levels['input_tp']),'scopeCheck':scope,'unchangedVideoChunksIdenticalToV5':parts,'rawVoiceMaximumDifferenceOutsideInsertedPause':voiceDiff,'addedPauseSilentRawVoiceSamples':18000,'generatedAssets':{'provider':'Higgsfield CLI','model':'soul_cinematic','count':4,'dimensions':[2048,2048],'prompts':'Proyecto/PROMPTS-HIGGSFIELD.json','imagegenAssetsUsed':False},'visualReview':'Native frames covering caption handoff, box transition, new thumbnails, production/CTA and final offer inspected. Full MP4 decode passes. Voice verified by source timing and aligned waveform, without claiming subjective full audio audition.','userApproval':False}
assert qa['frames']==2180 and abs(qa['duration']-qa['audioDuration'])<.0001
(a/'QA-FINAL.json').write_text(json.dumps(qa,indent=2));shutil.copy2(a/'QA-FINAL.json',o/'Proyecto/QA-FINAL.json')
subprocess.run(['ffmpeg','-v','error','-y','-ss','45','-i',str(o/'AD3-Pipeline-V7.mp4'),'-frames:v','1','-q:v','2',str(o/'poster.jpg')],check=True)
prev=json.loads((r.parent/'CURRENT-VERSION.json').read_text());assert prev['version']==6
prev['userFeedback']='Pide corregir solapes de solo/Esta y producción/Entra en, mejorar entrada de caja, sustituir fotos repetidas del sistema y retrasar el cierre. Rechaza las primeras imágenes de imagegen; solicita Higgsfield Soul Cinema y volver al verde de antes.'
dest=Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-16-ad3-pipeline-autonomo/edicion-final/V7')
meta={'version':7,'status':'rendered-and-inspected','userApproval':False,'duration':qa['duration'],'fps':48,'width':1080,'height':1920,'video':str(dest/'AD3-Pipeline-V7.mp4'),'aep':str(dest/'Proyecto/After-Effects/AD3-Pipeline-V7.aep'),'editables':str(dest/'AD3-Pipeline-V7-Editables.zip'),'review':'http://127.0.0.1:8784/Revisar-V7.html','videoSha256':qa['videoSha256'],'previousVersion':prev,'creativeDirection':'Restores V5 olive green, cream typography and native geometry. Four category photographs from Higgsfield Soul Cinematic replace repeated speaker stills.','revisionScope':['End solo at frame 340 to avoid Esta overlap','Larger entering box panel and shorter zoom; finishes at frame 840','Four distinct Soul Cinematic category photos','Delay final spoken CTA and its graphics by 18 frames; no production/Entra en overlap'],'sourceTimeline':str(r/'remotion/src/timeline.json'),'qa':str(a/'QA-FINAL.json')}
(o/'CURRENT-VERSION.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False))
with zipfile.ZipFile(o/'AD3-Pipeline-V7-Editables.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in (o/'Proyecto').rglob('*'):
  if p.is_file():z.write(p,str(Path('AD3-Pipeline-V7-Editables')/p.relative_to(o/'Proyecto')))
with zipfile.ZipFile(o/'AD3-Pipeline-V7-Editables.zip') as z:assert z.testzip() is None
print('V7 verified:',qa['duration'],'seconds;',qa['mixLUFS'],'LUFS;',qa['mixTruePeakDBTP'],'dBTP;',qa['videoSha256'])
