// One text node, one transition at a time. New events replace the pending target.
const transitions=new WeakMap();
export function changeThinkingText(label,value,{reduced=false,update=fn=>fn(),wait=ms=>new Promise(resolve=>setTimeout(resolve,ms))}={}){
 if(!label)return Promise.resolve();
 let state=transitions.get(label);
 if(state){state.target=value;state.reduced=reduced;return state.promise;}
 if(label.textContent===value)return Promise.resolve();
 state={target:value,reduced,promise:null};transitions.set(label,state);
 state.promise=(async()=>{
  while(label.isConnected&&label.textContent!==state.target){
   if(state.reduced){update(()=>{label.textContent=state.target;});break;}
   // Erase completely before writing; no overlapping layers or retained glyphs.
   while(label.isConnected&&label.textContent){
    update(()=>{label.textContent=Array.from(label.textContent).slice(0,-1).join('');});
    await wait(12);
   }
   if(!label.isConnected)break;
   let written='';const target=state.target;
   for(const letter of Array.from(target)){
    if(!label.isConnected||state.target!==target)break;
    written+=letter;update(()=>{label.textContent=written;});await wait(20);
   }
  }
 })().finally(()=>transitions.delete(label));
 return state.promise;
}
