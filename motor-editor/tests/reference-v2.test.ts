import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createReferenceEntrance,type ReferenceEntrance} from '../src/caption-keyframes/reference-v2.ts';
const profile=JSON.parse(readFileSync(new URL('../../estilo-editor/datos/revision-v2/v8-motion-fit.json',import.meta.url),'utf8'));
const spec:ReferenceEntrance={start:1,end:3,sourceRange:[2,60],initialOffset:52/1920,initialVelocity:-48*(60000/1001)/1920,settleSeconds:6*1001/60000,exit:{kind:'lift',seconds:.1,travel:18/1920}};
const motion=createReferenceEntrance(profile,spec);
test('24/30/59.94 output and shutter subframes preserve wall-clock motion',()=>{
  const t=1.1537,expected=motion.atSeconds(t,1920);
  for(const fps of [{num:24,den:1},{num:30,den:1},{num:60000,den:1001}]){
    const actual=motion.atFrame(t*fps.num/fps.den,fps,1920);
    assert.ok(Math.abs(actual.translationY-expected.translationY)<1e-9);
    assert.ok(Math.abs(actual.velocityPxPerSecond-expected.velocityPxPerSecond)<1e-8);
  }
});
test('geometry scales with canvas height, timing and phase do not',()=>{
  for(const t of [1.01,1.2,2.06,2.5,2.95]){
    const a=motion.atSeconds(t,1920),b=motion.atSeconds(t,960);
    assert.equal(a.translationY,b.translationY*2);assert.equal(a.velocityPxPerSecond,b.velocityPxPerSecond*2);assert.equal(a.phase,b.phase);
  }
});
test('arrival, measured segment, settling, hold and exit join in position and velocity',()=>{
  for(const t of Object.values(motion.boundaries)){
    const left=motion.atSeconds(t-1e-8,1920),right=motion.atSeconds(t+1e-8,1920);
    assert.ok(Math.abs(left.translationY-right.translationY)<1e-3,`position at ${t}`);
    assert.ok(Math.abs(left.velocityPxPerSecond-right.velocityPxPerSecond)<.01,`velocity at ${t}`);
  }
});
test('short words cannot squeeze a one-second fitted entrance over their exit',()=>{
  assert.throws(()=>createReferenceEntrance(profile,{...spec,end:1.7}),/overlap/);
  assert.doesNotThrow(()=>createReferenceEntrance(profile,{...spec,end:1.7,sourceRange:[2,23]}));
  assert.throws(()=>createReferenceEntrance(profile,{...spec,sourceRange:[0,60]}),/unsupported/);
});
test('same-video held-out entry retains observed errors, without claiming exit fit',()=>{
  const m=createReferenceEntrance(profile,{...spec,sourceRange:[2,23]});
  const dt=profile.sourceFps.den/profile.sourceFps.num;
  const offset=946-m.atSeconds(spec.start+2*dt,1920).translationY;
  const rows=profile.heldOut.rows.filter((r:number[])=>r[0]<=23);
  const errors=rows.map((r:number[])=>r[1]-(offset+m.atSeconds(spec.start+r[0]*dt,1920).translationY));
  const rmse=Math.sqrt(errors.reduce((s:number,e:number)=>s+e*e,0)/errors.length);
  assert.ok(Math.abs(rmse-profile.heldOut.entryPhaseReview.rmsePx)<1e-9);
  assert.equal(m.atSeconds(spec.start+24*dt,1920).positionProvenance,'authored');
});
test('half-open lifetime and shuffled seeks are deterministic',()=>{
  assert.equal(motion.atSeconds(3,1920).phase,'off');assert.equal(motion.atSeconds(.99,1920).opacity,0);
  const first=motion.atSeconds(1.3,1920);motion.atSeconds(2.95,1920);assert.deepEqual(motion.atSeconds(1.3,1920),first);
  assert.equal(first.positionProvenance,'fitted_position_only');
  assert.equal(motion.atSeconds(2.95,1920).positionProvenance,'authored');
  assert.throws(()=>motion.atFrame(3,{num:0,den:1},1920),/fps/);
});
