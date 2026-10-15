import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const runtime=process.env.EDITORIAL_REMOTION_RUNTIME;
const resolver=createRequire(runtime?runtime+'/package.json':import.meta.url);
console.log('Loading render runtime',runtime??'workspace');
const {bundle}=await import(pathToFileURL(resolver.resolve('@remotion/bundler')).href);
const {openBrowser,selectComposition,renderStill,renderMedia}=await import(pathToFileURL(resolver.resolve('@remotion/renderer')).href);
import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('motor-editor'),dir=path.join(root,'lab/relation-v2');
const inputProps=JSON.parse(await fs.readFile(path.join(dir,'plan.props.json'),'utf8'));
try {const p=path.join(dir,'build/public');if((await fs.lstat(p)).isSymbolicLink())await fs.unlink(p);}catch(e){if(e.code!=='ENOENT')throw e;}
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.tsx'),outDir:path.join(dir,'build'),publicDir:path.join(root,'public'),symlinkPublicDir:true,gitSource:null,rspack:true,rootDir:runtime??path.resolve('.'),webpackOverride:config=>runtime?{...config,resolve:{...config.resolve,modules:[runtime+'/node_modules',...(config.resolve.modules??['node_modules'])]}}:config,onProgress:p=>console.log('bundle',p)});
const browser=await openBrowser('chrome',{browserExecutable:path.resolve('node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'),logLevel:'error'});
try{
 const composition=await selectComposition({serveUrl,id:'ReferenceEdit',inputProps,puppeteerInstance:browser});
 const frames=[24,59,70,80,87,91,98,108,130,170];
 await fs.mkdir(path.join(dir,'stills'),{recursive:true});
 for(const frame of frames){await renderStill({serveUrl,composition,inputProps,puppeteerInstance:browser,frame,output:path.join(dir,'stills',`${frame}.png`),imageFormat:'png',scale:.5,logLevel:'error'});console.log('frame',frame);}
 await renderMedia({serveUrl,composition,inputProps,puppeteerInstance:browser,outputLocation:path.join(dir,'relation-lab.mp4'),codec:'h264',crf:18,x264Preset:'veryfast',scale:.5,concurrency:4,logLevel:'error'});
 console.log(JSON.stringify({frames:composition.durationInFrames,fps:composition.fps,output:path.join(dir,'relation-lab.mp4')}));
}finally{await browser.close({silent:true});}
