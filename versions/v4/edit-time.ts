import {useCurrentFrame,useVideoConfig} from 'remotion';
/** The edit decisions stay in their original 24 fps timebase; animation renders at 48 fps. */
export const useEditFrame=()=>useCurrentFrame()*24/useVideoConfig().fps;
export const OUTPUT_FPS=48;
export const FRAME_RATIO=OUTPUT_FPS/24;
