import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition,openBrowser} from '@remotion/renderer';
import fs from 'node:fs/promises';
import path from 'node:path';
const dir=path.resolve('birdieballs/v06'),build=path.join(dir,'build');
if(process.argv.includes('--bundle')){try{const p=path.join(build,'public');if((await fs.lstat(p)).isSymbolicLink())await fs.unlink(p);}catch(e){if(e.code!=='ENOENT')throw e;}await bundle({entryPoint:path.join(dir,'index.tsx'),outDir:build,publicDir:path.join(dir,'public'),rspack:true,symlinkPublicDir:true,gitSource:null,onProgress:p=>console.log('Bundle',p)});}
const browser=await openBrowser('chrome',{logLevel:'error'});
try{
 const serveUrl=build,composition=await selectComposition({serveUrl,id:'BirdieV06',puppeteerInstance:browser});
 if(process.argv.includes('--blur-tests')){
  for(const [label,blur] of [['bajo',.32],['medio',.58]]){await renderMedia({serveUrl,composition:{...composition,props:{blur,sound:false}},inputProps:{blur,sound:false},puppeteerInstance:browser,frameRange:[134,175],outputLocation:path.join(dir,`Blur-${label}.mp4`),codec:'h264',crf:18,x264Preset:'veryfast',scale:.5,pixelFormat:'yuv420p',concurrency:4,logLevel:'error'});console.log('Blur',label);}
 }else if(process.argv.includes('--stills')){
  const list=[['lagos-water',15.5],['lagos-sand',15.8],['campos',16.25],['product',13.23],['clean',20.3],['inspect',21.18],['one-by-one',22.21],['mindunguis',23.8],['nuevas',25.4],['dialogue',26.5],['discount',29.75],['cheaper',30.65],['cta',32.48],['enjoy',34.25],['brand-end',35.82],['tagline',37.4]];
  for(const [name,t] of list){if(process.argv.includes('--spot')&&!['no','mask-main','fields'].includes(name))continue;await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(t*composition.fps),output:path.join(dir,'stills',name+'.jpg'),imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log(name);}

 }else{
  let prev=-1;const started=Date.now();const draft=process.argv.includes('--draft');
  await renderMedia({serveUrl,composition,puppeteerInstance:browser,outputLocation:path.join(dir,draft?'Birdieballs-V06-draft.mp4':'Birdieballs-completo-V06.mp4'),codec:'h264',crf:draft?22:18,x264Preset:'veryfast',scale:draft?.5:1,pixelFormat:'yuv420p',audioBitrate:'192k',concurrency:4,logLevel:'error',onProgress:p=>{const n=Math.floor(p.progress*10);if(n>prev){prev=n;console.log(n*10+'%');}}});console.log(JSON.stringify({seconds:(Date.now()-started)/1000,draft}));
 }
}finally{await browser.close({silent:true});}
