// Motion follows semantic changes. Streaming text and ordinary state refreshes stay still.
const ease='cubic-bezier(.22,.8,.22,1)';
const media=matchMedia('(prefers-reduced-motion: reduce)');
const animations=new Set(),observers=new Set(),ghosts=new Set(),layoutCleanups=new Set();
const dockDuration=560;
const dockTiming={duration:dockDuration,easing:ease},positionTiming={duration:700,easing:'cubic-bezier(.4,0,.2,1)'};
const layoutMotions=new WeakMap();
let before=null,frame=0;
const canMove=()=>!media.matches&&!document.hidden;
const find=(selector,root=document)=>root?.querySelector(selector);
const rect=node=>{if(!node)return null;const r=node.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height};};
const moving=node=>[...animations].some(a=>a.effect?.target===node&&a.playState==='running');
const measure=node=>node?{node,rect:rect(node),moving:moving(node)}:null;
const key=button=>button?.dataset.tab||button?.dataset.step||button?.dataset.view||button?.dataset.id||'';
const localRect=(node,track)=>{
 if(!node||!track)return null;
 const r=rect(node),parent=rect(track);
 return {...r,x:r.x-parent.x+track.scrollLeft,y:r.y-parent.y+track.scrollTop};
};
const pillSnapshot=(track,selector)=>track?{...measure(find(selector,track)),local:localRect(find(selector,track),track),trackWidth:track.clientWidth,key:key(find('.active',track)),order:[...track.querySelectorAll('button')].map(key).filter(Boolean)}:null;

function cancelMotion(){
 for(const a of animations)a.cancel();
 animations.clear();
 for(const cleanup of layoutCleanups)cleanup();
 layoutCleanups.clear();
 for(const ghost of ghosts)ghost.remove();
 ghosts.clear();
}
function disconnect(){for(const observer of observers)observer.disconnect();observers.clear();}
function animate(node,keyframes,options={}){
 if(!node||!canMove()||typeof node.animate!=='function')return null;
 const animation=node.animate(keyframes,{duration:420,easing:ease,fill:'both',...options});
 animations.add(animation);
 // Remove the effect at completion: no stale transform, width or stacking context remains.
 animation.finished.then(()=>{animations.delete(animation);animation.cancel();},()=>animations.delete(animation));
 return animation;
}
function enter(node,{distance=16,delay=0,duration=420,opacity=0}={}){
 return animate(node,[{opacity,transform:`translateY(${distance}px)`},{opacity:1,transform:'none'}],{delay,duration});
}
function snapshot(){
 const main=find('#app>main'),tabTrack=find('.workspace-tabs'),tile=find('.scene-tile.selected'),liveAgent=find('#app .agent-main'),shell=find('.workspace-shell'),overview=find('.workspace-overview');
 // A rapid reopening continues from the still-visible exit, while docked
 // continues to describe the live UI state (never the inert visual copy).
 const exitAgent=!liveAgent?[...ghosts].at(-1)?.children[0]:null,agent=liveAgent||exitAgent;
 return {
  mainClass:main?.className||'',nav:pillSnapshot(find('.topbar nav'),'.nav-selection'),tabs:pillSnapshot(tabTrack,'.workspace-selection'),
  scene:key(tile),sceneIndex:tile?[...tile.parentElement.querySelectorAll('.scene-tile')].indexOf(tile):-1,
  version:key(find('.version-chip.active'))||find('.preview-stage video')?.getAttribute('src')||'',
  marker:{...measure(find('.flow-scene-marker')),local:localRect(find('.flow-scene-marker'),find('.scene-rail')),axis:find('.scene-rail')?.dataset.flowAxis},rail:measure(find('.scene-rail')),
  sceneSelection:{...measure(find('.flow-scene-selection')),local:localRect(find('.flow-scene-selection'),find('.scene-rail'))},
  layout:shell?{main:measure(main),shell:measure(shell),board:measure(find('#piece-board')),overview:measure(overview),columns:getComputedStyle(shell).gridTemplateColumns.split(/\s+/).map(parseFloat),position:find('.workspace-layout')?.dataset.agentPosition||'content',motion:layoutMotions.get(shell),moving:moving(main)||moving(shell)||moving(overview)||moving(agent)}:null,
  agent:agent?{...measure(agent),exiting:!!exitAgent,opacity:parseFloat(getComputedStyle(agent).opacity)||0,scroll:['.agent-history','.agent-composer textarea'].map(selector=>{const node=find(selector,agent);return {selector,top:node?.scrollTop||0,left:node?.scrollLeft||0,following:selector==='.agent-history'&&node?node._followTail!==false:false};})}:null,conversation:liveAgent?.dataset.conversation||'',docked:liveAgent?.classList.contains('agent-docked')||false,
 };
}

// Use the available first viewport, then grow naturally as the page scrolls.
// Native sticky positioning supplies the lower content boundary; the chat
// must never add height to the editor merely to fit an arbitrary minimum.
export function dockViewportHeight({top,bottom,viewportHeight,scrollTop=0,inset=24}){
 const visibleTop=Math.max(inset,top-scrollTop);
 return Math.max(0,Math.min(bottom-top,viewportHeight-inset-visibleTop));
}

export function captureFlow(){
 cancelAnimationFrame(frame);frame=0;
 // Read the presentation geometry before cancelling so a second click has no jump back.
 before=snapshot();
 disconnect();cancelMotion();
}

function installPill(track,active,className,old){
 if(!track||!active)return;
 track.querySelectorAll(`.${className}`).forEach(node=>node.remove());
 const pill=document.createElement('span');pill.className=className;pill.setAttribute('aria-hidden','true');
 track.prepend(pill);
 if(className==='workspace-selection')track.classList.add('has-flow-selection');
 const place=()=>Object.assign(pill.style,{left:active.offsetLeft+'px',top:active.offsetTop+'px',width:active.offsetWidth+'px',height:active.offsetHeight+'px'});
 place();
 const target=localRect(pill,track);
 if(old?.local&&target.width&&old.trackWidth&&Math.abs(old.trackWidth-track.clientWidth)<2&&(old.key!==key(active)||old.moving)){
  const dx=old.local.x-target.x,dy=old.local.y-target.y,sx=old.local.width/target.width;
  if(Math.abs(dx)>.5||Math.abs(dy)>.5||Math.abs(sx-1)>.01)animate(pill,[{transform:`translate(${dx}px,${dy}px) scaleX(${sx})`},{transform:'none'}],{duration:440});
 }
 const observer=new ResizeObserver(place);observer.observe(track);observer.observe(active);observers.add(observer);
 // Keep the selected item reachable in the horizontally scrolling navigation.
 if(active.offsetLeft<track.scrollLeft)track.scrollLeft=active.offsetLeft;
 else if(active.offsetLeft+active.offsetWidth>track.scrollLeft+track.clientWidth)track.scrollLeft=active.offsetLeft+active.offsetWidth-track.clientWidth+6;
}

function installSceneMarker(old,current){
 const rail=find('.scene-rail'),tile=find('.scene-tile.selected');
 if(!rail||!tile)return;
 rail.querySelectorAll('.flow-scene-marker').forEach(node=>node.remove());
 rail.querySelectorAll('.flow-scene-selection').forEach(node=>node.remove());
 rail.style.position='relative';
 // Read the existing selected appearance before making that button transparent.
 // Suppress its colour transition while sampling, or a reused rail would yield
 // the transparent start of a transition instead of the light/dark theme style.
 const selection=document.createElement('span');
 selection.className='flow-scene-selection';selection.setAttribute('aria-hidden','true');
 Object.assign(selection.style,{position:'absolute',pointerEvents:'none',zIndex:'0',boxSizing:'border-box',transformOrigin:'top left'});
 rail.append(selection);
 const appearance=()=>{
  const restoreTransition=holdStyle(tile,{transition:'none'});
  rail.classList.remove('has-flow-scene-selection');
  const selectedStyle=getComputedStyle(tile);
  Object.assign(selection.style,{background:selectedStyle.background,borderWidth:selectedStyle.borderWidth,borderStyle:selectedStyle.borderStyle,borderColor:selectedStyle.borderColor,borderRadius:selectedStyle.borderRadius,boxShadow:selectedStyle.boxShadow});
  rail.classList.add('has-flow-scene-selection');
  // Flush the transparent button while transitions are still disabled.
  getComputedStyle(tile).backgroundColor;restoreTransition();
 };
 appearance();
 // Appearance switches do not rerender the board. Resample the actual theme
 // rather than leaving a light selection behind in dark mode (or vice versa).
 const themeObserver=new MutationObserver(appearance);
 themeObserver.observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});observers.add(themeObserver);
 const marker=document.createElement('span');marker.className='flow-scene-marker';marker.setAttribute('aria-hidden','true');
 Object.assign(marker.style,{position:'absolute',pointerEvents:'none',zIndex:'2',borderRadius:'999px',background:'var(--accent)',boxShadow:'none',transformOrigin:'top left'});
 rail.append(marker);
 const place=()=>{
  const horizontal=getComputedStyle(rail).display==='flex';
  rail.dataset.flowAxis=horizontal?'horizontal':'vertical';
  const r=rail.getBoundingClientRect(),t=tile.getBoundingClientRect();
  Object.assign(selection.style,{left:t.left-r.left+rail.scrollLeft+'px',top:t.top-r.top+rail.scrollTop+'px',width:t.width+'px',height:t.height+'px'});
  const length=Math.min(88,Math.max(48,(horizontal?t.width:t.height)*.55));
  Object.assign(marker.style,horizontal?{left:t.left-r.left+rail.scrollLeft+(t.width-length)/2+'px',top:t.bottom-r.top+rail.scrollTop+'px',width:length+'px',height:'3px'}:{left:t.left-r.left+rail.scrollLeft-3+'px',top:t.top-r.top+rail.scrollTop+(t.height-length)/2+'px',width:'3px',height:length+'px'});
 };
 place();
 const target=localRect(marker,rail),source=old?.marker?.local;
 const changed=old?.scene&&old.marker.axis===rail.dataset.flowAxis&&(old.scene!==current.scene||old.marker.moving||old.sceneSelection?.moving);
 if(source&&changed){
  const dx=source.x-target.x,dy=source.y-target.y,sx=source.width/target.width,sy=source.height/target.height,horizontal=rail.dataset.flowAxis==='horizontal';
  // Follow the visible marker, including interrupted transitions and rail
  // scrolling. Only the little indicator stretches; the selected tile stays put.
  animate(marker,[
   {transform:`translate(${dx}px,${dy}px) scale(${sx},${sy})`},
   {offset:.45,transform:`translate(${dx*.4}px,${dy*.4}px) scale(${horizontal?1.35:1},${horizontal?1:1.35})`},
   {transform:'none'}
  ],{duration:560});
 }
 const previous=old?.sceneSelection?.local,destination=localRect(selection,rail);
 if(previous&&changed){
  const dx=previous.x-destination.x,dy=previous.y-destination.y,sx=previous.width/destination.width,sy=previous.height/destination.height,horizontal=rail.dataset.flowAxis==='horizontal';
  animate(selection,[
   {transform:`translate(${dx}px,${dy}px) scale(${sx},${sy})`},
   {offset:.45,transform:`translate(${dx*.4}px,${dy*.4}px) scale(${horizontal?1.025:1},${horizontal?1:1.025})`},
   {transform:'none'}
  ],{duration:560});
 }
 const observer=new ResizeObserver(place);observer.observe(rail);observer.observe(tile);observers.add(observer);
}

function leaveDock(old,{duration=230}={}){
 if(!old?.node||!old.rect||!canMove())return;
 const {x,y,width,height}=old.rect;
 const ghost=old.node.cloneNode(true);
 ghost.classList.add('flow-exit');ghost.setAttribute('aria-hidden','true');ghost.inert=true;
 [ghost,...ghost.querySelectorAll('[id]')].forEach(node=>node.removeAttribute('id'));
 // This is a brief inert visual only. It must never duplicate a player or a live region.
 ghost.querySelectorAll('video,audio,iframe').forEach(node=>node.remove());
 ghost.querySelectorAll('[aria-live]').forEach(node=>node.removeAttribute('aria-live'));
 Object.assign(ghost.style,{position:'fixed',left:x+'px',top:y+'px',width:width+'px',height:height+'px',maxWidth:'none',margin:'0',pointerEvents:'none',zIndex:'30',overflow:'hidden'});
 // Keep the dock's scoped typography and spacing during its exit. The host
 // carries no layout box and stays outside #app, so it is never a live agent.
 const host=document.createElement('div');host.className='workspace-shell';host.style.display='contents';host.setAttribute('aria-hidden','true');host.inert=true;
 host.append(ghost);document.body.append(host);ghosts.add(host);
 for(const saved of old.scroll||[]){const node=find(saved.selector,ghost);if(node){node.scrollTop=saved.top;node.scrollLeft=saved.left;if(saved.selector==='.agent-history')node._followTail=saved.following;}}
 const a=animate(ghost,[{opacity:old.opacity??1,transform:'none'},{opacity:0,transform:'translateX(16px)'}],{duration});
 const remove=()=>{host.remove();ghosts.delete(host);};
 if(a)a.finished.then(remove,remove);else remove();
 return a;
}
function holdStyle(node,values){
 const previous=Object.keys(values).map(name=>[name,node.style.getPropertyValue(name),node.style.getPropertyPriority(name)]);
 for(const [name,value] of Object.entries(values))node.style.setProperty(name,value);
 let restored=false;
 const restore=()=>{
  if(restored)return;restored=true;layoutCleanups.delete(restore);
  for(const [name,value,priority] of previous)if(value)node.style.setProperty(name,value,priority);else node.style.removeProperty(name);
 };
 layoutCleanups.add(restore);return restore;
}
function resizeWidth(current,old,timing=dockTiming){
 if(!current?.rect||!old?.rect||Math.abs(current.rect.width-old.rect.width)<.5)return;
 // Width, rather than scaleX, lets text and media keep their actual sizes.
 return animate(current.node,[{width:old.rect.width+'px',maxWidth:old.rect.width+'px'},{width:current.rect.width+'px',maxWidth:current.rect.width+'px'}],timing);
}
function preserveReadingPosition(node,saved){
 const history=find('.agent-history',node);
 if(!history||!saved)return {update(){},stop(){}};
 let active=true;
 const update=()=>{
  if(!active)return;
  const bottom=Math.max(0,history.scrollHeight-history.clientHeight);
  history.scrollTop=saved.following?bottom:Math.min(saved.top,bottom);
  history.scrollLeft=saved.left;
  // The normal scroll listener must not mistake a height correction for a
  // reader scrolling up. Real input immediately hands control back to it.
  history._lastReadTop=history.scrollTop;history._followTail=saved.following;
 };
 const observer=new ResizeObserver(update);
 const inputs=['wheel','touchstart','pointerdown','keydown'];
 const stop=()=>{
  if(!active)return;active=false;observer.disconnect();layoutCleanups.delete(stop);
  for(const event of inputs)history.removeEventListener(event,stop);
 };
 for(const event of inputs)history.addEventListener(event,stop,{passive:true});
 observer.observe(history);layoutCleanups.add(stop);
 return {update,stop};
}
function moveDock(current,old,{timing=dockTiming,preserveReading=false,fitLayout}={}){
 if(!current.agent)return;
 const target=current.agent.rect,continuing=old.docked||old.agent?.exiting;
 const source=continuing&&old.agent?old.agent.rect:target,node=current.agent.node;
 // Keep the live chat in its native grid/sticky context, including reopening.
 // A viewport-fixed child jumps when an ancestor is animated or a scroll is
 // restored. Holding only its real size prevents a growing track squeezing it.
 const restore=holdStyle(node,{height:source.height+'px',...(preserveReading?{}:{width:target.width+'px','max-width':'none','justify-self':'start'})});
 fitLayout?.();
 const native=rect(node);
 const reading=preserveReading||old.agent?.exiting?preserveReadingPosition(node,old.agent?.scroll.find(item=>item.selector==='.agent-history')):null;
 const dx=continuing?source.x-native.x:16,dy=continuing?source.y-native.y:0;
 const a=animate(node,[
  {height:source.height+'px',transform:`translate(${dx}px,${dy}px)`,opacity:continuing?old.agent?.opacity??1:0},
  {height:target.height+'px',transform:'none',opacity:1}
 ],timing);
 reading?.update();
 // Restore geometry before the last scroll correction, including cancellation
 // by a second toggle or reduced motion. A stale finished callback is harmless.
 layoutCleanups.delete(restore);if(reading)layoutCleanups.delete(reading.stop);
 let finished=false;
 const finish=()=>{if(finished)return;finished=true;layoutCleanups.delete(finish);restore();fitLayout?.();reading?.update();reading?.stop();};
 layoutCleanups.add(finish);
 if(a)a.finished.then(finish,finish);else finish();
 return a;
}
function workspaceResize(current,old,fitLayout){
 if(!current.layout||!old.layout)return false;
 const source=old.layout,target=current.layout;
 const reposition=current.docked&&old.docked&&(source.position!==target.position||source.moving&&source.motion==='position');
 const closing=old.docked&&!current.docked;
 // Clear the transparent chat before the editor expands into the same space.
 // fill:both reserves its old columns during that short, coordinated handoff.
 const exitDuration=140;
 const timing=reposition?positionTiming:closing?{...dockTiming,delay:exitDuration,duration:dockDuration-exitDuration}:dockTiming;
 const motion=reposition?'position':'resize',shell=target.shell.node;
 // Hide the divider immediately; its old width must not sweep through a rising chat.
 const divider=reposition?find('.guide-steps.workspace-tabs',target.overview?.node):null;
 const restoreDivider=divider?holdStyle(divider,{'border-bottom-color':'transparent'}):()=>{};
 layoutMotions.set(shell,motion);
 let cleared=false,completion;
 const clearMotion=()=>{if(cleared)return;cleared=true;restoreDivider();layoutMotions.delete(shell);layoutCleanups.delete(clearMotion);};
 layoutCleanups.add(clearMotion);
 completion=resizeWidth(target.main,source.main,timing)||completion;
 completion=resizeWidth(target.overview,source.overview,timing)||completion;
 const sideBySide=source.columns.length===3||target.columns.length===3;
 if(sideBySide){
  const start=source.columns.length===3?source.columns:[source.board?.rect.width||0,0,0];
  const end=target.columns.length===3?target.columns:[target.board?.rect.width||0,0,0];
  // Equal track counts make closing as fluid as opening. The flexible first
  // column follows the main width throughout, so the editor never overflows.
  completion=animate(shell,[{gridTemplateColumns:`minmax(0,1fr) ${start[1]}px ${start[2]}px`},{gridTemplateColumns:`minmax(0,1fr) ${end[1]}px ${end[2]}px`}],timing);
 }
 if(Math.abs(source.shell.rect.height-target.shell.rect.height)>.5)completion=animate(shell,[{minHeight:source.shell.rect.height+'px'},{minHeight:target.shell.rect.height+'px'}],timing)||completion;
 if(current.docked)completion=moveDock(current,old,{timing,preserveReading:reposition,fitLayout})||completion;
 else if(old.docked){const exit=leaveDock(old.agent,{duration:exitDuration});completion=completion||exit;}
 if(completion)completion.finished.then(clearMotion,clearMotion);else clearMotion();
 return true;
}
function pageEntrance(current,old,{tabChanged=false}={}){
 const main=find('#app>main');if(!main)return;
 const order=tabChanged?current.tabs?.order||[]:['home','conversation','workshop','brands','library','picks','activity'];
 const from=order.indexOf(tabChanged?old?.tabs?.key:old?.nav?.key),to=order.indexOf(tabChanged?current.tabs?.key:current.nav?.key);
 const direction=from>=0&&to>=0&&to<from?-1:1;
 const gentle='cubic-bezier(.22,.72,.2,1)';
 // The title, step controls and conversation are shared between steps. Only the
 // intro and content change; they travel together, without nested transforms.
 const content=find('#piece-board>.guided-studio');
 const targets=tabChanged&&content?[find('.workspace-overview .guide-intro'),content]:[main];
 for(const node of targets)animate(node,[{opacity:.25,transform:`translateX(${direction*28}px)`},{opacity:1,transform:'none'}],{duration:860,easing:gentle});
}

export function settleFlow({routeChanged=false,fitLayout}={}){
 cancelAnimationFrame(frame);
 const old=before;
 // applyLayout queues its width calculations first. Measure only after that callback.
 frame=requestAnimationFrame(()=>{
  frame=0;
  // render restores document scroll after applyLayout. Fit once more at that
  // final scroll position before sampling the animation destination.
  fitLayout?.();
  const current=snapshot(),nav=find('.topbar nav'),active=find('.nav-link.active',nav);
  nav?.querySelectorAll('.nav-link').forEach(node=>node.setAttribute('aria-current',node===active?'page':'false'));
  installPill(nav,active,'nav-selection',old?.nav);
  const tabs=find('.workspace-tabs');installPill(tabs,find('button.active',tabs),'workspace-selection',old?.tabs);
  installSceneMarker(old,current);
  if(!canMove())return;
  const sameWorkspace=current.mainClass==='piece-main'&&old?.mainClass==='piece-main';
  const tabChanged=sameWorkspace&&old.tabs?.key&&current.tabs?.key&&old.tabs.key!==current.tabs.key;
  const dockChanged=sameWorkspace&&current.docked!==old.docked;
  const dockPositionChanged=sameWorkspace&&current.docked&&old.docked&&current.layout?.position!==old.layout?.position;
  const sceneChanged=sameWorkspace&&old.scene&&current.scene&&old.scene!==current.scene;
  const versionChanged=sameWorkspace&&old.scene===current.scene&&old.version!==current.version;
  if(routeChanged||tabChanged){
   pageEntrance(current,old,{tabChanged});
  }else if(dockChanged||dockPositionChanged||sameWorkspace&&old.layout?.moving&&!sceneChanged&&!versionChanged){
   if(!workspaceResize(current,old,fitLayout)){
    if(current.docked)animate(current.agent?.node,[{opacity:0,transform:'translateX(16px)'},{opacity:1,transform:'none'}],{duration:dockDuration});
    else if(!current.agent)leaveDock(old.agent,{duration:dockDuration});
   }
  }else if(sceneChanged||versionChanged){
   const direction=sceneChanged&&current.sceneIndex<old.sceneIndex?-1:1;
   const nodes=[find('.scene-canvas'),...(sceneChanged?[find('.direction-panel')]:[])];
   for(const node of nodes)enter(node,{distance:direction*10,opacity:.35,duration:480});
  }else if(old?.conversation&&old.conversation!=='new'&&current.conversation&&old.conversation!==current.conversation){
   enter(find('.agent-history'),{distance:12,duration:300});
  }
 });
}

document.addEventListener('visibilitychange',()=>{
 if(document.hidden){cancelAnimationFrame(frame);frame=0;cancelMotion();}
 else{captureFlow();settleFlow();} // Rebuild static indicators if a hidden frame was cancelled.
});
media.addEventListener('change',()=>{if(media.matches)cancelMotion();});
