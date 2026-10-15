from pathlib import Path
import subprocess,json
import numpy as np
from PIL import Image
p=Path(__file__).resolve().parent.parent
T=json.loads((p/'timeline.json').read_text());out=p/'Andromeda-00-38s-V01-PREVIEW.mp4'
qa=json.loads((p/'QA.json').read_text());d=p/'study/decoded';d.mkdir(exist_ok=True)
frames=[f for s in T['scenes'] for f in [s['record_in_frame'],s['record_out_frame']-1]]
sel='+'.join('eq(n\\,%d)'%f for f in frames)
subprocess.run(['ffmpeg','-v','error','-y','-i',str(out),'-vf','select='+sel+',scale=540:960','-fps_mode','passthrough',str(d/'out-%02d.png')],check=True)
errors=[]
for i,s in enumerate(T['scenes']):
 sel='+'.join('eq(n\\,%d)'%f for f in [s['source_in_frame'],s['source_out_frame']-1])
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(p/'public'/s['asset']),'-vf','select='+sel+',scale=540:960','-fps_mode','passthrough',str(d/f'source-{i}-%02d.png')],check=True)
 for j in range(2):
  a=np.asarray(Image.open(d/f'out-{i*2+j+1:02d}.png').convert('RGB'),dtype=np.float32)[660:920]
  b=np.asarray(Image.open(d/f'source-{i}-{j+1:02d}.png').convert('RGB'),dtype=np.float32)[660:920]
  errors.append({'scene':s['id'],'outputFrame':frames[i*2+j],'sourceFrame':s['source_in_frame'] if j==0 else s['source_out_frame']-1,'meanAbsoluteRGBDifference':float(np.abs(a-b).mean())})
assert max(e['meanAbsoluteRGBDifference'] for e in errors)<8,errors
qa['cutPixelChecks']={'region':'bottom y1320–1840 of source1080x1920, clear of captions; images downscaled to540 for comparison','samples':errors,'note':'compression/resampling prevent pixel equality; every supplied cut start/end compared to exact source index'}
def pcm(file):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-ar','48000','-ac','1','-f','f32le','-']),np.float32).copy()
a=pcm(out);b=pcm(p/'public/assets/mix-preview.wav');results=[]
for t in [0,2,10,23,30,36]:
 begin=round(t*48000);x=a[begin:begin+48000].astype(np.float64);y=b[begin:begin+48000].astype(np.float64)
 x-=x.mean();y-=y.mean();n=1<<(len(x)*2-1).bit_length();cc=np.fft.irfft(np.fft.rfft(x,n)*np.conj(np.fft.rfft(y,n)),n)
 lags=list(range(-96,97));lag=max(lags,key=lambda lag:cc[lag%n]);corr=float(np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y)))
 results.append({'start':t,'lagSamples':lag,'lagMs':lag/48,'zeroLagCorrelation':corr})
assert all(abs(r['lagSamples'])<=1 and r['zeroLagCorrelation']>.98 for r in results),results
qa['audioRenderCheck']={'reference':'mix-preview.wav derived from delivered stems','sampleRate':48000,'renderSamples':len(a),'referenceSamples':len(b),'peakAbsoluteRendered':float(abs(a).max()),'windows':results,'scope':'checks output mux/codec timing; not phonetic/lip-sync verification or listening'}
qa['visualReview']={'selectedFrames':[19,31,60,86,119,185,211,251,270,307,338,406,468,542,596,638,677,715,767,828,862,886,913],'guide':'stills/review-meta-board.jpg','corrections':['Subtitles raised per Ale feedback','Paper/ticket and sweatshirt gags left clear','Machine text moved above screen after pixel inspection'],'fullPlaybackOrListening':False}
(p/'QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'maxCutDifference':max(e['meanAbsoluteRGBDifference'] for e in errors),'audioWindows':results},indent=2))
