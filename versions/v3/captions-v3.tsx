import React from 'react';
import {interpolate,Easing,useCurrentFrame} from 'remotion';
import captions from './captions-v3.json';
import timing from './timing-v3.json';
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const ease=Easing.bezier(.16,1,.3,1);
const ramp=(f:number,d:number)=>interpolate(f,[0,d],[0,1],{...clamp,easing:ease});
const inEvent=(f:number,k:keyof typeof timing.events)=>f>=timing.events[k].from&&f<timing.events[k].to;
/** Reference: small words settle in 2–3 frames. Large keywords rise in 5–6.
 * Every word moves on Y only: no rotation, X motion, squash, or diagonal path.
 * All critical text sits above y=1230 for Meta Reels placements. */
export const KineticCaptions=()=>{
 const f=useCurrentFrame();const c=captions.find(c=>f>=c.from&&f<c.to);
 if(!c||inEvent(f,'brand')||inEvent(f,'price'))return null;
 const board=inEvent(f,'accounts');const cost=inEvent(f,'cost');
 const prefix=c.emphasis&&!board?c.words.slice(0,-1):c.words;
 const last=c.words[c.words.length-1];const emphasis=c.emphasis&&!board;
 const word=(w:typeof last,i:number)=><span key={i} style={{display:'inline-block',marginRight:i===prefix.length-1?0:'.2em',opacity:interpolate(f-w.from,[0,2],[.45,1],clamp),visibility:f<w.from?'hidden':'visible',transform:`translateY(${14*(1-ramp(f-w.from,3))}px)`}}>{w.text}</span>;
 return <div style={{position:'absolute',left:90,right:100,top:board?1120:emphasis?1040:1120,color:board?'#26381e':'#fffef6',height:emphasis?200:110,overflow:'hidden',textAlign:'center',fontFamily:'Display',fontWeight:700,lineHeight:1,letterSpacing:'-.04em',textShadow:board?'0 2px 12px #faf7ee':cost?'0 2px 10px #10250944':'0 3px 16px #0007'}}>
  <div style={{fontSize:board?Math.min(c.fontSize,62):c.fontSize,whiteSpace:'nowrap',minHeight:emphasis&&prefix.length?68:0}}>{prefix.map(word)}</div>
  {emphasis&&<div style={{fontSize:Math.min(c.keywordSize,132),whiteSpace:'nowrap',opacity:interpolate(f-last.from,[0,3],[.38,1],clamp),visibility:f<last.from?'hidden':'visible',transform:`translateY(${66*(1-ramp(f-last.from,6))}px)`}}>{last.text}</div>}
 </div>;
};
