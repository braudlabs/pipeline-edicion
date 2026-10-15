from pathlib import Path
import json,subprocess,shutil
R=Path(__file__).resolve().parents[1];P=Path((R/'source-path.txt').read_text());F=48
sources=json.load(open(R/'analysis/sources.json'));takes=[[(0,192)],[(1,48),(58,91)],[(1,48),(63,92)],[(1,96)],[(5,116)],[(1,55),(63,117)],[(1,45),(49,94)],[(0,143)],[(1,117)],[(0,30),(35,120)]]
segments=[];clips=[];head=0
for i,(s,rs) in enumerate(zip(sources,takes),1):
 start=head
 for a,b in rs:
  n=(b-a)*2;segments.append({'clip':i,'src':s['name'],'from':head,'duration':n,'sourceFrame':a*2,'sourceEnd':b*2});head+=n
 clips.append({'id':i,'src':s['name'],'from':start,'to':head})
T={'fps':F,'duration':head,'video':segments,'clips':clips};(R/'remotion/src/timeline.json').write_text(json.dumps(T,indent=2));print('Timeline',head,'frames',head/F,'seconds');print(clips)
# Map spoken tokens, correcting recognizer spellings from the supplied script.
W=[]
trans=json.load(open(R/'analysis/transcripts.json'))
for i,c in enumerate(trans,1):
 for w in c['words']:
  a,b=w['start']*F,w['end']*F
  for seg in [s for s in segments if s['clip']==i]:
   if seg['sourceFrame']<=max(a,b-1)<seg['sourceEnd'] or (a<seg['sourceFrame']<b):
    aa=max(0,a-seg['sourceFrame']);bb=min(seg['duration'],b-seg['sourceFrame']);
    if bb>aa:W.append({'text':w['word'].strip(),'from':seg['from']+round(aa),'to':seg['from']+round(bb),'clip':i});break
(R/'analysis/mapped-words.json').write_text(json.dumps(W,ensure_ascii=False,indent=2))
# Audio cuts are identical to the image edit; no time-stretch.
inputs=[];filters=[]
for i,s in enumerate(sources):inputs+=['-i',s['path']]
for j,s in enumerate(segments):filters.append(f"[{s['clip']-1}:a]atrim=start={s['sourceFrame']/F}:end={s['sourceEnd']/F},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:d=0.004,afade=t=out:st={(s['duration']/F)-.004}:d=0.004[a{j}]")
filters.append(''.join(f'[a{j}]' for j in range(len(segments)))+f'concat=n={len(segments)}:v=0:a=1[out]')
subprocess.run(['ffmpeg','-v','error','-y',*inputs,'-filter_complex',';'.join(filters),'-map','[out]','-c:a','pcm_s24le',str(R/'assets/Voz-Montada.wav')],check=True)
# Exported sources are supplied as is; generated photographic inserts use these originals.
