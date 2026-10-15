import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
import {compile} from '../motor-editor/src/planner.ts';
import {auditPlan} from '../motor-editor/src/validate.ts';
import {fitText} from '../motor-editor/src/text.ts';
const edl=JSON.parse(await fs.readFile('birdieballs/analysis/edl.json','utf8'));
const transcript=JSON.parse(await fs.readFile('birdieballs/analysis/turbo/intro.json','utf8'));
const F=60000/1001;
const map=t=>{let out=0;for(const s of edl.segments){if(t>=s.sourceIn&&t<=s.sourceOut)return out+t-s.sourceIn;out+=s.sourceOut-s.sourceIn;}throw Error('Palabra fuera del montaje: '+t);};
const words=transcript.segments.flatMap(s=>s.words).map((w,i)=>({id:'w'+i,text:w.word.trim().replace('Mindungis,','mindunguis,'),start:map(w.start),end:map(w.end),speaker:i<13?'golfer':'birdieballs'}));
const job={version:1,id:'birdieballs-b01-v01',family:'braud',format:{width:1080,height:1920,fps:edl.fps},words,clauses:transcript.segments.map((s,i)=>({id:'line-'+i,wordIds:words.filter(w=>w.start>=map(s.start)-.001&&w.end<=map(s.end)+.001).map(w=>w.id),recipe:'rail'})),assets:[],options:{fontSize:100,captionY:.69,palette:{background:'#173e2d',foreground:'#fffdf0',accent:'#fffdf0'},maxCaptionGap:.06}};
const p=compile(job);
const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,duration','-of','json','birdieballs/public/base.mp4'],{encoding:'utf8'}));
const frames=Number(probe.streams[0].nb_frames);
p.durationInFrames=frames;p.assets=[{id:'base',src:'birdieballs/base.mp4',kind:'video',duration:frames/F},{id:'voice',src:'birdieballs/voice.wav',kind:'audio'}];
p.clips=[{id:'base-clip',assetId:'base',shotId:'base',start:0,end:frames,sourceStart:0,crop:{scale:1,x:0,y:0},mute:true}];
p.audio=[{id:'original-audio',assetId:'voice',start:0,end:frames,sourceStart:0,gain:[{f:0,v:1},{f:frames-4,v:1},{f:frames,v:0}]}];
for(const c of p.captions){
 c.y=c.speaker==='golfer'?1280:1430;c.fontSize=fitText(c.text,880,100);c.stroke='#163329';c.strokeWidth=2.1;
 c.motion={y:[{f:c.start,v:15,ease:'out'},{f:Math.min(c.end-1,c.start+7),v:0}],opacity:[{f:c.start,v:.55},{f:Math.min(c.end-1,c.start+3),v:1}]};
 if(c.text==='riñón'){c.text='RIÑÓN';c.fontSize=204;c.y=1270;c.strokeWidth=1.6;c.motion={y:[{f:c.start,v:45,ease:'out'},{f:Math.min(c.end-1,c.start+10),v:0}],scale:[{f:c.start,v:1.055,ease:'out'},{f:Math.min(c.end-1,c.start+12),v:1}]};}
 if(c.text==='solución.'){c.text='SOLUCIÓN';c.fontSize=fitText(c.text,870,173);c.y=1440;c.strokeWidth=1.5;c.motion={y:[{f:c.start,v:38,ease:'out'},{f:c.start+12,v:0}],scale:[{f:c.start,v:1.035,ease:'out'},{f:c.start+14,v:1}]};c.end=Math.min(frames,c.end+8);}
 if(c.text==='Literalmente.'){c.text='Literalmente.';c.fontSize=91;c.y=1440;c.end=frames;}
}
p.diagnostics=[];const issues=auditPlan(p);if(issues.length)throw Error(JSON.stringify(issues));
p.production={source:edl.source,segments:edl.segments,transcription:'Whisper large-v3-turbo local; spelling mindunguis corrected using supplied script',status:'first proposal, pending user feedback',notes:'Original gag preserved. Caption position and emphasis are editorial overrides of compiled rail recipe.'};
await fs.writeFile('birdieballs/v01/job.json',JSON.stringify(job,null,2));await fs.writeFile('birdieballs/v01/plan.json',JSON.stringify(p,null,2));
for(const folder of ['motor-editor/public/birdieballs','motor-editor/build/public/birdieballs']){await fs.mkdir(folder,{recursive:true});for(const file of ['base.mp4','voice.wav']){try{await fs.link('birdieballs/public/'+file,folder+'/'+file);}catch(e){if(e.code!=='EEXIST')throw e;}}}
console.log(JSON.stringify({frames,seconds:frames/F,words:words.length,captions:p.captions.length,issues}));
