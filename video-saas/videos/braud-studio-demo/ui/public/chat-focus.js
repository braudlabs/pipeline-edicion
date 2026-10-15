// Shared by the UI and send boundary: labels and excerpts always come from the
// current piece, never from a client-supplied label or instruction.
const clip=(value,max=1200)=>typeof value==='string'?value.slice(0,max):'';
const cleanId=value=>typeof value==='string'&&value.length>0&&value.length<=200;
const own=(object,key)=>Object.prototype.hasOwnProperty.call(object,key);
const topics={
 concept:['Concepto',['conceptTitle','concept']],
 audience:['Público y momento',['audience','audienceAwareness','audienceRelationship']],
 goal:['Objetivo y siguiente paso',['goal','cta']],
 tension:['La tensión',['tension']],
 proof:['Argumento y prueba',['offer','proof']],
 message:['Mensaje central',['message']],
 angles:['Ángulos de la idea',[]],
 versions:['Versiones de esta pieza',[]]
};
const steps={idea:'Idea',script:'Guion',casting:'Casting'};

export function resolveChatFocus(piece,input,{assets=[]}={}) {
 if(!piece||!input||typeof input!=='object'||Array.isArray(input)||!cleanId(input.kind)||!cleanId(input.id))return null;
 const {kind,id}=input;
 let label,details;
 if(kind==='intent'&&own(topics,id)) {
  const [title,fields]=topics[id];label=title;
  details=Object.fromEntries(fields.map(key=>[key,clip(piece.intentBrief?.[key])]));
  if(id==='concept'&&!details.concept)details.concept=clip(piece.brief);
 } else if(kind==='step'&&own(steps,id)) {
  label=steps[id];details={};
 } else if(kind==='angle') {
  const item=(piece.creativeAngles||[]).find(item=>item.id===id);if(!item)return null;
  label='Ángulo · '+clip(item.title,180);
  details=Object.fromEntries(['title','motivation','concept','hypothesis'].map(key=>[key,clip(item[key])]));
 } else if(kind==='opening') {
  const batch=piece.scriptOpenings,item=batch?.alternatives?.find(item=>item.id===id);if(!item||!Array.isArray(item.lines))return null;
  label='Apertura · '+clip(item.title||'Alternativa',180);
  details={openingSetId:clip(batch.id,200),title:clip(item.title),hypothesis:clip(item.hypothesis),targetLineIds:(batch.targetLineIds||[]).slice(0,10).map(id=>clip(id,200)),lines:item.lines.slice(0,10).map(line=>({text:clip(line.text,500),direction:clip(line.direction,120)}))};
 } else if(kind==='role') {
  const role=(piece.castRoles||[]).find(role=>role.id===id);if(!role)return null;
  label='Papel · '+clip(role.role,180);
  details={role:clip(role.role),purpose:clip(role.purpose),description:clip(role.description)};
 } else if(kind==='candidate'&&cleanId(input.roleId)) {
  const role=(piece.castRoles||[]).find(role=>role.id===input.roleId),candidate=role?.candidates?.find(candidate=>candidate.id===id);
  const asset=candidate&&assets.find(asset=>asset.id===candidate.assetId&&asset.clientId===piece.clientId&&asset.kind==='image'&&asset.category!=='inspiration');
  if(!role||!candidate||!asset)return null;
  label='Candidato · '+clip(asset.name||role.role,180);
  details={role:clip(role.role),assetId:asset.id,assetName:clip(asset.name),note:clip(candidate.note),status:['exploring','shortlisted'].includes(candidate.status)?candidate.status:'exploring'};
 } else return null;
 return {kind,id,...(kind==='candidate'?{roleId:input.roleId}:{}),label,details};
}

export function makeChatFocusTarget(piece,descriptor,options={}) {
 const focus=resolveChatFocus(piece,descriptor,options);
 return focus?{pieceId:piece.id,focus}:null;
}

export function focusLabel(target) {return clip(target?.focus?.label,240);}

function targetIdentity(target) {
 if(!target)return '';
 return JSON.stringify([target.pieceId||null,target.sceneId||null,target.assetId||null,target.time??null,target.focus?.kind||null,target.focus?.id||null,target.focus?.roleId||null]);
}

export function prepareChatFocusDraft({text='',target=null,nextTarget,prompt='',mode='focus'}={}) {
 const previous=typeof text==='string'?text:'';
 if(!nextTarget?.pieceId||!nextTarget.focus||!['focus','draft'].includes(mode))return {ok:false,reason:'Este foco ya no está disponible. Vuelve a elegirlo en la pieza.'};
 if(previous.trim()&&target&&targetIdentity(target)!==targetIdentity(nextTarget))return {ok:false,reason:'Tu borrador tiene otra referencia. Quítala antes de cambiar el foco; conservamos el texto que ya has escrito.'};
 const value=mode==='draft'&&typeof prompt==='string'?prompt.trim():'';
 if(mode==='draft'&&!value)return {ok:false,reason:'No se ha podido preparar el mensaje. Puedes poner el foco y escribirlo tú.'};
 const nextText=value&&!previous.includes(value)?previous+(previous?'\n\n':'')+value:previous;
 if(nextText.length>30000)return {ok:false,reason:'El borrador supera los 30.000 caracteres. Acórtalo antes de añadir otro mensaje.'};
 return {ok:true,text:nextText,target:structuredClone(nextTarget)};
}

const escape=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
export function focusActionMarkup(descriptor,{label='Comentar',ariaLabel=label,topic='',className='text-btn',esc=escape}={}) {
 const attrs=`data-focus-kind="${esc(descriptor.kind)}" data-focus-id="${esc(descriptor.id)}"${descriptor.roleId?` data-focus-role="${esc(descriptor.roleId)}"`:''}${topic?` data-focus-topic="${esc(topic)}"`:''}`;
 return `<details class="chat-focus-action"><summary class="${esc(className)}" aria-label="${esc(ariaLabel)}">${label}<svg class="chat-focus-chevron" viewBox="0 0 16 16" aria-hidden="true"><path d="m5 6 3 3 3-3"/></svg></summary><div class="chat-focus-menu"><button type="button" data-ecom="creative-focus" ${attrs}><strong>Poner foco</strong><span>Añadir contexto, sin escribir un mensaje.</span></button><button type="button" data-ecom="creative-draft" ${attrs}><strong>Redactar mensaje</strong><span>Preparar un borrador que puedes editar.</span></button></div></details>`;
}
