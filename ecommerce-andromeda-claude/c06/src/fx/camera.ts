import {clamp, hash, inOutSine, noise1, outCubic, outQuart, settle} from '../lib/anim';

// ───────── Cámara de C06 («upgrade infernal») ─────────
// Movimiento digital sobre el metraje: golpes de zoom, empujes lentos, zoom por escalones,
// caída y temblor. Solo escala uniforme ≥ 1 y traslación; nunca rotación (los mattes de los
// textos detrás del sujeto se transforman igual con mask-size/mask-position).
// La traslación final se acota al intervalo en que la imagen cubre todo el cuadro, así que
// ningún movimiento deja ver un borde. Los rótulos libres NO se mueven con la cámara: su
// margen seguro de Meta (x 100–980) no depende de ella.

export type Cam = {s: number; tx: number; ty: number};
const W = 1080;
const H = 1920;

type Ev =
  | {k: 'punch'; at: number; amt: number; x?: number; y?: number; attack?: number; release?: number}
  | {k: 'push'; from: number; to: number; amt: number; x?: number; y?: number; until: number}
  | {k: 'steps'; ats: number[]; amt: number; x?: number; y?: number; until: number}
  | {k: 'drop'; at: number; amt: number; frames?: number}
  | {k: 'shake'; at: number; frames: number; amp: number; seed?: number};

// Afín p → s·p + t. Aplicar A y luego B: (sB·sA, sB·tA + tB).
type Aff = {s: number; tx: number; ty: number};
const about = (s: number, x: number, y: number): Aff => ({s, tx: (1 - s) * x, ty: (1 - s) * y});
const then = (a: Aff, b: Aff): Aff => ({s: b.s * a.s, tx: b.s * a.tx + b.tx, ty: b.s * a.ty + b.ty});

function evAff(e: Ev, t: number): Aff | null {
  switch (e.k) {
    case 'punch': {
      const a = e.attack ?? 2;
      const r = e.release ?? 10;
      const age = t - e.at;
      if (age < 0 || age > a + r) return null;
      const env = age < a ? outCubic(age / a) : 1 - settle(0.9, 6)(clamp((age - a) / r));
      return about(1 + e.amt * env, e.x ?? W / 2, e.y ?? H / 2);
    }
    case 'push': {
      if (t < e.from || t >= e.until) return null;
      return about(1 + e.amt * inOutSine(clamp((t - e.from) / (e.to - e.from))), e.x ?? W / 2, e.y ?? H / 2);
    }
    case 'steps': {
      if (t < e.ats[0] || t >= e.until) return null;
      let v = 0;
      for (const at of e.ats) v += e.amt * outQuart(clamp((t - at) / 3));
      return about(1 + v, e.x ?? W / 2, e.y ?? H / 2);
    }
    case 'drop': {
      // La imagen «cae»: zoom anclado arriba (el contenido baja) y vuelve con rebote.
      const n = e.frames ?? 14;
      const age = t - e.at;
      if (age < 0 || age > n) return null;
      const env = age < 1.5 ? outCubic(age / 1.5) : 1 - settle(1.2, 5)(clamp((age - 1.5) / (n - 1.5)));
      return about(1 + e.amt * env, W / 2, 0);
    }
    case 'shake': {
      const age = t - e.at;
      if (age < 0 || age > e.frames) return null;
      const d = (1 - age / e.frames) ** 1.5;
      // Margen para temblar sin enseñar borde: escala mínima que cubre ±amp.
      const s = 1 + (2.2 * e.amp * d) / W;
      const f = 1.6; // oscilaciones por fotograma de 24 fps
      const jx = noise1(age * f, e.seed ?? 1) * e.amp * d;
      const jy = noise1(age * f, (e.seed ?? 1) + 7) * e.amp * d * 0.8;
      const c = about(s, W / 2, H / 2);
      return {s: c.s, tx: c.tx + jx, ty: c.ty + jy};
    }
  }
}

/** Composición de todos los eventos activos, acotada para que la imagen cubra el cuadro. */
export function camAt(events: Ev[], t: number): Cam {
  let a: Aff = {s: 1, tx: 0, ty: 0};
  for (const e of events) {
    const b = evAff(e, t);
    if (b) a = then(a, b);
  }
  const s = Math.max(1, a.s);
  return {s, tx: clamp(a.tx, W * (1 - s), 0), ty: clamp(a.ty, H * (1 - s), 0)};
}

export const camCss = (c: Cam) => `matrix(${c.s}, 0, 0, ${c.s}, ${c.tx}, ${c.ty})`;
export const camPt = (c: Cam, x: number, y: number): [number, number] => [c.s * x + c.tx, c.s * y + c.ty];
export const camId = (c: Cam) => c.s === 1 && c.tx === 0 && c.ty === 0;
/** Desplazamiento máximo de un píxel entre dos estados de cámara (para decidir si hay desenfoque). */
export const camDelta = (a: Cam, b: Cam) =>
  Math.max(Math.abs(a.tx - b.tx), Math.abs(a.ty - b.ty), Math.abs(a.s * W + a.tx - (b.s * W + b.tx)), Math.abs(a.s * H + a.ty - (b.s * H + b.ty)));

export type CamEvent = Ev;
export {hash};
