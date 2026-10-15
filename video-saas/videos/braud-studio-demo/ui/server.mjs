// Local visual preview only. No providers, credentials, production storage or external calls.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {randomUUID} from 'node:crypto';
const ROOT=path.dirname(fileURLToPath(import.meta.url));
const seed=JSON.parse(fs.readFileSync(path.join(ROOT,'demo/state.json'),'utf8'));
const MIME={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.gif':'image/gif','.webp':'image/webp','.mp4':'video/mp4','.mp3':'audio/mpeg','.m4a':'audio/mp4','.svg':'image/svg+xml','.woff2':'font/woff2'};
export function createDemoServer(){
 let state=structuredClone(seed);
 const streams=new Set();
 const json=(res,data,status=200)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
 const publicState=()=>({...state,assets:state.assets.map(({file,...a})=>a)});
 const notify=()=>{state.revision++;state.updatedAt=new Date().toISOString();for(const res of streams)res.write(`data: ${JSON.stringify({revision:state.revision,liveRevision:state.revision,conversations:state.conversations})}\n\n`);};
 const unsupported=()=>{const error=new Error('Esta es una demo visual. Esta operación necesita el backend de producción y no se ejecuta aquí.');error.status=501;throw error;};
 const catalogs={connections:[{id:'codex',name:'Catálogo de muestra · sin conexión',models:['gpt-6.1-sol','gpt-6-astra','gpt-6-sol','gpt-6-luna','gpt-5.6-sol','gpt-5.6-terra','gpt-5.6-luna'].map(id=>({id,name:id.toUpperCase().replace('GPT','GPT'),efforts:['low','medium','high','xhigh','max'],defaultEffort:'medium'}))}],dictation:'unavailable'};
 async function input(req){let bytes=0,parts=[];for await(const part of req){bytes+=part.length;if(bytes>1_000_000){const e=new Error('Solicitud demasiado grande.');e.status=413;throw e;}parts.push(part);}return JSON.parse(Buffer.concat(parts).toString()||'{}');}
 const server=http.createServer(async(req,res)=>{try{
  const url=new URL(req.url,'http://localhost'),route=url.pathname;
  // Bind to loopback and reject cross-origin changes, including DNS rebinding.
  const port=server.address().port;
  if(!['localhost:'+port,'127.0.0.1:'+port].includes(req.headers.host))return json(res,{error:'Host no permitido.'},403);
  if(!['GET','HEAD'].includes(req.method)&&req.headers.origin&&!['http://localhost:'+port,'http://127.0.0.1:'+port].includes(req.headers.origin))return json(res,{error:'Origen no permitido.'},403);
  if(route==='/api/agent/events'&&req.method==='GET'){
   res.writeHead(200,{'Content-Type':'text/event-stream','Cache-Control':'no-cache','Connection':'keep-alive'});res.write(': demo ready\n\n');streams.add(res);req.on('close',()=>streams.delete(res));return;
  }
  if(route.startsWith('/api/')){
   if(req.method==='GET'){
    if(route==='/api/state')return json(res,publicState());
    if(route==='/api/health')return json(res,{ok:true,mode:'visual-demo'});
    if(route==='/api/agent/catalog')return json(res,catalogs);
    if(route==='/api/workspace')return json(res,{documents:[]});
    if(route==='/api/feedback')return json(res,{reports:[],hasMore:false});
    if(route==='/api/agent/capabilities')return json(res,{tools:[],mode:'visual-demo'});
    if(route==='/api/piece-memory')return json(res,{pieceId:url.searchParams.get('pieceId'),records:[],conversations:[],decisions:[],pending:[],learnings:[],sources:[]});
    if(route==='/api/agent/context')return json(res,{loaded:['Datos de muestra de esta demo visual.'],documents:[],materials:[],pieces:state.pieces,method:[],rules:'Demo visual sin agente conectado.',brand:state.clients[0]});
    if(route==='/api/export')unsupported();
    return json(res,{error:'Ruta no disponible en la demo.'},404);
   }
   if(req.method!=='POST')return json(res,{error:'Método no permitido.'},405);
   if(['/api/generate','/api/quote','/api/upload','/api/material/upload','/api/dictation','/api/chat'].includes(route))unsupported();
   const data=await input(req);let result;
   if(route==='/api/demo/reset'){state=structuredClone(seed);notify();return json(res,{state:publicState()});}
   else if(route==='/api/agent/check')return json(res,{connections:catalogs.connections.map(c=>({...c,status:'unavailable'}))});
   else if(route==='/api/connections/check')return json(res,{higgsfield:'unavailable',message:'Demo visual, sin proveedores conectados.'});
   else if(route==='/api/conversations'){
    const id='demo-'+randomUUID(),at=new Date().toISOString();state.conversations.push({id,clientId:data.clientId||'braud',title:String(data.text||'Nueva conversación').slice(0,70),createdAt:at,updatedAt:at,pieceId:data.pieceId||null,pieceIds:data.pieceId?[data.pieceId]:[],selectedPieceId:data.pieceId||null,agent:{...state.agent},messages:[],jobs:[]});notify();return json(res,{state:publicState(),conversationId:id});
   }else if(route.startsWith('/api/conversations/')){
    const [, , ,id,action]=route.split('/'),c=state.conversations.find(c=>c.id===id);if(!c)return json(res,{error:'Conversación no encontrada.'},404);
    if(action==='settings')c.agent={provider:data.provider,model:data.model,effort:data.effort};
    else if(action==='send'){const at=new Date().toISOString();c.messages.push({id:randomUUID(),role:'user',text:String(data.text||''),at},{id:randomUUID(),role:'assistant',text:'Demo visual: el mensaje se conserva durante esta sesión. No hay un modelo conectado ni se generan recursos. Puedes recorrer el estudio, cambiar el tema y explorar todas las propuestas de diseño.',at});c.updatedAt=at;}
    else if(action==='archive')c.archivedAt=new Date().toISOString();
    else if(action==='restore')delete c.archivedAt;
    else if(action==='scope'){c.pieceId=c.selectedPieceId=data.pieceId;c.pieceIds=data.pieceId?[data.pieceId]:[];}
    else if(action!=='cancel')unsupported();
   }else if(route==='/api/action'){
    const p=state.pieces.find(p=>p.id===data.pieceId),sc=p?.scenes.find(s=>s.id===data.sceneId);
    if(data.type==='agent-default')state.agent={provider:data.provider,model:data.model,effort:data.effort};
    else if(data.type==='agent'&&p)p.agent={provider:data.provider,model:data.model,effort:data.effort};
    else if(data.type==='brief'&&p){p.title=data.title??p.title;p.brief=data.brief??p.brief;}
    else if(data.type==='script'&&p)p.script=data.lines;
    else if(data.type==='scene'&&sc)for(const key of ['title','lineId','intent','duration','audioMode','music']){if(key in data)sc[key]=data[key];}
    else if(data.type==='piece-intent'&&p){p.intentBrief||={};for(const key of ['goal','audience','audienceAwareness','audienceRelationship','tension','offer','proof','conceptTitle','message','concept','rationale','cta','heroReferenceId','selectedAngleId'])if(key in data)p.intentBrief[key]=data[key];}
    else if(data.type==='script-opening-apply'&&p){const opening=p.scriptOpenings.alternatives.find(o=>o.id===data.openingId);if(!opening)unsupported();opening.lines.forEach((l,i)=>Object.assign(p.script[i],l));p.scriptOpenings.appliedLines=structuredClone(p.script.slice(0,opening.lines.length));p.scriptOpenings.selectedId=opening.id;}
    else if(data.type==='piece-cast-candidate'&&p){const role=p.castRoles.find(r=>r.id===data.roleId);if(!role)unsupported();const c=role.candidates.find(c=>c.assetId===data.assetId);if(c){c.status=data.status;c.note=data.note||'';}else role.candidates.push({id:randomUUID(),assetId:data.assetId,status:data.status,note:data.note||''});}
    else if(data.type==='verdict'&&sc){const v=sc.versions.find(v=>v.assetId===data.assetId);if(!v)unsupported();v.status=data.status;v.feedback=data.feedback||'';if(data.select)sc.selectedId=data.assetId;}
    else unsupported();
   }else if(route==='/api/casting'){const a=state.assets.find(a=>a.id===data.assetId);if(!a)unsupported();a.castingSelected=!!data.selected;}
   else if(route==='/api/workspace/brand'){const c=state.clients.find(c=>c.id===data.clientId);if(!c)unsupported();c.name=String(data.name||c.name);}
   else unsupported();
   notify();return json(res,{state:publicState(),result});
  }
  if(!['GET','HEAD'].includes(req.method))return json(res,{error:'Método no permitido.'},405);
  if(route==='/'&&!url.search){res.writeHead(302,{Location:'/?dev=1&brand=braud'});return res.end();}
  let file;
  if(route.startsWith('/media/')){const a=state.assets.find(a=>a.id===decodeURIComponent(route.slice(7)));if(a)file=path.join(ROOT,a.file);}
  else {const rel=route==='/'?'index.html':decodeURIComponent(route.slice(1));const base=path.join(ROOT,'public');const candidate=path.resolve(base,rel);if(candidate.startsWith(base+path.sep)&&!rel.split('/').some(x=>x.startsWith('.')))file=candidate;}
  if(!file||!fs.existsSync(file)||!fs.statSync(file).isFile())return json(res,{error:'Archivo no encontrado.'},404);
  const stat=fs.statSync(file),headers={'Content-Type':MIME[path.extname(file)]||'application/octet-stream','Content-Length':stat.size,'Accept-Ranges':'bytes','X-Content-Type-Options':'nosniff'};
  const range=req.headers.range;
  if(range){const m=/^bytes=(\d*)-(\d*)$/.exec(range);let start,end;if(m&&(m[1]||m[2])){start=m[1]?Number(m[1]):Math.max(0,stat.size-Number(m[2]));end=m[1]?(m[2]?Math.min(Number(m[2]),stat.size-1):stat.size-1):stat.size-1;}
   if(!Number.isSafeInteger(start)||!Number.isSafeInteger(end)||start>end||start>=stat.size){res.writeHead(416,{'Content-Range':`bytes */${stat.size}`});return res.end();}
   res.writeHead(206,{...headers,'Content-Range':`bytes ${start}-${end}/${stat.size}`,'Content-Length':end-start+1});if(req.method==='HEAD')return res.end();fs.createReadStream(file,{start,end}).pipe(res);return;
  }
  res.writeHead(200,headers);if(req.method==='HEAD')return res.end();fs.createReadStream(file).pipe(res);
 }catch(error){json(res,{error:error.status?error.message:'No se ha podido completar la operación de demo.'},error.status||400);}});
 server.on('close',()=>{for(const res of streams)res.end();streams.clear();});
 return server;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(path.resolve(process.argv[1])).href){const port=Number(process.env.PORT||8799);createDemoServer().listen(port,'127.0.0.1',()=>console.log(`BRAUD Studio · DEMO VISUAL\nhttp://127.0.0.1:${port}/?dev=1&brand=braud\nSin IA conectada. Cambios de muestra en memoria; reiniciar restaura la demo.`));}
