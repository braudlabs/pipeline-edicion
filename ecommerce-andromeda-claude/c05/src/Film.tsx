import React from 'react';
import {AbsoluteFill} from 'remotion';
import {AudioTracks} from './AudioTracks';
import {HookA} from './captions/Hook';
import {Scene01} from './captions/Scene01';
import {Scene02} from './captions/Scene02';
import {Scene03, Scene03b} from './captions/Scene03';
import {Scene04} from './captions/Scene04';
import {Scene05} from './captions/Scene05';
import {Scene06} from './captions/Scene06';
import {Scene07} from './captions/Scene07';
import {Scene08} from './captions/Scene08';
import {Scene09} from './captions/Scene09';
import {Scene10} from './captions/Scene10';
import {Scene11} from './captions/Scene11';
import {Scene12} from './captions/Scene12';
import {Scene13} from './captions/Scene13';
import {Scene14, Scene15} from './captions/Scene14';
import {Moments} from './fx/Moments';
import {FontsGate} from './lib/Fonts';
import {VideoSpine} from './VideoSpine';

// C05 · Ecommerce Andrómeda (Claude). Montaje del MASTER_COMPLETO_24FPS (17 unidades, 2050 f).
// Feedback de Ale sobre C04: paleta solo blanco + azul claro, margen seguro de Meta en todos los
// rótulos, tarjeta «nuevo ángulo» integrada, sin eco en «mierda», momentos de luz (fx/Moments)
// y música nueva continua (toma 3). Ver CAMBIOS.md.
export const Film: React.FC<{audit?: boolean}> = ({audit}) => (
  <AbsoluteFill style={{background: audit ? '#000' : '#14262e'}}>
    {/* audit: solo rótulos sobre negro, para medir sus márgenes reales (study/audit-margins.json) */}
    {audit ? null : <VideoSpine />}
    {audit ? null : <Moments />}
    <FontsGate>
      <HookA />
      <Scene01 />
      <Scene02 />
      <Scene03 />
      <Scene03b />
      <Scene04 />
      <Scene05 />
      <Scene06 />
      <Scene07 />
      <Scene08 />
      <Scene09 />
      <Scene10 />
      <Scene11 />
      <Scene12 />
      <Scene13 />
      <Scene14 />
      <Scene15 />
    </FontsGate>
    {audit ? null : <AudioTracks />}
  </AbsoluteFill>
);
