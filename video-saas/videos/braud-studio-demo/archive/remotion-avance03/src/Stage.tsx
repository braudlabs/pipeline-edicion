import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {FPS} from './lib/motion';

// Dirección D (elegida el 15/10): escenario casi negro con brillo cobalto del anuncio y
// un punto morado; la interfaz real va encima en su tema claro.
export const COLORS = {
  ink: '#f2f3f5',
  muted: '#8a909b',
  accent: '#5b8cff',
  cobalt: '#2b4dff',
  violet: '#5b2dbf',
  uiInk: '#243448',
};

const NOISE = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='256' height='256'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 1.25 0'/></filter><rect width='256' height='256' filter='url(%23n)'/></svg>")`;

/** Fondo con textura: degradado, dos brillos que derivan muy despacio y grano vivo a 12 fps. */
export const Stage: React.FC<{glow?: number; children?: React.ReactNode}> = ({glow = 1, children}) => {
  const t = useCurrentFrame() / FPS;
  const g = Math.floor(t * 12); // el grano cambia 12 veces por segundo, como película
  const drift = (a: number, sp: number) => Math.sin(t * sp + a) * 40;
  return (
    <AbsoluteFill style={{background: 'radial-gradient(1400px 900px at 15% 110%, #16244d 0%, #0b0c10 55%, #08090b 100%)', overflow: 'hidden'}}>
      <div style={{position: 'absolute', width: 1100, height: 1100, left: -300 + drift(0, 0.21), top: 500 + drift(1, 0.17), borderRadius: '50%',
        background: COLORS.cobalt, opacity: 0.35 * glow, filter: 'blur(140px)'}} />
      <div style={{position: 'absolute', width: 800, height: 800, left: 1300 + drift(2, 0.19), top: -200 + drift(3, 0.23), borderRadius: '50%',
        background: COLORS.violet, opacity: 0.18 * glow, filter: 'blur(140px)'}} />
      {children}
      <div style={{position: 'absolute', inset: -64, backgroundImage: NOISE, opacity: 0.1, mixBlendMode: 'overlay', pointerEvents: 'none',
        transform: `translate(${((g * 37) % 64) - 32}px, ${((g * 53) % 64) - 32}px)`}} />
    </AbsoluteFill>
  );
};
