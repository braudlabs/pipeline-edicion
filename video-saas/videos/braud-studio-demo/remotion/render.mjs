// Render con el Remotion 4.0.534 de la raíz del proyecto editor (patrón de Andrómeda C03).
//   node render.mjs --bundle
//   node render.mjs --still Avance01 2.5,9.6,12.2          (segundos → stills/)
//   node render.mjs --render Avance01 [--draft]            (vídeo; --draft = mitad de tamaño y 1 muestra de obturador)
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs/promises';
import path from 'node:path';

const dir = path.dirname(new URL(import.meta.url).pathname);
// editor/ (o EDITOR_ROOT: espacio de render fuera de iCloud, p. ej. /private/tmp/claude-render-braud)
const root = process.env.EDITOR_ROOT ?? path.resolve(dir, '../../../..');
const req = createRequire(path.join(root, 'package.json'));
const {bundle} = await import(pathToFileURL(req.resolve('@remotion/bundler')).href);
const {renderMedia, renderStill, selectComposition, openBrowser} = await import(pathToFileURL(req.resolve('@remotion/renderer')).href);
const build = path.join(dir, 'build');
const args = process.argv.slice(2);
const draft = args.includes('--draft');
const envVariables = {REMOTION_SAMPLES: process.env.REMOTION_SAMPLES ?? (draft ? '1' : '8')};

if (args.includes('--bundle')) {
  await fs.rm(build, {recursive: true, force: true});
  await bundle({
    entryPoint: path.join(dir, 'src/index.tsx'), outDir: build, publicDir: path.join(dir, 'public'), rootDir: dir,
    rspack: true, symlinkPublicDir: true, gitSource: null,
    webpackOverride: (config) => ({...config, resolve: {...config.resolve, modules: [path.join(root, 'node_modules'), ...(config.resolve?.modules ?? ['node_modules'])]}}),
  });
  console.log('bundle listo');
}

const browser = await openBrowser('chrome', {
  logLevel: 'error',
  browserExecutable: path.join(root, 'node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'),
});
try {
  const still = args.indexOf('--still');
  if (still >= 0) {
    const [id, secs] = args.slice(still + 1);
    const composition = await selectComposition({serveUrl: build, id, puppeteerInstance: browser, envVariables});
    const outDir = path.join(dir, '..', 'stills');
    await fs.mkdir(outDir, {recursive: true});
    for (const s of secs.split(',').map(Number)) {
      const output = path.join(outDir, `${id}-${s.toFixed(2)}.jpg`);
      await renderStill({serveUrl: build, composition, puppeteerInstance: browser, frame: Math.round(s * composition.fps), output,
        imageFormat: 'jpeg', jpegQuality: 88, scale: 0.5, envVariables, timeoutInMilliseconds: 120000, logLevel: 'error'});
      console.log(output);
    }
  }
  const ai = args.indexOf('--audio'); // solo la mezcla (wav), para cambiar niveles sin re-renderizar la imagen
  if (ai >= 0) {
    const id = args[ai + 1];
    const composition = await selectComposition({serveUrl: build, id, puppeteerInstance: browser, envVariables});
    const output = path.join(process.env.OUT_DIR ?? path.join(dir, '..', 'output'), `${id}-mezcla.wav`);
    await renderMedia({serveUrl: build, composition, puppeteerInstance: browser, outputLocation: output, envVariables, codec: 'wav', logLevel: 'error'});
    console.log({output});
  }
  const ri = args.indexOf('--render');
  if (ri >= 0) {
    const id = args[ri + 1];
    const composition = await selectComposition({serveUrl: build, id, puppeteerInstance: browser, envVariables});
    const output = path.join(process.env.OUT_DIR ?? path.join(dir, '..', 'output'), `${id}${draft ? '-borrador' : ''}.mp4`);
    await fs.mkdir(path.dirname(output), {recursive: true});
    const started = Date.now();
    let last = -1;
    await renderMedia({
      serveUrl: build, composition, puppeteerInstance: browser, outputLocation: output, envVariables,
      codec: 'h264', crf: draft ? 23 : 16, x264Preset: draft ? 'veryfast' : 'medium', scale: draft ? 0.5 : 1,
      pixelFormat: 'yuv420p', audioCodec: 'aac', audioBitrate: '256k', concurrency: Number(process.env.CONCURRENCY ?? 6),
      timeoutInMilliseconds: 240000, offthreadVideoCacheSizeInBytes: Number(process.env.CACHE_MB ?? 2048) * 1024 ** 2, logLevel: 'error',
      onProgress: (p) => { const n = Math.floor(p.progress * 10); if (n > last) { last = n; console.log(`${n * 10}%`); } },
    });
    console.log({output, seconds: (Date.now() - started) / 1000, frames: composition.durationInFrames});
  }
} finally {
  await browser.close({silent: true});
}
