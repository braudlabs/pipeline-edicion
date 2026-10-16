import React from 'react';
import {Img, staticFile} from 'remotion';
import {Cam, camCss, H, W} from './lib/motion';

// Las vistas de Studio son capturas del frontal real (tools/snap.mjs, DPR 3) a 1512×900 px CSS.
export const UI_W = 1512;
export const UI_H = 900;

export type Rect = {x: number; y: number; w: number; h: number};
export const snapUrl = (name: string) => staticFile(`snaps/${name}.png`);

/**
 * Plano de interfaz en 3D. `children` se dibuja en coordenadas de la interfaz (px CSS de la
 * captura), así cursor, tecleo y vídeos siguen a la cámara.
 */
export const UIPlane: React.FC<{
  snap: string;
  cam: Cam;
  opacity?: number;
  radius?: number;
  children?: React.ReactNode;
  under?: string; // otra captura debajo (fundidos entre estados)
  underOpacity?: number;
  blur?: number;
}> = ({snap, cam, opacity = 1, radius = 26, children, under, underOpacity = 1, blur = 0}) => (
  <div style={{position: 'absolute', inset: 0, perspective: 2600, perspectiveOrigin: '50% 45%'}}>
    <div style={{
      position: 'absolute', left: (W - UI_W) / 2, top: (H - UI_H) / 2, width: UI_W, height: UI_H,
      transform: camCss(cam), transformOrigin: '50% 50%', opacity, filter: blur > 0.05 ? `blur(${blur}px)` : undefined,
      borderRadius: radius, overflow: 'hidden', background: '#f2f5f8',
      boxShadow: '0 80px 160px rgba(0,0,0,.7), 0 20px 50px rgba(0,0,0,.4)', outline: '1px solid rgba(255,255,255,.18)',
    }}>
      {under ? <Img src={snapUrl(under)} style={{position: 'absolute', inset: 0, width: UI_W, height: UI_H, opacity: underOpacity}} /> : null}
      <Img src={snapUrl(snap)} style={{position: 'absolute', inset: 0, width: UI_W, height: UI_H}} />
      {children}
    </div>
  </div>
);

/** Recorte de una captura (p. ej. una región que se revela con una cortinilla). */
export const SnapRegion: React.FC<{snap: string; r: Rect; style?: React.CSSProperties; fullH?: number}> = ({snap, r, style, fullH = UI_H}) => (
  <div style={{position: 'absolute', left: r.x, top: r.y, width: r.w, height: r.h, overflow: 'hidden', ...style}}>
    <Img src={snapUrl(snap)} style={{position: 'absolute', left: -r.x, top: -r.y, width: UI_W, height: fullH}} />
  </div>
);

/**
 * Módulo (V04): un recorte real de una captura presentado como panel, como en El Sistema FINAL.
 * `children` se dibuja en coordenadas de la interfaz; `under` permite fundir desde otra captura.
 */
export const Module: React.FC<{snap: string; crop: Rect; cx: number; cy: number; s: number; opacity?: number; dy?: number;
  under?: string; underOpacity?: number; radius?: number; edge?: boolean; transform?: string; children?: React.ReactNode}> = (
  {snap, crop, cx, cy, s, opacity = 1, dy = 0, under, underOpacity = 0, radius = 22, edge = true, transform, children}) => (
  <div style={{position: 'absolute', left: cx - (crop.w * s) / 2, top: cy - (crop.h * s) / 2 + dy, width: crop.w * s, height: crop.h * s, overflow: 'hidden',
    borderRadius: radius, opacity, background: '#111214', boxShadow: '0 40px 120px rgba(0,0,0,0.7)', transform}}>
    <div style={{position: 'absolute', left: -crop.x * s, top: -crop.y * s, width: UI_W, height: UI_H, transform: `scale(${s})`, transformOrigin: '0 0'}}>
      <Img src={snapUrl(snap)} style={{position: 'absolute', inset: 0, width: UI_W, height: UI_H}} />
      {under && underOpacity > 0 ? <Img src={snapUrl(under)} style={{position: 'absolute', inset: 0, width: UI_W, height: UI_H, opacity: underOpacity}} /> : null}
      {children}
    </div>
    {/* borde de 1 px con luz desde arriba, como las tarjetas de vidrio de la landing */}
    {edge ? <div style={{position: 'absolute', inset: 0, borderRadius: radius, padding: 1, pointerEvents: 'none',
      background: 'linear-gradient(180deg, rgba(255,255,255,0.24), rgba(255,255,255,0.07) 45%, rgba(255,255,255,0.05))',
      WebkitMask: 'linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0)', WebkitMaskComposite: 'xor', maskComposite: 'exclude'}} /> : null}
  </div>
);
/** Punto de la interfaz dentro de un módulo → coordenadas del cuadro. */
export const moduleToStage = (crop: Rect, cx: number, cy: number, s: number, x: number, y: number, dy = 0) => ({
  x: cx - (crop.w * s) / 2 + (x - crop.x) * s, y: cy - (crop.h * s) / 2 + dy + (y - crop.y) * s,
});
