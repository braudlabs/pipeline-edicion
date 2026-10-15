import React from 'react';
import {AbsoluteFill,Composition,OffthreadVideo,Sequence,registerRoot,staticFile} from 'remotion';
import t from './timeline.json';
const Base=()=> <AbsoluteFill style={{backgroundColor:'#273e1b'}}>{t.video.map((s,i)=><Sequence key={i} from={s.from} durationInFrames={s.duration}><OffthreadVideo src={staticFile(s.src)} trimBefore={s.sourceFrame} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/></Sequence>)}</AbsoluteFill>;
registerRoot(()=> <Composition id="AD3-Montaje" component={Base} width={1080} height={1920} fps={48} durationInFrames={t.duration}/>);
