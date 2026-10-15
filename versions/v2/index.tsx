import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Ad} from './video';
const Root=()=> <Composition id="VisualHubAd2" component={Ad} width={1080} height={1920} fps={24} durationInFrames={1765}/>;
registerRoot(Root);
