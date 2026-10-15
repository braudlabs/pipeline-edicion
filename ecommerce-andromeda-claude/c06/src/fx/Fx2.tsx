import React from 'react';
import {Img, staticFile, useCurrentFrame} from 'remotion';
import {clamp, hash, inOutSine, noise1, outCubic} from '../lib/anim';
import {useT} from '../lib/time';

// ───────── Efectos de C06 («upgrade infernal») ─────────
// Vocabulario del estudio del editor (estilo-editor/notas): onda expansiva, chispas que salen
// de un objeto, destello en estrella sobre lo que refleja, fuga de luz en transiciones clave,
// viñeta para dirigir la mirada, parpadeo de exposición, grano en el gag, rayos detrás del
// sujeto, haces de proyector y flechas hacia la llamada a la acción. Paleta: blanco, azul claro
// y luz cálida; nada sobre la pantalla de la maquinita. Todo determinista (hash, sin random).

const SKY = '169,205,255';
const WHITE = '255,255,255';
const pad = (n: number) => String(n).padStart(4, '0');

/** Onda expansiva: anillo de luz que se abre desde un punto (y un eco más fino detrás). */
export const Shockwave: React.FC<{at: number; x: number; y: number; r0?: number; r1?: number; frames?: number; width?: number; rgb?: string; peak?: number; squash?: number; below?: number}> = ({
  at,
  x,
  y,
  r0 = 40,
  r1 = 620,
  frames = 14,
  width = 10,
  rgb = SKY,
  peak = 0.9,
  squash = 1,
  below,
}) => {
  const t = useT();
  const rings = [0, 2.2].map((d, k) => {
    const age = t - at - d;
    if (age < 0 || age > frames) return null;
    const p = outCubic(age / frames);
    const r = r0 + (r1 - r0) * p * (k ? 0.82 : 1);
    const a = peak * (k ? 0.45 : 1) * (1 - p) ** 1.3;
    const w = width * (k ? 0.5 : 1) * (1 - 0.65 * p);
    return (
      <div
        key={k}
        style={{
          position: 'absolute',
          left: x - r,
          top: y - r * squash,
          width: 2 * r,
          height: 2 * r * squash,
          borderRadius: '50%',
          border: `${w}px solid rgba(${rgb},${a})`,
          boxShadow: `0 0 ${3 * w + 8}px rgba(${rgb},${a * 0.85}), inset 0 0 ${3 * w + 8}px rgba(${rgb},${a * 0.5})`,
        }}
      />
    );
  });
  if (rings.every((r) => r === null)) return null;
  // `below`: nada por debajo de esa y (p. ej. el borde superior de la pantalla de la maquinita).
  return <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen', clipPath: below === undefined ? undefined : `inset(0 0 ${1920 - below}px 0)`}}>{rings}</div>;
};

/** Chispas: partículas con estela proporcional a su velocidad (desenfoque de movimiento). */
export const Burst: React.FC<{
  at: number;
  x: number;
  y: number;
  count?: number;
  speed?: number;
  spread?: number;
  dir?: number;
  gravity?: number;
  frames?: number;
  size?: number;
  seed?: number;
  rgbs?: string[];
}> = ({at, x, y, count = 24, speed = 34, spread = Math.PI * 2, dir = -Math.PI / 2, gravity = 1.1, frames = 16, size = 7, seed = 1, rgbs = [WHITE, SKY]}) => {
  const t = useT();
  const age = t - at;
  if (age < 0 || age > frames) return null;
  const parts: React.ReactNode[] = [];
  for (let i = 0; i < count; i++) {
    const h1 = hash(seed * 131 + i * 7.13);
    const h2 = hash(seed * 71 + i * 3.7 + 1);
    const h3 = hash(seed * 17 + i * 1.9 + 2);
    const life = frames * (0.5 + 0.5 * h3);
    if (age > life) continue;
    const ang = dir + (h1 - 0.5) * spread;
    const v = speed * (0.4 + 0.6 * h2);
    const vx = Math.cos(ang) * v;
    const vy0 = Math.sin(ang) * v;
    const px = x + vx * age;
    const py = y + vy0 * age + 0.5 * gravity * age * age;
    const vy = vy0 + gravity * age;
    const len = Math.max(size, Math.hypot(vx, vy) * 0.55);
    const a = (1 - age / life) ** 1.1;
    const rgb = rgbs[i % rgbs.length];
    const sz = size * (0.6 + 0.7 * hash(seed * 5 + i));
    parts.push(
      <div
        key={i}
        style={{
          position: 'absolute',
          left: px - len,
          top: py - sz / 2,
          width: len,
          height: sz,
          borderRadius: sz,
          transformOrigin: '100% 50%',
          transform: `rotate(${Math.atan2(vy, vx)}rad)`,
          background: `linear-gradient(90deg, rgba(${rgb},0), rgba(${rgb},${a}))`,
          boxShadow: `0 0 ${sz * 1.6}px rgba(${rgb},${a * 0.8})`,
        }}
      />,
    );
  }
  return <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen'}}>{parts}</div>;
};

/** Corriente ascendente: partículas que suben durante un intervalo («escalarás»). */
export const Stream: React.FC<{from: number; to: number; x0: number; x1: number; y0: number; y1: number; count?: number; seed?: number; size?: number; until?: number}> = ({
  from,
  to,
  x0,
  x1,
  y0,
  y1,
  count = 28,
  seed = 1,
  size = 6,
  until,
}) => {
  const t = useT();
  if (t < from || t > to + 18 || (until !== undefined && t >= until)) return null;
  const parts: React.ReactNode[] = [];
  for (let i = 0; i < count; i++) {
    const birth = from + (to - from - 4) * hash(seed * 13 + i);
    const life = 9 + 9 * hash(seed * 29 + i);
    const age = t - birth;
    if (age < 0 || age > life) continue;
    const p = age / life;
    const rise = (y0 - y1) * (0.7 + 0.3 * hash(seed * 41 + i));
    const x = x0 + (x1 - x0) * hash(seed * 37 + i) + Math.sin(age * 0.45 + i) * 8;
    const y = y0 - rise * outCubic(p);
    const sp = (rise / life) * 3 * (1 - p) ** 2;
    const len = Math.max(size, sp * 0.8);
    const a = Math.sin(Math.PI * p) * 0.9;
    const rgb = i % 3 ? SKY : WHITE;
    const sz = size * (0.6 + 0.6 * hash(seed * 3 + i));
    parts.push(
      <div
        key={i}
        style={{
          position: 'absolute',
          left: x - sz / 2,
          top: y,
          width: sz,
          height: len,
          borderRadius: sz,
          background: `linear-gradient(180deg, rgba(${rgb},${a}), rgba(${rgb},0))`,
          boxShadow: `0 0 ${sz * 1.8}px rgba(${rgb},${a * 0.7})`,
        }}
      />,
    );
  }
  return <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen'}}>{parts}</div>;
};

/** Destello en estrella: un objeto o una palabra «refleja» la luz un instante. */
export const Twinkle: React.FC<{at: number; x: number; y: number; size?: number; frames?: number; rgb?: string}> = ({at, x, y, size = 70, frames = 10, rgb = WHITE}) => {
  const t = useT();
  const age = t - at;
  if (age < 0 || age > frames) return null;
  const p = age / frames;
  const e = p < 0.3 ? outCubic(p / 0.3) : (1 - (p - 0.3) / 0.7) ** 1.5;
  const s = size * (0.45 + 0.55 * e);
  const bar = (rot: number, k: number) => (
    <div
      key={k}
      style={{
        position: 'absolute',
        left: -s,
        top: -s * 0.035,
        width: 2 * s,
        height: s * 0.07,
        borderRadius: s,
        transform: `rotate(${rot}deg)`,
        background: `linear-gradient(90deg, rgba(${rgb},0), rgba(${rgb},${e}) 50%, rgba(${rgb},0))`,
      }}
    />
  );
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 0, height: 0, mixBlendMode: 'screen', transform: `rotate(${18 * p}deg)`}}>
      <div style={{position: 'absolute', left: -s * 0.3, top: -s * 0.3, width: s * 0.6, height: s * 0.6, borderRadius: '50%', background: `radial-gradient(circle, rgba(${rgb},${e}) 0%, rgba(${SKY},${e * 0.5}) 40%, rgba(${SKY},0) 75%)`}} />
      {bar(0, 0)}
      {bar(90, 1)}
      {bar(45, 2)}
      {bar(-45, 3)}
    </div>
  );
};

/** Fuga de luz que cruza el cuadro (solo en transiciones clave). */
export const LightLeak: React.FC<{at: number; frames?: number; from?: 'left' | 'right'; tint?: 'warm' | 'cool'; peak?: number; y?: number}> = ({
  at,
  frames = 14,
  from = 'left',
  tint = 'warm',
  peak = 0.5,
  y = 700,
}) => {
  const t = useT();
  const age = t - at;
  if (age < 0 || age > frames) return null;
  const p = clamp(age / frames);
  const m = inOutSine(p);
  const cx = from === 'left' ? -420 + 1920 * m : 1500 - 1920 * m;
  const a = peak * Math.sin(Math.PI * p);
  const [c1, c2] = tint === 'warm' ? ['255,176,112', '255,226,178'] : ['140,190,255', '214,234,255'];
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        mixBlendMode: 'screen',
        background: `radial-gradient(ellipse 600px 980px at ${cx}px ${y}px, rgba(${c1},${a}) 0%, rgba(${c2},${a * 0.5}) 38%, rgba(${c2},0) 72%), radial-gradient(ellipse 380px 520px at ${cx + (from === 'left' ? -260 : 260)}px ${y + 520}px, rgba(${c2},${a * 0.45}) 0%, rgba(${c2},0) 70%)`,
      }}
    />
  );
};

/** Viñeta: oscurece la periferia para dirigir la mirada (o cerrar a casi negro). */
export const Vignette: React.FC<{from: number; to: number; amount?: number; fade?: number; x?: number; y?: number; rx?: number; ry?: number; clear?: number}> = ({
  from,
  to,
  amount = 0.4,
  fade = 4,
  x = 540,
  y = 960,
  rx = 760,
  ry = 1240,
  clear = 45,
}) => {
  const t = useT();
  if (t < from || t >= to) return null;
  const a = amount * Math.min(clamp((t - from) / fade), 1 - clamp((t - (to - fade)) / fade));
  return <div style={{position: 'absolute', inset: 0, background: `radial-gradient(ellipse ${rx}px ${ry}px at ${x}px ${y}px, rgba(4,8,18,0) ${clear}%, rgba(4,8,18,${a}) 100%)`}} />;
};

/** Parpadeo de exposición: estados opaco / parcial / ausente, uno por fotograma fuente. */
export const Flicker: React.FC<{at: number; pattern: number[]}> = ({at, pattern}) => {
  const t = useT();
  const i = Math.floor(t - at);
  if (i < 0 || i >= pattern.length || pattern[i] <= 0) return null;
  return <div style={{position: 'absolute', inset: 0, background: `rgba(2,4,10,${pattern[i]})`}} />;
};

/** Grano de película (solo en el gag en blanco y negro). */
export const Grain: React.FC<{from: number; to: number; amount?: number}> = ({from, to, amount = 0.18}) => {
  const t = useT();
  const f = useCurrentFrame();
  if (t < from || t >= to) return null;
  const id = `grain-${f}`;
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, mixBlendMode: 'overlay', opacity: amount}}>
      <filter id={id}>
        <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={Math.floor(t)} stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="100%" height="100%" filter={`url(#${id})`} />
    </svg>
  );
};

/** Rayos de luz detrás del sujeto: recortados con su holdout, así nacen detrás de la cabeza. */
export const Rays: React.FC<{
  from: number;
  to: number;
  x: number;
  y: number;
  holdout: {dir: string; sceneFrom: number; srcIn: number; first: number; count: number};
  peak?: number;
  radius?: number;
  spokes?: number;
}> = ({from, to, x, y, holdout, peak = 0.5, radius = 980, spokes = 20}) => {
  const t = useT();
  if (t < from || t >= to) return null;
  const a = peak * Math.min(outCubic(clamp((t - from) / 6)), 1 - clamp((t - (to - 6)) / 6));
  const idx = Math.max(holdout.first, Math.min(holdout.first + holdout.count - 1, Math.floor(t + 1e-6) - holdout.sceneFrom + holdout.srcIn));
  const url = staticFile(`assets/mattes/${holdout.dir}/h${pad(idx)}.png`);
  const rot = (t - from) * 0.35;
  const step = 360 / spokes;
  return (
    <>
      <Img src={url} style={{position: 'absolute', width: 1, height: 1, opacity: 0}} />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          mixBlendMode: 'screen',
          WebkitMaskImage: `url("${url}")`,
          maskImage: `url("${url}")`,
          WebkitMaskSize: '1080px 1920px',
          maskSize: '1080px 1920px',
          WebkitMaskRepeat: 'no-repeat',
          maskRepeat: 'no-repeat',
        }}
      >
        <div
          style={{
            position: 'absolute',
            left: x - radius,
            top: y - radius,
            width: 2 * radius,
            height: 2 * radius,
            borderRadius: '50%',
            filter: 'blur(7px)',
            background: `repeating-conic-gradient(from ${rot}deg at 50% 50%, rgba(255,246,222,0) 0deg, rgba(255,246,222,${a}) ${step * 0.16}deg, rgba(255,246,222,0) ${step * 0.42}deg, rgba(255,246,222,0) ${step}deg)`,
            WebkitMaskImage: 'radial-gradient(circle, rgba(0,0,0,1) 0%, rgba(0,0,0,0.7) 22%, rgba(0,0,0,0) 68%)',
            maskImage: 'radial-gradient(circle, rgba(0,0,0,1) 0%, rgba(0,0,0,0.7) 22%, rgba(0,0,0,0) 68%)',
          }}
        />
        <div style={{position: 'absolute', inset: 0, background: `radial-gradient(circle 420px at ${x}px ${y}px, rgba(255,240,210,${a * 0.5}) 0%, rgba(255,240,210,0) 70%)`}} />
      </div>
    </>
  );
};

/** Haz de proyector: cono de luz desde la lente hacia la imagen proyectada, con motas. */
export const Beam: React.FC<{from: number; to: number; x: number; y: number; tx: number; ty: number; w0?: number; w1?: number; peak?: number; seed?: number}> = ({
  from,
  to,
  x,
  y,
  tx,
  ty,
  w0 = 16,
  w1 = 280,
  peak = 0.32,
  seed = 1,
}) => {
  const t = useT();
  if (t < from || t >= to) return null;
  const age = t - from;
  const on = clamp(age / 1.2);
  const a = peak * on * (0.86 + 0.14 * noise1(t * 0.8, seed)) * (1 - clamp((t - (to - 3)) / 3));
  const len = Math.hypot(tx - x, ty - y);
  const ang = Math.atan2(ty - y, tx - x);
  const e = (w0 / w1) * 50;
  const motes = Array.from({length: 9}, (_, k) => {
    const u = (hash(seed * 19 + k) + age * 0.006 * (0.5 + hash(seed * 23 + k))) % 1;
    const v = (hash(seed * 31 + k) - 0.5) * (e + (50 - e) * u) * 1.6;
    const ma = a * 2.2 * Math.sin(Math.PI * u) * (0.5 + 0.5 * noise1(t * 0.5 + k, seed));
    return <div key={k} style={{position: 'absolute', left: `${u * 100}%`, top: `${50 + v}%`, width: 5, height: 5, borderRadius: 5, background: `rgba(255,250,236,${Math.max(0, ma)})`, boxShadow: `0 0 6px rgba(255,250,236,${Math.max(0, ma)})`}} />;
  });
  return (
    <div style={{position: 'absolute', left: x, top: y - w1 / 2, width: len, height: w1, transformOrigin: `0 ${w1 / 2}px`, transform: `rotate(${ang}rad)`, mixBlendMode: 'screen'}}>
      <div style={{position: 'absolute', inset: 0, filter: 'blur(10px)'}}>
        <div
          style={{
            position: 'absolute',
            inset: 0,
            clipPath: `polygon(0 ${50 - e}%, 100% 0, 100% 100%, 0 ${50 + e}%)`,
            background: `linear-gradient(90deg, rgba(255,250,236,${a}) 0%, rgba(228,238,255,${a * 0.42}) 58%, rgba(220,234,255,0) 100%)`,
          }}
        />
      </div>
      {motes}
    </div>
  );
};

/** Flechas hacia abajo para «pincha abajo»: se encienden en cascada, en azul claro. */
export const Chevrons: React.FC<{from: number; to: number; x: number; y: number; gap?: number; size?: number}> = ({from, to, x, y, gap = 58, size = 66}) => {
  const t = useT();
  if (t < from || t >= to) return null;
  const vis = Math.min(clamp((t - from) / 4), 1 - clamp((t - (to - 4)) / 4));
  return (
    <svg width={1080} height={1920} style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
      {[0, 1, 2].map((k) => {
        const local = (((t - from - 3 * k) % 9) + 9) % 9;
        const glow = local < 4 ? Math.sin((Math.PI * local) / 4) : 0;
        const a = (0.38 + 0.62 * glow) * vis;
        const cy = y + k * gap + 6 * glow;
        const pts = `${x - size / 2},${cy - size / 4} ${x},${cy + size / 4} ${x + size / 2},${cy - size / 4}`;
        return (
          <polyline
            key={k}
            points={pts}
            fill="none"
            stroke={`rgba(${SKY},${a})`}
            strokeWidth={12}
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{filter: `drop-shadow(0 0 ${6 + 10 * glow}px rgba(${SKY},${0.8 * a})) drop-shadow(0 3px 6px rgba(6,16,40,${0.45 * vis}))`}}
          />
        );
      })}
    </svg>
  );
};

/** Reflejo que recorre un polígono (la tarjeta «nuevo ángulo»): banda especular recortada. */
export const PolyGlint: React.FC<{from: number; frames: number; poly: (t: number) => [number, number][]; angle?: number; strength?: number}> = ({
  from,
  frames,
  poly,
  angle = 115,
  strength = 0.6,
}) => {
  const t = useT();
  const age = t - from;
  if (age < 0 || age > frames) return null;
  const pts = poly(t);
  const p = -30 + 160 * inOutSine(clamp(age / frames));
  const a = strength * Math.sin(Math.PI * clamp(age / frames));
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        mixBlendMode: 'screen',
        clipPath: `polygon(${pts.map(([px, py]) => `${px}px ${py}px`).join(', ')})`,
        background: `linear-gradient(${angle}deg, rgba(255,255,255,0) ${p - 12}%, rgba(255,252,240,${a * 0.35}) ${p - 5}%, rgba(255,255,255,${a}) ${p}%, rgba(255,252,240,${a * 0.35}) ${p + 5}%, rgba(255,255,255,0) ${p + 12}%)`,
      }}
    />
  );
};
