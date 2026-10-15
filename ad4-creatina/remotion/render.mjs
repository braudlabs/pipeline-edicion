import {bundle} from '@remotion/bundler';
import {openBrowser, renderMedia, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs/promises';
const root = import.meta.dirname;
const serveUrl = await bundle({entryPoint: path.join(root,'src/index.tsx'), publicDir: path.join(root,'public')});
const browser = await openBrowser('chrome',{logLevel:'error'});
const composition = await selectComposition({serveUrl, id:'Montaje-Creatina', puppeteerInstance: browser});
const out = path.join(root,'../assets/Montaje-Creatina.mp4');
await fs.mkdir(path.dirname(out),{recursive:true});
let last=-10;
await renderMedia({serveUrl, composition, puppeteerInstance: browser, codec:'h264',
  outputLocation: out, crf:14, pixelFormat:'yuv420p', x264Preset:'slow', concurrency:4, logLevel:'error',
  onProgress:({progress})=>{const n=Math.floor(progress*100); if(n>=last+20){last=n; console.log(n+'%')}}});
await browser.close({silent:true});
console.log(out);
