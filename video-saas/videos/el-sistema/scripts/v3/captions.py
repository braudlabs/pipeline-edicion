from pathlib import Path
import json,textwrap
R=Path(__file__).resolve().parents[2];w=json.loads((R/'src/v3/words.json').read_text());chunks=[];cur=[]
for z in w:
 if cur and (z['start']-cur[-1]['end']>.33 or len(' '.join(q['word'].strip() for q in cur))+len(z['word'])>67):chunks.append(cur);cur=[]
 cur.append(z)
 if z['word'].strip().endswith(('.',',')):chunks.append(cur);cur=[]
if cur:chunks.append(cur)
def stamp(t,sep=','):
 x=round(max(0,t)*1000);return f'{x//3600000:02}:{x//60000%60:02}:{x//1000%60:02}{sep}{x%1000:03}'
srt=[];vtt=['WEBVTT\n']
for i,q in enumerate(chunks):
 s=' '.join(x['word'].strip() for x in q).replace('Tu apruebas','Tú apruebas').replace('El sistema.','El Sistema.');s='\n'.join(textwrap.wrap(s,width=37));a=q[0]['start'];b=min(q[-1]['end']+.035,chunks[i+1][0]['start']-.012 if i+1<len(chunks) else 46.3)
 srt.append(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}\n');vtt.append(f'{stamp(a,".")} --> {stamp(b,".")}\n{s}\n')
(R/'output/v3/El-Sistema-V3.srt').write_text('\n'.join(srt));(R/'output/v3/El-Sistema-V3.vtt').write_text('\n'.join(vtt));print(len(chunks),'cues')
