import React from 'react';
import {AbsoluteFill, Composition, registerRoot} from 'remotion';
import {AudioTracks} from './AudioTracks';
import {HookVariant} from './captions/Hook';
import {Film} from './Film';
import {Fonts} from './lib/Fonts';
import {TimeScale} from './lib/time';
import {VideoSpine} from './VideoSpine';

// Estudio de alternativas del bloque protagonista (hook). Solo fotogramas de diseño.
const HookStudy: React.FC<{variant: string}> = ({variant}) => (
  <AbsoluteFill style={{background: '#14262e'}}>
    <Fonts />
    <VideoSpine />
    <HookVariant variant={variant} />
    <AudioTracks only={['narrador', 'hook-nativo']} />
  </AbsoluteFill>
);

// Salida a 144 fps (petición de Ale): 144/24 = 6 exacto. El metraje repite cada fotograma
// fuente ×6 sin interpolar; rótulos, obturador y caídas se evalúan a 144 fps.
const Film144: React.FC = () => (
  <TimeScale.Provider value={6}>
    <Film />
  </TimeScale.Provider>
);

// Salida a 60 fps (alternativa más rápida): escala 2,5. Todos los cortes caen en fotograma
// entero (×2,5); el metraje de 24 fps queda en cadencia 3:2 sin interpolar.
const Film60: React.FC = () => (
  <TimeScale.Provider value={2.5}>
    <Film />
  </TimeScale.Provider>
);

registerRoot(() => (
  <>
    <Composition id="AndromedaC03" component={Film} durationInFrames={920} fps={24} width={1080} height={1920} />
    <Composition id="AndromedaC03-144" component={Film144} durationInFrames={920 * 6} fps={144} width={1080} height={1920} />
    <Composition id="AndromedaC03-60" component={Film60} durationInFrames={2300} fps={60} width={1080} height={1920} />
    <Composition id="HookStudy" component={HookStudy} defaultProps={{variant: 'A'}} durationInFrames={130} fps={24} width={1080} height={1920} />
  </>
));
