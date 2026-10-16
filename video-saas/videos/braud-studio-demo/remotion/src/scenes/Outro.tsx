import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Clip} from '../Clip';
import {CamKey, Panel, UICam} from '../Panel';
import {Rect} from '../UIPlane';
import {COLORS} from '../Stage';
import {SHOTS} from '../data/andromeda';
import {Headline, cardStyle} from '../system';
import {SF} from '../lib/Fonts';
import {at, clamp, ease, prog} from '../lib/motion';
import {META_END} from './Meta';

// Bloques 18–21 · V06. Lo que se queda (el papel, los clips aprobados, el aprendizaje real de Mi marca),
// Founders Picks con tres trabajos reales de BRAUD y su dato (selección de demo, anotada), y el cierre
// tipográfico que vuelve al logotipo del bloque 2.

const T = {
  todo: at(18, 'Todo'), personajes: at(18, 'personajes'), clips: at(18, 'clips'), aprendido: at(18, 'aprendido'),
  founders: at(18, 'Founders'), listas: at(18, 'listas'),
  tu19: at(19, 'Tú'), sistema: at(19, 'El'),
  no: at(20, 'No'), instalamos: at(20, 'Lo'), formamos: at(20, 'formamos'), queda: at(20, 'y'), tienda: at(20, 'tienda'),
  braud: at(21, 'BRAUD'),
};
export const OUTRO_START = META_END;
export const FILM_END = 124.0;

// ---------- bloque 18 · lo que se queda ----------
const ROLE: Rect = {x: 42 + 30, y: 338 + 230, w: 1000, h: 170}; // «El azul · La demanda insaciable de Meta»
const Kept: React.FC<{t: number}> = ({t}) => {
  // un foco por palabra: el papel («tus personajes»), los clips («tus clips»), el aprendizaje
  const cw = 230, ch = Math.round((cw * 16) / 9);
  const c0 = T.clips - 0.1, c1 = T.aprendido - 0.14;
  const k2 = prog(t, c0, c0 + 0.45, ease.out), o2 = prog(t, c1, c1 + 0.3, ease.in);
  return (
    <>
      <Panel t={t} t0={T.personajes - 0.15} t1={T.clips - 0.14} snap="a6-casting" crop={ROLE} s={1.25} top={420} />
      {t >= c0 && t <= c1 + 0.32 ? ['textura', 'campanas', 'sesion'].map((k, i) => (
        <div key={k} style={{...cardStyle(cw, ch), position: 'absolute', left: 960 - (3 * cw + 2 * 26) / 2 + i * (cw + 26), top: 330 + (1 - k2) * 70 - o2 * 60,
          opacity: clamp(k2 * 1.4 - i * 0.2) * (1 - o2)}}>
          <Clip id={SHOTS[k].id} t0={c0} crop={SHOTS[k].crop} offset={SHOTS[k].offset ?? 0} />
        </div>
      )) : null}
    </>
  );
};
const Learned: React.FC<{t: number}> = ({t}) => (
  <Panel t={t} t0={T.aprendido - 0.04} t1={T.founders - 0.3} snap="a6-marca-tarjetas-learning" s={1.25} top={390} edge={false} radius={18 * 1.25} />
);
const PICK_KEYS: CamKey[] = [
  [T.founders - 0.05, 628, 301, 1.0], // la selección entera
  [T.tu19 - 0.4, 628, 301, 1.08], // empuje lento
];

// ---------- bloque 21 · el logotipo ----------
const Wordmark: React.FC<{t: number}> = ({t}) => {
  const t0 = T.braud - 0.02;
  if (t < t0) return null;
  const k = ease.out(clamp((t - t0) / 0.8));
  const o = prog(t, FILM_END - 0.6, FILM_END, ease.in);
  return (
    <div style={{position: 'absolute', top: 540, left: 0, right: 0, transform: 'translateY(-50%)', textAlign: 'center', fontFamily: SF, whiteSpace: 'nowrap', opacity: 1 - o}}>
      <div style={{display: 'inline-block', overflow: 'hidden', paddingBottom: 12}}>
        <div style={{transform: `translateY(${(1 - k) * 110}%)`}}>
          <span style={{fontSize: 150, fontWeight: 300, letterSpacing: '-0.04em', color: COLORS.ink}}>braud</span>
          <span style={{fontSize: 150, fontWeight: 300, letterSpacing: '-0.03em', color: COLORS.dim, marginLeft: 40}}>studio</span>
        </div>
      </div>
    </div>
  );
};

export const Outro: React.FC<{t: number}> = ({t}) => {
  if (t < OUTRO_START - 0.05) return null;
  return (
    <AbsoluteFill>
      <Headline t={t} out={T.founders - 0.42} y={176} size={80} lines={[{text: 'Todo lo que funciona se queda.', t: T.todo}]} />
      <Kept t={t} />
      <Learned t={t} />
      <UICam t={t} t0={T.founders - 0.05} t1={T.tu19 - 0.4} snap="a6-picks-grid" keys={PICK_KEYS} win={[1300, 600]} top={300} />
      <Headline t={t} out={T.tu19 - 0.42} y={176} size={80} lines={[{text: 'Y lo que elegimos en BRAUD.', t: T.founders}]} />

      <Headline t={t} out={T.no - 0.42} y={540} size={118} lines={[{text: 'Tú das la dirección.', t: T.tu19}, {text: 'El sistema produce.', t: T.sistema}]} />
      <Headline t={t} out={T.instalamos - 0.4} y={540} size={118} lines={[{text: 'No es una agencia.', t: T.no}]} />
      <Headline t={t} out={T.braud - 0.42} y={540} size={84} lines={[
        {text: 'Lo instalamos con tu marca.', t: T.instalamos}, {text: 'Formamos a quien lo pilota.', t: T.formamos}, {text: 'Y se queda en tu tienda.', t: T.queda},
      ]} />
      <Wordmark t={t} />
    </AbsoluteFill>
  );
};
