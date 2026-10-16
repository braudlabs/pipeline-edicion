import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Cursor, CursorKey} from '../Cursor';
import {CamKey, Panel, UICam, Wipe} from '../Panel';
import {Module, Rect} from '../UIPlane';
import {COLORS} from '../Stage';
import {Headline, Pill} from '../system';
import {MONO, SF} from '../lib/Fonts';
import {at, ease, prog} from '../lib/motion';
import {EDIT_END} from './Edit';

// Bloques 14–17 · V06. La conexión con Meta no existe en el frontal v0.7 (el Taller dice «Conexión
// pendiente»): el estado «Conectado», la subida y el mensaje del agente son RECREACIÓN, anotada en
// DATOS-DEMO.md. Lo demás es real: el Administrador de anuncios (capturas de las campañas de BRAUD),
// sus cifras de hook y hold (crm-braud/dist/ecom/resultados.html), «Usar apertura» y su aviso.

const T = {
  agente: at(14, 'agente'), meta: at(14, 'Meta'), lee: at(14, 'Lee'), cada: at(14, 'cada'), interpreta: at(14, 'interpreta'), buyer: at(14, 'buyer'),
  este: at(15, 'Este'), pero: at(15, 'Pero'), propongo: at(15, 'Te'),
  boton: at(16, 'botón'), y16: at(16, 'Y'), nueva: at(16, 'nueva'), sube: at(16, 'sube'), cuenta: at(16, 'cuenta'),
  datos: at(17, 'Datos'), hipotesis: at(17, 'Hipótesis'), siguiente: at(17, 'Siguiente'), sin: at(17, 'Sin'), empezar: at(17, 'empezar'),
};
export const META_START = EDIT_END;
export const META_END = at(18, 'Todo');

// ---------- bloque 14 · conectado, lee, interpreta ----------
const B14_OUT = T.este - 0.3;
/** Barrido de lectura sobre las filas reales del Administrador de anuncios. */
const Reading: React.FC<{t: number}> = ({t}) => {
  const k = prog(t, T.lee - 0.05, T.interpreta - 0.1, ease.inOut);
  if (k <= 0 || k >= 1) return null;
  return <div style={{position: 'absolute', left: -120 + k * 1300, top: 44, width: 120, height: 96,
    background: 'linear-gradient(90deg, rgba(54,125,255,0), rgba(54,125,255,0.16), rgba(54,125,255,0))'}} />;
};
/** La lectura del agente, con las cifras reales de cada campaña. */
const METRICS = [
  {name: 'LATAM · Masterclass IA', hook: '52,9 %', hold: '34,7 %', cpl: '0,30 €'},
  {name: 'España · Masterclass IA', hook: '47,4 %', hold: '28,6 %', cpl: '1,86 €'},
];
const Reads: React.FC<{t: number}> = ({t}) => {
  const t0 = T.interpreta - 0.1;
  if (t < t0 || t > B14_OUT + 0.35) return null;
  const o = prog(t, B14_OUT, B14_OUT + 0.32, ease.in);
  return (
    <>
      {METRICS.map((m, i) => {
        const k = prog(t, t0 + i * 0.12, t0 + 0.55 + i * 0.12, ease.out);
        const x = 960 + (i === 0 ? -1 : 1) * 318 - 300;
        return (
          <div key={m.name} style={{position: 'absolute', left: x, top: 628 + (1 - k) * 50 - o * 50, width: 600, height: 230, borderRadius: 24, opacity: k * (1 - o),
            background: 'linear-gradient(180deg, #1d1e23, #16171b)', boxShadow: '0 30px 80px rgba(0,0,0,0.6), inset 0 0 0 1px rgba(255,255,255,0.09)', padding: '26px 32px'}}>
            <div style={{fontFamily: MONO, fontSize: 15, letterSpacing: '0.2em', textTransform: 'uppercase', color: COLORS.gray}}>{m.name}</div>
            <div style={{display: 'flex', gap: 38, marginTop: 26}}>
              {[['Hook rate', m.hook], ['Hold rate', m.hold], ['Por registro', m.cpl]].map(([l, v]) => (
                <div key={l}>
                  <div style={{fontFamily: SF, fontWeight: 600, fontSize: 46, letterSpacing: '-0.03em', whiteSpace: 'nowrap', color: l === 'Hook rate' && i === 1 ? COLORS.coral : COLORS.ink}}>{v}</div>
                  <div style={{fontFamily: MONO, fontSize: 13, letterSpacing: '0.18em', textTransform: 'uppercase', color: COLORS.dim, marginTop: 8}}>{l}</div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </>
  );
};

// ---------- bloque 15 · el mensaje del agente ----------
// Recorte del mensaje nuevo (m3) en la conversación real; las tres líneas llegan en dos tiempos.
const MSG: Rect = {x: 366, y: 486, w: 780, h: 128};
const MSG_LINES = [{x: 378, y: 511, w: 760, h: 26}, {x: 378, y: 547, w: 760, h: 26}, {x: 378, y: 585, w: 760, h: 26}];
const MsgModule: React.FC<{t: number}> = ({t}) => {
  const k = [prog(t, T.este - 0.05, T.este + 0.45, ease.out), prog(t, T.propongo - 0.12, T.propongo + 0.3, ease.out), prog(t, T.propongo + 0.12, T.propongo + 0.6, ease.out)];
  return (
    <Panel t={t} t0={T.este - 0.15} t1={T.boton - 0.45} snap="a6-agente-meta" crop={MSG} s={1.9} top={420}>
      {MSG_LINES.map((r, i) => <Wipe key={i} r={r} k={k[i]} color="#111214" />)}
    </Panel>
  );
};

// ---------- bloque 16 · un botón: la nueva apertura, la versión y la subida ----------
const OPEN_ZOOM: CamKey[] = [
  [T.boton - 0.45, 535, 300, 1.6],
  [T.boton - 0.1, 535, 300, 1.62],
  [T.y16 + 0.4, 535, 244, 1.2],
  [T.sube - 0.35, 535, 244, 1.21],
];
const CLICK = T.boton - 0.02;
const OpeningsApply: React.FC<{t: number}> = ({t}) => (
  <UICam t={t} t0={T.boton - 0.45} t1={T.sube - 0.35} snap={t < CLICK + 0.04 ? 'a6-guion-openings' : 'a6-guion-uso02-openings'} keys={OPEN_ZOOM} win={[1300, 590]} top={310} />
);
const ApplyCursor = (): CursorKey[] => [
  {t: T.boton - 0.6, x: 1560, y: 1150},
  {t: CLICK - 0.06, x: 960 + (640 - 535) * 1.62, y: 310 + 295 + (388 - 300) * 1.62}, {t: CLICK, x: 960 + (640 - 535) * 1.62, y: 310 + 295 + (388 - 300) * 1.62, click: true},
];
const Toast: React.FC<{t: number}> = ({t}) => {
  const t0 = CLICK + 0.15, out = T.sube - 0.4;
  if (t < t0 || t > out + 0.32) return null;
  const k = prog(t, t0, t0 + 0.4, ease.out), o = prog(t, out, out + 0.3, ease.in);
  const s = 1.5;
  return <Module snap="a6-guion-uso02" crop={{x: 582, y: 844, w: 347, h: 46}} cx={960} cy={950} s={s} dy={(1 - k) * 24 - o * 40} opacity={k * (1 - o)} radius={23 * s} edge={false} />;
};
const Uploaded: React.FC<{t: number}> = ({t}) => (
  <Panel t={t} t0={T.sube - 0.12} t1={T.datos - 0.32} snap="a6-taller-subida-meta" s={1.25} top={470} edge={false} radius={22 * 1.25} />
);

// ---------- bloque 17 · el bucle ----------
export const Meta: React.FC<{t: number}> = ({t}) => {
  if (t < META_START - 0.05 || t > META_END + 0.5) return null;
  return (
    <AbsoluteFill>
      <Pill t={t} t0={T.agente} out={B14_OUT} parts={['Meta Ads', 'Conectado']} y={226} />
      <Headline t={t} out={T.lee - 0.42} y={150} size={72} lines={[{text: 'Conectado a tu Ads Manager.', t: T.agente + 0.05}]} />
      <Headline t={t} out={T.interpreta - 0.42} y={150} size={72} lines={[{text: 'Lee cada anuncio.', t: T.lee}]} />
      <Headline t={t} out={B14_OUT - 0.1} y={150} size={72} lines={[{text: 'Como tu media buyer.', t: T.interpreta - 0.02}]} />
      <Panel t={t} t0={T.agente + 0.15} t1={B14_OUT} snap="meta-campanas" s={1.15} top={330} edge={false} radius={14}>
        <Reading t={t} />
      </Panel>
      <Reads t={t} />

      <MsgModule t={t} />
      <Pill t={t} t0={T.este - 0.1} out={T.boton - 0.45} parts={['Agente', 'Andrómeda pide más.']} y={226} />

      <OpeningsApply t={t} />
      <Cursor t={t} keys={ApplyCursor()} size={44} hideAfter={CLICK + 0.4} />
      <Toast t={t} />
      <Headline t={t} out={T.y16 - 0.42} y={176} size={80} lines={[{text: 'Un botón.', t: T.boton - 0.3}]} />
      <Headline t={t} out={T.sube - 0.45} y={176} size={80} lines={[{text: 'Nueva versión, con ese hook.', t: T.y16}]} />
      <Uploaded t={t} />
      <Headline t={t} out={T.datos - 0.4} y={176} size={80} lines={[{text: 'Y la sube a tu cuenta.', t: T.sube - 0.12}]} />

      <Headline t={t} out={T.sin - 0.42} y={540} size={112} lines={[{text: 'Datos.', t: T.datos}, {text: 'Hipótesis.', t: T.hipotesis}, {text: 'Siguiente versión.', t: T.siguiente}]} />
      <Headline t={t} out={META_END - 0.4} y={540} size={112} lines={[{text: 'Sin volver a empezar.', t: T.sin}]} />
    </AbsoluteFill>
  );
};

