import {bezier,hermite} from '../../motor-editor/src/caption-keyframes/index';
export type Caption={id:string;text:string;start:number;end:number;x:number;y:number;size:number;color:string;weight:number;motion:string;masked?:boolean;group?:string;out?:string;role?:string};
const clamp=(n:number)=>Math.min(1,Math.max(0,n));
const ease=(n:number)=>bezier(n,.17,.85,.22,1);
/** Authored motion by role, inspired by inspected V5 entries; no claim of recovered keys. */
export function pose(c:Caption,t:number){
 const age=t-c.start,remaining=c.end-t;if(age<0||remaining<=0)return{alpha:0,x:c.x,y:c.y,scale:1,rotate:0};
 let x=c.x,y=c.y,scale=1,rotate=0,alpha=1;
 if(c.motion==='settle'){
   // Fast arrival, restrained 8px overshoot, critically damped reading hold.
   const a=age/.11;
   const dy=age<.11?32-40*ease(a):age<.27?hermite((age-.11)/.16,-8,0,0,0):0;
   y+=dy;alpha=ease(age/.095);
 }else if(c.motion==='soft'){y+=20*(1-ease(age/.13));alpha=ease(age/.085)}
 else if(c.motion==='sweep'){x-=70*(1-ease(age/.19));alpha=ease(age/.065)}
 else if(c.motion==='drop'){y-=80*(1-ease(age/.20));alpha=ease(age/.06)}
 else if(c.motion==='snap'){scale=.94+.06*ease(age/.12);alpha=clamp(age/.045)}
 else if(c.motion==='punch'){
   scale=age<.075?.84+.19*ease(age/.075):age<.19?1.03-.03*ease((age-.075)/.115):1;
   alpha=clamp(age/.035);
 }
 if(c.role!=='rail'&&remaining<.075){const k=clamp(1-remaining/.075);alpha*=1-bezier(k,.4,0,.8,.5);if(c.out!=='fade')y-=10*k*k}
 return {alpha,x,y,scale,rotate};
}
export function envelope(t:number,points:number[][]){
 if(t<=points[0][0])return points[0][1];
 for(let i=1;i<points.length;i++){const[a,v]=points[i-1],[b,w]=points[i];if(t<=b)return v+(w-v)*clamp((t-a)/(b-a))}
 return points.at(-1)![1];
}
