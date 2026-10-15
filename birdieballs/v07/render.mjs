import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const runtime=process.env.BIRDIE_REMOTION_RUNTIME;
const resolver=createRequire(runtime?runtime+'/package.json':import.meta.url);
const {bundle}=await import(pathToFileURL(resolver.resolve('@remotion/bundler')).href);
const {renderMedia,renderStill,selectComposition,openBrowser}=await import(pathToFileURL(resolver.resolve('@remotion/renderer')).href);
import fs from 'node:fs/promises';
import path from 'node:path';
const dir=path.resolve('birdieballs/v07'),build=path.join(dir,'build');
if(process.argv.includes('--bundle')){try{const p=path.join(build,'public');if((await fs.lstat(p)).isSymbolicLink())await fs.unlink(p);}catch(e){if(e.code!=='ENOENT')throw e;}await bundle({entryPoint:path.join(dir,'index.tsx'),outDir:build,publicDir:path.join(dir,'public'),rspack:true,rootDir:runtime??path.resolve('.'),webpackOverride:config=>runtime?{...config,resolve:{...config.resolve,modules:[runtime+'/node_modules',...(config.resolve.modules??['node_modules'])]}}:config,symlinkPublicDir:true,gitSource:null,onProgress:p=>console.log('Bundle',p)});}
const browser=await openBrowser('chrome',{logLevel:'error',browserExecutable:process.env.BIRDIE_BROWSER??path.resolve('node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell')});
try{
 const serveUrl=build,composition=await selectComposition({serveUrl,id:'BirdieV07',puppeteerInstance:browser});
 if(process.argv.includes('--blur-tests')){
  for(const [label,blur] of [['bajo',.32],['medio',.58]]){await renderMedia({serveUrl,composition:{...composition,props:{blur,sound:false}},inputProps:{blur,sound:false},puppeteerInstance:browser,frameRange:[134,175],outputLocation:path.join(dir,`Blur-${label}.mp4`),codec:'h264',crf:18,x264Preset:'veryfast',scale:.5,pixelFormat:'yuv420p',concurrency:4,logLevel:'error'});console.log('Blur',label);}
 }else if(process.argv.includes('--stills')){
  const list=[['hook-entry',2.36],['hook-read',2.87],['question',3.98],['solution',9.65],['product-1',12.59],['product-2',12.68],['originales',13.49],['favorite',14.68],['lagos',15.6],['campos',16.55],['clean',20.25],['one-by-one',22.2],['mindunguis',23.8],['new',25.4],['offer-1',28.5],['offer-2',30.65],['cta',32.45],['enjoy',34.25],['end',37.4]];
  for(const [name,t] of list){if(process.argv.includes('--spot')&&!['product-1','product-2','originales','campos','offer-2','hook-entry'].includes(name))continue;await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(t*composition.fps),output:path.join(dir,'stills',name+'.jpg'),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log(name);}

 }else{
  let prev=-1;const started=Date.now();const draft=process.argv.includes('--draft');
  await renderMedia({serveUrl,composition,puppeteerInstance:browser,outputLocation:path.join(dir,draft?'Birdieballs-V07-draft.mp4':'Birdieballs-completo-V07.mp4'),codec:'h264',crf:draft?22:18,x264Preset:'veryfast',scale:draft?.5:1,pixelFormat:'yuv420p',audioBitrate:'192k',concurrency:4,logLevel:'error',onProgress:p=>{const n=Math.floor(p.progress*10);if(n>prev){prev=n;console.log(n*10+'%');}}});console.log(JSON.stringify({seconds:(Date.now()-started)/1000,draft}));
 }
}finally{await browser.close({silent:true});}
