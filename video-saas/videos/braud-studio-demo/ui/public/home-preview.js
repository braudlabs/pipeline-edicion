// Visual exploration is opt-in and local to the home view. It never changes a piece.
export const homePreviewStyles=Object.freeze([
 {id:'original',label:'Actual',description:'El inicio actual, como referencia.'},
 {id:'liquid',label:'Líquido',description:'Vidrio neutro, retícula fina y una entrada más amplia.'},
 {id:'grid',label:'Mosaico',description:'Una idea y todo tu estudio, en el mismo plano.'},
 {archived:true,id:'clear',label:'Cristal',description:'Cristal tallado sobre un campo de luz azul.'},
 {archived:true,id:'floating',label:'Cápsula',description:'Una lente, una idea y una conversación que flota.'},
 {archived:true,id:'continuous',label:'Mosaico',description:'Un estudio editorial: crear a un lado, explorar al otro.'}
]);
const styleFor=value=>homePreviewStyles.find(style=>style.id===value);

export function homePreviewState(search=''){
 const params=new URLSearchParams(search),enabled=params.get('dev')==='1'&&params.get('homePreview')==='1';
 return {enabled,style:enabled&&styleFor(params.get('homeStyle'))?params.get('homeStyle'):'original'};
}

export function homePreviewUrl(href,style){
 const url=new URL(href);
 if(!homePreviewState(url.search).enabled||!styleFor(style))return url.href;
 url.searchParams.set('homeStyle',style);
 return url.href;
}

export function renderHomePreview(content,search=''){
 const {enabled,style}=homePreviewState(search);
 if(!enabled)return content;
 const art=`<div class="home-preview-hero-art" aria-hidden="true"><i class="hp-plate hp-plate-outer"></i><i class="hp-plate hp-plate-inner"></i><div class="hp-lens"><i></i><span>+</span></div><div class="hp-glass-connection"><svg viewBox="0 0 600 240" focusable="false"><defs><linearGradient id="hp-connection-fill" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff" stop-opacity=".5"/><stop offset=".48" stop-color="#dceaff" stop-opacity=".08"/><stop offset="1" stop-color="#1b53ae" stop-opacity=".24"/></linearGradient><linearGradient id="hp-connection-edge" x1="0" y1="0" x2=".8" y2="1"><stop stop-color="#fff"/><stop offset=".4" stop-color="#d8e9ff" stop-opacity=".16"/><stop offset=".85" stop-color="#fff" stop-opacity=".82"/><stop offset="1" stop-color="#a7ccff" stop-opacity=".32"/></linearGradient></defs><path d="M118 22c40 0 64 20 87 38 20 16 34 16 54-1 24-22 52-37 91-37h133c61 0 95 42 95 98s-34 98-95 98H350c-39 0-67-15-91-37-20-17-34-17-54-1-23 18-47 38-87 38-58 0-96-43-96-98S60 22 118 22Z" fill="url(#hp-connection-fill)" stroke="url(#hp-connection-edge)" stroke-width="2.4"/><path d="M39 88c12-33 37-51 77-51 40 0 63 21 84 37 28 21 46 20 71-1 25-20 48-33 79-33h133c40 0 66 19 78 51" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="2"/></svg></div><div class="hp-art-tiles">${Array.from({length:12},()=>'<i></i>').join('')}</div></div>`;
 const decorated=content.replace('<section class="home-hero">','<section class="home-hero">'+art+'<button class="hp-grid-lens" type="button" data-home-focus aria-label="Escribir una idea"><span aria-hidden="true">+</span></button>');
 return `<div class="home-preview" data-home-style="${style}"><div class="home-preview-toolbar"><span class="home-preview-label">Explorar el inicio</span><div class="home-preview-options" role="group" aria-label="Estilo del inicio">${homePreviewStyles.filter(option=>!option.archived).map(option=>`<button type="button" class="home-preview-option" data-home-style-option="${option.id}" aria-pressed="${option.id===style}">${option.label}</button>`).join('')}</div><p class="home-preview-description" role="status" aria-live="polite">${styleFor(style).description}</p></div><div class="home-preview-content">${decorated}</div></div>`;
}

const bound=new WeakSet();
export function bindHomePreview(root=document){
 const preview=root.querySelector('.home-preview'),view=preview?.ownerDocument.defaultView;
 if(!preview||!view||bound.has(preview)||!homePreviewState(view.location.search).enabled)return;
 bound.add(preview);
 const input=preview.querySelector('#ecom-input');
 const cards=[...preview.querySelectorAll('.project-card')],hasCover=!!cards[0]?.querySelector('img'),units=cards.length===1?4:cards.length+(hasCover?1:0);
 preview.dataset.mosaicPieces=String(cards.length);
 preview.style.setProperty('--m-last-span',String(4-units%4));
 preview.style.setProperty('--m-last-span-mobile',String(2-cards.length%2));
 preview.querySelector('.new-project-card')?.setAttribute('data-mosaic-wide',String(units%4===0));
 let inputSize=null;
 const fitInput=()=>{
  if(!input)return;
  if(preview.dataset.homeStyle==='floating'){
   inputSize??={height:input.style.height,overflowY:input.style.overflowY};
   input.style.height='0px';
   input.style.height=Math.min(240,Math.max(46,input.scrollHeight))+'px';
   input.style.overflowY='auto';
  }else if(inputSize){Object.assign(input.style,inputSize);inputSize=null;}
 };
 input?.addEventListener('input',fitInput);
 fitInput();
 // Pointer selection keeps an in-progress message focused. Keyboard users keep
 // normal button focus, and the textarea node and its selection never change.
 preview.addEventListener('pointerdown',event=>{
  if(event.target.closest('[data-home-style-option]')&&preview.contains(preview.ownerDocument.activeElement)&&preview.ownerDocument.activeElement.id==='ecom-input')event.preventDefault();
 });
 preview.addEventListener('click',event=>{
  if(event.target.closest('[data-home-focus]')){event.preventDefault();input?.focus({preventScroll:true});return;}
  const button=event.target.closest('[data-home-style-option]');
  if(!button||!preview.contains(button)||!styleFor(button.dataset.homeStyleOption))return;
  event.preventDefault();
  const style=button.dataset.homeStyleOption,scroll={left:view.scrollX,top:view.scrollY};
  preview.dataset.homeStyle=style;
  fitInput();
  preview.querySelectorAll('[data-home-style-option]').forEach(option=>option.setAttribute('aria-pressed',String(option===button)));
  preview.querySelector('.home-preview-description').textContent=styleFor(style).description;
  view.history.replaceState(view.history.state,'',homePreviewUrl(view.location.href,style));
  // Layout changes must not trigger a route render or move the reader to the top.
  view.requestAnimationFrame(()=>view.scrollTo({...scroll,behavior:'instant'}));
 });
}
