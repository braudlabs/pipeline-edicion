#!/usr/bin/env python3
"""Readable native-frame pairs for manual attribution; candidates are not auto-approved."""
import io,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from common import ROOT,DATOS
out=ROOT/'analysis/raw-comparison/pairs';out.mkdir(parents=True,exist_ok=True)
matches=json.loads((DATOS/'raw-comparison/candidates.json').read_text())['matches']
refs=json.loads((DATOS/'referencias.json').read_text())['files']
requests=[('v8',180),('v8',1980),('v8',2160),('v8',2400),('v5-maquina',120),('v5-maquina',1380),('v2-churros',456),('v6-ads90',1500),('v1-pagado',672),('v3-ia-cara',1128)]
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',18)
def grab(path,n):
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-vf',f'select=eq(n\\,{n})','-frames:v','1','-fps_mode','passthrough','-f','image2pipe','-vcodec','png','-'])
 return Image.open(io.BytesIO(raw)).convert('RGB')
pairs_file=DATOS/'raw-comparison/pairs.json'
previous={p['id']:p for p in json.loads(pairs_file.read_text())} if pairs_file.exists() else {}
pairs=[]
for slug,frame in requests:
 m=next(r for r in matches if r['slug']==slug and r['editedFrame']==frame);c=m['candidates'][0];ref=next(r for r in refs if r['slug']==slug)
 a=grab(c['path'],c['rawFrame']);b=grab(ref['available_at'],frame)
 canvas=Image.new('RGB',(740,750),'#14241e');d=ImageDraw.Draw(canvas)
 d.text((10,10),f'BRUTO f{c["rawFrame"]} / {c["approxSeconds"]:.3f}s',font=font,fill='white');d.text((380,10),f'EDITADO f{frame} / {m["editedSeconds"]:.3f}s',font=font,fill='white')
 for x,im in [(10,a),(380,b)]:canvas.paste(im.resize((350,622)),(x,45))
 d.text((10,682),slug+' · '+Path(c['path']).name[:48],font=font,fill='#d5ed91')
 d.text((10,712),'Candidato temporal: revisar antes de atribuir diferencias.',font=font,fill='#c4d1c9')
 name=f'{slug}-{frame}.jpg';canvas.save(out/name,quality=93)
 pairs.append({'id':f'{slug}-{frame}','slug':slug,'editedFrame':frame,'editedSeconds':m['editedSeconds'],'editedSHA256':ref['sha256'],'rawPath':c['path'],'rawFrame':c['rawFrame'],'rawApproxSeconds':c['approxSeconds'],'rawSHA256':c['sha256'],'retrievalSimilarity':c['similarity'],'sheet':name,'reviewStatus':'pending','observations':[],'limitation':'Candidato a correspondencia; frame n exacto de cada archivo, alineación entre archivos aún no certificada.'})
 old=previous.get(pairs[-1]['id'])
 if old and all(old.get(k)==pairs[-1].get(k) for k in ['editedSHA256','editedFrame','rawSHA256','rawFrame']):
  for k in ['reviewStatus','observations','limitation']:
   if k in old:pairs[-1][k]=old[k]
 print(name,flush=True)
(DATOS/'raw-comparison/pairs.json').write_text(json.dumps(pairs,ensure_ascii=False,indent=2))
