/** Evidence contract for the new planner. It does not retrofit old renders. */
const finite=x=>typeof x==='number'&&Number.isFinite(x);
const integer=x=>Number.isInteger(x)&&x>=0;
export function auditSourceMapping({sourceWindow,segments,sourceFps,outputFps,allowTimingChanges=false}){
 const errors=[];if(!sourceWindow||!integer(sourceWindow.startFrame)||!integer(sourceWindow.endFrameExclusive)||sourceWindow.endFrameExclusive<=sourceWindow.startFrame)return ['INVALID_SOURCE_WINDOW'];
 if(!/^[a-f0-9]{64}$/.test(sourceWindow.sourceSha256??''))errors.push('MISSING_SOURCE_IDENTITY');
 if(!Array.isArray(segments)||!segments.length)return ['MISSING_SOURCE_MAPPING'];
 if(![sourceFps?.num,sourceFps?.den,outputFps?.num,outputFps?.den].every(v=>Number.isInteger(v)&&v>0))return ['INVALID_FPS'];
 const rate=sourceFps.num/sourceFps.den/(outputFps.num/outputFps.den);let end=0;
 for(const s of segments){
  if(!integer(s.startFrame)||!integer(s.endFrameExclusive)||s.endFrameExclusive<=s.startFrame||!finite(s.sourceStartFrame)||!finite(s.sourceEndFrameExclusive)){errors.push('INVALID_SEGMENT');continue;}
  if(s.startFrame!==end)errors.push('OUTPUT_GAP_OR_OVERLAP');end=s.endFrameExclusive;
  if(s.sourceSha256!==sourceWindow.sourceSha256)errors.push('SOURCE_IDENTITY_CHANGED');
  if(!allowTimingChanges){
   const expectedStart=sourceWindow.startFrame+s.startFrame*rate,expectedEnd=sourceWindow.startFrame+s.endFrameExclusive*rate;
   if(Math.abs(s.sourceStartFrame-expectedStart)>1e-6||Math.abs(s.sourceEndFrameExclusive-expectedEnd)>1e-6)errors.push('UNAUTHORIZED_SOURCE_TIME_CHANGE');
   if(s.speed!==undefined&&s.speed!==1)errors.push('UNAUTHORIZED_SPEED_CHANGE');
   if(s.audioSourceStartFrame!==undefined&&Math.abs(s.audioSourceStartFrame-s.sourceStartFrame)>1e-6)errors.push('AUDIO_VIDEO_DESYNC');
  }
 }
 if(!allowTimingChanges&&Math.abs(end*rate-(sourceWindow.endFrameExclusive-sourceWindow.startFrame))>1e-6)errors.push('SOURCE_WINDOW_DURATION_CHANGED');
 return [...new Set(errors)];
}
export function auditTreatment(t){
 const errors=[];for(const k of ['id','layoutId','role','narrativeFunction','speakerId'])if(typeof t[k]!=='string'||!t[k])errors.push(`MISSING_${k}`);
 if(!integer(t.startFrame)||!integer(t.endFrameExclusive)||t.endFrameExclusive<=t.startFrame)errors.push('INVALID_EVENT_RANGE');
 if(!Array.isArray(t.evidence)||!t.evidence.length)errors.push('MISSING_EVIDENCE');
 for(const e of t.evidence??[]){if(!e.slug||!/^[a-f0-9]{64}$/.test(e.sourceSha256??'')||!integer(e.f0)||!integer(e.f1)||e.f1<e.f0||!e.level)errors.push('INVALID_EVIDENCE_IDENTITY');}
 for(const k of ['layout','typography','entry','hold','exit','occlusion','audio']){
  const property=t[k];if(!property||!['measured','fitted','proposed','unknown'].includes(property.status))errors.push(`MISSING_PROVENANCE_${k}`);
  if(property?.status==='unknown'&&t.claim==='reconstruction_verified')errors.push(`UNSUPPORTED_VERIFICATION_${k}`);
  if(['measured','fitted'].includes(property?.status)&&!property.measurementPath)errors.push(`MISSING_MEASUREMENT_${k}`);
 }
 if(t.claim==='reconstruction_verified'&&!t.comparison?.artifact)errors.push('MISSING_RENDER_COMPARISON');
 return [...new Set(errors)];
}
export function independentEvidenceFamilies(examples){return [...new Set(examples.map(e=>/^(v6-|v7-)/.test(e.slug)?'ads90_variants':e.slug))];}
