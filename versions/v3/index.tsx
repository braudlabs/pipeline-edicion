import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Ad} from './video';
import timing from './timing-v3.json';
const Root=()=> <Composition id="VisualHubAd2" component={Ad} width={1080} height={1920} fps={24} durationInFrames={timing.duration}/>;
registerRoot(Root);
