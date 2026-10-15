import type {Job,Plan,Diagnostic,RecipeId} from './types.ts';
export const recipeIds:RecipeId[]=['rail','accumulate','hero','masked-hero','pulse','price','count','comparison','proof','steps','carousel','silence'];
const finite=(n:unknown)=>typeof n==='number'&&Number.isFinite(n);
function assert(ok:unknown,message:string):asserts ok{if(!ok)throw new Error(message);}
export function validateJob(value:unknown):asserts value is Job{
 assert(value&&typeof value==='object','El trabajo debe ser un objeto JSON');const j=value as Job;
 assert(j.version===1,'version debe ser1');assert(typeof j.id==='string'&&j.id.length,'Falta id');
 assert(j.format&&finite(j.format.width)&&j.format.width>0&&finite(j.format.height)&&j.format.height>0,'Dimensiones inválidas');
 assert(Number.isInteger(j.format.width)&&Number.isInteger(j.format.height),'Dimensiones deben ser enteras');
 assert(j.format.fps&&Number.isInteger(j.format.fps.num)&&j.format.fps.num>0&&Number.isInteger(j.format.fps.den)&&j.format.fps.den>0,'fps racional inválido');
 assert(['braud','lafabrica','landing'].includes(j.family),'Familia inválida');assert(Array.isArray(j.words)&&j.words.length,'Faltan palabras con tiempos');assert(Array.isArray(j.assets),'Falta assets');
 const unique=(ids:string[],label:string)=>assert(ids.every(x=>typeof x==='string'&&x.length)&&new Set(ids).size===ids.length,`${label}: ids duplicados o vacíos`);
 unique(j.words.map(w=>w.id),'Palabras');unique(j.assets.map(a=>a.id),'Assets');
 let prev=-Infinity;const ends=new Map<string,number>();
 for(const w of j.words){assert(typeof w.text==='string'&&w.text.trim(),'Palabra vacía');assert(finite(w.start)&&finite(w.end)&&w.start>=0&&w.end>w.start,`Tiempos inválidos: ${w.id}`);assert(w.start>=prev,'words debe estar ordenado por start');prev=w.start;const speaker=w.speaker??'narrator';assert(w.start>=(ends.get(speaker)??0)-.001,`Solapamiento de palabras del mismo hablante: ${w.id}`);ends.set(speaker,w.end);}
 const assets=new Map(j.assets.map(a=>[a.id,a]));
 for(const a of j.assets){assert(['video','image','audio'].includes(a.kind)&&typeof a.src==='string'&&a.src.length,`Asset inválido: ${a.id}`);if(a.duration!==undefined)assert(finite(a.duration)&&a.duration>0,`Duración inválida: ${a.id}`);}
 unique((j.shots??[]).map(s=>s.id),'Planos');
 for(const s of j.shots??[]){assert(assets.get(s.assetId)?.kind==='video'||assets.get(s.assetId)?.kind==='image',`Plano sin medio visual: ${s.id}`);assert(finite(s.sourceStart)&&finite(s.sourceEnd)&&s.sourceStart>=0&&s.sourceEnd>s.sourceStart,`Rango fuente inválido: ${s.id}`);assert(Array.isArray(s.tags),'shot.tags debe ser array');const duration=assets.get(s.assetId)?.duration;if(duration!==undefined)assert(s.sourceEnd<=duration+.001,`Plano fuera de duración: ${s.id}`);if(s.cutoutAssetId)assert(assets.get(s.cutoutAssetId)?.kind==='video'||assets.get(s.cutoutAssetId)?.kind==='image',`Falta recorte alpha: ${s.id}`);if(s.anchor)assert(s.anchor.length===2&&s.anchor.every(x=>finite(x)&&x>=0&&x<=1),'Ancla fuera de0..1');if(s.crop)assert(finite(s.crop.scale)&&s.crop.scale>0&&finite(s.crop.x)&&finite(s.crop.y),'Transformación de plano inválida');for(const b of s.avoid??[])assert([b.x,b.y,b.width,b.height].every(finite)&&b.width>0&&b.height>0,'Caja de exclusión inválida');}
 const wordIds=new Set(j.words.map(w=>w.id));const wordMap=new Map(j.words.map(w=>[w.id,w]));const assigned=new Set<string>();
 if(j.clauses){assert(j.clauses.length,'clauses vacío');unique(j.clauses.map(c=>c.id),'Cláusulas');for(const c of j.clauses){assert(Array.isArray(c.wordIds)&&c.wordIds.length,`Cláusula vacía: ${c.id}`);for(const id of c.wordIds){assert(wordIds.has(id),`Palabra desconocida: ${id}`);assert(!assigned.has(id),`Palabra en dos cláusulas: ${id}`);assigned.add(id);}const speakers=new Set(c.wordIds.map(id=>wordMap.get(id)!.speaker??'narrator'));assert(speakers.size===1,`Cláusula mezcla hablantes: ${c.id}`);if(c.speaker)assert(speakers.has(c.speaker),`Hablante de cláusula no coincide: ${c.id}`);assert(!c.recipe||recipeIds.includes(c.recipe),`Receta desconocida: ${c.recipe}`);if(c.shotId)assert(j.shots?.some(s=>s.id===c.shotId),`Plano desconocido: ${c.shotId}`);for(const id of c.focusWordIds??[])assert(c.wordIds.includes(id),'El foco debe pertenecer a cláusula');if(c.data?.value!==undefined)assert(finite(c.data.value)&&c.data.value>=0,'Valor de contador inválido');for(const id of c.data?.assetIds??[])assert(assets.get(id)?.kind==='image',`Se necesita imagen: ${id}`);for(const b of c.data?.proofRegions??[]){assert([b.rect.x,b.rect.y,b.rect.width,b.rect.height].every(finite)&&b.rect.x>=0&&b.rect.y>=0&&b.rect.width>0&&b.rect.height>0&&b.rect.x+b.rect.width<=1.0001&&b.rect.y+b.rect.height<=1.0001,'Región de prueba fuera de imagen');if(b.atWordId)assert(c.wordIds.includes(b.atWordId),'Beat de prueba fuera de cláusula');}}
 assert(assigned.size===wordIds.size,'Todas las palabras deben pertenecer a una cláusula');}
 for(const a of [j.narration,j.music,...(j.sounds??[])])if(a){assert(assets.get(a.assetId)?.kind==='audio',`Falta audio: ${a.assetId}`);if(a.gain!==undefined)assert(finite(a.gain)&&a.gain>=0&&a.gain<=2,'Ganancia fuera de0..2');}
 for(const s of j.sounds??[])assert(finite(s.at)&&s.at>=0&&finite(s.duration)&&s.duration>0&&typeof s.reason==='string'&&s.reason.length,'Cue de sonido inválido');
 if(j.music)assert(finite(j.music.duckGain)&&j.music.duckGain>=0&&j.music.duckGain<=j.music.gain,'duckGain debe estar entre0 y gain');
}
export function auditPlan(plan:Plan):Diagnostic[]{
 const out:Diagnostic[]=[];const err=(code:string,message:string)=>out.push({severity:'error',code,message});
 const assets=new Set(plan.assets.map(a=>a.id));
 for(const group of [plan.clips,plan.captions,plan.graphics,plan.audio])for(const e of group){if(!Number.isInteger(e.start)||!Number.isInteger(e.end)||e.start<0||e.end<=e.start||e.end>plan.durationInFrames)err('RANGE',`Intervalo inválido ${e.id}`);if('assetId'in e&&!assets.has(e.assetId))err('ASSET',`Medio ausente ${e.id}`);}
 for(const c of plan.coverage)if(!c.representations.length)err('UNREPRESENTED',c.wordId);
 const rails=new Map<string,typeof plan.captions>();for(const c of plan.captions){const a=rails.get(c.speaker)??[];a.push(c);rails.set(c.speaker,a);}
 for(const [speaker,captions] of rails){captions.sort((a,b)=>a.start-b.start);for(let i=1;i<captions.length;i++)if(captions[i].start<captions[i-1].end)err('CAPTION_COLLISION',`${speaker}: ${captions[i-1].id}/${captions[i].id}`);}
 for(const g of plan.graphics){for(const n of g.nodes){if(n.end<=n.start||n.start<g.start||n.end>g.end)err('NODE_RANGE',n.id);if(n.kind==='image'&&!assets.has(n.assetId??''))err('ASSET',n.id);}if(g.cutout&&!assets.has(g.cutout.assetId))err('MASK_MISSING',g.id);}
 const covered=new Set<string>();for(const c of plan.captions)c.wordIds.forEach(id=>covered.add(id));for(const g of plan.graphics)g.nodes.forEach(n=>n.wordIds?.forEach(id=>covered.add(id)));
 for(const c of plan.coverage)if(!covered.has(c.wordId)&&!c.representations.some(r=>r.startsWith('silence:')))err('UNBOUND_WORD',c.wordId);
 return out;
}
