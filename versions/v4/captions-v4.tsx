import React from 'react';
import {interpolate,Easing} from 'remotion';
import {useEditFrame} from './edit-time';
import captions from './captions-v3.json';
import layouts from './caption-layout-v4.json';
import timing from './timing-v3.json';
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const ease=Easing.bezier(.16,1,.3,1);
const ramp=(f:number,d:number)=>interpolate(f,[0,d],[0,1],{...clamp,easing:ease});
const inside=(f:number,k:keyof typeof timing.events)=>f>=timing.events[k].from&&f<timing.events[k].to;
/** Per-phrase placement clears the expanded face rectangle. Natural line height
 * and visible overflow retain the full glyph, including g/p/y descenders. */
export const KineticCaptions=()=>{
 const f=useEditFrame();const index=captions.findIndex(c=>f>=c.from&&f<c.to);
 if(index<0||inside(f,'brand')||inside(f,'price'))return null;
 const c=captions[index],layout=layouts[index];
 const board=inside(f,'accounts'),cost=inside(f,'cost'),process=inside(f,'process'),generation=inside(f,'generation');
 const graphic=board||cost||process||generation;
 const above=!graphic&&layout.mode==='above';
 const stacked=c.emphasis&&(cost||(!graphic&&layout.mode==='below'));
 const top=board?1100:cost?985:process||generation?1060:layout.top;
 const size=board?Math.min(c.fontSize,64):cost?58:process||generation?68:stacked?55:layout.fontSize;
 const last=c.words[c.words.length-1];const prefix=stacked?c.words.slice(0,-1):c.words;
 const renderWord=(w:typeof last,i:number)=>{
  const age=f-w.from;const travel=(above?-18:18)*(1-ramp(age,3));
  return <span key={i} style={{display:'inline-block',marginRight:i===prefix.length-1?0:'.2em',visibility:age<0?'hidden':'visible',opacity:interpolate(age,[0,2],[.4,1],clamp),transform:`translateY(${travel}px)`}}>{w.text}</span>;
 };
 return <div data-caption-index={index} style={{position:'absolute',left:90,right:100,top,color:board?'#26381e':'#fffef6',textAlign:'center',fontFamily:'Display',fontWeight:700,lineHeight:1.28,letterSpacing:'-.035em',overflow:'visible',paddingBottom:24,textShadow:board?'0 2px 12px #faf7ee':'0 3px 13px #0009'}}>
  <div style={{fontSize:size,whiteSpace:'nowrap'}}>{prefix.map(renderWord)}</div>
  {stacked&&<div style={{fontSize:Math.min(c.keywordSize,cost?128:layout.keywordSize),lineHeight:1.28,whiteSpace:'nowrap',visibility:f<last.from?'hidden':'visible',opacity:interpolate(f-last.from,[0,3],[.38,1],clamp),transform:`translateY(${28*(1-ramp(f-last.from,6))}px)`}}>{last.text}</div>}
 </div>;
};
