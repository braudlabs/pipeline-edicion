import {useT} from '../lib/time';
import React from 'react';
import {Img, staticFile} from 'remotion';
import {useCam} from '../fx/plan';

const pad = (n: number) => String(n).padStart(4, '0');

/**
 * Capa detrás del sujeto: recorta su contenido con el matte inverso (holdout) del
 * fotograma presentado. `sceneFrom` convierte el fotograma maestro en índice fuente.
 * Los mattes salen de Vision (VNGeneratePersonSegmentationRequest .accurate) sobre el
 * mismo clip y transformación que el metraje; ver tools/matte.swift.
 */
export const Behind: React.FC<{dir: string; sceneFrom: number; srcIn?: number; count: number; first?: number; children: React.ReactNode}> = ({
  dir,
  sceneFrom,
  srcIn = 0,
  count,
  first = 0,
  children,
}) => {
  const frame = useT();
  const idx = Math.max(first, Math.min(first + count - 1, Math.floor(frame + 1e-6) - sceneFrom + srcIn)); // fotograma fuente mostrado
  const url = staticFile(`assets/mattes/${dir}/h${pad(idx)}.png`);
  const cam = useCam(); // C06: la máscara sigue a la cámara (escala uniforme + traslación)
  return (
    <>
      <Img src={url} style={{position: 'absolute', width: 1, height: 1, opacity: 0}} />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          WebkitMaskImage: `url("${url}")`,
          maskImage: `url("${url}")`,
          WebkitMaskSize: `${1080 * cam.s}px ${1920 * cam.s}px`,
          maskSize: `${1080 * cam.s}px ${1920 * cam.s}px`,
          WebkitMaskPosition: `${cam.tx}px ${cam.ty}px`,
          maskPosition: `${cam.tx}px ${cam.ty}px`,
          WebkitMaskRepeat: 'no-repeat',
          maskRepeat: 'no-repeat',
        }}
      >
        {children}
      </div>
    </>
  );
};
