from pathlib import Path
import json, subprocess, shutil, os
R=Path(__file__).resolve().parents[1]; OLD=R.parents[0]; F=48
sources=json.load(open(OLD/'analysis/sources.json'))
# Fresh frame edit from the selected raw takes; no voice speed changes.
takes=[[(0,42),(52,130),(139,189)],[(1,48),(59,90)],[(1,47),(64,91)],[(1,95)],[(3,115)],[(1,54),(64,115)],[(1,43),(50,92)],[(0,141)],[(0,114)],[(0,28),(36,119)]]
segments=[]; clips=[]; head=0
for i,(s,ranges) in enumerate(zip(sources,takes),1):
 start=head
 for a,b in ranges:
  n=(b-a)*2;segments.append(dict(clip=i,src=s['name'],from_=head,duration=n,sourceFrame=a*2,sourceEnd=b*2));head+=n
 clips.append(dict(id=i,src=s['name'],from_=start,to=head))
for d in segments+clips:d['from']=d.pop('from_')
T=dict(fps=F,duration=head,video=segments,clips=clips)
(R/'remotion/src/timeline.json').write_text(json.dumps(T,indent=2))
for s in sources:
 dst=R/'remotion/public'/s['name']
 if not dst.exists():dst.symlink_to(s['path'])
for name in ['package.json','package-lock.json']:
 if (OLD/'remotion'/name).exists():shutil.copy2(OLD/'remotion'/name,R/'remotion'/name)
p=R/'remotion/node_modules'
if not p.exists():p.symlink_to(OLD/'remotion/node_modules',target_is_directory=True)
src='''import React from 'react';
import {AbsoluteFill,Composition,OffthreadVideo,Sequence,registerRoot,staticFile} from 'remotion';
import t from './timeline.json';
const Base=()=> <AbsoluteFill style={{backgroundColor:'#273e1b'}}>{t.video.map((s,i)=><Sequence key={i} from={s.from} durationInFrames={s.duration}><OffthreadVideo src={staticFile(s.src)} trimBefore={s.sourceFrame} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/></Sequence>)}</AbsoluteFill>;
registerRoot(()=> <Composition id="AD3-Montaje" component={Base} width={1080} height={1920} fps={48} durationInFrames={t.duration}/>);
'''
(R/'remotion/src/index.tsx').write_text(src)
(R/'remotion/render.mjs').write_text((OLD/'remotion/render.mjs').read_text().replace('concurrency:6','concurrency:4'))
inputs=[];filters=[]
for s in sources:inputs+=['-i',s['path']]
for j,s in enumerate(segments):filters.append(f"[{s['clip']-1}:a]atrim=start={s['sourceFrame']/F}:end={s['sourceEnd']/F},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.003,afade=t=out:st={s['duration']/F-.003}:d=0.003[a{j}]")
filters.append(''.join(f'[a{j}]' for j in range(len(segments)))+f'concat=n={len(segments)}:v=0:a=1[out]')
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',';'.join(filters),'-map','[out]','-c:a','pcm_s24le',str(R/'assets/Voz-Montada.wav')],check=True)
# Real source stills, never reference-video graphics.
for i,t in [(1,3.6),(2,1.0),(3,1.0),(5,1.0),(7,1.3),(8,1.5)]:
 subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',sources[i-1]['path'],'-frames:v','1','-q:v','2',str(R/f'assets/toma-{i:02d}.jpg')],check=True)
print(json.dumps(T['clips'],indent=2));print('NEW DURATION',head,head/F)
