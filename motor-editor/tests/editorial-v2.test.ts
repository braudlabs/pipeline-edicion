import test from 'node:test';
import assert from 'node:assert/strict';
import {compileEditorial,type EditorialSpec} from '../src/editorial-v2/index.ts';
import type {Job} from '../src/types.ts';
import {createReferenceEntrance} from '../src/caption-keyframes/reference-v2.ts';
const fixture=()=>{
  const job:Job={version:1,id:'editorial-test',family:'braud',format:{width:1080,height:1920,fps:{num:60,den:1}},assets:[{id:'source',kind:'video',src:'source.mp4',duration:20}],words:[{id:'a',text:'ni',start:0,end:.2},{id:'b',text:'me',start:.2,end:.4},{id:'c',text:'han',start:.4,end:.6},{id:'d',text:'pagado',start:.6,end:1.5}],clauses:[{id:'c1',wordIds:['a','b','c','d']}]};
  const spec:EditorialSpec={version:2,source:{assetId:'source',sourceStart:2,durationInFrames:180},annotations:[{clauseId:'c1',layoutId:'statement',function:'emphasis',focusWordIds:['d'],observation:{kind:'agent',reason:'Semantic predicate is the punchline; support remains readable.'}}]};
  return {job,spec};
};
test('semantic emphasis creates a compact stack with retained context and no duplicate word ownership',()=>{
  const {job,spec}=fixture(),p=compileEditorial(job,spec);
  assert.equal(p.editorial.decisions[0].treatment,'stack');assert.equal(p.captions.length,0);
  const ns=p.graphics[0].nodes;assert.equal(ns.length,4);assert.equal(ns[0].y,ns[2].y);assert.ok(ns[3].fontSize!>ns[0].fontSize!*2);
  assert.ok(ns[0].end>ns[3].start);assert.ok(ns[3].motion);assert.equal(ns[3].motionLabel,'authored-rise-to-avoid-context-collision');
  assert.ok(p.coverage.every(w=>w.representations.length===1));
});
test('number alone does not trigger count, full-screen, scale promotion or masking',()=>{
  const {job,spec}=fixture();job.words[3].text='300';spec.annotations[0].function='ordinary';
  job.assets.push({id:'cutout',kind:'video',src:'alpha.webm',duration:20});
  job.shots=[{id:'s',assetId:'source',sourceStart:0,sourceEnd:20,tags:[],cutoutAssetId:'cutout'}];
  const p=compileEditorial(job,spec);assert.equal(p.editorial.decisions[0].treatment,'rail');
  assert.ok(p.graphics.every(g=>!g.fullScreen&&!g.cutout&&g.nodes.every(n=>!n.counter&&!n.referenceEntrance)));
});
test('wide ordinary word is still a rail and preserves the block anchor',()=>{
  const {job,spec}=fixture();job.words[3].text='automáticamente';spec.annotations[0].function='ordinary';
  const p=compileEditorial(job,spec),ns=p.graphics[0].nodes;
  assert.equal(p.editorial.decisions[0].treatment,'rail');assert.ok(ns.every(n=>n.y===ns[0].y));assert.ok(ns[3].fontSize!<=ns[0].fontSize!);
});
test('locked source preserves full duration, trailing silence, source offset and audio',()=>{
  const {job,spec}=fixture(),p=compileEditorial(job,spec);
  assert.equal(p.durationInFrames,180);assert.deepEqual(p.clips.map(c=>[c.start,c.end,c.sourceStart,c.mute]),[[0,180,2,false]]);
});
test('global sequence varies compatible constructions without random movement or forced variety in ordinary rail',()=>{
  const {job,spec}=fixture();job.words.push(...job.words.map(w=>({...w,id:w.id+'2',start:w.start+1.5,end:w.end+1.5})));job.clauses!.push({id:'c2',wordIds:['a2','b2','c2','d2']});
  spec.annotations.push({...spec.annotations[0],clauseId:'c2',focusWordIds:['d2']});
  const p=compileEditorial(job,spec);assert.deepEqual(new Set(p.editorial.decisions.map(d=>d.treatment)),new Set(['stack','inline']));
  assert.deepEqual(p.editorial.decisions[0].anchor,p.editorial.decisions[1].anchor);
  spec.annotations.forEach(a=>a.function='ordinary');assert.deepEqual(compileEditorial(job,spec).editorial.decisions.map(d=>d.treatment),['rail','rail']);
});
test('a protected region arriving later relocates the whole group before its first word',()=>{
  const {job,spec}=fixture();spec.annotations[0].function='ordinary';spec.annotations[0].preferredAnchor=[.5,.56];
  spec.annotations[0].avoid=[{start:.7,end:1.5,rect:{x:0,y:.5,width:1,height:.12},reason:'Mouth enters this area later.'}];
  const p=compileEditorial(job,spec),ns=p.graphics[0].nodes;assert.notEqual(ns[0].y,1920*.56);assert.ok(ns.every(n=>n.y===ns[0].y));
});
test('impossible protected geometry fails instead of covering the actor or silently omitting speech',()=>{
  const {job,spec}=fixture();spec.annotations[0].avoid=[{start:0,end:2,rect:{x:0,y:0,width:1,height:1},reason:'All frame protected.'}];
  assert.throws(()=>compileEditorial(job,spec),/no safe anchor/);
});
test('short emphasis falls back without stretching the reference entrance',()=>{
  const {job,spec}=fixture();job.words[3].end=.8;
  const p=compileEditorial(job,spec);assert.notEqual(p.editorial.decisions[0].treatment,'stack');assert.ok(p.graphics[0].nodes.every(n=>!n.referenceEntrance));
});
test('noncontiguous focus cannot invent a combined headline that changes word order',()=>{
  const {job,spec}=fixture();spec.annotations[0].focusWordIds=['a','c'];
  assert.notEqual(compileEditorial(job,spec).editorial.decisions[0].treatment,'stack');
});
test('visual omission is explicit and records semantic coverage rather than disappearing silently',()=>{
  const {job,spec}=fixture();spec.annotations[0].function='visual-action';
  assert.equal(compileEditorial(job,spec).editorial.decisions[0].treatment,'rail');
  spec.annotations[0].omitReason='Physical gag carries the moment; retain voice.';
  const p=compileEditorial(job,spec);assert.equal(p.graphics.length,0);assert.ok(p.coverage.every(c=>c.representations[0]==='silence:c1'));
});
test('relationship request reports unfinished graphic design instead of treating a stock counter as final',()=>{
  const {job,spec}=fixture();spec.annotations[0].function='explain-relation';
  const p=compileEditorial(job,spec);assert.equal(p.editorial.decisions[0].needsDesign,true);assert.ok(p.diagnostics.some(d=>d.code==='EDITORIAL_DESIGN_REQUIRED'));
});
test('deterministic compilation, provenance, and unchanged input',()=>{
  const {job,spec}=fixture(),before=JSON.stringify({job,spec}),a=compileEditorial(job,spec),b=compileEditorial(job,spec);
  assert.deepEqual(a,b);assert.equal(JSON.stringify({job,spec}),before);assert.ok(a.editorial.decisions[0].evidence.length);
  spec.annotations[0].focusWordIds=['a'];const alternate=compileEditorial(job,spec);
  const n=alternate.graphics[0].nodes.find(n=>n.referenceEntrance)!,m=createReferenceEntrance(n.referenceEntrance!.profile,n.referenceEntrance!.spec);
  assert.equal(m.atFrame(n.end,{num:60,den:1},1920).opacity,0);
});
test('source window, malformed context and external focus reject before producing a plan',()=>{
  const {job,spec}=fixture();spec.source.durationInFrames=1800;assert.throws(()=>compileEditorial(job,spec),/duration/);
  spec.source.durationInFrames=180;spec.annotations[0].focusWordIds=['unknown'];assert.throws(()=>compileEditorial(job,spec),/Focus/);
  spec.annotations=[];assert.throws(()=>compileEditorial(job,spec),/annotation/);
});
