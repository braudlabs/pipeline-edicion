import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film,ReferenceTest,FPS,FRAMES} from './Film';
registerRoot(()=> <><Composition id="BirdieV04" component={Film} defaultProps={{concept:'C',sound:true}} width={1080} height={1920} fps={FPS} durationInFrames={FRAMES}/><Composition id="ReferenceRise" component={ReferenceTest} width={1080} height={1920} fps={FPS} durationInFrames={120}/></>);
