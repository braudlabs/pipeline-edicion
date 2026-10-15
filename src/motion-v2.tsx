import React from 'react';
import {AbsoluteFill,Img,OffthreadVideo,Sequence,interpolate,Easing,staticFile,useCurrentFrame} from 'remotion';
const CREAM='#f2f0e6',GREEN='#416b2c';
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const ease=Easing.bezier(.19,1,.22,1);
const key=(f:number,t:number[],v:number[])=>interpolate(f,t,v,clamp);
const smooth=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{...clamp,easing:ease});
const A=(s:string)=>staticFile('assets/'+s);
const v2=(s:string)=>A('v2/'+s);
const type:React.CSSProperties={fontFamily:'Display',fontWeight:700,letterSpacing:'-.055em',lineHeight:.96};

const Paper=({dark=false}:{dark?:boolean})=><AbsoluteFill style={{background:dark?'radial-gradient(ellipse at 55% 42%,#527c36 0%,#2e4c1f 65%,#182b10 100%)':'radial-gradient(ellipse at 50% 40%,#fffef8,#e6e5da 90%)'}}><svg width="1080" height="1920" style={{opacity:dark?.08:.035,mixBlendMode:dark?'screen':'multiply'}}><filter id="grain"><feTurbulence type="fractalNoise" baseFrequency=".62" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#grain)" opacity=".7"/></svg></AbsoluteFill>;

const Tile=({person,index,width=260}:{person:'kurt'|'elliot';index:number;width?:number})=><Img src={v2(`${person}-tile-${index}.jpg`)} style={{width,height:width*1.326,objectFit:'cover',borderRadius:13,boxShadow:'0 24px 55px rgba(10,17,5,.20)'}}/>;

/** One scene and one camera: the collage opens out into two real account panels. */
export const AccountMotion=()=>{
 const f=useCurrentFrame();
 const reveal=smooth(f,13,34);const swap=smooth(f,81,100);
 const cameraScale=key(f,[0,7,26,43,78,87,102,144],[1.35,.96,1,1.025,1.045,.91,1,1.02]);
 const turn=key(f,[0,10,31,81,88,105,144],[-6,1,0,0,-3,0,0]);
 const blur=key(f,[0,6,31,80,86,100],[5,0,0,0,3,0]);
 const number=smooth(f,57,67);
 return <AbsoluteFill style={{overflow:'hidden'}}>
  <Paper/>
  <div style={{position:'absolute',left:55,right:55,top:145,fontSize:390,...type,color:GREEN,opacity:number*.09,transform:`translateY(${(1-number)*45}px)`}}>2</div>
  <div style={{position:'absolute',inset:0,perspective:1800}}>
   <div style={{position:'absolute',inset:0,transformOrigin:'50% 43%',transform:`scale(${cameraScale}) rotate(${turn}deg)`,filter:`blur(${blur}px)`}}>
    {/* Moving source clips, framed by genuine feed tiles. */}
    <div style={{position:'absolute',left:0,top:0,opacity:1-reveal,transform:`scale(${1+reveal*.65}) translateY(${-reveal*190}px)`}}>
     {[0,1,2,3,4,5].map((n)=>{const col=n%3,row=Math.floor(n/3);const fly=1-smooth(f,n*1.5,10+n*1.5);return <div key={n} style={{position:'absolute',left:84+col*315,top:430+row*415,transform:`translateY(${fly*(row?300:-200)}px) rotate(${[-8,4,9,6,-5,7][n]}deg)`}}><Tile person={n<3?'kurt':'elliot'} index={n} width={280}/></div>})}
     <div style={{position:'absolute',left:335,top:590,width:410,height:665,border:'7px solid #f5f3e9',borderRadius:22,overflow:'hidden',boxShadow:'0 30px 100px rgba(20,30,10,.4)',transform:`rotate(${key(f,[0,16],[-8,-2])}deg)`}}><OffthreadVideo muted src={A('serum.mp4')} trimBefore={18} style={{width:'100%',height:'100%',objectFit:'cover'}}/></div>
    </div>
    <div style={{position:'absolute',left:0,top:0,opacity:reveal,transform:`translateY(${(1-reveal)*330}px)`}}>
     <div style={{position:'absolute',left:92-swap*1110,top:325,width:896,transform:`rotateY(${-swap*13}deg) rotate(${-swap*6}deg)`,transformOrigin:'right center'}}><AccountPanel person="kurt" frame={f-32}/></div>
     <div style={{position:'absolute',left:92+(1-swap)*1110,top:325,width:896,transform:`rotateY(${(1-swap)*13}deg) rotate(${(1-swap)*6}deg)`,transformOrigin:'left center'}}><AccountPanel person="elliot" frame={f-100}/></div>
    </div>
   </div>
  </div>
  <AbsoluteFill style={{pointerEvents:'none',background:'linear-gradient(transparent 65%,rgba(37,53,23,.25) 76%,rgba(26,40,18,.92) 88%,#1a2812 100%)'}}/>
 </AbsoluteFill>;
};

const AccountPanel=({person,frame}:{person:'kurt'|'elliot';frame:number})=>{
 const p=smooth(frame,22,55);const header=person==='kurt'?'@notkurtgodel':'@notelliotkay';
 return <div style={{position:'relative',color:CREAM,...type}}>
  <div style={{fontSize:58,color:GREEN,marginBottom:26,marginLeft:6,letterSpacing:'-.04em'}}>{header}<span style={{display:'inline-grid',placeItems:'center',width:32,height:32,marginLeft:12,borderRadius:'50%',background:GREEN,color:CREAM,fontSize:22,verticalAlign:'middle'}}>✓</span></div>
  <div style={{position:'relative',width:896,height:1040,borderRadius:25,overflow:'hidden',background:'#0e1013',border:'7px solid #f5f3e9',boxShadow:'0 28px 90px rgba(22,33,13,.32)'}}>
   <Img src={A(person+'-feed.png')} style={{position:'absolute',width:882,top:-p*(person==='kurt'?420:570),left:0}}/>
  </div>
 </div>;
};

export const CostMotion=()=>{
 const f=useCurrentFrame();const swap=smooth(f,13,28);const arrive=smooth(f,0,8);
 return <AbsoluteFill style={{overflow:'hidden'}}><Paper dark/>
  <div style={{position:'absolute',inset:0,transform:`scale(${key(f,[0,7,26,46],[1.3,1,1,1.035])}) rotate(${key(f,[0,8],[-7,0])}deg)`}}>
   <svg width="1080" height="1920" viewBox="0 0 1080 1920">
    <g transform={`translate(${540-swap*1100} 870) scale(${.78+.22*arrive})`}>
     {Array.from({length:60},(_,i)=>{const t=i*Math.PI/30;return <g key={i} opacity={.24+.7*smooth(f,i*.04,5+i*.04)}><line x1={Math.sin(t)*242} y1={Math.cos(t)*242} x2={Math.sin(t)*295} y2={Math.cos(t)*295} stroke={CREAM} strokeWidth={i%5===0?3:1}/><circle cx={Math.sin(t)*300} cy={Math.cos(t)*300} r={i%5===0?5:2.3} fill={CREAM}/></g>})}
     <circle r="214" fill="none" stroke={CREAM} strokeWidth="2" opacity=".4"/>
     <line y2="-160" stroke={CREAM} strokeWidth="10" strokeLinecap="round" transform={`rotate(${f*17})`}/><line y2="-100" stroke={CREAM} strokeWidth="12" strokeLinecap="round" transform={`rotate(${f*2.4+60})`}/><circle r="13" fill={CREAM}/>
    </g>
    <g transform={`translate(${540+(1-swap)*1100} 885) rotate(${(1-swap)*20})`}>
     {Array.from({length:8},(_,i)=>{const drop=smooth(f,28+i*.5,42+i*.5);return <g key={i} transform={`translate(${(i%2)*95-46+drop*(i%2?350:-350)} ${110-i*48+drop*550}) rotate(${drop*(i%2?70:-70)})`} opacity={1-drop}>
      <path d="M-150 0 v28 c0 68 300 68 300 0 V0" fill="#b8c9a1" stroke="#e4eada" strokeWidth="2"/>
      <ellipse rx="150" ry="43" fill={CREAM} stroke="#c8d0b5" strokeWidth="3"/><text y="13" textAnchor="middle" fill={GREEN} fontFamily="Display" fontSize="43" fontWeight="700">✦</text>
     </g>})}
    </g>
   </svg>
  </div>
 </AbsoluteFill>;
};

export const GenerationMotion=()=>{
 const f=useCurrentFrame();const positions=[-245,35,315];
 return <div style={{position:'absolute',left:0,right:0,top:0,height:1920,overflow:'hidden',background:'linear-gradient(transparent 42%,rgba(14,20,9,.88) 100%)'}}>
  {[0,1,2].map((n)=>{const a=smooth(f,n*4,n*4+9);const go=smooth(f,25,40);return <div key={n} style={{position:'absolute',left:335+positions[n],top:1370,width:235,height:290,borderRadius:14,border:`3px solid ${n===2?'#dce4ce':'#eeeae0'}`,overflow:'hidden',transform:`translateY(${(1-a)*200+go*40}px) rotate(${[-8,0,8][n]+(1-a)*12}deg) scale(${.85+.15*a})`,opacity:a*(1-go*.6),boxShadow:'0 14px 35px #0005'}}><Img src={v2(['bad-hand-still.jpg','bad-label-still.jpg','serum-still.jpg'][n])} style={{width:'100%',height:'100%',objectFit:'cover'}}/><span style={{position:'absolute',top:13,right:13,display:'grid',placeItems:'center',width:41,height:41,borderRadius:'50%',background:n===2?GREEN:'#a84435',color:'white',fontSize:35,fontFamily:'Display'}}>{n===2?'↻':'×'}</span></div>})}
  <svg width="1080" height="1920" style={{position:'absolute',top:0}}><path d="M210 1700 C130 1750 220 1800 550 1800 S930 1755 850 1700" stroke="white" strokeWidth="3" fill="none" opacity={smooth(f,8,18)*.6} strokeDasharray="8 6"/></svg>
 </div>;
};

export const ProcessMotion=()=>{
 const f=useCurrentFrame();const clean=smooth(f,21,53);const a=smooth(f,0,10);
 return <div style={{position:'absolute',left:0,right:0,top:0,height:1920,opacity:a,background:'linear-gradient(transparent 47%,rgba(15,25,10,.86) 100%)'}}>
  <svg width="1080" height="1920" viewBox="0 0 1080 1920">
   <path d="M160 1310 C320 1070 750 1610 400 1530 S730 1140 920 1330" fill="none" stroke="#edeedb" opacity={(1-clean)*.7} strokeWidth="3" strokeDasharray="6 6"/>
   <path d="M190 1320 H850" stroke="#edf0e2" strokeWidth="4" fill="none" strokeDasharray="660" strokeDashoffset={660*(1-clean)}/>
  </svg>
  {[0,1,2].map((n)=>{const x=175+n*320;const enter=smooth(f,7+n*9,22+n*9);const rot=(1-clean)*[-12,9,-8][n];return <div key={n} style={{position:'absolute',left:x-82,top:1220,width:165,height:218,overflow:'hidden',borderRadius:14,border:'3px solid #f5f4e6',boxShadow:'0 15px 45px #0006',transform:`translateY(${(1-enter)*120}px) rotate(${rot}deg) scale(${.8+.2*enter})`,opacity:enter}}><Img src={v2(['01-still.jpg','serum-still.jpg','09-still.jpg'][n])} style={{width:'100%',height:'100%',objectFit:'cover'}}/><div style={{position:'absolute',bottom:0,left:0,right:0,height:48,background:n===2?GREEN:'#ececdf',color:n===2?CREAM:GREEN,fontSize:24,...type,display:'grid',placeItems:'center',letterSpacing:'-.02em'}}>{['idea','sistema','resultado'][n]}</div></div>})}
 </div>;
};

export const PriceMotion=()=>{
 const f=useCurrentFrame();const a=smooth(f,0,10);const overshoot=key(f,[0,4,9,15],[.58,1.075,.985,1]);
 return <AbsoluteFill>
  <AbsoluteFill style={{background:'linear-gradient(transparent 33%,rgba(17,26,9,.2) 52%,rgba(13,23,7,.97) 100%)',opacity:a}}/>
  <div style={{position:'absolute',top:1130,left:80,right:100,textAlign:'center',color:CREAM,...type,transform:`translateY(${key(f,[0,6,12],[120,-7,0])}px)`}}>
   <div style={{fontSize:66,opacity:a,marginBottom:4}}>Visual<span style={{color:'#e5da64'}}>.</span>Hub</div>
   <div style={{fontSize:302,letterSpacing:'-.075em',transform:`scale(${overshoot}) rotate(${key(f,[0,7,15],[-5,1,0])}deg)`,filter:`blur(${key(f,[0,3,7],[6,1,0])}px)`}}><span>3</span><span style={{display:'inline-block',transform:`translateY(${key(f,[0,5,10],[65,-5,0])}px)`}}>9</span><span style={{fontSize:128,verticalAlign:'top',display:'inline-block',marginTop:38,marginLeft:8}}>$</span></div>
   <div style={{display:'inline-flex',alignItems:'center',gap:20,fontSize:46,letterSpacing:'-.025em',borderBottom:'2px solid #f2f0e665',padding:'14px 0',opacity:smooth(f,6,14),transform:`translateY(${(1-smooth(f,6,16))*20}px)`}}>skool.com/visual <span style={{display:'inline-block',transform:`translateX(${key(f,[8,15,22],[0,12,0])}px)`}}>↗</span></div>
  </div>
 </AbsoluteFill>;
};
