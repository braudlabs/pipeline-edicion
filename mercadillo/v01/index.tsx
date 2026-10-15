import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film,Concept,FRAMES,FPS} from './Film';
function Root(){return <><Composition id="MercadilloV01" component={Film} width={1080} height={1920} durationInFrames={FRAMES} fps={FPS} defaultProps={{sound:true,blur:.4}}/>{['A','B','C'].map(variant=><Composition key={variant} id={'Concept'+variant} component={Concept} width={1080} height={1920} durationInFrames={1} fps={FPS} defaultProps={{variant}}/>)}</>}
registerRoot(Root);
