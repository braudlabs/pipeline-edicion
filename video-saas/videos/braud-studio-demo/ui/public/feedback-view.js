const escape=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const uuid=/^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const kindName=kind=>kind==='suggestion'?'Sugerencia':'Problema';
function dateLabel(value){const date=new Date(value);return Number.isFinite(date.getTime())?new Intl.DateTimeFormat('es',{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'}).format(date):'';}
export function safeFeedbackImageUrl(value){
 if(typeof value!=='string'||!value.startsWith('/api/feedback/'))return null;
 try{const url=new URL(value,'http://studio.local'),parts=url.pathname.split('/');if(url.origin!=='http://studio.local'||parts.length!==5||!uuid.test(parts[3])||parts[4]!=='image'||!/^[a-z0-9_-]{1,100}$/i.test(url.searchParams.get('clientId')||'')||url.searchParams.has('messageId')&&!uuid.test(url.searchParams.get('messageId')))return null;return url.pathname+url.search;}catch{return null;}
}
function capture(message,esc){const url=safeFeedbackImageUrl(message.imageUrl);return url?`<a class="feedback-capture" href="${esc(url)}" target="_blank" rel="noopener"><img src="${esc(url)}" alt="Captura adjunta al mensaje" loading="lazy"><span>Ver captura</span></a>`:'';}
function compose({reply=false,id='',draftText='',draftKind='problem'},esc){return `<form id="${reply?'ecom-feedback-reply':'ecom-feedback'}" class="feedback-compose"${reply?` data-id="${esc(id)}"`:''}>
 ${reply?'':`<label class="feedback-field">Qué quieres compartir<select name="kind"><option value="problem"${draftKind!=='suggestion'?' selected':''}>Algo no funciona</option><option value="suggestion"${draftKind==='suggestion'?' selected':''}>Una sugerencia</option></select></label>`}
 <label class="feedback-field">${reply?'Añadir un mensaje':'Tu mensaje'}<textarea name="text" required maxlength="5000" rows="${reply?3:5}" placeholder="${reply?'Añade un detalle, una captura o lo que has podido comprobar…':'Qué estabas haciendo y qué te gustaría mejorar…'}">${esc(draftText)}</textarea></label>
 <div class="feedback-compose-foot"><label class="feedback-file">Captura opcional<input type="file" name="screenshot" accept="image/png,image/jpeg"><small>PNG o JPEG · hasta 5 MB</small></label><button class="btn primary" type="submit">${reply?'Guardar mensaje':'Guardar feedback'}</button></div>
 <p class="feedback-note">Guardado en este estudio. ${reply?'Se conserva junto al mensaje original.':'Incluimos la pantalla actual; tu conversación no se adjunta.'}</p>
 </form>`;}
export function renderFeedbackView({reports=[],report=null,tab='messages',brandName='',hasMore=false,loading=false,error='',draftText='',draftKind='problem'}={},helpers={}){
 const esc=helpers.esc||escape,icon=helpers.icon||(()=>''),isNew=tab==='new';
 const nav=`<div class="feedback-nav" role="group" aria-label="Feedback"><button type="button" data-ecom="feedback-tab" data-tab="messages" aria-pressed="${!isNew}">Mensajes</button><button type="button" data-ecom="feedback-tab" data-tab="new" aria-pressed="${isNew}">Nuevo feedback</button></div>`;
 let body='';
 if(loading)body='<div class="feedback-empty" role="status"><p>Cargando mensajes…</p></div>';
 else if(error)body=`<div class="feedback-empty" role="alert"><p>${esc(error)}</p><button class="text-btn" data-ecom="feedback-tab" data-tab="messages">Volver a intentar</button></div>`;
 else if(isNew)body=`<div class="feedback-intro"><h3>¿Qué mejorarías?</h3><p>Una idea o algo que no funciona. Puedes retomarlo aquí cuando quieras.</p></div>${compose({draftText,draftKind},esc)}`;
 else if(report&&uuid.test(report.id)){
  const messages=[{...report,original:true},...(Array.isArray(report.messages)?report.messages:[])];
  body=`<div class="feedback-thread-heading"><button class="text-btn" data-ecom="feedback-tab" data-tab="messages">${icon('back')} Todos los mensajes</button><span class="feedback-kind">${kindName(report.kind)}</span></div><div class="feedback-messages" role="log" aria-label="Mensajes de feedback">${messages.map(message=>`<article class="feedback-message"><header><strong>${message.original?'Tu mensaje':'Tu actualización'}</strong><time datetime="${esc(message.at||'')}">${esc(dateLabel(message.at))}</time></header><p>${esc(message.text)}</p>${capture(message,esc)}</article>`).join('')}</div>${compose({reply:true,id:report.id,draftText},esc)}`;
 }else{
  const rows=reports.filter(row=>row&&uuid.test(row.id));
  body=rows.length?`<div class="feedback-list" aria-label="Feedback guardado">${rows.map(row=>`<button type="button" class="feedback-row" data-ecom="feedback-open" data-id="${esc(row.id)}"><span class="feedback-row-top"><span class="feedback-kind">${kindName(row.kind)}</span><time datetime="${esc(row.updatedAt||row.at||'')}">${esc(dateLabel(row.updatedAt||row.at))}</time></span><strong>${esc(row.text)}</strong><span class="feedback-row-bottom"><span>${Math.max(1,Number(row.messageCount)||1)} ${Number(row.messageCount)>1?'mensajes':'mensaje'}${row.hasImage?' · Captura':''}</span>${icon('arrow')}</span></button>`).join('')}</div>${hasMore?'<p class="feedback-note">Se muestran los mensajes más recientes.</p>':''}`:`<div class="feedback-empty"><h3>Lo que podemos mejorar.</h3><p>Tus comentarios y sus actualizaciones quedarán reunidos aquí.</p><button class="btn secondary" data-ecom="feedback-tab" data-tab="new">Escribir feedback</button></div>`;
 }
 return `<div class="feedback-workspace">${nav}<p class="feedback-local">${brandName?esc(brandName)+' · ':''}Guardado en este estudio</p>${body}</div>`;
}
export async function readFeedbackScreenshot(file){
 if(!file||!file.size)return null;
 if(file.size>5*1024*1024)throw Error('La captura debe ocupar menos de 5 MB.');
 if(!['image/png','image/jpeg'].includes(file.type))throw Error('Adjunta una captura PNG o JPEG.');
 return new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=()=>reject(Error('No se ha podido leer la captura.'));reader.readAsDataURL(file);});
}
