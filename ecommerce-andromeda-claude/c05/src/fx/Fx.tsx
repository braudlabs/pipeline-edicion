import {useT} from '../lib/time';
import React from 'react';
import {Img, staticFile} from 'remotion';

import {clamp, inOutSine, outCubic} from '../lib/anim';

// ───────── Efectos de luz (C05 · «más salsa») ─────────
// Ale: «el editor metía… unas luces en cualquier momento, un objeto muy importante como que lo
// reflejaba». Recursos del estudio del editor: destello localizado sobre el sujeto/objeto,
// foco que destaca la opción elegida, flash que acompaña un corte. Todo por debajo de los
// subtítulos, en fotogramas concretos y con caída rápida; nada sobre la pantalla de la maquinita.

const pad = (n: number) => String(n).padStart(4, '0');

/** Flash de luz cálida que acompaña un corte o un golpe: sube en 1 f y cae en `frames`. */
export const Flash: React.FC<{at: number; frames?: number; peak?: number; x?: number; y?: number}> = ({at, frames = 5, peak = 0.5, x = 540, y = 820}) => {
  const t = useT();
  const age = t - at;
  if (age < -1 || age > frames) return null;
  const a = age < 0 ? peak * (age + 1) : peak * (1 - age / frames) ** 2;
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        background: `radial-gradient(circle at ${x}px ${y}px, rgba(255,248,232,${a}) 0%, rgba(255,246,228,${a * 0.62}) 45%, rgba(255,244,224,${a * 0.3}) 100%)`,
        mixBlendMode: 'screen',
      }}
    />
  );
};

/** Destello de lente: halo y estela horizontal en un punto de luz (proyectores al encenderse). */
export const LensGlow: React.FC<{at: number; x: number; y: number; frames?: number; size?: number; delay?: number}> = ({
  at,
  x,
  y,
  frames = 10,
  size = 160,
  delay = 0,
}) => {
  const t = useT();
  const age = t - at - delay;
  if (age < 0 || age > frames) return null;
  const a = age < 1.5 ? clamp(age / 1.5) : (1 - (age - 1.5) / (frames - 1.5)) ** 1.6;
  const s = size * (0.8 + 0.4 * outCubic(clamp(age / frames)));
  return (
    <div style={{position: 'absolute', inset: 0, mixBlendMode: 'screen'}}>
      <div
        style={{
          position: 'absolute',
          left: x - s,
          top: y - s,
          width: 2 * s,
          height: 2 * s,
          borderRadius: '50%',
          background: `radial-gradient(circle, rgba(255,255,255,${0.95 * a}) 0%, rgba(205,228,255,${0.55 * a}) 18%, rgba(150,190,255,${0.18 * a}) 45%, rgba(150,190,255,0) 70%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          left: x - 3.2 * s,
          top: y - 0.07 * s,
          width: 6.4 * s,
          height: 0.14 * s,
          borderRadius: '50%',
          background: `radial-gradient(ellipse at center, rgba(225,238,255,${0.7 * a}) 0%, rgba(180,210,255,${0.22 * a}) 40%, rgba(180,210,255,0) 75%)`,
        }}
      />
    </div>
  );
};

/** Reflejo especular que cruza un objeto recortado por su matte (por fotograma fuente). */
export const Glint: React.FC<{
  from: number;
  frames: number;
  dir: string; // carpeta de mattes «m» (blanco + alfa = objeto)
  sceneFrom: number;
  srcIn: number;
  first: number;
  count: number;
  angle?: number;
  strength?: number;
}> = ({from, frames, dir, sceneFrom, srcIn, first, count, angle = 112, strength = 0.75}) => {
  const t = useT();
  const age = t - from;
  if (age < 0 || age > frames) return null;
  const idx = Math.max(first, Math.min(first + count - 1, Math.floor(t + 1e-6) - sceneFrom + srcIn));
  const url = staticFile(`assets/mattes/${dir}/m${pad(idx)}.png`);
  const p = -30 + 160 * inOutSine(clamp(age / frames)); // posición de la banda (%)
  const a = strength * Math.sin(Math.PI * clamp(age / frames));
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
          background: `linear-gradient(${angle}deg, rgba(255,255,255,0) ${p - 14}%, rgba(255,252,240,${a * 0.35}) ${p - 6}%, rgba(255,255,255,${a}) ${p}%, rgba(255,252,240,${a * 0.35}) ${p + 6}%, rgba(255,255,255,0) ${p + 14}%)`,
        }}
      />
    </>
  );
};

/** Foco: la opción elegida queda iluminada y el resto baja un poco (puesta en escena por luz). */
export const Spotlight: React.FC<{from: number; to: number; x: number; y: number; rx: number; ry: number; dim?: number; fade?: number}> = ({
  from,
  to,
  x,
  y,
  rx,
  ry,
  dim = 0.42,
  fade = 6,
}) => {
  const t = useT();
  if (t < from || t >= to) return null;
  const a = Math.min(outCubic(clamp((t - from) / fade)), 1 - clamp((t - (to - fade)) / fade));
  return (
    <>
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `radial-gradient(ellipse ${rx}px ${ry}px at ${x}px ${y}px, rgba(4,8,20,0) 0%, rgba(4,8,20,0) 55%, rgba(4,8,20,${dim * a}) 100%)`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          mixBlendMode: 'screen',
          background: `radial-gradient(ellipse ${rx * 0.9}px ${ry * 0.9}px at ${x}px ${y}px, rgba(255,244,214,${0.16 * a}) 0%, rgba(255,244,214,0) 70%)`,
        }}
      />
    </>
  );
};

/** Halo de luz detrás de una palabra (respuesta satisfecha: «Sí»). */
export const WordGlow: React.FC<{at: number; to: number; x: number; y: number; size?: number}> = ({at, to, x, y, size = 260}) => {
  const t = useT();
  if (t < at || t >= to) return null;
  const age = t - at;
  const a = Math.min(clamp(age / 2), 1 - clamp((t - (to - 3)) / 3)) * (1 - 0.35 * clamp(age / 10));
  const s = size * (0.75 + 0.45 * outCubic(clamp(age / 8)));
  return (
    <div
      style={{
        position: 'absolute',
        left: x - s,
        top: y - s,
        width: 2 * s,
        height: 2 * s,
        borderRadius: '50%',
        mixBlendMode: 'screen',
        background: `radial-gradient(circle, rgba(169,205,255,${0.55 * a}) 0%, rgba(169,205,255,${0.22 * a}) 35%, rgba(169,205,255,0) 70%)`,
      }}
    />
  );
};
