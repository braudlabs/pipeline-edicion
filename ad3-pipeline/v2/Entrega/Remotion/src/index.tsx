import React from 'react';
import {AbsoluteFill,Composition,OffthreadVideo,Sequence,registerRoot,staticFile} from 'remotion';
import timeline from './timeline.json';
const Base=()=> <AbsoluteFill style={{backgroundColor:'#20211f'}}>{timeline.video.map((shot,i)=><Sequence key={i} from={shot.from} durationInFrames={shot.duration}><OffthreadVideo src={staticFile('assets/'+shot.src)} trimBefore={shot.sourceFrame} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/></Sequence>)}</AbsoluteFill>;
registerRoot(()=> <Composition id="AD3-Montaje" component={Base} width={1080} height={1920} fps={48} durationInFrames={timeline.duration}/>);
