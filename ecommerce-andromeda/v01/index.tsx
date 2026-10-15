import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Composition,OffthreadVideo,Sequence,staticFile,useCurrentFrame,registerRoot,delayRender,continueRender,cancelRender} from 'remotion';
import timeline from './timeline.json';
import cues from './cues.json';
import {textWidth,fitText} from '../../motor-editor/src/text';

type Cue=typeof cues[number];
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const ease=(n:number)=>1-(1-clamp(n))**4;
function Fonts(){const [handle]=useState(()=>delayRender('SF Pro local'));useEffect(()=>{Promise.all([['bold','700'],['regular','400']].map(async([file,weight])=>{const font=new FontFace('AndromedaSF',`url("${staticFile('assets/SFProDisplay-'+file+'.otf')}")`,{weight});await font.load();document.fonts.add(font)})).then(()=>continueRender(handle)).catch(cancelRender)},[handle]);return null}
function VideoSpine(){return <>{timeline.scenes.map(s=><Sequence key={s.id} name={`${s.id} · ${s.status}`} from={s.record_in_frame} durationInFrames={s.duration_frames}><OffthreadVideo src={staticFile(s.asset)} trimBefore={s.source_in_frame} muted style={{width:1080,height:1920,objectFit:'cover'}}/></Sequence>)}</>}
function Glyph({text,x,y,size,color='#f8fbff',weight=700}:{text:string;x:number;y:number;size:number;color?:string;weight?:number}){return <text x={x} y={y} textAnchor="middle" dominantBaseline="central" fontFamily="AndromedaSF" fontWeight={weight} fontSize={size} letterSpacing={size*-.035} fill={color} stroke="rgba(12,25,40,.45)" strokeWidth={1.3} paintOrder="stroke" style={{filter:'drop-shadow(0px 3px 5px rgba(6,20,34,.62))'}}>{text}</text>}
function Caption({cue:c,frame,variant='A'}:{cue:Cue;frame:number;variant?:string}){
 if(frame<c.start||frame>=c.end||c.kind==='drop')return null;
 const isDays=c.kind==='days';
 if(isDays&&variant==='B')return <svg width={1080} height={1920} style={{position:'absolute',inset:0}}><Glyph text="días" x={540} y={c.y-75} size={160}/><Glyph text="y días" x={540} y={c.y+70} size={160} color="#b1d8ff"/></svg>;
 if(isDays&&variant==='C'){const last=frame>=c.words[2].frame;return <svg width={1080} height={1920} style={{position:'absolute',inset:0}}><Glyph text={last?'y días':'días'} x={540} y={c.y} size={174}/></svg>}
 let layout:{x:number;y:number;size:number;color:string;axis:'x'|'y';distance:number;weight:number}[]=[];
 if(c.kind==='stack')layout=[{x:c.x,y:c.y-56,size:76,color:'#f8fbff',axis:'y',distance:0,weight:400},{x:c.x,y:c.y+36,size:148,color:'#b1d8ff',axis:'y',distance:32,weight:700}];
 else {
  let size=c.kind==='days'?158:c.kind==='punch'?c.size:Math.min(c.size,fitText(c.text,870,c.size,-.035));
  const sizes=c.words.map((_,i)=>isDays&&i===1?76:size);
  const widths=c.words.map((w,i)=>textWidth(w.text,sizes[i],-.035));const gap=size*.25;
  const total=widths.reduce((a,b)=>a+b,0)+gap*(widths.length-1);let x=c.x-total/2;
  layout=c.words.map((w,i)=>{const item={x:x+widths[i]/2,y:c.y,size:sizes[i],color:isDays&&i===2?'#b1d8ff':'#f8fbff',axis:(isDays?'x':'y') as 'x'|'y',distance:isDays?(i===2?30:-30):c.kind==='punch'?22:0,weight:700};x+=widths[i]+gap;return item;});
 }
 return <svg width={1080} height={1920} style={{position:'absolute',inset:0,overflow:'visible'}}>{c.words.map((w,i)=>{
  if(frame<w.frame)return null;const l=layout[i];const age=frame-w.frame;
  // Discrete word choice is evaluated once at the presentation frame. Blur samples geometry only.
  const moving=l.distance!==0;const samples=moving&&age<5?8:1;
  return <g key={i} style={{isolation:'isolate'}}>{Array.from({length:samples},(_,j)=>{
   const sample=frame+(samples===1?0:((j+.5)/samples-.5)*.5);const d=l.distance*(1-ease((sample-w.frame)/5));
   return <g key={j} opacity={1/samples} style={{mixBlendMode:samples>1?'plus-lighter':undefined}}><Glyph text={w.text+(i===c.words.length-1&&['c10','c14','c20','c24','c26','c30','c36','c40'].includes(c.id)?'.':'')} x={l.x+(l.axis==='x'?d:0)} y={l.y+(l.axis==='y'?d:0)} size={l.size} color={l.color} weight={l.weight}/></g>
  })}</g>
 })}</svg>
}
export function Andromeda(){const frame=useCurrentFrame();return <AbsoluteFill style={{background:'#1d343b'}}><Fonts/><VideoSpine/>{cues.map(c=><Caption key={c.id} cue={c} frame={frame}/>)}<Audio src={staticFile('assets/mix-preview.wav')}/></AbsoluteFill>}
function Concept({variant}:{variant:string}){const c=cues.find(c=>c.kind==='days')!;return <AbsoluteFill><Fonts/><OffthreadVideo src={staticFile(timeline.scenes[1].asset)} trimBefore={137} muted style={{width:1080,height:1920}}/><Caption cue={c} frame={269} variant={variant}/></AbsoluteFill>}
registerRoot(()=> <><Composition id="AndromedaV01" component={Andromeda} durationInFrames={920} fps={24} width={1080} height={1920}/>{['A','B','C'].map(variant=><Composition key={variant} id={'Concept'+variant} component={Concept} defaultProps={{variant}} durationInFrames={1} fps={24} width={1080} height={1920}/>)}</>);
