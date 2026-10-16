import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Clip} from '../Clip';
import {Cursor, CursorKey} from '../Cursor';
import {Panel, panelPoint} from '../Panel';
import {Module, Rect} from '../UIPlane';
import {Headline, cardStyle} from '../system';
import {at, ease, mix, prog} from '../lib/motion';
import {QUALITY_END} from './Quality';
import {FINAL_AD, SHOTS} from '../data/andromeda';

// Bloques 11–13 · V05. Las versiones reales de la escena (con el motivo del descarte), el montaje
// provisional de Studio con los cinco clips aprobados, el anuncio terminado y el «sí» del usuario:
// «Aprobar y usar» → «Seleccionado» y el aviso real «Versión aprobada y seleccionada para la entrega.»

const T = {
  te: at(11, 'Te'), y: at(11, 'Y'), monta: at(11, 'lo', 1), voz: at(11, 'voz'), clips: at(11, 'clips'), ritmo: at(11, 'ritmo'),
  listo: at(11, 'Listo'), tu: at(12, 'Tú'), y12: at(12, 'Y'), si: at(12, 'sí'), pero: at(13, 'Pero'), acaba: at(13, 'acaba'),
};
export const EDIT_START = QUALITY_END;
export const EDIT_END = 83.95; // antes de «El agente está conectado» (bloque 14)

// ---------- bloque 11 ----------
const VERSIONS: Rect = {x: 205, y: 375, w: 400, h: 315}; // las cuatro versiones reales de «Cinco ads» y el selector // las dos versiones reales y el selector

// Montaje provisional de Andrómeda: el tramo de la máquina, con sus tiempos reales (s07–s10, 32,6–51,5 s
// de 85,4 s). En el reproductor, cada clip va encuadrado hacia la máquina; la pista de miniaturas queda fuera.
const CLIPS = [
  {shot: 'maquina', a: 32.585, b: 35.002}, {shot: 'textura', a: 35.002, b: 38.335},
  {shot: 'detalle', a: 38.335, b: 42.585}, {shot: 'suela', a: 42.585, b: 51.543},
];
const MONTAGE = 85.4;
const ASM: Rect = {x: 0, y: 0, w: 1070, h: 712}; // hasta la pista «Voz en off»; la de miniaturas (con la sudadera) queda fuera
const ASM_VIDEO: Rect = {x: 403, y: 106, w: 264, h: 470};
const SEEK = {x0: 255, x1: 1005, y: 613.5, h: 7};
const PLAY0 = T.monta - 0.05, PLAY1 = T.listo - 0.25;
const Assembly: React.FC<{t: number}> = ({t}) => {
  const p = prog(t, PLAY0, PLAY1, ease.linear);
  const mt = mix(CLIPS[0].a, CLIPS[CLIPS.length - 1].b, p);
  const i = Math.max(0, CLIPS.findIndex((c) => mt >= c.a && mt < c.b));
  const span = CLIPS[CLIPS.length - 1].b - CLIPS[0].a;
  const slot0 = PLAY0 + ((CLIPS[i].a - CLIPS[0].a) / span) * (PLAY1 - PLAY0); // cada clip arranca desde su inicio al entrar en su tramo
  const kx = SEEK.x0 + 7 + (mt / MONTAGE) * (SEEK.x1 - SEEK.x0 - 14);
  return (
    <Panel t={t} t0={T.y + 0.05} t1={T.listo - 0.32} snap="a6-montaje-assembly" crop={ASM} s={0.9} top={316}>
      {t >= PLAY0 ? (
        <div style={{position: 'absolute', left: ASM_VIDEO.x, top: ASM_VIDEO.y, width: ASM_VIDEO.w, height: ASM_VIDEO.h, overflow: 'hidden', borderRadius: 8, background: '#000'}}>
          <Clip key={CLIPS[i].shot} id={SHOTS[CLIPS[i].shot].id} t0={slot0} crop={SHOTS[CLIPS[i].shot].crop} />
        </div>
      ) : null}
      {/* barra de reproducción: se tapa el tirador de la captura y avanza con el montaje */}
      <div style={{position: 'absolute', left: SEEK.x0, top: SEEK.y, width: SEEK.x1 - SEEK.x0, height: SEEK.h, borderRadius: 4, background: '#EFEFEF'}} />
      <div style={{position: 'absolute', left: SEEK.x0, top: SEEK.y, width: kx - SEEK.x0, height: SEEK.h, borderRadius: 4, background: '#367DFF'}} />
      <div style={{position: 'absolute', left: kx - 8, top: SEEK.y + SEEK.h / 2 - 8, width: 16, height: 16, borderRadius: 8, background: '#367DFF'}} />
    </Panel>
  );
};

/** El anuncio terminado, en grande (eco del «listo para publicar» del bloque 2). */
const Final: React.FC<{t: number}> = ({t}) => {
  const t0 = T.listo - 0.05, out = T.tu - 0.3;
  if (t < t0 || t > out + 0.35) return null;
  const k = prog(t, t0, t0 + 0.55, ease.out), o = prog(t, out, out + 0.32, ease.in);
  const w = 360, h = 640;
  return (
    <div style={{...cardStyle(w, h), position: 'absolute', left: 960 - w / 2, top: 296 + (1 - k) * 80 - o * 60, opacity: k * (1 - o)}}>
      <Clip id={FINAL_AD.id} t0={t0} offset={FINAL_AD.offset} rate={FINAL_AD.rate} crop={FINAL_AD.crop} />
    </div>
  );
};

// ---------- bloque 12 · «y has dicho que sí» ----------
const ROW: Rect = {x: 190, y: 606, w: 530, h: 160};
const RS = 1.9, RTOP = 470;
const CLICK = T.si - 0.16;
const APPROVE_CURSOR: CursorKey[] = [
  {t: T.y12 - 0.45, x: 1520, y: 1160},
  {t: CLICK - 0.06, ...panelPoint(ROW, RS, RTOP, 626, 737)}, {t: CLICK, ...panelPoint(ROW, RS, RTOP, 626, 737), click: true},
];
const Approve: React.FC<{t: number}> = ({t}) => (
  <Panel t={t} t0={T.tu + 0.08} t1={T.pero - 0.38} snap={t < CLICK + 0.04 ? 'a6-aprobar-workspace' : 'a6-aprobado-workspace'} crop={ROW} s={RS} top={RTOP} />
);
const Toast: React.FC<{t: number}> = ({t}) => {
  const t0 = CLICK + 0.12, out = T.pero - 0.38;
  if (t < t0 || t > out + 0.32) return null;
  const k = prog(t, t0, t0 + 0.4, ease.out), o = prog(t, out, out + 0.3, ease.in);
  const s = 1.55;
  return <Module snap="v5-aprobado" crop={{x: 594, y: 829, w: 324, h: 46}} cx={960} cy={890} s={s} dy={(1 - k) * 24 - o * 40} opacity={k * (1 - o)} radius={23 * s} edge={false} />;
};

export const Edit: React.FC<{t: number}> = ({t}) => {
  if (t < EDIT_START - 0.05 || t > EDIT_END) return null;
  return (
    <AbsoluteFill>
      <Panel t={t} t0={T.te + 0.04} t1={T.y - 0.3} snap="a6-escenas-versiones-workspace" crop={VERSIONS} s={1.85} top={300} />
      <Headline t={t} out={T.y - 0.42} y={176} size={80} lines={[{text: 'Cada versión.', t: T.te}]} />

      <Assembly t={t} />
      <Headline t={t} out={T.listo - 0.42} y={190} size={80} lines={[{text: 'Con lo que apruebas,', t: T.y}, {text: 'lo monta.', t: T.monta}]} />

      <Final t={t} />
      <Headline t={t} out={T.tu - 0.42} y={176} size={80} lines={[{text: 'Listo para publicar.', t: T.listo - 0.04}]} />

      <Approve t={t} />
      <Toast t={t} />
      <Cursor t={t} keys={APPROVE_CURSOR} size={30 * RS * 0.75} hideAfter={T.pero - 0.4} />
      <Headline t={t} out={T.pero - 0.42} y={270} size={88} lines={[{text: 'Tú pones la idea.', t: T.tu}, {text: 'Y dices que sí.', t: T.y12}]} />

      <Headline t={t} out={EDIT_END + 1} y={540} size={120} lines={[{text: 'Pero aquí no se acaba.', t: T.pero - 0.02}]} />
    </AbsoluteFill>
  );
};
