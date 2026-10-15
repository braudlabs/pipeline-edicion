import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs/promises';
import path from 'node:path';
const runtime=process.env.REMOTION_RUNTIME??'/private/tmp/birdie-v07-runtime';
const resolver=createRequire(runtime+'/package.json');
const {bundle}=await import(pathToFileURL(resolver.resolve('@remotion/bundler')).href);
const {renderMedia,renderStill,selectComposition,openBrowser}=await import(pathToFileURL(resolver.resolve('@remotion/renderer')).href);
const dir=path.resolve('ecommerce-andromeda/v03'),build=path.join(dir,'build');
if(process.argv.includes('--bundle')){
 try{const p=path.join(build,'public');if((await fs.lstat(p)).isSymbolicLink())await fs.unlink(p)}catch(e){if(e.code!=='ENOENT')throw e}
 await bundle({entryPoint:path.join(dir,'index.tsx'),outDir:build,publicDir:path.join(dir,'public'),rootDir:runtime,rspack:true,symlinkPublicDir:true,gitSource:null,webpackOverride:config=>({...config,resolve:{...config.resolve,modules:[runtime+'/node_modules',...(config.resolve.modules??['node_modules'])]}})});console.log('Bundle ready');
}
const browser=await openBrowser('chrome',{logLevel:'error',browserExecutable:process.env.BROWSER_EXECUTABLE??'/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'});
try{
 const serveUrl=build,composition=await selectComposition({serveUrl,id:'AndromedaV03',puppeteerInstance:browser});
 if(process.argv.includes('--concepts')){
  for(const variant of ['A','B','C']){const c=await selectComposition({serveUrl,id:'Concept'+variant,puppeteerInstance:browser});await renderStill({serveUrl,composition:c,puppeteerInstance:browser,frame:0,output:path.join(dir,'stills','concept-'+variant+'.jpg'),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log('Concept '+variant)}
 }else if(process.argv.includes('--stills')){
  const times=[1.3,2.5,4.15,4.95,7.7,9.6,10.45,11.25,12.2,12.8,14.1,15.15,15.9,16.9,17.9,19.5,22.6,24.85,26.6,28.2,29.8,31.95,34.5,35.9,36.9,38.05];
  for(const t of times){if(process.argv.includes('--spot')&&![35.9,36.9,38.05].includes(t))continue;await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(t*48),output:path.join(dir,'stills',`f${String(Math.round(t*48)).padStart(4,'0')}.jpg`),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log(t)}
 }else{
  const draft=process.argv.includes('--draft'),prototype=process.argv.includes('--prototype');let last=-1;const started=Date.now();
  const output=path.join(dir,prototype?'Andromeda-prototipo.mp4':draft?'Andromeda-draft.mp4':'Andromeda-00-38s-V03-PREVIEW.mp4');
  await renderMedia({serveUrl,composition,puppeteerInstance:browser,outputLocation:output,codec:'h264',crf:draft?23:18,x264Preset:'veryfast',scale:draft?.5:1,pixelFormat:'yuv420p',audioBitrate:'192k',concurrency:4,logLevel:'error',...(prototype?{frameRange:[0,629]}:{}),onProgress:p=>{const n=Math.floor(p.progress*10);if(n>last){last=n;console.log(n*10+'%')}}});
  const meta={output,seconds:(Date.now()-started)/1000,draft,prototype};await fs.writeFile(path.join(dir,prototype?'prototype-render.json':'render.json'),JSON.stringify(meta,null,2));console.log(meta);
 }
}finally{await browser.close({silent:true})}
