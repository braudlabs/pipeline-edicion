import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition,openBrowser} from '@remotion/renderer';
import fs from 'node:fs/promises';
const serveUrl=await bundle({entryPoint:'src/index.tsx',webpackOverride:c=>c});
const browser=await openBrowser('chrome',{logLevel:'error'});
const composition=await selectComposition({serveUrl,id:'VisualHubAd2',puppeteerInstance:browser});
if(process.argv.includes('--stills')){
 await fs.mkdir('output/stills',{recursive:true});
 const seconds=[.65,2.6,5.95,9.9,11.9,13.75,15,16.6,20.8,21.7,24.5,28.5,31.5,35.4,37.3,39.8,41.6,44,46.6,47.8,49,50.6,53.25,54.5,56.5,58.4,58.5,60.8,62.7,65.7,68.5,70.8,72.5,73.4];
 for(let i=0;i<seconds.length;i++){
  await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(seconds[i]*24),output:`output/stills/${String(i).padStart(2,'0')}-${seconds[i]}.jpg`,imageFormat:'jpeg',scale:.5,logLevel:'error'});
  console.log('still',seconds[i]);
 }
}else{
 let last=-1;
 await renderMedia({serveUrl,composition,puppeteerInstance:browser,codec:'h264',outputLocation:'output/AD2-La-IA-te-sale-cara-FINAL.mp4',crf:17,audioBitrate:'256k',audioCodec:'aac',pixelFormat:'yuv420p',concurrency:6,x264Preset:'medium',logLevel:'error',onProgress:p=>{let n=Math.floor(p.progress*100);if(n>=last+5){last=n;console.log('render',n+'%')}}});
}
await browser.close({silent:true});
