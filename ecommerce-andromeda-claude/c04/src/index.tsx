import React from 'react';
import {AbsoluteFill, Composition, registerRoot} from 'remotion';
import {AudioTracks} from './AudioTracks';
import {HookVariant} from './captions/Hook';
import {Film} from './Film';
import {Fonts} from './lib/Fonts';
import {TimeScale} from './lib/time';
import {VideoSpine} from './VideoSpine';
import timeline from './data/timeline.json';

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

// Salida a 60 fps (alternativa más rápida): escala 2,5. El metraje de 24 fps queda en cadencia
// 3:2 sin interpolar. Los cortes en fotograma de 24 fps impar (09, 12, 13, 15) caen en medio
// fotograma de 60 fps y VideoSpine/AudioTracks los redondean (±8,3 ms), sin huecos.
const Film60: React.FC = () => (
  <TimeScale.Provider value={2.5}>
    <Film />
  </TimeScale.Provider>
);

// C04 · 17 unidades, 2050 f a 24 fps = 85,416667 s (la locución dura 85,39425 s). Duración
// leída de timeline.json para que montaje y composiciones no puedan desincronizarse.
const FRAMES = timeline.renderedFrames;

registerRoot(() => (
  <>
    <Composition id="AndromedaC04" component={Film} durationInFrames={FRAMES} fps={24} width={1080} height={1920} />
    <Composition id="AndromedaC04-144" component={Film144} durationInFrames={FRAMES * 6} fps={144} width={1080} height={1920} />
    <Composition id="AndromedaC04-60" component={Film60} durationInFrames={Math.round(FRAMES * 2.5)} fps={60} width={1080} height={1920} />
    <Composition id="HookStudy" component={HookStudy} defaultProps={{variant: 'A'}} durationInFrames={130} fps={24} width={1080} height={1920} />
  </>
));
