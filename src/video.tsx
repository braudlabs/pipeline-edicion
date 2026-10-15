import React from 'react';
import {AbsoluteFill,Audio,OffthreadVideo,Img,Sequence,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
import edl from './edl-v3.json';
import timing from './timing-v3.json';
import {KineticCaptions} from './captions-v5';
import {AccountMotion,CostMotion,GenerationMotion,ProcessMotion,PriceMotion} from './motion-v4';

import {useEditFrame,FRAME_RATIO} from './edit-time';
const FPS=24;
const GREEN='#416b2c', CREAM='#f1f0e9', INK='#151714';
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const ease=Easing.bezier(.16,1,.3,1);
const pop=(f:number,d=8)=>interpolate(f,[0,d],[0,1],{...clamp,easing:ease});
const asset=(s:string)=>staticFile('assets/'+s);
const sec=(s:number)=>Math.round(s*FPS);
const baseText:React.CSSProperties={fontFamily:'Display',fontWeight:700,letterSpacing:'-.055em',lineHeight:.98};

export const graphics=timing.events;
const Footage=()=>{
 return <>{edl.map(c=><Sequence key={`${c.id}-${c.part}`} from={c.fromFrame*FRAME_RATIO} durationInFrames={c.duration*FRAME_RATIO} name={`Toma ${c.id} / ${c.sourceFrom}–${c.sourceTo}`}>
   <Shot id={c.id} part={c.part} src={c.src} start={c.sourceFrom}/>
 </Sequence>)}</>;
};
const Shot=({id,part,src,start}:{id:number;part:number;src:string;start:number})=>{
 const f=useEditFrame();let s=1;
 if(id===1)s=part===1?1.045:1+pop(f-44,4)*.055;
 if(id===3)s=1+pop(f-30,6)*.045;
 const close=[1,2,4,5,6,7,8,11,12].includes(id);
 if(close)s=id===6?.9:1;
 if(id===13)s=1+pop(f,100)*.055;
 const shotSrc=close?asset(`v5/${String(id).padStart(2,'0')}-reframed.mp4`):staticFile(src);
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <OffthreadVideo muted src={shotSrc} trimBefore={start*FRAME_RATIO} style={{position:'absolute',width:'100%',height:'100%',objectFit:'cover',transform:close?undefined:`scale(${s})`,transformOrigin:'50% 40%'}}/>
  {close&&<AbsoluteFill style={{background:id===6?'linear-gradient(to bottom, transparent 60%, rgba(15,16,13,.3) 69%, rgba(15,16,13,.94) 82%, #0f100d 95%)':'linear-gradient(to bottom, transparent 65%, rgba(15,16,13,.25) 74%, rgba(15,16,13,.95) 88%, #0f100d 100%)'}}/>}
 </AbsoluteFill>;
};

const FaceProof=()=>{
 const f=useEditFrame();const a=pop(f,6)*(1-interpolate(f,[24,30],[0,1],clamp));
 return <div style={{position:'absolute',left:270,top:390,width:525,height:580,opacity:a,transform:`scale(${1.04-.04*pop(f)})`}}>
  {[[0,0,0],[1,0,90],[1,1,180],[0,1,270]].map(([x,y,rot],i)=><div key={i} style={{position:'absolute',left:x?undefined:0,right:x?0:undefined,top:y?undefined:0,bottom:y?0:undefined,width:52,height:52,borderLeft:'3px solid rgba(255,255,255,.8)',borderTop:'3px solid rgba(255,255,255,.8)',transform:`rotate(${rot}deg)`}}/>)}
  <div style={{position:'absolute',right:-62,top:75,writingMode:'vertical-rl',fontSize:27,color:'white',letterSpacing:'.01em'}}>generada con IA</div>
 </div>;
};

const FailedCut=({src,frame,label}:{src:string;frame:number;label:string})=>{
 const f=useEditFrame();
 return <AbsoluteFill style={{background:'#181818'}}>
  <OffthreadVideo muted src={asset(src)} trimBefore={frame*FRAME_RATIO} style={{height:'100%',width:'100%',objectFit:'cover',transform:`scale(${1.02+f*.002})`}}/>
  <AbsoluteFill style={{background:'linear-gradient(transparent 55%,rgba(0,0,0,.25))'}}/>
  <div style={{position:'absolute',left:95,top:310,display:'flex',gap:15,alignItems:'center',color:'white',fontSize:34,...baseText,letterSpacing:'-.02em'}}><span style={{display:'grid',placeItems:'center',width:43,height:43,borderRadius:99,background:'#c54839',fontSize:36}}>×</span>{label}</div>
 </AbsoluteFill>;
};

const BrandBumper=()=>{
 const f=useEditFrame();
 return <AbsoluteFill style={{background:'#1b1b1b'}}>
   {f<24?<OffthreadVideo muted src={asset('brand-bumper.mp4')} style={{width:'100%',height:'100%'}}/>:<Img src={asset('brand-still.png')} style={{width:'100%',height:'100%',transform:`scale(${1+(f-24)*.0005})`}}/>}
 </AbsoluteFill>;
};

const Event=({name,children}:{name:keyof typeof timing.events;children:React.ReactNode})=>{
 const e=timing.events[name];return <Sequence from={e.from*FRAME_RATIO} durationInFrames={(e.to-e.from)*FRAME_RATIO} name={name}>{children}</Sequence>;
};
export const Ad=()=> <AbsoluteFill style={{background:'#161616',fontFamily:'Display'}}>
 <style>{`@font-face{font-family:Display;src:url('${asset('Display-Bold.otf')}');font-weight:700}@font-face{font-family:Display;src:url('${asset('Display-Regular.otf')}');font-weight:400}*{box-sizing:border-box}`}</style>
 <Footage/>
 <Audio src={asset('v3/audio-mix-master.wav')}/>
 <Event name="face"><FaceProof/></Event>
 <Event name="hand"><FailedCut src="bad-hand.mp4" frame={35} label="Generación fallida"/></Event>
 <Event name="label"><FailedCut src="bad-label.mp4" frame={40} label="Volver a generar"/></Event>
 <Event name="generation"><GenerationMotion/></Event>
 <Event name="cost"><CostMotion/></Event>
 <Event name="process"><ProcessMotion/></Event>
 <Event name="accounts"><OffthreadVideo muted src={asset('v5/accounts-ae.mp4')} style={{width:'100%',height:'100%'}}/></Event>
 <Event name="brand"><BrandBumper/></Event>
 <Event name="price"><PriceMotion/></Event>
 <KineticCaptions/>
</AbsoluteFill>;
