from pathlib import Path
import subprocess,json
p=Path(__file__).resolve().parent
source='/Users/alejandrorubiocamarero/Downloads/Birdieballs v1 (Sin Postpro).mp4'
lib=p.parents[1]/'ad3-pipeline/assets'
events=[('whoosh-short.mp3',2.19,.075,'entrada de riñón'),('pop.mp3',2.68,.04,'remate en bolas'),('click-soft.mp3',4.83,.026,'segunda insistencia'),('pop.mp3',5.0,.045,'tercera insistencia'),('impact-bass-1.mp3',6.22,.06,'NO sobre impacto original'),('whoosh-short.mp3',9.25,.075,'solución en profundidad'),('click-soft.mp3',10.74,.036,'literalmente'),('whoosh-short.mp3',13.08,.05,'originales'),('click-soft.mp3',14.30,.04,'favoritas'),('whoosh-short.mp3',20.81,.035,'barrido de revisión'),('click-soft.mp3',21.4,.025,'una'),('click-soft.mp3',22.06,.035,'una revisada'),('pop.mp3',25.16,.044,'nuevas'),('click-soft.mp3',30.16,.025,'más baratas'),('whoosh-short.mp3',32.16,.045,'tuyas'),('click-soft.mp3',36.88,.026,'por menos')]
args=['ffmpeg','-v','error','-i',source]
for f,_,_,_ in events:args+=['-i',str(lib/f)]
flt=['[0:a]atrim=end=38.004633,asetpts=PTS-STARTPTS,aresample=48000,volume=0.90[voice_music]']
for i,(f,t,g,why) in enumerate(events,1):flt.append(f'[{i}:a]aresample=48000,volume={g},adelay={round(t*48000)}S:all=1[s{i}]')
flt+=['[voice_music]'+''.join(f'[s{i}]' for i in range(1,len(events)+1))+f'amix=inputs={len(events)+1}:duration=first:normalize=0,alimiter=limit=0.94:level=false:latency=true,afade=t=out:st=37.91:d=0.094633,apad=whole_dur=38.004633,atrim=end=38.004633,volume=-1dB[out]']
args+=['-filter_complex',';'.join(flt),'-map','[out]','-ar','48000','-ac','2','-c:a','pcm_s24le','-y',str(p/'assets/mix.wav')]
subprocess.run(args,check=True)
(p/'study/sound-events.json').write_text(json.dumps([dict(file=f,time=t,gain=g,purpose=w) for f,t,g,w in events],ensure_ascii=False,indent=2))
