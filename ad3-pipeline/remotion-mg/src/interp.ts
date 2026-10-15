/**
 * Semántica de interpolación y de transformación de After Effects.
 *
 * Los fotogramas clave llegan ya normalizados desde `scripts/replay-ae.py`: cada
 * clave trae su influencia, su velocidad y su tipo, tal como los recibió AE. Aquí
 * solo se evalúan — la curva temporal de Bézier que AE deriva de influencia y
 * velocidad, y el trazado espacial suave de las tangentes automáticas.
 */

export const FPS = 48;

export type Key = {
  inInf: number;
  outInf: number;
  inSpeed: number;
  outSpeed: number;
  inType: string;
  outType: string;
  spatial?: boolean;
};

export type Track = {
  times: number[];
  values: (number | number[])[];
  keys: Key[];
  spatial?: boolean;
};

/* ------------------------------------------------------------------ Bézier */

const bez = (p1: number, p2: number, t: number) => {
  const u = 1 - t;
  return 3 * u * u * t * p1 + 3 * u * t * t * p2 + t * t * t;
};

const solve = (x1: number, x2: number, x: number) => {
  let lo = 0;
  let hi = 1;
  let t = x;
  for (let i = 0; i < 30; i++) {
    const v = bez(x1, x2, t);
    if (Math.abs(v - x) < 1e-7) return t;
    if (v < x) lo = t;
    else hi = t;
    t = (lo + hi) / 2;
  }
  return t;
};

const vec = (v: number | number[]): number[] => (Array.isArray(v) ? v : [v]);

/** Magnitud con la que AE normaliza la pendiente: euclídea si es espacial. */
const magnitude = (d: number[], spatial: boolean) =>
  d.length === 1
    ? d[0]
    : spatial
      ? Math.hypot(...d)
      : d.reduce((s, v) => s + v, 0) / d.length;

/** Fracción de valor recorrida en el segmento i, con la curva temporal de AE. */
function fraction(tr: Track, i: number, frame: number, spatial: boolean) {
  const f0 = tr.times[i];
  const f1 = tr.times[i + 1];
  const x = (f1 === f0 ? 1 : (frame - f0) / (f1 - f0));
  const a = tr.keys[i];
  const b = tr.keys[i + 1];

  // Una clave de retención mantiene su valor hasta la siguiente.
  if (a.outType === 'hold') return 0;
  if (a.outType === 'linear' && b.inType === 'linear') return x;

  const dt = (f1 - f0) / FPS;
  const v0 = vec(tr.values[i]);
  const v1 = vec(tr.values[i + 1]);
  const dv = magnitude(v1.map((v, k) => v - v0[k]), spatial);

  const x1 = a.outInf / 100;
  const x2 = 1 - b.inInf / 100;
  // La Y del punto de control es la pendiente normalizada, escalada por la influencia.
  const y1 = dv === 0 ? 0 : ((a.outSpeed * dt) / dv) * x1;
  const y2 = dv === 0 ? 1 : 1 - ((b.inSpeed * dt) / dv) * (b.inInf / 100);

  return bez(y1, y2, solve(x1, x2, x));
}

const dist = (a: number[], b: number[]) =>
  Math.hypot(...a.map((v, k) => v - b[k]));

/**
 * Tangente automática de AE en la clave i: apunta de la clave anterior a la
 * siguiente, con longitud acotada a un tercio de la distancia al vecino más
 * cercano. Esa cota es lo que impide que la trayectoria se desvíe, y hace que un
 * tramo entre dos claves iguales quede quieto en lugar de describir una curva.
 */
function tangent(values: number[][], i: number): number[] {
  const p = values[i];
  const prev = values[i - 1];
  const next = values[i + 1];
  if (!prev || !next) return p.map(() => 0);
  const dir = next.map((v, k) => v - prev[k]);
  const len = Math.hypot(...dir);
  if (len === 0) return p.map(() => 0);
  const m = Math.min(dist(p, prev), dist(next, p)) / 3;
  return dir.map((v) => (v / len) * m);
}

/** Trazado espacial entre dos claves, con las tangentes automáticas de AE. */
function spline(values: number[][], i: number, f: number) {
  const p1 = values[i];
  const p2 = values[i + 1];
  const t1 = tangent(values, i);
  const t2 = tangent(values, i + 1);
  const u = 1 - f;
  return p1.map((_, k) => {
    const c1 = p1[k] + t1[k];
    const c2 = p2[k] - t2[k];
    return u * u * u * p1[k] + 3 * u * u * f * c1 + 3 * u * f * f * c2 + f * f * f * p2[k];
  });
}

/** Evalúa una pista de fotogramas clave en un fotograma de la comp. */
export function evaluate(tr: Track, frame: number): number | number[] {
  const n = tr.times.length;
  if (n === 0) return 0;
  if (frame <= tr.times[0]) return tr.values[0];
  if (frame >= tr.times[n - 1]) return tr.values[n - 1];

  let i = 0;
  while (i < n - 2 && frame >= tr.times[i + 1]) i++;

  const spatial = Boolean(tr.spatial);
  const t = fraction(tr, i, frame, spatial);
  const v0 = tr.values[i];
  const v1 = tr.values[i + 1];

  if (!Array.isArray(v0) || !Array.isArray(v1)) {
    return (v0 as number) + ((v1 as number) - (v0 as number)) * t;
  }
  // Tres claves o más en una propiedad espacial describen una curva, no un tramo recto.
  if (spatial && n >= 3) return spline(tr.values as number[][], i, t);
  return v0.map((v, k) => v + (v1[k] - v) * t);
}

/* ------------------------------------------------------------- matrices 4×4 */
// Fila mayor internamente; `matrix3d` de CSS es columna mayor.

export type Mat = number[];

export const mul = (A: Mat, B: Mat): Mat => {
  const C = new Array(16).fill(0);
  for (let r = 0; r < 4; r++)
    for (let c = 0; c < 4; c++) {
      let s = 0;
      for (let k = 0; k < 4; k++) s += A[r * 4 + k] * B[k * 4 + c];
      C[r * 4 + c] = s;
    }
  return C;
};

export const translate = (x: number, y: number, z = 0): Mat =>
  [1, 0, 0, x, 0, 1, 0, y, 0, 0, 1, z, 0, 0, 0, 1];

export const scaleM = (x: number, y: number, z = 1): Mat =>
  [x, 0, 0, 0, 0, y, 0, 0, 0, 0, z, 0, 0, 0, 0, 1];

const rad = (d: number) => (d * Math.PI) / 180;

// AE mira con +Z hacia dentro de la pantalla y CSS con +Z hacia fuera: los giros
// en X e Y cambian de signo, el giro en Z no.
export const rotX = (d: number): Mat => {
  const c = Math.cos(rad(-d));
  const s = Math.sin(rad(-d));
  return [1, 0, 0, 0, 0, c, -s, 0, 0, s, c, 0, 0, 0, 0, 1];
};

export const rotY = (d: number): Mat => {
  const c = Math.cos(rad(-d));
  const s = Math.sin(rad(-d));
  return [c, 0, s, 0, 0, 1, 0, 0, -s, 0, c, 0, 0, 0, 0, 1];
};

export const rotZ = (d: number): Mat => {
  const c = Math.cos(rad(d));
  const s = Math.sin(rad(d));
  return [c, -s, 0, 0, s, c, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1];
};

export const toCss = (M: Mat) => {
  const o: number[] = [];
  for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) o.push(M[r * 4 + c]);
  return `matrix3d(${o.map((v) => Number(v.toFixed(6))).join(',')})`;
};

/** Color de AE (canales 0–1) a CSS. */
export const rgb = (c: number[], alpha = 1) =>
  `rgba(${c.slice(0, 3).map((v) => Math.round(v * 255)).join(',')},${alpha})`;
