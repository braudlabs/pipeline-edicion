const escape=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const effortLabels={none:'Directa',minimal:'Mínima',low:'Ágil',medium:'Equilibrada',high:'Profunda',xhigh:'Muy profunda',max:'Máxima',ultra:'Ultra'};
const check='<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m4 10 4 4 8-8"/></svg>';
const chevron='<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>';
const instances=new WeakMap();

export function availablePickerModels(models=[]){
 const seen=new Set();return (Array.isArray(models)?models:[]).filter(model=>model&&typeof model.id==='string'&&model.id&&typeof model.name==='string'&&!seen.has(model.id)&&seen.add(model.id)).map(model=>({...model,efforts:[...new Set((Array.isArray(model.efforts)?model.efforts:[]).filter(effort=>typeof effort==='string'&&effort))]}));
}
export function modelPickerSelection(models,current={},next={}){
 const id=next.model??current.model,model=models.find(model=>model.id===id);
 if(!model)throw Error('Este modelo no está disponible.');
 if(!model.efforts?.length)throw Error('No hay niveles de respuesta disponibles para este modelo.');
 if(next.effort!==undefined&&!model.efforts.includes(next.effort))throw Error('Este nivel no está disponible para el modelo.');
 const preferred=next.effort??current.effort,effort=model.efforts.includes(preferred)?preferred:model.efforts.includes('medium')?'medium':model.efforts[0];
 return {model:model.id,effort};
}
export function modelPickerPosition(anchor,{width,height,offsetLeft=0,offsetTop=0},panel={width:318,height:350}){
 const margin=12,gap=10,right=offsetLeft+width,bottom=offsetTop+height;
 const popupWidth=Math.max(0,Math.min(panel.width,width-margin*2));
 const above=Math.max(0,anchor.top-offsetTop-gap-margin),below=Math.max(0,bottom-anchor.bottom-gap-margin);
 const placement=above>=panel.height||above>=below?'above':'below',space=placement==='above'?above:below;
 const maxHeight=Math.max(0,Math.min(height-margin*2,space)),popupHeight=Math.min(panel.height,maxHeight);
 const left=Math.max(offsetLeft+margin,Math.min(anchor.left,right-popupWidth-margin));
 const top=placement==='above'?Math.max(offsetTop+margin,anchor.top-gap-popupHeight):Math.min(bottom-margin-popupHeight,anchor.bottom+gap);
 return {left,top,width:popupWidth,maxHeight,placement};
}
export function renderModelPicker(models,settings,{scope='Esta conversación'}={}){
 const selected=models.find(model=>model.id===settings.model),effort=effortLabels[settings.effort]||settings.effort||'Sin definir';
 return `<div class="model-picker-options" role="radiogroup" aria-label="Modelo"><span class="model-picker-lens" aria-hidden="true"></span>${models.map((model,index)=>`<button type="button" class="model-picker-option" role="radio" aria-checked="${model.id===settings.model}" tabindex="${model.id===settings.model||!selected&&index===0?0:-1}" data-picker-model="${escape(model.id)}"><span class="model-picker-check">${check}</span><span>${escape(model.name)}</span></button>`).join('')||'<p class="model-picker-empty">No hay modelos disponibles.</p>'}</div><div class="model-picker-footer"><button type="button" class="model-picker-effort-toggle" data-picker-effort-toggle aria-expanded="false"${!selected?' disabled':''}><span>Respuesta</span><strong data-picker-effort-label>${escape(effort)}</strong>${chevron}</button><div class="model-picker-efforts" role="radiogroup" aria-label="Profundidad de la respuesta" hidden></div><p class="model-picker-scope">${escape(scope)}</p><p class="model-picker-status" role="status" aria-live="polite" hidden></p></div>`;
}

export function openModelPicker({anchor,models,settings,onCommit,scope='Esta conversación'}){
 if(!anchor?.isConnected)return null;
 const doc=anchor.ownerDocument,view=doc.defaultView,previous=instances.get(doc);
 if(previous?.anchor===anchor){previous.close();return null;}
 previous?.close(false);
 models=availablePickerModels(models);let current={model:settings?.model,effort:settings?.effort},saving=false,closed=false,frame=0;
 const panel=doc.createElement('section');panel.className='model-picker-popover';panel.id='studio-model-picker';panel.setAttribute('role','dialog');panel.setAttribute('aria-label','Modelo del agente');panel.innerHTML=renderModelPicker(models,current,{scope});
 anchor.setAttribute('aria-haspopup','dialog');anchor.setAttribute('aria-controls',panel.id);anchor.setAttribute('aria-expanded','true');
 doc.body.append(panel);
 const options=panel.querySelector('.model-picker-options'),lens=panel.querySelector('.model-picker-lens'),effortGroup=panel.querySelector('.model-picker-efforts'),effortToggle=panel.querySelector('[data-picker-effort-toggle]'),status=panel.querySelector('.model-picker-status');
 const reduced=view.matchMedia('(prefers-reduced-motion: reduce)').matches;
 function position(){
  frame=0;if(closed)return;if(!anchor.isConnected){close(false);return;}
  const viewport=view.visualViewport||{width:view.innerWidth,height:view.innerHeight,offsetLeft:0,offsetTop:0};
  const rect=anchor.getBoundingClientRect();if(rect.bottom<=viewport.offsetTop||rect.top>=viewport.offsetTop+viewport.height||rect.right<=viewport.offsetLeft||rect.left>=viewport.offsetLeft+viewport.width){close(false);return;}
  // Measure the content before choosing a side; the body portal avoids dock clipping.
  panel.style.maxHeight='';panel.style.width=Math.min(318,viewport.width-24)+'px';
  const result=modelPickerPosition(rect,viewport,{width:318,height:panel.scrollHeight});
  panel.style.left=result.left+'px';panel.style.top=result.top+'px';panel.style.width=result.width+'px';panel.style.maxHeight=result.maxHeight+'px';panel.dataset.placement=result.placement;
 }
 const schedulePosition=()=>{if(!frame&&!closed)frame=view.requestAnimationFrame(position);};
 function moveLens(){const selected=options.querySelector('[aria-checked="true"]');lens.hidden=!selected;if(selected){lens.style.height=selected.offsetHeight+'px';lens.style.transform=`translateY(${selected.offsetTop}px)`;}}
 function reveal(button){if(!button)return;const group=button.closest('[role="radiogroup"]');if(group===options){if(button.offsetTop<options.scrollTop)options.scrollTop=button.offsetTop;else if(button.offsetTop+button.offsetHeight>options.scrollTop+options.clientHeight)options.scrollTop=button.offsetTop+button.offsetHeight-options.clientHeight;}}
 function fillEfforts(){
  const model=models.find(model=>model.id===current.model);effortGroup.innerHTML=(model?.efforts||[]).map((effort,index)=>`<button type="button" role="radio" aria-checked="${effort===current.effort}" tabindex="${effort===current.effort||!model.efforts.includes(current.effort)&&index===0?0:-1}" data-picker-effort="${escape(effort)}">${escape(effortLabels[effort]||effort)}</button>`).join('');
  effortToggle.disabled=!model;panel.querySelector('[data-picker-effort-label]').textContent=effortLabels[current.effort]||current.effort||'Sin definir';
 }
 function close(restoreFocus=true){
  if(closed)return;closed=true;if(frame)view.cancelAnimationFrame(frame);observer?.disconnect();
  doc.removeEventListener('pointerdown',outside,true);doc.removeEventListener('keydown',keydown,true);doc.removeEventListener('scroll',scroll,true);view.removeEventListener('resize',schedulePosition);view.visualViewport?.removeEventListener('resize',schedulePosition);view.visualViewport?.removeEventListener('scroll',schedulePosition);
  panel.remove();anchor.setAttribute('aria-expanded','false');anchor.removeAttribute('aria-controls');if(instances.get(doc)?.panel===panel)instances.delete(doc);
  if(restoreFocus&&anchor.isConnected)anchor.focus({preventScroll:true});
 }
 function outside(event){if(!panel.contains(event.target)&&!anchor.contains(event.target))close(false);}
 function scroll(event){if(!panel.contains(event.target))schedulePosition();}
 function keydown(event){
  if(event.key==='Escape'){event.preventDefault();event.stopImmediatePropagation();close();return;}
  if(event.key==='Tab'){const focusable=[...panel.querySelectorAll('button:not(:disabled)')].filter(button=>button.tabIndex>=0&&!button.closest('[hidden]')),index=focusable.indexOf(doc.activeElement);if(index<0||event.shiftKey&&index===0||!event.shiftKey&&index===focusable.length-1)close(true);return;}
  if(!panel.contains(event.target))return;
  const group=event.target.closest('[role="radiogroup"]');if(!group||!['ArrowDown','ArrowUp','ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();event.stopPropagation();const buttons=[...group.querySelectorAll('[role="radio"]')],index=buttons.indexOf(doc.activeElement);if(!buttons.length)return;
  const next=event.key==='Home'?0:event.key==='End'?buttons.length-1:(index+(['ArrowUp','ArrowLeft'].includes(event.key)?-1:1)+buttons.length)%buttons.length;
  buttons.forEach((button,i)=>button.tabIndex=i===next?0:-1);buttons[next].focus({preventScroll:true});reveal(buttons[next]);
 }
 async function commit(next){
  if(saving||closed)return;let selection;try{selection=modelPickerSelection(models,current,next);}catch(error){status.hidden=false;status.textContent=error.message;schedulePosition();return;}
  if(selection.model===current.model&&selection.effort===current.effort)return;
  saving=true;panel.setAttribute('aria-busy','true');status.hidden=false;status.textContent='Guardando…';
  panel.querySelectorAll('[role="radio"]').forEach(button=>button.setAttribute('aria-disabled','true'));
  try{await onCommit(selection);current=selection;if(closed)return;
   options.querySelectorAll('[data-picker-model]').forEach(button=>button.setAttribute('aria-checked',String(button.dataset.pickerModel===current.model)));
   const focusedEffort=effortGroup.contains(doc.activeElement);fillEfforts();if(focusedEffort)effortGroup.querySelector('[aria-checked="true"]')?.focus({preventScroll:true});moveLens();status.hidden=true;status.textContent='';
  }catch(error){if(!closed){status.hidden=false;status.textContent=error.message||'No se ha podido cambiar el modelo.';}}
  finally{saving=false;if(!closed){panel.removeAttribute('aria-busy');panel.querySelectorAll('[role="radio"]').forEach(button=>button.removeAttribute('aria-disabled'));schedulePosition();}}
 }
 panel.addEventListener('click',event=>{
  const model=event.target.closest('[data-picker-model]'),effort=event.target.closest('[data-picker-effort]');
  if(model){void commit({model:model.dataset.pickerModel});return;}
  if(effort){void commit({effort:effort.dataset.pickerEffort});return;}
  if(event.target.closest('[data-picker-effort-toggle]')){effortGroup.hidden=!effortGroup.hidden;effortToggle.setAttribute('aria-expanded',String(!effortGroup.hidden));schedulePosition();}
 });
 doc.addEventListener('pointerdown',outside,true);doc.addEventListener('keydown',keydown,true);doc.addEventListener('scroll',scroll,true);view.addEventListener('resize',schedulePosition);view.visualViewport?.addEventListener('resize',schedulePosition);view.visualViewport?.addEventListener('scroll',schedulePosition);
 // Route renders can replace the trigger without a resize or a scroll event.
 const observer=typeof view.MutationObserver==='function'?new view.MutationObserver(()=>{if(!anchor.isConnected)close(false);}):null;observer?.observe(doc.body,{childList:true,subtree:true});
 fillEfforts();moveLens();position();
 if(closed)return null;
 if(!reduced&&panel.animate)panel.animate([{opacity:0,transform:'translateY(4px)'},{opacity:1,transform:'translateY(0)'}],{duration:150,easing:'cubic-bezier(.2,.8,.2,1)'});
 const first=options.querySelector('[tabindex="0"]');first?.focus({preventScroll:true});reveal(first);
 const instance={anchor,panel,close};instances.set(doc,instance);return instance;
}
