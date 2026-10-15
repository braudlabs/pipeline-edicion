/**
 * Mide el render, separando el coste de arranque del de los fotogramas.
 *
 * Reutiliza un solo empaquetado y un solo navegador para las dos pasadas, de modo
 * que la diferencia entre ellas sea solo el muestreo del obturador.
 *
 * Uso: node scripts/bench.mjs [composición] [fotogramas]
 */
import {bundle} from '@remotion/bundler';
import {openBrowser, renderMedia, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs/promises';

const root = path.join(import.meta.dirname, '..');
const id = process.argv[2] ?? '05-Produccion-y-oferta';

let t = Date.now();
const serveUrl = await bundle({
  entryPoint: path.join(root, 'src/index.tsx'),
  publicDir: path.join(root, 'public'),
});
console.log('empaquetado', ((Date.now() - t) / 1000).toFixed(1), 's');

t = Date.now();
const browser = await openBrowser('chrome', {logLevel: 'error'});
console.log('navegador  ', ((Date.now() - t) / 1000).toFixed(1), 's');

const composition = await selectComposition({serveUrl, id, puppeteerInstance: browser});
const frames = composition.durationInFrames;
const out = path.join(root, 'analysis/bench.mp4');
await fs.mkdir(path.dirname(out), {recursive: true});

for (const samples of ['1', '8']) {
  t = Date.now();
  await renderMedia({
    serveUrl, composition, puppeteerInstance: browser,
    codec: 'h264', pixelFormat: 'yuv420p', crf: 18,
    outputLocation: out, concurrency: 4, logLevel: 'error',
    envVariables: {REMOTION_SAMPLES: samples},
  });
  const dt = (Date.now() - t) / 1000;
  console.log(`${id}  muestras=${samples}  ${dt.toFixed(1)} s  ${(frames / dt).toFixed(2)} fps`);
}
await browser.close({silent: true});
await fs.rm(out, {force: true});
