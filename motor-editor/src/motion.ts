import type {Motion,Track} from './types.ts';
export const clamp=(v:number,a=0,b=1)=>Math.max(a,Math.min(b,v));
export function ease(t:number,kind='linear'):number {
  t=clamp(t);
  if(kind==='hold')return t===1?1:0;
  if(kind==='out')return 1-Math.pow(1-t,4);
  if(kind==='inOut')return t<.5?8*t*t*t*t:1-Math.pow(-2*t+2,4)/2;
  // Position fit from landing Gracias, f9–55. Normalize only within measured domain.
  if(kind==='measuredRise')return (1-Math.exp(-.0859*46*t))/(1-Math.exp(-.0859*46));
  return t;
}
export function sample(track:Track|undefined,frame:number,fallback=0):number {
  if(!track?.length)return fallback;
  if(frame<=track[0].f)return track[0].v;
  for(let i=1;i<track.length;i++)if(frame<track[i].f){const a=track[i-1],b=track[i];return a.v+(b.v-a.v)*ease((frame-a.f)/(b.f-a.f),a.ease);}
  return track.at(-1)!.v;
}
export function state(m:Motion|undefined,f:number){return {x:sample(m?.x,f),y:sample(m?.y,f),scale:sample(m?.scale,f,1),rotate:sample(m?.rotate,f),rotateY:sample(m?.rotateY,f),opacity:clamp(sample(m?.opacity,f,1)),blur:Math.max(0,sample(m?.blur,f))};}
export function rise(at:number,duration:number,distance:number):Motion{return {y:[{f:at,v:distance,ease:'measuredRise'},{f:at+duration,v:0}],opacity:[{f:at,v:0},{f:at+Math.min(duration,6),v:1}]};}
export function pulse(at:number,fps:number):Motion{
  const values=[1,.5,0,.5,1,.5,0,.5,1];
  // Measured at60fps; preserve time when compiling to another cadence.
  const keys=new Map<number,number>();values.forEach((v,i)=>keys.set(at+Math.round(i*fps/60),v));
  return {opacity:[...keys].map(([f,v])=>({f,v,ease:'hold'}))};
}
export function countAt(target:number,elapsed:number,duration:number):number{
  // V1 f389–398 observed trajectory. Discrete digits, no interpolated glyph blur.
  const values=[1,6,15,21,24,26,28,29,29,30];
  if(elapsed<0)return 0;
  const i=Math.min(9,Math.floor(clamp(elapsed/Math.max(1,duration))*9));
  return Math.round(target*values[i]/30);
}
export const fpsValue=(f:{num:number;den:number})=>f.num/f.den;
export const frameAt=(seconds:number,fps:{num:number;den:number})=>Math.round(seconds*fpsValue(fps));
export function shutterSamples(frame:number,start:number,end:number,samples=8,angle=240){
 const count=Math.max(2,Math.min(12,Math.round(samples))),exposure=clamp(angle,0,360)/360;
 return Array.from({length:count},(_,i)=>({frame:clamp(frame+((i+.5)/count-.5)*exposure,start,end-1),weight:1/count}));
}
