import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Audio,Img,OffthreadVideo,staticFile,useCurrentFrame,delayRender,continueRender,cancelRender} from 'remotion';
export const FPS=60000/1001,FRAMES=2278;
const cream='#fffdf1',accent='#dcf395',ink='#18382b';
const clamp=(v:number)=>Math.max(0,Math.min(1,v)),mix=(a:number,b:number,p:number)=>a+(b-a)*p;
const ease=(x:number)=>1-Math.pow(1-clamp(x),4);
const smooth=(x:number)=>{let p=clamp(x);return p*p*(3-2*p)};
const asset=(s:string)=>staticFile('assets/'+s);
function Fonts(){const[h]=useState(()=>delayRender('V06 SF Pro'));useEffect(()=>{Promise.all([['SF Birdie','Sans-Regular.otf','400'],['SF Birdie','Sans-Bold.otf','700'],['Birdie Condensed','Condensed.ttf','400']].map(async([family,f,weight])=>{const face=new FontFace(family,`url(${asset(f)})`,{weight});await face.load();document.fonts.add(face)})).then(()=>continueRender(h)).catch(cancelRender)},[h]);return null}
type Cue={id:string;text:string;start:number;end:number;x:number;y:number;size:number;weight?:number;color?:string;entry?:'up'|'left'|'right'|'settle'|'snap'|'reveal';anchor?:'start'|'middle'|'end';tracking?:number;condensed?:boolean;rotate?:number;exit?:number;masked?:boolean;outline?:boolean;move?:{at:number;duration:number;x?:number;y?:number;size?:number}};
export const cues:Cue[]=[
 {id:'cansado',text:'¿Cansado',start:1.22,end:1.66,x:540,y:1090,size:138,entry:'left',exit:0},
 {id:'dejarte',text:'de dejarte un',start:1.66,end:3.07,x:540,y:1090,size:96,entry:'snap',exit:.04},
 {id:'rinon',text:'RIÑÓN',start:2.26,end:3.07,x:540,y:1350,size:253,weight:700,color:accent,tracking:-.062,entry:'settle',exit:.04},
 {id:'bolas-hook',text:'en bolas',start:2.68,end:3.07,x:210,y:1435,size:93,anchor:'start',entry:'right',exit:.04},
 {id:'cada',text:'cada vez',start:3.06,end:4.24,x:210,y:1100,size:94,anchor:'start',entry:'left'},
 {id:'sales',text:'que sales',start:3.42,end:4.24,x:210,y:1240,size:158,weight:700,anchor:'start',entry:'up'},
 {id:'jugar',text:'a jugar?',start:3.76,end:4.24,x:210,y:1390,size:163,weight:700,color:accent,anchor:'start',entry:'right'},
 {id:'venga1',text:'venga…',start:4.44,end:4.84,x:778,y:1140,size:86,entry:'left',exit:0},
 {id:'venga2',text:'venga…',start:4.84,end:5.00,x:778,y:1140,size:99,entry:'snap',exit:0},
 {id:'venga3',text:'¡VENGA!',start:5.00,end:5.34,x:740,y:1140,size:116,weight:700,color:accent,entry:'snap',exit:.07},
 {id:'no',text:'¡NO!',start:6.22,end:6.63,x:540,y:1140,size:335,condensed:true,color:ink,tracking:-.025,entry:'settle',exit:.09},
 {id:'tranquilo',text:'Tranquilo,',start:7.62,end:8.06,x:545,y:1410,size:118,entry:'right',exit:.015},
 {id:'mindunguis',text:'mindunguis.',start:8.06,end:8.59,x:545,y:1410,size:137,weight:700,entry:'up',exit:.04},
 {id:'traigo',text:'que te traigo la',start:8.62,end:9.97,x:92,y:355,size:79,anchor:'start',entry:'left',exit:.08},
 {id:'solucion',text:'SOLUCIÓN',start:9.34,end:9.97,x:540,y:570,size:207,weight:700,color:accent,tracking:-.06,entry:'up',masked:true,exit:.08},
 {id:'solucion-outline',text:'SOLUCIÓN',start:9.34,end:9.97,x:540,y:570,size:207,weight:700,color:accent,tracking:-.06,entry:'up',outline:true,exit:.08},
 {id:'literal',text:'Literalmente.',start:10.74,end:11.31,x:540,y:1480,size:125,weight:700,entry:'snap',exit:.06},
 {id:'brand-en',text:'En',start:11.48,end:11.76,x:150,y:1430,size:93,anchor:'start',entry:'up',exit:0},
 {id:'brand',text:'Birdieballs.',start:11.76,end:12.30,x:150,y:1430,size:130,weight:700,anchor:'start',entry:'left',exit:.035},
 {id:'recuperamos',text:'recuperamos',start:12.30,end:12.86,x:540,y:650,size:140,entry:'left',exit:.025},
 {id:'bolas-product',text:'bolas',start:12.86,end:13.70,x:115,y:565,size:96,anchor:'start',entry:'up',exit:.03},
 {id:'originales',text:'ORIGINALES',start:13.16,end:13.70,x:100,y:755,size:157,weight:700,color:accent,anchor:'start',tracking:-.055,entry:'reveal',exit:.03},
 {id:'detus',text:'de tus',start:13.70,end:14.89,x:890,y:600,size:90,anchor:'end',entry:'right',exit:.05},
 {id:'marcas',text:'marcas',start:13.94,end:14.89,x:890,y:755,size:197,weight:700,anchor:'end',entry:'left',exit:.05},
 {id:'favoritas',text:'favoritas.',start:14.30,end:14.89,x:890,y:890,size:144,weight:700,color:accent,anchor:'end',entry:'up',exit:.05},
 {id:'de-lagos',text:'de',start:15.08,end:15.90,x:180,y:1240,size:89,anchor:'start',entry:'left',exit:.02},
 {id:'lagos',text:'LAGOS,',start:15.24,end:15.90,x:180,y:1430,size:210,weight:700,color:cream,anchor:'start',entry:'up',exit:.02},
 {id:'de-campos',text:'de',start:15.90,end:16.76,x:915,y:1240,size:89,color:cream,anchor:'end',entry:'right',exit:.05},
 {id:'campos',text:'CAMPOS…',start:16.00,end:16.76,x:915,y:1390,size:173,weight:700,color:cream,anchor:'end',entry:'left',exit:.05},
 {id:'mecago',text:'me cago en…',start:16.79,end:17.44,x:600,y:1440,size:108,entry:'left',exit:.06},
 {id:'justo',text:'Justo',start:18.72,end:19.16,x:540,y:1330,size:126,entry:'up',exit:0},
 {id:'ahi',text:'Justo ahí.',start:19.16,end:19.47,x:540,y:1330,size:145,weight:700,entry:'snap',exit:.08},
 {id:'las-limpieza',text:'Las',start:19.62,end:20.54,x:540,y:390,size:86,entry:'up',exit:.025},
 {id:'limpiamos',text:'limpiamos',start:20.00,end:20.54,x:540,y:540,size:156,weight:700,entry:'left',exit:.025},
 {id:'y-las',text:'y las',start:20.54,end:21.40,x:540,y:390,size:86,entry:'snap',exit:.025},
 {id:'revisamos',text:'revisamos',start:20.82,end:21.40,x:540,y:540,size:150,weight:700,entry:'right',exit:.025},
 {id:'una1',text:'una',start:21.40,end:22.34,x:340,y:530,size:158,weight:700,color:accent,entry:'left',exit:.07},
 {id:'a-una',text:'a',start:21.86,end:22.34,x:540,y:530,size:98,entry:'snap',exit:.07},
 {id:'una2',text:'una.',start:22.06,end:22.34,x:747,y:530,size:158,weight:700,color:accent,entry:'right',exit:.07},
 {id:'al-punto',text:'Al punto de que',start:22.42,end:23.12,x:540,y:1480,size:113,entry:'left',exit:.025},
 {id:'ni-el',text:'ni el',start:23.12,end:24.10,x:120,y:1300,size:88,anchor:'start',entry:'up',exit:.035},
 {id:'mindunguis2',text:'mindunguis este',start:23.36,end:24.10,x:120,y:1455,size:112,weight:700,anchor:'start',entry:'right',exit:.035},
 {id:'se-da-cuenta',text:'se da cuenta',start:24.10,end:24.62,x:540,y:1455,size:127,entry:'left',exit:.02},
 {id:'no-son',text:'de que no son',start:24.62,end:25.58,x:540,y:1315,size:95,entry:'up',exit:.06},
 {id:'nuevas',text:'nuevas.',start:25.16,end:25.58,x:540,y:1500,size:209,weight:700,color:accent,entry:'settle',exit:.06}
,
 {id:'pues-si',text:'Pues sí que están',start:25.68,end:26.16,x:540,y:1390,size:105,entry:'snap',exit:.02},
 {id:'como-nuevas-dialogo',text:'como nuevas,',start:26.16,end:27.04,x:540,y:1390,size:144,weight:700,entry:'left',exit:.05},
 {id:'si-remate',text:'sí.',start:26.88,end:27.04,x:765,y:1520,size:90,entry:'snap',exit:.05},
 {id:'tu-lo-has-dicho',text:'Tú lo has dicho.',start:27.34,end:28.06,x:540,y:1450,size:123,entry:'up',exit:.06},
 {id:'como-nuevas-oferta',text:'Como nuevas',start:28.20,end:28.80,x:540,y:330,size:117,weight:700,entry:'left',exit:.02},
 {id:'hasta-un',text:'y hasta un',start:28.80,end:30.16,x:540,y:330,size:114,entry:'right',exit:.035},
 {id:'mas-baratas',text:'más baratas.',start:30.16,end:30.99,x:540,y:1680,size:131,weight:700,entry:'up',exit:.07},
 {id:'no-esperes',text:'No esperes más',start:31.16,end:31.86,x:540,y:1460,size:118,entry:'left',exit:.02},
 {id:'y-pide',text:'y pide',start:31.86,end:32.72,x:540,y:1315,size:93,entry:'up',exit:.06},
 {id:'las-tuyas',text:'las tuyas.',start:32.22,end:32.72,x:540,y:1485,size:173,weight:700,color:accent,entry:'right',exit:.06},
 {id:'que-el-golf',text:'Que el golf',start:32.92,end:33.44,x:750,y:1250,size:103,entry:'left',exit:.02},
 {id:'esta-para',text:'está para',start:33.44,end:34.53,x:520,y:1300,size:94,entry:'up',exit:.04},
 {id:'disfrutarlo',text:'disfrutarlo,',start:33.90,end:34.53,x:520,y:1475,size:172,weight:700,color:accent,entry:'left',exit:.04},
 {id:'chaval',text:'chaval.',start:34.62,end:35.08,x:730,y:1435,size:131,weight:700,entry:'snap',exit:.08},
 {id:'birdie-end',text:'Birdieballs.',start:35.52,end:36.06,x:540,y:1010,size:140,weight:700,entry:'up',exit:.06},
 {id:'juega-mas',text:'Juega más,',start:36.12,end:37.95,x:540,y:860,size:145,entry:'left',exit:.10},
 {id:'por-menos',text:'por menos.',start:36.88,end:37.95,x:540,y:1040,size:173,weight:700,color:accent,entry:'up',exit:.10}
];
function pose(c:Cue,t:number){const age=t-c.start,q=ease(age/.18);let x=c.x,y=c.y,size=c.size;
 if(c.move){const p=smooth((t-c.move.at)/c.move.duration);x=mix(x,c.move.x??x,p);y=mix(y,c.move.y??y,p);size=mix(size,c.move.size??size,p)}
 const mode=c.entry??'up';if(mode==='left')x-=65*(1-q);if(mode==='right')x+=65*(1-q);if(mode==='up')y+=74*(1-q);if(mode==='settle'){const a=Math.max(0,age*FPS);y+=Math.exp(-.16*a)*(65*Math.cos(.33*a)-32*Math.sin(.33*a))}
 let alpha=mode==='snap'?1:clamp(age/.035);if(c.exit)alpha*=clamp((c.end-t)/c.exit);return{x,y,size,alpha,q};}
function Letter({c,t,mask,uid}:{c:Cue;t:number;mask:string|null;uid:number}){if(t<c.start||t>=c.end)return null;const p=pose(c,t);const nativeFrame=Math.round(t*FPS);const onBrightSky=['recuperamos','bolas-product','originales'].includes(c.id)&&nativeFrame>=757&&nativeFrame<794;const color=c.color;const dark=color===ink;const contrast=onBrightSky||['lagos','de-lagos','campos','de-campos'].includes(c.id);return <g transform={onBrightSky?'translate(0 -200)':undefined} opacity={p.alpha} mask={c.masked&&mask?`url(#subject-mask-${uid})`:undefined} clipPath={c.entry==='reveal'?`url(#reveal-${c.id}-${uid})`:undefined}>
 {c.entry==='reveal'&&<clipPath id={`reveal-${c.id}-${uid}`}><rect x="60" y="480" width={970*p.q} height="400"/></clipPath>}
 <text x={p.x} y={p.y} textAnchor={c.anchor??'middle'} fontFamily={c.condensed?'Birdie Condensed':'SF Birdie'} fontSize={p.size} fontWeight={c.weight??400} letterSpacing={p.size*(c.tracking??-.048)} fill={c.outline?'none':color??cream} stroke={c.outline?(color??cream):dark?'#fffdec':ink} strokeWidth={c.outline?2.6:dark?1.5:contrast?2:.65} paintOrder="stroke" style={{filter:c.outline?'none':dark?'drop-shadow(0px 1px 2px #f1ecd255)':contrast?'drop-shadow(0px 2px 4px #082019df)':'drop-shadow(0px 2px 3px #082019b0)'}}>{c.text}</text>
 </g>}
export function Film({blur=.32,sound=true}:{blur?:number;sound?:boolean}){
 const frame=useCurrentFrame(),t=frame/FPS;const mask=frame>=550&&frame<=599?asset(`masks/${String(frame).padStart(4,'0')}.png`):null;const active=cues.filter(c=>t>=c.start-1/FPS&&t<c.end+1/FPS);
 const samples=blur>0?5:1;
 return <AbsoluteFill style={{background:ink,overflow:'hidden'}}><Fonts/><OffthreadVideo src={asset('source.mp4')} muted style={{width:'100%',height:'100%',objectFit:'cover'}}/>
 {mask&&<Img src={mask} style={{position:'absolute',width:1,height:1,opacity:0}}/>}
 {/* Restrained local exposure, confined to the typographic moment; never a subtitle band. */}
 {t>=2.26&&t<3.07&&<AbsoluteFill style={{background:'radial-gradient(ellipse 500px 310px at 540px 1180px,#0b261626,transparent)',opacity:Math.min(clamp((t-2.26)/.1),clamp((3.07-t)/.08))}}/>}
 <AbsoluteFill style={{isolation:'isolate'}}>{Array.from({length:samples},(_,i)=>{const sample=t+(samples===1?0:(i/(samples-1)-.5)*blur/FPS);return <svg key={i} viewBox="0 0 1080 1920" style={{position:'absolute',width:'100%',height:'100%',inset:0,opacity:1/samples,mixBlendMode:'plus-lighter'}}>
 <defs><filter id={`invert-${i}`}><feComponentTransfer><feFuncR type="linear" slope="-1" intercept="1"/><feFuncG type="linear" slope="-1" intercept="1"/><feFuncB type="linear" slope="-1" intercept="1"/></feComponentTransfer></filter><mask id={`subject-mask-${i}`} maskUnits="userSpaceOnUse" x="0" y="0" width="1080" height="1920" style={{maskType:'luminance'}}><rect width="1080" height="1920" fill="white"/>{mask&&<image href={mask} width="1080" height="1920" filter={`url(#invert-${i})`}/>}</mask></defs>
 {active.map(c=><Letter key={c.id} c={c} t={sample} mask={mask} uid={i}/>)}
 </svg>})}</AbsoluteFill>
 {sound&&<Audio src={asset('mix.wav')}/>}</AbsoluteFill>;
}
