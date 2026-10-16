import React from 'react';
import {Module, Rect, snapSize} from './UIPlane';
import {ease, prog} from './lib/motion';

/**
 * Módulo con la entrada y la salida del sistema V04: sube y aparece en `enter` s, sale hacia arriba
 * en `exit` s. El siguiente módulo entra cuando este ya ha salido: dos módulos a la vez dejan fantasmas. Anclado por arriba (`top`) y centrado en `cx`. Las tarjetas de sección del frontal ya
 * traen su borde: para ellas, `edge={false}` y el radio de la tarjeta (24 px CSS × escala).
 */
export const Panel: React.FC<{t: number; t0: number; t1: number; snap: string; crop?: Rect; s: number; top: number; cx?: number;
  radius?: number; edge?: boolean; enter?: number; exit?: number; dy?: number; dx?: number; children?: React.ReactNode}> = (
  {t, t0, t1, snap, crop, s, top, cx = 960, radius, edge = true, enter = 0.6, exit = 0.32, dy = 0, dx = 0, children}) => {
  if (t < t0 - 0.02 || t > t1 + exit) return null;
  const [w, h] = snapSize(snap);
  const c = crop ?? {x: 0, y: 0, w, h};
  const k = prog(t, t0, t0 + enter, ease.out), o = prog(t, t1, t1 + exit, ease.in);
  return (
    <Module snap={snap} crop={c} cx={cx + dx} cy={top + (c.h * s) / 2} s={s} radius={radius ?? (edge ? 22 : 24 * s)} edge={edge}
      dy={(1 - k) * 110 - o * 70 + dy} opacity={k * (1 - o)}>{children}</Module>
  );
};

/** Velo sobre una región (coordenadas de la captura): atenúa lo que la voz aún no ha nombrado. */
export const Veil: React.FC<{r: Rect; k: number; color?: string; max?: number}> = ({r, k, color = '#1b1c21', max = 0.62}) =>
  k >= 1 ? null : <div style={{position: 'absolute', left: r.x, top: r.y, width: r.w, height: r.h, background: color, opacity: max * (1 - k)}} />;

/** Cortina que descubre una región de izquierda a derecha (texto que «se escribe»). */
export const Wipe: React.FC<{r: Rect; k: number; color?: string}> = ({r, k, color = '#1b1c21'}) =>
  k >= 1 ? null : (
    <div style={{position: 'absolute', left: r.x + r.w * k, top: r.y, width: r.w * (1 - k) + 2, height: r.h, background: color,
      WebkitMaskImage: 'linear-gradient(90deg, transparent 0, #000 28px)'}} />
  );

/** Punto de un recorte → coordenadas del cuadro, para un módulo anclado por arriba. */
export const panelPoint = (crop: Rect, s: number, top: number, x: number, y: number, cx = 960) =>
  ({x: cx - (crop.w * s) / 2 + (x - crop.x) * s, y: top + (y - crop.y) * s});

/**
 * Cámara sobre la interfaz real (V06, tras «esos bloques son super cutres»): una ventana fija de
 * `win` px en pantalla y, dentro, la captura que se desliza y se amplía hasta el campo que nombra la
 * voz. Claves: [t, cx, cy, z] en coordenadas de la captura; entre claves, ease.inOut.
 */
export type CamKey = [number, number, number, number];
export const camAt = (t: number, keys: CamKey[]) => {
  if (t <= keys[0][0]) return keys[0];
  for (let i = 1; i < keys.length; i++) {
    const [t1, x1, y1, z1] = keys[i], [t0, x0, y0, z0] = keys[i - 1];
    if (t <= t1) {
      const k = ease.inOut(Math.min(1, Math.max(0, (t - t0) / Math.max(1e-6, t1 - t0))));
      return [t, x0 + (x1 - x0) * k, y0 + (y1 - y0) * k, z0 + (z1 - z0) * k] as CamKey;
    }
  }
  return keys[keys.length - 1];
};
export const UICam: React.FC<{t: number; t0: number; t1: number; snap: string; keys: CamKey[]; win: [number, number]; top: number;
  cx?: number; children?: React.ReactNode}> = ({t, t0, t1, snap, keys, win, top, cx = 960, children}) => {
  const [, fx, fy, z] = camAt(t, keys);
  const crop: Rect = {x: fx - win[0] / (2 * z), y: fy - win[1] / (2 * z), w: win[0] / z, h: win[1] / z};
  return <Panel t={t} t0={t0} t1={t1} snap={snap} crop={crop} s={z} top={top} cx={cx} radius={26}>{children}</Panel>;
};
