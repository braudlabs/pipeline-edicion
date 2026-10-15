import re
from pathlib import Path
import json,textwrap
from retime import T,D
R=Path(__file__).resolve().parents[1];words=json.loads((R/'analysis/words.json').read_text());groups=[];g=[]
def text(xs):return ' '.join(x['word'].strip() for x in xs)
for i,w in enumerate(words):
 w=dict(w);w['word']=w['word'].strip().replace('guión','guion').replace('subtítulo','subtitulo')
 if w['word']=='sistema.':w['word']='Sistema.'
 if w['word']=='Tu' and i+1<len(words) and words[i+1]['word'].strip() in ['apruebas','me']:w['word']='Tú'
 candidate=g+[w]
 if g and (len(textwrap.wrap(text(candidate),40))>2 or T(w['end'])-T(g[0]['start'])>3.25 or T(w['start'])-T(g[-1]['end'])>.20):groups.append(g);g=[]
 g.append(w)
 if w['word'].endswith(('.',',','?','!')) and T(w['end'])-T(g[0]['start'])>1.0:groups.append(g);g=[]
if g:groups.append(g)
def stamp(t):
 m=round(t*1000);h,m=divmod(m,3600000);mi,m=divmod(m,60000);se,ms=divmod(m,1000);return f'{h:02}:{mi:02}:{se:02},{ms:03}'
blocks=[]
for i,g in enumerate(groups):
 a=T(g[0]['start']);b=min(T(g[-1]['end'])+.06,T(groups[i+1][0]['start'])-.005 if i+1<len(groups) else D)
 blocks.append(f'{i+1}\n{stamp(a)} --> {stamp(max(a+.06,b))}\n'+ '\n'.join(textwrap.wrap(text(g),40))+'\n')
S='\n'.join(blocks);(R/'output/El-Sistema-V2.srt').write_text(S);(R/'output/El-Sistema-V2.vtt').write_text('WEBVTT\n\n'+re.sub(r'(\d{2}:\d{2}:\d{2}),(\d{3})',r'\1.\2',S))
assert sum(len(x) for x in groups)==len(words)
print(len(groups),'cues;',len(words),'words preserved; <=2 lines')
