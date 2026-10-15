import React from 'react';
const clamp=(x:number)=>Math.max(0,Math.min(1,x));
const ease=(x:number)=>1-(1-clamp(x))**3;
const smooth=(x:number)=>{x=clamp(x);return x*x*(3-2*x)};
export const WAITING_IN=480,WAITING_OUT=551; // 10.000–11.479s, original picture/audio clock untouched.
const flips=[{at:12,d:8},{at:23,d:7},{at:32,d:6},{at:39,d:5},{at:45,d:4},{at:50,d:4}];
function Paper({number,back=false}:{number:number;back?:boolean}){return <div style={{position:'absolute',inset:0,background:'linear-gradient(112deg,#faf3df,#ede4cf 74%,#d9cdb4)',border:'1px solid #d8cfbc',borderRadius:12,backfaceVisibility:'hidden',transform:back?'rotateX(180deg)':undefined,overflow:'hidden'}}>
 <svg width="100%" height="100%" viewBox="0 0 470 340" style={{position:'absolute',inset:0}}><defs><filter id={'paper-'+number+(back?'b':'f')}><feTurbulence baseFrequency=".74" numOctaves="2" seed="6" type="fractalNoise"/></filter></defs><rect width="470" height="340" opacity=".11" filter={`url(#paper-${number+(back?'b':'f')})`}/><path d="M24 65 H446" stroke="#a2a59b" strokeWidth="1.2" strokeDasharray="4 5"/><path d="M26 312H443" stroke="#d2c8b3"/><circle cx="92" cy="26" r="10" fill="#1a373a"/><circle cx="378" cy="26" r="10" fill="#1a373a"/>{!back&&<><text x="235" y="255" textAnchor="middle" fill="#153940" fontFamily="AndromedaSF" fontWeight="700" fontSize="237" letterSpacing="-15">{String(number).padStart(2,'0')}</text>{Array.from({length:7},(_,i)=><rect key={i} x={159+i*23} y={291} width={15} height={4} rx={2} fill={i<number?'#806990':'#bcbcaf'}/>)}</>}</svg>
 </div>}
function Calendar({age}:{age:number}){
 const active=flips.findIndex(f=>age>=f.at&&age<f.at+f.d);
 const completed=flips.filter(f=>age>=f.at+f.d).length;
 const next=active>=0?active+2:completed+1;
 const kick=active>=0?Math.sin(clamp((age-flips[active].at)/flips[active].d)*Math.PI):0;
 return <div style={{position:'relative',width:470,height:340,perspective:1100,transform:`rotateY(-11deg) rotateZ(3deg) translateY(${-2*kick}px)`,transformStyle:'preserve-3d'}}>
  {[5,4,3,2,1].map(i=><div key={i} style={{position:'absolute',inset:0,borderRadius:12,background:i===5?'#173941':'#d7cbb4',border:'1px solid #bdb6a5',transform:`translateY(${i*4}px) translateZ(${-i*1.5}px)`,boxShadow:i===5?'14px 24px 30px #172c3240':undefined}}/>)}
  <Paper number={Math.min(7,next)}/>
  {active>=0&&(()=>{const f=flips[active];const p=smooth((age-f.at)/f.d);return <div style={{position:'absolute',inset:0,transformOrigin:'50% 30px',transform:`translateZ(2px) rotateX(${-178*p}deg)`,transformStyle:'preserve-3d',filter:`blur(${Math.sin(Math.PI*p)*1.8}px)`}}><Paper number={active+1}/><Paper number={active+1} back/></div>})()}
  <svg width="470" height="90" style={{position:'absolute',top:-18,left:0,transform:'translateZ(9px)',overflow:'visible'}}><defs><linearGradient id="binder" x1="0" x2="1"><stop stopColor="#667a78"/><stop offset=".38" stopColor="#f9f7e7"/><stop offset=".62" stopColor="#a3aead"/><stop offset="1" stopColor="#415a5e"/></linearGradient></defs>{[92,378].map(x=><g key={x}><path d={`M${x-5} 50V20C${x-5} 0 ${x+10} 0 ${x+10} 20V41`} fill="none" stroke="#17333770" strokeWidth="11" transform="translate(3 3)"/><path d={`M${x-5} 50V20C${x-5} 0 ${x+10} 0 ${x+10} 20V41`} fill="none" stroke="url(#binder)" strokeWidth="7"/></g>)}</svg>
 </div>
}
function Grid({age}:{age:number}){const selected=Math.min(20,Math.floor(Math.max(0,age-8)/2.5));return <div style={{width:470,height:340,background:'#14343a',borderRadius:20,padding:26,boxSizing:'border-box',boxShadow:'10px 24px 35px #0f252b50',transform:'rotateY(-12deg) rotateZ(3deg)',display:'grid',gridTemplateColumns:'repeat(7,1fr)',gap:10}}>{Array.from({length:21},(_,i)=><div key={i} style={{display:'grid',placeItems:'center',color:i===selected?'#fffbed':'#aabbb7',fontSize:32,borderRadius:40,background:i===selected?'#9678b4':'transparent',transform:`scale(${i===selected?1.12:1})`,fontFamily:'AndromedaSF'}}>{i+1}</div>)}</div>}
function Clock({age}:{age:number}){return <svg width="470" height="340" viewBox="0 0 470 340" style={{filter:'drop-shadow(12px 24px 16px #172c3240)'}}><defs><radialGradient id="dial"><stop stopColor="#fffbed"/><stop offset="1" stopColor="#d6d8cc"/></radialGradient></defs><circle cx="235" cy="170" r="154" fill="#18383c"/><circle cx="235" cy="170" r="141" fill="url(#dial)"/>{Array.from({length:12},(_,i)=><path key={i} d="M235 39V53" stroke="#17383e" strokeWidth="4" transform={`rotate(${i*30} 235 170)`}/>)}<path d="M235 170V76" stroke="#18383c" strokeWidth="8" strokeLinecap="round" transform={`rotate(${age*21} 235 170)`}/><path d="M235 170H304" stroke="#9874ae" strokeWidth="12" strokeLinecap="round" transform={`rotate(${age*2} 235 170)`}/><circle cx="235" cy="170" r="9" fill="#18383c"/></svg>}
export function WaitingMotion({frame,variant='A'}:{frame:number;variant?:string}){
 if(frame<WAITING_IN||frame>=WAITING_OUT)return null;
 const age=frame-WAITING_IN;const entry=ease(age/9);const exit=smooth((age-61)/10);
 return <div style={{position:'absolute',left:500,top:286,width:470,height:340,perspective:1400,transformOrigin:'50% 30%',transform:`translateY(${42*(1-entry)-90*exit}px) scale(${.91+.09*entry-.08*exit})`,opacity:entry*(1-exit)}}>{variant==='A'?<Calendar age={age}/>:variant==='B'?<Grid age={age}/>:<Clock age={age}/>}</div>
}
