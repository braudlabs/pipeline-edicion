import React from 'react';
import {Img, staticFile, useCurrentFrame} from 'remotion';

const pad = (n: number) => String(n).padStart(4, '0');

/**
 * Capa detrás del sujeto: recorta su contenido con el matte inverso (holdout) del
 * fotograma presentado. `sceneFrom` convierte el fotograma maestro en índice fuente.
 * Los mattes salen de Vision (VNGeneratePersonSegmentationRequest .accurate) sobre el
 * mismo clip y transformación que el metraje; ver tools/matte.swift.
 */
export const Behind: React.FC<{dir: string; sceneFrom: number; srcIn?: number; count: number; children: React.ReactNode}> = ({
  dir,
  sceneFrom,
  srcIn = 0,
  count,
  children,
}) => {
  const frame = useCurrentFrame();
  const idx = Math.max(0, Math.min(count - 1, frame - sceneFrom + srcIn));
  const url = staticFile(`assets/mattes/${dir}/h${pad(idx)}.png`);
  return (
    <>
      <Img src={url} style={{position: 'absolute', width: 1, height: 1, opacity: 0}} />
      <div
        style={{
          position: 'absolute',
          inset: 0,
          WebkitMaskImage: `url("${url}")`,
          maskImage: `url("${url}")`,
          WebkitMaskSize: '1080px 1920px',
          maskSize: '1080px 1920px',
          WebkitMaskRepeat: 'no-repeat',
          maskRepeat: 'no-repeat',
        }}
      >
        {children}
      </div>
    </>
  );
};
