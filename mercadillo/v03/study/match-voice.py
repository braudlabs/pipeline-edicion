from pathlib import Path
import subprocess,numpy as np,json
R=Path(__file__).resolve().parent
orig=R/'narrator-original-16k.wav';aligned=R.parents[1]/'v01/public/assets/narrator.wav'
def read(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-ar','16000','-ac','1','-f','f32le','-']),np.float32).copy()
x=read(orig);y=read(aligned);out=[]
for a,b in [(13.5,14),(44,45),(46.5,47),(56.45,56.9),(57.2,57.7),(59.4,60)]:
 q=y[round(a*16000):round(b*16000)];n=1<<(len(x)+len(q)-1).bit_length();c=np.fft.irfft(np.fft.rfft(x,n)*np.fft.rfft(q[::-1],n),n);z=np.argmax(c[len(q)-1:len(x)])
 corr=np.corrcoef(x[z:z+len(q)],q)[0,1];out.append(dict(timeline=a,source=round(z/16000,6),offset=round(z/16000-a,6),corr=float(corr)))
print(out);(R/'voice-source-matches.json').write_text(json.dumps(out,indent=2))
