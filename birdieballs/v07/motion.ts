export {FPS,bezier,hermite} from '../../motor-editor/src/caption-keyframes/index.ts';
export type {Cue,Motion,Exit} from '../../motor-editor/src/caption-keyframes/index.ts';
import {createCaptionMotion} from '../../motor-editor/src/caption-keyframes/index.ts';
import {measuredProfile} from './reference-profile.ts';
export const {pose,heroOffset}=createCaptionMotion(measuredProfile);
