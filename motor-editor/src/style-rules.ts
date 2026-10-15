import type {Node,Plan,Diagnostic} from './types.ts';
import {state,fpsValue} from './motion.ts';
import inkMetrics from '../data/font-ink-bold.json' with {type:'json'};

// Ale, Birdieballs V02 feedback, 2026-10-10. Pixel tuning is an implementation
// hypothesis; the stable anchor and compact hierarchy are explicit preferences.
export function compactHierarchy(nodes:Node[],anchor:{x:number;y:number},accent:string,stroke:string,gap=8){
 const ink=(n:Node)=>{const boxes=Array.from(n.text??'').filter(c=>c.trim()).map(c=>(inkMetrics as Record<string,{top:number;bottom:number}>)[c]??{top:-.5,bottom:.5});return {top:Math.min(0,...boxes.map(b=>b.top))*(n.fontSize??0),bottom:Math.max(0,...boxes.map(b=>b.bottom))*(n.fontSize??0)};};
 const ys=[anchor.y];for(let i=1;i<nodes.length;i++)ys.push(ys[i-1]+ink(nodes[i-1]).bottom-ink(nodes[i]).top+gap+3);
 nodes.forEach((n,i)=>{n.x=anchor.x;n.y=ys[i];if(i){n.fill=accent;n.stroke=stroke;n.strokeWidth=2.5;n.shadow={color:stroke,x:0,y:4,blur:1.5};}});
}
export function auditStyle(plan:Plan):Diagnostic[]{
 const diagnostics:Diagnostic[]=[];
 for(const g of plan.graphics.filter(g=>g.fullScreen)){
  if(!g.nodes.some(n=>n.role==='background-texture'&&n.kind==='image'))diagnostics.push({severity:'warning',code:'ALE_FLAT_BACKGROUND',clauseId:g.clauseId,message:'Fondo sin textura declarada: revisar material, luz y profundidad según feedback Birdieballs V02.'});
  for(const n of g.nodes.filter(n=>n.role==='subject')){
   let still=0,longest=0;const F=fpsValue(plan.fps);
   for(let frame=n.start+1;frame<n.end;frame++){
    const a=state(n.motion,frame-1),b=state(n.motion,frame),ca=state(g.camera,frame-1),cb=state(g.camera,frame);
    const change=Math.hypot(b.x-a.x+cb.x-ca.x,b.y-a.y+cb.y-ca.y)+Math.abs(b.scale-a.scale+cb.scale-ca.scale)*(n.width??300)+Math.abs(b.rotate-a.rotate+cb.rotate-ca.rotate)*2;
    still=change<.5?still+1:0;longest=Math.max(longest,still);
   }
   if(longest/F>.65)diagnostics.push({severity:'warning',code:'ALE_STATIC_SUBJECT',clauseId:g.clauseId,message:`${n.id}: ${(longest/F).toFixed(2)} s sin acción perceptible. Diseñar un cambio ligado a la frase; no añadir oscilación de relleno.`});
  }
 }
 return diagnostics;
}
