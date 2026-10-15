import type {Job,Clause,Word,RecipeId,Shot,Plan,Decision,Diagnostic,AudioClip,Track} from './types.ts';
import {auditStyle} from './style-rules.ts';
import {catalog,eligible,makeGraphic} from './recipes.ts';
import {validateJob,auditPlan} from './validate.ts';
import {frameAt,fpsValue,sample} from './motion.ts';
import {fitText,textWidth} from './text.ts';
const clean=(s:string)=>s.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9€% ]/g,'');
export function segmentWords(words:Word[]):Clause[]{
 const bySpeaker=new Map<string,Word[]>();for(const w of words){const s=w.speaker??'narrator';bySpeaker.set(s,[...(bySpeaker.get(s)??[]),w]);}
 const groups:Word[][]=[];
 for(const ws of bySpeaker.values()){let group:Word[]=[];ws.forEach((w,i)=>{group.push(w);const next=ws[i+1];if(!next||/[.!?;:]$/.test(w.text)||next.start-w.end>.55||group.length>=12){groups.push(group);group=[];}});}
 return groups.sort((a,b)=>a[0].start-b[0].start).map((ws,i)=>({id:`clause-${i+1}`,wordIds:ws.map(w=>w.id),speaker:ws[0].speaker??'narrator'}));
}
function enrich(c:Clause,ws:Word[]):Clause{
 const result:Clause=structuredClone(c);const phrase=clean(ws.map(w=>w.text).join(' '));
 result.wordIds=ws.map(w=>w.id);
 if(!result.intent)result.intent=/pincha|agenda|llama|reserva|enlace/.test(phrase)?'cta':/problema|perder|tarde|caro|coste/.test(phrase)?'problem':/resultado|vistas|seguidores|ventas/.test(phrase)?'result':/instala|sistema|proceso|paso/.test(phrase)?'mechanism':/mira|pones|elige|genera/.test(phrase)?'demonstration':'hook';
 const numeric=ws.find(w=>/\d/.test(w.text));
 if(numeric&&!result.data){
  const price=ws.some(w=>/[€$]/.test(w.text)||/euros?/.test(clean(w.text)));
  const raw=numeric.text.replace(/[^0-9.,]/g,'');
  // Spanish grouping: 1.000 and 1.000,50; also accept an unambiguous decimal point.
  const normalized=/^\d{1,3}(\.\d{3})+(,\d+)?$/.test(raw)?raw.replaceAll('.','').replace(',','.'):/^\d+(,\d+)?$/.test(raw)?raw.replace(',','.'):/^\d+\.\d+$/.test(raw)?raw:'';
  const value=normalized?Number(normalized):NaN;
  if(Number.isFinite(value)){
   const at=ws.indexOf(numeric);result.data={...(price?{amount:numeric.text+(numeric.text.includes('€')?'':ws[at+1]?.text==='euros'?' €':'')}:{value}),prefix:ws.slice(0,at).map(w=>w.text).join(' '),label:ws.slice(at+1).map(w=>w.text).join(' ')};
   result.focusWordIds??=[numeric.id];
  }
 }
 return result;
}
function selectShot(job:Job,c:Clause,words:Word[],duration:number,previous?:string):Shot|undefined{
 if(c.shotId)return job.shots?.find(s=>s.id===c.shotId);
 const tags=[...(c.tags??[]),c.intent??'',...clean(words.map(w=>w.text).join(' ')).split(' ')];
 return (job.shots??[]).filter(s=>s.sourceEnd-s.sourceStart>=duration-.001&&(!s.speaker||s.speaker===(c.speaker??words[0].speaker??'narrator'))).map(s=>({s,score:s.tags.reduce((sum,t)=>sum+(tags.includes(clean(t))?5:0),0)+(s.id===previous?1:0)})).sort((a,b)=>b.score-a.score||a.s.id.localeCompare(b.s.id))[0]?.s;
}
function anchor(job:Job,shot:Shot|undefined,text:string,size:number,c:Clause,dialogIndex:number,diagnostics:Diagnostic[]):[number,number]{
 const W=job.format.width,H=job.format.height;
 const desired: [number,number]=shot?.anchor?[...shot.anchor]:[.5,job.options?.captionY??(job.family==='landing'?.77:job.family==='lafabrica'?.22:.56)];
 if(dialogIndex>0)desired[1]=Math.min(.84,desired[1]+dialogIndex*.13);
 if(job.options?.allowFaceOverlap||c.allowOverlap)return desired;
 const width=textWidth(text,size)/W,height=size*1.3/H;
 const positions=[desired,[.5,.68],[.5,.75],[.5,.6],[.5,.38]] as [number,number][];
 const score=([x,y]:[number,number])=>(shot?.avoid??[]).reduce((sum,b)=>sum+Math.max(0,Math.min(x+width/2,b.x+b.width)-Math.max(x-width/2,b.x))*Math.max(0,Math.min(y+height/2,b.y+b.height)-Math.max(y-height/2,b.y)),0);
 const best=positions.map((a,i)=>({a,score:score(a),i})).sort((a,b)=>a.score-b.score||a.i-b.i)[0];
 if(best.score>0)diagnostics.push({severity:'warning',code:'LAYOUT_OVERLAP',message:'Todas las posiciones propuestas intersectan una zona de exclusión; revisar el encuadre o el ancla.',clauseId:c.id});
 return best.a;
}
function choose(c:Clause,ws:Word[],shot:Shot|undefined,duration:number,previous:RecipeId|undefined,consecutive:number,job:Job,overlap:boolean):Decision{
 const base:Partial<Record<RecipeId,number>>={rail:20,hero:c.focusWordIds?.length?45:-100,'masked-hero':c.focusWordIds?.length&&shot?.cutoutAssetId?52:-100,price:c.data?.amount?75:-100,count:c.data?.value!==undefined?68:-100,comparison:c.data?.comparison?75:-100,proof:c.data?.proofRegions?80:-100,steps:c.data?.steps?70:-100,carousel:(c.data?.assetIds?.length??0)>=2?65:-100,accumulate:ws.length<=5&&c.intent==='hook'?25:-100,pulse:-100,silence:-100};
 const candidates=(Object.keys(catalog) as RecipeId[]).map(recipe=>{
  let reason=eligible(recipe,c,ws,shot);const meta=catalog[recipe];const minimum=Math.max(meta.minimum,meta.fullScreen?(job.options?.minGraphicSeconds??1):0,recipe==='steps'?(c.data?.steps?.length??0)*.65:0);
  if(duration<minimum)reason=`Necesita ${minimum.toFixed(2)}s para acción y lectura`;
  if(overlap&&recipe!=='rail'&&recipe!=='silence')reason='Dos hablantes simultáneos: preservar ambos rails';
  if(!c.recipe&&meta.fullScreen&&consecutive>=(job.options?.maxConsecutiveGraphics??2))reason='Respiración: límite de escenas gráficas consecutivas';
  let score=base[recipe]??-100;if(recipe===previous)score-=10;if(c.intent==='cta'&&recipe==='rail')score+=60;if(recipe===c.recipe)score+=1000;
  return {recipe,score,eligible:!reason,reason:reason??(recipe===c.recipe?'Selección editorial explícita':`Candidato según ${c.intent} y datos disponibles`)};
 });
 const selected=c.recipe?candidates.find(x=>x.recipe===c.recipe)!:[...candidates].filter(x=>x.eligible).sort((a,b)=>b.score-a.score||a.recipe.localeCompare(b.recipe))[0];
 if(!selected?.eligible)throw new Error(`${c.id}: ${c.recipe??'ninguna receta'}: ${selected?.reason??'sin candidato'}`);
 return {clauseId:c.id,recipe:selected.recipe,reason:selected.reason,wordIds:ws.map(w=>w.id),candidates,evidence:catalog[selected.recipe].evidence.map(x=>`estilo-editor/notas/${x}.md`),shotId:shot?.id};
}
function compileAudio(job:Job,duration:number):AudioClip[]{
 const F=fpsValue(job.format.fps),result:AudioClip[]=[];
 const add=(id:string,assetId:string,start:number,end:number,sourceStart:number,gain:Track)=>result.push({id,assetId,start,end,sourceStart,gain});
 if(job.narration)add('narration',job.narration.assetId,0,duration,job.narration.sourceStart??0,[{f:0,v:job.narration.gain??1}]);
 if(job.music){const m=job.music,attack=Math.round((m.attack??.12)*F),release=Math.round((m.release??.2)*F);const intervals: [number,number][]=[];
  for(const w of job.words){const a=Math.max(0,frameAt(w.start,job.format.fps)-attack),b=Math.min(duration,frameAt(w.end,job.format.fps)+release);const last=intervals.at(-1);if(last&&a<=last[1])last[1]=Math.max(last[1],b);else intervals.push([a,b]);}
  const gain:Track=[{f:0,v:m.gain}];for(const [a,b] of intervals)gain.push({f:a,v:m.gain},{f:Math.min(b,a+attack),v:m.duckGain},{f:Math.max(a,b-release),v:m.duckGain},{f:b,v:m.gain});gain.push({f:Math.max(0,duration-Math.round(.25*F)),v:m.gain},{f:duration,v:0});const map=new Map(gain.slice(0,-2).map(k=>[k.f,k]));const envelope=[...map.values()].sort((a,b)=>a.f-b.f);const fadeStart=Math.max(0,duration-Math.round(.25*F));add('music',m.assetId,0,duration,0,[...envelope.filter(k=>k.f<fadeStart),{f:fadeStart,v:sample(envelope,fadeStart,m.gain)},{f:duration,v:0}]);}
 for(const [i,s] of (job.sounds??[]).entries()){const start=frameAt(s.at,job.format.fps),end=Math.min(duration,start+frameAt(s.duration,job.format.fps));if(start>=duration)throw new Error(`SFX${i} fuera del montaje`);const v=s.gain??1,attack=Math.round((s.fadeIn??0)*F),release=Math.round((s.fadeOut??.05)*F);const gain:Track=attack?[{f:start,v:0},{f:Math.min(end-1,start+attack),v}]:[{f:start,v}];gain.push({f:Math.max(start,end-release),v},{f:end,v:0});add(`sfx-${i}`,s.assetId,start,end,s.sourceStart??0,gain);}
 return result;
}
export function compile(job:Job):Plan{
 validateJob(job);const F=fpsValue(job.format.fps),W=job.format.width,H=job.format.height;
 const wordsById=new Map(job.words.map(w=>[w.id,w]));const clauses=(job.clauses??segmentWords(job.words)).map(c=>enrich(c,c.wordIds.map(id=>wordsById.get(id)!).sort((a,b)=>a.start-b.start))).sort((a,b)=>wordsById.get(a.wordIds[0])!.start-wordsById.get(b.wordIds[0])!.start);
 const duration=Math.max(1,Math.ceil(Math.max(...job.words.map(w=>w.end))*F));
 const palette=job.options?.palette??{background:job.family==='landing'?'#080a0b':'#1b2020',foreground:'#ffffff',accent:job.family==='lafabrica'?'#b9d7f0':'#e5ed3c'};
 const plan:Plan={version:1,engineVersion:'0.1.0',jobId:job.id,width:W,height:H,fps:job.format.fps,durationInFrames:duration,family:job.family,font:{family:'Reference SF Pro',boldSrc:'fonts/SFProDisplay-bold.otf',regularSrc:'fonts/SFProDisplay-regular.otf'},palette,assets:structuredClone(job.assets),clips:[],captions:[],graphics:[],audio:[],decisions:[],diagnostics:[],coverage:[],provenance:{study:'estilo-editor/perfil-estilo.json',fidelity:'unverified_without_visual_comparison'}};
 const bindings=new Map(job.words.map(w=>[w.id,[] as string[]]));let previous:RecipeId|undefined,previousShot:string|undefined,consecutive=0;
 const speakers=[...new Set(job.words.map(w=>w.speaker??'narrator'))];
 for(let ci=0;ci<clauses.length;ci++){
  const c=clauses[ci],ws=c.wordIds.map(id=>wordsById.get(id)!).sort((a,b)=>a.start-b.start),start=frameAt(ws[0].start,job.format.fps);
  const spokenEnd=Math.max(...ws.map(w=>w.end));const nextStart=ci+1<clauses.length?Math.min(...clauses[ci+1].wordIds.map(id=>wordsById.get(id)!.start)):spokenEnd;
  const hold=ci+1<clauses.length&&nextStart>=spokenEnd&&nextStart-spokenEnd<=.55;
  const end=Math.max(start+1,hold?frameAt(nextStart,job.format.fps):Math.ceil(spokenEnd*F));const seconds=(end-start)/F;
  const overlap=clauses.some(other=>other.id!==c.id&&other.wordIds.some(id=>{const w=wordsById.get(id)!;return w.start<spokenEnd&&w.end>ws[0].start;}));
  const shot=selectShot(job,c,ws,seconds,previousShot);const d=choose(c,ws,shot,seconds,previous,consecutive,job,overlap);plan.decisions.push(d);
  if(!job.clauses)plan.diagnostics.push({severity:'warning',code:'INFERRED_INTENT',message:'Intención inferida por reglas léxicas; revisar decisión editorial.',clauseId:c.id});
  const full=catalog[d.recipe].fullScreen;consecutive=full?consecutive+1:0;previous=d.recipe;
  if(shot&&!full){if(shot.sourceEnd-shot.sourceStart<seconds-.001)throw new Error(`Plano ${shot.id} demasiado corto para ${c.id}`);plan.clips.push({id:`${c.id}:clip`,shotId:shot.id,assetId:shot.assetId,start,end,sourceStart:shot.sourceStart,crop:shot.crop??{scale:1,x:0,y:0},mute:shot.mute??true});previousShot=shot.id;}
  else if(!full)plan.diagnostics.push({severity:'warning',code:'NO_FOOTAGE',message:'Overlay sin metraje: se verá sobre fondo del perfil.',clauseId:c.id});
  if(d.recipe==='silence'){ws.forEach(w=>bindings.get(w.id)!.push(`silence:${c.id}`));continue;}
  if(d.recipe!=='rail'){
   const graphic=makeGraphic(d.recipe,c,ws,job,shot,start,end,palette);plan.graphics.push(graphic);
   for(const n of graphic.nodes)for(const id of n.wordIds??[])bindings.get(id)!.push(graphic.id);
  }
  const railWords=ws.filter(w=>!bindings.get(w.id)!.length);
  const speaker=c.speaker??ws[0].speaker??'narrator',dialogIndex=overlap?Math.max(0,speakers.indexOf(speaker)):0;
  const base=job.options?.fontSize??W*(job.family==='landing'?.034:job.family==='lafabrica'?.162:.095);
  const longest=[...railWords].sort((a,b)=>textWidth(b.text,base)-textWidth(a.text,base))[0]?.text??'';
  const pos=anchor(job,shot,longest,fitText(longest,W*.86,base),c,dialogIndex,plan.diagnostics); // Fixed anchor for this layout, never per-frame face jitter.
  for(const w of [...railWords].sort((a,b)=>a.start-b.start)){
   const at=frameAt(w.start,job.format.fps),wi=ws.indexOf(w),next=ws[wi+1];const spokenEnd=Math.ceil(w.end*F);
   const until=Math.min(end,next?frameAt(next.start,job.format.fps):end,spokenEnd+Math.round((job.options?.maxCaptionGap??.15)*F));
   if(until<=at)throw new Error(`Cadencia insuficiente para palabra ${w.id}`);
   const id=`caption:${w.id}`;plan.captions.push({id,wordIds:[w.id],speaker,start:at,end:until,text:w.text,x:pos[0]*W,y:pos[1]*H,fontSize:fitText(w.text,W*.86,base),fill:dialogIndex?palette.accent:palette.foreground,tracking:-.06});bindings.get(w.id)!.push(id);
  }
 }
 // A single visible base shot per frame; simultaneous dialogue reuses the first chosen visual.
 plan.clips.sort((a,b)=>a.start-b.start);for(let i=1;i<plan.clips.length;i++){const prev=plan.clips[i-1],next=plan.clips[i];if(next.start<prev.end){if(next.end<=prev.end){plan.clips.splice(i--,1);}else {next.sourceStart+=(prev.end-next.start)/F;next.start=prev.end;}}}
 const visual=[...plan.clips,...plan.graphics.filter(g=>g.fullScreen)].map(x=>[x.start,x.end]).sort((a,b)=>a[0]-b[0]);let until=0;for(const [a,b] of visual){if(a>until)plan.diagnostics.push({severity:'warning',code:'VISUAL_GAP',message:`Sin metraje/escena de f${until} a f${a-1}; fondo del perfil visible.`});until=Math.max(until,b);}if(until<duration)plan.diagnostics.push({severity:'warning',code:'VISUAL_GAP',message:`Sin metraje/escena de f${until} a f${duration-1}; fondo del perfil visible.`});
 plan.diagnostics.push(...auditStyle(plan));
 plan.audio=compileAudio(job,duration);plan.coverage=job.words.map(w=>({wordId:w.id,representations:[...new Set(bindings.get(w.id)!)]}));
 for(const a of plan.audio){const media=job.assets.find(x=>x.id===a.assetId)!;if(media.duration!==undefined&&a.sourceStart+(a.end-a.start)/F>media.duration+.001)plan.diagnostics.push({severity:'error',code:'AUDIO_SHORT',message:`Audio ${a.assetId} insuficiente; no se rellena ni repite automáticamente.`});}
 if(!job.narration)plan.diagnostics.push({severity:'warning',code:'NO_NARRATION',message:'Guion temporizado sin pista de narración adjunta.'});
 plan.diagnostics.push(...auditPlan(plan));if(plan.diagnostics.some(x=>x.severity==='error'))throw new Error(plan.diagnostics.filter(x=>x.severity==='error').map(x=>x.message).join('\n'));
 return plan;
}
