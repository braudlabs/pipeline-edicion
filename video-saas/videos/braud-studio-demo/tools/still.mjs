// Fotograma fijo de una página: node tools/still.mjs <ancho> <alto> <dpr> <espera_ms> <url> <salida.png> [<url> <salida.png>…]
import {spawn} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const CHROME = '/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell';
const [w, h, dpr, wait, ...pairs] = process.argv.slice(2);
const port = 9335, sleep = ms => new Promise(r => setTimeout(r, ms));
const profile = fs.mkdtempSync(path.join(process.env.TMPDIR || '/tmp', 'still-'));
const chrome = spawn(CHROME, [`--remote-debugging-port=${port}`, '--headless', '--hide-scrollbars', '--user-data-dir=' + profile, 'about:blank'], {stdio: 'ignore'});
let ws, id = 0; const pending = new Map();
const send = (method, params = {}) => new Promise((res, rej) => { const i = ++id; pending.set(i, {res, rej}); ws.send(JSON.stringify({id: i, method, params})); });
try {
  let url;
  for (let i = 0; i < 50 && !url; i++) { try { url = (await (await fetch(`http://127.0.0.1:${port}/json/list`)).json()).find(x => x.type === 'page')?.webSocketDebuggerUrl; } catch {} if (!url) await sleep(200); }
  ws = new WebSocket(url);
  await new Promise(r => ws.onopen = r); // attach before any await, or the open event is missed
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.rej(new Error(m.error.message)) : p.res(m.result); } };
  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', {width: +w, height: +h, deviceScaleFactor: +dpr, mobile: false});
  for (let i = 0; i < pairs.length; i += 2) {
    await send('Page.navigate', {url: pairs[i]}); await sleep(+wait);
    const r = await send('Page.captureScreenshot', {format: 'png'});
    fs.writeFileSync(pairs[i + 1], Buffer.from(r.data, 'base64')); console.log('ok', pairs[i + 1]);
  }
} catch (e) { console.error('still:', e.message); process.exitCode = 1; }
finally { try { ws?.close(); } catch {} chrome.kill(); await sleep(400); try { fs.rmSync(profile, {recursive: true, force: true}); } catch {} }
