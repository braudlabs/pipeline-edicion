from pathlib import Path
import sys,json,subprocess,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from retime import T
R=Path(__file__).resolve().parents[2]; RATE=1.14
# Only complete thoughts; cuts are in pauses or at original sentence boundaries.
ranges=[('hook',0,5.95),('simple',7.94,13.53),('inside',13.79,20.67),('script',20.78,22.31),('identity',22.56,27.23),('model',27.23,32.0),('map',32.09,36.20),('quality',36.30,38.58),('edit',45.21,53.37),('variants',54.54,61.04),('close',63.10,66.99)]
segs=[]; cursor=0
for label,a,b in ranges:
 d=(T(b)-T(a))/RATE;segs.append(dict(label=label,source_in=a,source_out=b,v2_in=T(a),v2_out=T(b),start=cursor,end=cursor+d));cursor+=d
D=math.ceil((cursor+.8)*30)/30
J={'rate':RATE,'duration':D,'voice_end':cursor,'segments':segs}
(R/'src/v3/edit-map.json').write_text(json.dumps(J,indent=2))
W=json.loads((R/'analysis/words.json').read_text());out=[]
for s in segs:
 for w in W:
  if s['source_in']<=w['start']<s['source_out']:
   z=dict(w);z['start']=s['start']+(T(w['start'])-T(s['source_in']))/RATE;z['end']=s['start']+(T(w['end'])-T(s['source_in']))/RATE
   z['word']=z['word'].replace('guión','guion').replace('subtítulo','subtitulo');out.append(z)
(R/'src/v3/words.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for s in segs:print(f"{s['label']:10} {s['start']:6.3f} - {s['end']:6.3f}")
print('Duration',D,'words',len(out))
if '--audio' in sys.argv:
 filters=[]
 for i,s in enumerate(segs):
  filters.append(f"[0:a]atrim=start={s['v2_in']}:end={s['v2_out']},asetpts=PTS-STARTPTS,afade=t=in:d=0.003,afade=t=out:st={s['v2_out']-s['v2_in']-.004}:d=0.004,atempo={RATE},apad,atrim=duration={s['end']-s['start']}[a{i}]")
 filters.append(''.join(f'[a{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,apad,atrim=duration={D}[out]')
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(R/'assets/Voz-V2.wav'),'-filter_complex',';'.join(filters),'-map','[out]','-ar','48000',str(R/'assets/v3/Voice.wav')],check=True)
