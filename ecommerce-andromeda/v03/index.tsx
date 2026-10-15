import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Composition,Img,OffthreadVideo,Sequence,staticFile,useCurrentFrame,registerRoot,delayRender,continueRender,cancelRender} from 'remotion';
import timeline from './timeline.json';
import elements from './choreography.json';
import {textWidth,fitText} from '../../motor-editor/src/text';
type Element=typeof elements[number];
const OUTPUT_FPS=48,SOURCE_FPS=24,RATIO=OUTPUT_FPS/SOURCE_FPS;
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
const ease=(n:number)=>1-(1-clamp(n))**3;
function Fonts(){const [handle]=useState(()=>delayRender('SF Pro local'));useEffect(()=>{Promise.all([['bold','700'],['regular','400']].map(async([file,weight])=>{const font=new FontFace('AndromedaSF',`url("${staticFile('assets/SFProDisplay-'+file+'.otf')}")`,{weight});await font.load();document.fonts.add(font)})).then(()=>continueRender(handle)).catch(cancelRender)},[handle]);return null}
function VideoSpine(){return <>{timeline.scenes.map(s=><Sequence key={s.id} name={`${s.id} · ${s.status}`} from={s.record_in_frame*RATIO} durationInFrames={s.duration_frames*RATIO}><OffthreadVideo src={staticFile(s.asset)} trimBefore={s.source_in_frame*RATIO} muted style={{width:1080,height:1920,objectFit:'cover'}}/></Sequence>)}</>}
function SubjectMask({frame}:{frame:number}){return <defs><filter id="invert-subject"><feComponentTransfer><feFuncR type="linear" slope="-1" intercept="1"/><feFuncG type="linear" slope="-1" intercept="1"/><feFuncB type="linear" slope="-1" intercept="1"/></feComponentTransfer></filter><mask id="behind-person" x={0} y={0} width={1080} height={1920} maskUnits="userSpaceOnUse" style={{maskType:'luminance'}}><rect width={1080} height={1920} fill="white"/><image href={staticFile(`assets/masks/${String(frame).padStart(4,'0')}.png`)} width={1080} height={1920} filter="url(#invert-subject)"/></mask></defs>}
function Caption({e,frame}:{e:Element;frame:number}){
 if(frame<e.start||frame>=e.end)return null;
 const age=frame-e.start;
 const hero=e.motion==='occlusion';
 const size=fitText(e.text,e.width??860,e.size,-.045,e.weight);
 // One complete semantic unit is legible on its first frame. Motion never delays the next word.
 const p=ease(age/(hero?6:4));const remain=1-p;
 const x=e.x+(e.motion==='slide'?18*remain:0);
 const y=e.y+(e.motion==='slide'?0:(hero?26:14)*remain);
 const transform=`translate(${x} ${y})`;
 const lettering={fontFamily:'AndromedaSF',fontWeight:e.weight,fontSize:size,letterSpacing:-size*.045,textAnchor:'middle' as const,dominantBaseline:'central' as const,transform};
 const shadow='drop-shadow(0px 2px 3px rgba(8,20,35,.6))';
 const width=textWidth(e.text,size,-.045,e.weight)+12;
 const reveal=ease((age-1.5)/5.5);
 if(hero)return <g>
   {e.resolveFill&&<defs><clipPath id={'fill-'+e.id}><rect x={x-width/2} y={y-size*.6} width={width*reveal} height={size*1.3}/></clipPath></defs>}
   <g mask="url(#behind-person)"><text {...lettering} fill="#fffdf3" style={{filter:shadow}}>{e.text}</text></g>
   <text {...lettering} fill="none" stroke="#fffdf3" strokeWidth={3.2} strokeLinejoin="round" opacity={.98} style={{filter:'drop-shadow(0px 1px 1.5px rgba(0,0,0,.65))'}}>{e.text}</text>
   {e.resolveFill&&<g clipPath={`url(#fill-${e.id})`}><text {...lettering} fill="#fffdf3" style={{filter:shadow}}>{e.text}</text></g>}
  </g>;
 return <text {...lettering} fill="#fcfdff" stroke="rgba(12,24,36,.32)" strokeWidth={1.1} paintOrder="stroke" style={{filter:shadow}}>{e.text}</text>
}
export function Andromeda(){const frame=useCurrentFrame()/RATIO;const nativeFrame=Math.floor(frame+1e-7);const active=elements.filter(e=>frame>=e.start&&frame<e.end);const masked=active.some(e=>e.motion==='occlusion');return <AbsoluteFill style={{background:'#1d343b'}}><Fonts/><VideoSpine/>{masked&&<Img src={staticFile(`assets/masks/${String(nativeFrame).padStart(4,'0')}.png`)} style={{position:'absolute',opacity:0,width:1,height:1}}/>}<svg width={1080} height={1920} style={{position:'absolute',inset:0}}>{masked&&<SubjectMask frame={nativeFrame}/>} {active.map(e=><Caption key={e.id} e={e} frame={frame}/>)}</svg><Audio src={staticFile('assets/mix-preview.wav')}/></AbsoluteFill>}
registerRoot(()=> <Composition id="AndromedaV03" component={Andromeda} durationInFrames={1840} fps={OUTPUT_FPS} width={1080} height={1920}/>);
