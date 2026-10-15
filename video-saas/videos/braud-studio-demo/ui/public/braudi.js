const interval=16*60*1000,recentWindow=90*1000,preference='studio-braudi-enabled';

// Count only time actually spent in an available, active interface.
export function advanceBraudiTimer(elapsed,delta,{enabled=true,visible=true,recent=true,blocked=false}={},limit=interval){
 const next=enabled&&visible&&recent&&!blocked?Math.min(limit,Math.max(0,elapsed)+Math.max(0,delta)):Math.max(0,elapsed);
 return {elapsed:next,due:enabled&&visible&&recent&&!blocked&&next>=limit};
}

function artwork(){return `<svg class="braudi-art" viewBox="0 0 240 150" aria-hidden="true">
 <ellipse cx="72" cy="142" rx="30" ry="4" fill="currentColor" opacity=".07"/><ellipse cx="173" cy="142" rx="26" ry="4" fill="currentColor" opacity=".06"/>
 <g transform="translate(72 87)"><g class="braudi-robot">
  <path d="M-12 35v17M12 35v17" stroke="#697d96" stroke-width="9" stroke-linecap="round"/><path d="M-18 54h13M7 54h13" stroke="#d7e2ed" stroke-width="9" stroke-linecap="round"/>
  <path d="M-19 7l-13 14" stroke="#b6c5d6" stroke-width="8" stroke-linecap="round"/><circle cx="-33" cy="22" r="5" fill="#e5edf5"/>
  <rect x="-22" y="-5" width="44" height="43" rx="12" fill="#397bff"/><path d="M-16 0h32" stroke="#8db3ff" stroke-width="2" opacity=".65"/>
  <text x="0" y="20" text-anchor="middle" fill="#fff" font-size="7.2" font-weight="700" letter-spacing=".8" font-family="system-ui,sans-serif">BRAUDI</text>
  <g class="braudi-robot-head"><path d="M0-46v-11" stroke="#8eacc8" stroke-width="3"/><circle cx="0" cy="-60" r="4" fill="#397bff"/>
   <rect x="-25" y="-47" width="50" height="39" rx="13" fill="#e5edf5" stroke="#a8bbcf" stroke-width="1.5"/><rect x="-18" y="-39" width="36" height="22" rx="9" fill="#223750"/>
   <path d="M-10-30h2M8-30h2" stroke="#86c4ff" stroke-width="4" stroke-linecap="round"/><path d="M-4-23q4 3 8 0" fill="none" stroke="#86c4ff" stroke-width="1.5" stroke-linecap="round"/>
  </g>
  <g class="braudi-robot-hand"><path d="M20 6l13 14" stroke="#b6c5d6" stroke-width="8" stroke-linecap="round"/><circle cx="34" cy="20" r="5" fill="#e5edf5"/></g>
 </g></g>
 <g transform="translate(176 98)"><g class="braudi-person">
  <path d="M-9 24l-3 17M9 24l3 17" stroke="#46515f" stroke-width="9" stroke-linecap="round"/><path d="M-17 43h10M8 43h11" stroke="#263442" stroke-width="6" stroke-linecap="round"/>
  <path d="M-16-17q16-8 32 0l4 43h-40z" fill="#667d99"/><path d="M0-20v43" stroke="#9eb0c6" stroke-width="1.4"/><path d="M17-9l7 22" stroke="#667d99" stroke-width="8" stroke-linecap="round"/><circle cx="24" cy="16" r="4" fill="#dfb998"/>
  <rect x="-5" y="-31" width="10" height="13" rx="4" fill="#dfb998"/><ellipse cx="0" cy="-44" rx="14" ry="17" fill="#e7c4a4"/>
  <path d="M-14-42q-4-23 14-22 18 0 15 23l-5-11q-12 7-23 0z" fill="#26313c"/><circle cx="-5" cy="-43" r="1.3" fill="#293746"/><circle cx="5" cy="-43" r="1.3" fill="#293746"/><path d="M-3-35h6" stroke="#9e6e59" stroke-width="1.3" stroke-linecap="round"/>
  <g class="braudi-swing"><path d="M-15-9l-14-16" stroke="#667d99" stroke-width="9" stroke-linecap="round"/><path d="M-29-25l-10-5" stroke="#dfb998" stroke-width="8" stroke-linecap="round"/><path d="M-35-29l-59-28" stroke="#bc8b53" stroke-width="8" stroke-linecap="round"/><path d="M-43-33l-50-24" stroke="#e1bb82" stroke-width="5" stroke-linecap="round"/>
  </g>
 </g></g>
 <g class="braudi-tap" fill="none" stroke="#e6b34b" stroke-width="2.2" stroke-linecap="round"><path d="M73 30v-7M63 33l-5-5M83 33l5-5"/><path d="M70 39l4-4 4 4"/></g>
 </svg>`;}

const installed=new WeakMap();
export function installBraudi({getTheme,previewTheme,restoreTheme,whenSettled=()=>Promise.resolve()}){
 const doc=document,view=doc.defaultView;
 if(installed.has(doc))return installed.get(doc);
 const reduced=view.matchMedia('(prefers-reduced-motion: reduce)');
 let enabled=true;try{enabled=view.localStorage.getItem(preference)!=='false';}catch{}
 let elapsed=0,lastTick=view.performance.now(),lastActivity=lastTick,current=null,themeQueue=Promise.resolve();
 const activity=()=>{lastActivity=view.performance.now();};
 const typing=()=>{const node=doc.activeElement;return !!node&&(node.isContentEditable||node.matches?.('input,textarea,select'));};
 const blocked=()=>!!doc.querySelector('[aria-modal="true"],dialog[open]')||typing();
 const visible=()=>doc.visibilityState!=='hidden'&&doc.hasFocus();
 const queueTheme=work=>{const next=themeQueue.catch(()=>{}).then(work);themeQueue=next;return next;};
 const restore=run=>queueTheme(async()=>{if(run.previewed){await restoreTheme(run.original);run.previewed=false;}});
 function place(stage){
  const anchor=doc.querySelector('.theme-toggle'),rect=anchor?.getBoundingClientRect(),width=Math.min(240,view.innerWidth-24);
  const left=Math.max(12,Math.min(view.innerWidth-width-12,rect?rect.right-width:view.innerWidth-width-20));
  const top=Math.max(12,Math.min(view.innerHeight-192,rect?rect.bottom+12:76));
  stage.style.left=left+'px';stage.style.top=top+'px';stage.style.width=width+'px';
 }
 async function stop(){
  const run=current;if(!run)return themeQueue.catch(()=>{});
  current=null;run.cancelled=true;for(const timer of run.timers)view.clearTimeout(timer);run.stage.remove();
  await restore(run);
 }
 function later(run,delay,work){const timer=view.setTimeout(()=>{run.timers.delete(timer);if(current===run&&!run.cancelled)Promise.resolve(work()).catch(()=>stop().catch(()=>{}));},delay);run.timers.add(timer);}
 async function play(){
  if(!enabled||current||!visible()||blocked())return false;
  // Finish any outstanding restoration before taking the next theme snapshot.
  await themeQueue.catch(()=>{});
  await whenSettled();
  if(current||!enabled||!visible()||blocked())return false;
  const stage=doc.createElement('aside'),run={stage,original:getTheme(),previewed:false,cancelled:false,timers:new Set()};
  current=run;elapsed=0;stage.className='braudi-stage'+(reduced.matches?' is-reduced':'');stage.setAttribute('aria-label','Braudi');
  stage.innerHTML=`<button type="button" class="braudi-close" aria-label="Cerrar Braudi"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 4 8 8m0-8-8 8"/></svg></button>${artwork()}<div class="braudi-apology" role="status">Perdón. Ya está.</div>`;
  stage.querySelector('.braudi-close').addEventListener('click',()=>{stop().catch(()=>{});});
  place(stage);doc.body.append(stage);
  if(reduced.matches){later(run,2600,stop);return true;}
  later(run,750,()=>queueTheme(async()=>{
   if(current!==run||run.cancelled)return;
   const dark=run.original==='dark'||run.original==='system'&&view.matchMedia('(prefers-color-scheme: dark)').matches||run.original==='auto'&&view.matchMedia('(prefers-color-scheme: dark)').matches;
   run.previewed=true;await previewTheme(dark?'light':'dark');
  }));
  later(run,4600,()=>restore(run));
  later(run,7000,stop);
  return true;
 }
 async function setEnabled(value){enabled=!!value;try{view.localStorage.setItem(preference,String(enabled));}catch{}if(!enabled)await stop();}
 const api={play,stop,setEnabled,get enabled(){return enabled;}};installed.set(doc,api);
 for(const event of ['pointerdown','pointermove','wheel','keydown'])doc.addEventListener(event,activity,{passive:true});
 doc.addEventListener('focusin',()=>{if(current&&typing())stop().catch(()=>{});});
 doc.addEventListener('visibilitychange',()=>{lastTick=view.performance.now();if(doc.visibilityState==='hidden')stop().catch(()=>{});});
 view.addEventListener('blur',()=>stop().catch(()=>{}));
 view.addEventListener('resize',()=>{if(current)place(current.stage);});
 reduced.addEventListener('change',()=>{if(reduced.matches)stop().catch(()=>{});});
 view.setInterval(()=>{
  const now=view.performance.now(),delta=Math.min(2000,now-lastTick);lastTick=now;
  if(current&&blocked())stop().catch(()=>{});
  const result=advanceBraudiTimer(elapsed,delta,{enabled,visible:visible(),recent:now-lastActivity<recentWindow,blocked:!!current||blocked()});elapsed=result.elapsed;
  if(result.due)play().catch(()=>{});
 },1000);
 return api;
}
