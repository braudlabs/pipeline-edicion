import {createReadStream} from 'node:fs';
import {stat} from 'node:fs/promises';
import path from 'node:path';
const [file,label]=process.argv.slice(2);
try{
 if(!file)throw Error('Uso: node motor-editor/review/import.mjs /ruta/corte.mp4 "Versión 1"');
 const info=await stat(file);if(!info.isFile())throw Error('La ruta no es un archivo');
 const url=process.env.REVIEW_URL||'http://127.0.0.1:4317';
 const response=await fetch(url+'/api/versions',{method:'POST',headers:{'Content-Type':'application/octet-stream','Content-Length':String(info.size),'X-File-Name':encodeURIComponent(path.basename(file)),'X-Version-Label':encodeURIComponent(label||path.basename(file,path.extname(file)))},body:createReadStream(file),duplex:'half'});
 const result=await response.json();if(!response.ok)throw Error(result.error);
 console.log(JSON.stringify({id:result.id,label:result.label,frames:result.frameCount,sha256:result.sha256,url},null,2));
}catch(e){console.error(e.message);process.exitCode=1;}
