from pathlib import Path
import json,subprocess,hashlib
from PIL import Image
import numpy as np
p=Path(__file__).resolve().parent;prev=p.parent/'v04';out=p/'Andromeda-00-38s-V05-PREVIEW.mp4';before=prev/'Andromeda-00-38s-V04-PREVIEW.mp4'
for name in ['timeline.json','choreography.json','audio.json']:assert (p/name).read_bytes()==(prev/name).read_bytes(),name
assert (p/'public/assets/mix-preview.wav').read_bytes()==(prev/'public/assets/mix-preview.wav').read_bytes()
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames','-of','json',str(out)]));s=probe['streams'][0];assert (s['width'],s['height'],s['r_frame_rate'],s['nb_frames'])==(1080,1920,'48/1','1840')
frames=[120,479,514,551,1000,1430,1482,1723,1826];sel='+'.join('eq(n\\,%d)'%f for f in frames);d=p/'study/compare';d.mkdir(exist_ok=True)
for f,label in [(out,'v05'),(before,'v04')]:subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f'select={sel},scale=540:960','-fps_mode','passthrough',str(d/f'{label}-%02d.png')],check=True)
checks=[]
for i,n in enumerate(frames):
 a=np.asarray(Image.open(d/f'v05-{i+1:02}.png').convert('RGB'),dtype=float);b=np.asarray(Image.open(d/f'v04-{i+1:02}.png').convert('RGB'),dtype=float);diff=float(abs(a-b).mean());inside=480<=n<551
 if not inside:assert diff<4,(n,diff)
 else:assert diff>1,(n,diff)
 checks.append({'outputFrame':n,'time':n/48,'motionExpected':inside,'meanRGBDifferenceVsV04':diff})
def audiohash(f):return subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
a,b=audiohash(out),audiohash(before);assert a==b,(a,b)
q={'format':probe,'V04TimelineAndCaptionsIdentical':True,'audioEncodedHashMatchesV04':True,'audioHash':a,'pixelChecks':checks,'motionWindowFrames':[480,551],'maquinitaUnchanged':True,'sweatshirtGagUnchanged':True,'referenceAndConceptReview':True,'visualReview':'concept states, motion phase sequence and rendered scope samples; not independent full playback/listening','approval':'V05 pending'};(p/'QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2));print(json.dumps(q,indent=2))
