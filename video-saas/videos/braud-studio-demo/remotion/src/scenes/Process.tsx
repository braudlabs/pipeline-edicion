import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Clip} from '../Clip';
import {Cursor, CursorKey} from '../Cursor';
import {CamKey, Panel, UICam, Wipe, panelPoint} from '../Panel';
import {Module, Rect} from '../UIPlane';
import {SHOTS} from '../data/andromeda';
import {Headline, cardStyle} from '../system';
import {at, ease, mix, prog} from '../lib/motion';
import {IDEA_END} from './Idea';

// Bloques 6–9 · V06 (tras «no me gustan los ads de ejemplo… esos bloques son super cutres, pilla el ad
// de la maquinita»). La pieza es el anuncio de la maquinita (Andrómeda pide más). La interfaz ya no
// entra como un formulario entero y apagado: una cámara se desliza sobre la interfaz real, grande y
// legible, de campo en campo al ritmo de la voz. Donde hay imagen (clips, la máquina), manda la imagen.

const T = {
  aterriza: at(6, 'Aterriza'), objetivo: at(6, 'objetivo'), publico: at(6, 'público'), frena: at(6, 'qué', 0), demuestra: at(6, 'qué', 1),
  propone: at(6, 'Y', 1), desde: at(6, 'desde'), donde: at(6, 'dónde'), contarla: at(6, 'contarla'), // la «y» 0 es «frena y qué»
  escribe: at(7, 'Escribe'), frase: at(7, 'frase'), hook: at(7, 'Y'), tres: at(7, 'te'), empezar: at(7, 'empezar'),
  reparto: at(8, 'Propone'), mantiene: at(8, 'mantiene'), personaje: at(8, 'personaje'), producto: at(8, 'producto'), cada: at(8, 'cada'),
  convierte: at(9, 'Convierte'), frase9: at(9, 'frase'), escena9: at(9, 'escena'), prompt: at(9, 'Escribe'), cuesta: at(9, 'te'), genera: at(9, 'y'),
};
export const PROCESS_START = IDEA_END;
export const PROCESS_END = at(10, 'Y'); // «Y no es solo velocidad»

const WIN: [number, number] = [1300, 560]; // ventana de la cámara en pantalla
const TOP = 300;

// ---------- bloque 6 · la intención, campo a campo ----------
const B6_OUT = T.propone - 0.2;
const INTENT_KEYS: CamKey[] = [
  [T.aterriza + 0.15, 535, 410, 1.22],
  [T.objetivo - 0.1, 535, 410, 1.22],
  [T.objetivo + 0.32, 790, 262, 2.05], // 02 · Objetivo: que reserven una llamada
  [T.publico - 0.05, 790, 262, 2.05],
  [T.publico + 0.33, 290, 262, 2.05], // 01 · A quién hablamos
  [T.frena - 0.05, 290, 262, 2.05],
  [T.frena + 0.33, 290, 505, 2.05], // 03 · La tensión
  [T.demuestra - 0.05, 290, 505, 2.05],
  [T.demuestra + 0.33, 790, 560, 2.05], // 04 · Qué lo sostiene: este mismo anuncio
  [B6_OUT - 0.25, 790, 560, 2.08],
];
const ANGLE_KEYS: CamKey[] = [
  [T.propone + 0.14, 198, 300, 1.75], // 01 · El ritmo de Meta
  [T.donde - 0.08, 198, 300, 1.75],
  [T.donde + 0.25, 535, 300, 1.75], // 02 · Depender de otros
  [T.contarla - 0.02, 535, 300, 1.75],
  [T.contarla + 0.3, 871, 300, 1.75], // 03 · Lo hizo la máquina
  [T.escribe - 0.75, 871, 300, 1.75],
  [T.escribe - 0.35, 535, 290, 1.21],
];

// ---------- bloque 7 · el guion, frase a frase; el hook y sus tres aperturas ----------
const SCRIPT_OUT = T.hook - 0.2;
const LINE_Y = [205, 472, 739, 1006, 1273]; // las cinco primeras frases del guion real
const SCRIPT_KEYS: CamKey[] = [
  [T.escribe + 0.04, 520, LINE_Y[0] + 40, 1.35],
  ...LINE_Y.slice(1).map((y, i) => [T.escribe + 0.42 + i * 0.38, 520, y + 40, 1.35] as CamKey),
  [SCRIPT_OUT, 520, LINE_Y[4] + 40, 1.37],
];
const OPEN_KEYS: CamKey[] = [
  [T.hook + 0.12, 199, 283, 1.95], // 01 · El problema (la apertura que está en el guion)
  [T.tres - 0.05, 199, 283, 1.95],
  [T.tres + 0.75, 535, 244, 1.2], // las tres
  [T.reparto - 0.25, 535, 244, 1.21],
];

// ---------- bloque 8 · el reparto ----------
const ROLE_KEYS: CamKey[] = [
  [T.reparto + 0.1, 330, 175, 1.85], // las pestañas de papeles: El azul · El protagonista
  [T.reparto + 0.45, 330, 175, 1.85],
  [T.reparto + 0.85, 300, 300, 1.75], // El azul: la demanda insaciable de Meta
  [T.mantiene - 0.62, 800, 300, 1.75], // carácter y apariencia
  [T.mantiene - 0.4, 800, 300, 1.75],
];
const ROLE: Rect = {x: 42, y: 338, w: 1070, h: 422}; // tarjeta del papel en la captura de Casting
const CONT = ['lavadora', 'detalle', 'maquina', 'estanteria', 'suela'];
const REF_MAQUINITA: Rect = {x: 752, y: 540, w: 304, h: 60}; // «La maquinita · Producto» (Dirección de la escena)
const Continuity: React.FC<{t: number}> = ({t}) => {
  const t0 = T.mantiene - 0.05, out = T.convierte - 0.32;
  if (t < t0 || t > out + 0.32) return null;
  const o = prog(t, out, out + 0.3, ease.in);
  const cw = 196, ch = Math.round((cw * 16) / 9), gap = 22, x0 = 960 - (5 * cw + 4 * gap) / 2;
  const rk = prog(t, T.producto - 0.12, T.producto + 0.38, ease.out);
  return (
    <>
      <Module snap="a6-escenas-workspace" crop={REF_MAQUINITA} cx={960} cy={372 + (1 - rk) * 30 - o * 60} s={1.5} radius={16} opacity={rk * (1 - o)} />
      {CONT.map((k, i) => {
        const a = t0 + 0.05 + i * 0.07;
        const kk = prog(t, a, a + 0.55, ease.out);
        const hl = prog(t, T.cada - 0.05 + i * 0.08, T.cada + 0.25 + i * 0.08, ease.out); // «en cada escena»: se encienden en ola
        return (
          <div key={k} style={{...cardStyle(cw, ch), position: 'absolute', left: x0 + i * (cw + gap), top: 470 + (1 - kk) * 80 - o * 70,
            opacity: kk * (1 - o) * mix(0.6, 1, hl), transform: `scale(${mix(0.97, 1, hl)})`}}>
            <Clip id={SHOTS[k].id} t0={a} crop={SHOTS[k].crop} offset={SHOTS[k].offset ?? 0} />
          </div>
        );
      })}
    </>
  );
};

// ---------- bloque 9 · la escena, su prompt y su coste ----------
// Escena 08 «Cinco ads»: reproductor y Dirección (la columna de escenas y el póster llevan la sudadera:
// fuera del recorte; en el reproductor va el clip real encuadrado hacia la máquina).
const WS: Rect = {x: 196, y: 0, w: 874, h: 560};
const PLAYER: Rect = {x: 199, y: 52, w: 512, h: 496};
const B9_SCENE_OUT = T.prompt - 0.3;
const SceneEditor: React.FC<{t: number}> = ({t}) => (
  <Panel t={t} t0={T.convierte + 0.05} t1={B9_SCENE_OUT} snap="a6-escenas-workspace" crop={WS} s={1.12} top={TOP}>
    <div style={{position: 'absolute', left: PLAYER.x + 101, top: PLAYER.y, width: 310, height: PLAYER.h, overflow: 'hidden', background: '#000'}}>
      <Clip id={SHOTS.textura.id} t0={T.convierte + 0.05} crop={SHOTS.textura.crop} /> {/* v5 · Cinco vídeos, la versión aprobada */}
    </div>
  </Panel>
);

// El modal real «Preparar una generación» y su cotización (16 créditos por segundo: tarifa real de Seedance 2.5).
const MODAL_G: Rect = {x: 416, y: 148, w: 680, h: 604};
const MODAL_C_TOP = 45;
const PROMPT_LINES = [369, 387, 405, 441, 459, 477, 513, 531].map((y) => ({x: 458, y: y - 9, w: 600, h: 18}));
const MS = 1.06, MTOP = 268;
const QUOTE_AT = T.cuesta - 0.02;
const scrollC = (t: number) => prog(t, QUOTE_AT + 0.08, QUOTE_AT + 0.6, ease.inOut) * 214;
const modalCrop = (t: number): Rect => (t < QUOTE_AT ? MODAL_G : {x: 416, y: MODAL_C_TOP + scrollC(t), w: 680, h: 604});
const Generate: React.FC<{t: number}> = ({t}) => {
  const quoted = t >= QUOTE_AT;
  return (
    <Panel t={t} t0={T.prompt + 0.05} t1={PROCESS_END - 0.3} snap={quoted ? 'a6-coste' : 'a6-generar'} crop={modalCrop(t)} s={MS} top={MTOP} edge={false} radius={28 * MS}>
      {!quoted ? PROMPT_LINES.map((r, i) => (
        <Wipe key={i} r={r} k={prog(t, T.prompt + 0.05 + i * 0.1, T.prompt + 0.2 + i * 0.1, ease.linear)} color="#181a1e" />
      )) : null}
    </Panel>
  );
};
const modalPoint = (t: number, x: number, y: number) => panelPoint(modalCrop(t), MS, MTOP, x, y);
const GEN_CURSOR = (): CursorKey[] => [
  {t: QUOTE_AT - 0.75, x: 1500, y: 1150},
  {t: QUOTE_AT - 0.1, ...modalPoint(QUOTE_AT - 0.2, 760, 704)}, {t: QUOTE_AT - 0.04, ...modalPoint(QUOTE_AT - 0.2, 760, 704), click: true},
  {t: T.genera - 0.35, ...modalPoint(T.genera, 760, 827)}, {t: T.genera, ...modalPoint(T.genera, 760, 827), click: true},
];

export const Process: React.FC<{t: number}> = ({t}) => {
  if (t < PROCESS_START - 0.05 || t > PROCESS_END + 0.6) return null;
  return (
    <AbsoluteFill>
      <UICam t={t} t0={T.aterriza + 0.15} t1={B6_OUT} snap="a6-idea-intent" keys={INTENT_KEYS} win={WIN} top={TOP} />
      <UICam t={t} t0={T.propone + 0.14} t1={T.escribe - 0.28} snap="a6-idea-angles" keys={ANGLE_KEYS} win={WIN} top={TOP} />
      <Headline t={t} out={B6_OUT - 0.1} y={176} size={80} lines={[{text: 'Aterriza la idea.', t: T.aterriza + 0.04}]} />
      <Headline t={t} out={T.escribe - 0.42} y={176} size={80} lines={[{text: 'Desde dónde contarla.', t: T.propone + 0.16}]} />

      <UICam t={t} t0={T.escribe + 0.04} t1={SCRIPT_OUT} snap="a6-guion-script" keys={SCRIPT_KEYS} win={WIN} top={TOP + 18} />
      <UICam t={t} t0={T.hook + 0.12} t1={T.reparto - 0.25} snap="a6-guion-openings" keys={OPEN_KEYS} win={[1300, 590]} top={TOP + 10} />
      <Headline t={t} out={T.hook - 0.42} y={190} size={80} lines={[{text: 'Escribe el guion.', t: T.escribe}, {text: 'Frase a frase.', t: T.frase - 0.05}]} />
      <Headline t={t} out={T.reparto - 0.4} y={176} size={80} lines={[{text: 'El hook lo decide casi todo.', t: T.hook + 0.02}]} />

      <UICam t={t} t0={T.reparto + 0.1} t1={T.mantiene - 0.4} snap="a6-casting" keys={ROLE_KEYS.map(([tt, x, y, z]) => [tt, x + ROLE.x, y + ROLE.y, z] as CamKey)} win={WIN} top={TOP} />
      <Continuity t={t} />
      <Headline t={t} out={T.mantiene - 0.15} y={176} size={80} lines={[{text: 'Propone el reparto.', t: T.reparto}]} />
      <Headline t={t} out={T.convierte - 0.45} y={190} size={80} lines={[{text: 'Tu personaje y tu producto,', t: T.personaje - 0.1}, {text: 'en cada escena.', t: T.cada - 0.08}]} />

      <SceneEditor t={t} />
      <Generate t={t} />
      <Cursor t={t} keys={GEN_CURSOR()} size={30 * MS * 0.95} hideAfter={T.genera + 0.25} />
      <Headline t={t} out={B9_SCENE_OUT - 0.05} y={176} size={80} lines={[{text: 'Cada frase, una escena.', t: T.convierte}]} />
      <Headline t={t} out={PROCESS_END - 0.35} y={150} size={72} lines={[{text: 'Cada prompt, con su coste.', t: T.prompt}]} />
    </AbsoluteFill>
  );
};
