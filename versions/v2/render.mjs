import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition,openBrowser} from '@remotion/renderer';
import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
const serveUrl=await bundle({entryPoint:'src/index.tsx',webpackOverride:c=>c});
const browser=await openBrowser('chrome',{logLevel:'error'});
const composition=await selectComposition({serveUrl,id:'VisualHubAd2',puppeteerInstance:browser});
if(process.argv.includes('--stills')){
 await fs.mkdir('output/v2-stills',{recursive:true});
 const seconds=process.env.STILL_TIMES?process.env.STILL_TIMES.split(',').map(Number):[.65,2.52,2.65,6.2,10.2,13.6,15.7,16.6,20.25,20.8,21.35,21.85,29.8,31.5,38.5,39.8,41.6,44.4,44.8,45.4,46.2,46.85,47.85,48.2,48.7,49.4,50.25,53.25,56.5,60.7,63.9,68.5,71.9,72.3,73.3];
 for(let i=0;i<seconds.length;i++){
  await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(seconds[i]*24),output:`output/v2-stills/${String(i).padStart(2,'0')}-${seconds[i]}.jpg`,imageFormat:'jpeg',scale:.5,logLevel:'error'});
  console.log('still',seconds[i]);
 }
}else{
 let last=-1;
 await renderMedia({serveUrl,composition,puppeteerInstance:browser,codec:'h264',outputLocation:'output/AD2-La-IA-te-sale-cara-V2.mp4',crf:17,audioBitrate:'256k',audioCodec:'aac',pixelFormat:'yuv420p',concurrency:6,x264Preset:'medium',logLevel:'error',onProgress:p=>{let n=Math.floor(p.progress*100);if(n>=last+5){last=n;console.log('render',n+'%')}}});
  // AAC padding from the renderer is replaced with the exact, frozen mix duration.
 await fs.rename('output/AD2-La-IA-te-sale-cara-V2.mp4','output/.v2-picture.mp4');
 execFileSync('ffmpeg',['-v','error','-y','-i','output/.v2-picture.mp4','-i','public/assets/v2/audio-mix-master.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t','73.541666667','-movflags','+faststart','output/AD2-La-IA-te-sale-cara-V2.mp4']);
}
await browser.close({silent:true});
