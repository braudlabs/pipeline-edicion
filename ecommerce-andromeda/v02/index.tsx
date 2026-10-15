import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Composition,OffthreadVideo,Sequence,staticFile,useCurrentFrame,registerRoot,delayRender,continueRender,cancelRender} from 'remotion';
import timeline from './timeline.json';
import elements from './choreography.json';
import {textWidth,fitText} from '../../motor-editor/src/text';
type Word={text:string;frame:number};
type Element={id:string;text:string;start:number;end:number;x:number;y:number;size:number;weight:number;motion:string;words?:Word[];width?:number;duration?:number;change?:number;join?:number};
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const out=(n:number)=>1-(1-clamp(n))**4;
const smooth=(n:number)=>{n=clamp(n);return n*n*(3-2*n)};
function Fonts(){const [handle]=useState(()=>delayRender('SF Pro local'));useEffect(()=>{Promise.all([['bold','700'],['regular','400']].map(async([file,weight])=>{const font=new FontFace('AndromedaSF',`url("${staticFile('assets/SFProDisplay-'+file+'.otf')}")`,{weight});await font.load();document.fonts.add(font)})).then(()=>continueRender(handle)).catch(cancelRender)},[handle]);return null}
function VideoSpine(){return <>{timeline.scenes.map(s=><Sequence key={s.id} name={`${s.id} · ${s.status}`} from={s.record_in_frame} durationInFrames={s.duration_frames}><OffthreadVideo src={staticFile(s.asset)} trimBefore={s.source_in_frame} muted style={{width:1080,height:1920,objectFit:'cover'}}/></Sequence>)}</>}
function Glyph({text,size,weight}:{text:string;size:number;weight:number}){return <text textAnchor="middle" dominantBaseline="central" fontFamily="AndromedaSF" fontWeight={weight} fontSize={size} letterSpacing={size*-.035} fill="#fcfdff" stroke="rgba(17,27,38,.36)" strokeWidth={1.15} paintOrder="stroke" style={{filter:'drop-shadow(0px 3px 4px rgba(7,18,31,.7))'}}>{text}</text>}
function pose(motion:string,age:number,duration=5){
 const u=out(age/duration),r=1-u;
 if(motion==='slide')return {x:34*r,y:0,scale:1,alpha:clamp((age+.4)/1.7),blur:3*r};
 if(motion==='fall')return {x:0,y:-28*r,scale:1,alpha:clamp((age+.4)/1.6),blur:2*r};
 if(motion==='impact'){const p=clamp(age/5);const scale=p<.55? .84+.19*out(p/.55):1.03-.03*smooth((p-.55)/.45);return {x:0,y:0,scale,alpha:clamp((age+.4)/1.4),blur:2*r}}
 if(motion==='mask')return {x:0,y:76*r,scale:1,alpha:1,blur:3*r};
 if(motion==='wipe')return {x:18*r,y:0,scale:1,alpha:1,blur:1.5*r};
 return {x:0,y:29*r,scale:1,alpha:clamp((age+.4)/1.7),blur:2.6*r};
}
function Token({e,text,start,frame,x,y,size,index=0}:{e:Element;text:string;start:number;frame:number;x:number;y:number;size:number;index?:number}){
 if(frame<start)return null;
 const p=pose(e.motion,frame-start,e.duration??5);const exit=e.end-frame;
 const q=clamp(1-exit/2); // two-frame directed handoff; no long opacity cross-fade of different strings
 const width=textWidth(text,size,-.035,e.weight)+18;
 const clip=e.id+'-'+index;
 return <g opacity={p.alpha*(1-q*q)}>
  <defs><clipPath id={clip}><rect x={x-width/2-9} y={y-size*.55} width={e.motion==='wipe'?(width+18)*out((frame-start+1)/5):width+18} height={size*1.14}/></clipPath></defs>
  <g clipPath={e.motion==='mask'||e.motion==='wipe'?`url(#${clip})`:undefined}>
   <g transform={`translate(${x+p.x} ${y+p.y-10*q*q}) scale(${p.scale})`} style={{filter:p.blur>.05?`blur(${p.blur.toFixed(2)}px)`:undefined}}><Glyph text={text} size={size} weight={e.weight}/></g>
  </g>
 </g>
}
function Caption({e,frame,variant='B'}:{e:Element;frame:number;variant?:string}){
 if(frame<e.start||frame>=e.end)return null;
 const size=fitText(e.text,e.width??860,e.size,-.035,e.weight);
 if(e.motion==='roll'){
  const changed=frame>=(e.change??0),p=out((frame-(e.change??0))/6);
  if(variant==='A')return <><Token e={{...e,motion:'rise'}} text="días" start={e.start} frame={frame} x={335} y={e.y} size={172}/>{frame>=261&&<Token e={{...e,motion:'slide'}} text="y días" start={261} frame={frame} x={720} y={e.y} size={172}/>}</>;
  if(variant==='C')return <><Token e={{...e,motion:'mask'}} text="días" start={e.start} frame={frame} x={540} y={e.y-75} size={154}/>{frame>=261&&<Token e={{...e,motion:'mask'}} text="y días" start={261} frame={frame} x={540} y={e.y+65} size={154}/>}</>;
  return <>
   <defs><clipPath id="day-slot"><rect x={180} y={e.y-110} width={720} height={220}/></clipPath></defs>
   <g clipPath="url(#day-slot)">
    {!changed?<Token e={{...e,motion:'mask'}} text="días" start={e.start} frame={frame} x={540} y={e.y} size={198}/>:<><g transform={`translate(540 ${e.y-175*p})`} opacity={1-p} style={{filter:`blur(${3*p}px)`}}><Glyph text="días" size={198} weight={400}/></g><g transform={`translate(540 ${e.y+175*(1-p)})`} style={{filter:`blur(${3*(1-p)}px)`}}><Glyph text="y días" size={198} weight={400}/></g></>}
   </g>
  </>
 }
 const words=e.words??[{text:e.text,frame:e.start}];
 const widths=words.map(w=>textWidth(w.text,size,-.035,e.weight));const gap=size*.245;
 let cursor=e.x-(widths.reduce((a,b)=>a+b,0)+gap*(words.length-1))/2;
 return <>{words.map((w,i)=>{const x=cursor+widths[i]/2;cursor+=widths[i]+gap;return <Token key={i} e={e} text={w.text} start={w.frame} frame={frame} x={x} y={e.y} size={size} index={i}/>})}</>
}
export function Andromeda(){const frame=useCurrentFrame();return <AbsoluteFill style={{background:'#1d343b'}}><Fonts/><VideoSpine/><svg width={1080} height={1920} style={{position:'absolute',inset:0}}>{(elements as Element[]).map(e=><Caption key={e.id} e={e} frame={frame}/>)}</svg><Audio src={staticFile('assets/mix-preview.wav')}/></AbsoluteFill>}
function Concept({variant}:{variant:string}){const e=elements.find(e=>e.motion==='roll')!;return <AbsoluteFill><Fonts/><OffthreadVideo src={staticFile(timeline.scenes[1].asset)} trimBefore={137} muted style={{width:1080,height:1920}}/><svg width={1080} height={1920} style={{position:"absolute",inset:0}}><Caption e={e} frame={271} variant={variant}/></svg></AbsoluteFill>}
registerRoot(()=> <><Composition id="AndromedaV02" component={Andromeda} durationInFrames={920} fps={24} width={1080} height={1920}/>{['A','B','C'].map(variant=><Composition key={variant} id={'Concept'+variant} component={Concept} defaultProps={{variant}} durationInFrames={1} fps={24} width={1080} height={1920}/>)}</>);
