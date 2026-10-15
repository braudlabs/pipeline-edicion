import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition,openBrowser} from '@remotion/renderer';
import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
const serveUrl=await bundle({entryPoint:'src/index.tsx',webpackOverride:c=>c});
const browser=await openBrowser('chrome',{logLevel:'error'});
const composition=await selectComposition({serveUrl,id:'VisualHubAd2',puppeteerInstance:browser});
if(process.argv.includes('--stills')){
 await fs.mkdir('output/v5-stills',{recursive:true});
 const seconds=process.env.STILL_TIMES?process.env.STILL_TIMES.split(',').map(Number):[.2,1.8,2.2,4.8,7.7,11.5,13.5,14.4,17.55,18.35,19,25.6,34.4,36.7,37.7,38.2,38.8,39.3,39.7,40.2,41,41.6,42,42.5,43.3,43.7,44.2,44.85,46.4,54,58.8,64.3,64.7,65.6];
 for(let i=0;i<seconds.length;i++){
  await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:Math.round(seconds[i]*composition.fps),output:`output/v5-stills/${String(i).padStart(2,'0')}-${seconds[i]}.jpg`,imageFormat:'jpeg',scale:.5,logLevel:'error'});
  console.log('still',seconds[i]);
 }
}else{
 let last=-1;
 await renderMedia({serveUrl,composition,puppeteerInstance:browser,codec:'h264',outputLocation:'output/AD2-La-IA-te-sale-cara-V5.mp4',crf:17,audioBitrate:'256k',audioCodec:'aac',pixelFormat:'yuv420p',concurrency:6,x264Preset:'medium',logLevel:'error',onProgress:p=>{let n=Math.floor(p.progress*100);if(n>=last+5){last=n;console.log('render',n+'%')}}});
  // AAC padding from the renderer is replaced with the exact, frozen mix duration.
 await fs.rename('output/AD2-La-IA-te-sale-cara-V5.mp4','output/.v5-picture.mp4');
 execFileSync('ffmpeg',['-v','error','-y','-i','output/.v5-picture.mp4','-i','public/assets/v3/audio-mix-master.wav','-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',String(composition.durationInFrames/composition.fps),'-movflags','+faststart','output/AD2-La-IA-te-sale-cara-V5.mp4']);
}
await browser.close({silent:true});
