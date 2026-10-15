import {useT} from '../lib/time';
import React from 'react';

import {clamp, inCubic, inOutCubic, outQuart, settle, track} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, typeStyle} from '../lib/type';
import {Behind} from './Masked';

// ───────── Línea grande de lectura (C02) ─────────
// Lenguaje del hook aprobado por Ale aplicado al resto: frase corta en UNA línea, SF Pro
// ~800, blanco con acento azul claro, palabras que suben con asentamiento y salida que se
// hunde. Centrada en su zona libre y ajustada para que la tinta quede dentro de los
// márgenes seguros (x≈100–980), sin columnas pegadas a los bordes.
//
// C04: cada unidad puede llevar su propia zona (planos con acercamientos, cortes internos o
// primeros planos), seguir el movimiento de la cámara con `yKeys`, usar tinta oscura sobre
// camisetas y mostrador claros, entrar desde arriba («pincha abajo») o leerse como la voz
// citada de la máquina (todo en azul claro). Sin estos campos se comporta como en C02/C03.

export const SAFE = {left: 100, right: 980};

const canvas = typeof document !== 'undefined' ? document.createElement('canvas') : null;
const cache = new Map<string, number>();
/** Anchura de tinta a 100 px con la fuente real (FontsGate garantiza que ya está cargada). */
export function widthAt100(text: string, weight: number, tracking: number): number {
  const key = `${weight}|${tracking}|${text}`;
  const hit = cache.get(key);
  if (hit !== undefined) return hit;
  const ctx = canvas!.getContext('2d')!;
  ctx.font = `${weight} 100px SFV`;
  (ctx as CanvasRenderingContext2D & {letterSpacing: string}).letterSpacing = `${tracking * 100}px`;
  const m = ctx.measureText(text);
  const w = m.actualBoundingBoxLeft + m.actualBoundingBoxRight;
  cache.set(key, w);
  return w;
}

export type BigWord = {text: string; at: number; key?: boolean; noRise?: boolean; echo?: boolean};
export type BigChunk = {
  words: BigWord[];
  from: number;
  to: number;
  size?: number;
  exit?: 'sink' | 'cut' | 'fade';
  /** Zona propia de la unidad (si no, la del bloque). */
  x?: number;
  y?: number;
  maxWidth?: number;
  /** Línea base a lo largo del tiempo [fotograma, y]: acompaña acercamientos y alejamientos. */
  yKeys?: [number, number][];
  /** 'halo': blanco y azul claro con halo oscuro difuso, para camisetas o mostrador claros. */
  ink?: 'light' | 'halo';
  /** 'down': las palabras bajan desde arriba en lugar de subir. */
  enter?: 'up' | 'down';
  /** Voz citada (la máquina): toda la línea en azul claro. */
  voice?: boolean;
  /** Una palabra que crece mientras se pronuncia («escalarás»). */
  grow?: {text: string; to: number; frames: number};
};

type Props = {
  chunks: BigChunk[];
  x: number; // centro horizontal de la zona libre
  y: number; // línea base
  maxWidth: number;
  maxSize?: number;
  weight?: number;
  tracking?: number;
  behind?: {dir: string; sceneFrom: number; srcIn: number; first: number; count: number};
  /** Estado discreto evaluado con el fotograma presentado (p. ej. apagado). */
  styleAt?: (frame: number) => React.CSSProperties | undefined;
  /** Transformación por palabra (caídas físicas, inclinaciones) con su propia curva. */
  wordMotion?: (w: BigWord, t: number) => {x?: number; y?: number; rot?: number; moving?: boolean} | undefined;
  /** Con `behind`: opacidad del contorno que se dibuja delante del sujeto (lenguaje del hook A). */
  outline?: number;
};

const E = 6;
const EXIT = 3;

const keysMoving = (keys: [number, number][] | undefined, t: number) => {
  if (!keys) return false;
  for (let i = 0; i < keys.length - 1; i++) {
    if (t >= keys[i][0] - 0.5 && t <= keys[i + 1][0] + 0.5 && keys[i][1] !== keys[i + 1][1]) return true;
  }
  return false;
};

export const BigLines: React.FC<Props> = (p) => {
  const frame = useT();
  const chunk = p.chunks.find((c) => frame >= c.from && frame < c.to);
  if (!chunk) return null;
  const weight = p.weight ?? 800;
  const tracking = p.tracking ?? -0.04;
  const text = chunk.words.map((w) => w.text).join(' ');
  const maxWidth = Math.min(chunk.maxWidth ?? p.maxWidth, (SAFE.right - SAFE.left - 24) / 1.04);
  const fit = (maxWidth / widthAt100(text, weight, tracking)) * 100;
  const size = Math.round(Math.min(chunk.size ?? p.maxSize ?? 150, fit));
  const exit = chunk.exit ?? 'sink';
  const dir = chunk.enter === 'down' ? -1 : 1;
  // Margen seguro para Meta (Ale, C04: «demasiado pegado al lateral… Meta recorta los bordes»):
  // la tinta de la línea, contando la palabra que crece, queda siempre dentro de x≈100–980.
  // La medida del lienzo subestima un 3–4 % la tinta real (corte óptico a cada tamaño, contorno):
  // se recoloca con un colchón de 12 px por lado, comprobado con study/audit-margins.py.
  const growMax = chunk.grow ? chunk.grow.to : 1;
  const inkW = 1.04 * ((widthAt100(text, weight, tracking) * size) / 100 + (growMax - 1) * (chunk.grow ? (widthAt100(chunk.grow.text, weight, tracking) * size) / 100 : 0));
  const x = Math.min(SAFE.right - 12 - inkW / 2, Math.max(SAFE.left + 12 + inkW / 2, chunk.x ?? p.x));
  const yAt = (t: number) =>
    chunk.yKeys ? track(t, chunk.yKeys.map(([f, v]) => [f, v, inOutCubic] as [number, number, typeof inOutCubic])) : chunk.y ?? p.y;
  const moving = (t: number) =>
    chunk.words.some((w) => t >= w.at - 0.5 && t < w.at + E + 5) ||
    (exit !== 'cut' && t >= chunk.to - EXIT - 0.5) ||
    keysMoving(chunk.yKeys, t) ||
    (chunk.grow !== undefined && chunk.words.some((w) => w.text === chunk.grow!.text && t >= w.at && t < w.at + chunk.grow!.frames + 0.5)) ||
    chunk.words.some((w) => p.wordMotion?.(w, t)?.moving);
  const discrete = p.styleAt?.(frame);
  // C05: Ale rechaza la tinta marino/azul BRAUD («la paleta… no me gusta»): siempre blanco + azul
  // claro; sobre fondos claros (`ink: 'halo'`) la lectura se resuelve con un halo oscuro difuso.
  const halo = chunk.ink === 'halo';
  const base = INK.white;
  const accent = INK.sky;
  const growAt = (w: BigWord, t: number) =>
    chunk.grow && w.text === chunk.grow.text ? 1 + (chunk.grow.to - 1) * outQuart(clamp((t - w.at) / chunk.grow.frames)) : 1;
  const render = (t: number, mode: 'fill' | 'stroke' = 'fill') => {
    const ex = exit === 'cut' ? 0 : clamp((t - (chunk.to - EXIT)) / EXIT);
    const sink = exit === 'sink' ? inCubic(ex) * 0.5 * size : 0;
    // La palabra que crece lo hace hacia la derecha desde su borde; la línea se desplaza la mitad
    // de lo que gana para seguir centrada y sin comerse el espacio con la palabra anterior.
    const gw = chunk.words.find((w) => chunk.grow && w.text === chunk.grow.text);
    const growShift = gw ? ((growAt(gw, t) - 1) * widthAt100(gw.text, weight, tracking) * size) / 100 / 2 : 0;
    return (
      <div
        style={{
          position: 'absolute',
          left: x,
          top: yAt(t),
          transform: `translate(-50%, -84%) translate(${-growShift}px, ${sink}px)`,
          opacity: exit === 'fade' || exit === 'sink' ? 1 - ex : 1,
          display: 'flex',
          alignItems: 'baseline',
          columnGap: '0.22em',
          fontSize: size,
          whiteSpace: 'nowrap',
          ...discrete,
        }}
      >
        {chunk.words.map((w, k) => {
          const age = t - w.at;
          const e = outQuart(clamp(age / E));
          const s = settle(0.9, 6.5)(clamp(age / (E + 5)));
          const extra = p.wordMotion?.(w, t);
          const color = chunk.voice ? INK.sky : w.key ? accent : base;
          const g = growAt(w, t);
          const style =
            mode === 'stroke'
              ? {...typeStyle({size, weight, tracking, color: 'transparent', shadowKind: 'none'}), WebkitTextStroke: `${Math.max(1.6, size / 62)}px rgba(255,255,255,0.95)`}
              : typeStyle({size, weight, tracking, color, shadowKind: halo ? 'halo' : 'hero'});
          return (
            <span
              key={k}
              style={{
                ...style,
                position: 'relative',
                zIndex: w.echo ? 0 : undefined, // el eco queda detrás de su palabra, no del vídeo
                display: 'inline-block',
                opacity: age < 0 ? 0 : mode === 'stroke' ? (p.outline ?? 0) * e * e : clamp(age / 1.5 + 0.34),
                transformOrigin: g !== 1 ? '0% 80%' : '50% 80%',
                transform: `translate(${extra?.x ?? 0}px, ${(w.noRise ? 0 : dir * (1 - (age < E ? e : s)) * 0.55 * size) + (extra?.y ?? 0)}px) rotate(${extra?.rot ?? 0}deg) scale(${g})`,
              }}
            >
              {w.echo && mode === 'fill' ? (
                <span
                  style={{
                    ...style,
                    position: 'absolute',
                    left: 0,
                    top: 0,
                    color: accent,
                    opacity: 0.5 * clamp((age - 2) / 2),
                    transform: `translate(${0.14 * size * outQuart(clamp((age - 2) / 4))}px, ${0.14 * size * outQuart(clamp((age - 2) / 4))}px)`,
                    zIndex: -1,
                  }}
                >
                  {w.text}
                </span>
              ) : null}
              {w.text}
            </span>
          );
        })}
      </div>
    );
  };
  const layer = <Shutter render={(t) => render(t, 'fill')} moving={moving} />;
  const stroke = p.behind && p.outline ? <Shutter render={(t) => render(t, 'stroke')} moving={moving} /> : null;
  return p.behind ? (
    <>
      <Behind dir={p.behind.dir} sceneFrom={p.behind.sceneFrom} srcIn={p.behind.srcIn} first={p.behind.first} count={p.behind.count}>
        {layer}
      </Behind>
      {stroke}
    </>
  ) : (
    layer
  );
};

/** Trocea con instantes: [['Y', f], ['sabes', f], ...] → palabras. */
export const ws = (items: [string, number, boolean?][]): BigWord[] => items.map(([text, at, key]) => ({text, at, key: !!key}));
