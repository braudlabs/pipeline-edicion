import {focusActionMarkup} from './chat-focus.js';
// Opening exploration is separate from the saved script and its local drafts.
const focusedOpenings = new Map();
const canonicalLines = lines => lines.map(line => ({id:line.id,text:line.text,direction:line.direction||''}));

export function scriptOpeningState(p) {
 const batch=p.scriptOpenings;
 const alternatives=Array.isArray(batch?.alternatives)?batch.alternatives.filter(option=>option&&typeof option.id==='string'&&Array.isArray(option.lines)&&option.lines.length&&option.lines.every(line=>typeof line.text==='string')).slice(0,3):[];
 const targetLineIds=Array.isArray(batch?.targetLineIds)?batch.targetLineIds:[];
 const source=batch?.appliedLines||batch?.sourceLines;
 const current=(p.script||[]).slice(0,targetLineIds.length);
 const stale=!!alternatives.length&&(!targetLineIds.length||!Array.isArray(source)||source.length!==targetLineIds.length||current.length!==targetLineIds.length||current.some((line,i)=>line.id!==targetLineIds[i])||JSON.stringify(canonicalLines(current))!==JSON.stringify(canonicalLines(source)));
 const requested=focusedOpenings.get(p.id);
 const focusedId=alternatives.some(option=>option.id===requested)?requested:alternatives.some(option=>option.id===batch?.selectedId)?batch.selectedId:null;
 return {alternatives,targetLineIds,stale,focusedId,selectedId:batch?.selectedId||null};
}

export function focusScriptOpening(p,id) {
 if(!scriptOpeningState(p).alternatives.some(option=>option.id===id))return false;
 focusedOpenings.set(p.id,id);
 return true;
}

export function findOpening(p,id) {
 return scriptOpeningState(p).alternatives.find(option=>option.id===id)||null;
}

// Rows are the current form fields, not a proposed replacement script. Keep the
// source guard: a stale form must be resolved before an opening can be applied.
export function scriptDraftDiffers(script,rows,sourceScript) {
 if(!Array.isArray(script)||!Array.isArray(rows)||rows.length!==script.length||sourceScript!==JSON.stringify(script))return true;
 // The draft store preserves literal field strings. Accepting an equivalent
 // numeric spelling would leave its old snapshot active after applying a hook.
 const timing=value=>String(value??'');
 return script.some((line,i)=>{
  const row=rows[i];
  if(!row||row.id!==line.id||String(row.text??'')!==String(line.text??'')||String(row.direction??'')!==String(line.direction??''))return true;
  return ['start','end'].some(key=>{
   const current=timing(row[key]),saved=timing(line[key]);
   return current!==saved;
  });
 });
}

export function openingProposalPrompt(p) {
 if(!(p.script||[]).length)return 'Quiero preparar el guion de esta pieza a partir de la idea, el público y el concepto acordados. Primero construyamos el guion base. Después exploraremos tres aperturas alternativas, manteniendo el cuerpo y el cierre. Todavía no definamos ni generemos las escenas.';
 return 'Quiero probar tres aperturas distintas para este guion. Revisa la idea y el guion guardados, identifica las primeras frases que forman la apertura y propón tres opciones con su intención y qué queremos comprobar. Mantén el cuerpo y el cierre del guion actual. Guarda las tres aperturas como alternativas de esta pieza para poder compararlas aquí, sin aplicar ninguna todavía. Si te pido cambiar otra parte, podremos trabajarla también. Todavía no generes escenas ni locuciones.';
}

export function openingFocusPrompt(p,id) {
 const option=findOpening(p,id);
 if(!option)return '';
 return `Quiero revisar esta apertura del guion: «${option.title||'Apertura alternativa'}».\n\n${option.lines.map(line=>line.text).join('\n')}\n\nValoremos cómo conecta con el público y la idea. Mantén el resto del guion y no apliques cambios hasta que los acordemos.`;
}

function openings(p,{esc,icon}) {
 const state=scriptOpeningState(p),hasScript=!!p.script?.length;
 const slots=Array.from({length:3},(_,i)=>state.alternatives[i]||null);
 return `<section class="guide-paper glass creative-openings" aria-labelledby="opening-heading"><header class="guide-section-head creative-script-head"><div><span class="guide-caption">En exploración · Guion</span><h2 id="opening-heading">Tres maneras de empezar.</h2><p>Probamos la apertura. El cuerpo y el cierre siguen siendo parte del mismo guion.</p></div>${focusActionMarkup({kind:'step',id:'script'},{label:state.alternatives.length?'Explorar otras aperturas':'Proponer tres aperturas',topic:'openings',esc})}</header><div class="creative-opening-grid">${slots.map((option,i)=>{
  const applied=option?.id===state.selectedId&&!state.stale,focused=option?.id===state.focusedId;
  return option?`<article class="creative-opening-card${focused?' is-focused':''}${applied?' is-applied':''}" data-opening="${esc(option.id)}"><button type="button" class="creative-opening-focus" data-ecom="script-opening-focus" data-id="${esc(option.id)}" aria-pressed="${focused}" aria-label="Revisar apertura ${i+1}: ${esc(option.title||'Sin título')}"><span class="creative-opening-meta"><span class="creative-opening-number">${String(i+1).padStart(2,'0')}</span><span class="creative-opening-status">${applied?'En el guion':focused?'En revisión':'Por explorar'}</span></span><h3>${esc(option.title||`Apertura ${i+1}`)}</h3><p class="creative-opening-text">${esc(option.lines.map(line=>line.text).join('\n'))}</p>${option.hypothesis?`<p class="creative-opening-intent">${esc(option.hypothesis)}</p>`:''}</button><footer>${focusActionMarkup({kind:'opening',id:option.id},{label:'Comentar',esc})}<button type="button" class="btn secondary" data-ecom="script-opening-apply" data-id="${esc(option.id)}" ${applied||state.stale?'disabled':''}>${applied?icon('check')+' En uso':'Usar apertura'}</button></footer></article>`:`<article class="creative-opening-card is-empty"><span class="creative-opening-meta"><span class="creative-opening-number">${String(i+1).padStart(2,'0')}</span><span class="creative-opening-status">Por explorar</span></span><h3>Apertura ${i+1}</h3><p class="creative-opening-placeholder">${hasScript?'Las propuestas del agente aparecerán aquí.':'Primero construimos el guion base.'}</p><span class="creative-opening-empty-mark" aria-hidden="true">${icon('plus')}</span></article>`;
 }).join('')}</div><div class="creative-openings-foot"><p class="micro" ${state.stale?'role="status"':''}>${state.stale?'La apertura del guion ha cambiado. Actualiza las propuestas antes de usarlas.':state.alternatives.length?'Elige una para comentarla. Solo «Usar apertura» cambia el guion.':'Las aperturas se preparan en el chat y se guardan aquí para compararlas.'}</p>${state.stale?'<button type="button" class="text-btn" data-ecom="script-openings-propose">Actualizar propuestas</button>':''}</div></section>`;
}

function savedScript(p,{esc,icon,button}) {
 const script=p.script||[],scenes=p.scenes||[];
 return `<section class="guide-paper glass creative-script-paper"><header class="guide-section-head creative-script-head"><div><span class="guide-caption">Guion de la pieza</span><h2>Lo que vamos a decir.</h2><p>Podemos ajustar cualquier parte hablando con el agente o editándola aquí.</p></div><div class="creative-script-tools">${focusActionMarkup({kind:'step',id:'script'},{label:'Trabajar con el agente',topic:'script',esc})}${button(icon('plus')+' Añadir frase','add-line','text-btn')}</div></header>${script.length?`<form id="script-form"><input type="hidden" name="_sourceScript" value="${esc(JSON.stringify(script))}">${script.map((line,i)=>{
  const linked=scenes.filter(scene=>scene.lineId===line.id);
  return `<article class="script-line guide-script-line" data-line="${esc(line.id)}"><span class="line-number">${String(i+1).padStart(2,'0')}</span><div><button type="button" class="script-speaker" data-ecom="line-voice" data-id="${esc(line.id)}">${esc(line.speaker||(['off','mixed'].includes(p.audioMode)?'Voz por definir':'Quién habla / texto en pantalla'))} ${icon('settings')}</button><label class="sr-only" for="text-${esc(line.id)}">Frase ${i+1}</label><textarea id="text-${esc(line.id)}" class="line-text" data-field="text" rows="${Math.max(2,Math.ceil((line.text||'').length/72))}">${esc(line.text)}</textarea>${linked.length?`<div class="guide-visual-note"><span>Qué se ve</span>${linked.map(scene=>`<button type="button" data-ecom="guide-scene" data-id="${esc(scene.id)}"><strong>${esc(scene.title)}</strong><span>${esc(scene.intent||'Visual por definir')}</span></button>`).join('')}</div>`:''}<details class="guide-details"><summary>Interpretación y tiempos</summary><label for="direction-${esc(line.id)}">Cómo debe sonar</label><textarea id="direction-${esc(line.id)}" data-field="direction" class="line-direction" placeholder="Cercano, pausado, con humor…">${esc(line.direction)}</textarea><div class="two-fields"><label>Inicio (s)<input data-field="start" type="number" min="0" step="0.01" value="${line.start??''}"></label><label>Final (s)<input data-field="end" type="number" min="0" step="0.01" value="${line.end??''}"></label></div></details></div></article>`;
 }).join('')}<div class="guide-actions"><span class="micro">Texto e interpretación se guardan por separado.</span><button class="btn primary" type="submit">Guardar guion ${icon('check')}</button></div></form>`:`<div class="guide-empty creative-script-empty"><span class="creative-script-empty-symbol" aria-hidden="true">${icon('audio')}</span><h3>De la idea a las palabras.</h3><p>El agente construye el guion contigo. El texto aparecerá aquí cuando lo guarde en la pieza.</p>${focusActionMarkup({kind:'step',id:'script'},{label:'Preparar el guion',topic:'openings',className:'btn secondary',esc})}</div>`}</section>`;
}

export function renderCreativeScript(p,h) {
 return `<div class="creative-script">${openings(p,h)}${savedScript(p,h)}<div class="guide-next"><p>Con el guion en mente, definimos quién aparece.</p><button type="button" class="btn secondary" data-ecom="guide-step" data-step="casting">Construir el reparto ${h.icon('arrow')}</button></div></div>`;
}
