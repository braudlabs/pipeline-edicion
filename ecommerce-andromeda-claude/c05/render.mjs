// Render de C05 con el Remotion 4.0.534 ya instalado en la raíz del proyecto editor.
//   node ecommerce-andromeda-claude/c04/render.mjs --bundle
//   node ecommerce-andromeda-claude/c04/render.mjs --still HookStudy A 12,31,62
//   node ecommerce-andromeda-claude/c04/render.mjs --still AndromedaC05 - 120,240,360   (fotogramas de revisión)
//   node ecommerce-andromeda-claude/c04/render.mjs --render [--144 | --60] [--draft]    (vídeo)
//   node ecommerce-andromeda-claude/c04/render.mjs --render --60 --range 3060-3140       (tramo suelto → study/)
// Importar @remotion/renderer tarda ~1 min en esta máquina (no es un cuelgue).
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
import fs from 'node:fs/promises';
import path from 'node:path';

const dir = path.dirname(new URL(import.meta.url).pathname);
const root = path.resolve(dir, '../..');
const req = createRequire(path.join(root, 'package.json'));
const {bundle} = await import(pathToFileURL(req.resolve('@remotion/bundler')).href);
const {renderMedia, renderStill, selectComposition, openBrowser} = await import(pathToFileURL(req.resolve('@remotion/renderer')).href);
const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const build = path.join(dir, opt('--build') ?? 'build');

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
    // Resolver react/remotion desde node_modules de la raíz del editor.
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
    const outDir = path.join(dir, 'stills', id === 'HookStudy' ? `hook-${variant}` : `film-${id}`);
    await fs.mkdir(outDir, {recursive: true});
    for (const f of frames.split(',').map(Number)) {
      const output = path.join(outDir, `f${String(f).padStart(5, '0')}.jpg`);
      await renderStill({serveUrl: build, composition, inputProps: props, puppeteerInstance: browser, frame: f, output, imageFormat: 'jpeg', jpegQuality: 88, scale: 0.5, logLevel: 'error'});
      console.log(output);
    }
  }
  if (args.includes('--render')) {
    const draft = args.includes('--draft');
    const hfr = args.includes('--144');
    const f60 = args.includes('--60');
    const range = opt('--range')?.split('-').map(Number);
    const audit = args.includes('--audit');
    const id = audit ? 'AndromedaC05-audit' : hfr ? 'AndromedaC05-144' : f60 ? 'AndromedaC05-60' : 'AndromedaC05';
    const composition = await selectComposition({serveUrl: build, id, puppeteerInstance: browser});
    const name = draft
      ? 'Andromeda-C05-draft.mp4'
      : hfr
        ? 'Andromeda-C05-00-85s-144fps-1080.mp4'
        : f60
          ? 'Andromeda-C05-00-85s-60fps-1080.mp4'
          : 'Andromeda-C05-00-85s-24fps-1080.mp4';
    // Un tramo suelto (--range a-b) nunca pisa los másteres: va a study/.
    const output = audit ? path.join(dir, 'study', 'audit-captions.mp4') : range ? path.join(dir, 'study', `tramo-${id}-${range[0]}-${range[1]}.mp4`) : path.join(dir, name);
    await fs.mkdir(path.dirname(output), {recursive: true});
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
      scale: draft || audit ? 0.5 : 1,
      muted: audit,
      pixelFormat: 'yuv420p',
      audioCodec: 'aac',
      audioBitrate: '256k',
      // 144 y 60 fps: concurrencia 3, timeout 240 s y caché de 3 GB (con más, el compositor se atascó en C03).
      concurrency: Number(opt('--concurrency') ?? (hfr || f60 ? 3 : 6)),
      timeoutInMilliseconds: 240000,
      // Con el swap casi lleno, macOS mata el compositor (SIGKILL): --cache-mb y --concurrency lo bajan.
      offthreadVideoCacheSizeInBytes: Number(opt('--cache-mb') ?? 3072) * 1024 ** 2,
      frameRange: range ? [range[0], range[1]] : undefined,
      logLevel: 'error',
      onProgress: (p) => {
        const n = Math.floor(p.progress * 20);
        if (n > last) {
          last = n;
          console.log(`${n * 5}%`);
        }
      },
    });
    const meta = {output, seconds: (Date.now() - started) / 1000, draft, fps: composition.fps, frames: range ? range[1] - range[0] + 1 : composition.durationInFrames, range: range ?? null};
    if (!range && !audit) await fs.writeFile(path.join(dir, draft ? 'render-draft.json' : hfr ? 'render-144.json' : f60 ? 'render-60.json' : 'render.json'), JSON.stringify(meta, null, 2));
    console.log(meta);
  }
} finally {
  await browser.close({silent: true});
}
