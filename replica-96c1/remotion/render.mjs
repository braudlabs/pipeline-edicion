import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import fs from 'node:fs/promises';
import {execFileSync} from 'node:child_process';
const url=await bundle({entryPoint:new URL('./src/index.tsx',import.meta.url).pathname,publicDir:new URL('./public',import.meta.url).pathname});
const browser=await openBrowser('chrome',{logLevel:'error'});const c=await selectComposition({serveUrl:url,id:'Replica96c1',puppeteerInstance:browser});
await fs.mkdir(new URL('../output',import.meta.url),{recursive:true});
const dir=new URL('../analysis/remotion-frames/',import.meta.url).pathname;await fs.mkdir(dir,{recursive:true});
if(process.argv.includes('--stills')){for(const f of (process.env.FRAMES||'18,45,62,105,150,175,230,266,290,329').split(',').map(Number)){await renderStill({serveUrl:url,composition:c,puppeteerInstance:browser,frame:f,output:dir+String(f).padStart(3,'0')+'.png',logLevel:'error'});console.log('frame',f);}}
else {let last=-10;const start=Date.now();await renderMedia({serveUrl:url,composition:c,puppeteerInstance:browser,codec:'h264',outputLocation:new URL('../output/Remotion-picture.mp4',import.meta.url).pathname,crf:17,pixelFormat:'yuv420p',concurrency:4,x264Preset:'medium',logLevel:'error',onProgress:p=>{const pct=Math.floor(p.progress*100);if(pct>=last+10){last=pct;console.log(pct+'%')}}});await fs.writeFile(new URL('../analysis/remotion-render-time.json',import.meta.url),JSON.stringify({seconds:(Date.now()-start)/1000,engine:'Remotion 4.0.525',samples:"6 during movement / 1 during holds",shutter:240}));}
await browser.close({silent:true});
if(!process.argv.includes('--stills')){
 const output=new URL('../output/Replica-Remotion.mp4',import.meta.url).pathname;
 execFileSync('ffmpeg',['-v','error','-y','-i',new URL('../output/Remotion-picture.mp4',import.meta.url).pathname,'-i',new URL('./public/assets/reference-audio.wav',import.meta.url).pathname,'-map','0:v:0','-map','1:a:0','-map_metadata','-1','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','11','-movflags','+faststart',output]);
 console.log('Vídeo terminado:',output);
}
