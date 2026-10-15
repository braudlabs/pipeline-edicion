from pathlib import Path
import subprocess,json,shutil
p=Path(__file__).resolve().parent.parent;d=p/'study/mask-input';d.mkdir(exist_ok=True);tmp=p/'study/frames-per-scene';tmp.mkdir(exist_ok=True)
frames=json.loads((p/'study/mask-frames.json').read_text());t=json.loads((p/'timeline.json').read_text())
for s in t['scenes']:
 fs=[f for f in frames if s['record_in_frame']<=f<s['record_out_frame']]
 if not fs:continue
 src=[f-s['record_in_frame']+s['source_in_frame'] for f in fs]
 ranges=[]
 for n in src:
  if ranges and n==ranges[-1][1]+1:ranges[-1][1]=n
  else:ranges.append([n,n])
 select='+'.join('between(n\\,%d\\,%d)'%(a,b) for a,b in ranges)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'public'/s['asset']),'-vf',f'select={select},scale=540:960','-fps_mode','passthrough',str(tmp/'%04d.png')],check=True)
 for i,f in enumerate(fs):(tmp/f'{i+1:04}.png').replace(d/f'{f:04}.png')
print('Prepared',len(frames),'exact source frame inputs')
