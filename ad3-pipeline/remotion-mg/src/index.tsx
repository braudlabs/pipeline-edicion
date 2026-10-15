import React from 'react';
import {Composition, continueRender, delayRender, registerRoot, staticFile} from 'remotion';

import {Bloques, DURACION_BLOQUES, FPS, GraphicsOnly, MASTER, Scene, comps} from './ae';

/* SF Pro Display Bold es la tipografía del proyecto; se carga desde public/. */
const handle = delayRender('Cargando SF Pro Display');
const style = document.createElement('style');
style.textContent = `
@font-face{font-family:"SF Pro Display";font-weight:700;font-style:normal;src:url("${staticFile(
  'fonts/SFProDisplay-Bold.otf',
)}") format("opentype");}
@font-face{font-family:"SF Pro Display";font-weight:400;font-style:normal;src:url("${staticFile(
  'fonts/SFProDisplay-Regular.otf',
)}") format("opentype");}
`;
document.head.appendChild(style);
Promise.all([
  document.fonts.load('700 100px "SF Pro Display"'),
  document.fonts.load('400 100px "SF Pro Display"'),
])
  .then(() => document.fonts.ready)
  .then(() => continueRender(handle))
  .catch(() => continueRender(handle));

/** Cada comp de gráficos, para revisarla aislada como en AE. */
const SCENES = [
  '00 - Verde BRAUD',
  '01 - Se monta solo',
  '01A - Pistas editables',
  '01B - Caja continua',
  '02 - Una creatividad',
  '03 - Todo encaje',
  '04 - Sistemas Visual Hub',
  '04A - Sistema y salidas',
  '05 - Produccion y oferta',
];

const id = (name: string) => name.replace(/[^A-Za-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

const Root: React.FC = () => {
  const master = comps[MASTER];
  return (
    <>
      {/* Recreación completa: metraje, gráficos nativos, subtítulos y mezcla. */}
      <Composition
        id="AD3-V8"
        component={Scene}
        defaultProps={{name: MASTER, withAudio: true}}
        width={master.width}
        height={master.height}
        fps={FPS}
        durationInFrames={master.duration}
      />
      {/* Los cinco bloques gráficos seguidos, para verlos sin el resto del anuncio. */}
      <Composition
        id="Motion-Graphics"
        component={Bloques}
        width={master.width}
        height={master.height}
        fps={FPS}
        durationInFrames={DURACION_BLOQUES}
      />
      {/* Solo los gráficos, sobre fondo transparente, para componer sobre el montaje. */}
      <Composition
        id="AD3-V8-Graficos"
        component={GraphicsOnly}
        width={master.width}
        height={master.height}
        fps={FPS}
        durationInFrames={master.duration}
      />
      {SCENES.map((name) => {
        const c = comps[name];
        return (
          <Composition
            key={name}
            id={id(name)}
            component={Scene}
            defaultProps={{name}}
            width={c.width}
            height={c.height}
            fps={FPS}
            durationInFrames={c.duration}
          />
        );
      })}
    </>
  );
};

registerRoot(Root);

