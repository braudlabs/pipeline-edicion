const sun='<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.4 1.4m11.2 11.2L19 19M5 19l1.4-1.4M17.6 6.4 19 5"/>';
const moon='<path d="M20 14.2A8.5 8.5 0 0 1 9.8 4 8.5 8.5 0 1 0 20 14.2Z"/>';
const glyph=body=>`<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${body}</svg>`;
export function themeButton(){const dark=document.documentElement.dataset.theme==='dark';return `<button class="icon-btn theme-toggle" data-theme-toggle aria-label="${dark?'Activar tema claro':'Activar tema oscuro'}" title="${dark?'Tema claro':'Tema oscuro'}">${glyph(dark?sun:moon)}</button>`;}
export function themeSettings(){const selected=document.documentElement.dataset.appearance||'light';return `<section class="glass settings-card appearance-card"><span class="eyebrow">Apariencia</span><h2>A tu manera.</h2><p>Claro, oscuro o al ritmo de tu dispositivo.</p><div class="appearance-options" role="group" aria-label="Apariencia del estudio">${[['light','Claro'],['dark','Oscuro'],['system','Sistema']].map(([id,label])=>`<button data-theme-choice="${id}" aria-pressed="${selected===id}"><span class="theme-swatch ${id}" aria-hidden="true"><i></i><i></i></span>${label}</button>`).join('')}</div><p class="micro">Se guarda en este navegador. Tus imágenes y vídeos mantienen sus colores originales.</p></section>`;}
export function installTheme(){
 const media=matchMedia('(prefers-color-scheme: dark)'),reduced=matchMedia('(prefers-reduced-motion: reduce)'),root=document.documentElement;
 let requested=root.dataset.appearance||'light',pending=null,switching=false,beforeChange=()=>{},waiters=[];
 const resolve=choice=>choice==='system'?(media.matches?'dark':'light'):choice;
 const apply=(choice,persist=true)=>{if(persist){root.dataset.appearance=choice;try{localStorage.setItem('studio-appearance',choice);}catch{}}root.dataset.theme=resolve(choice);document.querySelectorAll('[data-theme-toggle]').forEach(el=>{const template=document.createElement('template');template.innerHTML=themeButton();const next=template.content.firstElementChild;el.innerHTML=next.innerHTML;el.setAttribute('aria-label',next.getAttribute('aria-label'));el.title=next.title;});document.querySelectorAll('[data-theme-choice]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.themeChoice===root.dataset.appearance)));document.querySelector('meta[name="theme-color"]')?.setAttribute('content',root.dataset.theme==='dark'?'#111214':'#f2f5f8');};
 const curtain=[
  'polygon(-10% -10%,110% -10%,110% -4%,75% -4%,50% -4%,25% -4%,-10% -4%)',
  'polygon(-10% -10%,110% -10%,110% 25%,75% 34%,50% 38%,25% 34%,-10% 25%)',
  'polygon(-10% -10%,110% -10%,110% 69%,75% 78%,50% 82%,25% 78%,-10% 69%)',
  'polygon(-10% -10%,110% -10%,110% 110%,75% 110%,50% 110%,25% 110%,-10% 110%)'
 ];
 const drain=async()=>{
  if(switching)return;switching=true;
  try{while(pending){const {choice:next,persist:save}=pending;pending=null;
   if(reduced.matches||resolve(next)===root.dataset.theme){apply(next,save);continue;}
   if(document.startViewTransition){
    const dark=resolve(next)==='dark';root.dataset.themeCurtain=dark?'down':'up';root.classList.add('theme-revealing');
    try{
     const transition=document.startViewTransition(()=>apply(next,save));await transition.ready;
     const animation=root.animate({clipPath:dark?curtain:[...curtain].reverse()},{duration:820,easing:'cubic-bezier(.32,0,.16,1)',fill:'forwards',pseudoElement:dark?'::view-transition-new(root)':'::view-transition-old(root)'});
     await animation.finished;await transition.finished;
    }catch{apply(next,save);}finally{root.classList.remove('theme-revealing');delete root.dataset.themeCurtain;}
   }else{root.classList.add('theme-fading');apply(next,save);await new Promise(resolve=>setTimeout(resolve,420));root.classList.remove('theme-fading');}
  }}finally{switching=false;const finished=waiters;waiters=[];finished.forEach(resolve=>resolve());}
 };
 const change=(choice,persist=true)=>{
  if(!['light','dark','system'].includes(choice))return Promise.resolve();
  if(persist)requested=choice;pending={choice,persist};
  const complete=new Promise(resolve=>waiters.push(resolve));void drain();return complete;
 };
 document.addEventListener('click',async e=>{const toggle=e.target.closest('[data-theme-toggle]'),choice=e.target.closest('[data-theme-choice]');if(!toggle&&!choice)return;const next=toggle?(root.dataset.theme==='dark'?'light':'dark'):choice.dataset.themeChoice;await beforeChange();void change(next);});
 media.addEventListener('change',async()=>{if(requested==='system'){await beforeChange();if(requested==='system')void change('system');}});apply(requested);
 return {getTheme:()=>root.dataset.theme,previewTheme:choice=>change(choice,false),restoreTheme:choice=>change(choice,false),whenSettled:()=>switching||pending?new Promise(resolve=>waiters.push(resolve)):Promise.resolve(),beforeChange:fn=>{beforeChange=fn;}};
}
