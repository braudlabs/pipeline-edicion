import React from 'react';
import {AbsoluteFill} from 'remotion';
import {AudioTracks} from './AudioTracks';
import {HookA} from './captions/Hook';
import {Scene01} from './captions/Scene01';
import {Scene02} from './captions/Scene02';
import {Scene03, Scene03b} from './captions/Scene03';
import {Scene04} from './captions/Scene04';
import {Scene05, Scene06} from './captions/Scene05';
import {FontsGate} from './lib/Fonts';
import {VideoSpine} from './VideoSpine';

// C02 · Ecommerce Andrómeda (Claude). Montaje bloqueado del CSV; subtítulos por función.
// Hook, cartel de la persiana y «OTRA PUTA VEZ» aprobados por Ale; el resto en líneas
// grandes centradas (feedback sobre C01: fuente pequeña, pegada a los lados, poco estética).
export const Film: React.FC = () => (
  <AbsoluteFill style={{background: '#14262e'}}>
    <VideoSpine />
    <FontsGate>
      <HookA />
      <Scene01 />
      <Scene02 />
      <Scene03 />
      <Scene03b />
      <Scene04 />
      <Scene05 />
      <Scene06 />
    </FontsGate>
    <AudioTracks />
  </AbsoluteFill>
);
