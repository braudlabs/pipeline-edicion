import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Img,Composition,registerRoot,useCurrentFrame,staticFile,delayRender,continueRender,Easing} from 'remotion';
import spec from './design.json';
const S:any=spec;
const family:any={light:'ReplicaLight',regular:'ReplicaRegular',bold:'ReplicaBold',italic:'ReplicaItalic',bolditalic:'ReplicaBoldItalic'};
const face:any={light:'HelveticaNeue-Light.ttf',regular:'Arial.ttf',bold:'Arial-Bold.ttf',italic:'Arial-Italic.ttf',bolditalic:'Arial-Bold-Italic.ttf'};
const mix=(a:any,b:any,p:number):any=>Array.isArray(a)?a.map((v,i)=>mix(v,b[i],p)):a+(b-a)*p;
function value(n:any,p:string,f:number,def:any){
 const a=n.anim?.[p];if(!a)return n[p]??def;
 if(f<=a.frames[0])return a.values[0];if(f>=a.frames.at(-1))return a.values.at(-1);
 let i=a.frames.findIndex((v:number)=>v>f)-1;let t=(f-a.frames[i])/(a.frames[i+1]-a.frames[i]);
 if(a.ease==='hold')t=0;else if(a.ease==='out')t=Easing.bezier(.15,0,.2,1)(t);else if(a.ease==='smooth')t=Easing.bezier(.33,0,.67,1)(t);
 return mix(a.values[i],a.values[i+1],t);
}
function Layer({n,f,id}:{n:any,f:number,id:string}){
 if(f<n.from||f>=n.to)return null;
 let pos=value(n,'pos',f,[0,0]),a=value(n,'anchor',f,[0,0]),s=value(n,'scale',f,[1,1]);
 let filter=[];const blur=value(n,'blur',f,0);if(blur>0)filter.push(`blur(${blur}px)`);
 if(n.shadow){let [x,y,b,c,op]=n.shadow;filter.push(`drop-shadow(${x}px ${y}px ${b}px ${c})`)}
 if(n.chroma){filter.push(`drop-shadow(0px ${n.chroma}px 0.35px rgba(239,64,43,.65)) drop-shadow(0px -${n.chroma}px 0.3px rgba(24,77,255,.65))`)}
 if(n.glow)filter.push(`drop-shadow(0px 0px ${n.glow/2}px ${n.glowColor||'#b3a7b2'})`);
 let body:React.ReactNode=null;let common:any={overflow:'visible',display:'block'};
 if(n.type==='text'){
  const W=Math.ceil(n.text.length*n.size*.82+140),margin=70+(n.align==='center'?(W-140)/2:0),H=n.size*2+140;
  body=<svg width={W} height={H} style={{...common,position:'absolute',left:-margin,top:-n.size-margin}}><text x={margin} y={n.size+margin} fill={n.color} fontFamily={family[n.font]} fontSize={n.size} letterSpacing={n.track*n.size/1000} textAnchor={n.align==='center'?'middle':'start'}>{n.text}</text></svg>;
 }else if(n.type==='image')body=<Img src={staticFile('assets/'+n.asset)} style={{width:n.w,height:n.h,display:'block'}}/>;
 else if(n.type==='comp')body=<Stage name={n.source} f={f} nested/>;
 else if(n.type==='rect')body=<div style={{width:n.w,height:n.h,background:n.color,borderRadius:n.round||0}}/>;
 else if(n.type==='ellipse')body=<div style={{width:n.w,height:n.h,left:-n.w/2,top:-n.h/2,position:'absolute',borderRadius:'50%',background:n.color}}/>;
 else if(n.type==='gradient'){
  const c=n.center||[n.w/2,n.h/2];body=<div style={{width:n.w,height:n.h,background:n.radius?`radial-gradient(circle ${n.radius}px at ${c[0]}px ${c[1]}px,${n.color} 0%,${n.endColor} 100%)`:n.color}}/>;
 }else if(n.type==='path'){
  const d='M'+n.points.map((p:any)=>p.join(',')).join(' L')+(n.closed?' Z':'');
  body=<svg width={2200} height={2200} style={{...common,position:'absolute'}}><path d={d} fill={n.color||'none'} stroke={n.stroke||'none'} strokeWidth={n.strokeWidth||0} strokeLinejoin="round"/></svg>;
 }else if(n.type==='scanlines')body=<div style={{width:n.w,height:n.h,background:'repeating-linear-gradient(to bottom,transparent 0px,transparent 5px,#000 5px,#000 6px)'}}/>;
 let wipe=value(n,'wipe',f,0);
 const w=n.type==='comp'?S.comps[n.source].width:n.w||0,h=n.type==='comp'?S.comps[n.source].height:n.h||0;
 const transform=`translate3d(${pos[0]}px,${pos[1]}px,0) rotateZ(${value(n,'rot',f,0)}deg) rotateY(${value(n,'ry',f,0)}deg) rotateX(${value(n,'rx',f,0)}deg) scale(${s[0]},${s[1]}) translate(${-a[0]}px,${-a[1]}px)`;
 return <div style={{position:'absolute',left:0,top:0,width:w,height:h,transformOrigin:'0 0',transform,opacity:value(n,'opacity',f,1),filter:filter.join(' ')||undefined,clipPath:wipe?`inset(0 ${wipe/2}%)`:n.round?`inset(0 round ${n.round}px)`:undefined}}>{body}</div>;
}
function Stage({name,f,nested=false}:{name:string,f:number,nested?:boolean}){
 const c=S.comps[name];let layers=c.layers;
 if(name==='06 - Calendar board'){const rig=S.comps['07 - Calendar camera'].layers.find((n:any)=>n.source===name);const target=value(rig,'anchor',f,[405,400]);layers=layers.filter((n:any)=>!['text','ellipse'].includes(n.type)||(Math.abs(n.pos[0]-target[0])<780&&Math.abs(n.pos[1]-target[1])<1050));}
 return <div style={{position:'absolute',width:c.width,height:c.height,overflow:'hidden',perspective:1800,perspectiveOrigin:'50% 50%'}}>{layers.map((n:any,i:number)=><Layer key={i} n={n} f={f} id={name+i}/>)}</div>;
}
const Replica=()=>{
 const f=useCurrentFrame();const [handle]=useState(()=>delayRender('Cargando tipografía de réplica'));
 useEffect(()=>{Promise.all(Object.keys(family).map(async k=>{const font=new FontFace(family[k],`url(${staticFile('assets/'+face[k])})`);await font.load();document.fonts.add(font);})).then(()=>continueRender(handle));},[handle]);
 // Six subframe samples spanning a centered 240-degree shutter, with source cuts kept hard.
 const moving=[[0,28],[30,41],[55,95],[137,176],[213,231],[235,240],[297,330]].some(([a,b])=>f>=a&&f<b);
 const samples=moving?6:1,angle=240/360;const cuts=[0,30,138,215,...S.dateTargets.map((d:any)=>d[0]),330].sort((a,b)=>a-b);let lo=0,hi=330;for(let i=0;i<cuts.length-1;i++){if(f>=cuts[i]&&f<cuts[i+1]){lo=cuts[i];hi=cuts[i+1];}}
 return <AbsoluteFill style={{background:'#000',isolation:'isolate'}}><Audio src={staticFile('assets/reference-audio.wav')}/>{Array.from({length:samples},(_,i)=>{const t=Math.min(hi-.001,Math.max(lo,f+angle*((i+.5)/samples-.5)));return <AbsoluteFill key={i} style={{opacity:1/(i+1)}}><Stage name={S.master} f={t}/></AbsoluteFill>})}</AbsoluteFill>;
};
registerRoot(()=> <Composition id="Replica96c1" component={Replica} width={720} height={1280} fps={30} durationInFrames={330}/>);
