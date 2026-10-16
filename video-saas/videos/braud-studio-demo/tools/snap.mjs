// Congela vistas reales del frontal de Studio (DOM + CSS original) para montarlas en el vídeo.
// Cada toma: navega, ejecuta su guion de clics, espera y guarda
//   snaps/<nombre>.html  documento estático (sin scripts) con scroll y campos restaurados
//   snaps/<nombre>.png   captura a la DPR de shots.json (3 por defecto en este proyecto)
//   snaps/<nombre>.json  rectángulos de los elementos marcados (vídeos, botones, objetivos del cursor)
// Uso: node tools/snap.mjs shots.json [nombre…]   (con el servidor de ui/ en marcha)
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const CHROME = '/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const [shotsFile, ...only] = process.argv.slice(2);
const cfg = JSON.parse(fs.readFileSync(shotsFile, 'utf8'));
const out = path.join(root, 'snaps');
fs.mkdirSync(out, {recursive: true});
// Puerto propio por ejecución: un Chrome huérfano en un puerto fijo hacía que la herramienta se
// conectara al navegador equivocado y se colgara (15/10). Al salir, por la razón que sea, se cierra el suyo.
const port = 9400 + Math.floor(Math.random() * 500), sleep = ms => new Promise(r => setTimeout(r, ms));
const profileDir = path.join(out, '.profile-' + port);
const chrome = spawn(CHROME, [`--remote-debugging-port=${port}`, '--headless', '--hide-scrollbars', '--autoplay-policy=no-user-gesture-required',
  '--user-data-dir=' + profileDir, 'about:blank'], {stdio: 'ignore'});
for (const sig of ['SIGTERM', 'SIGINT', 'SIGHUP']) process.on(sig, () => { try { chrome.kill('SIGKILL'); } catch {} process.exit(1); });
process.on('exit', () => { try { chrome.kill('SIGKILL'); } catch {} try { fs.rmSync(profileDir, {recursive: true, force: true}); } catch {} });

let ws, id = 0;
const pending = new Map();
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, {res, rej}); ws.send(JSON.stringify({id: i, method, params})); });
const evalJs = async expr => {
  const r = await send('Runtime.evaluate', {expression: expr, awaitPromise: true, returnByValue: true});
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || JSON.stringify(r.exceptionDetails));
  return r.result.value;
};

// Helpers available to each shot's "act" script.
const HELPERS = `
window.__sleep=ms=>new Promise(r=>setTimeout(r,ms));
window.__byText=(sel,re)=>[...document.querySelectorAll(sel)].find(e=>re.test(e.innerText.trim()));
window.__find=async(sel,re,ms=6000)=>{for(let t=0;t<ms;t+=100){const e=re?__byText(sel,re):document.querySelector(sel);if(e)return e;await __sleep(100);}return null;};
window.__click=async(sel,re,wait=900)=>{const e=await __find(sel,re);if(!e)throw new Error('no '+sel+' '+re);e.scrollIntoView?.({block:'center'});e.click();await __sleep(wait);return true;};
window.__type=async(sel,text)=>{const e=document.querySelector(sel);e.focus();e.value=text;e.dispatchEvent(new Event('input',{bubbles:true}));await __sleep(200);};
`;

// Freeze: inline scroll offsets and field values, drop scripts, keep CSS resolvable from the server origin.
const FREEZE = `(()=>{
  let n=0;
  for(const e of document.querySelectorAll('*')){if(e.scrollTop||e.scrollLeft){e.setAttribute('data-snap-scroll',e.scrollTop+','+e.scrollLeft);}}
  for(const e of document.querySelectorAll('textarea')){e.textContent=e.value;}
  for(const e of document.querySelectorAll('input')){if(e.type==='checkbox'||e.type==='radio'){e.checked?e.setAttribute('checked',''):e.removeAttribute('checked');}else e.setAttribute('value',e.value);}
  for(const e of document.querySelectorAll('select')){for(const o of e.options)o.selected?o.setAttribute('selected',''):o.removeAttribute('selected');}
  for(const v of document.querySelectorAll('video')){v.setAttribute('data-snap-video',String(n++));v.removeAttribute('autoplay');}
  const d=document.documentElement.cloneNode(true);
  d.querySelectorAll('script').forEach(s=>s.remove());
  const base=document.createElement('base');base.href=location.origin+'/';d.querySelector('head').prepend(base);
  const restore=document.createElement('script');
  restore.textContent="document.querySelectorAll('[data-snap-scroll]').forEach(e=>{const [t,l]=e.dataset.snapScroll.split(',');e.scrollTop=+t;e.scrollLeft=+l;});window.scrollTo(0,"+window.scrollY+");";
  d.querySelector('body').append(restore);
  return '<!doctype html>'+d.outerHTML;
})()`;

const RECTS = marks => `(()=>{
  const r=e=>{const b=e.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height};};
  const out={viewport:{w:innerWidth,h:innerHeight,scrollY},videos:[...document.querySelectorAll('video')].map(v=>({...r(v),src:v.currentSrc||v.src,poster:v.poster})),marks:{}};
  for(const [k,[sel,re]] of Object.entries(${JSON.stringify(marks || {})})){const all=[...document.querySelectorAll(sel)];const e=re?all.find(x=>new RegExp(re).test((x.innerText||'').trim())):all[0];if(e)out.marks[k]={...r(e),text:e.innerText?.trim().slice(0,80)};}
  return out;
})()`;

try {
  for (let i = 0; i < 50; i++) {
    try { const t = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); const p = t.find(x => x.type === 'page'); if (p) { ws = new WebSocket(p.webSocketDebuggerUrl); break; } } catch {}
    await sleep(200);
  }
  await new Promise(r => ws.onopen = r);
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); } };
  await send('Page.enable'); await send('Runtime.enable');
  const {width = 1512, height = 900, theme = 'light', dpr = 2} = cfg.viewport || {};
  await send('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor: dpr, mobile: false});
  await send('Emulation.setEmulatedMedia', {features: [{name: 'prefers-color-scheme', value: theme}, {name: 'prefers-reduced-motion', value: 'reduce'}]});
  for (const shot of cfg.shots) {
    if (only.length && !only.includes(shot.name)) continue;
    // Blurs grandes (los brillos del inicio) hacen bandas a DPR 3: cada toma puede fijar su DPR.
    await send('Emulation.setDeviceMetricsOverride', {width, height, deviceScaleFactor: shot.dpr ?? dpr, mobile: false});
    // Studio remembers the last view, theme and drafts in localStorage: start every shot clean.
    await send('Storage.clearDataForOrigin', {origin: cfg.origin, storageTypes: 'local_storage,session_storage'});
    if (shot.storage) { await send('Page.navigate', {url: cfg.origin + '/api/health'}); await sleep(300); await evalJs(`Object.entries(${JSON.stringify(shot.storage)}).forEach(([k,v])=>localStorage.setItem(k,v))`); }
    await send('Page.navigate', {url: cfg.origin + (shot.url || cfg.url)});
    await sleep(shot.load ?? 2200);
    await evalJs(HELPERS);
    if (shot.act) await evalJs(`(async()=>{${shot.act}})()`);
    await sleep(shot.settle ?? 1200);
    if (shot.crops) { // regions anywhere in the page, one PNG each (page coordinates, beyond the viewport)
      const rects = await evalJs(RECTS(shot.crops).replace('scrollY}', 'scrollY}') + '.marks');
      for (const [k, r] of Object.entries(rects)) {
        const y = r.y + (await evalJs('scrollY'));
        const c = await send('Page.captureScreenshot', {format: 'png', captureBeyondViewport: true, clip: {x: r.x, y, width: r.w, height: r.h, scale: 1}});
        fs.writeFileSync(path.join(out, `${shot.name}-${k}.png`), Buffer.from(c.data, 'base64'));
      }
      fs.writeFileSync(path.join(out, shot.name + '-crops.json'), JSON.stringify(rects, null, 1));
    }
    const png = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync(path.join(out, shot.name + '.png'), Buffer.from(png.data, 'base64'));
    fs.writeFileSync(path.join(out, shot.name + '.json'), JSON.stringify(await evalJs(RECTS(shot.marks)), null, 1));
    // Marcas de desarrollo («DEV», «Explorar el inicio», «DESARROLLO / …»): delatan prototipo (feedback del Avance 03).
    const dev = await evalJs(`(()=>{const t=document.body.innerText;return [/(^|\\s)DEV(\\s|$)/m.test(document.querySelector('.edition-label')?.textContent||'')&&'DEV',/Explorar el inicio/.test(t)&&'Explorar el inicio',/DESARROLLO \\//.test(t)&&'DESARROLLO'].filter(Boolean)})()`);
    if (dev.length) console.log('AVISO marcas de desarrollo en', shot.name, dev.join(', '));
    // El documento congelado solo sirve para revisar: en piezas grandes (17 escenas) serializarlo se cuelga.
    if (!shot.noFreeze) fs.writeFileSync(path.join(out, shot.name + '.html'), await evalJs(FREEZE));
    console.log('ok', shot.name);
  }
} finally { try { ws?.close(); } catch {} chrome.kill(); }
