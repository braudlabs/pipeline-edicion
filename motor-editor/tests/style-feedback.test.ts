import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {shutterSamples} from '../src/motion.ts';
import {auditStyle} from '../src/style-rules.ts';
import type {Plan} from '../src/types.ts';
const v03=()=>JSON.parse(fs.readFileSync(new URL('../../birdieballs/v03/plan.json',import.meta.url),'utf8')) as Plan;
test('Birdieballs keeps the question anchor when the second line appears',()=>{
 const p=v03(),first=p.captions.find(c=>c.text==='¿Cansado')!,group=p.graphics.find(g=>g.id==='kidney')!;
 assert.equal(group.nodes[0].x,first.x);assert.equal(group.nodes[0].y,first.y);
 assert.ok(group.nodes[1].y>first.y);assert.ok(group.nodes[1].y-first.y<145);
});
test('shutter cannot leak neighbouring shots and is independent of evaluation order',()=>{
 for(const frame of [599,620,755,600,620]){
  const samples=shutterSamples(frame,599,756,8,270);
  assert.equal(samples.reduce((sum,s)=>sum+s.weight,0),1);
  assert.ok(samples.every(s=>s.frame>=599&&s.frame<=755));
  assert.deepEqual(samples,shutterSamples(frame,599,756,8,270));
 }
});
test('style audit catches the rejected static-object and flat-background regression',()=>{
 const p=v03();assert.deepEqual(auditStyle(p),[]);
 const g=p.graphics.find(g=>g.id==='original-ball')!;
 g.nodes=g.nodes.filter(n=>n.role!=='background-texture');
 for(const n of g.nodes.filter(n=>n.role==='subject'))n.motion=undefined;
 const codes=auditStyle(p).map(d=>d.code);
 assert.ok(codes.includes('ALE_FLAT_BACKGROUND'));assert.ok(codes.includes('ALE_STATIC_SUBJECT'));
});
