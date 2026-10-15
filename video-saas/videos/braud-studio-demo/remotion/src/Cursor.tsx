import React from 'react';
import {clamp, ease, mix} from './lib/motion';

export type CursorKey = {t: number; x: number; y: number; click?: boolean};

/**
 * Cursor de macOS en coordenadas de la interfaz. Entra desde fuera de cuadro, viaja con
 * curva; el clic es solo la pulsación del puntero (sin anillos: V04, más sobrio).
 */
export const Cursor: React.FC<{t: number; keys: CursorKey[]; size?: number; hideAfter?: number}> = ({t, keys, size = 30, hideAfter}) => {
  if (t < keys[0].t - 0.0001 || (hideAfter !== undefined && t > hideAfter)) return null;
  let x = keys[0].x, y = keys[0].y;
  for (let i = 1; i < keys.length; i++) {
    const a = keys[i - 1], b = keys[i];
    if (t >= b.t) { x = b.x; y = b.y; continue; }
    if (t > a.t) {
      const k = ease.inOut(clamp((t - a.t) / (b.t - a.t)));
      // arco suave: el cursor no viaja en línea recta
      const lift = Math.sin(k * Math.PI) * Math.min(60, Math.hypot(b.x - a.x, b.y - a.y) * 0.12);
      x = mix(a.x, b.x, k); y = mix(a.y, b.y, k) - lift;
    }
    break;
  }
  const press = keys.some((k) => k.click && t >= k.t - 0.06 && t < k.t + 0.08);
  return (
    <>
      <svg viewBox="0 0 28 28" width={size} height={size} style={{position: 'absolute', left: x - size * 0.2, top: y - size * 0.1,
        transform: `scale(${press ? 0.86 : 1})`, transformOrigin: '20% 10%', filter: 'drop-shadow(0 4px 8px rgba(0,0,0,.35))'}}>
        <path d="M6 3 L6 22 L11 17.5 L14.6 25 L18 23.4 L14.5 16 L21 16 Z" fill="#fff" stroke="#111" strokeWidth="1.6" strokeLinejoin="round" />
      </svg>
    </>
  );
};
