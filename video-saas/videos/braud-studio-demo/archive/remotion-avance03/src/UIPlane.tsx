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
