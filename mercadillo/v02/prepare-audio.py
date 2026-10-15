from pathlib import Path
import re,ast,json,subprocess,wave,numpy as np
R=Path(__file__).resolve().parent; old=R.parent/'v01';rate=48000;N=2121*2000
spec=json.load(open(R/'spec.json'))['cues']
def decode(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','f32le','-ar',str(rate),'-ac','2','-']),np.float32).reshape(-1,2).copy()
base=decode(old/'public/assets/dialogue-foley.wav');music=decode(old/'public/assets/music.wav')[rate*2:rate*2+N]
source=(old/'Film.tsx').read_text();pts=ast.literal_eval(re.search(r'export const musicPoints=(\[.*?\]);',source).group(1));t=np.arange(N)/rate;env=np.interp(t,[p[0] for p in pts],[p[1] for p in pts]);mix=base+music*env[:,None]
hits=[]
for group,name,gain in [('hook','air',.19),('tradeoff','tap',.2),('solution','resolve',.2),('premium','air',.18),('machine','tap',.19),('ten','tap',.2),('boom','resolve',.31),('chatgpt','tap',.2),('ya','tap',.22),('criterion','air',.2),('cause','tap',.21),('art','resolve',.27),('call','air',.18)]:
 cs=[c for c in spec if c['group']==group and c['motion']!='cut'];c=max(cs,key=lambda c:c['size']);at=c['start']+1/24
 a=decode(old/f'public/assets/{name}.wav')*gain;i=round(at*rate);z=min(len(a),N-i);mix[i:i+z]+=a[:z];hits.append({'time':at,'kind':name,'gain':gain,'cue':c['id']})
peak=float(abs(mix).max());gain=min(1,.86/peak);mix*=gain
with wave.open(str(R/'mix.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
(R/'audio.json').write_text(json.dumps({'source':str(old/'public/assets/dialogue-foley.wav'),'sourceTimingChanged':False,'music':'Funky Martian, Michael Ramir C., Mixkit 1029','musicStartSeconds':2,'musicPoints':pts,'hits':hits,'mixGain':gain,'peakBeforeGain':peak,'independentListening':False},indent=2))
print('Audio prepared',N/rate,peak,gain)
