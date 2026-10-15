from pathlib import Path
import subprocess
p=Path(__file__).parent
f=p/'Film.tsx';s=f.read_text();s=s.replace('\n];',""",
 {id:'pues-si',text:'Pues sí que están',start:25.68,end:26.16,x:540,y:1390,size:105,entry:'snap',exit:.02},
 {id:'como-nuevas-dialogo',text:'como nuevas,',start:26.16,end:27.04,x:540,y:1390,size:144,weight:700,entry:'left',exit:.05},
 {id:'si-remate',text:'sí.',start:26.88,end:27.04,x:765,y:1520,size:90,entry:'snap',exit:.05},
 {id:'tu-lo-has-dicho',text:'Tú lo has dicho.',start:27.34,end:28.06,x:540,y:1450,size:123,entry:'up',exit:.06},
 {id:'como-nuevas-oferta',text:'Como nuevas',start:28.20,end:28.80,x:540,y:330,size:117,weight:700,entry:'left',exit:.02},
 {id:'hasta-un',text:'y hasta un',start:28.80,end:30.16,x:540,y:330,size:114,entry:'right',exit:.035},
 {id:'mas-baratas',text:'más baratas.',start:30.16,end:30.99,x:540,y:1680,size:131,weight:700,entry:'up',exit:.07},
 {id:'no-esperes',text:'No esperes más',start:31.16,end:31.86,x:540,y:1460,size:118,entry:'left',exit:.02},
 {id:'y-pide',text:'y pide',start:31.86,end:32.72,x:540,y:1315,size:93,entry:'up',exit:.06},
 {id:'las-tuyas',text:'las tuyas.',start:32.22,end:32.72,x:540,y:1485,size:173,weight:700,color:accent,entry:'right',exit:.06},
 {id:'que-el-golf',text:'Que el golf',start:32.92,end:33.44,x:750,y:1250,size:103,entry:'left',exit:.02},
 {id:'esta-para',text:'está para',start:33.44,end:34.53,x:520,y:1300,size:94,entry:'up',exit:.04},
 {id:'disfrutarlo',text:'disfrutarlo,',start:33.90,end:34.53,x:520,y:1475,size:172,weight:700,color:accent,entry:'left',exit:.04},
 {id:'chaval',text:'chaval.',start:34.62,end:35.08,x:730,y:1435,size:131,weight:700,entry:'snap',exit:.08},
 {id:'birdie-end',text:'Birdieballs.',start:35.52,end:36.06,x:540,y:1300,size:140,weight:700,entry:'up',exit:.06},
 {id:'juega-mas',text:'Juega más,',start:36.12,end:37.95,x:540,y:1010,size:145,entry:'left',exit:.10},
 {id:'por-menos',text:'por menos.',start:36.88,end:37.95,x:540,y:1190,size:173,weight:700,color:accent,entry:'up',exit:.10}
];""",1);f.write_text(s)
r=p/'render.mjs';s=r.read_text();a=s.index('  const list=');b=s.index('\n  for(const [name,t]',a)
s=s[:a]+"  const list=[['lagos-water',15.5],['lagos-sand',15.8],['campos',16.25],['product',13.23],['clean',20.3],['inspect',21.18],['one-by-one',22.21],['mindunguis',23.8],['nuevas',25.4],['dialogue',26.5],['discount',29.75],['cheaper',30.65],['cta',32.48],['enjoy',34.25],['brand-end',35.82],['tagline',37.4]];"+s[b:];r.write_text(s)
# One continuous source mix; pre-existing music and dialogue retained.
source='/Users/alejandrorubiocamarero/Downloads/Birdieballs v1 (Sin Postpro).mp4'
sfx=[('whoosh-short.mp3',2.220,.055),('impact-bass-1.mp3',6.200,.035),('whoosh-short.mp3',9.290,.055),('click-soft.mp3',13.140,.04),('click-soft.mp3',21.400,.026),('click-soft.mp3',22.060,.030)]
args=['ffmpeg','-v','error','-i',source]
for name,_,_ in sfx:args+=['-i',str(p.parent/'v04/assets'/name)]
filters=['[0:a]atrim=0:38.004633,asetpts=PTS-STARTPTS,volume=0.90[base]']
for i,(_,t,gain) in enumerate(sfx,1): filters.append(f'[{i}:a]volume={gain},adelay={int(t*1000)}:all=1[s{i}]')
filters.append('[base]'+''.join(f'[s{i}]' for i in range(1,len(sfx)+1))+f'amix=inputs={len(sfx)+1}:duration=first:normalize=0,alimiter=limit=0.95:level=false:latency=true,afade=t=out:st=37.90:d=0.104633[out]')
args+=['-filter_complex',';'.join(filters),'-map','[out]','-ar','48000','-ac','2','-c:a','pcm_s24le','-y',str(p/'public/assets/mix.wav')]
subprocess.run(args,check=True)
