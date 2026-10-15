import React,{useEffect,useState} from 'react';
import {RelationView} from './editorial-v2/RelationView.tsx';
import {createReferenceEntrance} from './caption-keyframes/reference-v2.ts';
import {AbsoluteFill,Audio,Img,OffthreadVideo,Sequence,delayRender,continueRender,cancelRender,staticFile,useCurrentFrame} from 'remotion';
import type {Plan,Node,Graphic,Asset} from './types.ts';
import {fpsValue,sample,state,countAt,shutterSamples} from './motion.ts';
const url=(s:string)=>/^(https?:|data:|blob:)/.test(s)?s:staticFile(s);
const transform=(s:ReturnType<typeof state>)=>`translate(${s.x}px,${s.y}px) rotate(${s.rotate}deg) rotateY(${s.rotateY}deg) scale(${s.scale})`;
function Fonts({plan}:{plan:Plan}){
 const [handle]=useState(()=>delayRender('Cargando las fuentes fijadas del motor'));
 useEffect(()=>{let active=true;Promise.all([[plan.font.boldSrc,'700'],[plan.font.regularSrc,'400']].map(async([src,weight])=>{const font=new FontFace(plan.font.family,`url("${url(src)}")`,{weight});await font.load();document.fonts.add(font);})).then(()=>{if(active)continueRender(handle);}).catch(e=>{if(active)cancelRender(e);});return()=>{active=false;};},[handle,plan.font.boldSrc,plan.font.regularSrc,plan.font.family]);
 return null;
}
function DrawNode({node:n,frame,plan,weight=1,presentationFrame=frame}:{node:Node;frame:number;plan:Plan;weight?:number;presentationFrame?:number}){
 if(frame<n.start||frame>=n.end)return null;
 if(n.motionBlur)return <AbsoluteFill style={{isolation:'isolate',pointerEvents:'none'}}>{shutterSamples(frame,n.start,n.end,n.motionBlur.samples,n.motionBlur.angle).map((s,i)=><DrawNode key={i} node={{...n,motionBlur:undefined}} frame={s.frame} presentationFrame={presentationFrame} plan={plan} weight={s.weight}/>)}</AbsoluteFill>;
 if(n.kind==='relation')return <RelationView node={n} time={frame/fpsValue(plan.fps)} contextTime={presentationFrame/fpsValue(plan.fps)} width={plan.width} height={plan.height} fontFamily={plan.font.family} weight={weight}/>;
 const m=state(n.motion,frame);
 if(n.referenceEntrance){const p=createReferenceEntrance(n.referenceEntrance.profile,n.referenceEntrance.spec).atFrame(frame,plan.fps,plan.height);m.y+=p.translationY;m.opacity*=p.opacity;}
 let text=n.text;
 if(n.counter)text=`${n.counter.prefix}${countAt(n.counter.target,frame-n.counter.start,n.counter.duration)}${n.counter.suffix}`;
 const fill=n.fill??plan.palette.foreground;
 const common:React.CSSProperties={position:'absolute',inset:0,opacity:m.opacity*weight,mixBlendMode:weight<1?'plus-lighter':undefined,transform:transform(m),transformOrigin:`${n.x}px ${n.y}px`,filter:[m.blur?`blur(${m.blur}px)`:'',n.shadow?`drop-shadow(${n.shadow.x}px ${n.shadow.y}px ${n.shadow.blur}px ${n.shadow.color})`:''].filter(Boolean).join(' ')||undefined,pointerEvents:'none'};
 if(n.kind==='image'){
  const asset=plan.assets.find(a=>a.id===n.assetId)!;const width=n.width!,height=n.height!;
  const clip=n.crop?`inset(${n.crop.y*100}% ${(1-n.crop.x-n.crop.width)*100}% ${(1-n.crop.y-n.crop.height)*100}% ${n.crop.x*100}%)`:undefined;
  return <div style={common}><Img src={url(asset.src)} style={{position:'absolute',left:n.x-width/2,top:n.y-height/2,width,height,objectFit:'contain',clipPath:clip}}/></div>;
 }
 return <svg width={plan.width} height={plan.height} viewBox={`0 0 ${plan.width} ${plan.height}`} style={{...common,overflow:'visible'}}>
  {n.kind==='text'&&<text x={n.x} y={n.y} dominantBaseline="central" textAnchor="middle" fontFamily={plan.font.family} fontWeight={n.weight??700} fontSize={n.fontSize} letterSpacing={(n.tracking??-.06)*(n.fontSize??1)} fill={fill} stroke={n.stroke} strokeWidth={n.strokeWidth} paintOrder="stroke" style={{fontKerning:'normal'}}>{text}</text>}
  {n.kind==='rect'&&<rect x={n.x-(n.width??0)/2} y={n.y-(n.height??0)/2} width={n.width} height={n.height} rx={n.radius??0} fill={fill} stroke={n.stroke} strokeWidth={n.strokeWidth}/>}
  {n.kind==='circle'&&<ellipse cx={n.x} cy={n.y} rx={(n.width??0)/2} ry={(n.height??n.width??0)/2} fill={fill} stroke={n.stroke} strokeWidth={n.strokeWidth}/>}
  {n.kind==='line'&&<line x1={n.x} y1={n.y} x2={n.x+(n.width??0)} y2={n.y+(n.height??0)} stroke={n.stroke??fill} strokeWidth={n.strokeWidth??1}/>}
 </svg>;
}
function VisualMedia({asset,sourceStart,plan,crop,muted=true}:{asset:Asset;sourceStart:number;plan:Plan;crop:{scale:number;x:number;y:number};muted?:boolean}){
 const style:React.CSSProperties={width:'100%',height:'100%',objectFit:'cover',transform:`translate(${crop.x*plan.width}px,${crop.y*plan.height}px) scale(${crop.scale})`,transformOrigin:'50% 50%'};
 return asset.kind==='image'?<Img src={url(asset.src)} style={style}/>:<OffthreadVideo src={url(asset.src)} trimBefore={Math.round(sourceStart*fpsValue(plan.fps))} muted={muted} style={style}/>;
}
function GraphicLayer({g,frame,plan}:{g:Graphic;frame:number;plan:Plan}){
 if(frame<g.start||frame>=g.end)return null;const camera=state(g.camera,frame),sorted=[...g.nodes].sort((a,b)=>a.z-b.z);
 const mask=g.cutout;const clip=mask?plan.clips.find(c=>c.shotId===mask.shotId&&c.start<=frame&&c.end>frame):undefined;
 const cutout=mask&&clip?<Sequence from={clip.start} durationInFrames={clip.end-clip.start} layout="none"><AbsoluteFill><VisualMedia asset={plan.assets.find(a=>a.id===mask.assetId)!} sourceStart={clip.sourceStart} crop={clip.crop} plan={plan}/></AbsoluteFill></Sequence>:null;
 return <AbsoluteFill style={{background:g.fullScreen?g.background:undefined}}>
  <AbsoluteFill style={{transform:transform(camera),opacity:camera.opacity,transformOrigin:'50% 50%',perspective:plan.width*1.6}}>
   {sorted.filter(n=>!mask||n.z<=mask.fillZ).map(n=><DrawNode key={n.id} node={n} frame={frame} plan={plan}/>)}
   {cutout}
   {mask&&sorted.filter(n=>n.z>mask.fillZ).map(n=><DrawNode key={n.id} node={n} frame={frame} plan={plan}/>)}
  </AbsoluteFill>
 </AbsoluteFill>;
}
export function EditComposition({plan}:{plan:Plan}){
 const frame=useCurrentFrame();
 return <AbsoluteFill style={{background:plan.palette.background,overflow:'hidden'}}>
  <Fonts plan={plan}/>
  {plan.clips.map(clip=><Sequence key={clip.id} from={clip.start} durationInFrames={clip.end-clip.start}><VisualMedia asset={plan.assets.find(a=>a.id===clip.assetId)!} sourceStart={clip.sourceStart} crop={clip.crop} plan={plan} muted={clip.mute}/></Sequence>)}
  {plan.graphics.map(g=><GraphicLayer key={g.id} g={g} frame={frame} plan={plan}/>)}
  {plan.captions.map(c=><DrawNode key={c.id} frame={frame} plan={plan} node={{...c,kind:'text',z:50,weight:700}}/>)}
  {plan.audio.map(a=><Sequence key={a.id} from={a.start} durationInFrames={a.end-a.start} layout="none"><Audio src={url(plan.assets.find(x=>x.id===a.assetId)!.src)} trimBefore={Math.round(a.sourceStart*fpsValue(plan.fps))} volume={f=>sample(a.gain,f+a.start,1)}/></Sequence>)}
 </AbsoluteFill>;
}
