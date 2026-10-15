import test from 'node:test';
import assert from 'node:assert/strict';
import type {Job} from '../src/types.ts';
import {compileEditorial,type EditorialSpec} from '../src/editorial-v2/index.ts';
import {prepareRelation,relationNode,relationState,selectionWidthAt,type RelationInput} from '../src/editorial-v2/relation.ts';
const fixture=()=>{
  const job:Job={version:1,id:'relation-test',family:'braud',format:{width:1080,height:1920,fps:{num:60000,den:1001}},assets:[{id:'v',kind:'video',src:'v.mp4',duration:4}],words:[{id:'pre',text:'Nuevos',start:0,end:.3},{id:'old',text:'clientes',start:.3,end:.9},{id:'post',text:'Nuevos',start:1.5,end:1.6},{id:'new',text:'empleados',start:1.6,end:3}],clauses:[{id:'c',wordIds:['pre','old','post','new']}]};
  const relation:RelationInput={kind:'equivalence',fromWordIds:['old'],toWordIds:['new'],beforeContextWordIds:['pre'],afterContextWordIds:['post'],reason:'Reconstruct the declared comparison in the supplied reference; not a universal equivalence.'};
  const spec:EditorialSpec={version:2,source:{assetId:'v',sourceStart:0,durationInFrames:210},annotations:[{clauseId:'c',layoutId:'comparison',function:'explain-relation',relation,observation:{kind:'agent',reason:'The relation is the information to communicate; no numeric or mask shortcut.'}}]};
  return {job,relation,spec};
};
test('explicit supported relation compiles into the actual render node, with unique speech coverage',()=>{
  const {job,spec}=fixture(),p=compileEditorial(job,spec);
  assert.equal(p.editorial.decisions[0].treatment,'relation');assert.equal(p.editorial.decisions[0].needsDesign,false);
  assert.equal(p.graphics[0].nodes[0].kind,'relation');assert.equal(p.captions.length,0);assert.ok(p.coverage.every(w=>w.representations.length===1));
  assert.deepEqual(p.clips.map(c=>[c.start,c.end,c.sourceStart]),[[0,210,0]]);
});
test('native measured handles close and reopen, while glyph scale stays constant',()=>{
  const {job,relation}=fixture(),s=prepareRelation(relation,job.words,job).scene!;
  for(const [f,px] of [[230,810],[240,201.5],[255,2],[257,2],[270,614],[300,810]])assert.ok(Math.abs(selectionWidthAt(f)*810-px)<=.5);
  for(let f=230;f<=300;f+=.25)assert.equal(relationState(s,s.closeStart+(f-230)*1001/60000).glyphScaleX,1);
});
test('replacement does not invent equality; connector conveys only the declared relationship',()=>{
  const {job,relation}=fixture(),s=prepareRelation(relation,job.words,job).scene!,t=s.closeStart+25*1001/60000;
  assert.equal(relationState(s,t).context,'=');
  const replacement=prepareRelation({...relation,kind:'replacement'},job.words,job).scene!;assert.equal(relationState(replacement,t).context,'');
});
test('neither source term nor replacement appears before its spoken binding',()=>{
  const {job,relation}=fixture(),s=prepareRelation(relation,job.words,job).scene!;
  assert.equal(relationState(s,.1).fromOpacity,0);assert.equal(relationState(s,.31).fromOpacity,1);
  assert.equal(relationState(s,1.59).toOpacity,0);assert.ok(relationState(s,1.65).toOpacity>0);
  assert.equal(relationState(s,s.end).visible,false);
});
test('short available time rejects the graphic without squeezing measured motion',()=>{
  const {job,relation,spec}=fixture();job.words[3].end=1.9;
  assert.match(prepareRelation(relation,job.words,job).reason!,/reading time/);
  const p=compileEditorial(job,spec);assert.equal(p.editorial.decisions[0].treatment,'rail');assert.equal(p.editorial.decisions[0].needsDesign,true);
});
test('missing, duplicated or fabricated speech bindings cannot silently enter the scene',()=>{
  const {job,relation}=fixture();
  for(const invalid of [{...relation,toWordIds:['invented']},{...relation,toWordIds:['old']},{...relation,afterContextWordIds:[]}])assert.match(prepareRelation(invalid,job.words,job).reason!,/bind/);
});
test('label and opacity tracks are deterministic under out-of-order fractional seeks and different output fps',()=>{
  const {job,relation}=fixture(),s=prepareRelation(relation,job.words,job).scene!,t=1.723;
  const before=relationState(s,t);relationState(s,.2);relationState(s,2.9);
  assert.deepEqual(relationState(s,t),before);
  for(const fps of [24,30,60000/1001])assert.ok(Math.abs(relationState(s,(t*fps)/fps).width-before.width)<1e-8);
  for(let t=0;t<s.end;t+=.002){const p=relationState(s,t);assert.ok(!(p.fromOpacity>0&&p.toOpacity>0));}
});
test('mere two concepts or missing intent still do not trigger a graphic',()=>{
  const {job,spec}=fixture();spec.annotations[0].function='ordinary';assert.equal(compileEditorial(job,spec).editorial.decisions[0].treatment,'rail');
  spec.annotations[0].function='explain-relation';delete spec.annotations[0].relation;assert.equal(compileEditorial(job,spec).editorial.decisions[0].needsDesign,true);
});

test('speech that outlasts its track is declined rather than cut off or delayed',()=>{
  const {job,relation}=fixture();job.words[1].end=1.2;
  assert.match(prepareRelation(relation,job.words,job).reason!,/still spoken/);
  job.words[1].end=.9;job.words[2].start=1.3;
  assert.match(prepareRelation(relation,job.words,job).reason!,/context track/);
});

test('shutter samples may blur handles but never mix two discrete context strings',()=>{
  const {job,relation}=fixture(),s=prepareRelation(relation,job.words,job).scene!;
  const frameTime=s.closeStart+.001;
  const samples=[-.004,-.002,0,.002,.004].map(dt=>relationState(s,frameTime+dt,frameTime));
  assert.deepEqual([...new Set(samples.map(p=>p.context))],['=']);
  assert.ok(new Set(samples.map(p=>p.width)).size>1);
  const before=frameTime-.002;
  assert.ok(samples.every((_,i)=>relationState(s,frameTime+i*.001,before).context==='Nuevos'));
});

test('protected layout includes a long context even when both main labels are short',()=>{
  const {job,relation}=fixture();job.words[0].text='Automáticamente';job.words[1].text='IA';job.words[3].text='UX';
  const node=relationNode(relation,job.words,job,'wide-context');
  assert.ok(node.width!>node.relation!.width+1080*.04);
  assert.ok(node.width!>=1080*.72);
});
