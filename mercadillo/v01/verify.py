from pathlib import Path
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).parent
video=p/'Mercadillo-agencias-V01.mp4'
inputs=json.loads((p/'inputs.json').read_text());cues=json.loads((p/'cues.json').read_text())
def sha(file):
    with file.open('rb') as handle:return hashlib.file_digest(handle,'sha256').hexdigest()
def probe(file):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(file)]))
data=probe(video);v=next(s for s in data['streams'] if s['codec_type']=='video');a=next(s for s in data['streams'] if s['codec_type']=='audio')
assert int(v['nb_frames'])==2121 and v['r_frame_rate']=='24/1' and (v['width'],v['height'])==(1080,1920)
assert abs(float(v['duration'])-88.375)<1/24000
cursor=0;sources=[]
for c in inputs['clips']:
    assert c['timeline_in_frame']==cursor;cursor+=c['duracion_frames'];assert c['timeline_out_exclusive_frame']==cursor
    file=p/'public/assets'/Path(c['archivo']).name;original=Path(inputs['root'])/c['archivo']
    h=sha(file);assert h==sha(original)
    sources.append({'id':c['numero'],'sha256':h,'frames':c['duracion_frames'],'startFrame':c['timeline_in_frame']})
assert cursor==2121
assert sum(c['numero']==15 for c in inputs['clips'])==1
maskFrames=set(json.loads((p/'study/mask-frames.json').read_text()));missingMasks=[]
for c in cues:
    assert c['end']>c['start']>=0 and c['end']<=88.375
    if c.get('masked'):
        for frame in range(int(np.ceil(c['start']*24)),int(np.ceil(c['end']*24))):
            if frame not in maskFrames or not (p/f'public/assets/masks/{frame:04d}.png').exists():missingMasks.append(frame)
assert not missingMasks
subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
def pcm(file):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-vn','-ar','8000','-ac','1','-f','f32le','-']),dtype=np.float32)
x=pcm(p/'public/assets/dialogue-foley.wav');y=pcm(video);sync=[]
for lo,hi in [(1,3),(8,10),(15,17),(28,31),(48.3,51),(57,60),(69,71.5),(83,86)]:
    left=x[int(lo*8000):int(hi*8000)];right=y[int(lo*8000):int(hi*8000)];left=left-left.mean();right=right-right.mean()
    n=1<<(len(left)*2-1).bit_length();corr=np.fft.irfft(np.fft.rfft(right,n)*np.conj(np.fft.rfft(left,n)),n);lags=np.arange(-80,81);lag=int(lags[np.argmax(corr[lags%n])]);assert abs(lag)<=8
    sync.append({'rangeSeconds':[lo,hi],'lagMs':lag/8,'correlation':float(np.corrcoef(left,right)[0,1])})
meter=subprocess.run(['ffmpeg','-hide_banner','-i',str(video),'-af','loudnorm=print_format=json','-f','null','-'],capture_output=True,text=True,check=True).stderr
(p/'study/final-meter.log').write_text(meter)
start=meter.rfind('{');end=meter.find('}',start)+1;levels=json.loads(meter[start:end]);assert float(levels['input_tp'])<=-.1
info={'status':'technical_checks_passed_pending_user_verdict','output':str(video.resolve()),'sha256':sha(video),'video':{k:v.get(k) for k in ['codec_name','width','height','nb_frames','r_frame_rate','duration','pix_fmt']},'audio':{k:a.get(k) for k in ['codec_name','sample_rate','channels','duration']},'loudness':{k:levels[k] for k in ['input_i','input_tp','input_lra']},'sources':sources,'sourceCutsPreserved':True,'clip15Occurrences':1,'dialogueAndFoleyRetained':True,'audioSync':sync,'decodeWithoutErrors':True,'captionElements':len(cues),'maskedFramesAvailable':True,'independentAudioListening':False,'music':'Funky Martian / Michael Ramir C. / Mixkit 1029','musicVolumeAutomation':'Film.tsx musicPoints','visualReview':{'designAlternatives':['A','B','C'],'hookMaskRejectedForLegibility':True,'sampledSourceFrames':60,'compositionStills':44,'prototypeSequence':'stills/prototype-motion.jpg','finalNativeContacts':'pending','normalSpeedPlayback':'pending'},'limitations':['Local ASR timings with documented editorial repairs, not manual phonetic alignment','Automatic person segmentation','Source clip20 contains cropped head during action as noted in provided brief; retained as action shot','No independent auditory review of music or final mix']}
(p/'QA.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:info[k] for k in ['status','sha256','video','loudness','audioSync']},indent=2))
