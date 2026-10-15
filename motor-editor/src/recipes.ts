import type {RecipeId,Clause,Word,Job,Graphic,Node,Shot,Motion} from './types.ts';
import {frameAt,fpsValue,rise,pulse} from './motion.ts';
import {fitText} from './text.ts';
import {compactHierarchy} from './style-rules.ts';
export const catalog:Record<RecipeId,{label:string;fullScreen:boolean;minimum:number;evidence:string[];status:string}>={
 rail:{label:'Palabra ordinaria',fullScreen:false,minimum:0,evidence:['v6-ads90-C','landing-A'],status:'observed'},
 accumulate:{label:'Acumulación por beats',fullScreen:false,minimum:.5,evidence:['v1-pagado-A','landing-A'],status:'adaptation'},
 hero:{label:'Foco tipográfico',fullScreen:false,minimum:.3,evidence:['v1-pagado-A','v6-ads90-C'],status:'adaptation'},
 'masked-hero':{label:'Relleno tras oclusores, contorno opcional delante',fullScreen:false,minimum:.3,evidence:['v1-pagado-A','landing-B'],status:'observed-layer-order'},
 pulse:{label:'Título con estados de parpadeo',fullScreen:false,minimum:.3,evidence:['v6-ads90-rev-A'],status:'measured-states-60fps'},
 price:{label:'Cifra y unidad con entrada escalonada',fullScreen:true,minimum:1,evidence:['v1-pagado-A'],status:'adaptation'},
 count:{label:'Contador radial y frenada discreta',fullScreen:true,minimum:1.2,evidence:['v1-pagado-A'],status:'measured-counter/adapted-layout'},
 comparison:{label:'Desplazamiento entre conceptos',fullScreen:true,minimum:1.4,evidence:['v2-churros-A'],status:'observed-sequence/adapted-curves'},
 proof:{label:'Prueba visual revelada por partes',fullScreen:true,minimum:1.1,evidence:['landing-A'],status:'observed-sequence/adapted-regions'},
 steps:{label:'Proceso espacial y cámara por etapas',fullScreen:true,minimum:2,evidence:['lafabrica-v2p1-B'],status:'adaptation-not-replica'},
 carousel:{label:'Recursos en perspectiva y foco sucesivo',fullScreen:true,minimum:1.5,evidence:['v6-ads90-B','landing-C'],status:'adaptation'},
 silence:{label:'Pausa visual explícita',fullScreen:false,minimum:0,evidence:['v6-ads90-B'],status:'explicit-editorial-choice'}
};
export function eligible(id:RecipeId,c:Clause,words:Word[],shot:Shot|undefined):string|undefined{
 if(id==='masked-hero'&&!shot?.cutoutAssetId)return 'Necesita recorte alpha sincronizado del sujeto/objetos';
 if(['hero','masked-hero','pulse'].includes(id)&&!c.focusWordIds?.length)return 'Necesita foco verbal';
 if(id==='price'&&!c.data?.amount)return 'Necesita importe explícito';
 if(id==='count'&&c.data?.value===undefined)return 'Necesita cantidad verificable';
 if(id==='comparison'&&!c.data?.comparison)return 'Necesita dos conceptos del guion';
 if(id==='steps'&&(!c.data?.steps||c.data.steps.length<2))return 'Necesita al menos dos etapas explícitas';
 if(id==='proof'&&(!c.data?.assetIds?.length||!c.data.proofRegions?.length))return 'Necesita prueba y regiones de revelado';
 if(id==='carousel'&&(c.data?.assetIds?.length??0)<2)return 'Necesita al menos dos recursos';
 if(id==='accumulate'&&words.length>8)return 'Frase demasiado larga para acumulación';
 return undefined;
}
export function makeGraphic(id:RecipeId,c:Clause,words:Word[],job:Job,shot:Shot|undefined,start:number,end:number,palette:{background:string;foreground:string;accent:string}):Graphic{
 const W=job.format.width,H=job.format.height,F=fpsValue(job.format.fps),duration=end-start;
 const nodes:Node[]=[];let serial=0;const px=(v:number)=>v*W,py=(v:number)=>v*H;
 const first=(wid:string)=>frameAt(words.find(w=>w.id===wid)!.start,job.format.fps);
 const time=(t:number)=>Math.min(end-1,start+Math.round(t*duration));
 const add=(n:Omit<Node,'id'|'start'|'end'|'z'> & Partial<Pick<Node,'start'|'end'|'z'>>)=>{const node={id:`${c.id}:n${serial++}`,start,end,z:20,...n};nodes.push(node);return node;};
 const text=(s:string,x:number,y:number,max:number,at=start,width=.86,weight=700)=>add({kind:'text',text:s,x:px(x),y:py(y),fontSize:fitText(s,px(width),px(max),weight===400?-.02:-.06,weight),weight,tracking:weight===400?-.02:-.06,fill:palette.foreground,start:at,motion:rise(at,Math.min(Math.round(.4*F),end-at-1),py(.025))});
 const evidence=catalog[id].evidence.map(x=>`estilo-editor/notas/${x}.md`);
 const g:Graphic={id:`${c.id}:graphic`,clauseId:c.id,recipe:id,start,end,fullScreen:catalog[id].fullScreen,background:catalog[id].fullScreen?palette.background:undefined,nodes,evidence};
 const focus=words.filter(w=>c.focusWordIds?.includes(w.id));
 if(id==='hero'||id==='masked-hero'||id==='pulse'){
  const at=Math.max(start,first(focus[0].id));const hero=text(focus.map(w=>w.text).join(' '),.5,id==='masked-hero'?.46:(shot?.anchor?.[1]??job.options?.captionY??.56),.42,at,.76);hero.wordIds=focus.map(w=>w.id);
  if(id==='hero'){
   const context=words.filter(w=>!focus.includes(w));
   if(context.length){const railMeasure={...hero,text:context.map(w=>w.text).join(' '),fontSize:job.options?.fontSize??W*.095};compactHierarchy([railMeasure,hero],{x:shot?.anchor?.[0]?shot.anchor[0]*W:W/2,y:hero.y},palette.accent,palette.background,W*.0074);}
  }
  if(id==='pulse')hero.motion=pulse(at,F);
  if(id==='masked-hero'){
   g.cutout={assetId:shot!.cutoutAssetId!,shotId:shot!.id,fillZ:25};
   if(c.outline){const {id:unused,...copy}=hero;add({...copy,kind:'text',z:30,fill:'none',stroke:palette.foreground,strokeWidth:px(.0018),wordIds:undefined});}
  }
 }else if(id==='accumulate'){
  for(let i=0;i<words.length;i++){const at=first(words[i].id),until=i+1<words.length?first(words[i+1].id):end;const n=text(words.slice(0,i+1).map(w=>w.text).join(' '),.5,job.options?.captionY??.56,.095,at);n.end=until;n.motion=undefined;n.wordIds=[words[i].id];}
 }else if(id==='price'){
  const amount=c.data!.amount!;const match=words.find(w=>w.text.includes(amount)||/\d/.test(w.text));const at=match?first(match.id):time(.24);
  const prefix=c.data?.prefix??words.filter(w=>w.start<(match?.start??words[0].start)).map(w=>w.text).join(' ');
  if(prefix)text(prefix,.5,.34,.095,start);
  text(amount,.5,.49,.38,Math.min(at,end-2));
  const label=c.data?.label??words.filter(w=>w.start>(match?.start??words.at(-1)!.start)).map(w=>w.text).join(' ');
  if(label)text(label,.5,.66,.105,Math.min(end-1,at+Math.round(.25*F)));
  g.camera={scale:[{f:start,v:1},{f:end,v:1.04}]};
 }else if(id==='count'){
  const at=c.focusWordIds?.length?first(c.focusWordIds[0]):time(.1);const value=c.data!.value!;
  const radius=px(.32);
  for(let i=0;i<40;i++){const angle=i/40*Math.PI*2;add({kind:'line',x:W/2+Math.cos(angle)*radius,y:H*.43+Math.sin(angle)*radius,width:px(.025),height:0,stroke:palette.accent,strokeWidth:px(.0012),motion:{rotate:[{f:start,v:angle*180/Math.PI}],opacity:[{f:start,v:0},{f:Math.min(end-1,at),v:.6}]},z:10});}
  if(c.data?.prefix)text(c.data.prefix,.5,.22,.095,start);
  const n=text(`${value}${c.data?.suffix??''}`,.5,.43,.42,at);n.counter={target:value,prefix:'',suffix:c.data?.suffix??'',start:at,duration:Math.max(1,Math.round(F*9/24))};
  if(c.data?.label)text(c.data.label,.5,.64,.105,Math.min(end-1,at+Math.round(F*5/24)));
 }else if(id==='comparison'){
  const labels=c.data!.comparison!;const changeWord=words.find(w=>w.text.toLocaleLowerCase().includes(labels[1].toLocaleLowerCase()));const mid=changeWord?first(changeWord.id):time(.52);
  labels.forEach((label,i)=>{const n=text(label,.5+i,.47,.19,start,.82);n.motion=undefined;add({kind:'line',x:W*(.2+i),y:H*.57,width:W*.6,height:0,stroke:palette.accent,strokeWidth:px(.006)});});
  g.camera={x:[{f:start,v:0},{f:Math.max(start+1,mid-Math.round(.25*F)),v:0,ease:'inOut'},{f:Math.min(end-1,mid+Math.round(.2*F)),v:-W}]};
 }else if(id==='proof'){
  const assetId=c.data!.assetIds![0],asset=job.assets.find(a=>a.id===assetId)!;
  const ratio=(asset.width??1)/(asset.height??1),width=Math.min(W*.8,H*.72*ratio),height=width/ratio;
  const regions=c.data!.proofRegions!;
  regions.forEach((region,i)=>{const at=region.atWordId?first(region.atWordId):time(i/regions.length*.65);add({kind:'image',assetId,x:W/2,y:H*.5,width,height,crop:region.rect,start:at,motion:rise(at,Math.min(Math.round(.28*F),end-at-1),H*.012)});});
 }else if(id==='steps'){
  const labels=c.data!.steps!,spacing=W*.95;
  labels.forEach((label,i)=>{const cx=W/2+i*spacing;add({kind:'circle',x:cx,y:H*.35,width:W*.23,height:W*.23,fill:palette.accent,z:10});text(String(i+1),cx/W,.35,.14,start,.3).fill=palette.background;const t=text(label,cx/W,.55,.12,start,.8);t.motion=undefined;if(i<labels.length-1)add({kind:'line',x:cx+W*.13,y:H*.35,width:spacing-W*.26,height:0,stroke:palette.accent,strokeWidth:W*.003,z:5});});
  g.camera={x:[{f:start,v:0}]};
  for(let i=1;i<labels.length;i++){const at=start+Math.round(i*duration/labels.length);g.camera.x!.push({f:Math.max(start+1,at-Math.round(F*.2)),v:-(i-1)*spacing,ease:'inOut'},{f:Math.min(end-1,at+Math.round(F*.2)),v:-i*spacing});}
 }else if(id==='carousel'){
  const ids=c.data!.assetIds!,spacing=W*.73;
  ids.forEach((assetId,i)=>{const asset=job.assets.find(a=>a.id===assetId)!,ratio=(asset.width??1)/(asset.height??1);const width=Math.min(W*.65,H*.62*ratio);const n=add({kind:'image',assetId,x:W*.5+i*spacing,y:H*.5,width,height:width/ratio,z:20+i});n.motion={rotateY:[{f:start,v:-12},{f:end-1,v:12}]};});
  g.camera={x:[{f:start,v:0}]};
  for(let i=1;i<ids.length;i++){const at=start+Math.round(i*duration/ids.length);g.camera.x!.push({f:Math.max(start+1,at-Math.round(F*.25)),v:-(i-1)*spacing,ease:'inOut'},{f:Math.min(end-1,at+Math.round(F*.25)),v:-i*spacing});}
 }
 if(id==='price'){const lines=nodes.filter(n=>n.kind==='text');if(lines.length>1)compactHierarchy(lines,{x:W/2,y:lines[0].y},palette.accent,palette.background,W*.0074);}
 if(g.fullScreen&&nodes.length)nodes[0].wordIds=words.map(w=>w.id); // Semantic representation of this clause, recorded in decision trace.
 // Keyframes are always ordered; coincident keys take the latest explicit state.
 const clean=(m:Motion|undefined)=>{if(m)for(const track of Object.values(m)){const map=new Map(track.map(k=>[k.f,k]));track.splice(0,track.length,...[...map.values()].sort((a,b)=>a.f-b.f));}};
 clean(g.camera);nodes.forEach(n=>clean(n.motion));return g;
}
