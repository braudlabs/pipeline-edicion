import React from 'react';
import {AbsoluteFill,Composition,Img,OffthreadVideo,Sequence,registerRoot,useCurrentFrame,staticFile,interpolate} from 'remotion';
import timeline from './timeline.json';
const Shot:React.FC<{shot:typeof timeline.video[number]}>=({shot})=>{
 const f=useCurrentFrame();
 const durations:Record<string,number>={'09-nosotros-procesos-SIN-AUDIO.mp4':8,'13-en-directo-SIN-VOZ-recomendado.mp4':5,'05-plastica-artificial-HABLA-ELLA.mp4':8,'14-cierre-HABLA-ELLA.mp4':7,'01-hook.mp4':5,'07-hora-punta.mp4':5,'11-brigada.mp4':5,'12-platos-iguales.mp4':5};
 const lastFrame=Math.floor((durations[shot.src]??4)*48)-2;
 const scale=interpolate(f,[0,shot.duration],[shot.scale,shot.scale+shot.push],{extrapolateRight:'clamp'});
 const style:React.CSSProperties={width:'100%',height:'100%',objectFit:'cover',transform:`scale(${scale})`,filter:'contrast(1.035) saturate(0.94)'};
 return f+shot.sourceFrame<lastFrame ? <OffthreadVideo src={staticFile('assets/'+shot.src)} trimBefore={shot.sourceFrame} muted style={style}/> : <Img src={staticFile('assets/'+shot.src.replace('.mp4','-last.jpg'))} style={style}/>;
};
const Base=()=> <AbsoluteFill style={{backgroundColor:'#10100e'}}>{timeline.video.map((shot,i)=><Sequence key={i} from={shot.from} durationInFrames={shot.duration}><Shot shot={shot}/></Sequence>)}</AbsoluteFill>;
registerRoot(()=> <Composition id="Cocina-Montaje" component={Base} width={1080} height={1920} fps={48} durationInFrames={timeline.duration}/>);
