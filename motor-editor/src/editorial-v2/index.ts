import {prepareRelation,relationNode,type RelationInput} from './relation.ts';
import type {Job,Plan,Word,Node,Graphic,Rect} from '../types.ts';
import {compile} from '../planner.ts';
import {auditPlan,validateJob} from '../validate.ts';
import {textWidth,fitText} from '../text.ts';
import {fpsValue,frameAt,state} from '../motion.ts';
import {createReferenceEntrance} from '../caption-keyframes/reference-v2.ts';
import profile from '../../../estilo-editor/datos/revision-v2/v8-motion-fit.json' with {type:'json'};
import rules from '../../../estilo-editor/datos/revision-v2/rules.json' with {type:'json'};
import inkData from '../../data/font-ink-bold.json' with {type:'json'};

export type Treatment='rail'|'stack'|'inline'|'quiet'|'relation';
export type Annotation={
  clauseId:string;layoutId:string;relation?:RelationInput;
  function:'ordinary'|'emphasis'|'enumeration'|'visual-action'|'explain-relation';
  focusWordIds?:string[];
  /** Omission requires an explicit editorial reason; never inferred from missing OCR. */
  omitReason?:string;
  /** Source/author of the semantic observation, not a fabricated model confidence. */
  observation:{kind:'user'|'agent';reason:string};
  preferredAnchor?:[number,number];
  avoid?:{start:number;end:number;rect:Rect;reason:string}[];
};
export type EditorialSpec={
  version:2;
  source:{assetId:string;sourceStart:number;durationInFrames:number};
  annotations:Annotation[];
};
type Candidate={treatment:Treatment;eligible:boolean;cost:number;reasons:string[]};
type Local={annotation:Annotation;words:Word[];start:number;end:number;candidates:Candidate[]};
export type EditorialDecision={
  clauseId:string;layoutId:string;treatment:Treatment;reason:string;
  candidates:Candidate[];anchor:[number,number];evidence:unknown[];
  observation:Annotation['observation'];semanticFunction:Annotation['function'];omitReason?:string;
  motion:string;needsDesign:boolean;
};
export type EditorialPlan=Plan&{editorial:{version:2;decisions:EditorialDecision[];selectionCost:number;limits:string[]}};
const assert=(ok:unknown,message:string)=>{if(!ok)throw Error(message);};
const ink=(text:string,size:number)=>{
  const boxes=[...text].filter(c=>c.trim()).map(c=>(inkData as Record<string,{top:number;bottom:number}>)[c]);
  assert(boxes.every(Boolean),'Missing ink metrics');
  return {top:Math.min(0,...boxes.map(b=>b.top))*size,bottom:Math.max(0,...boxes.map(b=>b.bottom))*size};
};
const evidence=(ids:string[])=>rules.filter(r=>ids.includes(r.id)).map(r=>({rule:r.id,status:r.status,evidence:r.evidence}));

function candidates(a:Annotation,ws:Word[],end:number,job:Job):Candidate[]{
  const W=job.format.width;
  const focus=ws.filter(w=>a.focusWordIds?.includes(w.id));
  const indices=focus.map(w=>ws.indexOf(w));
  const contiguous=indices.length>0&&indices.every((n,i)=>!i||n===indices[i-1]+1);
  const support=ws.length-focus.length;
  const focusTime=focus.length?end-focus[0].start:0;
  const hasPause=ws.some((w,i)=>i>0&&w.start-ws[i-1].end>.4);
  const full=ws.map(w=>w.text).join(' ');
  const options:Candidate[]=[
    {treatment:'rail',eligible:true,cost:a.function==='emphasis'||a.function==='enumeration'?7:0,reasons:['Lectura ordinaria; cifras, longitud y assets disponibles no bastan para promover un gráfico.']},
    {treatment:'stack',eligible:a.function==='emphasis'&&contiguous&&support>0&&focusTime>=.55&&!hasPause&&ws.length<=9,cost:0,reasons:['Apoyo sintáctico + foco contiguo; espacio y tiempo para retener contexto.']},
    {treatment:'inline',eligible:['emphasis','enumeration'].includes(a.function)&&!hasPause&&ws.length<=8&&fitText(full,W*.82,W*.084)>=W*.065,cost:a.function==='enumeration'?0:2,reasons:['La frase cabe con lectura suficiente; reserva posiciones y revela sin recolocar palabras.']},
    {treatment:'quiet',eligible:a.function==='visual-action'&&Boolean(a.omitReason?.trim()),cost:-2,reasons:['La acción visual tiene prioridad y la omisión está justificada explícitamente.']},
  ];
  const relation=a.relation&&a.function==='explain-relation'?prepareRelation(a.relation,ws,job):undefined;
  options.push({treatment:'relation',eligible:Boolean(relation?.scene),cost:-3,reasons:[relation?.reason??(relation?.scene?'Shared clip window communicates the declared relationship; timings preserve both reading states.':'No supported explicit relationship supplied.')]});
  if(a.function==='explain-relation')options[0].reasons.push('La relación exige diseñar un recurso específico; no se sustituye por un contador genérico.');
  if(!options[1].eligible)options[1].reasons.push('No cumple función, foco contiguo, apoyo, duración o continuidad de frase.');
  if(!options[2].eligible)options[2].reasons.push('No cumple función, longitud, tamaño mínimo o continuidad de frase.');
  return options;
}

/** Exact dynamic program over candidate sequences. Costs are authored preferences, not learned probabilities. */
export function selectSequence(blocks:{candidates:Candidate[]}[]):{choices:Treatment[];cost:number}{
  let paths:{choices:Treatment[];cost:number}[]=[{choices:[],cost:0}];
  for(const b of blocks){
    const best=new Map<Treatment,{choices:Treatment[];cost:number}>();
    for(const p of paths)for(const c of b.candidates.filter(c=>c.eligible)){
      const prev=p.choices.at(-1);
      const repeated=c.treatment===prev&&['stack','inline'].includes(c.treatment)?5:0;
      const busy=prev&&['stack','inline'].includes(prev)&&['stack','inline'].includes(c.treatment)?1:0;
      const next={choices:[...p.choices,c.treatment],cost:p.cost+c.cost+repeated+busy};
      if(!best.has(c.treatment)||next.cost<best.get(c.treatment)!.cost)best.set(c.treatment,next);
    }
    assert(best.size,'No feasible editorial sequence');paths=[...best.values()];
  }
  return paths.sort((a,b)=>a.cost-b.cost||a.choices.join().localeCompare(b.choices.join()))[0]??{choices:[],cost:0};
}

function buildNodes(b:Local,t:Treatment,job:Job):Node[]{
  const W=job.format.width,H=job.format.height,F=fpsValue(job.format.fps),ws=b.words;
  const base=job.options?.fontSize??W*.095,accent=job.options?.palette?.accent??'#dcf395',fill=job.options?.palette?.foreground??'#fffdf1';
  const start=frameAt(b.start,job.format.fps),end=frameAt(b.end,job.format.fps);
  const make=(w:Word,x:number,y:number,size:number,hero=false):Node=>({id:`v2:${w.id}`,kind:'text',text:w.text,wordIds:[w.id],start:frameAt(w.start,job.format.fps),end,z:50,textRole:hero?'focus':'support',x,y,fontSize:size,weight:700,tracking:-.035,fill:hero?accent:fill,shadow:{color:'#00000066',x:0,y:H*.0015,blur:H*.001},motion:undefined});
  if(t==='quiet')return [];
  if(t==='relation')return [relationNode(b.annotation.relation!,ws,job,`relation:${b.annotation.clauseId}`)];
  if(t==='rail')return ws.map((w,i)=>{const n=make(w,0,0,fitText(w.text,W*.84,base,-.035));n.textRole='rail';n.end=Math.min(end,i+1<ws.length?frameAt(ws[i+1].start,job.format.fps):end,Math.ceil(w.end*F)+Math.round(.12*F));return n;});
  const rows:{words:Word[];hero:boolean;size:number}[]=[];
  if(t==='inline')rows.push({words:ws,hero:false,size:fitText(ws.map(w=>w.text).join(' '),W*.82,W*.084,-.035)});
  else {
    const f=ws.findIndex(w=>b.annotation.focusWordIds?.includes(w.id)),last=ws.length-1-[...ws].reverse().findIndex(w=>b.annotation.focusWordIds?.includes(w.id));
    for(const [words,hero] of [[ws.slice(0,f),false],[ws.slice(f,last+1),true],[ws.slice(last+1),false]] as [Word[],boolean][]){
      if(words.length)rows.push({words,hero,size:fitText(words.map(w=>w.text).join(' '),W*.82,hero?W*.255:W*.078,-.035)});
    }
  }
  let y=0,previous:{top:number;bottom:number}|undefined;const nodes:Node[]=[];
  for(const row of rows){
    const phrase=row.words.map(w=>w.text).join(' '),bounds=ink(phrase,row.size);
    if(previous)y+=previous.bottom-bounds.top+H*.006;
    let x=-textWidth(phrase,row.size,-.035)/2;
    for(const w of row.words){const width=textWidth(w.text,row.size,-.035),n=make(w,x+width/2,y,row.size,row.hero||(t==='inline'&&Boolean(b.annotation.focusWordIds?.includes(w.id))));nodes.push(n);x+=width+textWidth(' ',row.size,-.035)-.07*row.size;}
    previous=bounds;
  }
  // Stable first row: growing the stack never recentres already-visible context.
  for(const n of nodes){
    if(n.textRole==='focus'&&t==='stack'&&(end-n.start)/F>=.55){
      n.referenceEntrance={profile,spec:{start:n.start/F,end:end/F,sourceRange:[2,23],initialOffset:52/1920,initialVelocity:-48*(60000/1001)/1920,settleSeconds:.1,exit:{kind:'cut'}}};
      n.motionLabel='fitted-v8-position';
    }else if(t==='inline'){
      const travel=H*.009,d=Math.min(Math.round(.12*F),end-n.start-1);
      if(d>0)n.motion={y:[{f:n.start,v:travel,ease:'out'},{f:n.start+d,v:0}],opacity:[{f:n.start,v:0},{f:n.start+Math.min(d,2),v:1}]};
    }
  }
  // Inspect actual animated ink, not only a final bounding box. Keep compact resting
  // geometry; if overshoot would hit retained context, choose a different entrance.
  const poseAt=(n:Node,f:number)=>{
    const base=state(n.motion,f);
    if(n.referenceEntrance){const p=createReferenceEntrance(n.referenceEntrance.profile,n.referenceEntrance.spec).atFrame(f,job.format.fps,H);base.y+=p.translationY;base.opacity*=p.opacity;}
    return base;
  };
  const collides=(n:Node)=>{
    const ni=ink(n.text!,n.fontSize!),width=textWidth(n.text!,n.fontSize!,-.035),pad=H*.003;
    for(let f=n.start;f<Math.min(n.end,n.start+Math.ceil(.5*F));f+=.5){
      const pose=poseAt(n,f);if(pose.opacity<.2)continue;
      const rect={x:n.x-width/2,y:n.y+ni.top+pose.y-pad,width,height:ni.bottom-ni.top+pad*2};
      if(nodes.some(other=>{
        if(other===n||other.y===n.y||f<other.start||f>=other.end)return false;
        const op=poseAt(other,f);if(op.opacity<.2)return false;
        const oi=ink(other.text!,other.fontSize!),ow=textWidth(other.text!,other.fontSize!,-.035);
        return intersects(rect,{x:other.x-ow/2,y:other.y+oi.top+op.y,width:ow,height:oi.bottom-oi.top});
      }))return true;
    }
    return false;
  };
  for(const n of nodes.filter(n=>n.referenceEntrance)){
    if(collides(n)){
      n.referenceEntrance=undefined;n.motionLabel='authored-rise-to-avoid-context-collision';
      const d=Math.min(Math.round(.18*F),n.end-n.start-1);
      n.motion={y:[{f:n.start,v:H*.025,ease:'out'},{f:n.start+d,v:0}],opacity:[{f:n.start,v:0},{f:n.start+Math.min(3,d),v:1}]};
      if(collides(n)){delete n.motion.y;n.motionLabel='authored-opacity-only-for-tight-layout';}
      assert(!collides(n),'Animated text still collides after constrained entrance; redesign required');
    }
    n.motionBlur={samples:8,angle:180};
  }
  return nodes;
}

function box(nodes:Node[],W:number,H:number):Rect{
  if(!nodes.length)return {x:0,y:0,width:0,height:0};
  let x0=Infinity,x1=-Infinity,y0=Infinity,y1=-Infinity;
  for(const n of nodes){if(n.kind==='relation'){x0=Math.min(x0,n.x-n.width!/2);x1=Math.max(x1,n.x+n.width!/2);y0=Math.min(y0,n.y-n.height!/2);y1=Math.max(y1,n.y+n.height!/2);continue;}const i=ink(n.text!,n.fontSize!),w=textWidth(n.text!,n.fontSize!,-.035);const pad=H*.006; // shadow + design margin
    const travel=n.referenceEntrance?H*.04:n.motion?H*.01:0;
    x0=Math.min(x0,n.x-w/2-pad);x1=Math.max(x1,n.x+w/2+pad);y0=Math.min(y0,n.y+i.top-pad-travel);y1=Math.max(y1,n.y+i.bottom+pad+travel);
  }
  return {x:x0/W,y:y0/H,width:(x1-x0)/W,height:(y1-y0)/H};
}
const intersects=(a:Rect,b:Rect)=>a.x<b.x+b.width&&a.x+a.width>b.x&&a.y<b.y+b.height&&a.y+a.height>b.y;

export function compileEditorial(job:Job,spec:EditorialSpec):EditorialPlan{
  validateJob(job);assert(spec?.version===2,'editorial.version must be 2');assert(job.clauses?.length,'V2 requires reviewed clause boundaries');
  const W=job.format.width,H=job.format.height,F=fpsValue(job.format.fps),src=spec.source;
  assert(src&&Number.isInteger(src.durationInFrames)&&src.durationInFrames>0&&Number.isFinite(src.sourceStart)&&src.sourceStart>=0,'Invalid locked source window');
  const media=job.assets.find(a=>a.id===src.assetId);assert(media?.kind==='video','Locked source must be a video');
  assert(media?.duration!==undefined&&media.duration>=src.sourceStart+src.durationInFrames/F-1e-8,'Source window exceeds verified duration');
  assert(job.words.every(w=>w.end<=src.durationInFrames/F+1e-8),'Speech outside source window');
  assert(spec.annotations.length===job.clauses!.length&&new Set(spec.annotations.map(a=>a.clauseId)).size===spec.annotations.length,'Exactly one annotation per clause required');
  const locals:Local[]=job.clauses!.map(c=>{
    const a=spec.annotations.find(a=>a.clauseId===c.id);assert(a?.layoutId&&a.observation?.reason?.trim()&&['user','agent'].includes(a.observation.kind),'Missing semantic observation/provenance');
    assert(['ordinary','emphasis','enumeration','visual-action','explain-relation'].includes(a!.function),'Unknown narrative function');
    const ws=job.words.filter(w=>c.wordIds.includes(w.id));const end=ws.at(-1)!.end;
    assert((a!.focusWordIds??[]).every(id=>c.wordIds.includes(id)),'Focus outside clause');
    if(a!.preferredAnchor)assert(a!.preferredAnchor.length===2&&a!.preferredAnchor.every(n=>Number.isFinite(n)&&n>=0&&n<=1),'Invalid preferred anchor');
    for(const p of a!.avoid??[])assert([p.start,p.end,p.rect.x,p.rect.y,p.rect.width,p.rect.height].every(Number.isFinite)&&p.start>=0&&p.end>p.start&&p.rect.width>0&&p.rect.height>0&&p.reason?.trim(),'Invalid protected region');
    return {annotation:a!,words:ws,start:ws[0].start,end,candidates:candidates(a!,ws,end,job)};
  }).sort((a,b)=>a.start-b.start);
  assert(locals.every((b,i)=>!i||b.start>=locals[i-1].end),'V2 simultaneous speakers require separate reviewed compositions; use the dialogue workflow');
  // No hidden legacy recipe choices: use legacy only for audio and structural validation.
  const base=structuredClone(job);base.shots=[{id:'locked-source',assetId:src.assetId,sourceStart:src.sourceStart,sourceEnd:src.sourceStart+src.durationInFrames/F,tags:[],mute:Boolean(job.narration)}];
  base.clauses=base.clauses!.map(c=>({...c,recipe:'rail',shotId:'locked-source'}));
  const plan=compile(base) as EditorialPlan;
  plan.engineVersion='0.2.0-editorial-experimental';plan.durationInFrames=src.durationInFrames;
  plan.clips=[{id:'locked-source',shotId:'locked-source',assetId:src.assetId,start:0,end:src.durationInFrames,sourceStart:src.sourceStart,crop:{scale:1,x:0,y:0},mute:Boolean(job.narration)}];
  plan.captions=[];plan.graphics=[];plan.decisions=[];
  // These legacy diagnostics described its replaced clause-by-clause montage.
  plan.diagnostics=plan.diagnostics.filter(d=>!['VISUAL_GAP','NO_NARRATION'].includes(d.code));
  plan.provenance.study='estilo-editor/ALGORITMO-V2.md';
  const selection=selectSequence(locals),nodes=locals.map((b,i)=>buildNodes(b,selection.choices[i],job));
  // A layout group evaluates ALL its phrases and time-varying protected regions before choosing one anchor.
  const groups=new Map<string,number[]>();locals.forEach((b,i)=>groups.set(b.annotation.layoutId,[...(groups.get(b.annotation.layoutId)??[]),i]));
  const anchors=new Map<string,[number,number]>();let previous:[number,number]=[.5,job.options?.captionY??.56];
  for(const [id,indices] of groups){
    const explicit=indices.flatMap(i=>locals[i].annotation.preferredAnchor?[locals[i].annotation.preferredAnchor!]:[]);
    assert(explicit.every(a=>a[0]===explicit[0][0]&&a[1]===explicit[0][1]),`Conflicting anchors in layout ${id}`);
    const desired=explicit[0]??previous;
    const options:[number,number][]=[desired,previous,[.5,.56],[.5,.66],[.5,.74],[.3,.6],[.7,.6],[.5,.4]];
    const viable=options.filter(([x,y])=>indices.every(i=>{
      const b=box(nodes[i],W,H);if(!b.width)return true;
      const placed={...b,x:b.x+x,y:b.y+y};
      if(placed.x<.04||placed.x+placed.width>.96||placed.y<.08||placed.y+placed.height>.9)return false;
      return indices.flatMap(j=>locals[j].annotation.avoid??[]).filter(p=>p.start<locals[i].end&&p.end>locals[i].start).every(p=>!intersects(placed,p.rect));
    })).map((a,i)=>({a,i,cost:Math.hypot(a[0]-desired[0],a[1]-desired[1])+Math.hypot(a[0]-previous[0],a[1]-previous[1])*.3})).sort((a,b)=>a.cost-b.cost||a.i-b.i);
    assert(viable.length,`Layout ${id} has no safe anchor for the full block; redesign instead of covering the subject`);
    anchors.set(id,viable[0].a);previous=viable[0].a;
  }
  const decisions:EditorialDecision[]=[];
  locals.forEach((b,i)=>{
    const treatment=selection.choices[i],a=anchors.get(b.annotation.layoutId)!;
    const ev=evidence(treatment==='relation'?['G01','G03']:treatment==='stack'?['C01','C05','C06']:treatment==='inline'?['C01','C07']:['C01','C03','G01']);
    const reason=b.candidates.find(c=>c.treatment===treatment)!.reasons.join(' ')+' '+b.annotation.observation.reason;
    decisions.push({clauseId:b.annotation.clauseId,layoutId:b.annotation.layoutId,treatment,reason,observation:b.annotation.observation,semanticFunction:b.annotation.function,omitReason:treatment==='quiet'?b.annotation.omitReason:undefined,candidates:b.candidates,anchor:a,evidence:ev,motion:treatment==='relation'?'Measured selector separation; authored font, alpha and text movement':nodes[i].some(n=>n.motionLabel==='authored-opacity-only-for-tight-layout')?'Authored opacity: both motion paths collide in tight layout':nodes[i].some(n=>n.motionLabel==='authored-rise-to-avoid-context-collision')?'Authored monotone entrance: fitted overshoot rejected by animated ink collision':nodes[i].some(n=>n.referenceEntrance)?'V8 position subset 2–23 + authored joins':treatment==='inline'?'Authored single-axis stagger':'Direct replacement',needsDesign:b.annotation.function==='explain-relation'&&treatment!=='relation'});
    if(!nodes[i].length)return;
    nodes[i].forEach(n=>{n.x+=a[0]*W;n.y+=a[1]*H;});
    const g:Graphic={id:`v2:${b.annotation.clauseId}`,clauseId:b.annotation.clauseId,recipe:treatment==='relation'?'comparison':treatment==='stack'?'hero':treatment==='inline'?'accumulate':'rail',start:frameAt(b.start,job.format.fps),end:frameAt(b.end,job.format.fps),fullScreen:false,nodes:nodes[i],evidence:['estilo-editor/ALGORITMO-V2.md']};plan.graphics.push(g);
  });
  plan.coverage=job.words.map(w=>({wordId:w.id,representations:plan.graphics.filter(g=>g.nodes.some(n=>n.wordIds?.includes(w.id))).map(g=>g.id)}));
  locals.forEach((b,i)=>{if(selection.choices[i]==='quiet')for(const w of b.words)plan.coverage.find(c=>c.wordId===w.id)!.representations=[`silence:${b.annotation.clauseId}`];});
  const recipeFor=(t:Treatment)=>t==='relation'?'comparison' as const:t==='stack'?'hero' as const:t==='inline'?'accumulate' as const:t==='quiet'?'silence' as const:'rail' as const;
  plan.decisions=decisions.map((d,i)=>({clauseId:d.clauseId,recipe:recipeFor(d.treatment),reason:d.reason,wordIds:locals[i].words.map(w=>w.id),shotId:'locked-source',evidence:['estilo-editor/ALGORITMO-V2.md'],candidates:d.candidates.map(c=>({recipe:recipeFor(c.treatment),eligible:c.eligible,score:-c.cost,reason:c.reasons.join(' ')}))}));
  plan.editorial={version:2,decisions,selectionCost:selection.cost,limits:['Semantic observations are supplied by the agent/user, not inferred from pixels by this compiler.','Candidate costs and safety margins are authored hypotheses, not learned probabilities.','No new sound effects or automatic masks.','Cross-family visual fidelity remains unverified.','Source audio passes through unless a separate narration is supplied; this compiler does not listen or realign phonemes.']};
  if(decisions.some(d=>d.needsDesign))plan.diagnostics.push({severity:'warning',code:'EDITORIAL_DESIGN_REQUIRED',message:'A relationship still needs a designed graphic; the rail is a provisional fallback.'});
  plan.diagnostics.push(...auditPlan(plan));assert(!plan.diagnostics.some(d=>d.severity==='error'),JSON.stringify(plan.diagnostics.filter(d=>d.severity==='error')));
  return plan;
}
