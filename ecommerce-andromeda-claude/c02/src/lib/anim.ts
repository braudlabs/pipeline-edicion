// Curvas y utilidades deterministas. Todo se evalúa en fotogramas (fraccionarios permitidos
// para las submuestras del obturador); nada guarda estado entre fotogramas.

export const FPS = 24;
export const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const inv = (a: number, b: number, v: number) => (b === a ? 1 : clamp((v - a) / (b - a)));
export const sec = (s: number) => s * FPS;

export type Ease = (t: number) => number;
export const linear: Ease = (t) => t;
export const outCubic: Ease = (t) => 1 - (1 - t) ** 3;
export const outQuart: Ease = (t) => 1 - (1 - t) ** 4;
export const outQuint: Ease = (t) => 1 - (1 - t) ** 5;
export const outExpo: Ease = (t) => (t >= 1 ? 1 : 1 - 2 ** (-10 * t));
export const inCubic: Ease = (t) => t ** 3;
export const inQuad: Ease = (t) => t * t;
export const inOutCubic: Ease = (t) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2);
export const inOutSine: Ease = (t) => -(Math.cos(Math.PI * t) - 1) / 2;
/** Sobrepaso controlado (solo para énfasis que lo justifican). */
export const outBack =
  (s = 1.4): Ease =>
  (t) =>
    1 + (s + 1) * (t - 1) ** 3 + s * (t - 1) ** 2;

/**
 * Asentamiento amortiguado: llega a 1 y oscila con amplitud decreciente.
 * `cycles` oscilaciones visibles en la duración normalizada; `decay` amortigua.
 */
export const settle =
  (cycles = 1.15, decay = 5.5): Ease =>
  (t) => {
    if (t <= 0) return 0;
    if (t >= 1) return 1;
    return 1 - Math.exp(-decay * t) * Math.cos(cycles * 2 * Math.PI * t);
  };

/** Interpolación por tramos: [[frame, valor, curva hacia el siguiente], ...]. */
export function track(f: number, keys: [number, number, Ease?][]): number {
  if (f <= keys[0][0]) return keys[0][1];
  for (let i = 0; i < keys.length - 1; i++) {
    const [f0, v0, e] = keys[i];
    const [f1, v1] = keys[i + 1];
    if (f <= f1) return lerp(v0, v1, (e ?? linear)(inv(f0, f1, f)));
  }
  return keys[keys.length - 1][1];
}

/** Ruido determinista (sin Math.random) para temblores y parpadeos. */
export function hash(n: number): number {
  const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return s - Math.floor(s);
}
export function noise1(t: number, seed = 0): number {
  const i = Math.floor(t);
  const f = t - i;
  const a = hash(i + seed * 1000);
  const b = hash(i + 1 + seed * 1000);
  const u = f * f * (3 - 2 * f);
  return lerp(a, b, u) * 2 - 1;
}
