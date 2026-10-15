from pathlib import Path
import json,re,numpy as np,subprocess,wave
R=Path(__file__).resolve().parents[1]
log=(R/'analysis/voice-silence.log').read_text();starts=[float(x) for x in re.findall(r'silence_start: ([\d.]+)',log)];ends=[float(x) for x in re.findall(r'silence_end: ([\d.]+)',log)]
# Trim the middle only; preserve at least 95 ms after the previous sound and 65 ms before the next.
cuts=[]
for a,b in zip(starts,ends):
 if b-a>.27:cuts.append([a+.095,b-.065])
def T(t):return t-sum(max(0,min(t,b)-a) for a,b in cuts if t>a)
D=round(T(69)*30)/30
(R/'src/retime.json').write_text(json.dumps({'cuts':cuts,'saved':sum(b-a for a,b in cuts),'duration':D},indent=2))
if __name__=='__main__':
 raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(R/'assets/locucion.mp3'),'-f','f32le','-ac','2','-ar','48000','-']);s=np.frombuffer(raw,np.float32).reshape(-1,2);chunks=[];last=0
 for a,b in cuts:
  chunks.append(s[last:round(a*48000)].copy());last=round(b*48000)
 chunks.append(s[last:].copy());v=np.concatenate(chunks)
 # Sub-millisecond fades only at the inaudible join; no voice timestretch.
 for a,b in cuts:
  j=round(T(a)*48000);k=24
  v[j-k:j]*=np.linspace(1,0,k)[:,None];v[j:j+k]*=np.linspace(0,1,k)[:,None]
 out=np.zeros((round(D*48000),2),np.float32);out[:min(len(v),len(out))]=v[:len(out)]
 with wave.open(str(R/'assets/Voz-V2.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(48000);w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes())
 print('Pausas recortadas:',len(cuts),'Ahorro:',sum(b-a for a,b in cuts),'Duración:',D)
