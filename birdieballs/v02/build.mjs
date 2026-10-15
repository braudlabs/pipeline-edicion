import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {auditPlan} from '../../motor-editor/src/validate.ts';
const dir='birdieballs/v02',F=60000/1001,f=t=>Math.round(t*F);
const segments=[[.5,4.26],[4.44,6.58],[7.6,9.9],[10.5,22.38]];
const map=t=>{let o=0;for(const [a,b] of segments){if(t>=a-.001&&t<=b+.001)return o+t-a;o+=b-a;}throw Error('Unmapped '+t);};
const sf=t=>f(map(t)),ink='#f8f5e9',green='#173e2d',lime='#cfeb79';
const old=JSON.parse(await fs.readFile('birdieballs/v01/plan.json','utf8'));
const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-select_streams','v:0','-show_entries','stream=nb_frames','-of','json',dir+'/assets/base.mov']));
const N=+probe.streams[0].nb_frames;
const p={version:1,engineVersion:old.engineVersion,jobId:'birdieballs-20s-v02',width:1080,height:1920,fps:old.fps,durationInFrames:N,family:'braud',font:old.font,palette:{background:green,foreground:ink,accent:lime},assets:[],clips:[],captions:[],graphics:[],audio:[],decisions:[],diagnostics:[],coverage:[],provenance:old.provenance};
const asset=(id,file,kind)=>p.assets.push({id,src:'birdieballs/v02/'+file,kind});
asset('base','base.mov','video');asset('voice','voice.wav','audio');
p.clips.push({id:'base',assetId:'base',shotId:'base',start:0,end:N,sourceStart:0,crop:{scale:1,x:0,y:0},mute:true});
p.audio.push({id:'original',assetId:'voice',start:0,end:N,sourceStart:0,gain:[{f:0,v:.80},{f:N-5,v:.80},{f:N,v:0}]});
let id=0;
const motion=(at,{dy=60,scale=1,rotate=0,duration=.22}={})=>({y:[{f:at,v:dy,ease:'out'},{f:at+f(duration),v:0}],scale:[{f:at,v:scale,ease:'out'},{f:at+f(duration),v:1}],rotate:[{f:at,v:rotate,ease:'out'},{f:at+f(duration),v:0}],blur:[{f:at,v:8,ease:'out'},{f:at+f(.12),v:0}]});
function caption(text,a,b,{y=1340,size=92,x=540,animated=false,color=ink,...rest}={}){
 const start=sf(a),end=sf(b);const c={id:'c'+id++,wordIds:[],speaker:'original',start,end,text,x,y,fontSize:size,fill:color,tracking:size<100?-.025:-.045,stroke:'#153526',strokeWidth:2,...rest};
 if(animated)c.motion=motion(start,{dy:65,rotate:-3});p.captions.push(c);return c;
}
caption('¿Cansado',1.22,1.66);
caption('de dejarte un',1.66,2.68,{y:1195,size:67});
caption('riñón',2.26,2.68,{y:1340,size:210,animated:true});
caption('en bolas',2.68,3.06);
caption('cada vez',3.06,3.42);caption('que sales a jugar?',3.42,4.22,{size:90});
// Comic action breathes: no duplicate rail over the kidney flight and splash.
caption('Tranquilo,',7.62,8.06,{y:1440});caption('mindunguis.',8.06,8.56,{y:1440});
caption('que te traigo la',8.62,9.90,{size:66,y:1350});
caption('solución.',9.34,9.90,{size:176,y:1490,animated:true});
caption('Literalmente.',10.74,11.30,{size:91,y:1460});
caption('En Birdieballs',11.48,12.30,{size:96,y:1470});
caption('de lagos,',15.08,15.90,{size:116,y:1360});
caption('de campos…',15.90,16.76,{size:116,y:1360});
caption('Justo ahí.',18.72,19.38,{size:108,y:1410});
caption('01',19.62,20.54,{size:58,y:240,color:lime});
caption('limpiamos',20,20.54,{size:124,y:365,animated:true});
caption('02',20.54,21.40,{size:58,y:240,color:lime});
caption('revisamos',20.82,21.40,{size:124,y:365,animated:true});
caption('una',21.40,22.30,{size:100,y:330});
caption('a una.',21.86,22.38,{size:144,y:470,animated:true});
// Original vector ball: dimples projected onto a sphere, no borrowed reference imagery.
let dots='';for(let y=-.9;y<=.9;y+=.15){for(let x=-.9;x<=.9;x+=.15){const r=x*x+y*y;if(r>.9)continue;const z=Math.sqrt(1-r);const xx=500+x*450,yy=500+y*450;dots+=`<ellipse cx="${xx}" cy="${yy}" rx="${25*z+3}" ry="${20*z+2}" fill="url(#d)" opacity="${.45+.25*z}"/>`;}}
const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="b" cx="32%" cy="25%" r="75%"><stop stop-color="#fffef6"/><stop offset=".58" stop-color="#e9eadf"/><stop offset=".85" stop-color="#a3b4a3"/><stop offset="1" stop-color="#496352"/></radialGradient><radialGradient id="d" cx="50%" cy="70%"><stop stop-color="#fffff5"/><stop offset=".65" stop-color="#dde0d6"/><stop offset="1" stop-color="#849988"/></radialGradient><clipPath id="c"><circle cx="500" cy="500" r="456"/></clipPath></defs><circle cx="500" cy="500" r="456" fill="url(#b)"/><g clip-path="url(#c)">${dots}</g><circle cx="500" cy="500" r="454" fill="none" stroke="#f6f7e7" stroke-opacity=".35" stroke-width="3"/></svg>`;
await fs.writeFile(dir+'/assets/ball.svg',svg);asset('ball','ball.svg','image');
const start=sf(12.3),end=sf(14.92),s=map(12.3),e=map(14.92);
const nodes=[];
const node=(kind,props)=>{const n={id:'n'+id++,kind,start,end,z:10,x:540,y:960,...props};nodes.push(n);return n;};
node('circle',{x:540,y:790,width:1450,height:1450,fill:'none',stroke:'#4e7456',strokeWidth:2,motion:{scale:[{f:start,v:.65,ease:'out'},{f:start+28,v:1}]}});
node('circle',{x:540,y:790,width:1080,height:1080,fill:'none',stroke:'#4e7456',strokeWidth:2,motion:{scale:[{f:start,v:.65,ease:'out'},{f:start+32,v:1}]}});
node('circle',{x:540,y:970,width:420,height:70,fill:'#09261a',motion:{blur:[{f:start,v:28}],scale:[{f:start,v:.2},{f:start+35,v:1},{f:end-10,v:1},{f:end,v:.3}]}});
node('image',{assetId:'ball',x:540,y:710,width:540,height:540,z:12,motion:{x:[{f:start,v:680,ease:'out'},{f:sf(12.86),v:0},{f:end-15,v:0,ease:'inOut'},{f:end,v:-360}],y:[{f:start,v:420,ease:'out'},{f:sf(12.86),v:0},{f:end-15,v:0,ease:'inOut'},{f:end,v:-1200}],rotate:[{f:start,v:90,ease:'out'},{f:sf(12.86),v:0},{f:end-15,v:0},{f:end,v:-55}],blur:[{f:start,v:12},{f:start+14,v:0},{f:end-12,v:0},{f:end,v:10}]}});
const title=(text,a,b,y,size,animate=true)=>node('text',{text,start:sf(a),end:sf(b),y,fontSize:size,tracking:-.055,fill:ink,...(animate?{motion:motion(sf(a),{dy:100})}:{})});
title('recuperamos',12.3,12.86,1230,142);
title('bolas',12.86,13.70,1140,88,false);
title('originales',13.16,13.70,1290,174);
title('de tus',13.70,14.92,1140,78,false);
title('marcas favoritas.',13.94,14.92,1290,118);
p.graphics.push({id:'original-ball',clauseId:'originals',recipe:'hero',start,end,fullScreen:true,background:green,nodes,evidence:['v1-pagado: continuous identity across graphic beats','v2-churros: small premise + large semantic focus; designed graphic instead of duplicate rail']});
const cues=[['whoosh-short',12.30,.14],['click-soft',13.16,.19],['whoosh-short',14.72,.10],['click-soft',20,.13],['click-soft',20.82,.13]];
for(const name of new Set(cues.map(c=>c[0]))){await fs.copyFile('/Users/alejandrorubiocamarero/.agents/skills/media-use/audio/assets/sfx/'+name+'.mp3',dir+'/assets/'+name+'.mp3');asset(name,name+'.mp3','audio');}
for(const [name,t,gain] of cues){const at=sf(t);p.audio.push({id:'sfx'+id++,assetId:name,start:at,end:Math.min(N,at+f(.6)),sourceStart:0,gain:[{f:at,v:gain},{f:at+f(.40),v:gain},{f:at+f(.6),v:0}]});}
p.decisions=[
 ['question','accumulate','Premise held above riñón; context replaced by short readable groups.'],
 ['gag','silence','Kidney flight, splash and reaction already carry the joke.'],
 ['solution','hero','Small preparation accumulates into solución; dry Literalmente release.'],
 ['originals','hero','One ball carries three semantic beats; original vector artwork and green from packaging.'],
 ['cleaning','steps','Numbered cleaning and review synchronized to actual demonstration.']
].map(([clauseId,recipe,reason])=>({clauseId,recipe,reason,candidates:[],wordIds:[],evidence:['estilo-editor/notas/v1-pagado-A.md','estilo-editor/notas/v2-churros-A.md']}));
p.production={source:old.production.source,segments:segments.map(([sourceIn,sourceOut])=>({sourceIn,sourceOut})),authoring:'Editorially authored unified plan, rendered by the reference engine; not automatic style inference.',transcript:'Local Whisper large-v3-turbo, supplied spelling Birdieballs.',status:'proposal awaiting user review',audio:'Original mix plus five quiet local SFX cues; no copied reference soundtrack.'};
// Accumulated hierarchies belong to graphic groups, not simultaneous caption rails.
for(const [name,texts,recipe] of [['kidney',['de dejarte un','riñón'],'accumulate'],['solution',['que te traigo la','solución.'],'hero'],['steps',['01','limpiamos','02','revisamos','una','a una.'],'steps']]){
 const selected=p.captions.filter(c=>texts.includes(c.text));p.captions=p.captions.filter(c=>!texts.includes(c.text));
 p.graphics.push({id:name,clauseId:name,recipe,start:Math.min(...selected.map(c=>c.start)),end:Math.max(...selected.map(c=>c.end)),fullScreen:false,nodes:selected.map(c=>({...c,kind:'text',weight:700,z:20})),evidence:['Accumulated context and semantic emphasis; spatial separation verified in rendered stills.']});
}
const issues=auditPlan(p);if(issues.length)throw Error(JSON.stringify(issues));
await fs.writeFile(dir+'/plan.json',JSON.stringify(p,null,2));
// Alternative graphic states for internal art direction comparison; all share production font and palette.
const altB=structuredClone(p);altB.graphics[0].fullScreen=false;altB.graphics[0].nodes=nodes.filter(n=>n.kind==='text').map(n=>({...n,stroke:green,strokeWidth:2}));
const altC=structuredClone(p);const g=altC.graphics[0];g.nodes=g.nodes.filter(n=>n.kind!=='image');for(const [x,y] of [[290,660],[790,660],[540,820]])g.nodes.unshift({id:'trio'+x,kind:'image',assetId:'ball',start,end,z:11,x,y,width:340,height:340});
await fs.writeFile(dir+'/concept-b.json',JSON.stringify(altB));await fs.writeFile(dir+'/concept-c.json',JSON.stringify(altC));
for(const folder of ['motor-editor/public/birdieballs/v02','motor-editor/build/public/birdieballs/v02']){await fs.mkdir(folder,{recursive:true});for(const file of await fs.readdir(dir+'/assets')){await fs.copyFile(dir+'/assets/'+file,folder+'/'+file);}}
console.log(JSON.stringify({N,seconds:N/F,captions:p.captions.length,graphics:p.graphics.length,sounds:cues.length,graphicInterval:[s,e]}));
