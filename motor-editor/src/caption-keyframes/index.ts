import {sampleReferenceTranslation} from '../../forensics/reference-motion.mjs';
export type ReferenceProfile={sourceFps:{num:number;den:number};sourceHeight:number;fitDomainSourceFrames:number[];decayPerSourceFrame:number;omegaRadiansPerSourceFrame:number;cosCoefficientPx:number;sinCoefficientPx:number};

export const FPS=60000/1001;
export type Motion='direct'|'soft'|'cascade'|'hero'|'snap'|'reveal';
export type Exit='cut'|'fade'|'lift';
export type Cue={id:string;block:string;text:string;start:number;end:number;x:number;y:number;size:number;weight?:number;color?:string;anchor?:'start'|'middle'|'end';motion:Motion;axis?:'x'|'y';direction?:number;duration?:number;travel?:number;strength?:number;out?:Exit;outDuration?:number;highlight?:string;condensed?:boolean;masked?:boolean;outline?:boolean;tracking?:number;contrast?:boolean;revealWidth?:number;strokeWidth?:number};
const clamp=(x:number)=>Math.max(0,Math.min(1,x));
const cubic=(a:number,b:number,t:number)=>3*(1-t)*(1-t)*t*a+3*(1-t)*t*t*b+t*t*t;
/** Monotone time inversion; handles steep ease-out curves without Newton overshoot. */
export function bezier(x:number,x1:number,y1:number,x2:number,y2:number){x=clamp(x);if(x===0||x===1)return x;let lo=0,hi=1;for(let i=0;i<20;i++){const m=(lo+hi)/2;if(cubic(x1,x2,m)<x)lo=m;else hi=m}return cubic(y1,y2,(lo+hi)/2)}
export function hermite(p:number,y0:number,y1:number,m0:number,m1:number){p=clamp(p);return(2*p**3-3*p*p+1)*y0+(p**3-2*p*p+p)*m0+(-2*p**3+3*p*p)*y1+(p**3-p*p)*m1}
export function createCaptionMotion(measuredProfile:ReferenceProfile){
function referenceAt(age:number){return sampleReferenceTranslation(measuredProfile,age/FPS,1920).translationY}
function referenceSlope(age:number){const p=measuredProfile,d=p.decayPerSourceFrame,w=p.omegaRadiansPerSourceFrame,c=p.cosCoefficientPx,s=p.sinCoefficientPx;return Math.exp(-d*age)*((-d*c+w*s)*Math.cos(w*age)+(-d*s-w*c)*Math.sin(w*age))}
/** The V8 fit is used verbatim only on its measured domain. The boundary joins are design. */
function heroOffset(age:number){if(age<0)return 52;if(age<2)return hermite(age/2,52,referenceAt(2),-48,referenceSlope(2)*2);if(age<=60)return referenceAt(age);if(age<66)return hermite((age-60)/6,referenceAt(60),0,referenceSlope(60)*6,0);return 0}
function pose(c:Cue,t:number){
 const a=t-c.start,lifetime=c.end-c.start;if(a<0||a>=lifetime)return {x:c.x,y:c.y,scale:1,alpha:0,reveal:0,phase:'off'};
 let dx=0,dy=0,scale=1,alpha=1,reveal=1;const age=a*FPS;
 if(c.motion==='soft'||c.motion==='cascade'){
  const d=c.duration??(c.motion==='soft'?.12:.24),dist=c.travel??(c.motion==='soft'?24:46);
  const k=c.motion==='soft'?bezier(a/d,.22,.72,.25,1):bezier(a/d,.16,.92,.20,1);
  const move=(c.direction??1)*dist*(1-k);if(c.axis==='x')dx=move;else dy=move;
  alpha=bezier(a/Math.min(.075,d*.45),.18,.65,.3,1);
 }else if(c.motion==='hero'){
  dy=heroOffset(age)*(c.strength??1);alpha=bezier(age/3,.22,.55,.4,1);
 }else if(c.motion==='snap'){
  scale=.95+.05*bezier(a/.105,.12,.72,.2,1);alpha=clamp(age);
 }else if(c.motion==='reveal'){
  reveal=bezier(a/(c.duration??.23),.18,.84,.22,1);alpha=1;
 }
 const out=c.out??'fade',od=Math.min(c.outDuration??.075,lifetime*.22),remaining=c.end-t;
 let phase=a<(c.duration??.24)?'entry':'hold';
 if(out!=='cut'&&remaining<od){const progress=clamp(1-remaining/od);phase='exit';alpha*=1-bezier(progress,.42,0,.75,.5);if(out==='lift')dy-=18*bezier(progress,.42,0,.75,.5)}
 return{x:c.x+dx,y:c.y+dy,scale,alpha,reveal,phase};
}

 return {pose,heroOffset};
}
