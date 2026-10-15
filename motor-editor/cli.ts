import {readFile,writeFile,mkdir,copyFile,stat} from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import {compile} from './src/planner.ts';
import {compileEditorial,type EditorialSpec,type EditorialPlan} from './src/editorial-v2/index.ts';
import {auditPlan,validateJob} from './src/validate.ts';
import type {Job,Plan} from './src/types.ts';
const ROOT=path.dirname(fileURLToPath(import.meta.url));
function report(plan:Plan){return {job:plan.jobId,frames:plan.durationInFrames,seconds:plan.durationInFrames/(plan.fps.num/plan.fps.den),shots:plan.clips.length,captions:plan.captions.length,motionGraphics:plan.graphics.length,recipes:plan.decisions.map(d=>({clause:d.clauseId,recipe:d.recipe,reason:d.reason,evidence:d.evidence,candidates:d.candidates})),diagnostics:plan.diagnostics,wordCoverage:`${plan.coverage.filter(w=>w.representations.length).length}/${plan.coverage.length}`,editorial:(plan as EditorialPlan).editorial,fidelity:plan.provenance.fidelity};}
async function stage(job:Job,base:string){
 await mkdir(path.join(ROOT,'public/media'),{recursive:true});
 for(const asset of job.assets){
  if(/^https?:/.test(asset.src))throw new Error(`Descarga y fija el medio antes de compilar: ${asset.id}`);
  const file=path.resolve(base,asset.src);await stat(file);
  const media=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',file],{encoding:'utf8'}));
  const video=media.streams.find((s:{codec_type:string})=>s.codec_type==='video');if(video){asset.width=video.width;asset.height=video.height;}
  const seconds=Number(media.format.duration);if(Number.isFinite(seconds)&&seconds>0)asset.duration=seconds;
  if(asset.kind==='audio'&&!media.streams.some((s:{codec_type:string})=>s.codec_type==='audio'))throw new Error(`Asset ${asset.id} no contiene audio`);
  if(asset.kind!=='audio'&&!video)throw new Error(`Asset ${asset.id} no contiene imagen`);
  const bytes=await readFile(file);const hash=createHash('sha256').update(bytes).digest('hex');asset.sha256=hash;const name=hash.slice(0,20)+path.extname(file).toLowerCase();await copyFile(file,path.join(ROOT,'public/media',name));asset.src='media/'+name;
 }
}
try{
 const [command,input,...args]=process.argv.slice(2);
 if(!input||!['compile','compile-editorial','inspect'].includes(command)){console.error('Uso: node motor-editor/cli.ts compile|compile-editorial trabajo.json --out salida.json [--stage-media]\n     node motor-editor/cli.ts inspect salida.json');process.exitCode=1;}
 else if(command==='inspect'){const plan=JSON.parse(await readFile(input,'utf8')) as Plan;const errors=auditPlan(plan);console.log(JSON.stringify({...report(plan),audit:errors},null,2));if(errors.some(e=>e.severity==='error'))process.exitCode=1;}
 else {
  const job:unknown=JSON.parse(await readFile(input,'utf8'));validateJob(job);
  if(args.includes('--stage-media'))await stage(job,path.dirname(path.resolve(input)));
  const plan=(command==='compile-editorial'||'editorial' in job)?compileEditorial(job,(job as Job&{editorial:EditorialSpec}).editorial):compile(job);const oi=args.indexOf('--out');const output=oi>=0?args[oi+1]:path.join(path.dirname(input),'plan.json');if(!output)throw new Error('Falta ruta tras --out');if(path.resolve(output)===path.resolve(input))throw new Error('La salida no puede sobrescribir el trabajo fuente');
  await mkdir(path.dirname(path.resolve(output)),{recursive:true});await writeFile(output,JSON.stringify(plan,null,2)+'\n');await writeFile(output.replace(/\.json$/,'')+'.props.json',JSON.stringify({plan},null,2)+'\n');await writeFile(output.replace(/\.json$/,'')+'.report.json',JSON.stringify(report(plan),null,2)+'\n');console.log(JSON.stringify({output,...report(plan)},null,2));
 }
}catch(e){console.error(e instanceof Error?e.message:e);process.exitCode=1;}
