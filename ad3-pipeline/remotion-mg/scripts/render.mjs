/**
 * Render completo: node scripts/render.mjs [composición] [salida]
 *
 * `AD3-V8` entrega el anuncio entero — metraje, gráficos y mezcla.
 * `AD3-V8-Graficos` entrega solo los gráficos con alfa, para componer aparte.
 */
import {bundle} from '@remotion/bundler';
import {openBrowser, renderMedia, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs/promises';

const root = path.join(import.meta.dirname, '..');
const compId = process.argv[2] ?? 'AD3-V8';
const alpha = compId.endsWith('Graficos');
const out = process.argv[3] ?? path.join(root, 'output', `${compId}.${alpha ? 'mov' : 'mp4'}`);

const serveUrl = await bundle({
  entryPoint: path.join(root, 'src/index.tsx'),
  publicDir: path.join(root, 'public'),
});
const browser = await openBrowser('chrome', {logLevel: 'error'});
const composition = await selectComposition({serveUrl, id: compId, puppeteerInstance: browser});
await fs.mkdir(path.dirname(out), {recursive: true});

let last = -5;
await renderMedia({
  serveUrl,
  composition,
  puppeteerInstance: browser,
  codec: alpha ? 'prores' : 'h264',
  proResProfile: alpha ? '4444' : undefined,
  pixelFormat: alpha ? 'yuva444p10le' : 'yuv420p',
  crf: alpha ? undefined : 14,
  x264Preset: alpha ? undefined : 'slow',
  outputLocation: out,
  concurrency: 4,
  logLevel: 'error',
  // REMOTION_SAMPLES controla el muestreo del obturador; 1 lo desactiva.
  envVariables: Object.fromEntries(
    Object.entries(process.env).filter(([k]) => k.startsWith('REMOTION_')),
  ),
  onProgress: ({progress}) => {
    const n = Math.floor(progress * 100);
    if (n >= last + 5) {
      last = n;
      console.log(`${n}%`);
    }
  },
});
await browser.close({silent: true});
console.log(path.relative(root, out));
