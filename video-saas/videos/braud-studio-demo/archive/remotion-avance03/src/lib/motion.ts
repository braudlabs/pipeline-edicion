// Tiempo, curvas y cámara del vídeo. Todo se escribe en segundos y se evalúa a 60 fps.
import blocksJson from '../data/blocks.json';
import wordsJson from '../data/words.json';

export const FPS = 60;
export const W = 1920;
export const H = 1080;
export const f = (s: number) => Math.round(s * FPS);
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const mix = (a: number, b: number, k: number) => a + (b - a) * k;

/** Cubic-bezier como en CSS (resuelve x→t por Newton). */
export const bezier = (x1: number, y1: number, x2: number, y2: number) => {
  const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
  const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
  const sx = (t: number) => ((ax * t + bx) * t + cx) * t;
  const sy = (t: number) => ((ay * t + by) * t + cy) * t;
  const dx = (t: number) => (3 * ax * t + 2 * bx) * t + cx;
  return (x: number) => {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    let t = x;
    for (let i = 0; i < 8; i++) {
      const e = sx(t) - x, d = dx(t);
      if (Math.abs(e) < 1e-6 || !d) break;
      t -= e / d;
    }
    return sy(clamp(t));
  };
};
export const ease = {
  linear: (x: number) => x,
  out: bezier(0.16, 1, 0.3, 1), // expo out: llegadas
  inOut: bezier(0.65, 0, 0.35, 1), // power3 in-out: viajes de cámara
  in: bezier(0.7, 0, 0.84, 0), // salidas que aceleran (zoom-through)
  soft: bezier(0.33, 0, 0.2, 1), // deriva lenta
};
export const tween = (t: number, t0: number, t1: number, a: number, b: number, e = ease.inOut) => mix(a, b, e(clamp((t - t0) / (t1 - t0))));
/** 0→1 entre t0 y t1 con curva. */
export const prog = (t: number, t0: number, t1: number, e = ease.inOut) => e(clamp((t - t0) / (t1 - t0)));

export type Cam = {x: number; y: number; z: number; rx: number; ry: number; rz: number; s: number};
export const CAM0: Cam = {x: 0, y: 0, z: 0, rx: 0, ry: 0, rz: 0, s: 1};
type Key = [number, Partial<Cam>, ((x: number) => number)?];
/** Pista de cámara por fotogramas clave; cada tramo usa la curva de su clave de llegada. */
export const track = (t: number, keys: Key[]): Cam => {
  const full = keys.map(([kt, v, e]) => [kt, {...CAM0, ...v}, e ?? ease.inOut] as const);
  if (t <= full[0][0]) return full[0][1];
  for (let i = 1; i < full.length; i++) {
    const [t1, v1, e] = full[i];
    const [t0, v0] = full[i - 1];
    if (t <= t1) {
      const k = e(clamp((t - t0) / (t1 - t0)));
      const o = {} as Cam;
      (Object.keys(v0) as (keyof Cam)[]).forEach((p) => (o[p] = mix(v0[p], v1[p], k)));
      return o;
    }
  }
  return full[full.length - 1][1];
};
/** Lleva el punto (cx, cy) del plano de interfaz (1512×900) al centro del cuadro a escala s. */
export const focus = (cx: number, cy: number, s: number, extra: Partial<Cam> = {}): Partial<Cam> => ({
  x: -s * (cx - 756), y: -s * (cy - 450), s, ...extra,
});
export const camCss = (c: Cam) =>
  `translate3d(${c.x}px, ${c.y}px, ${c.z}px) rotateX(${c.rx}deg) rotateY(${c.ry}deg) rotateZ(${c.rz}deg) scale(${c.s})`;
// Umbral de desplazamiento visible en medio fotograma. Por debajo, una sola muestra: acumular
// 8 capas a 1/8 de opacidad cuantiza los degradados suaves y deja anillos y bordes dobles en la
// interfaz clara (visto en el inicio). Solo los movimientos rápidos llevan obturador.
const MOVE_EPS: Record<keyof Cam, number> = {x: 4, y: 4, z: 15, rx: 0.25, ry: 0.25, rz: 0.2, s: 0.004};
export const camMoving = (fn: (t: number) => Cam, t: number, dt = 1 / FPS / 2) => {
  const a = fn(t - dt), b = fn(t + dt);
  return (Object.keys(a) as (keyof Cam)[]).some((k) => Math.abs(a[k] - b[k]) > MOVE_EPS[k]);
};

// Tiempos reales de la locución (whisper + guion), en segundos del audio a 1,08×.
export type Word = {block: number; text: string; a: number; b: number};
export const WORDS = wordsJson as Word[];
export const BLOCKS = blocksJson as {block: number; start: number; end: number; text: string}[];
export const block = (n: number) => BLOCKS[n - 1];
/** Inicio de la palabra `text` (sin puntuación) dentro del bloque n; `nth` si se repite. */
export const at = (n: number, text: string, nth = 0) => {
  const norm = (s: string) => s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9ñ]/g, '');
  const hits = WORDS.filter((w) => w.block === n && norm(w.text) === norm(text));
  if (!hits[nth]) throw new Error(`Palabra «${text}» no encontrada en el bloque ${n}`);
  return hits[nth].a;
};
export const endOf = (n: number, text: string, nth = 0) => {
  const i = WORDS.findIndex((w) => w.a === at(n, text, nth) && w.block === n);
  return WORDS[i].b;
};
