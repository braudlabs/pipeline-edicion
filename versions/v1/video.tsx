import React from 'react';
import {AbsoluteFill,Audio,OffthreadVideo,Img,Sequence,staticFile,useCurrentFrame,interpolate,Easing} from 'remotion';
import clips from './clips.json';
import captions from './captions.json';

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
 {name:'Generation loop',from:sec(15.42),to:sec(17.08)},
 {name:'Hours and credits',from:sec(20.19),to:sec(22.12)},
 {name:'Process path',from:sec(38.05),to:sec(41.95)},
 {name:'Real profile Kurt',from:sec(45.9),to:sec(48.22)},
 {name:'Real profile Elliot',from:sec(48.22),to:1209},
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

const Caption=()=>{
 const f=useCurrentFrame();
 const c=captions.find(c=>f>=c.from&&f<c.to);
 if(!c)return null;
 if(f>=sec(52.73)&&f<1306)return null;
 if(f>=sec(71.79))return null;
 const isCost=f>=sec(20.19)&&f<sec(22.12);
 const profile=f>=sec(45.9)&&f<1209;
 const visible=c.words.filter(w=>f>=w.from);
 if(!visible.length)return null;
 const emphasized=c.emphasis&&visible.length===c.words.length;
 const last=visible[visible.length-1];
 const enter=pop(f-last.from,5);
 const fullphrase=visible.map(w=>w.text).join(' ');
 const size=emphasized?(last.text.length>11?115:140):78;
 const top=isCost?1115:profile?1480:(f>=sec(38.05)&&f<sec(41.95))?1450:1115;
 return <div style={{position:'absolute',left:80,right:105,top,textAlign:'center',color:isCost?GREEN:'white',...baseText,textShadow:isCost?'none':'0 3px 12px rgba(0,0,0,.28)',transform:`translateY(${(1-enter)*7}px)`}}>
  {emphasized?<><div style={{fontSize:68,marginBottom:2}}>{visible.slice(0,-1).map(w=>w.text).join(' ')}</div><div style={{fontSize:size,transform:`scale(${.96+.04*enter})`}}>{last.text}</div></>:<div style={{fontSize:size}}>{fullphrase}</div>}
 </div>;
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

const LoopGraphic=()=>{
 const f=useCurrentFrame();const a=pop(f);
 return <div style={{position:'absolute',left:112,top:1310,width:830,height:225,opacity:a,transform:`translateY(${(1-a)*45}px)`}}>
  <svg width="830" height="225" viewBox="0 0 830 225">
   <path d="M105 100 H690 Q775 100 775 155 Q775 210 710 210 H140 Q55 210 55 155 Q55 100 105 100" stroke="white" strokeWidth="3" fill="none" opacity=".7"/>
   <path d="M370 198 L395 210 L370 222" stroke="white" strokeWidth="3" fill="none"/>
   {[120,400,680].map((x,i)=><g key={i} opacity={pop(f-i*4)}><circle cx={x} cy="100" r="45" fill={i===2?GREEN:'#f1f0e9'}/><text x={x} y="112" fontSize="34" textAnchor="middle" fill={i===2?'white':INK} fontFamily="Display" fontWeight="700">{i===2?'↻':i===1?'×':'+'}</text></g>)}
  </svg>
 </div>;
};

const CostGraphic=()=>{
 const f=useCurrentFrame(); const a=pop(f,7);const coins=9;
 return <AbsoluteFill style={{background:'radial-gradient(ellipse at 50% 40%,#fff 0%,#edede7 75%,#dadbd4 100%)',color:GREEN}}>
  <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute'}}>
   <g transform={`translate(360 855) scale(${.7+.3*a})`}>
    {Array.from({length:48},(_,i)=>{let t=i*Math.PI/24;return <line key={i} x1={Math.sin(t)*171} y1={Math.cos(t)*171} x2={Math.sin(t)*(i%4===0?198:185)} y2={Math.cos(t)*(i%4===0?198:185)} stroke={GREEN} opacity={i%4===0?.9:.35} strokeWidth={i%4===0?4:2}/>})}
    <circle r="154" fill="none" stroke={GREEN} strokeWidth="3"/>
    <line y2="-115" stroke={GREEN} strokeWidth="8" strokeLinecap="round" transform={`rotate(${f*15})`}/><line y2="-80" stroke={GREEN} strokeWidth="9" strokeLinecap="round" transform={`rotate(${30+f*2.4})`}/><circle r="9" fill={GREEN}/>
   </g>
   {Array.from({length:coins},(_,i)=>{let drop=pop(f-17-i*2,12);return <g key={i} transform={`translate(${680+(i%3)*55} ${970-Math.floor(i/3)*58+drop*370})`} opacity={1-drop}><ellipse rx="70" ry="24" fill="#759359" stroke={CREAM} strokeWidth="2"/><path d="M-70 0v15c0 32 140 32 140 0V0" fill={GREEN}/><text textAnchor="middle" y="8" fontFamily="Display" fontSize="28" fill={CREAM}>✦</text></g>})}
  </svg>
 </AbsoluteFill>;
};

const ProcessGraphic=()=>{
 const f=useCurrentFrame();const a=pop(f);
 return <div style={{position:'absolute',left:95,right:95,top:1120,height:295,opacity:a,transform:`translateY(${(1-a)*40}px)`}}>
  <svg width="890" height="295" viewBox="0 0 890 295">
   <path d="M40 105 C180 -45 240 260 360 80 S580 250 670 70 S780 120 850 110" fill="none" stroke="white" strokeWidth="3" strokeDasharray="5 8" opacity={.6*(1-pop(f-32,18))}/>
   <path d="M60 110 H830" fill="none" stroke="white" strokeWidth="4" strokeDasharray="770" strokeDashoffset={770*(1-pop(f-26,32))}/>
   {[70,440,820].map((x,i)=><g key={i} opacity={pop(f-25-i*12,12)}><circle cx={x} cy="110" r="38" fill={i===2?GREEN:'white'}/><text x={x} y="121" textAnchor="middle" fontSize="32" fontFamily="Display" fontWeight="700" fill={i===2?'white':INK}>{i===2?'✓':i+1}</text></g>)}
  </svg>
 </div>;
};

const Profile=({person}:{person:'kurt'|'elliot'})=>{
 const f=useCurrentFrame();const a=pop(f,8);const scroll=interpolate(f,[14,56],[0,person==='kurt'?510:780],{...clamp,easing:Easing.bezier(.4,0,.2,1)});
 return <AbsoluteFill style={{background:'#0e1013'}}>
  <div style={{position:'absolute',left:90,right:90,top:205,color:CREAM,...baseText,fontSize:52,letterSpacing:'-.035em'}}>@{person==='kurt'?'notkurtgodel':'notelliotkay'}</div>
  <div style={{position:'absolute',left:70,top:320,width:940,height:1080,overflow:'hidden',borderRadius:15,transform:`translateY(${(1-a)*70}px) scale(${.97+.03*a})`,opacity:a,boxShadow:'0 20px 100px rgba(0,0,0,.4)'}}>
   <Img src={asset(person+'-feed.png')} style={{width:940,position:'absolute',top:-scroll}}/>
  </div>
  <AbsoluteFill style={{background:'linear-gradient(0deg,#0e1013 10%,transparent 27%)',pointerEvents:'none'}}/>
 </AbsoluteFill>;
};

const BrandBumper=()=>{
 const f=useCurrentFrame();
 return <AbsoluteFill style={{background:'#1b1b1b'}}>
   {f<24?<OffthreadVideo muted src={asset('brand-bumper.mp4')} style={{width:'100%',height:'100%'}}/>:<Img src={asset('brand-still.png')} style={{width:'100%',height:'100%',transform:`scale(${1+(f-24)*.0005})`}}/>}
 </AbsoluteFill>;
};

const Price=()=>{
 const f=useCurrentFrame();const a=pop(f,9);
 return <AbsoluteFill>
  <AbsoluteFill style={{background:'linear-gradient(transparent 33%,rgba(11,15,10,.10) 47%,rgba(11,15,10,.88) 90%)',opacity:a}}/>
  <div style={{position:'absolute',top:1120,left:95,right:105,color:CREAM,textAlign:'center',...baseText,transform:`translateY(${(1-a)*80}px)`,opacity:a}}>
   <div style={{fontSize:69}}>Visual<span style={{color:'#e5da64'}}>.</span>Hub</div>
   <div style={{fontSize:265,letterSpacing:'-.075em',marginTop:8}}>39<span style={{fontSize:145,verticalAlign:'top',display:'inline-block',marginTop:23,marginLeft:6}}>$</span></div>
   <div style={{fontSize:44,fontWeight:400,letterSpacing:'-.025em',marginTop:22}}>Entra en skool.com/visual</div>
  </div>
 </AbsoluteFill>;
};

export const Ad=()=> <AbsoluteFill style={{background:'#161616',fontFamily:'Display'}}>
 <style>{`@font-face{font-family:Display;src:url('${asset('Display-Bold.otf')}');font-weight:700}@font-face{font-family:Display;src:url('${asset('Display-Regular.otf')}');font-weight:400}*{box-sizing:border-box}`}</style>
 <Footage/>
 <Audio src={asset('narration-master.wav')}/>
 <Sequence from={sec(5.55)} durationInFrames={sec(6.8)-sec(5.55)}><FaceProof/></Sequence>
 <Sequence from={sec(13.4)} durationInFrames={sec(14.18)-sec(13.4)}><FailedCut src="bad-hand.mp4" frame={35} label="Generación fallida"/></Sequence>
 <Sequence from={sec(14.72)} durationInFrames={sec(15.32)-sec(14.72)}><FailedCut src="bad-label.mp4" frame={40} label="Volver a generar"/></Sequence>
 <Sequence from={sec(15.42)} durationInFrames={sec(17.08)-sec(15.42)}><LoopGraphic/></Sequence>
 <Sequence from={sec(20.19)} durationInFrames={sec(22.12)-sec(20.19)}><CostGraphic/></Sequence>
 <Sequence from={sec(38.05)} durationInFrames={sec(41.95)-sec(38.05)}><ProcessGraphic/></Sequence>
 <Sequence from={sec(45.9)} durationInFrames={sec(48.22)-sec(45.9)}><Profile person="kurt"/></Sequence>
 <Sequence from={sec(48.22)} durationInFrames={1209-sec(48.22)}><Profile person="elliot"/></Sequence>
 <Sequence from={sec(52.73)} durationInFrames={1306-sec(52.73)}><BrandBumper/></Sequence>
 <Sequence from={sec(71.79)} durationInFrames={1765-sec(71.79)}><Price/></Sequence>
 <Caption/>
</AbsoluteFill>;
