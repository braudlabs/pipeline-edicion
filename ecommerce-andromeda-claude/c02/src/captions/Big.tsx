import React from 'react';
import {useCurrentFrame} from 'remotion';
import {clamp, inCubic, outQuart, settle} from '../lib/anim';
import {Shutter} from '../lib/Shutter';
import {INK, typeStyle} from '../lib/type';
import {Behind} from './Masked';

// ───────── Línea grande de lectura (C02) ─────────
// Lenguaje del hook aprobado por Ale aplicado al resto: frase corta en UNA línea, SF Pro
// ~800, blanco con acento azul claro, palabras que suben con asentamiento y salida que se
// hunde. Centrada en su zona libre y ajustada para que la tinta quede dentro de los
// márgenes seguros (x≈100–980), sin columnas pegadas a los bordes.

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

export type BigWord = {text: string; at: number; key?: boolean; noRise?: boolean};
export type BigChunk = {words: BigWord[]; from: number; to: number; size?: number; exit?: 'sink' | 'cut' | 'fade'};

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
};

const E = 6;
const EXIT = 3;

export const BigLines: React.FC<Props> = (p) => {
  const frame = useCurrentFrame();
  const chunk = p.chunks.find((c) => frame >= c.from && frame < c.to);
  if (!chunk) return null;
  const weight = p.weight ?? 800;
  const tracking = p.tracking ?? -0.04;
  const text = chunk.words.map((w) => w.text).join(' ');
  const fit = (p.maxWidth / widthAt100(text, weight, tracking)) * 100;
  const size = Math.round(Math.min(chunk.size ?? p.maxSize ?? 150, fit));
  const exit = chunk.exit ?? 'sink';
  const moving = (t: number) =>
    chunk.words.some((w) => t >= w.at - 0.5 && t < w.at + E + 5) ||
    (exit !== 'cut' && t >= chunk.to - EXIT - 0.5) ||
    chunk.words.some((w) => p.wordMotion?.(w, t)?.moving);
  const discrete = p.styleAt?.(frame);
  const render = (t: number) => {
    const ex = exit === 'cut' ? 0 : clamp((t - (chunk.to - EXIT)) / EXIT);
    const sink = exit === 'sink' ? inCubic(ex) * 0.5 * size : 0;
    return (
      <div
        style={{
          position: 'absolute',
          left: p.x,
          top: p.y,
          transform: `translate(-50%, -84%) translateY(${sink}px)`,
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
          return (
            <span
              key={k}
              style={{
                ...typeStyle({size, weight, tracking, color: w.key ? INK.sky : INK.white, shadowKind: 'hero'}),
                display: 'inline-block',
                opacity: age < 0 ? 0 : clamp(age / 1.5 + 0.34),
                transformOrigin: '50% 80%',
                transform: `translate(${extra?.x ?? 0}px, ${(w.noRise ? 0 : (1 - (age < E ? e : s)) * 0.55 * size) + (extra?.y ?? 0)}px) rotate(${extra?.rot ?? 0}deg)`,
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    );
  };
  const layer = <Shutter render={render} moving={moving} />;
  return p.behind ? (
    <Behind dir={p.behind.dir} sceneFrom={p.behind.sceneFrom} srcIn={p.behind.srcIn} first={p.behind.first} count={p.behind.count}>
      {layer}
    </Behind>
  ) : (
    layer
  );
};

/** Trocea con instantes: [['Y', f], ['sabes', f], ...] → palabras. */
export const ws = (items: [string, number, boolean?][]): BigWord[] => items.map(([text, at, key]) => ({text, at, key: !!key}));
