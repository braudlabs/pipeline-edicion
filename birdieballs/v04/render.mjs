import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition,openBrowser} from '@remotion/renderer';
import fs from 'node:fs/promises';
import path from 'node:path';
const dir=path.resolve('birdieballs/v04'),build=path.join(dir,'build');
if(process.argv.includes('--bundle')){try{const p=path.join(build,'public');if((await fs.lstat(p)).isSymbolicLink())await fs.unlink(p);}catch(e){if(e.code!=='ENOENT')throw e;}await bundle({entryPoint:path.join(dir,'index.tsx'),outDir:build,publicDir:path.join(dir,'public'),rspack:true,symlinkPublicDir:true,gitSource:null,onProgress:p=>console.log('Bundle',p)});}
const browser=await openBrowser('chrome',{logLevel:'error'});
try{
 const serveUrl=build,composition=await selectComposition({serveUrl,id:'BirdieV04',puppeteerInstance:browser});
 if(process.argv.includes('--stills')){
  const list=[['no',6.42],['gag',17.10],['cansado',1.4],['apoyo',1.9],['rinon',2.50],['solucion',9.60],['literal',10.93],['brand',12.07],['motion-entry',12.40],['motion-action',12.65],['motion-main',13.43],['motion-resolution',14.55],['motion-exit',14.84],['lagos',15.50],['campos',16.35],['ahi',19.25]];
  for(const [name,t] of list){if(process.argv.includes('--spot')&&!['no','gag','campos'].includes(name))continue;await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(t*composition.fps),output:path.join(dir,'stills',name+'.jpg'),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log(name);}
  for(const concept of (process.argv.includes('--spot')?[]:['A','B','C'])){await renderStill({serveUrl,composition:{...composition,props:{concept,sound:false}},inputProps:{concept,sound:false},puppeteerInstance:browser,frame:Math.round(13.43*composition.fps),output:path.join(dir,'stills','concept-'+concept+'.jpg'),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log('Concept',concept);}
 }else if(process.argv.includes('--test-reference')){
  const c=await selectComposition({serveUrl,id:'ReferenceRise',puppeteerInstance:browser});await fs.mkdir(path.join(dir,'reference-test'),{recursive:true});
  for(const f of [2,6,16,26,40,59]){await renderStill({serveUrl,composition:c,puppeteerInstance:browser,frame:f,output:path.join(dir,'reference-test',`f${f}.png`),imageFormat:'png',logLevel:'error'});console.log('Reference',f);}
 }else{
  let prev=-1;const started=Date.now();const draft=process.argv.includes('--draft');
  await renderMedia({serveUrl,composition,puppeteerInstance:browser,outputLocation:path.join(dir,draft?'Birdieballs-V04-draft.mp4':'Birdieballs-20s-V04.mp4'),codec:'h264',crf:draft?22:18,x264Preset:'veryfast',scale:draft?.5:1,pixelFormat:'yuv420p',audioBitrate:'192k',concurrency:4,logLevel:'error',onProgress:p=>{const n=Math.floor(p.progress*10);if(n>prev){prev=n;console.log(n*10+'%');}}});console.log(JSON.stringify({seconds:(Date.now()-started)/1000,draft}));
 }
}finally{await browser.close({silent:true});}
