import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Ad} from './video';
import timing from './timing-v3.json';
import {OUTPUT_FPS,FRAME_RATIO} from './edit-time';
const Root=()=> <Composition id="VisualHubAd2" component={Ad} width={1080} height={1920} fps={OUTPUT_FPS} durationInFrames={timing.duration*FRAME_RATIO}/>;
registerRoot(Root);
