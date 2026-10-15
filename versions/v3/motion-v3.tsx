import React from 'react';
import {AbsoluteFill,Img,OffthreadVideo,interpolate,Easing,staticFile,useCurrentFrame} from 'remotion';
const CREAM='#f3f0e5',GREEN='#355526',INK='#1c2919';
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const out=Easing.bezier(.16,1,.3,1),travel=Easing.bezier(.7,0,.2,1);
const k=(f:number,t:number[],v:number[])=>interpolate(f,t,v,clamp);
const q=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{...clamp,easing:out});
const go=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{...clamp,easing:travel});
const A=(s:string)=>staticFile('assets/'+s);
const type:React.CSSProperties={fontFamily:'Display',fontWeight:700,letterSpacing:'-.055em',lineHeight:.96};
const Paper=({dark=false}:{dark?:boolean})=><AbsoluteFill style={{background:dark?'radial-gradient(ellipse at 48% 40%,#567b38,#2a471d 64%,#172a10)':'radial-gradient(ellipse at 48% 40%,#fffcf1,#e5e2d4 90%)'}}><svg width="1080" height="1920" style={{opacity:dark?.075:.035,mixBlendMode:dark?'screen':'multiply'}}><filter id="grain3"><feTurbulence type="fractalNoise" baseFrequency=".64" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(#grain3)"/></svg></AbsoluteFill>;
const Profile=({person}:{person:string})=><Img src={A(`v3/${person}-profile-proof.png`)} style={{width:680,borderRadius:14,border:'3px solid #ffffffaa',boxShadow:'0 18px 45px #13240822'}}/>;
const Node=({x,y,children}:{x:number;y:number;children:React.ReactNode})=><div style={{position:'absolute',left:x,top:y,width:0,height:0}}>{children}</div>;
const Follower=({person,value,label,frame}:{person:string;value:string;label:string;frame:number})=>{
 const a=q(frame,0,7);
 return <div style={{position:'absolute',left:-440,top:-295,width:880,textAlign:'center',color:INK,...type}}>
  <div style={{display:'flex',justifyContent:'center',alignItems:'center',gap:15,fontSize:42,letterSpacing:'-.025em'}}><Img src={A(`v3/${person}-avatar.png`)} style={{width:62,height:62,borderRadius:'50%'}}/>@{label}<span style={{fontSize:26,color:GREEN}}>✓</span></div>
  <div style={{fontSize:226,marginTop:18,letterSpacing:'-.065em',opacity:a,transform:`translateY(${70*(1-a)}px)`}}>{value}</div>
  <div style={{fontSize:43,letterSpacing:'.07em',textTransform:'uppercase',marginTop:10}}>seguidores</div>
  <div style={{position:'absolute',left:100,top:395,opacity:q(frame,9,16),transform:`translateY(${30*(1-q(frame,9,16))}px)`}}><Profile person={person}/></div>
 </div>;
};
const Views=({person,value,frame}:{person:string;value:string;frame:number})=>{
 const line=q(frame,3,17);const reveal=q(frame,9,18);
 return <div style={{position:'absolute',left:-440,top:-335,width:900,height:660,color:INK,...type}}>
  <div style={{position:'absolute',left:12,top:50,fontSize:37,letterSpacing:'-.025em'}}>@{person==='kurt'?'notkurtgodel':'notelliotkay'}</div>
  <div style={{position:'absolute',left:0,top:138,width:535,fontSize:196,letterSpacing:'-.06em',transform:`translateY(${50*(1-q(frame,0,8))}px)`}}>{value}</div>
  <div style={{position:'absolute',left:10,top:362,fontSize:41,letterSpacing:'-.02em'}}>visualizaciones</div>
  <div style={{position:'absolute',left:12,top:420,fontSize:29,fontWeight:400,letterSpacing:0,color:'#567044'}}>en un solo reel</div>
  <svg width="940" height="660" style={{position:'absolute',left:0,top:0}}>
   <path d="M90 491 H477 Q502 491 502 466 V110 Q502 84 530 84 H563" fill="none" stroke={GREEN} strokeWidth="3" pathLength="1" strokeDasharray="1" strokeDashoffset={1-line}/><circle cx="90" cy="491" r="6" fill={GREEN}/><circle cx="563" cy="84" r={6*line} fill={GREEN}/>
  </svg>
  <div style={{position:'absolute',left:573,top:0,width:290,opacity:reveal,transform:`translateX(${60*(1-reveal)}px)`}}>
   <Img src={A(`v3/${person}-proof-0.png`)} style={{width:290,borderRadius:15,border:'5px solid #fffdf6',boxShadow:'0 20px 55px #19301730'}}/>
   <div style={{marginTop:16,fontSize:28,letterSpacing:0,textAlign:'center',fontWeight:400}}>captura del reel</div>
  </div>
 </div>;
};
/** All four facts occupy one persistent world. The camera follows its connectors.
 * Motion along a single screen axis per move, with a brief zoom-out for context. */
export const AccountMotion=()=>{
 const f=useCurrentFrame();
 const down1=go(f,35,48),right=go(f,83,97),down2=go(f,130,144);
 const cx=right*1380,cy=down1*1180+down2*1180;
 const zoom=k(f,[0,8,33,39,48,80,88,97,127,136,145,181],[1.06,1,1,.77,1,1,.72,1,1,.77,1,1.025]);
 return <AbsoluteFill style={{overflow:'hidden'}}><Paper/>
  <div style={{position:'absolute',left:0,top:0,width:1080,height:1920,opacity:.19,backgroundImage:'radial-gradient(#536747 1.7px, transparent 1.7px)',backgroundSize:`${40*zoom}px ${40*zoom}px`,backgroundPosition:`${-cx*zoom}px ${-cy*zoom}px`}}/>
  <div style={{position:'absolute',left:520,top:720,width:0,height:0,transform:`scale(${zoom}) translate(${-cx}px,${-cy}px)`,transformOrigin:'0 0'}}>
   <svg width="3300" height="4000" style={{position:'absolute',left:-900,top:-800,overflow:'visible'}} viewBox="-900 -800 3300 4000">
    <path d="M0 310 V845 M470 1180 H910 M1380 1490 V2025" stroke="#70845c" strokeWidth="4" fill="none" opacity=".45"/>
    {[310,845].map(y=><circle key={y} cy={y} r="9" fill={GREEN}/>)}
    <circle cx="470" cy="1180" r="9" fill={GREEN}/><circle cx="910" cy="1180" r="9" fill={GREEN}/>
    <circle cx="1380" cy="1490" r="9" fill={GREEN}/><circle cx="1380" cy="2025" r="9" fill={GREEN}/>
   </svg>
   <Node x={0} y={0}><Follower person="kurt" value="83,3 mil" label="notkurtgodel" frame={f}/></Node>
   <Node x={0} y={1180}><Views person="kurt" value="7,7 M" frame={f-43}/></Node>
   <Node x={1380} y={1180}><Follower person="elliot" value="13,5 mil" label="notelliotkay" frame={f-91}/></Node>
   <Node x={1380} y={2360}><Views person="elliot" value="4,9 M" frame={f-138}/></Node>
  </div>
  <div style={{position:'absolute',left:98,top:310,right:110,display:'flex',justifyContent:'space-between',color:GREEN,fontSize:26,fontWeight:700,letterSpacing:'.09em'}}><span>CUENTAS CON IA</span><span>{f<90?'01 / KURT':'02 / ELLIOT'}</span></div>
  <AbsoluteFill style={{background:'linear-gradient(transparent 54%,#ece9ddee 70%,#e6e3d5 100%)',pointerEvents:'none'}}/>
 </AbsoluteFill>;
};
export const CostMotion=()=>{
 const f=useCurrentFrame();const switcher=go(f,10,25);const cy=switcher*990;
 return <AbsoluteFill style={{overflow:'hidden'}}><Paper dark/>
  <div style={{position:'absolute',inset:0,transform:`translateY(${-cy}px)`}}>
   <svg width="1080" height="2100">
    <g transform="translate(525 690)">
    {Array.from({length:60},(_,i)=>{const t=i*Math.PI/30,r=210+30*q(f,i*.035,5+i*.035);return <g key={i} opacity={.3+.65*q(f,i*.035,5+i*.035)}><line x1={Math.sin(t)*180} y1={Math.cos(t)*180} x2={Math.sin(t)*r} y2={Math.cos(t)*r} stroke={CREAM} strokeWidth={i%5?1.4:3}/><circle cx={Math.sin(t)*(r+10)} cy={Math.cos(t)*(r+10)} r={i%5?2:4} fill={CREAM}/></g>})}
    <circle r="152" fill="none" stroke={CREAM} strokeWidth="2" opacity=".4"/><line y2="-112" stroke={CREAM} strokeWidth="9" strokeLinecap="round" transform={`rotate(${f*29})`}/><line y2="-70" stroke={CREAM} strokeWidth="11" strokeLinecap="round" transform={`rotate(${f*3+65})`}/><circle r="9" fill={CREAM}/>
    <path d="M0 260 V680" stroke={CREAM} strokeWidth="2" opacity=".4" strokeDasharray="5 9"/>
    </g>
   </svg>
   <div style={{position:'absolute',left:105,top:1500,width:840,textAlign:'center',...type,color:CREAM}}>
    <div style={{fontSize:42,letterSpacing:'.04em'}}>CADA INTENTO CUESTA</div>
    <svg width="840" height="300" style={{marginTop:8}} viewBox="0 0 840 300">
      {Array.from({length:12},(_,i)=>{const col=i%3,row=Math.floor(i/3);const fall=q(f,30+i*.7,40+i*.7);return <g key={i} transform={`translate(${210+col*210} ${205-row*48+fall*260})`} opacity={1-fall}>
       <path d="M-85 0 v21 c0 45 170 45 170 0 V0" fill="#bbcca7" stroke="#edf0dd" strokeWidth="2"/>
       <ellipse rx="85" ry="28" fill={CREAM} stroke="#c9d5b7" strokeWidth="3"/><text y="11" textAnchor="middle" fill={GREEN} fontFamily="Display" fontSize="34">✦</text>
      </g>})}
     </svg>

   </div>
  </div>
 </AbsoluteFill>;
};
export const GenerationMotion=()=>{
 const f=useCurrentFrame();return <AbsoluteFill style={{background:'linear-gradient(transparent 27%,#13200ccc 48%,#12200ee6 72%)'}}>
  {[0,1,2].map(n=>{const a=q(f,n*3,n*3+7);return <div key={n} style={{position:'absolute',left:98+n*292,top:615,width:260,height:330,borderRadius:15,border:'4px solid #faf5e8',overflow:'hidden',opacity:a,transform:`translateY(${90*(1-a)}px)`}}><Img src={A(`v2/${['bad-hand-still.jpg','bad-label-still.jpg','serum-still.jpg'][n]}`)} style={{width:'100%',height:'100%',objectFit:'cover'}}/><div style={{position:'absolute',top:13,right:13,width:40,height:40,borderRadius:'50%',background:n===2?GREEN:'#b04738',color:CREAM,textAlign:'center',fontSize:32}}>{n===2?'↻':'×'}</div></div>})}
 </AbsoluteFill>;
};
export const ProcessMotion=()=>{
 const f=useCurrentFrame();return <AbsoluteFill style={{background:'linear-gradient(transparent 23%,#13210c88 40%,#13210ce6 62%)',opacity:q(f,0,6)}}>
  <svg width="1080" height="1920"><path d="M180 790 H885" fill="none" stroke={CREAM} strokeWidth="4" pathLength="1" strokeDasharray="1" strokeDashoffset={1-q(f,5,42)}/></svg>
  {['idea','sistema','resultado'].map((name,n)=>{const a=q(f,n*9,n*9+10);return <div key={n} style={{position:'absolute',left:97+n*302,top:650,width:230,height:285,borderRadius:16,border:'4px solid #f8f3e7',overflow:'hidden',transform:`translateY(${60*(1-a)}px)`,opacity:a}}><Img src={A(`v2/${['01-still.jpg','serum-still.jpg','09-still.jpg'][n]}`)} style={{width:'100%',height:'100%',objectFit:'cover'}}/><div style={{position:'absolute',left:0,right:0,bottom:0,padding:'12px 0',background:n===2?GREEN:CREAM,color:n===2?CREAM:GREEN,fontSize:33,textAlign:'center',...type}}>{name}</div></div>})}
 </AbsoluteFill>;
};
export const PriceMotion=()=>{
 const f=useCurrentFrame();return <AbsoluteFill>
  <AbsoluteFill style={{background:'linear-gradient(transparent 27%,#16230c77 44%,#14220eed 68%,#14220e)',opacity:q(f,0,6)}}/>
  <div style={{position:'absolute',left:95,right:110,top:820,textAlign:'center',color:CREAM,...type}}>
   <div style={{fontSize:55,opacity:q(f,0,3)}}>Visual<span style={{color:'#ede58e'}}>.</span>Hub</div>
   <div style={{fontSize:230,marginTop:3,transform:`translateY(${80*(1-q(f,0,7))}px)`,opacity:q(f,0,3)}}>39<span style={{fontSize:105,verticalAlign:'top',display:'inline-block',marginTop:22,marginLeft:10}}>$</span></div>
   <div style={{fontSize:42,letterSpacing:'-.025em',marginTop:9,opacity:q(f,7,12),transform:`translateY(${24*(1-q(f,7,13))}px)`}}>skool.com/visual <span>↗</span></div>
  </div>
 </AbsoluteFill>;
};
