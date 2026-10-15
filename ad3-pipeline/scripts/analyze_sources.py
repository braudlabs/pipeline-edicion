from pathlib import Path
import json,subprocess,shutil
R=Path(__file__).resolve().parents[1];P=Path((R/'source-path.txt').read_text());A=R/'analysis'
for p in sorted((P/'entrega').glob('*.mp4')):
 shutil.copy2(p,R/'remotion/public/assets'/p.name)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p),'-vn','-ar','16000','-ac','1',str(A/(p.stem+'.wav'))],check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-ss','1.4','-i',str(p),'-frames:v','1','-q:v','2',str(R/'assets'/(p.stem+'.jpg'))],check=True)
import whisper
model=whisper.load_model('small')
all=[]
for p in sorted((A).glob('*.wav')):
 result=model.transcribe(str(p),language='es',word_timestamps=True,fp16=False,verbose=False,condition_on_previous_text=False)
 (A/(p.stem+'-words.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2));all.append({'file':p.name,'text':result['text'],'words':[w for s in result['segments'] for w in s.get('words',[])]});print(p.name,result['text'],flush=True)
(A/'transcripts.json').write_text(json.dumps(all,ensure_ascii=False,indent=2))
