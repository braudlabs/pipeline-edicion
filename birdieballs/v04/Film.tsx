import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,Sequence,staticFile,useCurrentFrame,useVideoConfig,delayRender,continueRender,cancelRender} from 'remotion';

export const FPS=60000/1001, FRAMES=1175;
const paper='#eeeada',white='#fffdf3',lime='#d5ed91',forest='#17362c';
const clamp=(x:number,a=0,b=1)=>Math.max(a,Math.min(b,x));
const lerp=(a:number,b:number,p:number)=>a+(b-a)*p;
const out=(x:number)=>1-Math.pow(1-clamp(x),4);
const io=(x:number)=>{const p=clamp(x);return p*p*(3-2*p);};
const url=(name:string)=>staticFile('assets/'+name);

function Fonts(){
 const [handle]=useState(()=>delayRender('Birdieballs V04 fonts'));
 useEffect(()=>{Promise.all([['Birdie Sans','Sans-Regular.otf','400','normal'],['Birdie Sans','Sans-Bold.otf','700','normal'],['Birdie Editorial','Editorial-Italic.ttf','400','italic']].map(async([family,file,weight,style])=>{const font=new FontFace(family,`url(${url(file)})`,{weight,style});await font.load();document.fonts.add(font);})).then(()=>continueRender(handle)).catch(cancelRender);},[handle]);
 return null;
}

// Fit to measured V8 position, not a recovered font/alpha/easing. Age0–2 is a design extension.
export function measuredRise(seconds:number){
 const a=Math.max(0,seconds*FPS);
 return Math.exp(-.099*a)*(37.83377648725731*Math.cos(.313*a)-60.95800791408276*Math.sin(.313*a));
}
type TextProps={text:string;start:number;end:number;x?:number;y?:number;size?:number;color?:string;serif?:boolean;weight?:number;entry?:'direct'|'rise'|'left'|'right'|'measured';rotate?:number;anchor?:'start'|'middle'|'end';stroke?:boolean;outline?:string;tracking?:number;motionScale?:number};
const captionPlan:TextProps[]=[
 {text:'¿Cansado',start:1.22,end:1.66,y:1100,size:104},
 {text:'de dejarte un',start:1.66,end:2.68,y:1100,size:74},
 {text:'riñón',start:2.26,end:2.68,y:1260,size:182,serif:true,color:lime,entry:'measured'},
 {text:'en bolas',start:2.68,end:3.06,y:1100,size:104},
 {text:'cada vez',start:3.06,end:3.42,y:1100,size:104},
 {text:'que sales',start:3.42,end:3.76,y:1100,size:104},
 {text:'a jugar?',start:3.76,end:4.24,y:1100,size:104},
 {text:'venga…',start:4.44,end:4.83,x:790,y:660,size:78,serif:true,color:lime,entry:'left',rotate:-7},
 {text:'venga…',start:4.84,end:5,x:790,y:660,size:86,serif:true,color:lime,entry:'direct',rotate:-7},
 {text:'¡VENGA!',start:5,end:5.32,x:735,y:655,size:108,color:lime,entry:'rise',rotate:-7},
 {text:'¡NO!',start:6.22,end:6.61,y:1120,size:190,color:forest,outline:paper,weight:700,entry:'rise'},
 {text:'Tranquilo,',start:7.62,end:8.06,y:1460,size:100},
 {text:'mindunguis.',start:8.06,end:8.56,y:1460,size:100},
 {text:'que te traigo la',start:8.62,end:9.96,y:1460,size:74},
 {text:'solución.',start:9.34,end:9.96,y:1620,size:177,serif:true,color:lime,entry:'measured'},
 {text:'Literalmente.',start:10.74,end:11.30,y:1470,size:103,entry:'right'},
 {text:'En',start:11.48,end:11.76,y:1470,size:94},
 {text:'Birdieballs',start:11.76,end:12.30,y:1470,size:116,weight:700,entry:'rise'},
 {text:'de lagos,',start:15.08,end:15.90,y:1330,size:119,serif:true,color:lime,entry:'left'},
 {text:'de campos…',start:15.90,end:16.76,y:1370,size:119,serif:true,color:forest,outline:paper,entry:'right'},
 {text:'me cago en…',start:16.79,end:17.43,x:765,y:225,size:89,serif:true,color:forest,outline:paper,rotate:-5,entry:'rise'},
 {text:'Justo',start:18.72,end:19.45,y:1370,size:100},
 {text:'ahí.',start:19.16,end:19.45,y:1518,size:169,serif:true,color:lime,entry:'measured'},
];
export {captionPlan};

function Lettering({p,t,plain=false}:{p:TextProps;t:number;plain?:boolean}){
 if(t<p.start||t>=p.end)return null;
 const a=t-p.start,q=out(a/.15),entry=p.entry??'direct';
 const dy=entry==='measured'?measuredRise(a)*(p.motionScale??.45):entry==='rise'?(1-q)*48:0;
 const dx=entry==='left'?-(1-q)*52:entry==='right'?(1-q)*52:0;
 const opacity=entry==='direct'?1:clamp(a/.045),blur=entry==='direct'?0:(1-q)*2.5;
 return <svg viewBox="0 0 1080 1920" style={{position:'absolute',inset:0,width:'100%',height:'100%',overflow:'visible',filter:blur?`blur(${blur}px)`:undefined}}>
  <text x={p.x??540} y={p.y??1100} textAnchor={p.anchor??'middle'} fill={p.color??white} fontFamily={p.serif?'Birdie Editorial':'Birdie Sans'} fontStyle={p.serif?'italic':'normal'} fontSize={p.size??104} fontWeight={p.weight??400} letterSpacing={(p.tracking??-.04)*(p.size??104)} opacity={opacity} transform={`translate(${dx} ${dy}) rotate(${p.rotate??0} ${p.x??540} ${p.y??1100})`} stroke={plain?'none':p.outline??forest} strokeWidth={plain?0:p.outline?2.4:1.25} paintOrder="stroke" style={{filter:plain?'none':'drop-shadow(0px 3px 3px #061d2170)'}}>{p.text}</text>
 </svg>;
}

function Ball({x,y,size,rotation=0,opacity=1,blur=0}:{x:number;y:number;size:number;rotation?:number;opacity?:number;blur?:number}){
 return <Img src={url('golf-ball-photo.png')} style={{position:'absolute',left:x-size/2,top:y-size/2,width:size,height:size,transform:`rotate(${rotation}deg)`,opacity,filter:blur?`blur(${blur}px)`:undefined}}/>;
}
function Shadow({x,y,w,opacity=.3}:{x:number;y:number;w:number;opacity?:number}){
 return <div style={{position:'absolute',left:x-w/2,top:y-25,width:w,height:50,borderRadius:'50%',background:'#061812',filter:'blur(29px)',opacity}}/>;
}
function Grain(){return <svg width="1080" height="1920" style={{position:'absolute',inset:0,opacity:.12,mixBlendMode:'soft-light',pointerEvents:'none'}}><filter id="papergrain"><feTurbulence type="fractalNoise" baseFrequency=".56" numOctaves="3" seed="26" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#papergrain)"/></svg>;}

// Only the photographic objects are shutter sampled; the metrage and type remain crisp.
function ProductObjects({time,concept='C'}:{time:number;concept:string}){
 const u=time-12.30;
 if(concept==='A')return <><Shadow x={540} y={1130} w={520}/><Ball x={540} y={760} size={820} rotation={-18}/><svg viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}}>{[1,2,3].map(i=><ellipse key={i} cx="540" cy="1090" rx={i*135} ry={i*35} fill="none" stroke={lime} strokeWidth="3" opacity={.35/i}/>)}</svg></>;
 if(concept==='B')return <><Shadow x={800} y={1390} w={1050} opacity={.34}/><Ball x={860} y={690} size={1700} rotation={-35}/></>;
 // The initial photograph arrives, settles in depth, and leads a reveal of two followers.
 const arrive=out(u/.40),open=io((u-.82)/.56),handoff=io((u-1.65)/.54),exit=clamp((u-2.38)/.24);
 const main={x:lerp(1140,530,arrive)-open*190+handoff*200,y:lerp(1320,810,arrive)-open*105-handoff*40,size:lerp(1390,790,arrive)-open*70+handoff*65,rotation:lerp(42,-12,arrive)-open*14-handoff*11};
 const slide=exit*exit*1400;
 const rearOpacity=clamp((u-.96)/.16),rearTravel=out((u-.96)/.62);
 return <>
  <Shadow x={810-slide*.75} y={1025-handoff*90} w={400} opacity={.22*rearOpacity}/>
  <Ball x={lerp(1240,840,rearTravel)-slide*.75} y={lerp(730,770,rearTravel)-handoff*145} size={lerp(360,510,rearTravel)} rotation={32-handoff*28} opacity={rearOpacity} blur={1.3}/>
  <Shadow x={180-slide*.6} y={1170} w={280} opacity={.18*rearOpacity}/>
  <Ball x={lerp(-300,155,rearTravel)-slide*.6} y={1030-handoff*280} size={390} rotation={-38+rearTravel*20} opacity={rearOpacity} blur={2}/>
  <Shadow x={main.x-slide} y={1120-handoff*80} w={550} opacity={.32*(1-exit)}/>
  <Ball {...main} x={main.x-slide} y={main.y+exit*220}/>
 </>;
}
function ProductScene({t,concept='C',samples=5}:{t:number;concept?:string;samples?:number}){
 if(t<12.30||t>=14.92)return null;
 const u=t-12.30;
 const reveal=out(u/.15),leave=io((u-2.46)/.16);
 const pan=io((u-.9)/1.5);
 return <AbsoluteFill style={{opacity:1-leave,clipPath:`inset(${(1-reveal)*100}% 0 0 0)`,background:`radial-gradient(ellipse at ${35+pan*30}% 25%,#8a9870 0%,#5d7151 32%,#2b4838 67%,#102c22 100%)`}}>
  <div style={{position:'absolute',width:1750,height:1150,left:-430+pan*110,top:610,borderRadius:'50%',transform:'rotate(-22deg)',background:'linear-gradient(175deg,#d1d7b825,#061b1840)',boxShadow:'inset 0 3px 5px #f4f8c62b'}}/>
  <div style={{position:'absolute',left:-140,top:140,width:870,height:960,background:'radial-gradient(ellipse,#f9f2d32b,transparent 64%)',filter:'blur(80px)'}}/>
  <Grain/>
  <AbsoluteFill style={{isolation:'isolate'}}>{Array.from({length:samples},(_,i)=>{const sampleT=t+(i/(Math.max(1,samples-1))-.5)*.5/FPS;return <AbsoluteFill key={i} style={{opacity:1/samples,mixBlendMode:'plus-lighter'}}><ProductObjects time={sampleT} concept={concept}/></AbsoluteFill>;})}</AbsoluteFill>
  <Lettering t={t} plain p={{text:'recuperamos',start:12.30,end:12.86,y:1330,size:111,entry:'left'}}/>
  <Lettering t={t} plain p={{text:'bolas',start:12.86,end:13.70,y:1270,size:83,entry:'rise'}}/>
  <Lettering t={t} plain p={{text:'originales',start:13.16,end:13.70,y:1410,size:174,serif:true,color:lime,entry:'measured'}}/>
  <Lettering t={t} plain p={{text:'de tus',start:13.70,end:14.90,y:1265,size:75,entry:'rise'}}/>
  <Lettering t={t} plain p={{text:'marcas',start:13.94,end:14.90,y:1367,size:159,entry:'measured'}}/>
  <Lettering t={t} plain p={{text:'favoritas.',start:14.30,end:14.90,y:1495,size:164,serif:true,color:lime,entry:'rise'}}/>
 </AbsoluteFill>;
}

function Pointer({t}:{t:number}){
 if(t<18.72||t>=19.42)return null;
 const q=out((t-18.72)/.28),targetX=lerp(725,540,clamp((t-18.72)/.70)),targetY=810;
 // The arrow ends by the actual swimmer; no replacement of the action.
 return <svg viewBox="0 0 1080 1920" style={{position:'absolute',inset:0,width:'100%',height:'100%',opacity:clamp((t-18.72)/.06)}}>
  <path d={`M 680 1140 C 730 1055, ${targetX+80} 945, ${targetX} ${targetY}`} fill="none" stroke={lime} strokeWidth="5" strokeLinecap="round" pathLength="1" strokeDasharray="1" strokeDashoffset={1-q}/>
  {q>.94&&<path d={`M ${targetX-7} ${targetY+30} L ${targetX} ${targetY} L ${targetX+28} ${targetY+18}`} fill="none" stroke={lime} strokeWidth="5" strokeLinecap="round"/>}
 </svg>;
}
export function Film({concept='C',sound=true}:{concept?:string;sound?:boolean}){
 const f=useCurrentFrame(),t=f/FPS;
 return <AbsoluteFill style={{background:forest,overflow:'hidden'}}>
  <Fonts/>
  <OffthreadVideo src={url('source.mp4')} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/>
  {captionPlan.map((p,i)=><Lettering key={i} p={p} t={t}/>)}
  <Pointer t={t}/>
  <ProductScene t={t} concept={concept}/>
  {sound&&<Audio src={url('mix.wav')}/>}
 </AbsoluteFill>;
}

export function ReferenceTest(){
 const t=useCurrentFrame()/FPS;
 return <AbsoluteFill style={{background:'#16372b'}}><Fonts/><Lettering t={t} plain p={{text:'pagar',start:0,end:2,x:517,y:1184,size:409,color:'#d9ff8a',entry:'measured',motionScale:1,tracking:-29.36/409}}/></AbsoluteFill>;
}
