import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import {pose,heroOffset,FPS} from './motion.ts';
import {cues} from './cues.ts';
import {measuredProfile} from './reference-profile.ts';
import {sampleReferenceTranslation} from '../../motor-editor/forensics/reference-motion.mjs';
let maxReferenceError=0;for(let a=2;a<=60;a+=.125){const expected=sampleReferenceTranslation(measuredProfile,a/FPS,1920).translationY;maxReferenceError=Math.max(maxReferenceError,Math.abs(heroOffset(a)-expected));}assert(maxReferenceError<1e-10);
const joins=[];for(const a of [2,60,66]){const h=.00001,l=heroOffset(a-h),v=heroOffset(a),r=heroOffset(a+h),velocityDifference=Math.abs((v-l)/h-(r-v)/h);assert(Math.abs(r-l)<.002);assert(velocityDifference<.01);joins.push({age:a,positionDifference:r-l,velocityDifference})}
for(const c of cues){assert(c.end>c.start);for(let t=c.start-1/FPS;t<=c.end+1/FPS;t+=1/FPS){const p=pose(c,t);assert([p.x,p.y,p.scale,p.alpha,p.reveal].every(Number.isFinite));assert(p.alpha>=0&&p.alpha<=1);}}
const cuts=[];for(const [id,f]of [['recuperamos',757],['originales',794]]){const c=cues.find(c=>c.id===id),a=pose(c,(f-1)/FPS),b=pose(c,f/FPS),delta=Math.hypot(a.x-b.x,a.y-b.y);assert(delta<.01);cuts.push({id,frame:f,positionDeltaPx:delta,V06DeltaPx:200})}
for(const block of ['offer','product','origins']){const cs=cues.filter(c=>c.block===block);assert(new Set(cs.map(c=>c.y)).size===1)}
const mask=cues.filter(c=>c.masked||c.outline);for(let f=560;f<=598;f++){const a=pose(mask[0],f/FPS),b=pose(mask[1],f/FPS);assert.deepEqual(a,b)}
const info={maxReferenceErrorPx:maxReferenceError,measuredDomainFrames:[2,60],designedBoundaryJoins:joins,cuts,uniformBlockBaselines:['offer','product','origins'],maskAndOutlineSynchronized:true,cues:cues.length,limitation:'Motion-fit equivalence applies to the measured positional curve only, not entire editor style.'};await fs.writeFile('birdieballs/v07/motion-validation.json',JSON.stringify(info,null,2));await fs.writeFile('birdieballs/v07/cues.json',JSON.stringify(cues,null,2));console.log(JSON.stringify(info));
