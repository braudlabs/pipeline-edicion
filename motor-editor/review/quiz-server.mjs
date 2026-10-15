import {readFile,writeFile,rename,mkdir} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec=promisify(execFile);
const ROOT=path.dirname(fileURLToPath(import.meta.url));
const source='/Users/alejandrorubiocamarero/Downloads/Birdieballs v1 (Sin Postpro).mp4';
const send=(res,data,status=200)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
export function validateAnswers(answers,catalog){
 if(!answers||typeof answers!=='object'||Array.isArray(answers))throw Error('Respuestas inválidas');
 const clean={};
 for(const [id,a] of Object.entries(answers)){
  const q=catalog.questions.find(q=>q.id===id);if(!q)throw Error('Pregunta desconocida: '+id);
  if(!a||!Array.isArray(a.selected)||typeof a.note!=='string'||typeof a.deferred!=='boolean')throw Error('Respuesta incompleta');
  if(a.note.length>8000||a.selected.some(id=>typeof id!=='string'||!q.options.some(o=>o.id===id))||new Set(a.selected).size!==a.selected.length)throw Error('Opciones o comentario inválidos');
  if((q.type==='single'&&a.selected.length>1)||(q.maxSelections&&a.selected.length>q.maxSelections))throw Error('Demasiadas opciones');
  if(a.selected.length>1&&a.selected.some(id=>q.options.find(o=>o.id===id).exclusive))throw Error('Una opción excluyente debe elegirse sola');
  if(a.deferred&&(a.selected.length||a.note.trim()))throw Error('Una decisión aplazada no puede incluir una respuesta');
  if(a.selected.length||a.note.trim()||a.deferred)clean[id]={selected:[...a.selected],note:a.note,deferred:a.deferred};
 }
 return clean;
}
export function compileDecisions(catalog,state){
 const decisions=catalog.questions.map(q=>{const a=state.answers[q.id];return {id:q.id,section:q.section,question:q.title,ruleIds:q.ruleIds,status:a?.deferred?'deferred':a&&(a.selected.length||a.note.trim())?'answered':'unanswered',selections:(a?.selected||[]).map(id=>({id,label:q.options.find(o=>o.id===id).label,description:q.options.find(o=>o.id===id).description})),note:a?.note||'',birdieballsScene:q.scene,referenceEvidence:q.examples.map(id=>catalog.examples[id])};});
 return {schemaVersion:1,catalogId:catalog.id,catalogDigest:state.catalogDigest,revision:state.revision,status:state.status,updatedAt:state.updatedAt,scope:'Birdieballs · primeros ~20 segundos',constraints:catalog.constraints,decisions,open:decisions.filter(d=>d.status!=='answered').map(d=>d.id),interpretation:'Preferencias de Ale. No son parámetros medidos del editor ni aprobación automática de una futura ejecución. Pendientes y aplazados no autorizan un recurso.'};
}
export function decisionMarkdown(doc){
 return '# Dirección de edición · Birdieballs\n\nEstado: '+doc.status+' · revisión '+doc.revision+'\n\n'+doc.interpretation+'\n\n## Criterios ya expresados\n\n'+doc.constraints.map(c=>'- '+c.text).join('\n')+'\n\n'+doc.decisions.map(d=>'## '+d.question+'\n\n'+(d.status==='answered'?d.selections.map(s=>'- '+s.label+(s.description?' — '+s.description:'')).join('\n')+(d.note?'\n\nComentario: '+d.note:''):d.status==='deferred'?'Aplazado expresamente.':'Sin responder.')+'\n').join('\n');
}
export function createQuizHandler(DATA){
 const file=path.join(DATA,'quiz-answers.json');let queue=Promise.resolve();const frameRuns=new Map();
 const catalogPromise=readFile(path.join(ROOT,'quiz/catalog.json'),'utf8').then(text=>({catalog:JSON.parse(text),digest:createHash('sha256').update(text).digest('hex')}));
 const state=async digest=>{try{return JSON.parse(await readFile(file,'utf8'));}catch(e){if(e.code!=='ENOENT')throw e;return {schemaVersion:1,revision:0,status:'draft',answers:{},updatedAt:null,catalogDigest:digest};}};
 return async(req,res,p,sendFile)=>{
  const files={'/direction':'direction.html','/quiz':'quiz.html','/quiz.js':'quiz.js','/quiz.css':'quiz.css'};
  if(req.method==='GET'&&files[p]){await sendFile(req,res,path.join(ROOT,'public',files[p]));return true;}
  if(req.method==='GET'&&p==='/quiz-rejected.png'){await sendFile(req,res,path.resolve(ROOT,'../../birdieballs/feedback/V04-de-campos-rechazado.png'));return true;}
  if(req.method==='GET'&&p==='/quiz-source'){await sendFile(req,res,source);return true;}
  if(req.method==='GET'&&p==='/api/direction'){const doc=JSON.parse(await readFile(path.resolve(ROOT,'../../birdieballs/v05-direction/direction.json'),'utf8'));send(res,doc);return true;}
  if(!p.startsWith('/api/quiz'))return false;
  const frameMatch=/^\/api\/quiz\/source-frame\/(\d+)$/.exec(p);
  if(req.method==='GET'&&frameMatch){const f=Number(frameMatch[1]);if(!Number.isInteger(f)||f<0||f>=2278)throw Error('Frame fuera del original');const dir=path.join(DATA,'quiz-source-frames'),file=path.join(dir,`${f}.png`);
   let exists=false;try{await readFile(file);exists=true;}catch(e){if(e.code!=='ENOENT')throw e;}
   if(!exists){if(!frameRuns.has(f)){const run=(async()=>{await mkdir(dir,{recursive:true});await exec('ffmpeg',['-v','error','-threads','2','-i',source,'-vf',`select=eq(n\\,${f})`,'-frames:v','1','-fps_mode','vfr','-y',file+'.tmp.png'],{maxBuffer:4e6});await rename(file+'.tmp.png',file);})();frameRuns.set(f,run);}try{await frameRuns.get(f);}finally{frameRuns.delete(f);}}
   await sendFile(req,res,file);return true;
  }
  const {catalog,digest}=await catalogPromise;
  if(req.method==='GET'&&p==='/api/quiz'){send(res,{catalog,state:await state(digest)});return true;}
  if(req.method==='GET'&&['/api/quiz/export','/api/quiz/brief'].includes(p)){
   const doc=compileDecisions(catalog,await state(digest));res.setHeader('Content-Disposition','attachment; filename="birdieballs-direccion.'+(p.endsWith('brief')?'md':'json')+'"');
   if(p.endsWith('brief')){res.writeHead(200,{'Content-Type':'text/markdown; charset=utf-8','Cache-Control':'no-store'});res.end(decisionMarkdown(doc));}else send(res,doc);return true;
  }
  if(req.method==='PUT'&&p==='/api/quiz'){
   let bytes=0,chunks=[];for await(const chunk of req){bytes+=chunk.length;if(bytes>800000)throw Error('Respuestas demasiado grandes');chunks.push(chunk);}const body=JSON.parse(Buffer.concat(chunks).toString());
   const answers=validateAnswers(body.answers,catalog);
   if(!Number.isSafeInteger(body.baseRevision)||body.baseRevision<0||!['draft','ready'].includes(body.status)||body.catalogDigest!==digest)throw Error('Revisión o catálogo incompatible. Recarga el cuestionario.');
   const run=queue.then(async()=>{const old=await state(digest);if(old.revision!==body.baseRevision){send(res,{error:'Hay respuestas más recientes en otra pestaña. Tu borrador local se conserva; recarga antes de reconciliarlo.',conflict:true,revision:old.revision},409);return;}
    const next={schemaVersion:1,catalogDigest:digest,revision:old.revision+1,status:body.status,answers,updatedAt:new Date().toISOString()};
    await mkdir(DATA,{recursive:true});
    // Each accepted revision is retained, so an answer change never erases its history.
    await mkdir(path.join(DATA,'quiz-history'),{recursive:true});await writeFile(path.join(DATA,'quiz-history',`${next.revision}.json`),JSON.stringify(next,null,2));
    await writeFile(file+'.tmp',JSON.stringify(next,null,2));await rename(file+'.tmp',file);
    // Derived exports are rebuilt from the canonical answers; never modify video notes.
    const doc=compileDecisions(catalog,next);await writeFile(path.join(DATA,'quiz-decisions.json.tmp'),JSON.stringify(doc,null,2));await rename(path.join(DATA,'quiz-decisions.json.tmp'),path.join(DATA,'quiz-decisions.json'));
    await writeFile(path.join(DATA,'quiz-brief.md.tmp'),decisionMarkdown(doc));await rename(path.join(DATA,'quiz-brief.md.tmp'),path.join(DATA,'quiz-brief.md'));
    send(res,next);
   });queue=run.catch(()=>{});await run;return true;
  }
  send(res,{error:'Ruta del cuestionario desconocida'},404);return true;
 };
}
