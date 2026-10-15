from pathlib import Path
import json,hashlib,shutil,zipfile,subprocess
r=Path(__file__).resolve().parents[1];o=r/'output';a=r/'analysis';prevDir=r.parent/'v5'
rows=[json.loads(s)['result']['structuredContent'] for s in (r/'ae/package-results.jsonl').open()]
assert all(x['ok'] for x in rows)
res=rows[0]['result'];assert res['failed']==0
assert res['results'][7]['count']==0 and res['results'][8]['count']==0
info=rows[-1]['result'];comps=[x for x in info['items'] if x['type']=='CompItem']
probe=json.loads((a/'final-probe.json').read_text());v=next(x for x in probe['streams'] if x['codec_type']=='video');audio=next(x for x in probe['streams'] if x['codec_type']=='audio')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
videoHash=sha(o/'AD3-Pipeline-V6.mp4')
with (a/'final-decode.log').open('w') as log:subprocess.run(['ffmpeg','-v','error','-i',str(o/'AD3-Pipeline-V6.mp4'),'-f','null','-'],stderr=log,stdout=subprocess.DEVNULL,check=True)
assert not (a/'final-decode.log').read_text()
# Compare exact encoded AAC payloads, without container metadata.
def audioHash(p):return hashlib.sha256(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','-'])).hexdigest()
audioIdentical=audioHash(o/'AD3-Pipeline-V6.mp4')==audioHash(prevDir/'output/AD3-Pipeline-V5.mp4');assert audioIdentical
parts=[i for i in range(16) if i not in json.loads((a/'affected-parts.json').read_text())]
assert all(sha(a/f'parts/{i:02d}.mp4')==sha(prevDir/f'analysis/parts/{i:02d}.mp4') for i in parts)
diffs=json.loads((a/'native-diff.json').read_text());unexpected=[d for d in diffs if '/fillColor/' not in d[0] and not d[0].startswith('00 - Verde BRAUD/layers/2/effectsGroup/groups/0/properties/') and not d[0].endswith('/compName')];assert not unexpected
qa={'resolution':[v['width'],v['height']],'fps':48,'frames':int(v['nb_frames']),'duration':float(v['duration']),'audioDuration':float(audio['duration']),'fullDecodeErrors':0,'nativeComps':len(comps),'nativeLayers':sum(x['layerCount'] for x in comps),'missingFonts':0,'missingMedia':0,'videoSha256':videoHash,'mixLUFS':-14.16,'mixTruePeakDBTP':-1.48,'encodedAudioBitIdenticalToV5':audioIdentical,'unaffectedChunksBitIdenticalToV5':parts,'nativePropertiesDiff':'Only 11 caption fill colors, 2 gradient colors and main composition version name differ. All other inspected layer properties, keyframes, font metrics and effects are identical.','colors':json.loads((a/'color-changes.json').read_text()),'visualReview':'Native frames 414, 900, 1625 and 2070 inspected for warm caption/background color and contrast. Rendered video decoded in full.','userApproval':False,'scope':'Warm color variant of V5. No timing, footage, camera, motion, size or placement changes.'}
assert qa['frames']==2162 and abs(qa['duration']-qa['audioDuration'])<0.0001
(a/'QA-FINAL.json').write_text(json.dumps(qa,indent=2));shutil.copy2(a/'QA-FINAL.json',o/'Proyecto/QA-FINAL.json')
subprocess.run(['ffmpeg','-v','error','-y','-ss','44.5','-i',str(o/'AD3-Pipeline-V6.mp4'),'-frames:v','1','-q:v','2',str(o/'poster.jpg')],check=True)
prev=json.loads((r.parent/'CURRENT-VERSION.json').read_text());assert prev['version']==5
prev['userFeedback']='Va, está de locos. Solicita una variante que cambie únicamente el verde de los subtítulos y del fondo por rojo cálido.'
dest=Path('/Users/alejandrorubiocamarero/Desktop/El director/sistema-ale/cliente/creativos/2026-09-16-ad3-pipeline-autonomo/edicion-final/V6')
meta={'version':6,'status':'rendered-and-inspected','userApproval':False,'duration':qa['duration'],'fps':48,'width':1080,'height':1920,'video':str(dest/'AD3-Pipeline-V6.mp4'),'aep':str(dest/'Proyecto/After-Effects/AD3-Pipeline-V6.aep'),'editables':str(dest/'AD3-Pipeline-V6-Editables.zip'),'review':'http://127.0.0.1:8783/Revisar-V6.html','videoSha256':videoHash,'previousVersion':prev,'creativeDirection':prev['creativeDirection']+' V6 changes only green caption fills and gradient background to warm red/terracotta.','revisionScope':qa['scope'],'sourceTimeline':prev['sourceTimeline'],'qa':str(a/'QA-FINAL.json')}
(o/'CURRENT-VERSION.json').write_text(json.dumps(meta,indent=2,ensure_ascii=False))
with zipfile.ZipFile(o/'AD3-Pipeline-V6-Editables.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in (o/'Proyecto').rglob('*'):
  if p.is_file():z.write(p,str(Path('AD3-Pipeline-V6-Editables')/p.relative_to(o/'Proyecto')))
with zipfile.ZipFile(o/'AD3-Pipeline-V6-Editables.zip') as z:assert z.testzip() is None
print('V6 ready: 2162 frames, 1080x1920, 48fps, audio bit identical, archive verified; SHA256',videoHash)
