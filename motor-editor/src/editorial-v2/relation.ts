import measured from '../../../estilo-editor/datos/revision-v2/v8-selector-curves.json' with {type:'json'};
import type {Word,Node,Job} from '../types.ts';
import {fitText,textWidth} from '../text.ts';
import {frameAt} from '../motion.ts';

export type RelationInput={
  kind:'replacement'|'equivalence';
  fromWordIds:string[];toWordIds:string[];
  beforeContextWordIds?:string[];afterContextWordIds?:string[];
  reason:string;
};
export type RelationScene={
  kind:RelationInput['kind'];from:string;to:string;beforeContext:string;afterContext:string;
  start:number;end:number;closeStart:number;oldTextAt:number;newTextAt:number;newContextAt:number;
  width:number;height:number;fontSize:number;fontWeight:400;contextSize:number;tracking:number;
  inkColor:string;accent:string;
  provenance:{handleWidth:'native-measurements-interpolated';typography:'authored';alpha:'authored';textTranslation:'authored';source:string};
};
const SOURCE_FPS=measured.fps.num/measured.fps.den;
const points=measured.rows.filter(r=>r.frame>=230&&r.frame<=300).map(r=>{
  const a=r.threshold50,b=r.threshold70;
  if(!a.handles.every(h=>h.reliable)||!b.handles.every(h=>h.reliable)||a.separationX===null||b.separationX===null)throw Error(`Unreliable selector measurement ${r.frame}`);
  return {frame:r.frame,width:(a.separationX+b.separationX)/2/810};
});
/** Only handle separation was measured. Interpolation between decoded frames is a model. */
export function selectionWidthAt(sourceFrame:number):number{
  if(!Number.isFinite(sourceFrame))throw Error('Invalid source time');
  if(sourceFrame<=230)return 1;if(sourceFrame>=300)return 1;
  const i=Math.floor(sourceFrame)-230,p=sourceFrame-Math.floor(sourceFrame);
  return points[i].width*(1-p)+points[i+1].width*p;
}
const clamp=(n:number)=>Math.max(0,Math.min(1,n));
export function relationState(s:RelationScene,t:number,contextTime=t){
  if(!Number.isFinite(t)||!Number.isFinite(contextTime))throw Error('Invalid relation time');
  const sourceFrame=230+(t-s.closeStart)*SOURCE_FPS;
  const visible=t>=s.start&&t<s.end;
  const newAge=t-s.newTextAt,newContextAge=contextTime-s.newContextAt;
  // A discrete text replacement must not mix two strings across shutter samples.
  // Geometry still evaluates at fractional t; context evaluates at the presentation frame.
  const contextFrame=230+(contextTime-s.closeStart)*SOURCE_FPS;
  const old=visible&&t>=s.oldTextAt&&sourceFrame<258;
  const fresh=visible&&newAge>=0;
  return {
    visible,sourceFrame,width:s.width*selectionWidthAt(sourceFrame),glyphScaleX:1,
    fromOpacity:old?1:0,toOpacity:fresh?clamp(newAge/.065):0,
    toY:fresh?s.height*.26*(1-clamp(newAge/.22))**4:0,
    context:contextFrame<=230?s.beforeContext:contextFrame<258?(s.kind==='equivalence'?'=':''):s.afterContext,
    contextOpacity:contextFrame<258?1:clamp(newContextAge/.065),
    phase:!visible?'off':sourceFrame<=230?'read-before':sourceFrame<255?'close':sourceFrame<258?'bridge':sourceFrame<300?'open':'read-after',
    provenance:sourceFrame>=230&&sourceFrame<=300?'measured-width-interpolation':'authored-hold',
  };
}

export function prepareRelation(input:RelationInput,words:Word[],job:Job):{scene?:RelationScene;reason?:string}{
  const invalid=(reason:string)=>({reason});
  if(!['replacement','equivalence'].includes(input.kind)||!input.reason?.trim())return invalid('Relation requires a supported meaning and an editorial reason.');
  const ids=[...(input.beforeContextWordIds??[]),...input.fromWordIds,...(input.afterContextWordIds??[]),...input.toWordIds];
  if(!input.fromWordIds.length||!input.toWordIds.length||new Set(ids).size!==ids.length||ids.length!==words.length||ids.some(id=>!words.some(w=>w.id===id)))return invalid('Relation must bind each spoken unit exactly once; no invented, missing or duplicated words.');
  const group=(ids:string[])=>words.filter(w=>ids.includes(w.id));
  const old=group(input.fromWordIds),fresh=group(input.toWordIds),before=group(input.beforeContextWordIds??[]),after=group(input.afterContextWordIds??[]);
  const contiguous=(ws:Word[])=>ws.every((w,i)=>!i||words.indexOf(w)===words.indexOf(ws[i-1])+1);
  if(![old,fresh,before,after].every(contiguous))return invalid('Relation groups must be contiguous spoken units.');
  if(old.at(-1)!.end>fresh[0].start||(before.length&&before.at(-1)!.end>old[0].start)||(after.length&&(after[0].start<old.at(-1)!.end||after.at(-1)!.end>fresh[0].start)))return invalid('Relation order contradicts the speech.');
  const text=(ws:Word[])=>ws.map(w=>w.text).join(' ');
  const from=text(old),to=text(fresh),W=job.format.width;
  // A stable optical size and full-width window; the glyphs never scale horizontally.
  const fontSize=Math.min(fitText(from,W*.72,W*.21,-.035,400),fitText(to,W*.72,W*.21,-.035,400));
  if(fontSize<W*.09)return invalid('Terms too long for a readable shared window.');
  const end=words.at(-1)!.end,newTextAt=fresh[0].start,closeStart=newTextAt-(266-230)/SOURCE_FPS;
  const openEnd=closeStart+(300-230)/SOURCE_FPS;
  const reopenStart=closeStart+(258-230)/SOURCE_FPS;
  // Authored speech safeguards: decline this choreography rather than delay a spoken context
  // or erase a term whose spoken unit has not finished. These are not measured editor rules.
  if(old.at(-1)!.end>closeStart)return invalid('Source term still spoken when the window starts closing.');
  if(after.length&&after[0].start<reopenStart)return invalid('New context precedes the available context track; redesign instead of delaying speech.');
  const minBefore=Math.max(.32,from.length*.025),minAfter=Math.max(.32,to.length*.025);
  if(closeStart-old.at(-1)!.start<minBefore||end-Math.max(openEnd,fresh.at(-1)!.start)<minAfter)return invalid('Insufficient reading time around the measured close/open; do not accelerate it to fit.');
  // No early display of later words inside either term: multi-unit terms need an explicit animation graph.
  if(old.length!==1||fresh.length!==1||before.length>1||after.length>1)return invalid('Multi-unit relation labels need separate reveal bindings; do not anticipate speech.');
  const contextSize=Math.min(W*.16,fitText(text(before),W*.72,W*.16,-.035,400),fitText(text(after),W*.72,W*.16,-.035,400));
  const width=Math.max(textWidth(from,fontSize,-.035,400),textWidth(to,fontSize,-.035,400))+W*.045;
  return {scene:{kind:input.kind,from,to,beforeContext:text(before),afterContext:text(after),start:words[0].start,end,closeStart,oldTextAt:old[0].start,newTextAt,newContextAt:after[0]?.start??newTextAt,width,height:fontSize*1.14,fontSize,fontWeight:400,contextSize,tracking:-.035,inkColor:job.options?.palette?.foreground??'#fffdf1',accent:job.options?.palette?.accent??'#dcf395',provenance:{handleWidth:'native-measurements-interpolated',typography:'authored',alpha:'authored',textTranslation:'authored',source:'estilo-editor/datos/revision-v2/v8-selector-curves.json'}}};
}
export function relationNode(input:RelationInput,words:Word[],job:Job,id:string):Node{
  const prepared=prepareRelation(input,words,job);if(!prepared.scene)throw Error(prepared.reason);
  const s=prepared.scene;
  // Include context and handle discs in the protected-layout envelope.
  const height=s.height+s.contextSize*2+job.format.width*.04;
  const width=Math.max(s.width,textWidth(s.beforeContext,s.contextSize,s.tracking,400),textWidth(s.afterContext,s.contextSize,s.tracking,400))+job.format.width*.04;
  return {id,kind:'relation',relation:s,x:0,y:0,width,height:height*2,start:frameAt(s.start,job.format.fps),end:frameAt(s.end,job.format.fps),z:50,wordIds:words.map(w=>w.id),motionLabel:'measured-clip-window-with-authored-text-tracks',motionBlur:{samples:8,angle:180}};
}
