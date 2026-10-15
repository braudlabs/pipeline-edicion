import React from 'react';
import {AbsoluteFill,Audio,OffthreadVideo,Img,Sequence,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
import clips from './clips.json';
import {KineticCaptions} from './captions-v2';
import {AccountMotion,CostMotion,GenerationMotion,ProcessMotion,PriceMotion} from './motion-v2';

const FPS=24;
const GREEN='#416b2c', CREAM='#f1f0e9', INK='#151714';
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const ease=Easing.bezier(.16,1,.3,1);
const pop=(f:number,d=8)=>interpolate(f,[0,d],[0,1],{...clamp,easing:ease});
const asset=(s:string)=>staticFile('assets/'+s);
const sec=(s:number)=>Math.round(s*FPS);
const baseText:React.CSSProperties={fontFamily:'Display',fontWeight:700,letterSpacing:'-.055em',lineHeight:.98};

export const graphics=[
 {name:'Face proof',from:sec(5.55),to:sec(6.8)},
 {name:'Failed hand',from:sec(13.40),to:sec(14.18)},
 {name:'Failed label',from:sec(14.72),to:sec(15.32)},
 {name:'Generation loop',from:sec(15.42),to:411},
 {name:'Hours and credits',from:sec(20.19),to:532},
 {name:'Process path',from:sec(38.05),to:sec(41.95)},
 {name:'Account motion collage and profiles',from:1064,to:1209},
 {name:'Visual Hub bumper',from:sec(52.73),to:1306},
 {name:'Price and CTA',from:sec(71.79),to:1765},
];

const Footage=()=>{
 const f=useCurrentFrame();
 return <>{clips.map(c=>{
   let s=1;
   // Continuous shots share one transform across their source boundary.
   if(c.id===7||c.id===8)s=1;
   else if(c.id===11||c.id===12)s=1;
   else if(c.id===1)s=f<sec(2.31)?1:f<sec(2.9)?1.095:1;
   else if(c.id===2)s=f>=sec(9.75)?1.08:1;
   else if(c.id===3)s=f<sec(12.75)?1:f<sec(14.36)?1.08:1.03;
   else if(c.id===6)s=f>=sec(30.45)?1.065:1;
   else if(c.id===13)s=1+pop(f-c.from,110)*.065;
   return <Sequence key={c.id} from={c.from} durationInFrames={c.duration} name={`Toma ${c.id}`}>
    <AbsoluteFill style={{overflow:'hidden'}}><OffthreadVideo muted src={staticFile(c.src)} style={{width:'100%',height:'100%',objectFit:'cover',transform:`scale(${s})`,transformOrigin:'50% 40%'}}/></AbsoluteFill>
   </Sequence>
 })}</>;
};

const FaceProof=()=>{
 const f=useCurrentFrame();const a=pop(f,6)*(1-interpolate(f,[24,30],[0,1],clamp));
 return <div style={{position:'absolute',left:270,top:390,width:525,height:580,opacity:a,transform:`scale(${1.04-.04*pop(f)})`}}>
  {[[0,0,0],[1,0,90],[1,1,180],[0,1,270]].map(([x,y,rot],i)=><div key={i} style={{position:'absolute',left:x?undefined:0,right:x?0:undefined,top:y?undefined:0,bottom:y?0:undefined,width:52,height:52,borderLeft:'3px solid rgba(255,255,255,.8)',borderTop:'3px solid rgba(255,255,255,.8)',transform:`rotate(${rot}deg)`}}/>)}
  <div style={{position:'absolute',right:-62,top:75,writingMode:'vertical-rl',fontSize:27,color:'white',letterSpacing:'.01em'}}>generada con IA</div>
 </div>;
};

const FailedCut=({src,frame,label}:{src:string;frame:number;label:string})=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{background:'#181818'}}>
  <OffthreadVideo muted src={asset(src)} trimBefore={frame} style={{height:'100%',width:'100%',objectFit:'cover',transform:`scale(${1.02+f*.002})`}}/>
  <AbsoluteFill style={{background:'linear-gradient(transparent 55%,rgba(0,0,0,.25))'}}/>
  <div style={{position:'absolute',left:95,top:190,display:'flex',gap:15,alignItems:'center',color:'white',fontSize:34,...baseText,letterSpacing:'-.02em'}}><span style={{display:'grid',placeItems:'center',width:43,height:43,borderRadius:99,background:'#c54839',fontSize:36}}>×</span>{label}</div>
 </AbsoluteFill>;
};

const BrandBumper=()=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{background:'#1b1b1b'}}>
   {f<24?<OffthreadVideo muted src={asset('brand-bumper.mp4')} style={{width:'100%',height:'100%'}}/>:<Img src={asset('brand-still.png')} style={{width:'100%',height:'100%',transform:`scale(${1+(f-24)*.0005})`}}/>}
 </AbsoluteFill>;
};

export const Ad=()=> <AbsoluteFill style={{background:'#161616',fontFamily:'Display'}}>
 <style>{`@font-face{font-family:Display;src:url('${asset('Display-Bold.otf')}');font-weight:700}@font-face{font-family:Display;src:url('${asset('Display-Regular.otf')}');font-weight:400}*{box-sizing:border-box}`}</style>
 <Footage/>
 <Audio src={asset('v2/audio-mix-master.wav')}/>
 <Sequence from={sec(5.55)} durationInFrames={sec(6.8)-sec(5.55)}><FaceProof/></Sequence>
 <Sequence from={sec(13.4)} durationInFrames={sec(14.18)-sec(13.4)}><FailedCut src="bad-hand.mp4" frame={35} label="Generación fallida"/></Sequence>
 <Sequence from={sec(14.72)} durationInFrames={sec(15.32)-sec(14.72)}><FailedCut src="bad-label.mp4" frame={40} label="Volver a generar"/></Sequence>
 <Sequence from={sec(15.42)} durationInFrames={411-sec(15.42)}><GenerationMotion/></Sequence>
 <Sequence from={sec(20.19)} durationInFrames={532-sec(20.19)}><CostMotion/></Sequence>
 <Sequence from={sec(38.05)} durationInFrames={sec(41.95)-sec(38.05)}><ProcessMotion/></Sequence>
 <Sequence from={1064} durationInFrames={1209-1064}><AccountMotion/></Sequence>
 <Sequence from={sec(52.73)} durationInFrames={1306-sec(52.73)}><BrandBumper/></Sequence>
 <Sequence from={sec(71.79)} durationInFrames={1765-sec(71.79)}><PriceMotion/></Sequence>
 <KineticCaptions/>
</AbsoluteFill>;
