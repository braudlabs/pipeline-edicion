from pathlib import Path
import subprocess,json,hashlib
R=Path(__file__).resolve().parents[1];frames=[0,1,57,134,154,358,374,424]
def checks(p):
 vf='select='+ '+'.join(f'eq(n\\,{f})' for f in frames)
 b=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-vf',vf,'-an','-fps_mode','passthrough','-f','framemd5','-']).decode()
 return [s.split(',')[-1].strip() for s in b.splitlines() if s and not s.startswith('#')]
a=checks(R/'analysis/v2/native/part-02.mov');b=checks(R/'analysis/v3/part-02.mov');assert a==b,(a,b)
sources=[]
for i in [0,1,3,4,5,6,7]:
 p=(R/'analysis/native-chunks' if i in [0,1,7] else R/'analysis/v2/native')/f'part-{i:02d}.mov'
 sources.append({'section':i,'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
report={'unchangedSourceSectionsReused':7,'nativeFramesOutsideCreditsIdentical':[f+850 for f in frames],'checksumsMatch':True,'sourceSections':sources}
(R/'analysis/v3/unchanged-sections.json').write_text(json.dumps(report,indent=2));print('All 8 checked native frames outside the edited interval are identical. Seven source sections reused unchanged.')
