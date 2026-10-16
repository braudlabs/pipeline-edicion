import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {FPS} from './lib/motion';

// Sistema visual V04 (tras «se ve muy IA, hazlo más pro»): el lenguaje de la landing de BRAUD.
// Negro casi puro, un único haz de luz suave arriba y una línea de luz horizontal tenue.
// Sin degradados de color, sin orbes, sin grano.
export const COLORS = {
  bg: '#050506',
  ink: '#F5F5F7',
  gray: '#A1A1A6',
  dim: '#6E6E73',
  line: 'rgba(255,255,255,0.14)',
  faint: 'rgba(255,255,255,0.06)',
  coral: '#FF8F86', // acento de la landing; se usa como mucho una vez por escena
  accent: '#5B8CFF', // azul de la interfaz de Studio (solo dentro de la interfaz)
  uiInk: '#E8E9EC', // texto de la interfaz en tema oscuro
};

export const Stage: React.FC<{beam?: number; children?: React.ReactNode}> = ({beam = 1, children}) => {
  const t = useCurrentFrame() / FPS;
  const breathe = 0.85 + 0.15 * Math.sin(t * 0.9);
  return (
    <AbsoluteFill style={{background: COLORS.bg, overflow: 'hidden'}}>
      {/* haz vertical, como en la landing */}
      <div style={{position: 'absolute', left: 960 - 260, top: -120, width: 520, height: 900, opacity: 0.55 * beam * breathe,
        background: 'radial-gradient(ellipse 50% 60% at 50% 0%, rgba(255,255,255,0.16), rgba(255,255,255,0.04) 45%, rgba(255,255,255,0) 75%)'}} />
      <div style={{position: 'absolute', left: 959, top: -40, width: 2, height: 260, opacity: 0.35 * beam,
        background: 'linear-gradient(rgba(255,255,255,0), rgba(255,255,255,0.7), rgba(255,255,255,0))', filter: 'blur(1px)'}} />
      {/* viñeta suave */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse 75% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)'}} />
      {children}
    </AbsoluteFill>
  );
};
