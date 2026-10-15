import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {EditComposition} from './Composition.tsx';
import defaultPlan from '../examples/plan.json';
import type {Plan} from './types.ts';
const Root=()=> <Composition id="ReferenceEdit" component={EditComposition} defaultProps={{plan:defaultPlan as Plan}} durationInFrames={defaultPlan.durationInFrames} width={defaultPlan.width} height={defaultPlan.height} fps={defaultPlan.fps.num/defaultPlan.fps.den} calculateMetadata={({props})=>({durationInFrames:props.plan.durationInFrames,width:props.plan.width,height:props.plan.height,fps:props.plan.fps.num/props.plan.fps.den})}/>;
registerRoot(Root);
