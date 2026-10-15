import {renderMedia,renderStill,selectComposition,openBrowser} from '@remotion/renderer';
import fs from 'node:fs/promises';
import path from 'node:path';
const plan=JSON.parse(await fs.readFile('birdieballs/v01/plan.json','utf8'));
const serveUrl=path.resolve('motor-editor/build');
const browser=await openBrowser('chrome',{logLevel:'error'});
try{
 const inputProps={plan};const composition=await selectComposition({serveUrl,id:'ReferenceEdit',inputProps,puppeteerInstance:browser});
 if(process.argv.includes('--stills')){
  for(const [name,seconds] of [['hook',1.4],['kidney',2.22],['solution',8.30],['literal',9.70]]){await renderStill({serveUrl,composition,inputProps,puppeteerInstance:browser,frame:Math.round(seconds*composition.fps),output:`birdieballs/v01/${name}.jpg`,imageFormat:'jpeg',scale:.5,logLevel:'error'});console.log('Diseño',name);}
 }else{
  let previous=-1;const began=Date.now();await renderMedia({serveUrl,composition,inputProps,puppeteerInstance:browser,outputLocation:'birdieballs/v01/Birdieballs-B01-V01.mp4',codec:'h264',crf:18,x264Preset:'veryfast',audioBitrate:'192k',pixelFormat:'yuv420p',concurrency:4,logLevel:'error',onProgress:p=>{const n=Math.floor(p.progress*10);if(n>previous){previous=n;console.log(`Render ${n*10}%`);}}});console.log('Render completado',((Date.now()-began)/1000).toFixed(1),'s');
 }
}finally{await browser.close({silent:true});}
