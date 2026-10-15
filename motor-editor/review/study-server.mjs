import path from 'node:path';
import {readFile,mkdir,rename,stat} from 'node:fs/promises';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import {fileURLToPath} from 'node:url';
const exec=promisify(execFile),root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../../estilo-editor');
const data=path.join(root,'datos/revision-v2');
const read=async name=>JSON.parse(await readFile(path.join(data,name),'utf8'));
const json=(res,value)=>{res.writeHead(200,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(value));};
const pending=new Map();
let frameQueue=Promise.resolve();
async function source(slug){const manifest=JSON.parse(await readFile(path.join(root,'datos/referencias.json'),'utf8'));const entry=manifest.files.find(x=>x.slug===slug);if(!entry)throw Error('Referencia desconocida');return entry;}
async function exactFrame(s,f){
 if(!Number.isInteger(f)||f<0||f>=s.frames)throw Error('Fotograma fuera de referencia');
 const dir=path.join(data,'frame-cache',s.slug),file=path.join(dir,`${f}.png`);try{await stat(file);return file;}catch{}
 const key=s.slug+':'+f;if(pending.has(key))return pending.get(key);
 const run=frameQueue.then(async()=>{await mkdir(dir,{recursive:true});const temp=file+'.tmp.png';await exec('ffmpeg',['-v','error','-threads','2','-i',s.available_at,'-vf',`select=eq(n\\,${f})`,'-frames:v','1','-fps_mode','vfr','-y',temp],{maxBuffer:4e6});await rename(temp,file);return file;});
 frameQueue=run.catch(()=>{});pending.set(key,run);try{return await run;}finally{pending.delete(key);}
}
export async function serveStudy(req,res,p,sendFile){
 if(req.method!=='GET')return false;
 if(p==='/raw-study'){await sendFile(req,res,path.join(root,'../motor-editor/review/public/raw-study.html'));return true;}
 if(p==='/api/study/raw'){const manifest=JSON.parse(await readFile(path.join(root,'datos/raw-comparison/manifest.json'),'utf8')),pairs=JSON.parse(await readFile(path.join(root,'datos/raw-comparison/pairs.json'),'utf8'));json(res,{manifest,pairs});return true;}
 let rawMatch=/^\/study-raw-pair\/([a-z0-9-]+)\.jpg$/.exec(p);
 if(rawMatch){const pairs=JSON.parse(await readFile(path.join(root,'datos/raw-comparison/pairs.json'),'utf8'));const pair=pairs.find(x=>x.id===rawMatch[1]);if(!pair)throw Error('Comparativa desconocida');await sendFile(req,res,path.join(root,'analysis/raw-comparison/pairs',pair.sheet));return true;}
 rawMatch=/^\/study-raw-media\/([a-f0-9]{64})$/.exec(p);
 if(rawMatch){const manifest=JSON.parse(await readFile(path.join(root,'datos/raw-comparison/manifest.json'),'utf8'));const asset=manifest.files.find(x=>x.sha256===rawMatch[1]);if(!asset)throw Error('Bruto desconocido');await sendFile(req,res,asset.path);return true;}
 if(p==='/api/study'){const [corpus,rules,events]=await Promise.all(['corpus.json','rules.json','events.json'].map(read));json(res,{corpus,rules,events});return true;}
 let m=/^\/api\/study\/source\/([a-z0-9-]+)$/.exec(p);
 if(m){const s=await source(m[1]);const [tracks,words,faces,audio]=await Promise.all([read(`${s.slug}-tracks.json`),...['words','faces','audio'].map(async n=>JSON.parse(await readFile(path.join(root,'datos',s.slug,n+'.json'),'utf8')))]);json(res,{...tracks,words,faces,audio});return true;}
 m=/^\/study-media\/([a-z0-9-]+)$/.exec(p);
 if(m){await sendFile(req,res,(await source(m[1])).available_at);return true;}
 m=/^\/api\/study\/frame\/([a-z0-9-]+)\/(\d+)$/.exec(p);
 if(m){await sendFile(req,res,await exactFrame(await source(m[1]),Number(m[2])));return true;}
 m=/^\/study-evidence\/v8\/(overview-[0-5]|native-(clientes|pagar|brand|pregunta|servir|rail|tall|serve-exit|selector-[abc]|selector-detail))\.jpg$/.exec(p);
 if(m){await sendFile(req,res,path.join(root,'analysis/revision-v2/v8',m[1]+'.jpg'));return true;}
 m=/^\/study-spectro\/([a-z0-9-]+)\/(s_[0-9.]+-[0-9.]+\.png)$/.exec(p);
 if(m){await source(m[1]);await sendFile(req,res,path.join(root,'analysis/spectro',m[1],m[2]));return true;}
 if(p==='/study-fit.svg'){await sendFile(req,res,path.join(data,'v8-motion-comparison.svg'));return true;}
 if(p==='/study-selector.svg'){await sendFile(req,res,path.join(data,'v8-selector-comparison.svg'));return true;}
 if(p==='/study-font-fit.jpg'){await sendFile(req,res,path.join(root,'analysis/revision-v2/v8/font-calibration.jpg'));return true;}
 if(p==='/study-reconstruction.jpg'){await sendFile(req,res,path.join(root,'../birdieballs/v04/reference-test/comparison.jpg'));return true;}
 if(p==='/api/study/curves'){json(res,await read('v8-native-curves.json'));return true;}
 return false;
}
