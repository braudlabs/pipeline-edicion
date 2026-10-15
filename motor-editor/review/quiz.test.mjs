import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,mkdtemp,rm} from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import {createHash} from 'node:crypto';
import {createQuizHandler,validateAnswers,compileDecisions,decisionMarkdown} from './quiz-server.mjs';
const raw=await readFile(new URL('./quiz/catalog.json',import.meta.url),'utf8'),catalog=JSON.parse(raw),digest=createHash('sha256').update(raw).digest('hex');
test('catalog covers all 11 sources; unique questions and native bounds',()=>{
 assert.equal(catalog.sources.length,11);assert.equal(catalog.questions.length,69);assert.equal(new Set(catalog.questions.map(q=>q.id)).size,69);
 for(const q of catalog.questions){assert.ok(catalog.sections.some(s=>s.id===q.section));for(const id of q.examples)assert.ok(catalog.examples[id]);}
 for(const e of Object.values(catalog.examples)){const s=catalog.sources.find(s=>s.slug===e.source);assert.ok(s);assert.ok(e.f0>=0&&e.f1<s.frames&&e.f1>=e.f0);assert.equal(e.sha256,s.sha256);}
 for(const s of catalog.sources)assert.ok(catalog.questions.some(q=>q.id==='ref-'+s.slug));
});
test('rejects invented options, contradictory exclusions and too many priorities',()=>{
 const a=(selected,note='',deferred=false)=>({selected,note,deferred});
 assert.throws(()=>validateAnswers({'peso':a(['o1','o2'])},catalog));
 assert.throws(()=>validateAnswers({'peso':a(['invented'])},catalog));
 assert.throws(()=>validateAnswers({'unknown':a([])},catalog));
 assert.throws(()=>validateAnswers({'oclusiones':a(['o1','o4'])},catalog));
 assert.throws(()=>validateAnswers({'prioridades':a(['o1','o2','o3','o4'])},catalog));
 assert.throws(()=>validateAnswers({'peso':a(['o1'],'',true)},catalog));
 assert.deepEqual(validateAnswers({'peso':a([],'Mi alternativa')},catalog).peso,a([],'Mi alternativa'));
});
test('decisions preserve free text, pending and provenance, never infer approvals',()=>{
 const doc=compileDecisions(catalog,{answers:{peso:{selected:['o1'],note:'No copiar el color <script>',deferred:false},escala:{selected:[],note:'',deferred:true}},revision:1,status:'draft',catalogDigest:digest});
 assert.equal(doc.decisions.find(d=>d.id==='peso').selections[0].label,'Regular / Medium');assert.equal(doc.decisions.find(d=>d.id==='escala').status,'deferred');assert.equal(doc.open.length,68);assert.ok(doc.decisions.find(d=>d.id==='peso').referenceEvidence.length);assert.match(decisionMarkdown(doc),/No copiar el color <script>/);
});
test('API persists, recovers, exports and rejects stale writes without overwriting',async()=>{
 const dir=await mkdtemp(path.join(os.tmpdir(),'cutroom-quiz-test-'));let handler=createQuizHandler(dir);
 const server=http.createServer(async(req,res)=>{try{if(!await handler(req,res,new URL(req.url,'http://localhost').pathname,async()=>{})){res.writeHead(404);res.end();}}catch(e){res.writeHead(400,{'Content-Type':'application/json'});res.end(JSON.stringify({error:e.message}));}});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const url='http://127.0.0.1:'+server.address().port;
 try{
  const initial=await(await fetch(url+'/api/quiz')).json();assert.equal(initial.state.revision,0);assert.deepEqual(initial.state.answers,{});
  const put=b=>fetch(url+'/api/quiz',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)});
  const b={answers:{peso:{selected:['o2'],note:'Conservar SF Pro',deferred:false}},baseRevision:0,catalogDigest:digest,status:'draft'};
  const responses=await Promise.all([put(b),put(b)]);assert.deepEqual(responses.map(r=>r.status).sort(),[200,409]);
  handler=createQuizHandler(dir);const restored=await(await fetch(url+'/api/quiz')).json();assert.equal(restored.state.revision,1);assert.equal(restored.state.answers.peso.note,b.answers.peso.note);
  assert.equal((await put({...b,baseRevision:1,status:'ready'})).status,200);
  const doc=await(await fetch(url+'/api/quiz/export')).json();assert.equal(doc.revision,2);assert.equal(doc.status,'ready');assert.equal(doc.open.length,68);
  assert.match(await(await fetch(url+'/api/quiz/brief')).text(),/Conservar SF Pro/);
  assert.equal((await put({...b,baseRevision:2,catalogDigest:'bad'})).status,400);
  assert.equal((await fetch(url+'/api/quiz/source-frame/999999')).status,400);
  const saved=JSON.parse(await readFile(path.join(dir,'quiz-answers.json')));assert.equal(saved.revision,2);assert.equal(JSON.parse(await readFile(path.join(dir,'quiz-history/1.json'))).status,'draft');
 }finally{server.closeAllConnections();await new Promise(r=>server.close(r));await rm(dir,{recursive:true,force:true});}
});
