import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,staticFile,useCurrentFrame,delayRender,continueRender,cancelRender} from 'remotion';
import {cues,cream,accent,ink} from './cues';
import {pose,FPS,type Cue} from './motion';
export {cues,FPS};
export const FRAMES=2278;
const asset=(s:string)=>staticFile('assets/'+s);
function Fonts(){const[h]=useState(()=>delayRender('V07 SF Pro'));useEffect(()=>{Promise.all([['SF Birdie','Sans-Regular.otf','400'],['SF Birdie','Sans-Bold.otf','700'],['Birdie Condensed','Condensed.ttf','400']].map(async([family,f,weight])=>{const face=new FontFace(family,`url(${asset(f)})`,{weight});await face.load();document.fonts.add(face)})).then(()=>continueRender(h)).catch(cancelRender)},[h]);return null}
function TextContent({c}:{c:Cue}){if(!c.highlight)return <>{c.text}</>;const at=c.text.indexOf(c.highlight);if(at<0)return <>{c.text}</>;return <>{c.text.slice(0,at)}<tspan fill={accent} fontWeight={700}>{c.highlight}</tspan>{c.text.slice(at+c.highlight.length)}</>}
function Letter({c,t,mask,uid}:{c:Cue;t:number;mask:string|null;uid:number}){
 const p=pose(c,t);if(p.alpha<=0)return null;const color=c.color??cream,dark=color===ink;
 return <g opacity={p.alpha} mask={c.masked&&mask?`url(#subject-mask-${uid})`:undefined}>
  <g transform={`translate(${p.x} ${p.y}) scale(${p.scale})`}>
   {c.motion==='reveal'&&<defs><clipPath id={`reveal-${c.id}-${uid}`}><rect x={c.anchor==='start'?-5:-540} y="-700" width={(c.revealWidth??1000)*p.reveal} height="1000"/></clipPath></defs>}
   <g clipPath={c.motion==='reveal'?`url(#reveal-${c.id}-${uid})`:undefined}>
    <text x="0" y="0" textAnchor={c.anchor??'middle'} fontFamily={c.condensed?'Birdie Condensed':'SF Birdie'} fontSize={c.size} fontWeight={c.weight??400} letterSpacing={c.size*(c.tracking??-.045)} fill={c.outline?'none':color} stroke={c.outline?color:dark?'#fffdec':ink} strokeWidth={c.outline?2.6:c.strokeWidth??(dark?1.5:c.contrast?1.5:.45)} paintOrder="stroke" style={{filter:c.outline?'none':dark?'drop-shadow(0px 1px 2px #f1ecd255)':c.contrast?'drop-shadow(0px 2px 3.5px #082019df)':'drop-shadow(0px 1.5px 2.5px #08201990)'}}><TextContent c={c}/></text>
   </g>
  </g>
 </g>
}
export function Film({blur=.32,sound=true}:{blur?:number;sound?:boolean}){
 const frame=useCurrentFrame(),t=frame/FPS,mask=frame>=550&&frame<=599?asset(`masks/${String(frame).padStart(4,'0')}.png`):null;
 const active=cues.filter(c=>t>=c.start-1/FPS&&t<c.end+1/FPS),samples=blur>0?5:1;
 return <AbsoluteFill style={{background:ink,overflow:'hidden'}}><Fonts/><OffthreadVideo src={asset('source.mp4')} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/>
  {mask&&<Img src={mask} style={{position:'absolute',width:1,height:1,opacity:0}}/>}
  <AbsoluteFill style={{isolation:'isolate'}}>{Array.from({length:samples},(_,i)=>{
   const sample=t+(samples===1?0:(i/(samples-1)-.5)*blur/FPS);
   return <svg key={i} viewBox="0 0 1080 1920" style={{position:'absolute',width:'100%',height:'100%',inset:0,opacity:1/samples,mixBlendMode:'plus-lighter'}}>
    <defs><filter id={`invert-${i}`}><feComponentTransfer><feFuncR type="linear" slope="-1" intercept="1"/><feFuncG type="linear" slope="-1" intercept="1"/><feFuncB type="linear" slope="-1" intercept="1"/></feComponentTransfer></filter><mask id={`subject-mask-${i}`} maskUnits="userSpaceOnUse" x="0" y="0" width="1080" height="1920" style={{maskType:'luminance'}}><rect width="1080" height="1920" fill="white"/>{mask&&<image href={mask} width="1080" height="1920" filter={`url(#invert-${i})`}/>}</mask></defs>
    {active.map(c=><Letter key={c.id} c={c} t={sample} mask={mask} uid={i}/>)}
   </svg>
  })}</AbsoluteFill>
  {sound&&<Audio src={asset('mix.wav')}/>}</AbsoluteFill>;
}
