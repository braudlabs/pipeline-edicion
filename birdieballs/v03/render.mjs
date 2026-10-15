import {renderMedia,renderStill,selectComposition,openBrowser} from '@remotion/renderer';
import fs from 'node:fs/promises';
import path from 'node:path';
const dir='birdieballs/v03',serveUrl=path.resolve('motor-editor/build-v03');
const browser=await openBrowser('chrome',{logLevel:'error'});
try{
 const plan=JSON.parse(await fs.readFile(dir+'/plan.json'));const inputProps={plan};const composition=await selectComposition({serveUrl,id:'ReferenceEdit',inputProps,puppeteerInstance:browser});
 if(process.argv.includes('--stills')){
  const states=[['anchor-before',.9],['anchor-after',1.3],['kidney',1.96],['solution',7.90],['graphic-entry',10.2],['graphic-main',11.04],['graphic-resolution',12.02],['graphic-exit',12.46],['inspection',19.82]];
  for(const [name,t]of states){await renderStill({serveUrl,composition,inputProps,puppeteerInstance:browser,frame:Math.round(t*composition.fps),output:dir+'/'+name+'.jpg',imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log(name);}
 }else{
  let prev=-1;const began=Date.now();await renderMedia({serveUrl,composition,inputProps,puppeteerInstance:browser,outputLocation:dir+'/Birdieballs-20s-V03.mp4',codec:'h264',crf:18,x264Preset:'veryfast',audioBitrate:'192k',pixelFormat:'yuv420p',concurrency:4,logLevel:'error',onProgress:p=>{const n=Math.floor(p.progress*10);if(n>prev){prev=n;console.log(n*10+'%');}}});console.log('Seconds',((Date.now()-began)/1000).toFixed(1));
 }
}finally{await browser.close({silent:true});}
