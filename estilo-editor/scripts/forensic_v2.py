#!/usr/bin/env python3
"""Reproducible audit. All OCR tracks remain observations, never certified subtitles."""
import hashlib,json,statistics,sys,gzip
from collections import Counter
from pathlib import Path
from datetime import datetime,timezone
from common import ROOT,DATOS,VIDEOS,probe,src
OUT=DATOS/'revision-v2';OUT.mkdir(exist_ok=True)
def write(p,x):
 tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(x,ensure_ascii=False,indent=2));tmp.replace(p)
def read_vision(slug):
 file=ROOT/'analysis/vision'/f'{slug}.jsonl'
 for attempt in range(3):
  try:return list(map(json.loads,file.read_text().splitlines()))
  except TimeoutError:
   print(f'{slug}: local read timed out; retry {attempt+1}/3',flush=True)
 raise TimeoutError(f'Cannot read vision observations for {slug}')
def q(values,p):
 s=sorted(values);return round(s[round((len(s)-1)*p)],3) if s else None
def summary(values):return {'n':len(values),'p10':q(values,.1),'p50':q(values,.5),'p90':q(values,.9)}
manifest=json.loads((DATOS/'referencias.json').read_text())
if not any(x['slug']=='v8' for x in manifest['files']):
 p=src('v8');i=probe('v8');manifest['files'].append({'slug':'v8','original_filename':VIDEOS['v8'],'sha256':hashlib.file_digest(p.open('rb'),'sha256').hexdigest(),'bytes':p.stat().st_size,'frames':i['frames'],'fps_num':i['fps_num'],'fps_den':i['fps_den'],'available_at':str(p),'fallback_at':str(Path.home()/'Downloads'/VIDEOS['v8'])});write(DATOS/'referencias.json',manifest)
events=json.loads((DATOS/'eventos.json').read_text())
extra=OUT/'v8-events.json'
if extra.exists():events+=json.loads(extra.read_text())
corpus=[]
for slug in VIDEOS:
 p=DATOS/slug;i=probe(slug);texts=json.loads((p/'texts.json').read_text());raw=read_vision(slug)
 fids=[r['f'] for r in raw];assert fids==list(range(i['frames'])),f'OCR frame coverage mismatch: {slug}'
 aligned=json.loads((p/'align.json').read_text()).get('words',[]);matched={x['track'] for x in aligned if x.get('shown') and 'track' in x}
 tracks=[]
 for t in texts['tracks']:
  rows=t['per_frame'];frames=sorted({r[0] for r in rows});n=t['f_out']-t['f_in']+1
  stable=[b for a,b in zip(rows,rows[1:]) if b[0]==a[0]+1 and b[7]==a[7] and min(a[6],b[6])>=.5]
  motion=[]
  for a,b in zip(rows,rows[1:]):
   if b[0]==a[0]+1 and a[7]==b[7] and min(a[6],b[6])>=.5:
    motion.append([b[0],round((b[1]-a[1])*i['fps']/i['width'],5),round((b[2]-a[2])*i['fps']/i['height'],5)])
  track={k:v for k,v in t.items() if k!='per_frame'}
  track.update({'observedFrames':len(frames),'missingDetectionFrames':n-len(frames),'detectionCoverage':round(len(frames)/n,4),'transcriptCandidate':t['id'] in matched,'status':'automatic_ocr_unverified','fontIdentity':None,'fontSize':None,'alpha':None,'maskType':None,'firstVisiblePixel':None,'lastVisiblePixel':None,'trajectoryKind':None,'geometryColumns':texts['per_frame_columns'],'geometry':rows,'sameTextVelocityColumns':['frame','dx_widths_per_second','dy_heights_per_second'],'sameTextVelocity':motion,'warnings':['Caja OCR, no caja de tinta ni cuerpo tipográfico.','La pista puede fusionar palabras acumuladas o incluir texto físico.','Aparición OCR no certifica primer píxel; conf no es probabilidad calibrada.']})
  tracks.append(track)
 write(OUT/f'{slug}-tracks.json',{'slug':slug,'width':i['width'],'height':i['height'],'fps_num':i['fps_num'],'fps_den':i['fps_den'],'tracks':tracks})
 spans=sorted([[e['f0'],e['f1']] for e in events if e['slug']==slug and e['tipo']=='grafico'])
 merged=[]
 for a,b in spans:
  if merged and a<=merged[-1][1]+1:merged[-1][1]=max(b,merged[-1][1])
  else:merged.append([a,b])
 intervals=[(b[0]-a[0])/i['fps'] for a,b in zip(merged,merged[1:])]
 holds=[(b-a+1)/i['fps'] for a,b in merged]
 cov=json.loads((p/'exact-frames.json').read_text())
 cand=[t for t in tracks if t['transcriptCandidate']]
 source=next(x for x in manifest['files'] if x['slug']==slug)
 corpus.append({'slug':slug,'title':VIDEOS[slug],'source_sha256':source['sha256'],'width':i['width'],'height':i['height'],'frames':i['frames'],'fps_num':i['fps_num'],'fps_den':i['fps_den'],'seconds':i['frames']/i['fps'],'family':'ads90_variants' if slug.startswith(('v6-','v7-')) else slug,'ocrFrames':len(raw),'ocrTracks':len(tracks),'transcriptCandidateTracks':len(cand),'exactDuplicates':len(cov['native_identical_to_previous']),'nativeForensicComplete':False,'audioIdentified':False,'candidateCaptionStats':{'ink_height_px':summary([t['h'] for t in cand]),'box_width_pct':summary([t['w_pct'] for t in cand]),'center_y_pct':summary([t['cy_pct'] for t in cand])},'annotatedGraphics':{'spans':merged,'count':len(merged),'durations_seconds':[round(x,3) for x in holds],'onset_intervals_seconds':[round(x,3) for x in intervals],'interval_cv':round(statistics.pstdev(intervals)/statistics.mean(intervals),3) if len(intervals)>1 else None,'note':'Solo intervalos etiquetados grafico en notas. No censo completo de todo motion; cero significa no etiquetado. Se fusionan tramos contiguos para no duplicar escenas.'}})
write(OUT/'corpus.json',{'generatedAt':datetime.now(timezone.utc).isoformat(),'status':'forensic_study_in_progress','complete':False,'sources':corpus,'totalFrames':sum(x['frames'] for x in corpus),'totalOCRTracks':sum(x['ocrTracks'] for x in corpus),'independentFamilies':len({x['family'] for x in corpus}),'warnings':['OCR completo no equivale a revisión humana exhaustiva.','V6, V6 revisada y V7 pertenecen a una misma familia de variantes.','Los motivos editoriales son hipótesis contrastables, no acceso a la intención del autor.']})
enriched=[]
for j,event in enumerate(events):
 record=dict(event,id=f'event-{j}')
 record['source_note_sha256']=record.pop('source_sha256',None)
 record['source_video_sha256']=next(s['source_sha256'] for s in corpus if s['slug']==record['slug'])
 note=ROOT/record.get('source_note','')
 if note.is_file():record['source_note_sha256_current']=hashlib.sha256(note.read_bytes()).hexdigest()
 enriched.append(record)
write(OUT/'events.json',enriched)
rulefile=OUT/'rules.json'
if rulefile.exists():
 rules=json.loads(rulefile.read_text())
 for rule in rules:
  for e in rule['evidence']:
   source=next(s for s in corpus if s['slug']==e['slug']);e['sourceSha256']=source['source_sha256'];e['independentFamily']=source['family']
 write(rulefile,rules)
print(f"{len(corpus)} sources, {sum(x['frames'] for x in corpus)} native frames, {sum(x['ocrTracks'] for x in corpus)} OCR tracks, {len(events)} editorial observations")
for x in corpus:print(x['slug'],x['annotatedGraphics'])
