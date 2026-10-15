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
import {FontsGate} from './lib/Fonts';
import {VideoSpine} from './VideoSpine';

// C04 · Ecommerce Andrómeda (Claude). Montaje bloqueado del MASTER_COMPLETO_24FPS (17 unidades,
// 2050 f); subtítulos por función en las 17 unidades. Hook, cartel de la persiana y «OTRA PUTA
// VEZ» aprobados por Ale; el resto en líneas grandes centradas en la zona libre de cada plano
// (feedback sobre C01). 06 rehecho para la toma v5; 07–15 nuevos (ver CAMBIOS.md).
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
    <AudioTracks />
  </AbsoluteFill>
);
