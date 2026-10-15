/** Headless, continuous-time trajectory. No React, AE, output-fps or 1920px dependency.
 * This is a position primitive, not an automatic editorial decision or recovered easing. */
import type {ReferenceProfile} from './index.ts';

export type ReferenceEntrance = {
  start: number; end: number;
  /** Reviewed subset of the source fit, in source frame ages (inclusive endpoints). */
  sourceRange: [number, number];
  /** Authored arrival, expressed as fractions of output height, and height/second. */
  initialOffset: number; initialVelocity: number;
  settleSeconds: number;
  exit: {kind: 'cut'} | {kind: 'lift'; seconds: number; travel: number};
};
const positive=(n:number)=>Number.isFinite(n)&&n>0;
function bridge(p:number,y0:number,y1:number,v0:number,v1:number,seconds:number){
  const m0=v0*seconds,m1=v1*seconds;
  return {
    y:(2*p**3-3*p*p+1)*y0+(p**3-2*p*p+p)*m0+(-2*p**3+3*p*p)*y1+(p**3-p*p)*m1,
    velocity:((6*p*p-6*p)*y0+(3*p*p-4*p+1)*m0+(-6*p*p+6*p)*y1+(3*p*p-2*p)*m1)/seconds,
  };
}
export function createReferenceEntrance(profile:ReferenceProfile,spec:ReferenceEntrance){
  if(!positive(profile.sourceFps.num)||!positive(profile.sourceFps.den)||!positive(profile.sourceHeight))throw Error('Invalid source coordinate system');
  const fps=profile.sourceFps.num/profile.sourceFps.den;
  const [lo,hi]=spec.sourceRange,[a,b]=profile.fitDomainSourceFrames;
  if(![lo,hi,a,b,profile.decayPerSourceFrame,profile.omegaRadiansPerSourceFrame,profile.cosCoefficientPx,profile.sinCoefficientPx,spec.start,spec.end,spec.initialOffset,spec.initialVelocity].every(Number.isFinite)||lo<=0||hi<=lo||lo<a||hi>b)throw Error('Invalid or unsupported source fit range');
  if(!positive(spec.settleSeconds)||spec.end<=spec.start)throw Error('Invalid phase duration');
  if(!['cut','lift'].includes(spec.exit.kind))throw Error('Unsupported exit');
  if(spec.exit.kind==='lift'&&(!positive(spec.exit.seconds)||!Number.isFinite(spec.exit.travel)))throw Error('Invalid exit');
  const fitStart=lo/fps,fitEnd=hi/fps,settleEnd=fitEnd+spec.settleSeconds;
  const exitStart=spec.end-spec.start-(spec.exit.kind==='lift'?spec.exit.seconds:0);
  if(settleEnd>exitStart+1e-10)throw Error('Entry and exit overlap: choose a reviewed shorter source range or another motion; never silently retime the fit');
  const fitted=(age:number)=>{
    const d=profile.decayPerSourceFrame,w=profile.omegaRadiansPerSourceFrame,c=profile.cosCoefficientPx,s=profile.sinCoefficientPx;
    const e=Math.exp(-d*age),cos=Math.cos(w*age),sin=Math.sin(w*age);
    return {y:e*(c*cos+s*sin)/profile.sourceHeight,velocity:fps*e*((-d*c+w*s)*cos+(-d*s-w*c)*sin)/profile.sourceHeight};
  };
  const first=fitted(lo),last=fitted(hi);
  function atSeconds(t:number,height:number){
    if(!Number.isFinite(t)||!positive(height))throw Error('Invalid output sample');
    const age=t-spec.start;
    let y=0,velocity=0,opacity=1;
    let phase:'off'|'arrival'|'reference-fit'|'settle'|'hold'|'exit'='hold';
    let provenance:'visibility'|'authored'|'fitted_position_only'='authored';
    if(age<0||t>=spec.end){phase='off';opacity=0;provenance='visibility';}
    else if(age<fitStart){
      phase='arrival';({y,velocity}=bridge(age/fitStart,spec.initialOffset,first.y,spec.initialVelocity,first.velocity,fitStart));
      opacity=age/fitStart;
    }else if(age<=fitEnd){phase='reference-fit';provenance='fitted_position_only';({y,velocity}=fitted(age*fps));}
    else if(age<settleEnd){phase='settle';({y,velocity}=bridge((age-fitEnd)/spec.settleSeconds,last.y,0,last.velocity,0,spec.settleSeconds));}
    else if(spec.exit.kind==='lift'&&age>=exitStart){
      phase='exit';const p=(age-exitStart)/spec.exit.seconds;
      // Authored accelerating exit; deliberately distinct from the measured entrance.
      y=-spec.exit.travel*p*p;velocity=-2*spec.exit.travel*p/spec.exit.seconds;opacity=1-p*p;
    }
    return {translationY:y*height,velocityPxPerSecond:velocity*height,opacity,phase,positionProvenance:provenance,opacityProvenance:'authored' as const};
  }
  function atFrame(frame:number,outputFps:{num:number;den:number},height:number){
    if(!positive(outputFps.num)||!positive(outputFps.den))throw Error('Invalid output fps');
    // Fractional frames are intentional: shutter sampling must not quantize time.
    return atSeconds(frame*outputFps.den/outputFps.num,height);
  }
  return {atSeconds,atFrame,boundaries:{fitStart:spec.start+fitStart,fitEnd:spec.start+fitEnd,settleEnd:spec.start+settleEnd,exitStart:spec.start+exitStart}};
}
