import React from 'react';
import {interpolate,useCurrentFrame} from 'remotion';
import captions from './captions.json';

const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const key=(f:number,t:number[],v:number[])=>interpolate(f,t,v,clamp);

/** Words keep their measured place in the line while their transform animates.
 * No reflow on every spoken word, and the entire keyword is readable on impact. */
export const KineticCaptions=()=>{
 const f=useCurrentFrame();
 const c=captions.find(c=>f>=c.from&&f<c.to);
 if(!c||(f>=1266&&f<1306)||f>=1723)return null;
 const cost=f>=485&&f<532;
 const proof=f>=1064&&f<1209;
 const process=f>=913&&f<1007;
 const isKeyword=c.emphasis;
 const last=c.words[c.words.length-1];
 const prefix=isKeyword?c.words.slice(0,-1):c.words;
 const top=proof?1480:process?1480:cost?1240:1175;
 const exit=key(f,[c.to-2,c.to],[0,1]);
 const keywordSize=last.text.length>11?133:last.text.length>9?146:164;
 const variant=c.clip%3;
 const renderWord=(w:typeof last,i:number)=>{
  const a=f-w.from;
  return <span key={w.from+'-'+i} style={{display:'inline-block',visibility:a<0?'hidden':'visible',marginRight:'.21em',whiteSpace:'pre',transformOrigin:'50% 85%',opacity:a<0?0:1,transform:`translate3d(${key(a,[0,3,7],[variant===1?-15:variant===2?15:0,2,0])}px,${key(a,[0,3,7],[23,-3,0])}px,0) rotate(${key(a,[0,3,7],[variant===1?-3:2,.4,0])}deg) scale(${key(a,[0,3,7],[.87,1.06,1])})`,filter:`blur(${key(a,[0,2,5],[1.8,.2,0])}px)`}}>{w.text}</span>;
 };
 const k=f-last.from;
 const strong=['rápido','contrario','generar','dinero','consistencia','error'].includes(last.text.toLowerCase());
 const slant=last.text==='contrario'?-1:1;
 const chars=last.text.split('');
 return <div style={{position:'absolute',left:82,right:100,top,textAlign:'center',fontFamily:'Display',fontWeight:700,color:'#fffef6',letterSpacing:'-.048em',lineHeight:1.01,textShadow:cost?'0 2px 20px rgba(10,35,5,.13)':'0 3px 17px rgba(0,0,0,.32)',transform:`translateY(${-6*exit}px)`,opacity:1-exit*.25}}>
  <div style={{fontSize:isKeyword?63:80,minHeight:isKeyword&&prefix.length?70:0,whiteSpace:'nowrap'}}>{prefix.map(renderWord)}</div>
  {isKeyword&&<div style={{fontSize:keywordSize,marginTop:prefix.length?-2:0,whiteSpace:'nowrap',visibility:k<0?'hidden':'visible',transformOrigin:'center',transform:`translateX(${key(k,[0,3,7,11],[strong?-40*slant:0,6*slant,-1,0])}px) translateY(${key(k,[0,3,7,11],[strong?35:22,-7,2,0])}px) rotate(${key(k,[0,4,9],[strong?-3.5*slant:0,.8*slant,0])}deg) scaleX(${key(k,[0,3,7,11],[strong?1.19:.90,.98,1.01,1])}) scaleY(${key(k,[0,3,7,11],[.72,1.09,.985,1])})`,filter:`blur(${key(k,[0,2,5],[strong?2:1,0,0])}px)`}}>
   {chars.map((ch,i)=><span key={i} style={{display:'inline-block',transform:`translateY(${key(k-i*.25,[0,3,7],[strong?12:4,-2,0])}px)`}}>{ch}</span>)}
  </div>}
 </div>;
};
