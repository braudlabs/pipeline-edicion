/** Renderiza fotogramas sueltos: node scripts/still.mjs <composición> <f1,f2,...> [carpeta] */
import {bundle} from '@remotion/bundler';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';
import fs from 'node:fs/promises';

const root = path.join(import.meta.dirname, '..');
const [, , compId = 'AD3-V8', list = '0', outDir = 'analysis/still', tag = ''] = process.argv;
const frames = list.split(',').map((n) => parseInt(n, 10));

const serveUrl = await bundle({
  entryPoint: path.join(root, 'src/index.tsx'),
  publicDir: path.join(root, 'public'),
});
const browser = await openBrowser('chrome', {logLevel: 'error'});
const composition = await selectComposition({serveUrl, id: compId, puppeteerInstance: browser});
await fs.mkdir(path.join(root, outDir), {recursive: true});

for (const frame of frames) {
  const output = path.join(root, outDir, `${compId}-${frame}${tag}.png`);
  await renderStill({
    serveUrl,
    composition,
    puppeteerInstance: browser,
    frame,
    output,
    overwrite: true,
    logLevel: 'error',
    envVariables: Object.fromEntries(Object.entries(process.env).filter(([k]) => k.startsWith("REMOTION_"))),
  });
  console.log(path.relative(root, output));
}
await browser.close({silent: true});
