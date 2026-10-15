import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs/promises';
import path from 'node:path';
const runtime=process.env.REMOTION_RUNTIME??'/private/tmp/birdie-v07-runtime';
const resolver=createRequire(runtime+'/package.json');
const {bundle}=await import(pathToFileURL(resolver.resolve('@remotion/bundler')).href);
const {renderMedia,renderStill,selectComposition,openBrowser}=await import(pathToFileURL(resolver.resolve('@remotion/renderer')).href);
const dir=path.resolve('mercadillo/v01'),build=path.join(dir,'build');
if(process.argv.includes('--bundle')){
 try{const p=path.join(build,'public');if((await fs.lstat(p)).isSymbolicLink())await fs.unlink(p)}catch(e){if(e.code!=='ENOENT')throw e}
 await bundle({entryPoint:path.join(dir,'index.tsx'),outDir:build,publicDir:path.join(dir,'public'),rootDir:runtime,rspack:true,symlinkPublicDir:true,gitSource:null,webpackOverride:config=>({...config,resolve:{...config.resolve,modules:[runtime+'/node_modules',...(config.resolve.modules??['node_modules'])]}})});console.log('Bundle ready');
}
const browser=await openBrowser('chrome',{logLevel:'error',browserExecutable:process.env.BROWSER_EXECUTABLE??'/Users/alejandrorubiocamarero/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell'});
try{
 const serveUrl=build,composition=await selectComposition({serveUrl,id:'MercadilloV01',puppeteerInstance:browser});
 if(process.argv.includes('--concepts')){
  for(const variant of ['A','B','C']){const c=await selectComposition({serveUrl,id:'Concept'+variant,puppeteerInstance:browser});await renderStill({serveUrl,composition:c,puppeteerInstance:browser,frame:0,output:path.join(dir,'stills','concept-'+variant+'.jpg'),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log('Concept '+variant)}
 }else if(process.argv.includes('--stills')){
  const times=[.2,.7,1.3,2.4,3.6,5.8,7.95,8.8,10.3,12.7,14.1,16.8,19.0,20.3,21.4,23.4,24.7,26.3,27.8,30.6,34.8,38.9,39.45,40.9,42.7,44.7,48.75,50.85,51.9,54.2,58.85,60.7,62.8,65.8,68.6,70.4,71.2,73.0,74.5,76.8,79.1,81.5,83.3,87.6];
  for(const t of times){if(process.argv.includes('--spot')&&![12.7,34.8,81.5].includes(t))continue;await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(t*24),output:path.join(dir,'stills',`f${String(Math.round(t*24)).padStart(4,'0')}.jpg`),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log(t)}
 }else{
  const draft=process.argv.includes('--draft'),prototype=process.argv.includes('--prototype');let last=-1;const started=Date.now();
  const output=path.join(dir,prototype?'Mercadillo-prototipo.mp4':draft?'Mercadillo-draft.mp4':'Mercadillo-agencias-V01.mp4');
  await renderMedia({serveUrl,composition,puppeteerInstance:browser,outputLocation:output,codec:'h264',crf:draft?23:18,x264Preset:'veryfast',scale:draft?.5:1,pixelFormat:'yuv420p',audioBitrate:'192k',concurrency:4,logLevel:'error',...(prototype?{frameRange:[0,314]}:{}),onProgress:p=>{const n=Math.floor(p.progress*10);if(n>last){last=n;console.log(n*10+'%')}}});
  const meta={output,seconds:(Date.now()-started)/1000,draft,prototype};await fs.writeFile(path.join(dir,prototype?'prototype-render.json':'render.json'),JSON.stringify(meta,null,2));console.log(meta);
 }
}finally{await browser.close({silent:true})}
