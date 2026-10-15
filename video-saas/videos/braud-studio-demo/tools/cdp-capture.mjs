// Feasibility test: capture the real Studio DOM per state and re-render it statically.
// usage: node cdp-capture.mjs <outDir>
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const CHROME='/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const out=process.argv[2];fs.mkdirSync(out,{recursive:true});
const port=9333;
const chrome=spawn(CHROME,[`--remote-debugging-port=${port}`,'--headless','--hide-scrollbars','--user-data-dir='+path.join(out,'.profile'),'about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let ws,id=0;const pending=new Map();
async function connect(){for(let i=0;i<50;i++){try{const t=await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();const p=t.find(x=>x.type==='page');if(p)return p.webSocketDebuggerUrl;}catch{}await sleep(200);}throw new Error('no chrome');}
const send=(method,params={})=>new Promise((res,rej)=>{const i=++id;pending.set(i,{res,rej});ws.send(JSON.stringify({id:i,method,params}));});
const evalJs=async expr=>{const r=await send('Runtime.evaluate',{expression:expr,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
async function shot(file){const r=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(file,Buffer.from(r.data,'base64'));}
try{
 ws=new WebSocket(await connect());
 await new Promise(r=>ws.onopen=r);
 ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.rej(new Error(m.error.message)):p.res(m.result);}};
 await send('Page.enable');await send('Runtime.enable');
 await send('Emulation.setDeviceMetricsOverride',{width:1512,height:900,deviceScaleFactor:2,mobile:false});
 const states=[
  {name:'home',url:'http://127.0.0.1:8799/?dev=1&brand=braud&homePreview=1&homeStyle=original',act:''},
  {name:'guion',url:'http://127.0.0.1:8799/?dev=1&brand=braud&homePreview=1&homeStyle=original',act:`[...document.querySelectorAll('button,a,[role=button]')].find(b=>/Más clientes/.test(b.innerText)&&b.closest('article,section,div'))?.click();await new Promise(r=>setTimeout(r,1500));[...document.querySelectorAll('button')].find(b=>/^\\s*02\\s*Guion/.test(b.innerText))?.click();`},
 ];
 for(const s of states){
  await send('Page.navigate',{url:s.url});await sleep(2500);
  if(s.act)await evalJs(`(async()=>{${s.act}})()`);
  await sleep(1800);
  await shot(path.join(out,s.name+'-live.png'));
  // Freeze: strip scripts, keep links resolvable, pin scroll and theme state.
  const html=await evalJs(`(()=>{const d=document.documentElement.cloneNode(true);d.querySelectorAll('script').forEach(s=>s.remove());const base=document.createElement('base');base.href=location.origin+'/';d.querySelector('head').prepend(base);return '<!doctype html>'+d.outerHTML;})()`);
  fs.writeFileSync(path.join(out,s.name+'.html'),html);
  await send('Page.navigate',{url:'file://'+path.join(out,s.name+'.html')});await sleep(2000);
  await shot(path.join(out,s.name+'-static.png'));
  console.log(s.name,'html',html.length);
 }
}finally{try{ws?.close();}catch{}chrome.kill();}
