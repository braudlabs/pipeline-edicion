#!/usr/bin/env python3
"""Coarse visual retrieval for raw/edited pairs. Candidates, never exact attribution."""
import concurrent.futures,json,subprocess
from fractions import Fraction
from pathlib import Path
import numpy as np
from PIL import Image,ImageOps
from common import ROOT,DATOS
out=DATOS/'raw-comparison';cache=ROOT/'analysis/raw-comparison';cache.mkdir(parents=True,exist_ok=True)
manifest=json.loads((out/'manifest.json').read_text())
videos=[d for d in manifest['files'] if any(s['codec_type']=='video' for s in d['streams'])]
def extract(d):
 s=next(s for s in d['streams'] if s['codec_type']=='video');fps=float(Fraction(s['r_frame_rate']));step=max(1,round(fps));folder=cache/d['sha256'][:12];folder.mkdir(exist_ok=True)
 if not (folder/'done.json').exists():
  subprocess.run(['ffmpeg','-v','error','-threads','2','-i',d['path'],'-vf',f'select=not(mod(n\\,{step})),scale=128:228:force_original_aspect_ratio=increase,crop=128:228','-fps_mode','passthrough','-start_number','0','-q:v','3',str(folder/'%05d.jpg')],check=True)
  (folder/'done.json').write_text(json.dumps({'step':step,'nominalFPS':fps}))
 return d,folder,step,fps
def feature(img,scale=1):
 w,h=img.size;cw,ch=w/scale,h/scale;im=img.crop(((w-cw)/2,(h-ch)/2,(w+cw)/2,(h+ch)/2)).convert('L').resize((16,28),Image.Resampling.BILINEAR)
 a=np.asarray(im,dtype=np.float32)/255;a-=a.mean();a/=max(float(a.std()),.08);g=np.concatenate([a.flatten(),np.diff(a,axis=0).flatten()*2,np.diff(a,axis=1).flatten()*2]);return g/(np.linalg.norm(g)+1e-8)
features=[];index=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for d,folder,step,fps in pool.map(extract,videos):
  for image in sorted(folder.glob('*.jpg')):
   im=Image.open(image);n=int(image.stem)*step
   for scale in [1,1.12,1.28,1.5]:
    features.append(feature(im,scale));index.append({'path':d['path'],'sha256':d['sha256'],'rawFrame':n,'approxSeconds':n/fps,'nominalFPS':fps,'cropScale':scale,'thumbnail':str(image)})
mat=np.stack(features);refs=json.loads((DATOS/'referencias.json').read_text())['files'];result=[]
for ref in refs:
 fps=ref['fps_num']/ref['fps_den'];fs=range(0,ref['frames'],max(1,round(fps)))
 queries=[];frames=[]
 for f in fs:
  p=ROOT/'analysis/frames'/ref['slug']/f'f{f:06d}.jpg'
  if p.exists():queries.append(feature(Image.open(p)));frames.append(f)
 scores=np.stack(queries)@mat.T
 for row,f in zip(scores,frames):
  order=np.argsort(row)[::-1];found=[];seen=set()
  for j in order:
   candidate=index[int(j)];key=candidate['path']
   if key in seen:continue
   seen.add(key);found.append({**candidate,'similarity':round(float(row[j]),5)})
   if len(found)==2:break
  result.append({'slug':ref['slug'],'editedFrame':f,'editedSeconds':f/fps,'candidates':found})
 print(ref['slug'],'retrieved',len(frames),flush=True)
(out/'candidates.json').write_text(json.dumps({'method':'1 native frame approximately per second; center-crop scales1/1.12/1.28/1.5; normalized luminance+gradient cosine. Scores are NOT probabilities. Top two distinct raw files, not exact temporal alignment.','rawSources':len(videos),'rawDescriptors':len(index),'matches':result},ensure_ascii=False,indent=2))
for ref in refs:
 candidates=[r for r in result if r['slug']==ref['slug']];candidates.sort(key=lambda r:r['candidates'][0]['similarity'],reverse=True)
 print(ref['slug'],[(round(r['editedSeconds'],2),Path(r['candidates'][0]['path']).name,round(r['candidates'][0]['approxSeconds'],2),r['candidates'][0]['similarity']) for r in candidates[:3]])
