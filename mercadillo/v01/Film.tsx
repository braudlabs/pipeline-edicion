import React,{useState,useEffect} from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,Sequence,staticFile,useCurrentFrame,delayRender,continueRender,cancelRender} from 'remotion';
import rawCues from './cues.json';
import inputs from './inputs.json';
import maskFrames from './study/mask-frames.json';
import {pose,envelope,type Caption} from './motion';
export const FPS=24,FRAMES=2121;
export const captions=rawCues as Caption[];
const assets=(s:string)=>staticFile('assets/'+s);
const masks=new Set(maskFrames);
export function Fonts(){const[h]=useState(()=>delayRender('Mercadillo typefaces'));useEffect(()=>{Promise.all([['Sans-Regular.otf','400'],['Sans-Bold.otf','700']].map(async([file,weight])=>{const f=new FontFace('Mercadillo SF',`url(${assets(file)})`,{weight});await f.load();document.fonts.add(f)})).then(()=>continueRender(h)).catch(cancelRender)},[h]);return null}
function Mask({frame,id}:{frame:number;id:string}){return <defs><filter id={'invert-'+id}><feComponentTransfer><feFuncR type="linear" slope="-1" intercept="1"/><feFuncG type="linear" slope="-1" intercept="1"/><feFuncB type="linear" slope="-1" intercept="1"/></feComponentTransfer></filter><mask id={id} x="0" y="0" width="1080" height="1920" maskUnits="userSpaceOnUse" style={{maskType:'luminance'}}><rect width="1080" height="1920" fill="white"/><image href={assets(`masks/${String(frame).padStart(4,'0')}.png`)} width="1080" height="1920" filter={`url(#invert-${id})`}/></mask></defs>}
function Type({c,t,mask}:{c:Caption;t:number;mask?:string}){
 const q=pose(c,t);if(q.alpha<=0)return null;
 const transform=`translate(${q.x} ${q.y}) scale(${q.scale}) rotate(${q.rotate})`;
 const lettering={fontFamily:'Mercadillo SF',fontSize:c.size,fontWeight:c.weight,letterSpacing:-c.size*.055,textAnchor:'middle' as const};
 return <g opacity={q.alpha}>
   <g mask={c.masked&&mask?`url(#${mask})`:undefined}><text {...lettering} transform={transform} fill={c.color} stroke="#16282a" strokeWidth={c.masked?0:.7} paintOrder="stroke" style={{filter:c.masked?'none':'drop-shadow(0px 2px 3.5px #102226ab)'}}>{c.text}</text></g>
   {c.masked&&mask&&<text {...lettering} transform={transform} fill="none" stroke={c.color} strokeWidth="1.65" opacity=".9">{c.text}</text>}
 </g>
}
export const musicPoints=[[0,0],[.09,.34],[13.1,.33],[14.5,.39],[20.7,.30],[21,.11],[21.95,.13],[22.083,.42],[26.83,.31],[32.5,.29],[32.67,.10],[35.55,.10],[35.7,.31],[39.3,.34],[39.43,.16],[40.3,.31],[42.1,.29],[42.17,.025],[43.32,.025],[43.4,.25],[47.6,.17],[47.88,.095],[51.55,.07],[52.5,.45],[56.15,.36],[56.38,.29],[62.08,.36],[65.1,.30],[69.98,.28],[70.1,.12],[71.6,.12],[71.91,.37],[74.10,.35],[74.20,.43],[75,.29],[80.54,.35],[86.8,.3],[87.08,.14],[87.3,.27],[87.92,.15],[88.375,0]];
const hits=[{t:.54,file:'air',gain:.28},{t:7.79,file:'tap',gain:.28},{t:8.65,file:'air',gain:.25},{t:12.31,file:'resolve',gain:.27},{t:18.86,file:'tap',gain:.2},{t:23.82,file:'air',gain:.22},{t:38.42,file:'tap',gain:.22},{t:39.31,file:'resolve',gain:.35},{t:51.61,file:'tap',gain:.23},{t:58.18,file:'air',gain:.24},{t:74.16,file:'resolve',gain:.3},{t:81.28,file:'tap',gain:.22}];
export function Film({sound=true,blur=.4}:{sound?:boolean;blur?:number}){
 const frame=useCurrentFrame(),t=frame/FPS;
 const mono=t>=42.16&&t<43.15;
 const active=captions.filter(c=>t>c.start-1/FPS&&t<c.end+1/FPS);
 const hasMask=masks.has(frame)&&active.some(c=>c.masked);
 const samples=blur>0?5:1;
 return <AbsoluteFill style={{background:'#12242c',overflow:'hidden'}}><Fonts/>
  <AbsoluteFill style={{filter:mono?'grayscale(1) contrast(1.05)':'none'}}>
   {inputs.clips.map(c=><Sequence key={c.numero} from={c.timeline_in_frame} durationInFrames={c.duracion_frames} name={c.titulo}><OffthreadVideo src={assets(c.archivo.split('/').at(-1)!)} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/></Sequence>)}
  </AbsoluteFill>
  {hasMask&&<Img src={assets(`masks/${String(frame).padStart(4,'0')}.png`)} style={{position:'absolute',opacity:0,width:1,height:1}}/>}
  <AbsoluteFill style={{isolation:'isolate'}}>{Array.from({length:samples},(_,i)=>{
   const sample=t+(samples===1?0:(i/(samples-1)-.5)*blur/FPS),mask='subject-'+i;
   return <svg key={i} viewBox="0 0 1080 1920" style={{position:'absolute',inset:0,width:'100%',height:'100%',opacity:1/samples,mixBlendMode:'plus-lighter'}}>
    {hasMask&&<Mask frame={frame} id={mask}/>}
    {active.map(c=><Type key={c.id} c={c} t={sample} mask={hasMask?mask:undefined}/>)}
   </svg>
  })}</AbsoluteFill>
  {sound&&<><Audio src={assets('dialogue-foley.wav')}/><Audio src={assets('music.wav')} trimBefore={48} volume={f=>envelope(f/FPS,musicPoints)}/>{hits.map((h,i)=><Sequence key={i} from={Math.round(h.t*FPS)} durationInFrames={12}><Audio src={assets(h.file+'.wav')} volume={h.gain}/></Sequence>)}</>}
 </AbsoluteFill>
}
export function Concept({variant='A'}:{variant?:string}){
 const lime='#d7f58c';const base:Caption={id:'design',text:'',start:0,end:20,x:540,y:1000,size:180,weight:700,color:lime,motion:'direct'};
 return <AbsoluteFill><Fonts/><Img src={assets('design.jpg')} style={{width:'100%',height:'100%'}}/>
 <svg viewBox="0 0 1080 1920" style={{position:'absolute',inset:0,width:'100%',height:'100%'}}><Mask frame={30} id="concept-person"/>
 {variant==='A'&&captions.filter(c=>c.group==='hook').map(c=><Type key={c.id} c={{...c,motion:'direct'}} t={1.3} mask="concept-person"/>)}
 {variant==='B'&&<>{[[-210,0,.8],[0,230,1],[180,470,.8]].map(([x,y,s],i)=><g key={i} opacity={i===1?1:.55}><Type c={{...base,x:540+x,y:690+y,size:225*s,text:'agencia',masked:true}} t={1} mask="concept-person"/></g>)}<Type c={{...base,y:1420,size:102,text:'de contenido'}} t={1}/></>}
 {variant==='C'&&<g transform="translate(150 1090) rotate(-6)"><defs><filter id="paper"><feTurbulence baseFrequency=".4" numOctaves="2" seed="4" type="fractalNoise"/><feComposite operator="in" in2="SourceGraphic"/><feBlend in="SourceGraphic" mode="multiply"/></filter></defs><path d="M0 0 H760 L845 135 L760 360 H0 Z" fill="#eee7cc" stroke="#c7bea3" strokeWidth="3" style={{filter:'drop-shadow(0 18px 20px #16282a44)'}}/><circle cx="775" cy="135" r="17" fill="#203f45"/><path d="M775 135 C990 -220,950 -460,875 -560" stroke="#c7aa7d" strokeWidth="5" fill="none"/><text x="50" y="92" fontFamily="Mercadillo SF" fontWeight="700" fontSize="75" fill="#23434a">Si eres una</text><text x="44" y="239" fontFamily="Mercadillo SF" fontWeight="700" fontSize="155" letterSpacing="-7" fill="#23434a">agencia</text><text x="50" y="312" fontFamily="Mercadillo SF" fontSize="66" fill="#23434a">de contenido.</text></g>}
 </svg></AbsoluteFill>
}
