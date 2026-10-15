// Render de C01 con el Remotion 4.0.534 ya instalado en la raíz del proyecto editor.
//   node ecommerce-andromeda-claude/c01/render.mjs --bundle
//   node ecommerce-andromeda-claude/c01/render.mjs --still HookStudy A 12,31,62
//   node ecommerce-andromeda-claude/c01/render.mjs --stills          (fotogramas de revisión)
//   node ecommerce-andromeda-claude/c01/render.mjs --render [--draft] (vídeo)
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs/promises';
import path from 'node:path';

const dir = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(dir, '../..');
const req = createRequire(path.join(root, 'package.json'));
const {bundle} = await import(pathToFileURL(req.resolve('@remotion/bundler')).href);
const {renderMedia, renderStill, selectComposition, openBrowser} = await import(pathToFileURL(req.resolve('@remotion/renderer')).href);
const build = path.join(dir, 'build');
const args = process.argv.slice(2);

if (args.includes('--bundle')) {
  await fs.rm(build, {recursive: true, force: true});
  await bundle({
    entryPoint: path.join(dir, 'src/index.tsx'),
    outDir: build,
    publicDir: path.join(dir, 'public'),
    rootDir: dir,
    rspack: true,
    symlinkPublicDir: true,
    gitSource: null,
    onProgress: (p) => (p % 25 === 0 ? console.log(`bundle ${p}%`) : null),
    webpackOverride: (config) => ({
      ...config,
      resolve: {...config.resolve, modules: [path.join(root, 'node_modules'), ...(config.resolve?.modules ?? ['node_modules'])]},
    }),
  });
  console.log('bundle listo');
}

const browser = await openBrowser('chrome', {
  logLevel: 'error',
  browserExecutable:
    process.env.BROWSER_EXECUTABLE ??
    path.join(root, 'node_modules/.remotion/chrome-headless-shell/mac-arm64/chrome-headless-shell-mac-arm64/chrome-headless-shell'),
});
try {
  const still = args.indexOf('--still');
  if (still >= 0) {
    const [id, variant, frames] = args.slice(still + 1);
    const props = variant && variant !== '-' ? {variant} : {};
    const composition = await selectComposition({serveUrl: build, id, inputProps: props, puppeteerInstance: browser});
    const outDir = path.join(dir, 'stills', id === 'HookStudy' ? `hook-${variant}` : 'film');
    await fs.mkdir(outDir, {recursive: true});
    for (const f of frames.split(',').map(Number)) {
      const output = path.join(outDir, `f${String(f).padStart(4, '0')}.jpg`);
      await renderStill({serveUrl: build, composition, inputProps: props, puppeteerInstance: browser, frame: f, output, imageFormat: 'jpeg', jpegQuality: 88, scale: 0.5, logLevel: 'error'});
      console.log(output);
    }
  }
  if (args.includes('--render')) {
    const draft = args.includes('--draft');
    const composition = await selectComposition({serveUrl: build, id: 'AndromedaC01', puppeteerInstance: browser});
    const output = path.join(dir, draft ? 'Andromeda-C01-draft.mp4' : 'Andromeda-C01-00-38s-PREVIEW.mp4');
    const started = Date.now();
    let last = -1;
    await renderMedia({
      serveUrl: build,
      composition,
      puppeteerInstance: browser,
      outputLocation: output,
      codec: 'h264',
      crf: draft ? 23 : 16,
      x264Preset: draft ? 'veryfast' : 'medium',
      scale: draft ? 0.5 : 1,
      pixelFormat: 'yuv420p',
      audioCodec: 'aac',
      audioBitrate: '256k',
      concurrency: 6,
      logLevel: 'error',
      onProgress: (p) => {
        const n = Math.floor(p.progress * 20);
        if (n > last) {
          last = n;
          console.log(`${n * 5}%`);
        }
      },
    });
    const meta = {output, seconds: (Date.now() - started) / 1000, draft};
    await fs.writeFile(path.join(dir, draft ? 'render-draft.json' : 'render.json'), JSON.stringify(meta, null, 2));
    console.log(meta);
  }
} finally {
  await browser.close({silent: true});
}
