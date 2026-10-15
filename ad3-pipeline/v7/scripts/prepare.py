from pathlib import Path
import json,shutil,os,subprocess,numpy as np,re
R=Path(__file__).resolve().parents[1];base=R.parent/'v4';pack=R.parent/'v6/output/Proyecto';F=48;D=18;CUT=1940
T=json.loads((base/'remotion/src/timeline.json').read_text());T['duration']+=D
for s in T['video']:
 if s['from']>=CUT:s['from']+=D
T['video'].append({'clip':9,'src':'09-linea-produccion.mp4','from':CUT,'duration':D,'sourceFrame':227,'sourceEnd':228,'hold':True});T['video'].sort(key=lambda x:x['from'])
for c in T['clips']:
 if c['id']==10:c['from']+=D;c['to']+=D
(R/'remotion/src/timeline.json').write_text(json.dumps(T,indent=2))
for n in ['package.json','package-lock.json','render.mjs']:shutil.copy2(pack/'Remotion'/n,R/'remotion'/n)
# Render to the working assets; the package keeps its portable render destination later.
p=R/'remotion/render.mjs';p.write_text(p.read_text().replace('../After-Effects/Assets','../assets'))
for p in (pack/'Remotion/public').iterdir():os.link(p,R/'remotion/public'/p.name)
(R/'remotion/node_modules').symlink_to(base/'remotion/node_modules',target_is_directory=True)
(R/'remotion/src/index.tsx').write_text('''import React from 'react';
import {AbsoluteFill,Composition,OffthreadVideo,Sequence,Freeze,registerRoot,staticFile} from 'remotion';
import t from './timeline.json';
const Base=()=> <AbsoluteFill style={{backgroundColor:'#273e1b'}}>{t.video.map((s,i)=><Sequence key={i} from={s.from} durationInFrames={s.duration}>{s.hold ? <Freeze frame={s.sourceFrame}><OffthreadVideo src={staticFile(s.src)} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/></Freeze> : <OffthreadVideo src={staticFile(s.src)} trimBefore={s.sourceFrame} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/>}</Sequence>)}</AbsoluteFill>;
registerRoot(()=> <Composition id="AD3-Montaje" component={Base} width={1080} height={1920} fps={48} durationInFrames={t.duration}/>);
''')
x=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(base/'assets/Voz-Montada.wav'),'-ar','48000','-ac','2','-f','f32le','-']),np.float32).reshape(-1,2)
x=np.concatenate([x[:CUT*1000],np.zeros((D*1000,2),np.float32),x[CUT*1000:]])
subprocess.run(['ffmpeg','-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i','-','-c:a','pcm_s24le',str(R/'assets/Voz-Montada.wav')],input=x.astype(np.float32).tobytes(),check=True)
s=(base/'scripts/mix.py').read_text().replace('810/48','820/48').replace('1949/48','1967/48').replace('2012/48','2030/48');(R/'scripts/mix.py').write_text(s)
srt=(R.parent/'v6/output/AD3-Pipeline-V6.srt').read_text();blocks=[]
def parse(s):
 h,m,ss,ms=map(int,re.split('[:,]',s));return round((h*3600+m*60+ss+ms/1000)*48)
def stamp(f):
 ms=round(f/48*1000);return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
for block in srt.strip().split('\n\n'):
 lines=block.splitlines();a,b=map(parse,lines[1].split(' --> '));txt='\n'.join(lines[2:])
 if txt=='solo':b=min(b,340)
 if a>=CUT:a+=D
 if b>CUT:b+=D
 blocks.append(f'{len(blocks)+1}\n{stamp(a)} --> {stamp(b)}\n{txt}')
(R/'output/AD3-Pipeline-V7.srt').write_text('\n\n'.join(blocks)+'\n')
print('Prepared',T['duration'],'frames; CTA delayed 18 frames / 0.375s')
