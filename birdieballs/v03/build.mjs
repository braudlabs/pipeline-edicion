import fs from 'node:fs/promises';
import {compactHierarchy,auditStyle} from '../../motor-editor/src/style-rules.ts';
import {auditPlan} from '../../motor-editor/src/validate.ts';
const d='birdieballs/v03',p=JSON.parse(await fs.readFile('birdieballs/v02/plan.json'));
const F=60000/1001,f=t=>Math.round(t*F),ink='#f8f5e9',accent='#e7e5b8',dark='#193329';
p.jobId='birdieballs-20s-v03';p.engineVersion='0.2.0';
const byText=(g,text)=>g.nodes.find(n=>n.text===text);
const kidney=p.graphics.find(g=>g.id==='kidney'),solution=p.graphics.find(g=>g.id==='solution'),steps=p.graphics.find(g=>g.id==='steps');
compactHierarchy(kidney.nodes,{x:540,y:p.captions.find(c=>c.text==='¿Cansado').y},accent,dark,6);
compactHierarchy(solution.nodes,{x:540,y:p.captions.find(c=>c.text==='mindunguis.').y},accent,dark,6);
// Remove the animated positional offset so the compact gap also survives arrival.
for(const g of [kidney,solution]){const lower=g.nodes[1];lower.motion={opacity:[{f:lower.start,v:0},{f:lower.start+4,v:1}]};}
compactHierarchy([byText(steps,'una'),byText(steps,'a una.')],{x:540,y:330},accent,dark,6);
byText(steps,'a una.').motion={opacity:[{f:byText(steps,'a una.').start,v:0},{f:byText(steps,'a una.').start+4,v:1}]};
const g=p.graphics.find(g=>g.id==='original-ball'),a=g.start,b=g.end;
let serial=0;g.nodes=[];
const add=(kind,props)=>{const n={id:'v03-'+serial++,kind,start:a,end:b,z:10,x:540,y:960,...props};g.nodes.push(n);return n;};
const K=values=>values.map(([t,v,ease='linear'])=>({f:a+f(t),v,ease}));
p.assets.push({id:'felt',kind:'image',src:'birdieballs/v03/felt-light.png'});
add('image',{assetId:'felt',role:'background-texture',width:1200,height:2133,z:0,motion:{x:K([[0,-28],[2.62,28]]),y:K([[0,40],[2.62,-40]])}});
// Retrieval ripples expand from the arrival point and become the camera's depth cues.
for(let i=0;i<3;i++)add('circle',{x:540,y:820,width:680+i*220,height:190+i*65,fill:'none',stroke:'#c4d29c',strokeWidth:2,z:2,motion:{scale:K([[0,.3+i*.07],[.65,1.1+i*.08,'inOut'],[1.45,1.5+i*.06],[2.62,2.6]]),opacity:K([[0,0],[.16,.24-i*.035],[1.25,.14],[2.62,0]])}});
// Ball is a 2.5D illustration. Travel, scale and focus form a three-beat action,
// not a loop or a stationary hero under changing captions.
const ball=add('image',{assetId:'ball',role:'subject',x:540,y:620,width:580,height:580,z:12,motionBlur:{samples:8,angle:270},motion:{
 x:K([[0,670,'out'],[.34,90,'inOut'],[.82,-140,'inOut'],[1.27,-235],[1.78,-210,'inOut'],[2.12,-155,'inOut'],[2.62,160]]),
 y:K([[0,650,'out'],[.34,60,'inOut'],[.82,-10,'inOut'],[1.27,80],[1.78,125,'inOut'],[2.12,95,'inOut'],[2.62,-720]]),
 scale:K([[0,.32,'out'],[.34,1.07,'inOut'],[.82,1.42,'inOut'],[1.27,.88],[1.78,.82,'inOut'],[2.12,.97,'inOut'],[2.62,3.4]]),
 rotate:K([[0,100,'out'],[.34,18],[.82,-32],[1.27,-80],[1.78,-108],[2.12,-145],[2.62,-250]]),
 blur:K([[0,9],[.24,0],[2.22,0],[2.62,8]])
}});
add('circle',{x:340,y:1010,width:450,height:70,z:3,fill:'#061c14',motion:{blur:K([[0,30]]),opacity:K([[0,0],[.34,.65],[1.78,.4],[2.4,0]]),scale:K([[0,.5],[.82,1.1],[1.78,.7],[2.62,.1]])}});
add('image',{assetId:'ball',role:'subject',x:540,y:620,width:500,height:500,z:11,start:a+f(1.22),motionBlur:{samples:8,angle:270},motion:{
 x:K([[1.22,-170,'out'],[1.63,270],[2.12,220,'inOut'],[2.62,820]]),
 y:K([[1.22,10,'out'],[1.63,60],[2.12,-20,'inOut'],[2.62,-1100]]),
 scale:K([[1.22,.18,'out'],[1.63,.82],[2.12,.95,'inOut'],[2.62,1.9]]),
 rotate:K([[1.22,-50],[1.63,14],[2.12,55],[2.62,155]]),
 opacity:K([[1.22,0],[1.34,1]]),blur:K([[1.22,12],[1.5,0],[2.22,0],[2.62,9]])
}});
const label=(text,t,until,size,y)=>add('text',{text,start:a+f(t),end:Math.min(b,a+f(until)),fontSize:size,tracking:-.045,fill:ink,y,weight:700,z:20,motion:{x:K([[t,75,'out'],[t+.16,0]]),opacity:K([[t,0],[t+.065,1]]),blur:K([[t,7,'out'],[t+.12,0]])}});
label('recuperamos',0,.56,134,1180);
const first=label('bolas',.56,1.4,82,1120),second=label('originales',.86,1.4,172,1240);
compactHierarchy([first,second],{x:540,y:1120},accent,dark,6);
const third=label('de tus',1.4,2.62,76,1120),fourth=label('marcas favoritas.',1.64,2.62,115,1240);
compactHierarchy([third,fourth],{x:540,y:1120},accent,dark,6);
// Exit carries the eye upward into the real ball falling into the lake.
g.evidence.push('Ale feedback V02: dynamic object, textured background, motion blur; compact secondary line.');
p.production={...p.production,status:'V03 awaiting user feedback',authoring:'V02 edit retained; feedback applied through reusable compactHierarchy, style audit and temporal shutter renderer.',feedback:'estilo-editor/FEEDBACK-ALE.md',motion:'2.5D ball illustration; 8 temporal samples, 270 degree shutter, deterministic procedural material.'};
p.diagnostics=[...auditPlan(p),...auditStyle(p)];if(p.diagnostics.length)throw Error(JSON.stringify(p.diagnostics));
await fs.writeFile(d+'/plan.json',JSON.stringify(p,null,2));
await fs.mkdir('motor-editor/public/birdieballs/v03',{recursive:true});await fs.copyFile(d+'/assets/felt-light.png','motor-editor/public/birdieballs/v03/felt-light.png');
console.log(JSON.stringify({frames:p.durationInFrames,graphics:p.graphics.length,diagnostics:p.diagnostics,anchor: kidney.nodes[0].y,lower:kidney.nodes[1].y}));
