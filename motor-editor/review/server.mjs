import http from 'node:http';
import {serveStudy} from './study-server.mjs';
import {createQuizHandler} from './quiz-server.mjs';
import {readFile,writeFile,mkdir,rename,stat,rm} from 'node:fs/promises';
import {createReadStream,createWriteStream} from 'node:fs';
import {pipeline} from 'node:stream/promises';
import {Transform} from 'node:stream';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {createHash,randomUUID} from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateNote,exportFeedback} from './model.mjs';
const exec=promisify(execFile),ROOT=path.dirname(fileURLToPath(import.meta.url));
const DATA=path.resolve(process.env.REVIEW_DATA_DIR||path.join(ROOT,'data')),PORT=Number(process.env.PORT||4317),HOST='127.0.0.1';
await mkdir(DATA,{recursive:true});
let project;try{project=JSON.parse(await readFile(path.join(DATA,'project.json'),'utf8'));}catch(e){if(e.code!=='ENOENT')throw e;project={id:randomUUID(),title:'Laboratorio de edición',versions:[],notes:[]};}
const save=async()=>{await writeFile(path.join(DATA,'project.tmp'),JSON.stringify(project,null,2));await rename(path.join(DATA,'project.tmp'),path.join(DATA,'project.json'));};
let queue=Promise.resolve();const mutate=fn=>{const result=queue.then(fn);queue=result.catch(()=>{});return result;};
const json=(res,data,status=200)=>{res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
const mime={'.html':'text/html; charset=utf-8','.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4','.mov':'video/quicktime','.webm':'video/webm','.svg':'image/svg+xml','.json':'application/json'};
async function sendFile(req,res,file){const size=(await stat(file)).size;const type=mime[path.extname(file)]||'application/octet-stream';const range=req.headers.range;if(range){const m=/^bytes=(\d+)-(\d*)$/.exec(range);if(!m){res.writeHead(416,{'Content-Range':`bytes */${size}`});return res.end();}const start=Number(m[1]),end=Math.min(size-1,m[2]?Number(m[2]):size-1);if(start>=size||end<start){res.writeHead(416,{'Content-Range':`bytes */${size}`});return res.end();}res.writeHead(206,{'Content-Type':type,'Content-Length':end-start+1,'Accept-Ranges':'bytes','Content-Range':`bytes ${start}-${end}/${size}`});await pipeline(createReadStream(file,{start,end}),res);}else{res.writeHead(200,{'Content-Type':type,'Content-Length':size,'Accept-Ranges':'bytes','Cache-Control':'no-cache'});await pipeline(createReadStream(file),res);}}
const version=id=>{const v=project.versions.find(v=>v.id===id);if(!v)throw Error('Versión desconocida');return v;};
const runningFrames=new Map();
async function frameFile(v,f){if(!Number.isInteger(f)||f<0||f>=v.frameCount)throw Error('Fotograma fuera del vídeo');const file=path.join(DATA,v.id,`frame-${f}.png`);try{await stat(file);return file;}catch{}const key=v.id+':'+f;if(runningFrames.has(key))return runningFrames.get(key);const run=(async()=>{const tmp=file+'.tmp.png';await exec('ffmpeg',['-v','error','-i',path.join(DATA,v.id,v.file),'-vf',`select=eq(n\\,${f}),scale=iw*sar:ih,setsar=1`,'-frames:v','1','-fps_mode','vfr','-y',tmp],{maxBuffer:4e6});await rename(tmp,file);return file;})();runningFrames.set(key,run);try{return await run;}finally{runningFrames.delete(key);}}
async function body(req,limit=2e6){let size=0,chunks=[];for await(const chunk of req){size+=chunk.length;if(size>limit)throw Error('Petición demasiado grande');chunks.push(chunk);}return JSON.parse(Buffer.concat(chunks).toString());}
async function importVideo(req){
 const id=randomUUID(),dir=path.join(DATA,id);await mkdir(dir);const originalName=decodeURIComponent(req.headers['x-file-name']||'clip.mp4');const extension=path.extname(originalName).toLowerCase();if(!['.mp4','.mov','.webm','.m4v'].includes(extension)){await rm(dir,{recursive:true});throw Error('Usa MP4, MOV, M4V o WebM');}
 const file='source'+extension;let bytes=0;const hash=createHash('sha256');
 try{await pipeline(req,new Transform({transform(chunk,enc,cb){bytes+=chunk.length;if(bytes>1024**3)return cb(Error('El límite es 1 GB por versión'));hash.update(chunk);cb(null,chunk);}}),createWriteStream(path.join(dir,file)));
 const {stdout}=await exec('ffprobe',['-v','error','-select_streams','v:0','-show_frames','-show_streams','-show_format','-show_entries','frame=best_effort_timestamp_time,pkt_duration_time:stream=width,height,avg_frame_rate,codec_name,duration:format=duration','-of','json',path.join(dir,file)],{maxBuffer:64e6});
 const probe=JSON.parse(stdout),stream=probe.streams?.[0];if(!stream||!probe.frames?.length)throw Error('No se encontraron fotogramas de vídeo');
 const raw=probe.frames.map(f=>Number(f.best_effort_timestamp_time));if(raw.some(x=>!Number.isFinite(x)))throw Error('El vídeo no tiene tiempos de fotograma válidos');const offset=raw[0],frameTimes=raw.map(t=>t-offset);if(frameTimes.some((x,i)=>i&&x<frameTimes[i-1]))throw Error('Orden temporal de fotogramas no compatible');
 const [num,den]=stream.avg_frame_rate.split('/').map(Number),fps=num/den;if(!Number.isFinite(fps)||fps<=0)throw Error('Cadencia inválida');
 const last=frameTimes.at(-1),lastDuration=Number(probe.frames.at(-1).pkt_duration_time)||1/fps;
 const v={id,label:decodeURIComponent(req.headers['x-version-label']||'')||`Versión ${project.versions.length+1}`,originalName:path.basename(originalName),file,createdAt:new Date().toISOString(),width:stream.width,height:stream.height,codec:stream.codec_name,fps:{num,den},duration:last+lastDuration,frameCount:frameTimes.length,frameTimes,sha256:hash.digest('hex'),mediaUrl:`/media/${id}/${file}`};
 const firstFrame=await readFile(await frameFile(v,0));v.sourceWidth=v.width;v.sourceHeight=v.height;v.width=firstFrame.readUInt32BE(16);v.height=firstFrame.readUInt32BE(20);
 await mutate(async()=>{project.versions.push(v);await save();});return v;
 }catch(e){await rm(dir,{recursive:true,force:true});throw e;}
}
function annotationSVG(v,n,f){const W=v.width,H=v.height,stroke=Math.max(2,W/400);const point=p=>[p.x*W,p.y*H];let marks='';n.shapes.filter(s=>s.frame===f).forEach((s,i)=>{const [x,y]=point(s.points[0]),[x2,y2]=point(s.points[1]||s.points[0]);const color='#d8ff63';if(s.type==='rect')marks+=`<rect x="${Math.min(x,x2)}" y="${Math.min(y,y2)}" width="${Math.abs(x2-x)}" height="${Math.abs(y2-y)}" fill="#d8ff6320" stroke="${color}" stroke-width="${stroke}"/>`;else if(s.type==='arrow')marks+=`<path d="M${x} ${y}L${x2} ${y2}" stroke="${color}" stroke-width="${stroke}" marker-end="url(#arrow)"/>`;else marks+=`<circle cx="${x}" cy="${y}" r="${W*.015}" fill="#d8ff6340" stroke="${color}" stroke-width="${stroke}"/>`;marks+=`<text x="${x+8}" y="${y-8}" fill="${color}" font-size="${Math.max(20,W*.023)}" font-family="sans-serif">${n.shapes.indexOf(s)+1}</text>`;});return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#d8ff63"/></marker></defs><image width="${W}" height="${H}" xlink:href="data:image/png;base64,FRAME_DATA"/>${marks}</svg>`;}
const serveQuiz=createQuizHandler(DATA);
const server=http.createServer(async(req,res)=>{try{
 if(![`${HOST}:${PORT}`,`localhost:${PORT}`].includes(req.headers.host))return json(res,{error:'Host no permitido'},403);
 if(req.method!=='GET'&&req.headers.origin&&!['http://'+req.headers.host].includes(req.headers.origin))return json(res,{error:'Origen no permitido'},403);
 const url=new URL(req.url,`http://${HOST}:${PORT}`),p=url.pathname;
 if(req.method==='GET'&&p==='/favicon.ico'){res.writeHead(204);return res.end();}
 if(await serveQuiz(req,res,p,sendFile))return;
 if(await serveStudy(req,res,p,sendFile))return;
 if(req.method==='GET'&&p==='/api/project')return json(res,project);
 if(req.method==='GET'&&p==='/api/export'){res.setHeader('Content-Disposition','attachment; filename="indicaciones.json"');return json(res,exportFeedback(project));}
 if(req.method==='POST'&&p==='/api/versions')return json(res,await importVideo(req),201);
 if(req.method==='POST'&&p==='/api/notes'){const data=await body(req),v=version(data.versionId),clean=validateNote(data,v);const n={id:randomUUID(),versionId:v.id,...clean,status:'pending',createdAt:new Date().toISOString(),snapshots:[]};for(const f of [...new Set([n.startFrame,n.endFrame,...n.shapes.map(s=>s.frame)])]){const file=await frameFile(v,f),png=await readFile(file),name=`note-${n.id}-${f}.svg`;await writeFile(path.join(DATA,v.id,name),annotationSVG(v,n,f).replace('FRAME_DATA',png.toString('base64')));n.snapshots.push({frame:f,seconds:v.frameTimes[f],image:`${v.id}/frame-${f}.png`,annotated:`${v.id}/${name}`});}await mutate(async()=>{project.notes.push(n);await save();});return json(res,n,201);}
 if(req.method==='PATCH'&&/^\/api\/notes\/[\w-]+$/.test(p)){const data=await body(req);if(!['pending','resolved'].includes(data.status))throw Error('Estado inválido');const n=project.notes.find(n=>n.id===p.split('/').at(-1));if(!n)throw Error('Nota desconocida');await mutate(async()=>{n.status=data.status;await save();});return json(res,n);}
 if(req.method==='GET'&&p.startsWith('/api/frame/')){const [, , ,id,f]=p.split('/');return await sendFile(req,res,await frameFile(version(id),Number(f)));}
 if(req.method==='GET'&&p.startsWith('/media/')){const parts=p.split('/');if(parts.length!==4)throw Error('Ruta inválida');const v=version(parts[2]),name=parts[3];if(name!==v.file&&!/^frame-\d+\.png$/.test(name)&&!/^note-[\w-]+-\d+\.svg$/.test(name))throw Error('Archivo no permitido');return await sendFile(req,res,path.join(DATA,v.id,name));}
 const files={'/study':'study.html','/study.js':'study.js','/study.css':'study.css','/':'index.html','/app.js':'app.js','/style.css':'style.css','/model.mjs':'../model.mjs'};if(req.method==='GET'&&files[p])return await sendFile(req,res,path.join(ROOT,'public',files[p]));
 json(res,{error:'No encontrado'},404);
 }catch(e){if(!res.headersSent)json(res,{error:e.message},400);else res.destroy();}});
server.listen(PORT,HOST,()=>console.log(`Review listo: http://${HOST}:${PORT}\nDatos: ${DATA}`));
