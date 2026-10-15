import React from 'react';
import {SF} from './Fonts';

// Sistema tipográfico C01 · Lavandería Andrómeda.
// Blanco + azul claro (acento de lectura) + azul BRAUD (UI/selección). Sin tinta oscura
// sobre el metraje: el contraste se resuelve con posición y sombra discreta.
export const INK = {
  white: '#FFFFFF',
  cream: '#FFF6E6',
  sky: '#A9CDFF',
  skyDeep: '#7FB2FF',
  azul: '#2F5BFF',
  azulDeep: '#1B37C9',
  navy: 'rgba(6,16,40,1)',
  dim: 'rgba(255,255,255,0.42)',
};

/** Identidad aprobada en el hook (variante A, «me molaba mucho»): blanco + azul claro. */
export const HERO_WHITE = {weight: 840, tracking: -0.045, color: '#FFFFFF', shadowKind: 'deep' as const};
export const HERO_SKY = {weight: 840, tracking: -0.045, color: '#A9CDFF', shadowKind: 'deep' as const};

export type ShadowKind = 'soft' | 'deep' | 'tight' | 'none';
export const shadow = (k: ShadowKind, a = 1): string => {
  switch (k) {
    case 'soft':
      return `0 2px 3px rgba(6,16,40,${0.32 * a}), 0 5px 18px rgba(6,16,40,${0.38 * a})`;
    case 'deep':
      return `0 3px 5px rgba(6,16,40,${0.34 * a}), 0 10px 34px rgba(6,16,40,${0.46 * a})`;
    case 'tight':
      return `0 1.5px 2px rgba(6,16,40,${0.45 * a}), 0 3px 10px rgba(6,16,40,${0.3 * a})`;
    default:
      return 'none';
  }
};

export type TypeSpec = {
  size: number;
  weight?: number;
  width?: number; // eje wdth en %, 100 = normal
  tracking?: number; // em
  color?: string;
  shadowKind?: ShadowKind;
  shadowAlpha?: number;
  stroke?: string; // CSS -webkit-text-stroke
  lineHeight?: number;
};

export const typeStyle = (s: TypeSpec): React.CSSProperties => ({
  fontFamily: SF,
  fontSize: s.size,
  fontWeight: s.weight ?? 700,
  fontStretch: `${s.width ?? 100}%`,
  letterSpacing: `${s.tracking ?? -0.02}em`,
  color: s.color ?? INK.white,
  textShadow: shadow(s.shadowKind ?? 'soft', s.shadowAlpha ?? 1),
  WebkitTextStroke: s.stroke,
  lineHeight: s.lineHeight ?? 1,
  whiteSpace: 'pre',
  fontKerning: 'normal',
  fontOpticalSizing: 'auto',
  fontFeatureSettings: "'kern' 1, 'liga' 1",
});

/** Capa a pantalla completa, sin interceptar nada. */
export const Layer: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div style={{position: 'absolute', inset: 0, pointerEvents: 'none', ...style}}>{children}</div>
);
